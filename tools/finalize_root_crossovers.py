"""Idempotent corrections after later-book reveals; source text stays read-only."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
B=ROOT/'data/character_batches'
SOURCE=Path('C:/Users/mapodoufu/Downloads/NK_Source')
def ev(prefix,a,b,s):
 p=next((SOURCE/'卫斯理系列').glob(prefix+'*.txt'))
 return dict(path=p.relative_to(SOURCE).as_posix(),start_line=a,end_line=b,supports=s,kind='原文')
def add(c,s,refs):
 if s not in c['biography']:c['biography']+=s
 for e in refs:
  if e not in c['evidence']:c['evidence'].append(e)
def patch(c):
 cid=c['id']
 if cid=='weisili_wei_qishu':
  add(c,'《在数难逃》揭示，女婴确为穆秀珍，他只是救助与托养者。为寻找那位只见一面的少妇，他不惜改容，带领武装参加战乱，以韦司令之名救援败军、影响战局，最后仍未救回她。多年后见到穆秀珍生父，得知对方为事业杀害恋人，并想寻找女儿；他选择隐瞒穆的下落，避免她被卷进政权继承。此后关系须以这些终局事实为准，不能再把他当成穆的亲生父亲。',[ev('106',626,672,'改容、军旅与寻人'),ev('106',2459,2571,'认出母女'),ev('106',2615,2638,'韦司令旧恩'),ev('106',2678,2725,'隐瞒穆下落')])
  c['aliases']=list(dict.fromkeys(c['aliases']+['韦司令']))
  c['version']['canonical_endpoint']='《在数难逃》认出穆秀珍是当年托养女婴，获知其母被杀，选择不向生父透露她的下落；后来归隐。'
  c['uncertainties']=['卫七曾改容，是经历手术损伤与恢复的长期过程，不是即时变化面容的法术。']
  c['ooc']=list(dict.fromkeys(c['ooc']+['不是穆秀珍生父；他救下并托养她，终局保护她免被迫接受政权与亲属安排。']))
 if cid=='weisili_shenying':
  c['evidence']=[e for e in c['evidence'] if not(e['path'].startswith('卫斯理系列/104') and e['start_line']==273 and e['supports']=='海东青对抗')]
  add(c,'《暗号之二》中，它与监视海东青发生实际空中对抗，不能把对方疑有三只雌鸟的推测当作自己击败全部监视网。《解脱》中说明它经红绫外婆处理而通灵，可以与亲近伙伴沟通；面对毒蜗牛小绿，它明知危险仍受诱惑，最后在蓝丝引导下克制。蓝丝明确否认这是向它施术，因此结局是克服一次诱惑，不是取得抗毒体质或对所有精神影响免疫。',[ev('104',2282,2286,'识别海东青'),ev('104',2376,2381,'捕获海东青'),ev('107',998,1006,'通灵背景'),ev('107',1027,1090,'毒蜗牛诱惑与克服')])
 if cid=='yuanzhenxia_kangwei':
  add(c,'《在数难逃》中，他主持星际资料会商，带来设备并组织对数字的研究，但初步生命密码判断并未成为最终答案。结尾仍未找到解码器，不能把联系发达星球等同于随时获得真相或预言未来。',[ev('106',2257,2260,'仪器装设'),ev('106',2310,2335,'星际研究会议'),ev('106',2727,2744,'未解条件')])
 if cid=='yuanzhenxia_liu_xu':
  add(c,'《在数难逃》中，她因自身不知亲生父母的孤独而理解穆秀珍追问身世的愿望；这种共情是亲历造成的选择，不是被改造后便没有私人感情，也不表示她知道数字的全部意义。',[ev('106',1667,1765,'身世与共情')])
 if cid=='yuanzhenxia_oriental_sun_leader':
  extra=json.loads((B/'weisili_bridge/part_g.cards.json').read_text(encoding='utf-8'))
  old=next((x for x in extra if x['id']=='weisili_chuanghuo_old_leader'),None)
  if old:
   add(c,old['biography'],old['evidence'])
   c['version']['canonical_endpoint']=old['version']['canonical_endpoint']
  c['aliases']=list(dict.fromkeys(c['aliases']+['老人家（文物库事件）','文物库事件的老人家']))
  add(c,'《闯祸》以曾拿两人的自由交换二十年青春这一独特旧事，明确连接《人鬼疑云》的谈判，因此文物库事件老人家归入本卡；不与其他仅称老人家、领袖或首长的匿名人物合并。',[ev('091',207,209,'交换自由与青春的明确回指'),ev('105',575,612,'同一交易旧史')])
  if '卫斯理系列' not in c['series']:c['series'].append('卫斯理系列')
 if cid in ('weisili_taoge','weisili_taoge_furen','weisili_tangna','weisili_yifan'):
  ends={'weisili_taoge':'《圈套》说明未来主宰已结束及其文明的娱乐安排后死亡。','weisili_taoge_furen':'《圈套》急速衰老，唐娜灵魂进入其半脑后解释逆时布置，随后死亡。','weisili_yifan':'《圈套》随全家急速衰老，从失控黄光笼中坠出死亡。','weisili_tangna':'《圈套》肉身跌石死亡，曾占陈安安与母亲半脑；终局不愿争夺陈安安、不愿再做人，未证实消散。'}
  add(c,'《圈套》补全一家四口的结局：未来发生变故，小机械人衰退失控，全家急速衰老。伊凡从黄光笼掉出，唐娜在洞中跌石死亡；她曾进入陈安安和母亲半脑，能退出却不能保证再次进入。陶格夫妇先后死亡，陶格最后传达女儿不愿再做人、不愿与陈安安的现有灵魂争夺身体。前书设备不能因此继续作为永久有效的庇护。',[ev('088',2149,2194,'失控与死亡'),ev('088',2220,2235,'唐娜离入的限制'),ev('088',2539,2580,'母女共躯与母亡'),ev('088',3081,3125,'未来结局和陶格死亡')])
  c['version']['canonical_endpoint']=ends[cid]
  c['version']['deployment']='若需实体参战，明确采用最后可独立行动的身体作为跨世界改编，并保留终局认知；不自动恢复未来主宰、失能机械人或占据其他人的身体。'
  a=dict(change='恢复终局前可独立行动身体供跨世界演绎。',reason='原作终局已死亡或失去肉身。',power_impact='仅为明确部署约定，不能作为复活、不死、随意夺舍或恢复未来设备的原作能力。')
  if a not in c['adaptations']:c['adaptations'].append(a)
 if cid=='weisili_wanju_robots':
  add(c,'《圈套》展示两枚小机械人均已失去原来的功能，轻触或小石就能使其解体，不能再按《玩具》时期的强大系统作为常态。较强版本只供明确注明修复设备的改编场景使用，不能由旧日战绩推出终局仍有效。',[ev('088',2344,2394,'失能与脆弱'),ev('088',2463,2467,'小石破坏')])
  c['version']['canonical_endpoint']='《圈套》两枚小机械人失能并被轻易破坏，原控制系统已不能提供昔日功能。'
  c['version']['deployment']='默认保留终局失能状态，旧能力仅为历史档案；若故事需要有效设备，须明确声明修复这一改编条件。'
  c['name']='《玩具》的机械执行体'
  c['aliases']=list(dict.fromkeys(c['aliases']+['《玩具》的机器统治群体']))
  c['biography']=c['biography'].replace('这组机器来自小说描写的遥远未来，包含体形不足二十厘米的小机器人、其他形制机器和控制中心。','这些机械执行体来自小说描写的遥远未来，其中有体形不足二十厘米的小机器人；它们服从上层控制中心，执行端与主宰本体分开记录。')
  c['baseline'].update(destruction='终局已失能并解体，没有可实施的物理攻击。',durability='终局小机械体被轻触或小石击散，已经失去昔日结构和功能；历史坚固性不计入当前状态。',speed='终局不能主动移动；飞行只属于明确修复后的历史功能。',energy='默认终局不能发出原有光线或调用培养、逆转设施。',mind='历史执行逻辑是把人当作玩具管理；终局未展示可继续行动的独立意识，不能据机器身份声称精神免疫。',stamina='终局失能，没有持续作业；历史供能与维护条件只用于另行声明的修复版本。')
  c['baseline']['intelligence']['in_combat']='终局不能实施战斗；历史资料只供复盘或明确修复版本使用。'
  c['modes']['ordinary']='默认不能行动；若明确修复，则按照旧有玩具管理逻辑观察具体对象。'
  c['modes']['pressure']='默认不能反击；修复版本必须有可用执行端，才可能实施控制。'
  for t in c['logic']['triggers']:
   prefix='仅在明确修复且设备可用时：'
   if not t['condition'].startswith(prefix):t['condition']=prefix+t['condition']
  a=dict(change='需要机械执行体作为行动角色时，明确恢复已失能的最后可运作形态；原作结局和默认评级仍按失能记录。',reason='使历史敌手可以参与新场景，同时不把瓦解状态暗中改成正常。',power_impact='不恢复整套未来统治文明，不自动配置逆转设施；另用历史形态时需重新评估实际装备条件。')
  if a not in c['adaptations']:c['adaptations'].append(a)
  c['rating_input']['positive']={k:v for k,v in zip(['physical','energy','scope','sustain','range','combat'],[0,0,0,0,0,0])}
  c['rating_input']['positive_reasons']={k:'终局失能并解体，不能实际实施昔日功能。'for k in c['rating_input']['positive']}
  for k,v in c['rating_input']['negative'].items():v['score']=0;v['reason']='失能已计入六项正面维度，不重复扣除。'
  c['rating_input']['mastery']='不适用'
  c['rating_input']['theoretical_tier']='纸'
  c['rating_input']['ceiling'].update(tier='纸',description='默认终局失能，无当前可控上限。历史光线、飞行和设施功能仅在明确修复改编中另行评估。',uncontrolled='没有证据表明危急时能够自行恢复旧系统。')
  for a in c['abilities']:
   a['type']='历史能力'
   prefix='历史能力，终局装置已经失能并解体；只有显式修复改编方可启用。'
   if not a['limits'].startswith(prefix):a['limits']=prefix+a['limits']
for batch in ['yuanzhenxia','weisili_mid','weisili_bridge']:
 folder=B/batch
 for p in [folder/'cards.json',*folder.glob('*.cards.json')]:
  cs=json.loads(p.read_text(encoding='utf-8'))
  for c in cs:patch(c)
  p.write_text(json.dumps(cs,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# Keep part_g's source card as evidence input, but remove the duplicate from final aggregation.
p=B/'weisili_bridge/cards.json';cs=json.loads(p.read_text(encoding='utf-8'))
p.write_text(json.dumps([c for c in cs if c['id']!='weisili_chuanghuo_old_leader'],ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for p in [B/'weisili_bridge/coverage.json',B/'weisili_bridge/part_g.coverage.json']:
 cs=json.loads(p.read_text(encoding='utf-8'))
 for book in cs:
  for e in book['included']:
   if e['card_id']=='weisili_chuanghuo_old_leader':e['card_id']='yuanzhenxia_oriental_sun_leader'
 p.write_text(json.dumps(cs,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Root cross-book endpoints and identities synchronized')
