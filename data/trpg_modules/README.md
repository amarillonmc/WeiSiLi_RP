# TRPG 扩展的维护输入

- `dossiers.json`：32 个手工整理主题及对应奇物、环境、对手、剧本方案。不是关键词自动提取的结果。
- `policy.json`：来源、认识层级、数值改编和论坛兼容性边界。
- `guide_audit.json`：对附件示例的修订与尚未完成的候选定位。
- `schema.json`：四个成品 JSON 的结构契约。

使用 [build_trpg_kb.py](../../tools/build_trpg_kb.py) 生成 `knowledge/trpg_modules/`。添加主题时，给每个源文本添加有支持说明的行号；原文事实用 `canonical`，数值建议用各模块配置。对手必须使用已有角色 ID，并说明阶段和敌对条件。剧本的三层编排、线索顺序和三组任务均为改编。

`source_books` 中每一文本都须有引用；被引用不代表全文通读。全书检索结果只作筛查记录。正文更改导致 SHA-256 变化时，应回读受影响引用，不能只更新哈希以绕过检查。

结构检查与生成一致性：`python -X utf8 tools/build_trpg_kb.py --check`。阅读与装配见 [使用说明](../../docs/trpg_modules_guide.md)。
