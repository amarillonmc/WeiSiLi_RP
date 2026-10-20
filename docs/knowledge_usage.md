# 倪匡角色知识库使用说明

本库供其他项目检索角色背景、能力和行为逻辑，使用范围为已清理的九个系列、336 个文本。每个角色或无法拆分的具名行动群体有独立角色卡和独立强度档案，使用稳定 ID 关联。

世界运行、跨书时间关系、成长阶段及关键目标另见 [世界观与 RP 使用说明](worldbuilding_guide.md)和 [世界知识库](../knowledge/world/README.md)。在原世界的历史场景中，先用 `tools/query_world.py --scene <事件ID>` 约束阶段，再取本页所述的角色资料；本库默认综合终局卡不能直接当作早期人物的记忆和身体状态。

## 文件入口

| 文件 | 用途 |
| --- | --- |
| `knowledge/index.json` | 名称、别名、系列、身份、评级摘要及单卡路径；先从这里检索 |
| `knowledge/characters/<id>.json` | 角色卡，供程序及 LLM 按需载入 |
| `knowledge/characters/<id>.md` | 同一角色的可读版本 |
| `knowledge/ratings/<id>.json` | 独立评分，包含各维度、扣分、概念门槛、实战与理论位阶 |
| `knowledge/ratings/<id>.md` | 可读评分解释 |
| `knowledge/coverage.json` | 逐书纳入角色、未单独建卡者及理由 |
| `knowledge/identity_map.json` | 跨系列身份合并依据与旧 ID 跳转 |
| `knowledge/rules.json` | 模板和评级规则、来源网址及项目解释 |
| `knowledge/manifest.json` | 条目数量、覆盖状态和语料哈希 |

`complete` 表示本次 336 个文本的覆盖清单已全部完成并通过结构检查，不表示原文本身毫无缺页，也不等于文学解释已经穷尽。已知缺页、乱码与未完文本仍见项目根目录的语料说明。

## 调用单个角色

先通过 `name_lookup` 获取候选 ID，再读取候选对应的 `card`。同一称谓可能指向多人，例如军师、首长或同姓角色，调用方应结合系列与证据选择，不要默取第一个。若保存了旧 ID，先查 `id_redirects`。路径均相对 `knowledge/`。

```python
import json
from pathlib import Path

kb = Path("knowledge")
index = json.loads((kb / "index.json").read_text(encoding="utf-8"))
ids = index["name_lookup"].get("白素", [])
if len(ids) != 1:
    raise ValueError(f"需要选择确切角色：{ids}")

entry = next(c for c in index["characters"] if c["id"] == ids[0])
character = json.loads((kb / entry["card"]).read_text(encoding="utf-8"))
# 仅在需要比较强度或裁定战斗时读取。
rating = json.loads((kb / entry["rating"]).read_text(encoding="utf-8"))
```

命令行可用 `python -X utf8 tools/query_character.py 白素`；加 `--rating` 读取评分，加 `--markdown` 输出可读版本。检索不到时返回非零状态；有多个候选时输出候选信息，需要进一步选择。

## 演绎时使用哪些字段

需要奇物机制、环境危险、对手招式或调查剧本时，另读 [TRPG 扩展说明](trpg_modules_guide.md) 与 [模块索引](../knowledge/trpg_modules/README.md)。这些成品补充角色库，保留原著证据层级；热度、骰子和秘密任务是改编，不能反写为角色原作能力。

先读取 `version`，确认最后明确状态与参战部署，再用 `logic` 和 `modes` 决定角色面对当前处境会怎样选择。`biography` 提供动机的来历，`abilities`、`baseline` 与 `weaknesses` 决定实际能做什么。`ooc` 保存最容易误写的边界，`adaptations` 标明为了演绎作出的调整。

每次只加载本场景参与者。角色不需要在对白中背诵传记或能力清单，行为扳机也不是必须顺次执行的剧本。具体动作应随关系、已知信息、现场资源及代价改变；同一原则可以通过追问、沉默、协作、拒绝或冒险表现。

完整索引供应用侧检索，不必把索引全文或所有卡片一起塞进 LLM 上下文。需要节省 Token 时，先运行检索脚本取得单卡，强度分析仅在本场景需要比较或裁定时另行读取。

总体能力与总体经历不等于读者全知。角色只能使用自己亲历、学会或被告知的信息；伙伴的技术、机构的装备、历史形态和一次性奇遇不会自动成为随身能力。失踪或死亡没有被暗中改写为原作已复活；需要恢复参战的情况，应采用卡内明确注明的部署约定。

## 覆盖和身份

系列主角、具有独立主线的单书人物、实际跨书参与的重要配角及可辨认的反派纳入角色卡。一次性辅助者、只被提及的背景人物、没有独立人格的器械，以及未证实存在的假想幕后者，在逐书覆盖表中记录判断。原文无法区分的施害群体可作为小组建卡，不能从一个小组生成无限成员或虚构每人的姓名。

同名并不自动同人。生念祖家族的不同世代分别记录；跨系列的胡怀玉、金特、水银将军则有身份关联依据。复制体、转世、冒名者和终局换形按各自证据处理，不把互斥身体与能力叠加。

## 评级与证据

评分依据[角色模板首帖](https://number81.xyz/index.php?topic=667.0)和[通用评估标准](https://number81.xyz/index.php?topic=1067.0)建立的本地规则。六项正面维度使用各自权重，再扣除自我限制、环境依赖与波动性。项目保留小数原始分数，四舍五入后分段，再应用概念门槛与掌握程度；取整办法是为衔接原帖整数分段而明确采用的项目约定。

`raw_score`、`practical_tier`、`theoretical_tier` 与最终显示标签承担不同用途，比较时不要混用。外星身份、长寿或认识强者都不能单独决定高位阶；传说、设备条件和偶发事件应连同解释读取。评分与置信度是项目分析，不能当作原作给出的精确数值。

评级随档案中的 `assessment_basis` 生效。部分条目按原作终局失能状态评分，部分死亡或被封存角色按卡内明示的恢复形态参战；调用时应读取 `deployment`，不能只比较索引中的等级。选择另一历史形态或另配设施后，原评级不自动适用。

每条 `evidence` 含相对原文路径、清理后起止行号、支持内容和证据类型。原文仍位于项目外的 `NK_Source`，没有复制进成品库。行号依赖当前清理版本；修改原文后应重新核对证据，构建工具会检查哈希并拒绝静默使用变化后的正文。

## 维护与检查

维护现成角色时，修改对应 `data/character_batches/<batch>/cards.json`，并按需要修改该批 `coverage.json`。分片和作者脚本保留整理过程，重新运行它们可能覆盖聚合数据；进行跨系列重建时，必须重新应用对应合并和终局修正，并核对差异。

```powershell
python -X utf8 tools/build_character_kb.py --check
python -X utf8 -m unittest discover -s tests -p test_character_rating.py -v
python -X utf8 tools/build_character_kb.py
```

构建会检查模板必需字段、传记长度、行为扳机、证据行界、唯一 ID、逐书覆盖、评分范围与位阶一致性。结构通过不代替逐条文学判断；新增证据应同时检查是否改变相关角色的最后状态、身份归属及装备条件。
