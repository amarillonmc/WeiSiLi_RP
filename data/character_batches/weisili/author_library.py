"""Local authoring helpers: shared wording only for genuinely shared physiological limits."""
import json
from pathlib import Path
BASE=Path(__file__).resolve().parent
ROOT=Path('C:/Users/mapodoufu/Downloads/NK_Source')
CARDS=BASE/'cards.json'
def ev(prefix,a,z,support):
    matches=[p for p in (ROOT/'卫斯理系列').glob('*.txt') if p.name.startswith(prefix)]
    if len(matches)!=1: raise ValueError((prefix,matches))
    p=matches[0];lines=p.read_text(encoding='utf-8').splitlines()
    assert 0<a<=z<=len(lines),(p,a,z,len(lines))
    return {'path':'卫斯理系列/'+p.name,'start_line':a,'end_line':z,'supports':support,'kind':'原文'}
def ab(name,mechanism,limits,applications=None,visual=None,kind='技能'):
    return {'name':name,'type':kind,'mechanism':mechanism,'visual':visual or '由叙述中的实际动作、对话和结果呈现，不追加光效。','applications':applications or ['以此处理眼前的具体难题','在前提不满足时改用协商、撤离或求助','用于相应的调查与日常协作'],'limits':limits}
PROFILES={
 'martial':([4,0,1,4,3,8],(1,1,1),'强','受过训练的人体近战、临时武器及可取得的常规枪械；不能据技巧宣称能摧毁建筑。','武术反应和短程爆发高于常人，远距离移动仍依赖交通工具。'),
 'investigator':([3,0,1,3,3,7],(1,1,1),'并','人体擒拿、械斗及有条件使用的常规枪械；破坏对象是人体和一般障碍。','有实战训练的反应和移动，没有超音速或瞬移证据。'),
 'ordinary':([1,0,1,1,1,2],(1,1,1),'纸','常人徒手与可取得的普通工具，未证实独立大范围攻击。','常人反应与步行奔跑；交通速度不计作肉身速度。'),
 'expert':([1,0,1,2,1,3],(1,2,1),'纸','常人肉身；研究、财富与情报的间接效果不等于个人破坏力。','常人身体反应；专业判断快慢不能换算成移动速度。'),
 'strong':([5,0,1,5,3,7],(1,1,1),'强','显著超出常人的近身力量；只按明确物体和遭遇描述，不外推城市级。','近距离爆发与攀援突出，未证实无限加速或空间移动。'),
}
def person(id,name,bio,endpoint,role,motivation,ordinary,pressure,reasoning,principles,triggers,abilities,evidence,profile='ordinary',aliases=None,appearance=None,portrayal=None,adaptations=None,ooc=None,extra=None):
    positive,neg,theory,destruction,speed=PROFILES[profile]
    scores=dict(zip(['physical','energy','scope','sustain','range','combat'],positive))
    baseline={'destruction':destruction,'durability':'肉身仍会受穿刺、钝击、灼烧、严寒与电击伤害；没有文本依据的抗性不赋予。','speed':speed,'energy':'未证实独立释放非物理攻击；使用设备时另核实际携带与能源。','mind':'有个人意志与知识，不能据此判定免疫催眠、脑控制、灵魂干预或信息欺骗。','stamina':'按其身体、训练和现场状态行动；需要休息、治疗与补给，不编造无限续航或精确时长。','intelligence':{'in_combat':pressure,'knowledge':ordinary,'planning':reasoning,'adaptation':'先以已掌握的本领处理新情况，遇到证据不符时允许调整；不预先知道异世界规则。'}}
    reasons={'physical':destruction,'energy':'本卡未把接触到的外星技术或他人的能力计入个人能量输出。','scope':'按能直接作用的人体、局部物件或现场计分，社会势力不等于攻击面积。','sustain':baseline['stamina'],'range':'近身与常规工具的有限距离；没有无条件远程法术。','combat':'根据正文中的'+('实战技巧与现场判断' if profile in ('martial','investigator','strong') else '实际行动、专业能力及缺少战斗展示的边界')+'作项目分析。'}
    card={'id':'weisili_'+id,'name':name,'aliases':aliases or [],'series':['卫斯理系列'],'roles':role if isinstance(role,list) else [role],
    'version':{'basis':'综合本语料终局经历，保留人物变化与不确定项','canonical_endpoint':endpoint,'deployment':endpoint+'。仅携带卡中明确列出的随身装备；朋友、机构与失去的装置均需另行取得支持。'},
    'ooc':ooc or ['不得把叙述者的推测写成此人已证实的全知事实。','能力、身份与道德选择须以卡中的证据边界为准。'],
    'terms':[],'biography':bio,'appearance':{'description':appearance or '服饰和五官以当前场景为准；本卡没有足够原文依据指定统一战衣或额外生理特征。','portrayal':portrayal or ordinary},
    'role_function':motivation,'modes':{'ordinary':ordinary,'pressure':pressure,'reasoning':reasoning},'abilities':abilities,'baseline':baseline,'passives':[],'trump_cards':[],'weaknesses':[],
    'logic':{'motivation':motivation,'principles':principles,'triggers':[{'situation':t[0],'condition':t[1],'action':t[2]} for t in triggers]},
    'adaptations':adaptations or [{'change':'将原作中的选择习惯扩展为下列跨场景行为扳机；现场对白可重新生成，不强制复演旧案。','reason':'让人物围绕当下证据、关系和代价作选择，避免逐段朗诵身世。','power_impact':'不增加原作未有的技能、资源或权能。'}],
    'evidence':evidence,'confidence':'medium','uncertainties':['数值评级为项目分析，原文没有相应战斗数值。'],
    'rating_input':{'positive':scores,'positive_reasons':reasons,'negative':{'self_limit':{'score':neg[0],'af':1.0,'reason':'受到自身身体、知识与本人选择边界限制，见七维和行为逻辑。'},'environment':{'score':neg[1],'af':1.0,'reason':'须有可操作的现场、器材与接触条件，不自动调用整个关系网。'},'volatility':{'score':neg[2],'reason':'陌生规则、信息缺口和身体伤害会影响发挥。'}},'concept_level':0,'concept_reason':'未证实独立的概念权柄；科学知识、意志与特殊经历本身不构成概念干涉。','theoretical_tier':theory,'mastery':'不适用','ceiling':{'description':'在本卡列明条件下使用已证实的本领；历史上失去的设备不计常驻。','tier':theory,'uncontrolled':'若正文存在未能自行复现的事件，须作为经历而非必定可发动的能力。'},'rating_confidence':'medium'}}
    if extra:
        for k,v in extra.items():
            if k=='baseline':card[k].update(v)
            else:card[k]=v
    if not card['weaknesses']:
        card['weaknesses']=[{'name':'条件与经验边界','mechanism':abilities[0]['limits'],'visible':'在前提不足、工具不在或身体状态不支持时，行动不能按计划完成。','discovery':'通过观察能力的实际失败条件及询问可核经历发现，不默认对方读过本卡。','mitigation':'确认条件、寻找可用帮助或改变方案；不以口头宣称消除限制。'}]
    assert len(bio)>=300,(name,len(bio))
    assert len(evidence)>=2,(name,'evidence')
    return card
def save(cards):
    existing=json.loads(CARDS.read_text(encoding='utf8')) if CARDS.exists() else []
    byid={c['id']:c for c in existing}
    byid.update({c['id']:c for c in cards})
    CARDS.write_text(json.dumps(list(byid.values()),ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(f'Saved {len(cards)} cards; total {len(byid)}')
def rate(c,values,neg=(1,1,1),tier='强',reason='依据本卡所列的直接能力及条件，未把关系网计作个人火力。',concept=0,mastery='不适用'):
    r=c['rating_input'];r['positive']=dict(zip(['physical','energy','scope','sustain','range','combat'],values))
    for k in r['positive_reasons']:r['positive_reasons'][k]=reason+'；该项仅评价本卡机制在对应维度上的作用。'
    for k,n in zip(['self_limit','environment','volatility'],neg):r['negative'][k]['score']=n
    r['theoretical_tier']=tier;r['ceiling']['tier']=tier;r['mastery']=mastery;r['concept_level']=concept
    return c
def compact(id,name,bio,endpoint,role,motive,practice,pressure,judgment,skills,evidence,profile='ordinary',aliases=None,triggers=None,extra=None):
    return person(id,name,bio,endpoint,role,motive,practice,pressure,judgment,
      [judgment,'不把他人提供的帮助当作自己无条件拥有的能力'],
      triggers or [('出现适合其本领处理的具体难题','有实际线索或工具可供行动',practice+'；先检查前提再行动。'),('自身在意的关系或目标受到威胁','威胁已具体到眼前的人和选择',pressure),('现有解释与新证据矛盾','可以查验的事实否定了原先判断',judgment+'；说明仍然不知道的部分。')],
      skills,evidence,profile=profile,aliases=aliases,extra=extra)
def cover(prefix,items,excluded=(),notes=()):
    p=BASE/'coverage.json';rows=json.loads(p.read_text(encoding='utf8'))
    found=[r for r in rows if Path(r['path']).name.startswith(prefix)]
    if len(found)!=1:raise ValueError((prefix,len(found)))
    row=found[0];row['status']='reviewed'
    row['included']=[{'name':n,'card_id':i if '_' in i and i.startswith(('adventure_','yuanzhenxia_','detective_','mulanhua_','gaosi_','guihua_')) else 'weisili_'+i,'role':role,'basis':basis} for n,i,role,basis in items]
    row['excluded']=[{'name':n,'reason':r} for n,r in excluded]
    row['notes']=list(notes)
    p.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
