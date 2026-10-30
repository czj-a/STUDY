# STUDY cloud skill guidance

## User instructions

- 在用户提出明确“修改代码”之前，不修改用户的现有代码。安装技能不等于授权重写技能脚本。
- 开始具体任务前，询问影响执行的关键不确定点；已经明确的信息不重复询问。以可验证事实说明判断和限制。
- 中间文件放入任务目录下的 `.codexfile/`；最终答复说明生成的中间文件和目标文件位置。没有生成文件则无需说明。
- 经授权新增的功能代码应包含简单注释。

## Skills

Skills are stored in `.agents/skills/`. Use `skill-inventory.json` as the complete index, including the nested patent skills. Read the relevant `SKILL.md` before applying a skill. Do not load every skill for every task.

Keep each package intact: Nature skills use sibling `nature-shared` resources; the standalone patent search skills use sibling `shared-references`; the patent-disclosure package has internal `skills/` paths. Resolve relative paths against the referring skill or resource directory, according to that package's instructions.

The directory `nature-proposal-writer` declares the skill name `researchwrite`. Nested patent skills remain in `.agents/skills/patent-disclosure-skill/skills/`. If the runtime selector does not expose a nested skill, read its indexed file directly when the user requests it.

## Cloud execution

The original skill packages are unmodified snapshots. Confirm required commands, libraries and tools exist before using them. Install dependencies only for the requested task and follow the package requirements. Do not treat a skill's tool names as evidence that tools or connectors are available.

Local Windows/macOS paths, local browser login sessions, Zotero, Obsidian vaults, external MCP services and API keys do not transfer with these files. Ask for missing materials or a suitable connection when necessary. Never pretend that a local connection is available in this cloud environment.

Use the current runtime's actual tools for equivalent operations. Never claim that reading a skill, installing a Python dependency, or passing a file check proves its end-to-end workflow works. Record concrete validation and any unmet dependencies.

Keep credentials, cookies, unpublished task data and generated outputs out of Git commits. Retain bundled license and attribution files.
