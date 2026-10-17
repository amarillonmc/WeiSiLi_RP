from author_library import *
cards=json.loads(CARDS.read_text(encoding='utf8'));cv=json.loads((BASE/'coverage.json').read_text(encoding='utf8'))
redirects={'weisili_jiaozhang':'weisili_kaoyan_priest','weisili_royal_elder':'weisili_tusheng'}
handoff=[]
for c in cards:
 if c['id'] in redirects:handoff.append({'source_id':c['id'],'target_id':redirects[c['id']],'source_card':c,'merge_note':'同一原文身份，保留目标卡，不另生成此旧ID。'})
cards=[c for c in cards if c['id'] not in redirects]
d={c['id']:c for c in cards}
for r in cv:
 for x in r['included']:
  x['card_id']=redirects.get(x['card_id'],x['card_id'])
 name=Path(r['path']).name
 if name.startswith('083'):
  r['excluded']=[x for x in r['excluded'] if x['name']!='温先生']
  r['included'].append({'name':'温宝裕之父温伯如','card_id':'weisili_wen_boru','role':'重要配角','basis':'向妻子建议、暗示儿子不要争执；与133父亲身份互认，不和其他系列温先生合并'})
 if name.startswith('085'):
  r['excluded']=[x for x in r['excluded'] if x['name']!='原振侠']
  r['included'].append({'name':'原振侠','card_id':'yuanzhenxia_yuanzhenxia','role':'重要配角','basis':'开篇由老蔡转述实际来电找卫氏夫妇及温宝裕，属于通信行动；主卡归原振侠批'})
 if name.startswith('126'):
  r['excluded']=[x for x in r['excluded'] if x['name']!='大羊鹰']
  r['included'].append({'name':'大羊鹰','card_id':'adventure_daying','role':'重要配角','basis':'124重述孤峰身份；126与成人神鹰以鹰语沟通，载金维和神鹰去山顶'})
  r['notes'].append('大羊鹰与神鹰是两个独立角色；飞行由大羊鹰承担，变成人的神鹰仍不能独立飞行。')
 # Clear provisional wording where the actual conclusion is simply that the corpus contains no second event.
 for x in r['excluded']:
  x['reason']=x['reason'].replace('未核到另一独立故事实际登场','本语料未见另一独立故事实际登场')
c=d['weisili_wen_boru'];c['biography']+=' 《毒誓》中他曾试图在妻子面前给儿子提出办法，被压回后用眼色示意儿子不要徒费唇舌。这种退让与后来研究时的自负并不矛盾：他把自主性更多放在自己的书籍和药物世界里。';c['evidence'].append(ev('083',1006,1019,'父亲在家庭中的建议与眼色'))
c=d['weisili_hong_ling'];c['biography']+=' 神鹰成人后要与金维离去，她虽不舍，仍平静让他寻找新的秘密，把远行理解成成长，而不是以过去照顾过他为由要求永久依附。她与鹰相处的经验也不等于完全理解鹰语：看到神鹰和大羊鹰真正对话，才承认自己仍隔着一层。';c['evidence'] += [ev('126',117,124,'亲历交流与自认沟通边界'),ev('126',130,158,'不舍而尊重离去的选择')]
CARDS.write_text(json.dumps(cards,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(BASE/'coverage.json').write_text(json.dumps(cv,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(BASE/'shared_merge_evidence.json').write_text(json.dumps(handoff,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Cards',len(cards),'reviewed',sum(r['status']=='reviewed' for r in cv),'/',len(cv))
