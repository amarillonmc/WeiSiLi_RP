"""Evidence-led local authoring source; only emits this batch's files."""
from pathlib import Path
import json
OUT=Path(__file__).parent
CARDS=[]
COVER=[]
def E(book,a,b,s):
 return {'path':book,'start_line':a,'end_line':b,'supports':s,'kind':'原文'}
def A(name,mechanism,apps,limits,visual=None,kind='技能'):
 return {'name':name,'type':kind,'mechanism':mechanism,'visual':visual or '以观察、选择动作和实际结果体现，不添加原作没有的光效。','applications':apps,'limits':limits}
def T(s,c,a):return {'situation':s,'condition':c,'action':a}
def W(n,m,v,d,x):return {'name':n,'mechanism':m,'visible':v,'discovery':d,'mitigation':x}
def card(key,name,series,roles,bio,appearance,endpoint,ability,evidence,motivation,triggers,
         scores=(1,0,0,1,0,1),limits=(1,1,0),aliases=(),pressure='',ordinary='',reasoning='',
         weaknesses=(),mind='没有证据表明能抵抗精神控制；意志与专长不是精神免疫。',
         destruction='徒手只能伤害普通人或处理轻小物件，未显示大范围破坏。',
         durability='常人血肉；不能据其声望推定抗枪弹、极温、电击或腐蚀。',
         speed='移动和动作按人类尺度；没有超音速或闪避已发射子弹的证据。',
         energy='没有独立的能量投射能力。',stamina='可完成其专长范围内活动，仍需休息；无无限续航证据。',
         intelligence=None,deploy=None,adapt=None,terms=(),ooc=(),confidence='medium',uncertainties=(),
         theoretical='并',concept=0,ceiling=None):
 if intelligence is None:intelligence={'in_combat':'依据自身专长选择逃离、求助或有限反击，不凭故事地位获得制胜知识。','knowledge':motivation,'planning':reasoning or '会把已知经历用于比较风险，未知部分仍须调查。','adaptation':pressure or '先确认变化的原因和可用资源，再作决定。'}
 pos=dict(zip(('physical','energy','scope','sustain','range','combat'),scores))
 reasons={'physical':destruction+' '+durability,'energy':energy,'scope':'按本人能直接落实的作用范围计；组织、人脉和财富不等于物理覆盖。','sustain':stamina,'range':ability[0]['limits'] if ability else '没有可用于远距战斗的已证据。','combat':intelligence['in_combat']}
 adapt=adapt or [{'change':'将原有选择扩展为下列跨场景行为扳机；即兴台词与小动作只属演绎接口。','reason':'允许由眼前证据产生新反应，而非复述原著台词和情节。','power_impact':'无新增能力。'}]
 c={'id':'mulanhua_'+key,'name':name,'aliases':list(aliases),'series':list(series),'roles':list(roles),
  'version':{'basis':'综合终局经历','canonical_endpoint':endpoint,'deployment':deploy or '采用正文最后稳定可独立行动形态，保留已确认经历；不自动携带朋友的科技或组织全部资源。'},
  'ooc':list(ooc),'terms':list(terms),'biography':bio,'appearance':{'description':appearance,'portrayal':ordinary or '用具体行动和对话表现其立场，不反复自报设定。'},
  'role_function':motivation,'modes':{'ordinary':ordinary or motivation,'pressure':pressure or triggers[0]['action'],'reasoning':reasoning or motivation},
  'abilities':ability,'baseline':{'destruction':destruction,'durability':durability,'speed':speed,'energy':energy,'mind':mind,'stamina':stamina,'intelligence':intelligence},
  'passives':[],'trump_cards':[],'weaknesses':list(weaknesses),'logic':{'motivation':motivation,'principles':['已确认的能力和资源才进入行动判断。',reasoning or motivation],'triggers':triggers},
  'adaptations':adapt,'evidence':evidence,'confidence':confidence,'uncertainties':list(uncertainties),
  'rating_input':{'positive':pos,'positive_reasons':reasons,'negative':{'self_limit':{'score':limits[0],'af':1.0,'reason':reasoning or motivation},'environment':{'score':limits[1],'af':1.0,'reason':ability[0]['limits'] if ability else '身体与具体环境限制'},'volatility':{'score':limits[2],'reason':'不确定性见能力条件与原文结局；不添加无证据的随机失控。'}},'concept_level':concept,'concept_reason':'所示属于生物、技能或有限科技机制；没有改写抽象规则的权柄。' if not concept else '仅按有证据的局部规则作用分析，不推至全能。','theoretical_tier':theoretical,'mastery':'不适用','ceiling':{'description':ceiling or '以卡内明确机制与必要资源可控使用为上限，不叠加推测能力。','tier':theoretical,'uncontrolled':'无已确认的额外不可控战斗形态。'},'rating_confidence':confidence}}
 assert len(bio)>=300,(name,len(bio))
 CARDS.append(c);return c['id']
N='非人协会系列/'
def nc(*args,**kw):return card(*args,series=['非人协会系列'],**kw)
def coverage(path,included,excluded=(),notes=()):
 COVER.append({'path':path,'status':'reviewed','included':[{'name':n,'card_id':i if '_' in i else 'mulanhua_'+i,'role':r,'basis':b} for n,i,r,b in included],'excluded':[{'name':n,'reason':r} for n,r in excluded],'notes':list(notes)})

def save():
 (OUT/'cards.json').write_text(json.dumps(CARDS,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (OUT/'coverage.json').write_text(json.dumps(COVER,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

