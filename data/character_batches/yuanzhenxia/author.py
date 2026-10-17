"""Shared serialization for individually authored Yuan Zhenxia profiles."""
import json,re
from pathlib import Path
from decimal import Decimal,ROUND_HALF_UP
HERE=Path(__file__).resolve().parent
SOURCE=Path('C:/Users/mapodoufu/Downloads/NK_Source/原振侠系列')
BOOKS={int(p.name[:2]):'原振侠系列/'+p.name for p in SOURCE.glob('*.txt')}

def ev(book,start,end,supports):
    return dict(path=BOOKS[book],start_line=start,end_line=end,supports=supports,kind='原文')

def skill(name,mechanism,visual,applications,limits,type='主动技能'):
    return dict(name=name,type=type,mechanism=mechanism,visual=visual,applications=applications,limits=limits)

def make(key,name,bio,end,ability,drive,principles,triggers,evidence,stats,reasons,
         roles=None,aliases=None,look='外形依原作出场身份；原文未确定的衣饰不固定。',
         style='先以具体行动表达立场，再说明理由；不反复自报设定。',ordinary=None,pressure=None,
         thinking=None,weak=None,negative=(1,1,1),body=None,terms=None,dead=False,uncertain=None,
         deployment=None,theory=None,mastery='不适用',ceiling=None,confidence='medium',concept=0):
    assert len(re.findall('[\u3400-\u9fff]',bio))>=300,(name,len(re.findall('[\u3400-\u9fff]',bio)))
    cid='yuanzhenxia_'+key
    defaults={
        'destruction':'人类肉身，徒手只能对人体与小型物件造成有限损伤；武器效果取决于实际配备。',
        'durability':'普通人体会被枪弹、利器、钝击、窒息及极端温度伤害；没有特殊电击或腐蚀抗性证据。',
        'speed':'人类反应与移动；不把剧情中迅速行动换算为超声速，也不把交通工具速度算作步行。',
        'energy':'未证实独立施放非物理攻击。',
        'mind':'具有人的情绪与判断；坚持意志不等同于抵抗一切精神干涉。',
        'stamina':'需要休息、饮食与治疗，受伤会妨碍行动；原文未给统一持续时限。',
        'intelligence':{'in_combat':ability[0]['limits'],'knowledge':ability[0]['mechanism'],
                        'planning':thinking or drive,'adaptation':triggers[-1][2]}
    }
    if body:defaults.update(body)
    if weak is None:weak=[]
    keys=['physical','energy','scope','sustain','range','combat']
    pos=dict(zip(keys,stats));prs=dict(zip(keys,reasons))
    ns,ne,nv=negative
    raw=sum(Decimal(str(s))*Decimal(str(w)) for s,w in zip(stats,[1.5,1.5,2,2,1.5,1.5]))-ns-ne-nv
    score=int(raw.quantize(Decimal('1'),rounding=ROUND_HALF_UP))
    tiers=['纸','并','强','凶','狂','准神','神下','神中','神上']
    tier=next(t for t,hi in zip(tiers,[10,25,33,40,55,70,80,90,100]) if score<=hi)
    tier=tiers[min(tiers.index(tier),{0:5,1:6,2:8,3:8}[concept])]
    adaptation=[{'change':'把本卡列出的处境作为开放式触发条件；允许用沉默、追问或行动表达同一立场，具体台词均可随场景改写。','reason':'使性格产生选择而非重复小说情节或逐条背诵设定。','power_impact':'不新增能力，不改变原作关键关系。'}]
    if dead:
        adaptation.append({'change':'如需实际参战，恢复最后可独立行动的形态并保留已知终局记忆；这只是跨世界部署约定。','reason':'使已经死亡、消散或失踪者仍可参与互动。','power_impact':'不宣称原作已经复活，不追加重生或不死能力。'})
    return dict(id=cid,name=name,aliases=aliases or [],series=['原振侠系列'],roles=roles or ['单书主角'],
        version={'basis':'本语料中的完整故事经过与后续明确出场；不将被提及等同于登场。','canonical_endpoint':end,
                 'deployment':deployment or ('按最后可独立行动形态加入；终局异常作为明确改编恢复，不重演死亡过程。' if dead else '使用终局认知与最后稳定形态；外援须取得同意，现场没有的装备不能凭空调用。')},
        ooc=['不把间接见闻、朋友的能力或临时获救手段写成本人永久权能。'],terms=terms or [],
        biography=bio,appearance={'description':look,'portrayal':style},role_function=drive,
        modes={'ordinary':ordinary or triggers[0][2],'pressure':pressure or triggers[1][2],'reasoning':thinking or drive},
        abilities=ability,baseline=defaults,passives=[],trump_cards=[],weaknesses=weak,
        logic={'motivation':drive,'principles':principles,'triggers':[dict(situation=s,condition=c,action=a) for s,c,a in triggers]},
        adaptations=adaptation,evidence=evidence,confidence=confidence,uncertainties=uncertain or [],
        rating_input={'positive':pos,'positive_reasons':prs,
          'negative':{'self_limit':{'score':ns,'af':1.0,'reason':weak[0]['mechanism'] if weak else '能力的已知边界：'+ability[0]['limits']},
                      'environment':{'score':ne,'af':1.0,'reason':'场景条件：'+ability[0]['limits']},
                      'volatility':{'score':nv,'reason':'临场情绪与选择：'+(pressure or triggers[1][2])}},
          'concept_level':concept,'concept_reason':'所列能力作用于身体、信息或特定装置；没有任意改写抽象概念或叙事层的可靠证据。',
          'theoretical_tier':theory or tier,'mastery':mastery,
          'ceiling':{'description':ceiling or ability[0]['mechanism']+'；'+ability[0]['limits'],'tier':theory or tier,
                     'uncontrolled':'故事中的偶发实验或其他角色施展的效果均不算可主动调用；没有证实超出所列上限的独立权能。'},
          'rating_confidence':confidence})

def save(part,cards,coverage):
    for name,obj in [(part+'.cards.json',cards),(part+'.coverage.json',coverage)]:
        (HERE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    allcards=[];allcov={}
    for p in sorted(HERE.glob('*.cards.json')):allcards.extend(json.loads(p.read_text(encoding='utf-8')))
    for p in sorted(HERE.glob('*.coverage.json')):
        for e in json.loads(p.read_text(encoding='utf-8')):allcov[e['path']]=e
    for n,path in BOOKS.items():allcov.setdefault(path,dict(path=path,status='pending',included=[],excluded=[],notes=[]))
    (HERE/'cards.json').write_text(json.dumps(allcards,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (HERE/'coverage.json').write_text(json.dumps(sorted(allcov.values(),key=lambda x:x['path']),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Yuan: {len(allcards)} cards; {sum(x["status"]=="reviewed" for x in allcov.values())}/32 reviewed')

def cov(book,included,excluded=(),notes=()):
    return dict(path=BOOKS[book],status='reviewed',included=[dict(name=n,card_id=i,role=r,basis=b) for n,i,r,b in included],
                excluded=[dict(name=n,reason=r) for n,r in excluded],notes=list(notes))

def human(k,n,b,end,mechanism,drive,trigs,refs,stats=(1,0,1,2,1,2),roles=None,dead=False,aliases=None):
    return make(k,n,b,end,[skill('经验与现场行动',mechanism,'通过观察、交谈和实际操作显现，不附加超自然光效。',[trigs[0][2],trigs[1][2],trigs[2][2]],'依靠人的身体、已掌握的知识和现场资源；没有证实的能力不能由经历推导。')],drive,
        ['根据亲历事实作选择','重视自身真正愿意承担的代价'],trigs,refs,stats,
        ['以实际人体条件计','未证实主动能量攻击','个体与身边环境','人类体力和休息','手边工具与沟通距离','按该人物实际行动经验计'],roles=roles,dead=dead,aliases=aliases)
