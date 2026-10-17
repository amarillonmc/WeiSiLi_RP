from build_cards import *
S='卫斯理系列/'
def make(key,name,book,bio,end,skill,mechanism,ability_limit,refs,motive,triggers,roles=('单书主角',),aliases=(),scores=(1,0,0,1,1,1),tier='纸',dead=False,appearance='正文未提供需要固定保留的完整外貌；按年龄、身份与当下行为呈现。',**kw):
 ability=[A(skill,mechanism,['在已确认条件下运用该专长','根据实际线索调整方法，不能预先知道谜底'],ability_limit)]
 evidence=[E(S+book,a,b,s) for a,b,s in refs]
 deploy=kw.pop('deploy',None);adapt=kw.pop('adapt',None)
 if dead:
  deploy='原作终局已经死亡或失去可行动形态；参战用最后清醒行动形态，保留终局经历，仅作为明确的角色扮演恢复，不宣称原作复活。'
  adapt=[{'change':'为可操作角色恢复最后清醒行动形态，保留终局经历。','reason':'满足剧情完结后参战；不改写原作死亡或封存结局。','power_impact':'没有复活、再生或脱离控制的新能力。'},{'change':'把既有动机展开为可由新情境触发的选择。','reason':'避免重复原著对白。','power_impact':'无能力增幅。'}]
 return card(key,name,[S.rstrip('/')],list(roles),bio,appearance,end,ability,evidence,motive,[T(*t) for t in triggers],aliases=aliases,scores=scores,theoretical=tier,deploy=deploy,adapt=adapt,weaknesses=[W('机制边界',ability_limit,'条件不足时无法继续落实预期效果。','观察其准备条件与失败结果。','补充原作已允许的条件，或改用协商、调查和撤退。')],**kw)
def cov(book,items,excluded=(),notes=()):
 coverage(S+book,[('卫斯理','weisili_wei_sili','系列主角','本书叙述与主要调查行动。')]+[(n,i if i.startswith(('adventure_','yuanzhenxia_','mulanhua_','gaosi_','weisili_')) else 'weisili_'+i,r,b) for n,i,r,b in items],excluded,notes)
