from author_library import *
cards=json.loads(CARDS.read_text(encoding='utf8'));d={c['id']:c for c in cards}
def get(i):return d['weisili_'+i]
changes={
 'qiu_lun':([2,0,1,4,2,3],(1,1,1),'并','摄影记者的旅行、攀越和观察经验较强，但原文没有高等武术或可靠枪战本领，不能按格斗专家计真实战斗力。'),
 'bu_ping':([3,0,1,5,2,3],(1,1,1),'并','专业登山的力量、耐力和山地经验有实证；技术性攀登不等于近战或枪战训练。'),
 'ma_zuimu':([2,0,1,3,2,3],(1,1,1),'并','强健牧马人的骑行与经营经验，未证实与卫斯理相当的战斗技巧；过去牧场势力不计个人火力。'),
 'zhuo_changgen':([5,0,1,5,2,4],(1,1,1),'强','老年仍有显著力量和骑术，但没有同等级武术对抗展示；财富、父亲药物和守陵者能力不计本人。'),
 'wang_lian':([1,0,1,2,1,3],(1,2,1),'纸','主要依靠信息布局和谈判；141被突袭时甚至未明白遇袭，卫收招自伤不是她的格斗战绩。'),
 'tai_feng':([2,0,1,2,2,4],(1,1,1),'并','军政经验有助判断和调度，未见足以按武术专家评分的个人动作；国家武装属于外部机构。'),
 'gao_tian':([2,0,1,3,2,4],(1,1,1),'并','警务调查与迅速调物证有实证，没有大师级徒手或枪械战绩。'),
 'zeng_yuan':([2,0,1,3,2,4],(1,1,1),'并','刑事调查、现场观察和报告是主要本领，警察身份不自动提供高等个人武技。'),
 'chen_tianhao':([1,0,1,1,2,4],(2,1,1),'并','部署为最后尚能发令的负伤本人；保留判断与组织经验，不能同时恢复完整军队或健康巅峰身体。'),
 'chen_warlord':([2,0,1,2,2,4],(1,1,1),'并','有军事威胁和伏击安排，不等于个人拥有部属的全部攻击，也没有卓越单人格斗实证。'),
 'feifu_laoda':([2,0,1,2,3,6],(1,1,2),'并','晚年仍保留飞斧经验，但身体衰老且没有重现盛年技巧；挡枪传说和过去精密拦截不作为终局稳定防御。'),
 'yu_fang':([2,0,1,2,2,6],(2,1,1),'并','独眼独臂的最后可行动身体保留夜战判断和经验，破坏力、续航与动作选择均受终局伤残限制。'),
 'qingsi_grandmother':([3,0,1,2,2,6],(2,1,1),'并','保留老年家传技巧，但最后形态接近生命末期，不能用早年背负孩子疾驰的耐力覆盖临终状态。'),
}
for i,(values,negative,tier,reason) in changes.items():
 c=get(i);rate(c,values,negative,tier,reason)
 if i in ['qiu_lun','bu_ping','ma_zuimu','wang_lian','tai_feng','gao_tian','zeng_yuan','chen_warlord']:
  c['baseline']['destruction']='按本人的常规身体与实际工具计；没有独立大型破坏或高级武术证据，专业、职位和部属不能直接换算火力。'
  c['baseline']['speed']='人类反应与运动；专业判断、组织调度和交通工具速度不算个人高速移动。'
  c['baseline']['intelligence']['in_combat']=reason
get('wang_lian')['ooc'].append('卫斯理对王主任突然收招造成的自伤，不是王莲出手击伤他的战绩。')
get('chen_tianhao')['baseline']['stamina']='最后能自主发令时已中枪濒死，需照护，不能作健康军人连续冲锋。'
get('yu_fang')['baseline']['stamina']='独眼独臂且受迫害的最后可行动身体，体力与双侧动作受限；不恢复盛年完整身体。'
get('qingsi_grandmother')['baseline']['stamina']='生命末期老年形态，保留技巧和判断；早年老者仍能背孩子疾驰的展示不保证临终可以重演。'
get('tianjia')['baseline']['stamina']='终局脑癌病体，保留最后可交谈决策状态；不能恢复先前驾驶和探洞时的体能。'
get('tianchi')['rating_input']['positive_reasons']['sustain']='灵体长期存在与精神修行经验，不是持续施展攻击的时间；现有记分只反映无需肉体补给的条件优势。'
get('cao_puzhao')['baseline']['stamina']='终局灵体无普通进食休息模式；持续借身或传话的条件与极限不明，不推定永远可显现。'
get('yin_4')['baseline']['stamina']='脑信息作用依赖实际残余思想仪的运行和能量；本体生理及独立持续输出时长未知。'
get('immortal_master')['baseline']['destruction']='未显示徒手杀伤；已展示的是局部空间阻隔与转送，不能由修行称号推导任意物质毁灭。'
get('tomb_giant')['baseline']['destruction']='历史巨大身体与建陵技术不能直接换算当前攻击；本篇只以远距通讯投影出现，没有个人破坏力实绩。'
get('shen_wansan')['baseline']['energy']='有依附物件与灵魂沟通现象，未展示稳定伤人的能量输出。'
get('gong_yun')['baseline']['stamina']='最后可核为盲眼老年修行者，离地后形态与续航未说明；不能按长寿或受接引推定无限活动。'

# Explicitly record restoration adapters already stated in deployment, without changing the source endpoint.
restored=[]
for c in cards:
 v=c['version']['deployment'];a=json.dumps(c['adaptations'],ensure_ascii=False)
 if ('恢复' in v or '复原' in v) and ('恢复' not in a and '复原' not in a):
  c['adaptations'].append({'change':'用于互动时采用版本栏明确的最后可行动形态，并保留已知终局记忆。','reason':'原作中的死亡、失能或失踪仍成立；需要行动时明确区分部署适配和原作事实。','power_impact':'只恢复版本栏指定的本人状态，不重建失去的组织、同伴、设备或互斥形态。'})
  restored.append(c['id'])
 # Normalize template limits now that source records, not just rendered output, will be used by other projects.
 if not c['weaknesses']:
  limits=list(dict.fromkeys(x['limits'] for x in c['abilities']))
  c['weaknesses']=[{'name':'已证实能力的条件','mechanism':'；'.join(limits),'visible':'当上述条件不足时，行动受阻、效果缩小或需要实际协作。','discovery':'观察行动结果或询问条件，不默认对手已经知道全部卡片。','mitigation':'确认和补足现有条件，改变方案或求助；不临时新增免疫取消限制。'}]
 elif isinstance(c['weaknesses'][0],str):
  c['weaknesses']=[{'name':'已记录限制','mechanism':s,'visible':'触及限制时以相应行动困难体现，不额造症状。','discovery':'通过实际观察和线索核实。','mitigation':'改用本人已有的办法或取得帮助，不增设能力。'} for s in c['weaknesses']]
CARDS.write_text(json.dumps(cards,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(BASE/'rating_audit.json').write_text(json.dumps({'adjusted':list(changes),'restoration_adapters':restored,'scope':'本批评分与终局状态一致性复核；不修改原文。'},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Adjusted',len(changes),'ratings; recorded',len(restored),'existing restoration deployments')
