from pathlib import Path
import json, re
ROOT=Path(__file__).parent
SRC=Path(r'C:/Users/mapodoufu/Downloads/NK_Source')
def build(r):
 p=r['path']; bio=r['bio']; name=r['name']; endpoint=r['endpoint']; skill=r.get('skill','未展示超常能力；以观察、交谈和普通人的行动处理眼前问题。')
 ghost=r.get('ghost',False)
 scores=r.get('scores',{'physical':1,'energy':0,'scope':0,'sustain':1,'range':0,'combat':0})
 abilities=[{'name':r.get('ability_name','实际行动与判断'),'type':r.get('ability_type','普通人的经验与选择'),'mechanism':skill,'visual':r.get('visual','表现为注视、交谈、行动及其可观察的结果，不添加特效。'),'applications':r.get('applications',['以本人经验解决与动机直接相关的障碍','意识到危险时求助、离开或利用现有环境','在交流与日常行动中表现原有关系和偏好']),'limits':r.get('limits','没有得到超常战斗能力的证据；知道经历过的事件不等于知道世界上所有同类事件。')}]
 human={'destruction':'以能力段列明的身体行动、器物或异常机制为限，不从身份和动机推导额外破坏力。','durability':'普通人体的穿刺、钝击与环境耐受；没有证明防弹、耐火、耐电或耐腐蚀。' if not ghost else '异常形态的受伤方式未完全写明，不能由身份推出物理免疫或不死。','speed':'以已展示的动作和反应为限，不从叙事紧张程度推导超常速度。','energy':'没有已列异常机制之外的主动能量攻击证据。','mind':'以原作实际心理状态及已列干涉手段为限，不默认精神免疫、读心或支配他人。','stamina':'需要常规休息与照料；未给出可量化的极限或快速恢复。' if not ghost else '异常显现的维持条件和持续上限未明，不默认无限行动或自动恢复。','intelligence':{'in_combat':r.get('combat_intel','以能力段所列实际对抗经验为限，不补齐未展示的战斗体系。'),'knowledge':r.get('knowledge',skill),'planning':r.get('planning','依据本人掌握的信息行动，不把读者知道的真相提前交给角色。'),'adaptation':r.get('adaptation_logic',r['triggers'][0][2])}}
 human.update(r.get('baseline',{}))
 abilities=r.get('abilities',abilities)
 ev=[]
 for evidence_item in r['evidence']:
  ep,a,b,support=(p,*evidence_item) if len(evidence_item)==3 else evidence_item
  n=len((SRC/ep).read_text(encoding='utf-8').splitlines())
  assert 1<=a<=b<=n,(p,a,b,n)
  ev.append({'path':ep,'start_line':a,'end_line':b,'supports':support,'kind':'原文'})
 adap=[{'change':'把原作选择转为可重复遇到的情境扳机；示例行动是演绎接口，不是必须重演的剧情。','reason':'让角色回应当前人物与证据，而非逐条背诵自己的设定。','power_impact':'无新增能力。'}]
 if r.get('revive'):adap.append({'change':'恢复最后可独立行动形态并保留终局记忆。','reason':'原作死亡或失能者如需参战，显式采用回溯式登场；不宣称原作复活。','power_impact':'只恢复原有身体与能力，不获得不死或额外抗性。'})
 adap.extend(r.get('adaptations',[]))
 reasons={k:r.get('reasons',{}).get(k,{'physical':'按文本明确展示的身体或物质作用评分；未给出大范围破坏。','energy':'按已证实的超常作用评分；异常身份或见闻本身不算能量攻击。','scope':'按本人单次可作用的对象与局部场景评分，不把社会地位当物理范围。','sustain':'依赖正常身体、器物或事件条件；没有无限供能或无限复原证据。','range':'按文本中的近身、视线或现有器物接触范围评估，不扩张成全域作用。','combat':'按本人实际解决对抗的表现评分；没有把遭遇奇事自动换算成作战技巧。'}[k]) for k in scores}
 return {'id':r['id'],'name':name,'aliases':r.get('aliases',[]),'series':[p.split('/')[0]],'roles':r.get('roles',['主角']),'version':{'basis':'本批原文剧情结束后的经历与认知','canonical_endpoint':endpoint,'deployment':r.get('deployment','保留终局经历；以最后已证实的可行动状态登场，未随身拥有原文未说明的器材。')},'ooc':r.get('ooc',['不得把未知的怪异机制说成自己随时可控制的能力。']),'terms':r.get('terms',[]),'biography':bio,'appearance':{'description':r['appearance'],'portrayal':r.get('portrayal',r['pressure'])},'role_function':r.get('function',r['motivation']),'modes':{'ordinary':r.get('ordinary',r['motivation']),'pressure':r['pressure'],'reasoning':r.get('reasoning',r['motivation'])},'abilities':abilities,'baseline':human,'passives':r.get('passives',[]),'trump_cards':r.get('trump_cards',[]),'weaknesses':r.get('weaknesses',[]),'logic':{'motivation':r['motivation'],'principles':r.get('principles',['依据自己的经历与关系判断，不替其他人物预先掌握真相。']),'triggers':[{'situation':a,'condition':b,'action':c} for a,b,c in r['triggers']]},'adaptations':adap,'evidence':ev,'confidence':r.get('confidence','high'),'uncertainties':r.get('uncertainties',[]),'rating_input':{'positive':scores,'positive_reasons':reasons,'negative':r.get('negative',{'self_limit':{'score':0,'af':1.0,'reason':'无另行证实且应重复扣分的能力性自限；普通人能力低已计入正向分。'},'environment':{'score':0,'af':1.0,'reason':'未把一般生存环境需求另算特殊限制。'},'volatility':{'score':0,'reason':'无证据表明拥有随机失控的主动战斗能力。'}}),'concept_level':0,'concept_reason':r.get('concept_reason','原文未显示改写世界规则或叙事层的可控权柄；异常事件与知情不等同概念干涉。'),'theoretical_tier':r.get('tier','并' if sum(scores.values())>=6 else '纸'),'mastery':'不适用','ceiling':{'description':r.get('ceiling',skill),'tier':r.get('tier','并' if sum(scores.values())>=6 else '纸'),'uncontrolled':r.get('uncontrolled','未展示可归属于本人、可反复发动的额外不可控上限。')},'rating_confidence':r.get('rating_confidence','medium')}}
def main():
 cards=[]; cov=json.loads((ROOT/'coverage.json').read_text(encoding='utf-8')); by={x['path']:x for x in cov}
 for f in sorted(ROOT.glob('*.draft.json')):
  for book in json.loads(f.read_text(encoding='utf-8')):
   entry=by[book['path']]; entry.update({'status':book.get('status','reviewed'),'included':[],'excluded':book.get('excluded',[]),'notes':book.get('notes',[])})
   for r in book['characters']:
    r['path']=book['path']; c=build(r);cards.append(c);entry['included'].append({'name':c['name'],'card_id':c['id'],'role':'/'.join(c['roles']),'basis':r.get('basis','该人物直接承担本篇行动、冲突或叙事视角。')})
   entry['included'].extend(book.get('external',[]))
 core_path=ROOT/'core_cards.raw.json'
 if core_path.exists():
  for r in json.loads(core_path.read_text(encoding='utf-8')):
   c=build(r)
   c['series']=r.get('series',c['series'])
   c['version']['basis']='综合本语料各书终局经历'
   cards.append(c)
   entry=by[r['path']]
   if not any(x['card_id']==c['id'] for x in entry['included']):
    entry['included'].append({'name':c['name'],'card_id':c['id'],'role':'/'.join(c['roles']),'basis':'核心跨书综合人物；本书为首次可定位的实际行动。'})
 assert len({c['id'] for c in cards})==len(cards)
 canonical_names={c['id']:c['name'] for c in cards}
 for entry in cov:
  for item in entry['included']:
   if item['card_id'] in canonical_names:item['name']=canonical_names[item['card_id']]
 (ROOT/'cards.json').write_text(json.dumps(cards,ensure_ascii=False,indent=2),encoding='utf-8');(ROOT/'coverage.json').write_text(json.dumps(cov,ensure_ascii=False,indent=2),encoding='utf-8')
 short=[(c['id'],len(re.findall('[\u4e00-\u9fff]',c['biography']))) for c in cards if len(re.findall('[\u4e00-\u9fff]',c['biography']))<300]
 print('cards',len(cards),'reviewed',sum(x['status']=='reviewed' for x in cov),'short',short)
if __name__=='__main__':main()
