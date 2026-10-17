import json
from pathlib import Path
p=Path(__file__).resolve().parent
c=json.loads((p/'cards.json').read_text(encoding='utf8'))
c=[x for x in c if x['id']!='weisili_lun_lun']
(p/'cards.json').write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
for target in ['author_dianwang.py','coverage.json']:
 s=(p/target).read_text(encoding='utf8')
 s=s.replace("('伦伦','lun_lun'","('伦伦','adventure_lunlun'")
 s=s.replace('"card_id": "weisili_lun_lun"','"card_id": "adventure_lunlun"')
 (p/target).write_text(s,encoding='utf8')
print('Merged Lunlun ownership')
