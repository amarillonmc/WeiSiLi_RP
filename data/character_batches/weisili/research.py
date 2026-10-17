import json,re,sys,collections,math
from pathlib import Path
BASE=Path(__file__).resolve().parent
ROOT=Path('C:/Users/mapodoufu/Downloads/NK_Source/卫斯理系列')
def books():
    return sorted(ROOT.glob('*.txt'))
def indexed(path):
    return [(i+1,x) for i,x in enumerate(path.read_text(encoding='utf-8').splitlines()) if x.strip()]
def emit(x): print(json.dumps(x,ensure_ascii=False))
if sys.argv[1]=='init':
    p=BASE/'coverage.json'
    if not p.exists(): p.write_text(json.dumps([{'path':'卫斯理系列/'+b.name,'status':'pending','included':[],'excluded':[],'notes':[]} for b in books()],ensure_ascii=False,indent=2),encoding='utf-8')
elif sys.argv[1]=='index':
    allc=[]; df=collections.Counter()
    for b in books():
        tx=b.read_text(encoding='utf-8')
        counts=collections.Counter()
        for s in re.findall(r'[\u4e00-\u9fff]+',tx):
            for size in (2,3):
                counts.update(s[i:i+size] for i in range(len(s)-size+1))
        df.update(k for k,v in counts.items() if v>=5)
        allc.append((b,counts))
    out=[]
    for b,c in allc:
        scored=sorted(((v*math.log(148/(df[k]+1)),k,v,df[k]) for k,v in c.items() if v>=8),reverse=True)
        picked=[]
        for score,k,v,n in scored:
            if any(k in z['text'] or z['text'] in k for z in picked):continue
            picked.append({'text':k,'count':v,'books':n})
            if len(picked)>=30:break
        out.append({'path':b.name,'candidates':picked})
    (BASE/'name_candidates.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    emit({'indexed':len(out)})
elif sys.argv[1]=='names':
    data=json.loads((BASE/'name_candidates.json').read_text(encoding='utf-8'))
    a=int(sys.argv[2]);n=int(sys.argv[3])
    for o in data[a:a+n]:emit({'path':o['path'],'candidates':o['candidates'][:20]})
elif sys.argv[1]=='end':
    pattern=sys.argv[2]; limit=int(sys.argv[3]) if len(sys.argv)>3 else 16
    for b in books():
        if pattern in b.name:
            emit({'path':b.name,'lines':indexed(b)[-limit:]})
elif sys.argv[1]=='ends':
    a=int(sys.argv[2]);z=int(sys.argv[3]);n=int(sys.argv[4]) if len(sys.argv)>4 else 12
    for b in books()[a:a+z]:emit({'path':b.name,'lines':indexed(b)[-n:]})
elif sys.argv[1]=='head':
    pattern=sys.argv[2];limit=int(sys.argv[3]) if len(sys.argv)>3 else 16
    for b in books():
        if pattern in b.name:emit({'path':b.name,'lines':indexed(b)[:limit]})
elif sys.argv[1] in ('find','last'):
    pattern=sys.argv[2];term=sys.argv[3];limit=int(sys.argv[4]) if len(sys.argv)>4 else 12
    for b in books():
        if pattern in b.name:
            hits=[(n,x) for n,x in indexed(b) if re.search(term,x)]
            emit({'path':b.name,'count':len(hits),'lines':hits[-limit:] if sys.argv[1]=='last' else hits[:limit]})
elif sys.argv[1]=='range':
    pattern=sys.argv[2];a=int(sys.argv[3]);z=int(sys.argv[4])
    for b in books():
        if pattern in b.name:emit({'path':b.name,'lines':[(i,x) for i,x in indexed(b) if a<=i<=z]})
