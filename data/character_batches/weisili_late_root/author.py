import sys,json,re,importlib.util
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('bridge_common',HERE.parent/'weisili_bridge/author.py')
common=importlib.util.module_from_spec(spec);spec.loader.exec_module(common)
BOOKS=common.BOOKS
ev=common.ev;skill=common.skill;make=common.make;human=common.human;cov=common.cov
WEI=common.WEI;BAI=common.BAI
def save(part,cards,coverage):
 for n,obj in [(part+'.cards.json',cards),(part+'.coverage.json',coverage)]:
  (HERE/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 cc=[];cv={}
 for p in sorted(HERE.glob('*.cards.json')):cc.extend(json.loads(p.read_text(encoding='utf-8')))
 for p in sorted(HERE.glob('*.coverage.json')):
  for e in json.loads(p.read_text(encoding='utf-8')):cv[e['path']]=e
 for n in range(117,125):cv.setdefault(BOOKS[str(n)],dict(path=BOOKS[str(n)],status='pending',included=[],excluded=[],notes=[]))
 (HERE/'cards.json').write_text(json.dumps(cc,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (HERE/'coverage.json').write_text(json.dumps(list(cv.values()),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(len(cc),'cards;',sum(e['status']=='reviewed'for e in cv.values()),'/8 books')
