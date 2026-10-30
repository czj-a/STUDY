# STUDY — Personal skills for Codex cloud tasks

本仓库收录从个人本地安装目录迁移的技能快照（2026-10-30）。在 Codex 云端选择 **czj-a/STUDY / main** 发起新任务，技能位于仓库级 `.agents/skills/`。

## 安装范围

- 33 个顶层技能包，包含 41 个 `SKILL.md` 入口（其中 8 个是专利子技能）。
- 附带 `shared-references`、`nature-shared`、脚本、模板、图片等原包资源及许可证；实际文件以清单为准。
- 原有技能及脚本逐字节复制，没有改写功能代码。系统技能、插件缓存、真实 `.env`、凭据文件及 Python 缓存未迁移。
- `nature-proposal-writer` 的调用名是 `researchwrite`，沿用原包设置。
- 这是仓库范围的安装，不会自动成为其他云端仓库或整个账户的全局技能。

## 开始使用

在新的云端任务中输入：

> 请先读取 AGENTS.md 和 skill-inventory.json，确认能够读取本仓库的技能。然后使用 $paper-quick-scan 分析我提供的论文。

也可指定 `$nature-writing`、`$nature-figure`、`$ppt-master`、`$patent-disclosure-skill` 等。嵌套的专利子技能保留在完整原包内；如果当前运行器未在选择器显示子技能，按清单中的路径读取对应 `SKILL.md`。

## 云端依赖与适用边界

技能文件可被发现，不等于所有外部工具和账户已配置。纯文本工作流可直接读取执行；脚本工作流需要按对应包的说明安装依赖。

| 场景 | 云端要求 |
| --- | --- |
| Python 脚本、PDF、Word、PPT 和绘图 | 按具体任务安装该技能的 `requirements.txt`；部分流程还需要 LibreOffice、Poppler、Pandoc、中文字体或 R。不要无差别运行所有安装脚本。 |
| 文献检索与下载 | 配置任务所需网络访问；出版社 API、机构订阅、CNKI 登录需要单独授权。 |
| 本机 Chrome、Zotero、Obsidian | 云端不能读取本地电脑会话或磁盘。应上传任务材料或配置云端可访问的连接；`localhost` 指云端容器。 |
| 图像生成、飞书、定时任务、MCP | 只有实际提供相关工具或连接时才能使用；复制技能不创建这些连接。 |
| Windows / macOS 示例命令 | 使用云端 Linux 可用的等价命令；若需要修改原脚本，先获得用户明确的代码修改请求。 |

所有发现的依赖清单位于 `skill-inventory.json` 的 `requirements_files` 字段。可在 Codex 的环境设置中，按计划使用的技能配置安装命令。例如，仅需专利文档时：

```bash
# Install the original patent package dependencies for this environment.
python -m pip install -r .agents/skills/patent-disclosure-skill/requirements.txt
```

环境初始化脚本可联网安装依赖；任务阶段的网络权限另行配置。敏感凭据不应提交到本公开仓库；环境 secrets 的可用阶段须遵循 Codex 官方说明。

## 验证状态

迁移时检查技能入口、重复名称、常见凭据特征，以及复制前后的 SHA-256 一致性。未执行原包安装脚本或所有功能测试，也未运行用户账户的 Codex 云端任务；本仓库不声称已连接外部账户或完成全功能云端验收。

## 技能清单

- [grill-me](.agents/skills/grill-me/SKILL.md)
- [grilling](.agents/skills/grilling/SKILL.md)
- [nature-academic-search](.agents/skills/nature-academic-search/SKILL.md)
- [nature-citation](.agents/skills/nature-citation/SKILL.md)
- [nature-data](.agents/skills/nature-data/SKILL.md)
- [nature-downloader](.agents/skills/nature-downloader/SKILL.md)
- [nature-experiment-log](.agents/skills/nature-experiment-log/SKILL.md)
- [nature-figure](.agents/skills/nature-figure/SKILL.md)
- [nature-image2ppt](.agents/skills/nature-image2ppt/SKILL.md)
- [nature-literature-pipeline](.agents/skills/nature-literature-pipeline/SKILL.md)
- [nature-paper-card](.agents/skills/nature-paper-card/SKILL.md)
- [nature-paper-to-patent](.agents/skills/nature-paper-to-patent/SKILL.md)
- [nature-paper-trans](.agents/skills/nature-paper-trans/SKILL.md)
- [nature-paper-xray](.agents/skills/nature-paper-xray/SKILL.md)
- [nature-paper2ppt](.agents/skills/nature-paper2ppt/SKILL.md)
- [nature-polishing](.agents/skills/nature-polishing/SKILL.md)
- [researchwrite](.agents/skills/nature-proposal-writer/SKILL.md)
- [nature-reader](.agents/skills/nature-reader/SKILL.md)
- [nature-ref-verifier](.agents/skills/nature-ref-verifier/SKILL.md)
- [nature-response](.agents/skills/nature-response/SKILL.md)
- [nature-reviewer](.agents/skills/nature-reviewer/SKILL.md)
- [nature-shared](.agents/skills/nature-shared/SKILL.md)
- [nature-social-science](.agents/skills/nature-social-science/SKILL.md)
- [nature-statistics](.agents/skills/nature-statistics/SKILL.md)
- [nature-writing](.agents/skills/nature-writing/SKILL.md)
- [ppt-master](.agents/skills/ppt-master/SKILL.md)
- [find-skills](.agents/skills/find-skills/SKILL.md)
- [paper-critical-analysis](.agents/skills/paper-critical-analysis/SKILL.md)
- [paper-deep-read](.agents/skills/paper-deep-read/SKILL.md)
- [paper-quick-scan](.agents/skills/paper-quick-scan/SKILL.md)
- [patent-disclosure-skill](.agents/skills/patent-disclosure-skill/SKILL.md)
- [patent-application](.agents/skills/patent-disclosure-skill/skills/patent-application/SKILL.md)
- [patent-disclosure](.agents/skills/patent-disclosure-skill/skills/patent-disclosure/SKILL.md)
- [patent-docket](.agents/skills/patent-disclosure-skill/skills/patent-docket/SKILL.md)
- [patent-exam-policy](.agents/skills/patent-disclosure-skill/skills/patent-exam-policy/SKILL.md)
- [patent-map](.agents/skills/patent-disclosure-skill/skills/patent-map/SKILL.md)
- [patent-oa](.agents/skills/patent-disclosure-skill/skills/patent-oa/SKILL.md)
- [patent-reader](.agents/skills/patent-disclosure-skill/skills/patent-reader/SKILL.md)
- [patent-search](.agents/skills/patent-disclosure-skill/skills/patent-search/SKILL.md)
- [patent-novelty-check](.agents/skills/patent-novelty-check/SKILL.md)
- [prior-art-search](.agents/skills/prior-art-search/SKILL.md)

## 来源与许可

来源是用户个人安装的技能目录，不包括系统/插件技能。各包的作者、上游链接及许可证保持原样；本仓库不为第三方材料授予额外许可。

## 官方配置参考

- [技能发现与仓库目录](https://learn.chatgpt.com/docs/build-skills)
- [Codex 云端环境与初始化](https://learn.chatgpt.com/docs/environments/cloud-environment)
