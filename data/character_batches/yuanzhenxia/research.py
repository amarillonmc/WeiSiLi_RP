import sys,re
from pathlib import Path
SOURCE=Path('C:/Users/mapodoufu/Downloads/NK_Source/原振侠系列')
def scan(num,term,n=6,width=550):
    p=next(SOURCE.glob(f'{num:02}.*.txt'));lines=p.read_text(encoding='utf-8').splitlines()
    hits=[i for i,s in enumerate(lines) if re.search(term,s)]
    pos=hits if len(hits)<=n else [hits[round(k*(len(hits)-1)/(n-1))] for k in range(n)]
    print(f'\n{p.name} / {term} / {len(hits)} hits')
    for i in pos:
        lo=max(0,i-1);hi=min(len(lines),i+4)
        s=''.join(lines[lo:hi])
        print(f'L{lo+1}-{hi}: {s[:width]}')
if __name__=='__main__':
    scan(int(sys.argv[1]),sys.argv[2],int(sys.argv[3]) if len(sys.argv)>3 else 8)
