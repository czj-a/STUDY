# 可读取源图时的逐页图像翻译
仅在用户明确要求纯图片 PDF 时使用此流程。常规论文翻译及 Zotero 阅读任务使用主说明中的文字层输出。
原页尺寸、方向、图表和公式优先；生图每页最多一次。仅向内置 image_gen 提交已验证能被其读取的源图片路径。并发上限为 10，遇到路径或服务故障即停止提交新页并切换本地排版。
1. 用 `python scripts/pages.py prepare --pdf SOURCE --pages all --work-dir JOB` 准备源页并执行 `status --work-dir JOB`。将 references/image-translation-prompt.md 复制到 JOB/generation-prompt.md。
2. 检查本页源图。执行 `reserve --work-dir JOB --page N --purpose initial --prompt-file PROMPT`。立即用同一提示词和当前源图提交，绑定 attempt_id。路径必须指向同一张源图；不要猜测其他系统上的挂载位置。
3. 得到图片后执行 `record --work-dir JOB --page N --attempt-id ID --image IMAGE`。结果未定则等待；确认无图后执行 `fail --work-dir JOB --page N --attempt-id ID --reason REASON`。不要重设账本或增加生图次数。
4. 全部成功按原流程执行 `assemble --work-dir JOB --output NEW.pdf --pdf-only`，用户要求 A4 时才附加 `--a4`。对失败页或未提交页按 SKILL.md 填写本地译文，使用 `local_pdf.py build ... --image-only --work-dir JOB` 合并原有成功页和本地排版页。正常全文任务只在全部所选页就绪时交付。
