from author_library import *
data=json.loads(CARDS.read_text(encoding='utf8')); by={x['id']:x for x in data}
c=by['weisili_chen_yuelan']
c['biography']=c['biography'].replace('她是否接受异星人的脑改造并离开地球，仍属推测，不能写成已经拥有异星全能力。','《祸根》终局证实她已经成为外星人，在遥远地方通过基地的立体投影与女儿相见，承认自己的乖张，却仍拒绝白奇伟前来，随即结束联络。她放心不下红绫，教会外孙女操作飞行背心和基地设备；具体转化过程与新身体的战斗能力没有展示，不能据异星身份拥有全部外星技术。')
c['version']['canonical_endpoint']='《祸根》已成为外星人，在远方经苗疆基地立体投影与白素相见并结束联络；本体具体性能未展示'
c['version']['deployment']='常态以有基地接口的远程投影交流、指导，投影不能触碰物体。若需亲身参战，以明确改编恢复其最后已证实的人类武者形态并保留终局知识；不把未展示的外星肉体强化与旧形态叠加。'
c['abilities'].append(ab('基地通信与操作指导','借外星基地呈现可对话的立体投影，指引红绫使用背心飞行及基地装置','依赖对应设备与本人愿意接通；投影没有实体，无法召唤她强制回应，具体装备不自动随身',kind='有条件设备'))
c['evidence'].append(ev('091',3095,3160,'外星身份、远程立体投影、拒见与指导红绫，明确更正前书猜测'))
c['adaptations'].append({'change':'跨世界需要实体行动时恢复最后已证实的人类武者身体，保留与女儿重逢后的知识。','reason':'原作终局只展示远程投影，没有足以评级的外星本体战斗数据；避免把未知当全能。','power_impact':'不增设异星肉体强化；人类近战评级为这一显式部署形态，远程投影自身没有接触攻击。'})
c['uncertainties'].append('远方身体的材质、寿命、耐久和转化细节未展示；不可从外星称呼推导。')
c=by['weisili_chen_yuemei']
c['biography']=c['biography'].replace('身上的虫物又使猛哥明白这不是可以置之不理的陌生母女。','她已断气，却凭一愿神虫暂时复苏，看了女儿并要求寻找孩子父亲，随即真正死去；这一愿对她已经用尽。信物同时使猛哥承担不可推却的寻找义务。').replace('贵重信物只提供有限社会请求资格，不是随意实现愿望的宇宙法则。','一愿神虫只提供一次有关自身身体行为的助力，同时是向蛊苗族长提出请求的信物，不是任意实现宇宙愿望的法则；终局不再给她第二次使用。')
c['abilities'][0]['limits']='信物的族群请求作用依对方识别和习俗；一愿神虫曾使她短暂复苏，但对她的一次作用已经耗尽，不计常驻技能；没有高明战斗或独立治疗能力。'
c['evidence'].append(ev('089',2400,2460,'一次身体愿望使其暂时复苏并托付寻父，此后对她失效'))
c['terms'].append({'term':'一愿神虫','explanation':'蛊苗稀有虫物，使同一拥有者的一次自身身体行为获得助力，并带来向族长提出请求的习俗约束；月梅已经用过，不能刷新复活。'})
c=by['weisili_hong_ling'];c['evidence'].append(ev('091',3144,3160,'祖母教用背心及基地设备，主动留下背心，不能主动召祖母'))
c['abilities'].append(ab('已学基地操作','陈月兰教会她使用苗疆基地中的装置及飞行背心，能在该设备环境中实际操作','必须回到原基地或取得兼容装置；背心主动留在基地，不是肉身飞行，也没有召祖母显现的方法',kind='设备知识'))
c['biography']+='在苗疆基地，她从已成为外星人的外祖母陈月兰处学到装置操作，表现出不愿把一切秘密立即告诉父母的自主。所会的是有接触和教学依据的设备，并非遇见任意异星机器都自然精通。'
c=by['weisili_bai_su'];c['evidence'].append(ev('099',2288,2292,'反对在小仙私居安装偷拍器，明确无权干涉'))
c['biography']+='《成精变人》中她反对在小仙私居装偷拍设备，明确不能只因好奇就侵犯对方生活；这一界限与她为家人有时越界的选择并存。'
c=by['weisili_tie_dan'];c['evidence'].append(ev('104',1903,1908,'参与十二花培养的背景、失势堕楼断腿与德国隐居的后书叙述'))
c['uncertainties'].append('091以受迫害被打断双腿回述，104写失势堕楼断腿；保留两书表述差异，不另造调和过程。')
c=by['weisili_huang_chan'];c['evidence'] += [ev('104',2663,2679,'伪喇嘛并非卫七所派，黄蝉化装为卫的推测'),ev('104',2699,2713,'阻止公开确认但损失三法物，监视机制仍是推断')]
c['biography']+='转世事件中，她阻止公开确认而失去三件法物，所得有限；伪装喇嘛及以雄海冬青吸引目光、雌隼暗中监视，是卫斯理事后推测，不应写成她亲口承认的全程布局。'
for key in ['weisili_yin_1','weisili_yin_2','weisili_yin_3','weisili_yin_4','weisili_di_ke']:
 if key not in by: continue
 c=by[key];c['evidence'].append(ev('103',2735,2758,'海中电离子层与帐顶装置形成信息死角，非无处不知'))
 c['weaknesses'].append({'name':'信息屏蔽区','mechanism':'某海水电离子层及相似的顶帐装置能够隔绝其信息探测。','visible':'已有探测系统找不到藏于屏蔽区的目标。','discovery':'比较目标进入与离开特定区域的侦测结果。','mitigation':'依靠外部线索寻找出入口；没有文本证实可随意穿透屏蔽。'})
CARDS.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
p=BASE/'coverage.json';rows=json.loads(p.read_text(encoding='utf8'))
r=next(x for x in rows if Path(x['path']).name.startswith('085'))
r['included']=[x for x in r['included'] if x['card_id']!='weisili_bai_su']
r['included'].append({'name':'温妈妈','card_id':'weisili_wen_mama','role':'重要配角','basis':'在家中与老蔡、卫斯理的实际互动并推动开端误会'})
r['excluded'].append({'name':'白素','reason':'本书在苗疆，检索为背景提及或借述，未发现实际参与本案'})
p.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Endpoint corrections and shared supplements saved')
