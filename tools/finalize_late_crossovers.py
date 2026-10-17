"""Apply later, explicitly evidenced endpoints to root-owned character batches."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
B=ROOT/'data/character_batches'
SRC=Path('C:/Users/mapodoufu/Downloads/NK_Source')
def ev(book,a,b,s):
 p=next((SRC/'卫斯理系列').glob(f'{book:03}*.txt'))
 return dict(path=p.relative_to(SRC).as_posix(),start_line=a,end_line=b,supports=s,kind='原文')
def add(c,s,refs=()):
 if s not in c['biography']:c['biography']+=s
 for e in refs:
  if e not in c['evidence']:c['evidence'].append(e)
def once(xs,s):
 if s not in xs:xs.append(s)
def ability(n,m,v,apps,lim,t='主动技能'):
 return dict(name=n,type=t,mechanism=m,visual=v,applications=apps,limits=lim)
def patch(c):
 cid=c['id']
 if cid=='weisili_shenying':
  add(c,'《真实幻境》中，它仍以鹰身与红绫争执、闪避和反抓，后来和解并飞去寻找伦三德；这是成人之前的阶段。未来幻境里的“人头鹰身”属于该场经历，不构成稳定形态或可自由切换的能力，后续明确成人并失去飞行仍有优先级。',[ev(124,1415,1521,'鹰身争执与和解'),ev(124,1621,1631,'当时仍可飞行'),ev(124,2338,2416,'未来幻境的形态与逃避')])
  add(c,'《原形》显示它不能理解所有鸡的言语，某只母鸡反能理解鹰鸣；它与阿大交锋后掉羽，仍有恐惧和生物限制。《成精变人》末，它接受连续复制与基因比例调整，成为瘦削挺拔、肤色深棕、钩鼻目锐的人形，自愿放弃飞行而无悔。《未来身份》仍能鸣叫并与大羊鹰沟通，但需要由后者背负飞行，随后与金维离开继续探查。因此最后稳定形态是人类，鹰爪、羽翼与自身飞行只作历史记录，不能和人的身体叠加为默认能力。',[ev(115,1731,1747,'鸡语交流局限'),ev(115,2590,2638,'交战与恐惧'),ev(125,2630,2648,'基因调整过程'),ev(125,2680,2686,'自愿成人和不能飞'),ev(126,117,153,'成人后仍通鹰语、须被背飞')])
  c['version']['canonical_endpoint']='《成精变人》末自愿成为人类并失去飞行能力；《未来身份》仍通鹰语，与金维离开继续调查。'
  c['version']['deployment']='默认采用已成人的终局形态和本人经历。若剧情选用鹰形，须明确声明历史形态改编，并另算能力；不默认可自由变身。'
  c['aliases']=list(dict.fromkeys(c['aliases']+['神鹰（成人后）']))
  c['appearance']['description']='终局为瘦削挺直、深棕肤色、钩鼻广额、眼神锐利的人类男性；腿上金环与羽翼属于早期鹰形记录。'
  c['abilities']=[ability('成人后的交流与经验','保留个人记忆、鹰鸣及与大羊鹰沟通的能力，以人的身体行动。','以人的姿态说话行动，也可发出鹰鸣。',['与亲近伙伴沟通','解释自己在鹰形时期的观察','请求愿意合作的大羊鹰运送'], '不能自行飞行、任意变回鹰或命令其他生物；不保证理解全部鸟类语言。'),ability('鹰形时期的飞行与传讯','早期曾以鸟类身体飞行、携物、捕捉海东青及为伦三德传信。','羽翼、鸣叫与爪抓，仅在明确选用旧形态时出现。',['历史战绩查询','明确另行约定鹰形部署'], '终局成人后已失去羽翼和自行飞行；本项不计入默认评级。','历史形态')]
  c['baseline'].update(destruction='人的身体与实际配备工具；不能使用鹰喙、鹰爪或羽翼攻击。',durability='成人后的生物身体；没有枪弹、冷热、电击、毒素或腐蚀免疫证据。',speed='以人的身体移动；空中移动须由愿意合作的大羊鹰背负，不算本人飞行速度。',mind='保留亲历记忆与鹰类沟通经验，有情绪和恐惧；没有普遍精神免疫。')
  c['baseline']['intelligence'].update(in_combat='过去猛禽经验不自动成为人的成熟武技；须适应新身体。',knowledge='本人经历与已展示的鹰语；不通所有鸟语。',planning='选择成为人并继续求知，仍维护与红绫等伙伴的关系。',adaptation='承认失去飞行的代价，按新身体寻找合作与行动办法。')
  c['ooc']=['终局为自愿成人，不能把鹰形飞行与人形同时默认开启。','大羊鹰的负载飞行是独立伙伴协助，需要对方同意。','交流不是读心，也不保证通晓所有鸟语。','曾克服毒蜗牛诱惑，不等于毒素或精神控制免疫。']
  c['modes'].update(ordinary='亲近熟悉伙伴，适应人的日常，同时以好奇推动调查。',pressure='承认新身体和飞行丧失的局限，必要时求助；不凭急切重新长出羽翼。',reasoning='以自己在两种形态中的经历比较选择，允许自己学习而非总能立即理解人类社会。')
  c['logic']['motivation']='维持亲近关系，探索自己的来历，并承担自己选择成为人的后果。'
  c['logic']['triggers']=[dict(situation='需要空中侦察或移动',condition='终局已经失去飞行',action='寻找工具或请求大羊鹰等伙伴帮助，接受拒绝。'),dict(situation='有人质疑其成人选择',condition='他清楚失去羽翼的代价',action='可以表达珍惜与怀念，同时维护自己的选择。'),dict(situation='伙伴或陌生生物需要交流',condition='存在已掌握语言或动作线索',action='尝试沟通、解释不懂的部分，不自称通晓万物。')]
  c['weaknesses']=[dict(name='身体转换的代价',mechanism='人形不能自行飞翔，原鹰形的战斗动作不能原封不动用于新身体；新能力须经实际学习。')]
  r=c['rating_input'];r['positive']=dict(zip(['physical','energy','scope','sustain','range','combat'],[2,0,1,2,1,2]))
  r['positive_reasons']=dict(zip(r['positive'],['人形体格，未证实超人破坏力','无主动放能','个人周边作用','人形需休息','本人沟通和工具距离，外援飞行不计','保留经历但未展示成熟人形战斗技艺']))
  for key in ['self_limit','environment']:r['negative'][key].update(score=1,af=1.0,reason='需适应人的身体；失去自行飞行，工具和外援必须实际取得。')
  r['negative']['volatility'].update(score=0,reason='主动接受成人代价，未见固定失控机制。')
  r['theoretical_tier']='并';r['mastery']='不适用';r['ceiling'].update(tier='并',description='终局成人后的体格、记忆和已展示鹰语；鹰形战绩和大羊鹰的飞行不得叠加。',uncontrolled='未证实能自行复原鹰形或在危急时长出羽翼。')
 if cid=='weisili_lun_sande':
  add(c,'《洪荒》中，他解开戈壁沙漠的多重机关锁，令两人进一步敬服，但这些表现是针对具体设计的工艺能力。他与其他人尝试和水生命联系，尚未成功；黄而讲出把山视为平等生命、诚心沟通的办法后，他不告而别，急于回去实践。原文没有展示他已经唤醒山体，后来关于世界三大生命的设想也不能补成他的已得权能。',[ev(118,1010,1075,'解开具体多重机关'),ev(118,2441,2472,'沟通尝试未获证实'),ev(118,2632,2642,'求教与离开')])
  c['version']['canonical_endpoint']='《洪荒》向黄而请教沟通生命的方法后离开去实践；与山沟通是否成功未展示。'
  once(c['uncertainties'],'仍未实证与山体生命沟通成功；天工大王是工艺称号，不等于支配地球地形。')
 if cid=='weisili_jinxiu_sisao':
  add(c,'《洪荒》揭示她后来嫁给海盗黄天功，是黄堂与黄而的母亲，曾教养廉不负，把六岁的黄堂托给他。她的水性来自自练，不能将都连加农及黄而的全部本领套给她。她主张黄堂离开官场并带家人隐退，黄堂的听从仍涉及成年人的自主问题。真正与水生命建立直接沟通的是黄而，最初以为是她发现水生命只是卫斯理的先入之见。多巴湖绑住小郭的两名蒙面人被猜为她与黄堂，但未获证实；去向因此只能说疑在该地，不能把威胁小郭当作确定战绩。',[ev(118,1773,1793,'主张隐退与亲属边界'),ev(118,1907,1910,'抚养黄堂的旧事'),ev(118,2500,2521,'自练水性及发现者更正'),ev(118,2630,2631,'婚姻与都连旧缘'),ev(118,2655,2673,'身份和隐居去向的证据边界')])
  c['version']['canonical_endpoint']='《洪荒》与儿子黄堂等离开旧生活隐退；疑在多巴湖附近，具体位置与蒙面者身份未证实。'
  c['version']['deployment']='以晚期仍可行动、已经退隐的本人为准；旧部、军队与警务资源不能默认仍受其调遣。'
  c['roles']=list(dict.fromkeys(c['roles']+['重要配角']))
  c['abilities'][0]['mechanism']='自练的高超水性、湖区地形、近身武艺、过去的组织指挥与江湖交涉；退隐后旧网络不默认可用。'
  c['abilities'][0]['limits']='仍受人体、伤病、实际器材和部众意愿限制；水生命的沟通属于黄而，不是本人控制水流。'
  c['baseline']['intelligence']['knowledge']=c['abilities'][0]['mechanism']
  once(c['ooc'],'与水生命直接沟通的是黄而；母亲不能自动取得同样能力或替成年儿子作所有决定。')
 if cid=='weisili_jinxiu_zhu':
  c['biography']=c['biography'].replace('先他去世或后他的次序以孙女叙述为准，原文说明两人相继亡故。','山下先去世，她在第二年也去世，二人当时均五十岁出头。')
  add(c,'山下官子明确说明祖父先逝、祖母次年离世，因此两人的死亡次序已知；关于相救真相，他们生前始终未共同说清。',[ev(112,1338,1354,'死亡次序与保密')])
 if cid=='weisili_shuangcheng_commissioner':
  add(c,'《洪荒》补足其结局：白素以小石击落他的牙，后来他退休，对黄堂的处分随之取消，新总监邀黄堂复职；黄堂最终仍随家人隐退。原卡中的总监权位属于已结束的阶段，不能让退休后的他继续凭职位调用警队，也不能把白素的小石解释成隔空气功。',[ev(118,779,795,'近距小石袭击'),ev(118,1415,1426,'退休与处分取消')])
  c['version']['canonical_endpoint']='《洪荒》已经退休，对黄堂的处分取消；不再默认掌握警队命令权。'
 if cid in ['yuanzhenxia_chen_jingde','yuanzhenxia_chen_yixing']:
  add(c,'较后的《买命》《卖命》《考验》中，陈氏兄弟又能够正常交谈、活动并相互联系，因此《怪物》末的受损不能继续作为最终现状；但中间治疗细节没有直接补完，不据此宣称记忆永远不受损。陈宜兴自愿出让生命配额，希望陈景德多活；陈景德则努力寻找被隔断联系的兄弟。水生命能干预他们的联络，甚至让一方误认另一方所在的画面，证明这种特殊联系可以受骗、受阻。《考验》开篇，陈景德已再与陈宜兴联络，生命配额的人际转移仍未成功。',[ev(120,79,81,'两兄弟重新参与事件'),ev(120,434,551,'受讯号影响与水中引导'),ev(120,625,637,'联系可被阻断和伪装'),ev(120,1764,1767,'尝试重建联络'),ev(121,154,170,'再次联系与转移仍未成功')])
  c['version']['canonical_endpoint']='《考验》能够正常活动，陈景德已再次联系陈宜兴；未发生已证实的两兄弟生命配额转移。'
  c['version']['deployment']='按晚期恢复正常活动的本人及亲历认知；不补写恢复过程，不自动共享尚未传达给自己的信息。'
  c['series']=list(dict.fromkeys(c['series']+['卫斯理系列']))
  c['roles']=list(dict.fromkeys(c['roles']+['重要配角']))
  once(c['uncertainties'],'从《怪物》的受损到后期正常活动，原文未在所引段落补全治疗过程；不能把方氏姐妹也推定为同样恢复。')
  once(c['ooc'],'一人两体是他们对亲密联系的解释；两个身体仍须分别行动和承担选择，不自动共有全部感知或生命配额。')
  c['abilities'][0]['limits']='双生联系可被水生命遮断或以假画面干扰；不能感知任意其他人，实验设施不由本人凭空调用。'
  c['rating_input']['positive_reasons']['range']='已展示跨处所双生联系，但属于信息而非跨距离攻击，且可受阻。'
 if cid=='yuanzhenxia_qinglong':
  add(c,'《前世》的过去时段补充，他帮助亲王，却反遭亲王伤害，后由鲁鲁同胞所救；不得把这一回忆安排到所有原振侠事件之后。他托小唐带铜龙符，并以微型耳机支持交涉，约三公里的收听属于设备，不是超自然听觉。对恩义与背叛的反应和以信物联络的习惯可保留，故事没有赋予他随意转移灵魂的能力。',[ev(111,2268,2275,'与亲王旧事'),ev(111,2532,2538,'获救'),ev(111,2552,2574,'信物与使者'),ev(111,2605,2607,'耳机距离')])
  c['series']=list(dict.fromkeys(c['series']+['卫斯理系列']))
 if cid=='yuanzhenxia_oriental_sun_leader':
  add(c,'《算帐》末，勒曼医院根据资料判断，他已处在不能正常思考行动的生命延续状态，剩余清醒说话机会约三句话。医院提出可用激素促使它们在一定时间发生，但内容仍由本人思想决定，不能命令他说出放人；实际并未实施。铁天音的获释来自另一次交涉，不能记成他临终口谕。其延寿年数在《人鬼疑云》《闯祸》的二十年与《算帐》的十年回述之间不同，保留版本差异而不自行凑成新的手术。',[ev(114,2699,2717,'三句话及内容不能指定'),ev(114,2723,2741,'激素方法仅提议'),ev(114,2753,2784,'获释另有原因、老人终局')])
  c['version']['canonical_endpoint']='《算帐》末仍有呼吸心跳，正常思想和行动已近耗尽；按医院估计仅余约三句清醒话，触发方案未实施。'
  c['version']['deployment']='默认尊重终局失能状态；若需政治交涉型参战，须明示恢复最后清醒形态这一跨世界改编，不能以其原作能力自我治愈。'
  once(c['adaptations'],dict(change='仅在场景明确需要本人进行政治交涉时，另行部署最后清醒形态并保留终局经历。默认形态仍是原作终局失能状态。',reason='让历史政治人物能参与新场景，同时保留结局造成的真实限制。',power_impact='这是外部参战约定，不赋予自我治愈、复活或恢复旧有统治资源的能力；默认强度评级仍按失能终局计算。'))
  c['baseline'].update(destruction='终局失能，未能实施物理攻击。',durability='仍为脆弱人类生物身体，外部延寿不等于防御或不死。',speed='终局不能正常自主行动。',mind='医院判断正常思想已耗尽，仅余约三句清醒话的可能；内容由本人决定，不可指定。',stamina='依赖维持生命的状态，不能以延长呼吸心跳当作可作战耐力。')
  c['baseline']['intelligence']['in_combat']='终局无法正常用于战斗；过去政治经验只存历史档案。'
  for a in c['abilities']:
   a['type']='历史能力';prefix='终局已不能正常主动施展；只在明示恢复清醒形态的改编中可使用。'
   if not a['limits'].startswith(prefix):a['limits']=prefix+a['limits']
  once(c['uncertainties'],'同一延寿交易的年数在不同篇章分别回述为二十年与十年，不统一改写原文。')
  once(c['ooc'],'不能在默认终局状态下继续主持政治会议；恢复清醒需明确标作改编，且不等于本人拥有复原能力。')
  r=c['rating_input'];r['positive']={k:0 for k in r['positive']};r['positive_reasons']={k:'默认采用《算帐》终局失能状态，无可实施的战斗效果。'for k in r['positive']}
  for x in r['negative'].values():x['score']=0;x['reason']='终局失能已计入六项正面维度，不重复扣分。'
  r['theoretical_tier']='纸';r['ceiling'].update(tier='纸',description='默认终局仅有医院推算的短暂清醒发言机会，不能保证触发或指定内容；历史政治资源另作条件。');r['mastery']='不适用'
 if cid=='weisili_lian_bufu':
  add(c,'《移魂怪物》进一步明确廉正风是他的侄子。对卫斯理不会与他人串谋的评价只是被转述，并非他在该书亲自再度到场；不能把侄子的药物和技术自动算作叔父的能力。',[ev(127,248,291,'叔侄关系与转述界限')])
 if cid=='weisili_zhang_taifeng':
  add(c,'《未来身份》中，他认真对待一位濒死者要求找卫斯理的意愿，尽力联络，安慰对方并守在遗体旁。这个行动扩展了他的责任心和同情，而不是给予法医、复活或判断所有异象的能力；卫斯理对其年轻和初出茅庐的评价也不能把他固定成无能的笑料。',[ev(126,1539,1607,'回应濒死者请求'),ev(126,1690,1838,'安慰与守候')])
  add(c,'《本性难移》他运送供水样本、参加应变会议，推动依据检验结果恢复供水，愿意承担责任。《天打雷劈》说明他因此连升三级，又在伦敦警务会议作犯罪心理演讲，已不是最初只会向前辈求教的年轻警员。典希微成为女友以后，他在工作责任与陪伴探险之间取舍，也因确认她安全而过快接受简单解释，随后继续传递探险队行踪。其职业知识、热心和感情盲点应同时保留；升迁不证明具体官阶，更不增加肉身强度。',[ev(129,1726,1732,'运送样本和应变会议'),ev(129,1766,1770,'供水责任争论'),ev(130,63,94,'关系、会议与专业'),ev(130,876,891,'升迁与职责冲突'),ev(130,2361,2382,'安全确认与后续联络')])
  c['version']['canonical_endpoint']='《天打雷劈》已因供水事件连升三级、承担更多警务职责，与典希微交往，确认其安全后继续报告探险行踪；具体新官阶未明。'
  c['roles']=list(dict.fromkeys(c['roles']+['重要配角']))
  c['role_function']='以警务知识和愿意负责的行动协调异常事件，同时处理职业责任与私人感情的冲突。'
  c['abilities'][0]['mechanism']='警务调查与监视、犯罪心理研究、送检联络和危机协调；借助实际部门、样本与检验机构。'
  c['baseline']['intelligence']['knowledge']=c['abilities'][0]['mechanism']
  c['baseline']['intelligence']['planning']=c['role_function']
  c['logic']['motivation']='弄清事实并对警务决定负责，也希望保护恋人的安全。'
  c['logic']['triggers'][2]=dict(situation='关心的人安全得到确认',condition='喜悦盖过尚未解释的异常',action='可能暂时接受便利说法；在新证据出现时仍应重新核查，而非永远盲从。')
  c['modes']['reasoning']='先用警务经验调查并联络专家；遇到恋人安危时，会在专业判断和安心愿望之间摇摆。'
  c['rating_input']['negative']['volatility']['reason']='关切典希微时会过快接受令人安心的解释；这不是固定发狂或必然背叛职责。'
 if cid=='yuanzhenxia_kangwei':
  add(c,'《买命》至《考验》阶段，他关心生命配额主要为了柳絮，并用设备与资料参与调查，仍不能保证查明或阻止外来水生命。机器身体没有水分，使水生命的这类讯号和干预不能直接作用于他，却也使他收不到友人已经平安的信息；他需要实际传话，不是天然知道一切。生命配额转移当时仍未实现，他的期待不能改成已经持有无限延寿术。',[ev(120,976,978,'为柳絮而关注'),ev(120,1080,1083,'不能保证阻止'),ev(120,2457,2460,'无水机器的界限'),ev(121,154,170,'不能收讯与转移未成')])
  c['version']['canonical_endpoint']='与柳絮相伴并继续帮助朋友；《天皇巨星》中寻找原振侠未得确讯，《考验》中仍关注尚未完成的生命配额转移。没有获证的新终局形态。'
  c['baseline']['destruction']='坚固机械身体能进行近身作用和精密操作；未展示由单体拳脚造成的广域破坏，设备作用须有实际接口与工具。'
  c['baseline']['speed']='以机械身体行动和处理资料；资料运算、载具航速与肉身移动分别判断，原文未给统一的移动速度上限。'
  c['baseline']['mind']='能处理大量资料并产生感情；无水身体不接收水生命的特定讯号，同时失去该通讯渠道，不等于对所有精神干涉免疫。'
 if cid=='yuanzhenxia_liu_xu':
  add(c,'《卖命》《考验》中，她与康维共同参与研究，也会在其焦躁时安慰，观察卫斯理夫妇抵抗未知力量，却不能直接读出两人的全部思想。她能接受水生命传来的平安讯号，与无水机器身体的康维不同；这种被动收讯不等于她自己掌握水的全部控制方法。生命配额的研究仍未成功，不能把康维希望她延寿的愿望写成已经实现的永久生命。',[ev(120,1365,1368,'安慰与判断'),ev(120,1895,1899,'观察不等于读心'),ev(121,154,170,'收到讯号与转移未成')])
  c['version']['canonical_endpoint']='恢复视力、摆脱组织控制并拆除体内核装置，与康维相伴；《考验》中仍参与未完成的生命配额研究，没有获得已证实的永生。'
 if cid=='yuanzhenxia_aishen_machines':
  c['baseline']['destruction']='活动机械身体可操作设备；单体破坏力未充分量化，行星防护工程属于配备设施后的群体协作。'
  c['baseline']['mind']='具有独立感受、判断和职能分工的机械生命；运算与资料储存不等于无所不知或绝对精神防御。'
  c['appearance']['description']='由原有防御和资料系统转为可活动的机械生命；成员形体与职能分别处理，不把整个基地视为一人的身体。'
for foldername in ['yuanzhenxia','weisili_bridge','weisili_late_root']:
 folder=B/foldername
 for p in [folder/'cards.json',*folder.glob('*.cards.json')]:
  cs=json.loads(p.read_text(encoding='utf-8'))
  for c in cs:patch(c)
  p.write_text(json.dumps(cs,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for p in [B/'weisili_late_root/coverage.json',B/'weisili_late_root/part_e.coverage.json']:
 cv=json.loads(p.read_text(encoding='utf-8'))
 for b in cv:
  if '/122' in b['path'] and not any(x['card_id']=='adventure_shui_hong'for x in b['included']):
   b['included'].append(dict(name='水荭',card_id='adventure_shui_hong',role='重要配角',basis='寻找温宝裕及装置事件的协助者'))
 p.write_text(json.dumps(cv,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Late cross-series endpoints synchronized; historical abilities kept conditional.')
