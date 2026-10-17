import json,re
from pathlib import Path
p=Path(__file__).resolve().parent/'coverage.json'
xs=json.loads(p.read_text(encoding='utf8'))
out=[]
for x in xs:
 m=re.match(r'(\d+)',x['path'].split('/')[-1])
 n=int(m.group(1)) if m else -1
 if 55<=n<=93 or 95<=n<=145:out.append(x)
assert len(out)==90,len(out)
p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Coverage scoped to',len(out))
