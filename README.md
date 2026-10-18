# WeiSiLi_RP

基于倪匡小说建设可供其他项目调用的知识库。现已建立原始语料清理记录、角色卡、独立强度档案，以及按共同世界前提整理的世界规则、时间关系和 RP 状态资料。

角色入口：[knowledge/README.md](knowledge/README.md)。调用方式和整理口径：[知识库使用说明](docs/knowledge_usage.md)。实际条目数、覆盖数量和原文哈希见 [knowledge/manifest.json](knowledge/manifest.json)，校验结果见 [reports/character_kb_validation.json](reports/character_kb_validation.json)。

## 世界观、时间线与 RP 状态

先读 [世界如何运作与演绎说明](docs/worldbuilding_guide.md)，条目入口为 [knowledge/world/README.md](knowledge/world/README.md)。

- 336 个文本均有事件证据入口，连接已有 1,409 个角色的经历；保留原文行号和资料来源。
- 另行整理 14 条世界规则、30 个机构／地点／争夺目标、67 个关键事件、24 条成长线、11 组跨系列连接及 12 项争议与未决问题。
- 时间表使用有证据的先后关系，区分发生、回忆和后来揭露；没有证据的跨系列年代保持未知。
- 按事件生成 RP 状态时，不自动加载人物终局记忆、互斥身体或已经失效的旧装备。

```powershell
python -X utf8 tools/query_world.py 思想仪 --kind entities
python -X utf8 tools/query_world.py --book 微晶之密
python -X utf8 tools/query_world.py --scene w_eagle_human --character 神鹰
python -X utf8 tools/build_world_kb.py --check
```

本轮重点条目关联 85 个文本，直接回读引用来自 8 个文本，全部逐书入口复用已有角色证据；索引全覆盖不表示重新通读全部作品或穷尽世界设定。细分覆盖与构建校验见 [世界覆盖记录](knowledge/world/coverage.json)及 [校验报告](reports/world_kb_validation.json)。

## 角色卡与强度档案

角色卡依照[角色模板首帖](https://number81.xyz/index.php?topic=667.0)整理，强度按[通用评估标准](https://number81.xyz/index.php?topic=1067.0)另存。每张卡保留整体经历、最后明确状态、能力条件、行为扳机、轻微改编和原文行号；同一人物跨系列出场合并，身份尚有疑问的角色不强行归一。

供其他项目调用的文件在 `knowledge/`。`data/character_batches/` 是整理材料，含分批草稿和中间版本，调用方应使用已校验的 `knowledge/index.json` 与它指向的单张卡片。

```powershell
# 输出单张角色卡；同名时返回候选，使用明确 ID 区分。
python -X utf8 tools/query_character.py 卫斯理

# 单独读取强度分析，或切换为便于阅读的 Markdown。
python -X utf8 tools/query_character.py 神鹰 --rating
python -X utf8 tools/query_character.py 白素 --markdown

# 修改聚合数据后，校验全部角色、评分、引用及原文哈希，再重新生成成品。
python -X utf8 tools/build_character_kb.py
```

评分是基于文本的项目分析。涉及原作矛盾、失踪、传闻能力或未展示的治疗过程时，卡片保留不确定性；死亡或特殊形态的参战部署在改编项中说明。

## 2026-10-17 语料清理

正文目录：`C:\Users\mapodoufu\Downloads\NK_Source`。

- 原有 345 个 TXT 和 1 张 JPG；现在保留 336 个正文 TXT，统一为 UTF-8、无 BOM、LF 换行。
- 9 个独立序言/整合说明和 1 张人物关系图移出正文目录，保存在备份区。
- 清除作者出版序跋、整合者和网友说明、目录、网页 CSS 与导航、广告、水印、论坛信息、扫描署名、装饰线、空字符和冗余空白。
- 保留书名、章节标题、原文措辞和换行，以及故事内的序言、楔子、后记和世界观介绍。例如《困兽》的序言、《头发》《神仙》的叙事后记、《双程》的人物来信，以及《非人协会》的背景介绍。
- 10 个文件存在误粘贴的重复正文，已逐段核对清除。《蛇神》现在按 01–10 章排列，每章保留一次。
- 共减少 2,190,284 个字符，包含空白及重复内容；这不是实测 Token 数。UTF-8 每个汉字通常比原 GBK 编码占更多字节，文件字节总量不能直接用于比较 Token 消耗。

清理摘要及质量问题清单：[reports/nk_source_cleanup_20261017.json](reports/nk_source_cleanup_20261017.json)。逐文件审核边界及原始 SHA-256：[data/nk_source_review.json](data/nk_source_review.json)。

## 尚待校勘的原始问题

以下问题原本就在源文件中，本次没有猜测或补写正文：

| 文件 | 无法按 GB18030 解码的原始字节数 |
| --- | ---: |
| 卫斯理系列/133异种人生.txt | 65 |
| 卫斯理系列/135闭关开关.txt | 63 |
| 卫斯理系列/138财神宝库.txt | 1 |
| 原振侠系列/03.血咒.txt | 14 |

这些字节在 UTF-8 文本中用 `U+FFFD`（�）显式标记。详细报告记录原始字节位置和十六进制值，原始字节仍在 ZIP 备份中。另有 32 个文件保留了无法可靠判定的私用字符，可能来自旧字体映射或既有乱码，质量报告列出文件和码位，详细报告还记录其所在行。转成合法 UTF-8 不等于已经完成 OCR 校勘。

`年轻人/13神话世界.txt` 原文注明缺一页；已移除求补文字，没有补写缺页。`浪子高达系列/蛇王石.txt` 原始帖子标注“1-9”和“待续”，完整性需要另行核实。`浪子高达系列/学美人.txt` 的正文题名为《血美人》，文件名暂予保留。

## 备份、检查与恢复

本次运行目录为 `.local/nk-cleanup-20261017/`，已通过 `.gitignore` 排除，避免原文和备份进入 Git：

| 路径 | 内容 |
| --- | --- |
| `originals.zip` | 346 个文件的逐字节原始备份，已校验 SHA-256 |
| `excluded/` | 移出的非正文材料；其中 TXT 也已转为 UTF-8 |
| `preview/` | 与写回正文一致的清理结果 |
| `report.json` | 每个文件的哈希、字符数、清理规则和编码异常 |
| `removals.jsonl` | 被移除或替换的文字、原始行号及原因 |
| `source_verification.json` | 对写回目录进行全量校验的结果 |

需要 Python 3.12 或更新版本，仅使用标准库。当前环境可使用桌面应用自带的 Python：

```powershell
$nkPython = 'C:\Users\mapodoufu\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'

# 校验所有正文的哈希、UTF-8、换行、残留网站标识与关键叙事章节。
& $nkPython -X utf8 tools/verify_nk_source.py --run .local/nk-cleanup-20261017

# 测试正文保留、导航清除、乱码记录、备份恢复和覆盖保护。
& $nkPython -X utf8 -m unittest discover -s tests -v

# 需要撤销时，恢复 346 个原始文件的原始字节。
& $nkPython -X utf8 tools/clean_nk_source.py restore --run .local/nk-cleanup-20261017

# 需要重新应用本次已审核结果时。
& $nkPython -X utf8 tools/clean_nk_source.py apply --run .local/nk-cleanup-20261017
```

应用和恢复都会先核对整批文件及备份的 SHA-256；文件若被另行修改，会拒绝覆盖。`clean_nk_source.py prepare` 仅适用于审核清单对应的原始快照，不应拿已转码文件再次尝试 GB18030 解码，也不是未经审核即可处理其他语料的通用删除规则。

本次验证：13 项测试通过，336 个正文文件的严格 UTF-8 解码、无 BOM、LF 换行与哈希校验均通过；已知网站标识残留为 0。

