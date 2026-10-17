from pathlib import Path
import json,collections,math
base=Path(__file__).parent
root=Path('C:/Users/mapodoufu/Downloads/NK_Source')
cards=json.loads((base/'cards.json').read_text(encoding='utf-8'))
cover=json.loads((base/'coverage.json').read_text(encoding='utf-8'))
rules=json.loads((base.parents[1]/'character_rules.json').read_text(encoding='utf-8'))
errs=[];counts={};ids={c['id'] for c in cards};bands=rules['rating']['bands'];rank={b['name']:i for i,b in enumerate(bands)}
for c in cards:
 if len(c['biography'])<300:errs.append((c['id'],'short biography'))
 if len(c['logic']['triggers'])<3:errs.append((c['id'],'few triggers'))
 for e in c['evidence']:
  p=root/e['path']
  if not p.exists():errs.append((c['id'],'missing evidence',e['path']));continue
  n=counts.setdefault(str(p),len(p.read_text(encoding='utf-8').splitlines()))
  if not 1<=e['start_line']<=e['end_line']<=n:errs.append((c['id'],'bad range',e))
 ri=c['rating_input'];neg=ri['negative'];s=sum(ri['positive'][k]*v for k,v in rules['rating']['positive_weights'].items())-sum(neg[k]['score']*neg[k]['af'] for k in ['self_limit','environment'])-neg['volatility']['score'];r=math.floor(s+0.5)
 tier=next(b['name'] for b in bands if b['min']<=r<=b['max'])
 if rank[tier]>rank[ri['theoretical_tier']]:errs.append((c['id'],'theory below practical',s,tier,ri['theoretical_tier']))
for k,v in collections.Counter(c['id'] for c in cards).items():
 if v>1:errs.append(('duplicate id',k))
for x in cover:
 if not (root/x['path']).exists():errs.append(('missing coverage source',x['path']))
 for c in x['included']:
  if c['card_id'].startswith('adventure_') and c['card_id'] not in ids:errs.append(('missing own card',x['path'],c['card_id']))
expected={str(p.relative_to(root)).replace('\\','/') for s in ['亚洲之鹰罗开系列','年轻人','非人协会系列','浪子高达系列'] for p in (root/s).glob('*.txt')}
actual={x['path'] for x in cover}
if actual!=expected:errs.append(('coverage difference',sorted(expected-actual),sorted(actual-expected)))
report={'cards':len(cards),'books':len(cover),'evidence_sources':len(counts),'errors':errs,'shared_card_ids':sorted({i['card_id'] for x in cover for i in x['included'] if not i['card_id'].startswith('adventure_')})}
(base/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
