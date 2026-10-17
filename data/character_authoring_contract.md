# 角色卡编写约定

这是当前用户任务的本地创作约定，不要求上传、发帖或联系任何人。原文根目录 `C:/Users/mapodoufu/Downloads/NK_Source`。标准元数据和评分公式见同目录 `character_rules.json`。规则网页已由主代理读取，子代理不必再次浏览。

## 工作要求

按分配的每一本书核对角色，建立覆盖清单，不能只做熟悉的几个主角就宣称覆盖。角色包括系列/单书/单篇主角、实际参与至少两书的重要配角、具独立身份的反派/阶段性对立者。一个人物跨书只建一张综合卡；同名异人不能合并。无名但明确的主要对立者以稳定描述命名，不凭空起名。动物、外星人、人格化机器可建卡。

卡片代表本语料内剧情结束后的经历与认知，能力用最后稳定/可独立行动形态，标明死亡、失踪、失去设备、转化形态。不得把经历过的所有外挂永久叠加。需要死者参战时，在改编记录中写明“恢复最后可行动形态并保留终局记忆”，不宣称原作复活。借用机构、人脉和武器需交代可用条件，不能自动拥有朋友的全部科技。

阅读以全文检索定位、关键情节精读和跨书证据核对为基础。每张卡至少两个真实行号证据（短篇可用一处足以支持），人物能力/立场不能根据名字频率猜测。请保存不确定项而非把猜测写成确定事实。重复出现的名字只证明提及，不能自动满足多书登场。

## 单卡 JSON 格式

写入自己分配目录 `data/character_batches/<batch>/cards.json`，为对象数组。每个对象如下，字段可增加但不得省略必填字段。中文自然语言请写得具体，忌同质化套话。实际角色卡由主代理统一渲染为 Markdown；评级另生成档案。

```json
{
  "id":"weisili_wei_sili",
  "name":"卫斯理",
  "aliases":[],
  "series":["卫斯理系列"],
  "roles":["主角"],
  "version":{"basis":"综合终局经历","canonical_endpoint":"具体原作结局及最后可行动形态","deployment":"说明参战时身体/设备/记忆状态"},
  "ooc":[],
  "terms":[{"term":"必要术语","explanation":"本意与跨世界接口"}],
  "biography":"至少300个汉字的独立人物化传记。通过原作事件、选择与后果展现此人的性格，不得用通用模板段落凑数。",
  "appearance":{"description":"1至3句具体外观；无依据的服饰等列入改编","portrayal":"神态、语气、动作表现"},
  "role_function":"人物在互动中的作用",
  "modes":{"ordinary":"常态","pressure":"受压/被卷入时","reasoning":"他怎样理解自己的选择"},
  "abilities":[{"name":"能力或行为","type":"范畴","mechanism":"直接原理","visual":"可观察表现，普通技能无需炫光","applications":["攻击或解决阻碍","防护与脱身","生活/侦察/交往"],"limits":"能力本身的前提和边界"}],
  "baseline":{"destruction":"标准攻击可作用的物体","durability":"肉身对穿刺、钝击、冷热、电腐蚀等的已知底线；未知不编抗性","speed":"反应与移动区分","energy":"能源或非物理能力，无则写明","mind":"精神攻防，不把意志坚定等同免疫","stamina":"续航与恢复，不虚构时长","intelligence":{"in_combat":"战中综合表现","knowledge":"常规知识推理","planning":"策略经验复盘","adaptation":"非战斗突发应对"}},
  "passives":[],
  "trump_cards":[],
  "weaknesses":[{"name":"确有因果关系的限制","mechanism":"为何存在","visible":"别人能看到什么","discovery":"如何发现而非自动全知","mitigation":"本人已会采取的对策"}],
  "logic":{"motivation":"主要欲求/特殊胜利条件","principles":["1至3项选择准则"],"triggers":[{"situation":"跨世界也可触发的情境","condition":"触发条件","action":"动作、判断与可能台词；台词若为创作不要冒称原话"}]},
  "adaptations":[{"change":"具体细微改编或新增演绎接口","reason":"如何避免背设定而不改变底色","power_impact":"无新增能力/具体影响"}],
  "evidence":[{"path":"卫斯理系列/001钻石花 .txt","start_line":1,"end_line":5,"supports":"该段实际支持的经历、能力或行为","kind":"原文"}],
  "confidence":"high / medium / low",
  "uncertainties":[],
  "rating_input":{
    "positive":{"physical":2,"energy":0,"scope":1,"sustain":2,"range":2,"combat":7},
    "positive_reasons":{"physical":"理由","energy":"理由","scope":"理由","sustain":"理由","range":"理由","combat":"理由"},
    "negative":{"self_limit":{"score":2,"af":1.0,"reason":"理由"},"environment":{"score":1,"af":1.0,"reason":"理由"},"volatility":{"score":1,"reason":"理由"}},
    "concept_level":0,
    "concept_reason":"为何属于该概念层；科技/超能力不自动是概念权柄",
    "theoretical_tier":"并",
    "mastery":"不适用",
    "ceiling":{"description":"可控最高表现及依赖条件","tier":"并","uncontrolled":"有则说明，无则明确无已证据"},
    "rating_confidence":"medium"
  }
}
```

所有数值必须依据原文能力与任务场景自行判断，示例分数不代表任何人物的默认值。正向六项为0至10，权重依次1.5/1.5/2/2/1.5/1.5；负向自我与环境先乘各自AF，再加波动扣分。普通人类不因为武术好就拥有城市级破坏；“武功高”只影响体能、战术和技巧。财富、跨国机构的社会影响不是能力物理作用范围。非战斗人物可标不参与战斗胜负，有其角色目标，评级仍按自身实际战斗手段。

原帖允许省略不存在的底牌/弱点，故数组可空。不得人为编造“大招后虚弱十分钟”。每卡至少3个不同场景的行为扳机，避免把原剧情作为固定下一步；不需反复喊人物关键词。

## 覆盖清单

`data/character_batches/<batch>/coverage.json` 为逐书数组：

```json
{"path":"系列/文件.txt","status":"reviewed","included":[{"name":"角色","card_id":"同上","role":"主角/重要配角/反派/阶段性对立者","basis":"为什么纳入"}],"excluded":[{"name":"已查过的边缘人物","reason":"一次性配角/仅提及等"}],"notes":[]}
```

一个已识别的重要角色若归其他批次，填写统一ID并通知主代理，不重建卡。没有完成阅读的书用 `pending`，不伪称reviewed。保存稿件后反馈覆盖数、卡数、疑难角色，主代理合并和复核。禁止访问其他代理未授权目录进行覆盖，不修改NK_Source或现有清理记录。
