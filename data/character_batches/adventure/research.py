import json,re,sys,collections
from pathlib import Path
ROOT=Path('C:/Users/mapodoufu/Downloads/NK_Source')
SERIES=['亚洲之鹰罗开系列','年轻人','非人协会系列','浪子高达系列']
files=[p for s in SERIES for p in sorted((ROOT/s).glob('*.txt'))]
def lines(p):return p.read_text(encoding='utf-8').splitlines()
def findfile(q):return next(p for p in files if q in p.name)
def show(p,seq,cap=180):
 print('\n###',p.relative_to(ROOT))
 for i,s in seq:print(f'{i}: {s[:cap]}'+('…' if len(s)>cap else ''))
if __name__=='__main__':
 mode=sys.argv[1]
 if mode=='overview':
  for p in files:
   if len(sys.argv)>2 and sys.argv[2] not in str(p):continue
   ls=lines(p);text=''.join(ls)
   c=collections.Counter(re.findall(r'[，。！？：“”\s]([\u4e00-\u9fff]{2,5})(?:道|说|问|叫|笑|望|听|想)',text))
   print('\n###',p.relative_to(ROOT),'lines',len(ls),'actors',c.most_common(40))
   show(p,[(i+1,s) for i,s in enumerate(ls) if s][:12],220)
   show(p,[(i+1,s) for i,s in enumerate(ls) if s][-18:],260)
 elif mode=='actors':
  for p in files:
   if len(sys.argv)>2 and sys.argv[2] not in str(p):continue
   ls=lines(p);t=''.join(ls)
   c=collections.Counter(re.findall(r'[，。！？：“”\s]([\u4e00-\u9fff]{2,4})(?:道|说|问|叫|笑|望|听|想)',t))
   print(str(p.relative_to(ROOT)),len(ls),c.most_common(25))
 elif mode=='range':
  p=findfile(sys.argv[2]);a=int(sys.argv[3]);b=int(sys.argv[4]);show(p,[(i+1,s) for i,s in enumerate(lines(p)) if a<=i+1<=b],int(sys.argv[5]) if len(sys.argv)>5 else 1000)
 elif mode=='search':
  q,pat=sys.argv[2:4]
  for p in files:
   if q!='all' and q not in str(p):continue
   show(p,[(i+1,s) for i,s in enumerate(lines(p)) if re.search(pat,s)],int(sys.argv[4]) if len(sys.argv)>4 else 240)
