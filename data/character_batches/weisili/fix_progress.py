import json
from pathlib import Path
B=Path(__file__).resolve().parent
p=B/'cards.json';cs=json.loads(p.read_text(encoding='utf8'))
tiers={'weisili_li_yixin':'凶','weisili_en_ji':'并','weisili_zhuo_chi':'强'}
for c in cs:
    if c['id'] in tiers:
        c['rating_input']['theoretical_tier']=tiers[c['id']]
        c['rating_input']['ceiling']['tier']=tiers[c['id']]
p.write_text(json.dumps(cs,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
p=B/'coverage.json';rows=json.loads(p.read_text(encoding='utf8'))
for r in rows:
    if Path(r['path']).name.startswith('071'):
        r['excluded']=[x for x in r['excluded'] if x['name']!='王居风、高彩虹']
        for name,id in [('王居风','weisili_wang_jufeng'),('高彩虹','weisili_gao_caihong')]:
            if not any(x['card_id']==id for x in r['included']):
                r['included'].append({'name':name,'card_id':id,'role':'重要配角','basis':'时空旅行中拍摄、救助并把录像与信送交常福；与《迷藏》统一主卡'})
        r['notes']=['张拾来后半生真实身份被有意隐去，不推断成现实人物；伤后刀术不如从前。王居风、高彩虹主卡由中段批次统一。']
    if Path(r['path']).name.startswith('068'):
        r['excluded']=[x for x in r['excluded'] if '文依来父亲' not in x['name']]
        if not any(x['card_id']=='adventure_nizhao_huoren' for x in r['included']):
            r['included'].append({'name':'泥沼火人／文依来兄弟之父','card_id':'adventure_nizhao_huoren','role':'重要配角','basis':'与非人协会原书及本书确认相同身世，合并其历史行动，不额建人名'})
p.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
for filename,old,new in [('author_dongtian.py',"tier='强',reason='按本人可操作", "tier='凶',reason='按本人可操作"),('author_dongtian.py',"tier='纸',reason='以有限信息", "tier='并',reason='以有限信息"),('author_huoyong.py',"tier='并',reason='精壮人体", "tier='强',reason='精壮人体")]:
    p=B/filename;t=p.read_text(encoding='utf-8-sig');p.write_text(t.replace(old,new),encoding='utf8')
print('Repaired tiers and shared coverage')
