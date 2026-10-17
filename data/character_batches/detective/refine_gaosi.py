from pathlib import Path
import json
P=Path(__file__).parent
p=P/'gaosi_i.py'
s=p.read_text(encoding='utf8').replace('陷害堂兄','陷害陈生发')
p.write_text(s,encoding='utf8')
p=P/'gaosi_a.py'
s=p.read_text(encoding='utf8')
marker="(P/'gaosi_a.draft.json').write_text"
extra="""
# All-series evidence added after reading the later books; these are ordinary
# bodily skills and situational feats, not permanent invulnerability.
for c in books[0]['characters']:
 if c['id']=='gaosi_gao_si':
  c['skill']='专业摄影和暗房处理、观察推理；有西洋拳、驾驶、潜水、简单锁具开启与瑜珈静息经历，各依身体、设备及现场条件。'
  c['evidence'].extend([('神探高斯系列/27亚洲皇后.txt',377,424,'共同以静卧、瑜珈和节食减耗，仍几近死亡'),('神探高斯系列/28妖女煞星.txt',271,302,'误把真枪当玩具，受伤须手术'),('神探高斯系列/29预告.txt',243,249,'用铁丝开启简单门锁'),('神探高斯系列/29预告.txt',382,468,'摄影分析成功，但把嫌疑当结论遭纠正')])
  c['baseline']['stamina']='曾在《亚洲皇后》以静卧、瑜珈及严格分配少量食水支撑多日，但随后衰弱至几乎不能行动；这段小说表现不等于辟谷、无限续航或普遍生存保证。'
  c['applications']=['从光线、镜头和角度检验照片与叙述的矛盾。','在具备工具和机会时进行摄影、驾驶、潜水或简单开锁，承担被发现及失误风险。','遭拘禁时利用伪装、节约体力或临时求援争取机会；实际伤病仍需救治。']
  c['limits']='摄影判断和推理均可能失误；会中枪、饥渴和受骗。简单开锁不等于开启所有锁具，瑜珈不赋予辟谷或不死，武器只在实际持有时可用。'
 if c['id']=='gaosi_li_yufang':
  c['skill']='刑事调查、化装跟踪、警务组织、手枪射击和近身制敌；曾以瑜珈静息及配给管理延长囚禁中的生存，仍须真实身份、身体和装备条件。'
  c['evidence'].extend([('神探高斯系列/27亚洲皇后.txt',377,424,'严格分配食水与静息求生，仍严重衰弱'),('神探高斯系列/27亚洲皇后.txt',445,479,'借高斯扑击机会击杀巡查者，随即力竭'),('神探高斯系列/28妖女煞星.txt',341,434,'调查亲近者不徇私，但也有先入怀疑'),('神探高斯系列/29预告.txt',539,674,'继承事实、假救援与逐层纠正嫌疑')])
  c['baseline']['destruction']='持手枪可击伤人体；在地窖末段曾以手指刺入近旁巡查者咽喉致死，随即力竭，不外推穿甲或远程杀伤。'
  c['baseline']['stamina']='依靠静卧、瑜珈和少量食水配给在地下囚禁中支撑多日，最终接近死亡；需要水、食物和恢复，不是辟谷或无限忍耐。'
  c['applications']=['把证词、通讯录音、物证与社会关系逐项互证，区分嫌疑与定罪。','有具体权限和同僚支持时设置跟踪、伪装接近与拘捕行动。','在近身或持枪对抗中抓住真实机会；陷入资源匮乏时统筹配给并等待可验证的脱身窗口。']
  c['limits']='警权与组织支援依场景成立，不能跨世界自动调用。射击和近身杀伤均须距离与动作机会，长期断食仍可致命，判断也需证据纠正。'
"""
if '# All-series evidence added' not in s:s=s.replace(marker,extra+'\n'+marker)
p.write_text(s,encoding='utf8')
