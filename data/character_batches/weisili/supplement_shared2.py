from author_library import *
data=json.loads(CARDS.read_text(encoding='utf8')); by={x['id']:x for x in data}
def append(id,text,evidence):
 c=by['weisili_'+id]
 if text not in c['biography']:c['biography']+=text
 for e in evidence:
  if e not in c['evidence']:c['evidence'].append(e)
append('tie_dan','少年时他曾作为叔父的传令兵，和叔父以铁匠身份伪装，参与诱使漏网日军骑兵取钥匙的安排；这段早年主动参与军务的经历应与后来的将军、父亲和伤残生活一并保留。',[ev('94',388,429,'少年传令兵、叔侄伪装与后来成为将军')])
append('yin_4','少年卫斯理所接触的神秘声音后来确认属于四号：他曾误抓况英豪，承认难以分辨人类面容，在卫集中思念联络后释放人并托寻王天兵。植入的联络密码也不是残缺的一至三号能自由解读的内容。',[ev('94',2217,2264,'误抓、释放、委托与识别限制'),ev('102',1863,1884,'四号声音、密码与一至三号限制')])
append('yin_1','他在后来的解释中曾模拟四号的声音；这种模仿不能反推少年时期的接触者也是他，残缺思想仪不能解读四号植入的联络密码。',[ev('102',1863,1884,'模拟声音与密码限制')])
append('huang_chan','《还阳》中她化名黄芳子参与联络、恋爱伪装和专机驾驶，并被委任主管奇异现象研究会；宋舅经历记忆清除，早期只是卫的推断，后书才作为既成事实回述，不能据此认定每一步手术均由她亲自实施。',[ev('098',949,951,'黄芳子身份揭明'),ev('098',2316,2319,'主管任命'),ev('098',2717,2720,'当时关于记忆清除的推断'),ev('119',11,18,'后书明确回述记忆被清除')])
c=by['weisili_song_tianran'];c['name']='宋天然／宋自然';c['aliases']=list(dict.fromkeys(c['aliases']+['宋自然','温宝裕的舅舅','温舅']))
append('song_tianran','后来的故事改称他为宋自然，并明确回指《命运》《还阳》中的同一温舅。他在还阳事件后失去相关记忆，后来仍与温宝裕实际会面；这段遭遇不会使他掌握记忆操作，也不表示他能自行恢复被清除的内容。',[ev('098',1208,1211,'温妈妈弟弟身份'),ev('098',2717,2720,'失去相关记忆的表现与推断'),ev('119',11,18,'同一身份及清除记忆回述'),ev('119',184,186,'后续与温实际登场')])
c['version']['canonical_endpoint']='经历《还阳》后相关记忆被清除，后书仍作为温宝裕舅舅活动；没有自行恢复记忆或命运能力';c['version']['deployment']=c['version']['canonical_endpoint']+'。保留其实际可记忆内容，不用读卡补回原作已丢失的秘密。'
append('xiao_guo','后续郭夫人在《成精变人》中被明确称为小唐；尚无直接原文把她与早年导游唐婉儿完全互认，因此配偶关系以小唐为准，保留同人可能而不强行合并。',[ev('099',687,708,'郭夫人小唐及孤儿院同学经历')])
CARDS.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
cov=json.loads((BASE/'coverage.json').read_text(encoding='utf8'))
for row in cov:
 for p in row['included']:
  if p['card_id']=='yuanzhenxia_suyaoxi':p['card_id']='yuanzhenxia_su_yaoxi'
(BASE/'coverage.json').write_text(json.dumps(cov,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
cover('085',[('卫斯理','wei_sili','主角','追查异常'),('白素','bai_su','重要配角','对事件的联系与讨论'),('陈景德','yuanzhenxia_chen_jingde','主角','记忆联结试探'),('陈宜兴','yuanzhenxia_chen_yixing','主角','记忆联结试探'),('方如花','yuanzhenxia_fang_ruhua','主角','与陈氏组成四人记忆联结'),('方似玉','yuanzhenxia_fang_siyu','主角','记忆被攫取及待恢复'),('成金润','cheng_jinrun','主角','调查线索及退避理论'),('管理主任','twin_tower_manager','阶段性对立者','掩饰、伤人及失神'),('电脑系统','twin_tower_computer','非人对立实体','设施异常与疑似记忆攫取'),('良辰','liang_chen','重要配角','调查及救黄堂'),('美景','mei_jing','重要配角','调查及救黄堂'),('黄堂','huang_tang','重要配角','搜救与警方调查'),('陶启泉','tao_qiquan','重要配角','助手失神求助'),('陈岛','chen_dao','重要配角','陶的巨型保镖实际阻拦陈氏'),('老蔡','lao_cai','重要配角','转述原医生来电')],[('十二名失神受害者、陶氏杨姓助手等','被害与搜救对象，缺独立主角行为；不因其惨遇推定为敌'),('成金润同行、六号、酿酒者','一次讨论中的未具名专业协作者，其共同理论由成卡记录'),('搜寻犬、训犬员、电梯工程师、守卫','一次性工作或受害角色，无独立主要人格'),('亲王','一次来访与电梯现象说明，不另造王室主角'),('原振侠','本书开头来电转述及背景，主卡归原系列'),('陈景润等现实人物','叙述举例和推测，不属于实际故事登场角色')],['陈方四人跨系列统一，不把良辰美景视为接受记忆复制的实验者。','本案技术危机属于小说设定，叙述中的计算、历史举例不当作现实科学事实。'])
print('Supplemented shared continuity and reviewed085')
