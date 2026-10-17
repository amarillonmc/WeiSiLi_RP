"""Merge proven cross-series identities without merging mere shared titles."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
B=ROOT/'data/character_batches'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def union(a,b):return list(dict.fromkeys(a+b))
def ev(path,a,b,s):return dict(path=path,start_line=a,end_line=b,supports=s,kind='原文')
groups={p:read(p)for p in B.glob('*/cards.json')}
def find(cid):
 return next((c for cs in groups.values()for c in cs if c['id']==cid),None)
records=[]
def merge(oldid,newid,why,proof,endpoint=None):
 old,new=find(oldid),find(newid)
 assert new is not None,newid
 records.append(dict(previous_id=oldid,canonical_id=newid,reason=why,evidence=proof))
 if old is None:return
 oldbio='较早或另一系列经历：'+old['biography']
 if oldbio not in new['biography']:new['biography']+='\n\n'+oldbio
 for k in ['aliases','series','roles']:new[k]=union(new[k],old[k])
 if old['name']!=new['name']:new['aliases']=union(new['aliases'],[old['name']])
 for e in old['evidence']+proof:
  if e not in new['evidence']:new['evidence'].append(e)
 if endpoint:new['version']['canonical_endpoint']=endpoint
 for p,cs in groups.items():groups[p]=[c for c in cs if c['id']!=oldid]
merge('weisili_shuiyin_general','adventure_shuiyin','同名外号、黛娜的情报上司、将军身份在《谜踪》明确接续。',
 [ev('卫斯理系列/075谜踪.txt',63,91,'黛娜明确指认自己的上司水银将军')],
 '《妖偶》《怪头》《谜踪》中持续作为情报高层行动；《谜踪》结局不在最初核心知情名单之内，没有证据证明其从头出卖巴图。')
merge('weisili_jin_te','yuanzhenxia_jinte','《快活秘方》由卫斯理介绍自己的旧识金特，来客皆熟悉其已记述的经历；保留后期灵媒能力及石门失联结局。',
 [ev('原振侠系列/21.快活秘方.txt',143,201,'卫斯理旧识、既有经历与灵媒能力')])
merge('yuanzhenxia_hu_huaiyu','weisili_hu_huaiyu','《黑白无常》直接说明研究所与主持人曾在《犀照》出现。',
 [ev('原振侠系列/25.黑白无常.txt',85,107,'明确跨书指认'),ev('原振侠系列/25.黑白无常.txt',291,295,'后期仍有对自身感知的疑虑')],
 '《黑白无常》继续主持海洋生物研究所并参与宝盒事件，仍有感知真假的困扰；不再把《犀照》冲突当作最后一次活动，未获遗传改造异能。')
c=find('weisili_hu_huaiyu')
if c:
 c['roles']=union(c['roles'],['重要配角'])
 c['abilities'][0]['mechanism']='海洋生物研究、标本保存与培养、合格潜水、研究设施操作及经费组织；雷射设备需要实际配置。'
 c['baseline']['intelligence']['knowledge']=c['abilities'][0]['mechanism']
 e=ev('原振侠系列/25.黑白无常.txt',2255,2257,'合格潜水及实际出海')
 if e not in c['evidence']:c['evidence'].append(e)
c=find('yuanzhenxia_jinte')
if c:c['roles']=union(c['roles'],['重要配角'])
# The late Wei Sili owner merges the root's 121 details into its longer endpoint.
p=B/'weisili_late_root/cards.json';late=groups[p]
other=next(c for cs in groups.values()for c in cs if c['id']=='weisili_hai_gao')
if any(c['id']=='weisili_haigao'for c in late):
 assert any('/121' in e['path'] and e['start_line']==1643 for e in other['evidence']), 'Merge 海高 121 details first'
groups[p]=[c for c in late if c['id'] not in ['weisili_tianjia','weisili_haigao']]
assert find('weisili_tianjia') is not None,'Missing canonical 天嘉'
records.append(dict(previous_id='weisili_haigao',canonical_id='weisili_hai_gao',reason='《考验》与《只限老友》同一王族竞争者，合并后期结局。',evidence=[ev('卫斯理系列/121考验.txt',1643,1647,'冒名破坏合作'),ev('卫斯理系列/145只限老友.txt',1124,1135,'后期支持者离散')]))
# Overlapping drafts were retired by their owner; retain useful evidence and aliases,
# not their superseded endpoint or the early mistaken description as unnamed.
shared=B/'weisili/shared_merge_evidence.json'
if shared.exists():
 for item in read(shared):
  old=item['source_card'];new=find(item['target_id'])
  assert new is not None,item['target_id']
  new['aliases']=union(new['aliases'],old['aliases']+[old['name']])
  for e in old['evidence']:
   if e not in new['evidence']:new['evidence'].append(e)
  records.append(dict(previous_id=item['source_id'],canonical_id=item['target_id'],reason='《考验》同一人物的早期描述与后文具名身份；以完整终局卡为准。',evidence=old['evidence']))
  for p,cs in groups.items():groups[p]=[c for c in cs if c['id']!=item['source_id']]
c=find('weisili_kaoyan_priest')
if c:
 c['appearance']['description']='原出场穿红色教长长袍，由人抬行；终局袍服已被收走，不能继续把它当作现任身份凭证。'
 c['appearance']['portrayal']='以冷淡姿态和标准英语保持距离；权威受检验时，讥讽比解释来得更快。'
c=find('weisili_tusheng')
if c:
 c['appearance']['portrayal']='以礼貌和耐心回应尖锐问题，涉及自身利益时仍可以平静承认害怕改变。'
for p,cs in groups.items():write(p,cs)
redirects={r['previous_id']:r['canonical_id']for r in records}
for p in B.glob('*/coverage.json'):
 cv=read(p)
 for book in cv:
  for role in book['included']:role['card_id']=redirects.get(role['card_id'],role['card_id'])
 # Delegate-owned books were placeholders in the initial detective batch.
 if p.parent.name=='detective':
  owned={x['path']for x in read(B/'mulanhua_late/coverage.json')if x['status']=='reviewed'}
  cv=[x for x in cv if not(x['status']=='pending'and x['path']in owned)]
 write(p,cv)
 if p.parent.name=='detective' and (p.parent/'audit.json').exists():
  audit=read(p.parent/'audit.json')
  audit['reviewed']=sum(x['status']=='reviewed' for x in cv)
  audit['pending']=sum(x['status']=='pending' for x in cv)
  audit['scope']='鬼话25、神探高斯29、木兰花01至40，共94文件；木41至60由mulanhua_late批独立记录，已移除完成书目的重复占位。'
  write(p.parent/'audit.json',audit)
# Early wood-human patients receive complete cards when their later stories are known.
for p in [B/'weisili_bridge/coverage.json',B/'weisili_bridge/part_c.coverage.json']:
 cv=read(p)
 for book in cv:
  if '/098' not in book['path']:continue
  book['excluded']=[e for e in book['excluded']if e['name']!='木中男女']
  for cid in ['weisili_wood_man','weisili_wood_woman']:
   c=find(cid)
   if c and not any(x['card_id']==cid for x in book['included']):book['included'].append(dict(name=c['name'],card_id=cid,role='跨书主角',basis='本书实验对象，后来《遗传》《水晶宫》明确人格与行动，合并记录早期状态'))
  book['notes']=[x for x in book['notes']if x!='木中人被救出或研究成功未有终局展示。']
  note='本篇木中人尚未完成救治，后续《水晶宫》明确恢复行动，终局见各自主卡。'
  if note not in book['notes']:book['notes'].append(note)
 write(p,cv)
write(ROOT/'data/character_identity_map.json',dict(redirects=redirects,decisions=records))
print('Proven identities merged and coverage references redirected.')
