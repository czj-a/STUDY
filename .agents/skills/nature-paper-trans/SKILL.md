---
name: nature-paper-trans
description: 将英文论文 PDF 的指定页或全文翻译为简体中文 PDF。默认保留可选择、复制和搜索的中文文字层，支持在 Zotero 中高亮、摘录和批注，尽量保留原页尺寸、分栏、图表与公式。
---

# 论文 PDF 翻译

收到 PDF 后，默认翻译全文，也可按实际页码选页。保留原页顺序、尺寸、方向、栏位、公式编号和数值；仅显式要求时使用 A4。最终交付一个中文 PDF。

## 选择生成方式

- 常规调用直接用下方的本地排版。正文、标题、图注和译出的图表标签写为 PDF 原生文字。即使源页为扫描图，也要识读内容并排入可选择的中文译文。
- 用户明确要求纯图片 PDF 时才启用 `--image-only`。此时可参见 [图像翻译流程](references/image-workflow.md) 和 [生成提示词](references/image-translation-prompt.md)。已有生图结果仅用于显式图片模式。

## 本地排版

使用 Python 3.9+、PyMuPDF 1.24.2+ 和 Pillow。所有命令中的路径需绑定实际文件；Windows PowerShell 使用 `& $python $script ...`。若源文件在聊天的文件区，先取得可读取的 PDF 原件。任务中间文件放在单独工作目录。下文 SCRIPT 是技能的 `scripts/local_pdf.py`。

用同一解释器先执行 `python -c "import fitz; from PIL import Image"`。如依赖缺失，使用工作区内的虚拟环境或 `python -m pip install --target <任务依赖目录> -r <技能目录>/requirements.txt`，并为后续命令设置对应的 PYTHONPATH。不要把基础环境缺少 PyMuPDF 误判为 PDF 无法处理。

1. 执行 `python SCRIPT extract --pdf SOURCE --pages all --dir TRANSLATIONS`。选页可用 `1-3,5`。脚本按源文件指纹和真实物理页号生成 UTF-8 JSON，续跑保留已有译文。读取原页和 JSON，遵循分栏阅读顺序、上下文与公式编号。
2. 逐页填写每个块的 `translation`。保留 `source` 和键。正文、标题、图注和表头须译为中文，不摘要、不遗漏；数字、单位、公式和变量保持原意。仅对无需替换的标识、公式、参考文献的原始著录等显式设为 JSON `null`。未填写的空字符串会阻止交付。按需用换行表示原有条目，明确可用时可在块中指定 `bbox` 排版范围。多栏或公式混合块特别注意来源，避免压住邻区。
3. 对扫描页、嵌在图像中的英文标签或缺少文本层的区域，先查看源页图，再于 `regions` 填入 `{"bbox":[x0,y0,x1,y1],"translation":"中文","size":8}`。坐标以未旋转源页左上角为原点，单位为 PDF 点。背景默认白色，有色底可填 `background`（三个 0 到 1 的 RGB 值）。仅遮盖原文字，保留图例线、数据点和曲线。整页确属无需翻译的纯图或书目页，才可显式设 `preserve_page:true`；扫描正文不能用此标志跳过。
4. 执行 `python SCRIPT build --pdf SOURCE --pages all --dir TRANSLATIONS --output NEW.pdf`。默认生成可批注 PDF，无需指定参数。仅在用户要求统一 A4 时加 `--a4`。输出路径必须是新路径。脚本逐页验证尺寸和文本可提取性，再发布成品。
5. 从成品的中文正文及图注抽取片段，核对选区位置，并在临时副本中测试高亮保存后可重开。最终交付干净的 PDF。若用户明确要求部分翻译，在交付时标明实际页码。
