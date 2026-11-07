"""Local typesetting for paper translation. JSON is UTF-8, coordinates are PDF points."""
import argparse
import html
import json
import math
import re
from contextlib import ExitStack
from pathlib import Path
from statistics import median
from tempfile import NamedTemporaryFile

import fitz
from pages import (A4_PAGE_SIZE_POINTS, _publish_without_replace, check_assets,
                   digest, load, locked, overview, require, selected_pages)


def read_blocks(page):
    data = {}
    for block in page.get_text("dict", flags=fitz.TEXTFLAGS_DICT & ~fitz.TEXT_PRESERVE_IMAGES)["blocks"]:
        lines = block.get("lines", [])
        if not lines:
            continue
        spans = [span for line in lines for span in line["spans"] if span["text"].strip()]
        if not spans:
            continue
        key = str(block["number"])
        data[key] = {
            "source": "\n".join("".join(s["text"] for s in line["spans"]) for line in lines),
            "bbox": list(block["bbox"]), "size": median(s["size"] for s in spans),
            "spans": [list(span["bbox"]) for span in spans],
        }
    return data


def template(path, page, number, fingerprint):
    blocks = read_blocks(page)
    record = {"sha256": fingerprint, "page": number, "blocks": {
        k: {"source": b["source"], "translation": ""} for k, b in blocks.items()
    }, "regions": []}
    if path.exists():
        old = json.loads(path.read_text(encoding="utf-8-sig"))
        require(old["sha256"] == fingerprint and old["page"] == number, f"Wrong existing template: {path}")
        return
    with path.open("x", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)


def validate_rect(coords, bounds):
    rect = fitz.Rect(coords)
    require(all(math.isfinite(v) for v in rect) and not rect.is_empty and bounds.contains(rect),
            f"Rectangle outside page: {rect}")
    return rect


def local_page(page, path, number, fingerprint, dpi, selectable=False):
    record = json.loads(path.read_text(encoding="utf-8-sig"))
    require(record["sha256"] == fingerprint and record["page"] == number, f"Wrong translation file: {path}")
    blocks = read_blocks(page)
    require(blocks.keys() == record["blocks"].keys(), f"Block keys differ on page {number}")
    rotation = page.rotation
    page.set_rotation(0)
    bounds = page.rect
    replacements = []
    for key, block in blocks.items():
        entry = record["blocks"][key]
        require(entry["source"] == block["source"], f"Source mismatch: page {number}, block {key}")
        value = entry["translation"]
        if value is None:  # explicitly preserved equation, reference, identifier, etc.
            continue
        require(isinstance(value, str) and value.strip(), f"Missing translation: page {number}, block {key}")
        rect = validate_rect(entry.get("bbox", block["bbox"]), bounds)
        # Superscripts and subscripts can fall outside the parent line's midline.
        for coords in block["spans"]:
            span = fitz.Rect(coords)
            mid = (span.y0 + span.y1) / 2
            page.add_redact_annot((span.x0, mid - 0.08, span.x1, mid + 0.08), fill=False)
        replacements.append((rect, value, block["size"], key))
    if selectable:
        # The visible paint used for translated labels would leave selectable English
        # underneath. Remove those covered text glyphs while retaining vector artwork.
        for item in record["regions"]:
            r = validate_rect(item["bbox"], bounds)
            page.add_redact_annot(r, fill=False)
    if replacements or (selectable and record["regions"]):
        page.apply_redactions(images=0, graphics=0, text=0)
    for idx, item in enumerate(record["regions"]):
        # Explicitly identified raster text, never erase a whole figure automatically.
        rect = validate_rect(item["bbox"], bounds)
        value = item["translation"]
        require(isinstance(value, str) and value.strip(), f"Missing region translation on page {number}")
        page.draw_rect(rect, color=None, fill=item.get("background", (1, 1, 1)), overlay=True)
        replacements.append((rect, value, float(item["size"]), f"region {idx}"))
    require(replacements or record.get("preserve_page") is True,
            f"Page {number} has no translated text; supply regions or explicitly preserve a non-prose page")
    for rect, value, size, key in replacements:
        require(math.isfinite(size) and size > 0, "Invalid font size")
        paragraph = rect.height > 4 * size and len(value) > 60
        font_size = size * 1.18 if paragraph else size
        leading = 1.32 if paragraph else 1.05
        style = f"* {{font-family:sans-serif; margin:0; padding:0; font-size:{font_size:.2f}pt; line-height:{leading}}}"
        box = html.escape(value).replace("\n", "<br/>")
        remaining, scale = page.insert_htmlbox(rect, box, css=style, scale_low=0.62)
        require(remaining >= 0, f"Text overflow: page {number}, block {key}; adjust translation or bbox")
    page.set_rotation(rotation)
    if not selectable:
        return page.get_pixmap(dpi=dpi, alpha=False).tobytes("png")


def recorded_images(work, fingerprint, numbers):
    if not work:
        return {}
    work = work.resolve()
    with locked(work):
        task = load(work)
        require(task["source"]["sha256"] == fingerprint, "Image job belongs to another PDF")
        status = overview(work, task)
        require(not status["in_flight"], "Resolve pending image calls before publishing")
        check_assets(work, task, allow_pending_missing=True)
        for p in status["pages"]:
            if p["page"] not in numbers:
                continue
            require(not any(a.get("recoverable_output") for a in p["attempt_records"]),
                    f"Record the recovered image for page {p['page']} before merging")
            require(p["state"] != "recorded" or p["selection_confirmed"],
                    f"Select an image for page {p['page']} before merging")
        return {p["page"]: Path(p["output"]) for p in status["pages"]
                if p["page"] in numbers and p["state"] == "recorded" and p["selection_confirmed"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["extract", "build"])
    parser.add_argument("--pdf", required=True, type=Path)
    parser.add_argument("--pages", default="all")
    parser.add_argument("--dir", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--work-dir", type=Path)
    parser.add_argument("--dpi", type=int, default=200)
    parser.add_argument("--a4", action="store_true")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--selectable", dest="selectable", action="store_true", help="Keep selectable text (default)")
    mode.add_argument("--image-only", dest="selectable", action="store_false", help="Explicitly request flattened image pages")
    parser.set_defaults(selectable=True)
    args = parser.parse_args()
    fingerprint = digest(args.pdf)
    with fitz.open(args.pdf) as src:
        require(src.is_pdf and not src.needs_pass, "An unlocked PDF is required")
        numbers = selected_pages(args.pages, len(src))
        def page_file(n):
            return args.dir / f"page-{n:04d}.json"
        if args.action == "extract":
            args.dir.mkdir(parents=True, exist_ok=True)
            for n in numbers:
                template(page_file(n), src[n-1], n, fingerprint)
            return
        out = args.output
        require(out and not out.exists(), "Specify a new output path")
        require(72 <= args.dpi <= 600, "DPI must be between 72 and 600")
        images = {} if args.selectable else recorded_images(args.work_dir, fingerprint, numbers)
        out.parent.mkdir(parents=True, exist_ok=True)
        with ExitStack() as cleanup, fitz.open() as result:
            # Stage beside the destination to inherit its directory's Windows ACL.
            with NamedTemporaryFile(dir=out.parent, suffix=".pdf", delete=False) as temp:
                staged = Path(temp.name)
            cleanup.callback(staged.unlink, missing_ok=True)
            sizes = []
            for n in numbers:
                page = src[n-1]
                size = A4_PAGE_SIZE_POINTS if args.a4 else (page.rect.width, page.rect.height)
                sizes.append(size)
                if args.selectable:
                    local_page(page, page_file(n), n, fingerprint, args.dpi, selectable=True)
                    if args.a4:
                        dest = result.new_page(width=size[0], height=size[1])
                        dest.show_pdf_page(dest.rect, src, n-1)
                    continue
                img = images[n].read_bytes() if n in images else local_page(page, page_file(n), n, fingerprint, args.dpi)
                dest = result.new_page(width=size[0], height=size[1])
                dest.insert_image(dest.rect, stream=img, keep_proportion=True)
            output_doc = result
            if args.selectable and not args.a4:
                if len(numbers) != len(src):
                    src.select([n-1 for n in numbers])
                output_doc = src
            if args.selectable:
                output_doc.subset_fonts()
            output_doc.save(staged, garbage=3, deflate=True)
            with fitz.open(staged) as verify:
                require(len(verify) == len(numbers), "Page count mismatch")
                for n, p, size in zip(numbers, verify, sizes):
                    require(abs(p.rect.width-size[0]) < .02 and abs(p.rect.height-size[1]) < .02, "PDF dimensions mismatch")
                    if args.selectable:
                        record = json.loads(page_file(n).read_text(encoding="utf-8-sig"))
                        actual = "".join(p.get_text().split())
                        require(actual or record.get("preserve_page"), f"Missing text layer on page {n}")
                        translations = [e["translation"] for e in record["blocks"].values()] + [r["translation"] for r in record["regions"]]
                        for value in filter(None, translations):
                            chinese = re.findall(r"[\u3400-\u9fff]+", value)
                            if chinese:
                                probe = max(chinese, key=len)[:5]
                                require(probe in actual, f"Translated text not selectable on page {n}: {probe}")
                    else:
                        require(p.get_images(), "Embedded image missing")
            _publish_without_replace(staged, out)
    print(out)


if __name__ == "__main__":
    main()
