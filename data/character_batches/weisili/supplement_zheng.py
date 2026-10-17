from author_library import *
data=json.loads(CARDS.read_text(encoding='utf8'))
data=[c for c in data if c['id']!='weisili_chen_san']
byid={c['id']:c for c in data}
def add(c,s,e):
    if s not in c['biography']:c['biography']+=s
    for x in e:
        if x not in c['evidence']:c['evidence'].append(x)
add(byid['weisili_zheng_tianlu'],'早期《尸变》记录了费格发现他的异样体温、脉搏与骨骼后，应他的请求保守秘密并预备死亡证明；尸体在未知液滴后停止活动并迅速腐烂，不能把这段无自主选择的尸体现象加成常驻复生。家属所说的数日预见重大事故也只是转述，其机制和是否可重复未明。',[ev('017',1035,1059,'方言、婚配眼镜与家属转述预见'),ev('017',937,979,'尸体活动及液滴后停止'),ev('017',1155,1182,'尸体腐烂、异骨'),ev('017',1507,1556,'费格诊察与郑请求守密')])
add(byid['weisili_zheng_baoyun'],'他在《尸变》中曾因害怕被当作研究标本而安排灭口，身体挣扎虽有力量，仍被卫斯理制住；后来吞毁父亲笔记而失常，是《血统》重新解释的前段，不能略去他的主动伤害行为，也不能停在这一个失常终点。',[ev('017',1681,1729,'受制、恐惧被解剖、灭口与合作'),ev('017',1991,2016,'阅读并吞毁笔记、异常状态')])
CARDS.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
p=BASE/'coverage.json';rows=json.loads(p.read_text(encoding='utf8'))
for r in rows:
    if Path(r['path']).name.startswith('074'):
        r['included']=[x for x in r['included'] if x['card_id']!='weisili_chen_san']
        if not any(x['name']=='陈三' for x in r['excluded']):r['excluded'].append({'name':'陈三','reason':'郑宅总管，单书提供闹鬼线索、食宿后勤，无反派行为；017尸变全文不见此人，不能误当跨书角色。'})
p.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Updated Zheng family; removed unsupported recurring classification for Chen San')
