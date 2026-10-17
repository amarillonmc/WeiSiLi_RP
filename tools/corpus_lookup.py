"""Read-only line references and optional name candidates for the NK corpus."""
import argparse
import collections
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=Path('C:/Users/mapodoufu/Downloads/NK_Source')


def books(pattern='.',source=SOURCE):
    for p in sorted(source.rglob('*.txt')):
        rel=p.relative_to(source).as_posix()
        if re.search(pattern,rel):
            yield rel,p.read_text(encoding='utf-8').splitlines()


def catalog(source=SOURCE):
    out=[]
    for p in sorted(source.rglob('*.txt')):
        b=p.read_bytes();t=b.decode('utf-8')
        out.append({'path':p.relative_to(source).as_posix(),'sha256':hashlib.sha256(b).hexdigest(),
                    'bytes':len(b),'characters':len(t),'lines':len(t.splitlines())})
    target=ROOT/'data/corpus_catalog.json'
    target.write_text(json.dumps({'source':str(source),'files':out},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Catalogued',len(out),'texts')


def candidates(pattern,output):
    sys.path.insert(0,str(ROOT/'.local/vendor'))
    import jieba
    import jieba.posseg as posseg
    jieba.setLogLevel(40)
    result=[]
    for path,lines in books(pattern):
        text='\n'.join(lines)
        counts=collections.Counter(w.word for w in posseg.cut(text) if w.flag.startswith('nr') and 1<len(w.word)<8)
        dialog=collections.Counter()
        for s in lines:
            for m in re.finditer(r'(?:^|[，。！？“”「」：；\s])([\u4e00-\u9fff]{2,5})(?:道|说|问|笑道|叫道|问道|说道|冷笑|摇头|点头)[：，：“「]',s):
                dialog[m[1]]+=1
        result.append({'path':path,'names':counts.most_common(65),'speakers':dialog.most_common(45)})
        print(path, ' '.join(f'{n}:{c}' for n,c in counts.most_common(35)))
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--book',default='.')
    parser.add_argument('--term')
    parser.add_argument('--regex',action='store_true')
    parser.add_argument('--context',type=int,default=1)
    parser.add_argument('--limit',type=int,default=12)
    parser.add_argument('--chars',type=int,default=220)
    parser.add_argument('--sample',action='store_true',help='Spread hits across the complete book')
    parser.add_argument('--last',action='store_true',help='Select the last matching lines')
    parser.add_argument('--range',dest='line_range')
    parser.add_argument('--edges',type=int)
    parser.add_argument('--catalog',action='store_true')
    parser.add_argument('--names',type=Path)
    args=parser.parse_args()
    if args.catalog:catalog();return
    if args.names:candidates(args.book,args.names);return
    for path,lines in books(args.book):
        selected=set();hits=0
        if args.line_range:
            a,b=map(int,args.line_range.split(':'));selected.update(range(max(1,a),min(b,len(lines))+1))
        elif args.edges:
            nonempty=[i for i,s in enumerate(lines,1) if s.strip()]
            selected.update(nonempty[:args.edges]+nonempty[-args.edges:])
        elif args.term:
            pattern=re.compile(args.term if args.regex else re.escape(args.term))
            positions=[i for i,s in enumerate(lines,1) if pattern.search(s)]
            hits=len(positions)
            if args.sample and hits>args.limit:
                positions=[positions[round(k*(hits-1)/max(1,args.limit-1))] for k in range(args.limit)]
            elif args.last:positions=positions[-args.limit:]
            else:positions=positions[:args.limit]
            for i in positions:selected.update(range(max(1,i-args.context),min(len(lines),i+args.context)+1))
        else:
            raise ValueError('Choose --term, --range, --edges, --catalog or --names')
        if selected:
            print(f'\n{path} ({len(lines)} lines; {hits} hits)')
            for i in sorted(selected):
                s=lines[i-1]
                if not s:continue
                if args.chars and len(s)>args.chars:s=s[:args.chars]+'…'
                print(f'L{i}: {s}')


if __name__=='__main__':main()
