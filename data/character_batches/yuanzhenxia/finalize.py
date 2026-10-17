"""Apply cross-series end states after running this batch's authoring files."""
from author import *

cards=json.loads((HERE/'cards.json').read_text(encoding='utf-8'))
by={c['id']:c for c in cards}
def add(c,e):
    if e not in c['evidence']:c['evidence'].append(e)
def ext(path,a,b,s):return dict(path=path,start_line=a,end_line=b,supports=s,kind='原文')

c=by['yuanzhenxia_gutuo']
c['biography']='古托在不知道家世的情况下长大，却有庞大财力默默支持生活。腿上突然出现的孔洞，使财富带来的便利变成恐惧：没有子弹穿破裤子，身体却像中了枪，各种治疗都不能消除伤口。原振侠后来把他与盛远天的过去连接起来，说明父亲的杀戮与背弃留下血咒，未参与恶行的儿子仍承担后果。古托起初选择不育，希望阻断后代受害，也投入巫术研究，试着把恐惧变成可以理解的问题。后来的达伊安并未将血咒凭空消灭，而把它转到一棵大树上；到原应发作的时刻，树身涌出汁液，古托的腿安然无事，转移确实成功。他随后创立巫术研究院，本身获得很强的精神感应，与玛仙、史奈和达伊安一起接触石球留下的灾难讯息。卡片采用这段后续，不能让他永远停留在流血的受咒者身份，也不能因为能感应信息就赋予任意施咒能力。他仍会对家族、继承和别人把伤害解释成命运特别敏感；当遇到新的异常，既可能动用研究资源，也会承认曾经需要他人帮助，愿意从具体条件而非名望出发寻找答案。'
c['version']['canonical_endpoint']='血咒已由达伊安转移至树，后创立巫术研究院并具有强精神感应；继续参与后期巫术研究。'
c['abilities'][0]['mechanism']='巫术研究、资金组织与精神感应；能接收石球等特定异常信息，不等于任意施咒。'
c['abilities'].append(skill('精神感应','在研究与特殊经历后具有强烈感应能力，可参与接收特定异星遗留讯息。','集中精神、目光改变，解释收到的信息。',['察觉特殊讯号','参与巫术研究'],'对象、场景及解释仍有限；不能由读到信息推出必能控制信息源。')) if not any(a['name']=='精神感应' for a in c['abilities']) else None
c['baseline']['mind']='具有原文明确的强精神感应；没有证实对一切操心或降术免疫。'
c['baseline']['energy']='主要是讯息接收与理解，未见直接能量杀伤。'
c['logic']['triggers'][1]={'situation':'家族旧伤被当作命运','condition':'别人认定只能永远承受','action':'以自己获助的经历追问改变条件，同时区分转移与彻底消灭。'}
c['modes']['pressure']=c['logic']['triggers'][1]['action']
c['rating_input']['positive'].update(energy=2,sustain=3,range=2)
c['rating_input']['positive_reasons'].update(energy='明确具强精神感应，未证实能量伤害',sustain='普通人体，研究与集中需要休息',range='特定讯息接收，范围未量化')
c['rating_input']['theoretical_tier']='并'
c['rating_input']['ceiling'].update(tier='并',description='巫术研究资源与特定精神感应；不包含达伊安替他转移血咒的施术能力。')
c['rating_input']['negative']['volatility']['reason']='旧创伤仍影响选择，但血咒现时已离身，不重复扣除历史伤口。'
add(c,ev(13,537,579,'血咒转移成功，并非仍承受伤口'))
add(c,ev(20,7979,8019,'创立研究院、强精神感应和接收讯号'))

c=by['yuanzhenxia_qinglong']
c['biography']='青龙熟悉丛林、毒虫、暴雨与隐蔽路线，原振侠跟随他行动，才体会到装备不能替代真正的环境判断。他被毒蛇咬中后曾被确认死亡并埋葬，雷雨后的重新出现使双方都难以理解；他与有相似经历的杰西拒绝成为科学检查的样本，采取隐匿和阻断追索的办法保护自主。这次经历没有使他取得主动复活的能力，雷雨更不是随时可用的再生按钮。后续年轻人与公主到访时，青龙仍在中南半岛的山洞生活，身手矫捷，也照顾并培养少年山水，愿意托可靠来客把少年送到能继续学习的地方。他保存一名未在本段具名的深爱女子的旧衣，恳请公主感应她的下落；得知她已通过宗教寄托恢复平静，终于接受不再打扰，因为寻找原本是为了减轻她的痛苦。卡片以这个较后的实际行动修正只剩逃避的印象。他会警惕被物化，会保护亲近的人，却也能在感情最强烈时承认对方不需要自己出现。遇到新关系，信任应来自具体尊重，不能因一次获救就永远忠于某人。'
c['version']['canonical_endpoint']='后在《消失女神》仍居中南半岛，托年轻人和公主送山水求学；得知所爱女子安宁后决定不打扰。复生机制仍不明。'
if '年轻人' not in c['series']:c['series'].append('年轻人')
add(c,ext('年轻人/11消失女神.txt',831,883,'山洞生活、矫捷与托付山水'))
add(c,ext('年轻人/11消失女神.txt',1100,1164,'旧衣感应、选择不打扰和同一人物确认'))
c['uncertainties']=list(dict.fromkeys(c['uncertainties']+['《消失女神》此段未具名的女子不与杰西合并，也不在缺乏明确身份链时另定姓名。']))
c['logic']['triggers'][2]={'situation':'终于有寻找爱人的线索','condition':'得知对方已安宁且再会可能伤害她','action':'先确认她的处境，再克制占有与打扰的冲动。'}

c=by['yuanzhenxia_shinai']
if '在《鬼混》中，他又企图' not in c['biography']:
    c['biography']+='在《鬼混》中，他又企图把军事强人的灵魂召回尸身，最后步骤需要特定亲密关系留下的精气；蓝丝替身破坏条件，仪式失败。他仍能闪开卫斯理全力冲撞并反拍一掌。失败证明施术条件不可省略，其宣称无所不能不等于成功战绩。'
c['version']['canonical_endpoint']='《鬼混》召回强人的仪式因关键媒介被替换而失败；史奈仍能避开冲撞，未证实死亡或失去全部降术。'
if '卫斯理系列' not in c['series']:c['series'].append('卫斯理系列')
add(c,ext('卫斯理系列/079鬼混.txt',4011,4086,'鬼混降的条件、失败及现场反应'))
c['rating_input']['ceiling']['uncontrolled']='鬼混降未完成，所谓人鬼横行无阻只是施术宣言，不计为成功复活或无限战力。'
c=by['yuanzhenxia_baku']
if '在《鬼混》中，他预先' not in c['biography']:
    c['biography']+='在《鬼混》中，他预先向卫斯理等人布置保护，抑制被识别追查的灵气，也使蓝丝和卫斯理免受史奈相应手段的伤害。此处表现出老练的预防安排，但不能扩大成对所有攻击永久免疫。'
c['version']['canonical_endpoint']='《鬼混》中以事前保护降协助蓝丝、卫斯理等破坏史奈仪式；没有后续死亡或失能实证。'
if '卫斯理系列' not in c['series']:c['series'].append('卫斯理系列')
add(c,ext('卫斯理系列/079鬼混.txt',4096,4109,'保护降与遮蔽追查的效果'))
c=by['yuanzhenxia_guijie_aliens']
add(c,ev(29,7423,7617,'与组织技术合作，最后只约定未来脱离鬼界的援助'))
if not any(a['name']=='与地球组织交换技术' for a in c['abilities']):
    c['abilities'].append(skill('与地球组织交换技术','其中一员以讯息联系组织，指导柳絮体内装置与脑部植入体的关联。','不必以可见身体现身，通过声音和接收者交涉。',['指导相容技术实施','接收灵魂讯息并参与谈判'],'仍依地球组织操作和合作者，未解除鬼界的整体环境困境。'))

# Give every ordinary profile a concrete, discoverable limit, not a hidden rule.
for c in cards:
    if not c['weaknesses']:
        limit=c['abilities'][0]['limits']
        c['weaknesses']=[dict(name='已证实能力的适用边界',mechanism=limit,
            visible='当场景超出这些条件时，行动会停顿、失败或需要寻求额外帮助。',
            discovery='通过观察实际出手、询问准备条件和核对已发生的失败来识别，不预先读出整张卡。',
            mitigation='先确认本场景具备的身体、媒介、装备与信息，再选择可行方法；动机仍为：'+c['logic']['motivation'])]

# Persist corrections in both the merged dataset and its authored JSON parts.
for p in HERE.glob('*.cards.json'):
    part=json.loads(p.read_text(encoding='utf-8'))
    p.write_text(json.dumps([by[c['id']] for c in part],ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(HERE/'cards.json').write_text(json.dumps(cards,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for p in list(HERE.glob('*.coverage.json'))+[HERE/'coverage.json']:
    covs=json.loads(p.read_text(encoding='utf-8'))
    for e in covs:
        for r in e['included']:
            if r['card_id']=='adventure_youngman':r['card_id']='adventure_young'
        if e['path']==BOOKS[27]:
            e['notes']=[n for n in e['notes'] if 'ID' not in n]
            if not any(r['card_id']=='adventure_bajiaoxing_yingzi' for r in e['included']):
                e['included'].append(dict(name='八角星恋人',card_id='adventure_bajiaoxing_yingzi',role='重要配角',basis='接触与交通协助'))
    p.write_text(json.dumps(covs,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Finalized',len(cards),'Yuan cards and 32 coverage records')
