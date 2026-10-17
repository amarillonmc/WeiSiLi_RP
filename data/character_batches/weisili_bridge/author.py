"""Authoring for books 098–112, using the common validated card structure."""
import sys,json,re,importlib.util
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('yuan_common',HERE.parent/'yuanzhenxia/author.py')
common=importlib.util.module_from_spec(spec);spec.loader.exec_module(common)
SOURCE=Path('C:/Users/mapodoufu/Downloads/NK_Source/卫斯理系列')
BOOKS={p.name[:3]:'卫斯理系列/'+p.name for p in SOURCE.glob('*.txt') if re.match(r'\d{3}',p.name)}
BOOKS['94x']='卫斯理系列/94少年卫斯理.txt'
skill=common.skill
def ev(book,a,b,s):return dict(path=BOOKS[str(book).zfill(3)],start_line=a,end_line=b,supports=s,kind='原文')
def fix(c):
 c['id']=c['id'].replace('yuanzhenxia_','weisili_',1);c['series']=['卫斯理系列'];return c
def human(*a,**k):return fix(common.human(*a,**k))
def make(*a,**k):return fix(common.make(*a,**k))
def cov(book,included,excluded=(),notes=()):
 return dict(path=BOOKS[str(book).zfill(3)],status='reviewed',included=[dict(name=n,card_id=i,role=r,basis=b)for n,i,r,b in included],excluded=[dict(name=n,reason=r)for n,r in excluded],notes=list(notes))
WEI=('卫斯理','weisili_wei_sili','系列主角','调查与行动')
BAI=('白素','weisili_bai_su','系列主角','判断与协助')
def save(part,cards,coverage):
 for n,obj in [(part+'.cards.json',cards),(part+'.coverage.json',coverage)]:
  (HERE/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 cc=[];cv={}
 for p in sorted(HERE.glob('*.cards.json')):cc.extend(json.loads(p.read_text(encoding='utf-8')))
 for p in sorted(HERE.glob('*.coverage.json')):
  for e in json.loads(p.read_text(encoding='utf-8')):cv[e['path']]=e
 for n in range(98,113):cv.setdefault(BOOKS[str(n).zfill(3)],dict(path=BOOKS[str(n).zfill(3)],status='pending',included=[],excluded=[],notes=[]))
 (HERE/'cards.json').write_text(json.dumps(cc,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (HERE/'coverage.json').write_text(json.dumps(list(cv.values()),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(len(cc),'cards;',sum(e['status']=='reviewed'for e in cv.values()),'/15 books')
