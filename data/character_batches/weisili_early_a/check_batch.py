from pathlib import Path
import json,re,math
p=Path(__file__).parent
cards=json.loads((p/'cards.json').read_text(encoding='utf-8'))
src=Path('C:/Users/mapodoufu/Downloads/NK_Source')
errors=[];cache={}
tiers=['纸','并','强','凶','狂','准神','神下','神中','神上']
for c in cards:
 n=len(re.findall(r'[\u3400-\u9fff]',c['biography']))
 if n<300:errors.append([c['id'],'han',n])
 for e in c['evidence']:
  f=src/e['path']
  if not f.exists():errors.append([c['id'],'missing',e['path']]);continue
  if str(f) not in cache:cache[str(f)]=len(f.read_text(encoding='utf-8').splitlines())
  if not 1<=e['start_line']<=e['end_line']<=cache[str(f)]:errors.append([c['id'],'range',e])
 r=c['rating_input'];v=list(r['positive'].values());neg=r['negative'];s=sum(a*b for a,b in zip(v,[1.5,1.5,2,2,1.5,1.5]))-sum(neg[k]['score']*neg[k]['af'] for k in ['self_limit','environment'])-neg['volatility']['score'];s=math.floor(max(s,0)+.5)
 actual=next((i for i,t in enumerate([10,25,33,40,55,70,80,90,100]) if s<=t),8)
 if tiers.index(r['theoretical_tier'])<actual:errors.append([c['id'],'tier',s,r['theoretical_tier'],tiers[actual]])
print(json.dumps({'cards':len(cards),'coverage':len(json.loads((p/'coverage.json').read_text(encoding='utf-8'))),'errors':errors},ensure_ascii=False))
