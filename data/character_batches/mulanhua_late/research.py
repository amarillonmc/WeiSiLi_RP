from pathlib import Path
import json,re,sys
ROOT=Path('C:/Users/mapodoufu/Downloads/NK_Source/木兰花全集')
def out(x):print(json.dumps(x,ensure_ascii=False))
mode,pat=sys.argv[1:3]
for p in sorted(ROOT.glob('*.txt')):
 if not re.search(pat,p.name):continue
 ls=p.read_text(encoding='utf-8').splitlines()
 if mode=='range':
  a,b=map(int,sys.argv[3:5]); out({'book':p.name,'lines':[(i+1,ls[i]) for i in range(a-1,min(b,len(ls))) if ls[i].strip()]})
 elif mode=='names':
  for term in sys.argv[3].split('|'):
   hits=[i for i,x in enumerate(ls) if term in x]; n=int(sys.argv[4]) if len(sys.argv)>4 else 6
   chosen=sorted(set(hits[:n]+hits[-n:])); indices=set(j for i in chosen for j in range(max(0,i-1),min(len(ls),i+3)))
   out({'book':p.name,'term':term,'hits':len(hits),'lines':[(i+1,ls[i]) for i in sorted(indices) if ls[i].strip()]})
 elif mode=='all': out({'book':p.name,'lines':[(i+1,x) for i,x in enumerate(ls) if x.strip()]})

