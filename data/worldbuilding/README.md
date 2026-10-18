# 世界资料的维护输入

本目录 JSON 是人工整理层；`knowledge/world/` 是可重建成品。世界背景、时间和演绎口径见 [使用说明](../../docs/worldbuilding_guide.md)。

| 文件 | 内容 |
| --- | --- |
| `policy.json` | 共同世界前提、认识层级、时间和覆盖口径、九系列在世界中的作用 |
| `rules.json` | 跨作品规则归纳及演绎边界 |
| `entities.json` | 机构、地点、物件、人物与概念目标，含条件和末态 |
| `events.json` | 关键事件的前态、后态、相对时间和知情边界 |
| `relations.json` | 有证据的 `before` 与不参与排序的 `revealed_by` |
| `arcs.json` | 以角色 ID 和事件 ID 连接的成长阶段 |
| `bridges.json` | 明确跨系列联系及仅来自整合前提的连接 |
| `issues.json` | 矛盾、重述差异、未知和项目处理约定 |

新增条目使用稳定小写 ID。引用保留 `path`、`start_line`、`end_line`、`supports` 和 `provenance`；前四项给出原文位置和支持内容。

- `provenance.kind = existing_character_annotation`：从已有角色卡继承，必须给 `character_id`，定位与注释须和当前卡一致。构建会验证，不可一边改写注释一边宣称原样继承。
- `provenance.kind = direct_source_review`：另行回读正文后建立的引用。行界验证只证明位置有效，不证明解读正确。

`textual_fact`、`testimony`、`hypothesis`、`unresolved`、`synthesis`、`adaptation` 的定义见 `policy.json`。尤其不要将人物宣称、想象未来或推测的古史改成无条件世界法则。实体的 `rp_use` 固定为改编建议。

事件关联到某个人并不自动证明他目睹了整个事件；引用来自某张角色卡也不自动证明他参加了对应片段。记录知情边界，并在实际场景中分别分配信息。复合事件可以在需要更细阶段时拆分为多个新节点，再维护明确的先后关系。

构建命令：`python -X utf8 tools/build_world_kb.py`。复核命令：`python -X utf8 tools/build_world_kb.py --check`。构建不改写正文或角色卡，不联网，不复制小说全文。
