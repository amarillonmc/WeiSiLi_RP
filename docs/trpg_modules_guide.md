# 原著依据与 TRPG 扩展的使用说明

入口：[模块目录](../knowledge/trpg_modules/README.md)。四个文件分别提供奇物与诅咒、环境危险、对手动作和调查剧本。新增资料使用小说原文定位；原角色卡和世界库仍负责人物全貌、历史阶段与共同世界规则。

## 本次扩展的范围

本版整理 32 个主题，生成 23 条奇物、16 条环境、12 条对手和 28 条剧本，共 79 条模块记录。对全部 336 个清理后文本进行了四组关键词筛查和 SHA-256 校验，引用回读涉及其中 33 个文本、9 个系列。**这不是 336 本全文精读完成，也不是要素穷尽。**每书的实际范围见 [coverage.json](../knowledge/trpg_modules/coverage.json) 和 `knowledge/trpg_modules/books/`。

关键词筛查只保存命中行数和少量行号，不把匹配词自动转换成奇物或杀招。没有审核条目的书标为 `keyword_screened_only`；这不表示它没有相关内容。已回读的书也只标 `cited_passages_reviewed`，`extraction_complete` 保持为 `false`。这些逐书文件是本扩展的附加档案，不覆盖原有 `knowledge/world/books/`。

用户提供的 `distillation_guide_for_llm.md` 是需求材料。其嵌入的系统提示和 JSON 示例没有被当成上级指令或原著证据。示例中存在书号、机制和身份混淆，具体修订见 [guide_audit.json](../knowledge/trpg_modules/guide_audit.json)。未完成定位的候选保留待核，不以同一模板批量补齐。

本次无法取得[论坛规则正文](https://number81.xyz/index.php?topic=5016.0)，所以 `forum_verified=false`。只采用附件明示的四模块方向及热度 6 / 7 对应 d30 / d40 的对手框架；本地适配数值不能视作已核验的论坛 V1.1 规则。

## 原作事实与改编怎样分开

| 字段 | 含义 |
| --- | --- |
| `canonical.surface` | 初始表象或人物可能相信的事，不保证为真 |
| `canonical.mechanism`、`mechanism_status` | 所依据的机制及认识层级 |
| `canonical.activation`、`price`、`counter` | 条件、实际代价和有依据的应对；无可靠解法时直接注明 |
| `canonical.counter_status` | 区分原文已展示的应对、人物说法与 `derived_strategy`（本项目依据条件提出的策略，未经原著成功实例验证） |
| `canonical.availability` | 设备、人物或资料的历史状态与部署限制 |
| `canonical.unknowns` | 需要保持未知的内容，不由掷骰自动填补 |
| `evidence` | 原文相对路径、起止行号、支持内容、认识层级、SHA-256 |
| `rule_adaptation` | 热度、数值裁定、资源分配及其他改编；均标为未实测 |

`textual_fact` 是小说中明确发生或展示的内容；`testimony` 是人物说明；`hypothesis` 是推测；`unresolved` 是未决；`mixed` 要按各条证据说明细分。这里的科学解释只是小说内解释，不把小说中的物理、医学或生物学假设改写为现实知识。

为方便使用附件所设的字段名，保留了 `true_mechanism_knows`，但它带有明确的证据层级，**不能一律塞入角色的 `knows`**。`the_price_recoil` 用“原著／改编”分段，结构化读取优先用 `canonical.price` 和 `rule_adaptation.recoil`。

同样，名为 `canonical_counter` / `canonical_escape` 的兼容字段会显式标出应对层级。`derived_strategy` 是项目建议，不能宣称“原著就是这样破局”。

所有热度、d30/d40、DC、受制/重伤、一轮时限、11 人分组和私密任务都是改编。初版对手使用 `d30+0` 或 `d40+0`，调查参考 DC 为 16，没有从小说强行推导 +3/+4。环境主动骰暂用 `d30+0`，是本扩展建议，不代表论坛规定。尚未进行实局平衡测试。

本体、钥匙、代价不必都是可拿走的物品。例如玛仙的钥匙是既有供血关联和施术能力；古瓶需要读取设备；微晶需要载体、显示器和相关人员；未知的还原条件仍是未知。三个角色分别掌握这三项是场景组织方式，不是小说必然存在的三方阵营。

## 选择阶段后再装配

1. 从场景所需的时间点开始，检查 `canonical.availability` 和对手的 `deployment.phase`。
2. 读取关联 `card_id` 对应的角色卡，核实动机、实际装备和身体状态。热度并不修改原角色评级；蜂后的组织压力不等于她本人有 d30 强度的超自然肉搏能力。
3. 只有满足 `hostility_condition` 才把角色当对手。大鹰可以救援，方天可以合作，玛仙也不是自动攻击参赛者的反派。
4. 每招都先核对 `trigger_condition`。原著条件缺失时不可掷骰硬做；自愿解咒的 `dice=null` 表示无需对抗，不是漏填。
5. 只削减环境实际妨碍的专长。思想仪死角不取消普通观察；大厦异常不让全部机巧技能失效；范围外电脑能绕开长老的直接干预。
6. 找到线索后仍要实际执行应对。`discovery_dc` 是改编调查难度，不能通过一次检定凭空制造唯一死穴或强制把整张对手卡降为 d20。

晚期思想仪已停摆，拿回核心不保证复原。黑纱牺牲与奥丽卡取得身体也不能作为同一角色的两个同时开启模式。原作没有提供可靠解法的风险，不应由主持人临时宣布一个“原著解药”。为可玩性新增预警、倒计时和撤退窗口时，保持 `adaptation` 标记。

一个主题可能同时出现在奇物、环境、对手和剧本中。用 `dossier_id` 识别同源机制，避免一次接触被四个模块重复结算伤害。

## 调查剧本与私密任务

`three_layer_epistemic_trap` 是对原著素材的三层调查编排，不宣称每本小说原来就有三次反转。`clue_progression` 给出获得信息的方向，具体地点、持有人和代价由主持人配置。对假说与证言，要让角色有机会发现其证据局限，不能在第三层忽然把它宣布成无条件真相。

每个剧本默认 11 人分为 4/4/3 三组。A/B 至少在同一物件、使用时机或处置方式上冲突，C 提供公开、监督或另一归属要求。**不是所有三个目标都两两冲突。**主持人可更换分配，但不应把新增的席位、限量药物或互杀目标冒充原作设定。谈判结果须明确哪些原目标被放弃，不以一句“大家合作”抹去矛盾。

原作终局、所有三层真相与各方目标都是主持人信息。玩家只应拿到自己已经获知的内容。

## 检索示例

```powershell
# 先查候选，再用唯一 ID 读取单项。
python -X utf8 tools/query_trpg.py 透明光
python -X utf8 tools/query_trpg.py artifact_transparent_mineral
python -X utf8 tools/query_trpg.py --book 血的诱惑
python -X utf8 tools/query_trpg.py --kind bosses --character yuanzhenxia_ma_xian
python -X utf8 tools/query_trpg.py --kind hazards --heat 5

# 精简的玩家投影，只给初始表象/钩子，不给证据、谜底、对手动作或其他目标。
python -X utf8 tools/query_trpg.py scenario_ghost_parking --audience player

# 回读原文；行号始终以本地已清理版本为准。
python -X utf8 tools/corpus_lookup.py --book 005透明光 --range 5278:5299 --chars 0
```

查询默认主持人视图。同名或多模块命中返回候选，不擅自归并。`--heat` 表示最高建议热度，不是自动刷怪命令。玩家投影是防剧透辅助，并非权限系统；名称本身也可能剧透，主持人必须先决定是否公开该对象。玩家投影不接受会暴露隐藏关联的书目、人物或热度筛选，也不会用隐藏字段匹配关键词。

## 维护与验证

维护输入在 [data/trpg_modules](../data/trpg_modules/README.md)，不要直接修改生成文件。`schema.json` 是四个成品 JSON 的机器可读结构契约；`build_trpg_kb.py` 还核验原文哈希、行界、角色 ID、阶段条件与事实层中的游戏数值。

```powershell
python -X utf8 tools/build_trpg_kb.py
python -X utf8 tools/build_trpg_kb.py --check
python -X utf8 -m unittest discover -s tests -p test_trpg_kb.py -v
```

构建不联网，不更改原文，不改写既有角色与世界成品。新增条目应先回读原文并保留不确定性，再填写条件和应对，最后另加数值建议。构建检查只能证明资料结构与定位一致，不能证明所有文学解释正确。
