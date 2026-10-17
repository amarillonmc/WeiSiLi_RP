from pathlib import Path
import json,re,sys
ROOT=Path(r'C:/Users/mapodoufu/Downloads/NK_Source')
OUT=Path('data/character_batches/detective')
SERIES=['木兰花全集','神探高斯系列','倪匡之鬼话系列']
books=[p for s in SERIES for p in sorted((ROOT/s).glob('*.txt'))]
if sys.argv[1]=='init':
 (OUT/'coverage.json').write_text(json.dumps([{'path':p.relative_to(ROOT).as_posix(),'status':'pending','included':[],'excluded':[],'notes':[]} for p in books],ensure_ascii=False,indent=2),encoding='utf-8')
elif sys.argv[1]=='read':
 for p in books:
  if sys.argv[2] in p.name:
   ls=p.read_text(encoding='utf-8').splitlines(); a=int(sys.argv[3]) if len(sys.argv)>3 else 1;b=int(sys.argv[4]) if len(sys.argv)>4 else len(ls)
   print('\nFILE',p.relative_to(ROOT),'LINES',len(ls))
   ranges=[(int(sys.argv[i]),int(sys.argv[i+1])) for i in range(3,len(sys.argv)-1,2)] if len(sys.argv)>4 else [(a,b)]
   for a,b in ranges:
    for n,l in enumerate(ls[a-1:b],a):
     if l.strip(): print(f'{n}:{l}')
elif sys.argv[1]=='summary':
 for p in books:
  if sys.argv[2] in str(p):
   ls=p.read_text(encoding='utf-8').splitlines(); tx='\n'.join(ls)
   names={}
   for m in re.finditer(r'([\u4e00-\u9fff]{2,4})(?:说道|问道|答道|叫道|道：|道∶|说：|说∶|冷笑|大笑|大声|低声|摇头|点头)',tx):
    n=m.group(1);names[n]=names.get(n,0)+1
   print('\nFILE',p.relative_to(ROOT),'LINES',len(ls),'NAMES',sorted(names.items(),key=lambda x:-x[1])[:25])
   non=[(n,l) for n,l in enumerate(ls,1) if l.strip()]
   for n,l in non[:8]+non[-12:]: print(f'{n}:{l[:450]}')
