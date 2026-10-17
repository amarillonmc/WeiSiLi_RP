"""Resolve body/spirit deployment ambiguities after cross-series endpoint merges."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
B=ROOT/'data/character_batches'

def evidence(path,a,b,s):
    return dict(path=path,start_line=a,end_line=b,supports=s,kind='原文')

def once(xs,item):
    if item not in xs:xs.append(item)

def add(c,text,refs=()):
    if text not in c['biography']:c['biography']+=text
    for ref in refs:once(c['evidence'],ref)

def patch(c):
    cid=c['id']
    if cid=='yuanzhenxia_nige':
        c['version']['deployment']='明确恢复空间实验前尼格自己的身体，保留已知终局经历；不携带徐玉音身体，也不获得主动夺舍能力。'
        add(c,'《迷路》的解释进一步区分死亡与记忆逸出：他在实验过程中因惊恐而自杀，记忆系统离开身体是意外结果，不能成为随意出窍的方法。新场景恢复的是他自己的原身，徐玉音的身体、关系和身份均不随之归他所有。',[evidence('原振侠系列/02.迷路.txt',3737,3745,'死亡原因及记忆逸出的事故性质')])
    if cid=='yuanzhenxia_liu_liangzhong':
        c['version']['deployment']='需要实际互动时，明确恢复车祸前刘量中自己的身体并保留已知终局经历。原作终局仍在薄片内，不能同时使用薄片隐蔽与人体行动，也不能自行离片。'
        once(c['evidence'],evidence('原振侠系列/17.幽灵星座.txt',8041,8055,'薄片中的点圈与无法联络'))
        once(c['uncertainties'],'原作终局外界无法继续联络；卡内人体七维评价的是明示恢复后的参战身体。')
    if cid in ['yuanzhenxia_lu_dafa','yuanzhenxia_yu_bao']:
        c['version']['deployment']='默认采用与爱人共同离去后的离体意识，保留本人经历；不同时取得健康肉身。若另行恢复原身，须明确标作形态改编，原文没有证明随时安全回体。'
        c['baseline'].update(
            destruction='离体意识未展示可破坏物体的攻击；身体留存不等于可以同时操纵它作战。',
            durability='灵体承受物理伤害的方式未明；没有实证的肉体伤害接口不等于对精神或其他作用全免疫。',
            speed='曾跨地域显现并向特定见证者告别；宇宙旅行或超光速只是讨论，没有可套用的战斗速度。',
            energy='有有限的意识交流和显现，没有已证实的能量攻击。',
            stamina='离体维持与回归条件未明；留存身体的营养护理和灵体是否需要补给分别记录。')
        c['appearance']['description']='终局以离体意识活动，曾向特定见证者显现；不默认所有人都能看见，也不把旧日实体服饰当作护甲。'
        c['adaptations']=[a for a in c['adaptations'] if not a['change'].startswith('如需实际参战，恢复最后可独立行动')]
        once(c['adaptations'],dict(change='让离去后的意识在新场景继续面对关系和选择；若使用原身，必须单独声明恢复身体的部署。',reason='保持终局自主离体的选择，避免把肉体与灵体的优点同时叠加。',power_impact='不新增自由回体、无限瞬移、夺舍或物理攻击；两种形态分别适用能力条件。'))
        once(c['evidence'],evidence('原振侠系列/11.失魂.txt',3189,3205,'共同离体告别与肉身另行护理'))
        if cid=='yuanzhenxia_lu_dafa':
            once(c['evidence'],evidence('原振侠系列/13.巫艳.txt',5,9,'后续仍照料留在医院的身体'))
        r=c['rating_input'];r['positive']['physical']=0
        r['positive_reasons']['physical']='默认离体意识未展示物理攻击；不使用另留的身体同时作战。'
        r['positive_reasons']['sustain']='意识维持与回归机制未明，保守计有限延续，不由身体护理推成无限灵体寿命。'
    if cid=='yuanzhenxia_shizhe':
        c['version']['deployment']='明确恢复进入薄片前的低温幻变人形，并保留已知终局经历；原作仍在薄片内失去外界联系，这一部署不表示她能自行逃离。'
        c['baseline'].update(
            destruction='能拉开人的手臂；低温接触可令普通人疼痛、僵硬发抖，未展示巨力或大范围冻结。',
            durability='已展示穿透仪器和墙等实体障碍；枪弹、极温、电、腐蚀的具体作用未获实证，不宣称全面免疫。',
            speed='可穿墙改变路径，显现及离去速度未量化；不由穿透推成无限瞬移。',
            energy='能进行有限意识沟通，并依原体系媒介处理灵魂信息；不是任意能量放射。',
            stamina='依赖幻变形体、媒介和原体系条件；未说明人类饮食或医疗需求，也未证明可以无限维持。')
        c['appearance']['description']='呈女子人形而体温异常低，属于幻变形态；终局薄片内表现为包围刘量中小黑点的淡圈。'
        for e in [evidence('原振侠系列/17.幽灵星座.txt',4371,4445,'低温接触与推拉'),evidence('原振侠系列/17.幽灵星座.txt',5375,5397,'穿透仪器与墙'),evidence('原振侠系列/17.幽灵星座.txt',5283,5303,'无语言沟通'),evidence('原振侠系列/17.幽灵星座.txt',8041,8055,'终局薄片与无法联络')]:once(c['evidence'],e)
        if not any(a['name']=='低温形体与穿透' for a in c['abilities']):
            c['abilities'].append(dict(name='低温形体与穿透',type='形态特性',mechanism='幻变人形具有异常低温，能接触推拉人，也能穿过部分实体障碍。',visual='接触者疼痛发抖；身形穿过仪器和墙。',applications=['避免长时间直接拥抱伤害普通人','穿过已能穿透的障碍改变接近路线','用具体触感说明形体差异'],limits='未证明对所有材质、力场或伤害皆无效；不能把亲密接触的低温影响扩张成远程冻结。'))
        c['rating_input']['positive_reasons']['physical']='低温接触和有限推拉；没有巨力或广域冻结。'
        c['rating_input']['positive_reasons']['sustain']='按明确恢复的使者形态评价，维持条件仍受媒介与规则限制。'
    if cid=='yuanzhenxia_youming_collectors':
        c['version']['deployment']='限定为当场实际参与的使者及其已获准使用的媒介；选择幻变人形或电脑载体时说明具体成员与权限，不配置整个星座和医院资源。'
        c['baseline'].update(
            destruction='幻变人形能产生低温接触影响，曾冻僵接触者手臂；脑干涉导致意外另列，不能作为无限物理破坏。',
            durability='非人类肉体，形态、媒介和权限有条件；枪弹、电、腐蚀等具体抗性未充分展示，不按普通人体或绝对无敌处理。',
            speed='形体显现、媒介转接和医院设备运输分别处理；没有全员可用的无限瞬移速度。',
            stamina='按各自形体、载体与任务条件维持；没有普通人进食治疗需求的统一证据，也不推定全体无供能限制。',
            mind='能干涉特定对象脑活动、采集和收容意识；成员有情绪与伦理分歧，没有全员共享一切思想或绝对精神防御的证据。')
        c['appearance']['description']='执行者可幻变为低温人形，部分通过电脑载体或设备联系；外观相近不等于同一成员，也不表示占有普通人的身体。'
        for e in [evidence('原振侠系列/17.幽灵星座.txt',7401,7421,'低温接触'),evidence('原振侠系列/17.幽灵星座.txt',8141,8149,'幻变人形而非人类身体'),evidence('原振侠系列/18.黑暗天使.txt',2715,2741,'电脑载体'),evidence('原振侠系列/18.黑暗天使.txt',6043,6063,'医院设备参与接回'),evidence('原振侠系列/18.黑暗天使.txt',6083,6121,'接回过程与条件')]:once(c['evidence'],e)
        c['rating_input']['positive_reasons']['physical']='低温接触有具体影响，未展示巨力；不以人形外观当作人类肉身。'
        c['rating_input']['positive_reasons']['sustain']='执行者可持续完成相关任务，但单个形体的维持上限与媒介条件未全部交代。'
    if cid=='weisili_tangna':
        c['biography']=c['biography'].replace('结局中一家落魄后再次失去踪迹，孩子未来是否安全并无确定交代。','《玩具》篇末一家落魄后再次失去踪迹，后续安全当时尚未交代。')
        add(c,'最终她拒绝为了重获身体而争夺别人的生命位置，这个决定应比早年的儿童游戏习惯更有优先级。《圈套》中死亡前的原身已经急速衰老；如另行恢复最后实体形态，应保留暮年与有限行动条件，不能默认回到不长大的健康儿童状态。',[evidence('卫斯理系列/088圈套.txt',2147,2194,'急速衰老在先、跌石死亡在后'),evidence('卫斯理系列/088圈套.txt',3116,3120,'不再做人、不争夺其他灵魂')])
        c['version']['deployment']='默认采用不愿再占用身体的离体意识；联系须有实际情境和已证实渠道。若明确需要实体参战，另行恢复死亡前已衰老的原身，保留终局记忆，不叠加幼年健康身体或未来机器保护。'
        c['appearance']['description']='历史上外貌长期停留在儿童，死亡前急速衰老；默认终局为离体意识，未给统一可见外形。'
        c['abilities']=[dict(name='有限的离体与借体交流',type='意识现象',mechanism='失去原身后曾进入陈安安和母亲的半脑表达经历；能够退出，却不能保证再次进入。',visual='由已有身体说出自己的经历，或退出后失去直接联系。',applications=['在已经形成的有限联系中表达意愿','向可信者解释未来家庭经历','拒绝为了生存争夺其他灵魂的身体'],limits='不具任意夺舍、随时显形、复活或机器控制能力；对新对象不能默认建立同样渠道。')]
        c['baseline'].update(destruction='离体意识未展示可直接破坏物体的攻击。',durability='原身已经死亡；灵体受伤的具体机制未知，不据此宣称对精神、媒介或其他力量全免疫。',speed='没有可量化的自由移动或战斗瞬移；进入、退出具体身体的经历不等于无限机动。',energy='有特定借体表达经历，未证实能量攻击。',mind='保留自主意愿，明确不愿争夺陈安安的身体；进入与再进入并不由自己完全掌控。',stamina='灵体延续与联系持续条件未知；不能以未来曾维持外貌来证明永久存在。')
        c['baseline']['intelligence'].update(in_combat='没有以灵体战胜他人的实绩，优先表达意愿与避免争夺。',knowledge='本人在未来家庭及后续死亡、借体经历中的所知；不掌握控制中心全部科技。',planning='把是否继续拥有身体视为自己的选择，同时承认他人已有生命位置。',adaptation='遇到所谓重生机会时先确认代价、宿主与同意，不因能活便接受一切条件。')
        c['modes'].update(ordinary='以具体记忆和感受表达自己，不假装了解整个未来世界。',pressure='对侵占别人的身体保留明确拒绝；无法交流时不能自行创造万能通道。',reasoning='自己的延续不应以抢夺另一灵魂的位置为当然代价。')
        c['logic']['motivation']='保有自己的意愿与经历，拒绝以争夺他人身体换取重新做人。'
        c['logic']['principles']=['尊重自己是否继续拥有身体的决定','不把别人的身体当作空置工具','只据本人实际经历解释未知']
        c['logic']['triggers']=[dict(situation='有人提出重获身体',condition='需要排挤现有灵魂或隐瞒代价',action='拒绝，并追问身体和原主人的处境。'),dict(situation='形成可以表达的联系',condition='对方愿意听取本人意愿',action='讲述具体经历与选择，不替未来主宰解释一切。'),dict(situation='旁人只把她当作旧日孩子',condition='忽略已经历死亡和作出的决定',action='可以保留早年的亲切或好奇，也会坚持现在的拒绝和边界。')]
        c['weaknesses']=[dict(name='不能保证重新建立借体联系',mechanism='已能退出的身体不一定能再次进入，终局也不愿争夺其他人的生命位置。')]
        r=c['rating_input'];r['positive']=dict(zip(['physical','energy','scope','sustain','range','combat'],[0,2,1,1,1,1]))
        r['positive_reasons']=dict(zip(r['positive'],['没有灵体物理攻击','有限借体交流现象，不是任意夺舍','只涉及具体宿主与关系人','意识延续条件未明','没有任意远距联系能力','没有主动战斗表现']))
        r['negative']['self_limit'].update(score=1,reason='明确拒绝争夺别人的身体；不是可以随意解除的自保开关。')
        r['negative']['environment'].update(score=1,reason='能表达依赖具体联系与宿主条件，退出后未必能再进入。')
        r['negative']['volatility'].update(score=1,reason='现象可控程度有限，不能承诺每次获得有效交流。')
        r['theoretical_tier']='纸';r['mastery']='不适用';r['ceiling'].update(tier='纸',description='在已经形成的有限借体联系中表达经历或退出；未证实可任意创造新渠道。',uncontrolled='原来的外貌维持、机器保护和家庭遭遇不是可主动发动的能力。')

for name in ['yuanzhenxia','weisili_mid']:
    folder=B/name
    for p in [folder/'cards.json',*folder.glob('*.cards.json')]:
        cards=json.loads(p.read_text(encoding='utf-8'))
        for c in cards:patch(c)
        p.write_text(json.dumps(cards,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Terminal body and spirit forms reconciled with explicit deployment variants.')
