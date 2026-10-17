"""Apply source-backed cross-series additions to root-owned authoring records."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=Path('C:/Users/mapodoufu/Downloads/NK_Source/卫斯理系列')
def ev(prefix,a,b,s):
 p=next(p for p in SRC.glob('*.txt') if p.name.startswith(prefix))
 return dict(path='卫斯理系列/'+p.name,start_line=a,end_line=b,supports=s,kind='原文')
updates={
 'yuanzhenxia_qinglong':dict(
  biography='在《瘟神》中，青龙成为主宰会新任东南亚联络员。他向上层谎报卫斯理与照片无关，以保护旧友，明知这样做会承担欺瞒组织的风险。这使他的组织身份与私人情义形成持续冲突，而非只有无条件服从。',
  endpoint='后在《瘟神》任主宰会东南亚联络员，冒险隐瞒卫斯理牵涉照片的事实以护友；不把组织整体力量计作个人随身能力。',
  refs=[ev('076',4470,4487,'组织处置与任职'),ev('076',4665,4687,'为护卫斯理隐瞒实情')]),
 'yuanzhenxia_hanliemi':dict(
  biography='《毒誓》中，他因找不到原振侠而转向卫斯理，为保护古物接受酋长委托，协助判断水晶女尸的来历，并安排金月亮前往勒曼医院，自己留下安抚酋长。《拼命》后续说明，酋长得到第二个复制金月亮后，给予他巨额考古资助；这种资助不代表他掌握复制生命的技术。',
  endpoint='在《毒誓》《拼命》继续考古与协调救援，留下安抚酋长，后来获得考古资助；勒曼的复制技术属于外援。',
  refs=[ev('083',2261,2334,'经胡明求助卫斯理'),ev('083',2383,2424,'体格与保护古物'),ev('083',2636,2655,'水晶女尸线索'),ev('083',2780,2844,'联络医院及安抚'),ev('084',763,765,'后续考古资助')]),
 'yuanzhenxia_su_yaoxi':dict(
  biography='在《毒誓》的古物与慈善拍卖线中，苏耀西仍以相关交往和事务协助参与，延续其人脉与办事经验；这不等于拥有拍品或拍卖参与者的超常能力。',
  refs=[ev('083',1024,1040,'古物及慈善拍卖协助')]),
 'weisili_gao_caihong':dict(
  biography='《规则》再现她与王居风的旅行：两人曾救助一个断腿刀手，受袭后借时移脱离；又在张拾来的经历中提供枪械并出面解围。卫白从录像认出他们，温宝裕试图召唤却未取得联系。具体救助和失联并存，不能把朋友呼叫等同于必然到场。早在《支离人》她还是白素十六岁的表妹，与电脑伊乐笔谈，并与麦隆上尉相恋；这段早期恋情不能误记为王居风。',
  refs=[ev('019',15,21,'年龄与亲属关系'),ev('019',539,554,'麦隆身份'),ev('019',1533,1537,'早期关系'),ev('071',2657,2749,'救人、受袭及脱离'),ev('071',2948,2977,'录像认人'),ev('071',3264,3335,'后续援助与无法联络')]),
 'weisili_wang_jufeng':dict(
  biography='《规则》中他与高彩虹继续旅行，救断腿刀手后遭袭而离去，又在张拾来的经历中提供枪械和解围；其影像被卫白识别。温宝裕后来不能仅凭召唤把二人叫来，说明旅行并不提供所有朋友随时可用的救援渠道。',
  refs=[ev('071',2657,2749,'援助与遭袭'),ev('071',2948,2977,'录像识别'),ev('071',3264,3335,'解围和联络限制')]),
 'weisili_jina_jidu':dict(
  biography='在《奇门》的少年阶段，她十一二岁，能接待访客、补寄母亲的信、协商父亲遗物并帮助检视记录。母亲被杀后她失踪，这才连接到《天书》的再会；少年时期没有已证实的独立超常能力。',
  refs=[ev('016',71,105,'少年接待'),ev('016',129,134,'寄信'),ev('016',945,1028,'遗物和记录'),ev('016',2735,2740,'母亡失踪')])}
for cid in ['yuanzhenxia_chen_jingde','yuanzhenxia_chen_yixing','yuanzhenxia_fang_ruhua','yuanzhenxia_fang_siyu']:
 updates[cid]=dict(
  biography='后在《怪物》中，四人参与电脑异常调查，其中一半失去正常神智，另一半同步感到分裂与被拉扯。卫斯理据此推断其记忆被电脑攫走。他们已联络原先的研究者，准备通过另一半的记忆帮助恢复，结尾尚未直接展示恢复完成；把人类记忆送入电脑能够阻止暴走，也只是设想。',
  endpoint='《怪物》参与调查后，一半失去神智，另一半有同步感受，四人准备前往旧研究者处修复；恢复结果未展示。',
  refs=[ev('085',3091,3117,'同步感受和记忆被攫的推断'),ev('085',3121,3134,'冒险动机和准备求助')])
changed=[]
for batch in ['yuanzhenxia','weisili_mid']:
 folder=ROOT/'data/character_batches'/batch
 for p in [folder/'cards.json',*folder.glob('*.cards.json')]:
  cards=json.loads(p.read_text(encoding='utf-8'));dirty=False
  for c in cards:
   u=updates.get(c['id'])
   if not u:continue
   if u['biography'] not in c['biography']:c['biography']+=u['biography'];dirty=True
   if 'endpoint' in u and c['version']['canonical_endpoint']!=u['endpoint']:c['version']['canonical_endpoint']=u['endpoint'];dirty=True
   if '卫斯理系列' not in c['series']:c['series'].append('卫斯理系列');dirty=True
   for e in u['refs']:
    if e not in c['evidence']:c['evidence'].append(e);dirty=True
  if dirty:p.write_text(json.dumps(cards,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');changed.append(str(p.relative_to(ROOT)))
print('Updated',len(changed),'files')
