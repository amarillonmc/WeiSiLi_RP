from author_library import *
import json
cards=json.loads(CARDS.read_text(encoding='utf8'));by={c['id']:c for c in cards}
def append(c,key,text):
    if text not in c[key]:c[key]+=text
def evidence(c,e):
    if not any(x['path']==e['path'] and x['start_line']==e['start_line'] for x in c['evidence']):c['evidence'].append(e)
def other(path,a,z,support):
    assert z<=len((ROOT/path).read_text(encoding='utf8').splitlines())
    return {'path':path,'start_line':a,'end_line':z,'supports':support,'kind':'原文'}
c=by['weisili_wei_sili']
append(c,'biography','在《第二种人》中，他答应保密，却仍想偷取皮膜样本并把秘密写出，求知欲能压过承诺；《背叛》中面对君花，他也曾以偏见否定对方感情，遭到直接反驳。这些是需要承担的缺陷，不能由终局知识自动洗去。')
for e in [ev('054',4314,4324,'偷样本打算与写出秘密的违诺'),ev('078',1963,1983,'君花抗辩其偏见')]:evidence(c,e)
if not any(t['situation']=='秘密关系到他迫切想验证的未知' for t in c['logic']['triggers']):c['logic']['triggers'].append({'situation':'秘密关系到他迫切想验证的未知','condition':'对方明确限制取样或公开，他却认为自己能避免伤害','action':'可能先为越界找理由、试图自行验证；必须允许被发现、被质问及承担失信后果，不自动写成守约圣人。'})
c['ooc'].append('不能把求知欲、偏见和违诺抹成绝对诚实守约；终局经验允许反省，但不伪造原作从未有过的温和历史。') if '不能把求知欲、偏见和违诺抹成绝对诚实守约；终局经验允许反省，但不伪造原作从未有过的温和历史。' not in c['ooc'] else None
c=by['weisili_bai_su']
append(c,'biography','她也有江湖伦理的偏向：《木炭》中认可陈长青挨打是受教训，强调江湖人的信用；她并非在所有冲突中都坚持现代法律的裁判。另一方面，《创造》中，她从毁掉记录和逃亡识破研究者的说法，并指出把自己当作好人范本的盲点；《老猫》中她能推动既有工潮、协调电力，却不是凭空创造民意。')
for e in [ev('037',1335,1348,'从行为识破说法'),ev('037',1450,1479,'指出好人范本的伦理盲点'),ev('039',2403,2443,'已有工潮与七日电力协调'),ev('050',740,828,'江湖信用与认可受教训的偏向')]:evidence(c,e)
c['ooc'].append('不把她写成永远中立、从不合理化伤害的现代法律代言；她的江湖亲疏与信任也会影响判断。') if '不把她写成永远中立、从不合理化伤害的现代法律代言；她的江湖亲疏与信任也会影响判断。' not in c['ooc'] else None
for id in ('weisili_liang_chen','weisili_mei_jing'):
    c=by[id];c['biography']=c['biography'].replace('参与密码、血统、谜踪等事件','参与密码、谜踪、招魂等事件')
    append(c,'biography','《招魂》的古人记忆触及她们不愿轻易示人的家族历史；《变换双星》中，她们反对长期禁锢另一半双生子，愿帮忙也会追问成果公开。她们没有接受那项记忆复制实验，不能把实验对象的能力转给自己。')
    c['appearance']['description']='外貌极相似的年轻双生少女，习惯穿鲜红衣服，身手轻快；不得无证据固定谁永远更冷静。'
    for e in [ev('077',1069,1111,'家族秘密与红娘子后代线索'),other('原振侠系列/22.变换双星.txt',2983,2987,'反对禁锢另一半双生子'),other('原振侠系列/22.变换双星.txt',3115,3157,'愿协助、问公开和清除基地记忆的同意')]:evidence(c,e)
c=by['weisili_cao_jinfu']
append(c,'biography','在原振侠的后续中，他曾护送柳絮逃离，却直到后来才知道她携带的高科技武器远超自己的理解；见她受制时冲拳保护，又被康维轻易制止。豪爽和勇气并不使他拥有对方的科技。他还持续关心姐姐曹银雪及三个孩子，寻找尚未恢复的仲大雅，亲族责任没有随旧仇放下而结束。')
for e in [other('原振侠系列/28.无间地狱.txt',1949,1955,'骗上车实为护送逃离'),other('原振侠系列/28.无间地狱.txt',2803,2827,'不懂柳絮武器且意识保护判断有限'),other('原振侠系列/28.无间地狱.txt',2987,2991,'保护动作被康维单手压回'),other('原振侠系列/29.人鬼疑云.txt',207,231,'探姐姐三胞胎并寻找姐夫')]:evidence(c,e)
if '原振侠系列' not in c['series']:c['series'].append('原振侠系列')
c=by['weisili_hu_ming']
append(c,'biography','早期他以开罗考古教授身份邀卫斯理调查支离木乃伊，曾遭麻醉剂损伤脑神经，后来由外来盒子的原子重组修复；头部暂时离体是那次设备作用，断电后接回，盒子随后被丢进海里，不能成为他的自主支离能力。')
for e in [ev('011',895,911,'考古教授与邀请调查'),ev('011',1981,1983,'麻醉造成脑伤'),ev('011',4173,4189,'设备修复、断电接回与盒子丢海')]:evidence(c,e)
c=by['weisili_zhang_jian']
append(c,'biography','《地心洪炉》中他是南极探险队副队长，能协助证件、观察模型变化并寻找通讯，却曾看守失误被杰弗生击倒。生还时所用飞行带依赖后来爆炸的平台供能，不是永久飞行能力。')
for e in [ev('006',20,26,'探险队副队长'),ev('006',2535,2548,'看守失误'),ev('006',3023,3033,'获救与失去平台供能')]:evidence(c,e)
c=by['weisili_lao_cai']
evidence(c,ev('047',60,64,'蔡根富为唯一亲人'))
evidence(c,ev('047',407,413,'送机与晚年情感'))
c=by['weisili_wang_lian'];c['appearance']['description']='样貌普通、已开始发福的中年妇女；神情可亲切，也能表现对突袭的惊讶。'
evidence(c,ev('141',1041,1047,'明确外貌及卫斯理突然收招'))
c=by['weisili_tao_qiquan']
c['biography']=c['biography'].replace('朱槿的关系又把他接到另一套政治与情报网络上，但双方并非彼此的提线人偶。','他经朋友及朱槿等人的联络接触另一套政治与情报网络；朱槿的丈夫是大亨，不能把这层婚配移给陶启泉。')
evidence(c,ev('108',901,913,'朱槿丈夫明确为大亨，并非陶启泉'))
c=by['weisili_sai_guanyin']
append(c,'biography','她早年练过武术，曾试图借山崖地形对抗于放，却因对方的夜间行动优势而败下风。终局重病使这些旧日身手只保留为经验，不能自动恢复年轻身体。')
evidence(c,ev('134',632,645,'早年武术、布置与失败'))
c=by['weisili_zheng_baoyun']
append(c,'biography','最终他乘红人赠送的小飞船赶到海底，坦承没有帮助就难以到达，仍主动救回可能泄露自己身份的朋友；飞船是明确赠物，但其维修、能源和完整功能没有交代，不能推成无限宇航武库。')
evidence(c,ev('074',3291,3319,'快反应、红人赠船与救友'))
if not any(x['name']=='红人赠送的小飞船' for x in c['abilities']):c['abilities'].append(ab('红人赠送的小飞船','在红人帮助下使用赠送的小飞船抵达深海洞穴救人','具体能源、维护、星际续航和武器配置未说明；不是本人裸身潜海或瞬移能力',kind='装备'))
CARDS.write_text(json.dumps(cards,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
p=BASE/'coverage.json';rows=json.loads(p.read_text(encoding='utf8'))
for r in rows:
    if Path(r['path']).name.startswith('073') and not any(x['card_id']=='weisili_lao_cai' for x in r['included']):r['included'].append({'name':'老蔡','card_id':'weisili_lao_cai','role':'重要配角','basis':'开篇与温宝裕争执、参与卫家日常场景'})
    if Path(r['path']).name.startswith('132'):
        note='原文把三位盗墓者之一写成单相，依《盗墓》单思身份链视为疑似笔误；植物学专家单相是单思哥哥，不并卡、不判单相死亡。'
        if note not in r['notes']:r['notes'].append(note)
p.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Applied core and cross-series evidence supplements')
