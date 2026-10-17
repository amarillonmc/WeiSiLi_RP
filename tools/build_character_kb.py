"""Validate authored character records and render independently retrievable cards/ratings."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from collections import Counter, defaultdict
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TIERS = ['纸', '并', '强', '凶', '狂', '准神', '神下', '神中', '神上', '论外']
POSITIVE = ['physical', 'energy', 'scope', 'sustain', 'range', 'combat']


def complete_profile(source_card):
    """Expose already-authored limits in the template's five weakness fields.

    Old authoring batches used a string list or kept limits inside abilities.
    This migration neither invents a weakness nor changes the numerical rating.
    Observable presentation and discovery below are explicit RP suggestions.
    """
    c=copy.deepcopy(source_card)
    if isinstance(c.get('aliases'),list):
        c['aliases']=list(dict.fromkeys(a for a in c['aliases'] if a!=c.get('name')))
    if 'weaknesses' not in c or 'abilities' not in c:return c
    existing=c['weaknesses']
    if not existing:
        limits=list(dict.fromkeys(a['limits'] for a in c['abilities'] if a.get('limits')))
        existing=[{'name':'已证实能力的边界','mechanism':'；'.join(limits)}] if limits else []
    normalized=[]
    for i,w in enumerate(existing):
        if isinstance(w,str):w={'name':f'限制 {i+1}','mechanism':w}
        if not isinstance(w,dict):normalized.append(w);continue
        w=dict(w)
        w.setdefault('visible','演绎建议：触及上述条件时，以行动受阻、效果减弱或必须补足条件表现，不另加无根据症状。')
        w.setdefault('discovery','通过观察实际行动、询问准备条件或取得相关线索识别；不让对手直接读取角色卡。')
        w.setdefault('mitigation','核实并补足上述条件，或改用本人已有的其他办法；不能临时新增免疫来取消边界。')
        normalized.append(w)
    c['weaknesses']=normalized
    return c


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2) + '\n'
    path.write_text(text, encoding='utf-8', newline='\n')


def textof(value):
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return '；'.join(textof(v) for v in value) or '无已证据项目。'
    if isinstance(value, dict):
        labels={'name':'名称','type':'类型','mechanism':'机制','visual':'表现','applications':'应用',
                'limits':'边界','condition':'条件','trigger':'触发','cost':'代价','effect':'效果',
                'description':'说明','tier':'位阶','uncontrolled':'不可控表现','source':'来源'}
        return '；'.join(f'{labels.get(k,k)}：{textof(v)}' for k, v in value.items())
    return str(value)


def rating(card, rules):
    r = card['rating_input']
    weights = rules['rating']['positive_weights']
    pos = sum(Decimal(str(r['positive'][k])) * Decimal(str(weights[k])) for k in POSITIVE)
    neg = r['negative']
    deductions = sum(Decimal(str(neg[k]['score'])) * Decimal(str(neg[k]['af'])) for k in ['self_limit', 'environment'])
    deductions += Decimal(str(neg['volatility']['score']))
    raw = pos - deductions
    rounded = int(raw.quantize(Decimal('1'), rounding=ROUND_HALF_UP))
    numeric = next(b['name'] for b in rules['rating']['bands'] if b['min'] <= rounded <= b['max'])
    concept = r['concept_level']
    cap = {0: 5, 1: 6, 2: 8, 3: 9}[concept]
    practical = TIERS[min(TIERS.index(numeric), cap)]
    theory = r['theoretical_tier']
    practical_index, theory_index = TIERS.index(practical), TIERS.index(theory)
    if theory_index < practical_index:
        raise ValueError(f'{card["id"]}: theoretical tier {theory} below practical {practical} ({raw})')
    if theory_index > cap:
        raise ValueError(f'{card["id"]}: theoretical tier {theory} exceeds concept gate {concept}')
    final, suffix = practical, ''
    mastery = r['mastery']
    if theory_index > practical_index:
        if mastery == '稍有掌握':
            suffix = '顶'
        elif mastery == '基本掌握':
            final = TIERS[min(practical_index + 1, theory_index)]
        elif mastery == '完全掌握':
            final = theory
        elif mastery == '被动触发':
            # No automatic upward promotion without a demonstrated frequency judgment.
            suffix = '（被动触发；按常态计）'
    return {
        'id': card['id'], 'name': card['name'], 'standard_version': rules['version'],
        'standard_url': rules['rating_source']['url'], 'standard_section': rules['rating_source']['section'],
        'assessment_basis': card['version'], 'positive': r['positive'], 'positive_weights': weights,
        'positive_reasons': r['positive_reasons'], 'negative': neg,
        'positive_total': float(pos), 'deduction_total': float(deductions),
        'raw_score': float(raw), 'rounded_score': rounded, 'numeric_tier': numeric,
        'concept_level': concept, 'concept_reason': r['concept_reason'],
        'practical_tier': practical, 'theoretical_tier': theory,
        'mastery': mastery, 'final_tier': final, 'display_tier': final + suffix,
        'controlled_ceiling': r['ceiling'], 'confidence': r['rating_confidence'],
        'rounding_policy': rules['rating']['rounding_policy'],
        'analysis_notice': '本项目基于小说文本的分析值，非原作官方数值；外援、一次性经历与常态能力分开。',
        'evidence': card['evidence'], 'uncertainties': card['uncertainties'],
    }


def markdown_card(c):
    out = [f'# {c["name"]}', '', f'标识：`{c["id"]}`｜系列：{textof(c["series"])}｜身份：{textof(c["roles"])}', '',
           f'别名：{textof(c["aliases"])}', '', '## 版本与使用约定', '',
           f'原作终局：{c["version"]["canonical_endpoint"]}', '',
           f'出场状态：{c["version"]["deployment"]}', '', f'综合依据：{c["version"]["basis"]}', '']
    if c['ooc']:
        out += ['OOC 约束：', ''] + [f'- {textof(v)}' for v in c['ooc']] + ['']
    if c['terms']:
        out += ['必要术语：', ''] + [f'- **{v["term"]}**：{v["explanation"]}' for v in c['terms']] + ['']
    out += ['## 背景传记', '', c['biography'], '', '## 外观与行为表现', '',
            c['appearance']['description'], '', f'演绎：{c["appearance"]["portrayal"]}', '',
            f'角色作用：{c["role_function"]}', '',
            f'常态：{c["modes"]["ordinary"]}', '', f'受压：{c["modes"]["pressure"]}', '',
            f'认知逻辑：{c["modes"]["reasoning"]}', '', '## 核心能力与手法', '']
    for a in c['abilities']:
        out += [f'### {a["name"]}（{a["type"]}）', '', f'机制：{a["mechanism"]}', '',
                f'表现：{a["visual"]}', '', f'应用：{textof(a["applications"])}', '', f'边界：{a["limits"]}', '']
    out += ['## 基础七维', '']
    labels = {'destruction':'破坏力','durability':'耐久度','speed':'速度','energy':'能量／非物理攻击','mind':'精神／意念','stamina':'战斗续航'}
    out += [f'- **{v}**：{c["baseline"][k]}' for k,v in labels.items()]
    intel = c['baseline']['intelligence']
    out += [f'- **战斗智商**：战中表现：{intel["in_combat"]}；常规知识：{intel["knowledge"]}；策略经验：{intel["planning"]}；应变：{intel["adaptation"]}', '']
    for field, label in [('passives','被动特性'),('trump_cards','终极底牌／终局表现')]:
        if c[field]:
            out += [f'## {label}', ''] + [f'- {textof(v)}' for v in c[field]] + ['']
    if c['weaknesses']:
        out += ['## 弱点与自我限制', '']
        for w in c['weaknesses']:
            out += [f'**{w["name"]}**：{w["mechanism"]}', '', f'外显：{w["visible"]}；识别方式：{w["discovery"]}；本人对策：{w["mitigation"]}', '']
    out += ['## 行为逻辑与核心行为库', '', f'动机：{c["logic"]["motivation"]}', '', '原则：', '']
    out += [f'- {p}' for p in c['logic']['principles']] + ['']
    for t in c['logic']['triggers']:
        out += [f'**{t["situation"]}**：当{t["condition"]}，{t["action"]}', '']
    out += ['行为扳机是对原作性格的场景化归纳，不要求重演原事件；未标作逐字引文的台词均为演绎示例。', '', '## 改编记录', '']
    out += [f'- {a["change"]}；目的：{a["reason"]}；能力影响：{a["power_impact"]}' for a in c['adaptations']] + ['']
    out += ['## 原文证据与不确定项', '', f'置信度：{c["confidence"]}', '']
    out += [f'- `{e["path"]}` L{e["start_line"]}–L{e["end_line"]}：{e["supports"]}' for e in c['evidence']]
    out += [''] + [f'- 待核：{u}' for u in c['uncertainties']] + ['']
    out += [f'强度另档：[{c["name"]}评级](../ratings/{c["id"]}.md)', '']
    return '\n'.join(out)


def markdown_rating(r, rules):
    out = [f'# {r["name"]} · 强度档案', '', f'综合标签：**{r["display_tier"]}**；常态实战：{r["practical_tier"]}；理论位阶：{r["theoretical_tier"]}。', '',
           f'原始分数 {r["raw_score"]:g} = 正向 {r["positive_total"]:g} − 负向 {r["deduction_total"]:g}；分段值 {r["rounded_score"]}。', '',
           f'[采用标准]({r["standard_url"]})：{r["standard_section"]}。{r["analysis_notice"]}', '',
           '| 正向维度 | 分数 | 权重 | 判断依据 |', '|---|---:|---:|---|']
    for k in POSITIVE:
        reason = r['positive_reasons'][k].replace('|','／').replace('\n',' ')
        out.append(f'| {rules["rating"]["positive_labels"][k]} | {r["positive"][k]} | {r["positive_weights"][k]} | {reason} |')
    out += ['', '| 负向维度 | 分数 | AF | 判断依据 |', '|---|---:|---:|---|']
    for k,label in [('self_limit','自我限制'),('environment','环境依赖'),('volatility','发挥波动')]:
        n=r['negative'][k]
        out.append(f'| {label} | {n["score"]} | {n.get("af","不适用")} | {n["reason"].replace("|","／")} |')
    out += ['', f'概念层 {r["concept_level"]}：{r["concept_reason"]}', '', f'掌握程度：{r["mastery"]}', '',
            f'可控上限（{r["controlled_ceiling"]["tier"]}）：{r["controlled_ceiling"]["description"]}', '',
            f'不可控事件：{r["controlled_ceiling"]["uncontrolled"]}', '',
            f'置信度：{r["confidence"]}。{r["rounding_policy"]}', '',
            f'原作终局：{r["assessment_basis"]["canonical_endpoint"]}', '',
            f'参战前提：{r["assessment_basis"]["deployment"]}', '', '证据：', '']
    out += [f'- `{e["path"]}` L{e["start_line"]}–L{e["end_line"]}：{e["supports"]}' for e in r['evidence']]
    out += [''] + [f'- 待核：{u}' for u in r['uncertainties']] + ['',f'[返回角色卡](../characters/{r["id"]}.md)', '']
    return '\n'.join(out)


def validate(cards, coverage, catalog, source, incomplete=False):
    errors=[]; ids=set(); files={f['path']:f for f in catalog['files']}
    required='id name aliases series roles version ooc terms biography appearance role_function modes abilities baseline passives trump_cards weaknesses logic adaptations evidence confidence uncertainties rating_input'.split()
    for c in cards:
        cid=c.get('id','<missing>')
        if cid in ids: errors.append(f'duplicate id {cid}')
        ids.add(cid)
        for k in required:
            if k not in c: errors.append(f'{cid}: missing {k}')
        if any(k not in c for k in required): continue
        nested = {
            'version':['basis','canonical_endpoint','deployment'],
            'appearance':['description','portrayal'],
            'modes':['ordinary','pressure','reasoning'],
            'baseline':['destruction','durability','speed','energy','mind','stamina','intelligence'],
            'logic':['motivation','principles','triggers'],
            'rating_input':['positive','positive_reasons','negative','concept_level','concept_reason',
                            'theoretical_tier','mastery','ceiling','rating_confidence'],
        }
        malformed=False
        for field,keys in nested.items():
            if not isinstance(c[field],dict) or any(k not in c[field] for k in keys):
                errors.append(f'{cid}: malformed {field}');malformed=True
        if malformed:continue
        for field in ['aliases','series','roles','ooc','terms','abilities','passives','trump_cards',
                      'weaknesses','adaptations','evidence','uncertainties']:
            if not isinstance(c[field],list):errors.append(f'{cid}: {field} must be a list');malformed=True
        if malformed:continue
        if not c['abilities']:errors.append(f'{cid}: no ability description')
        if not c['weaknesses']:errors.append(f'{cid}: no discoverable weakness')
        if len(c['ooc'])>5:errors.append(f'{cid}: more than 5 OOC constraints')
        if not 1<=len(c['logic']['principles'])<=3:errors.append(f'{cid}: principles must have 1–3 entries')
        if c['confidence'] not in ['high','medium','low']:errors.append(f'{cid}: invalid confidence')
        intel=c['baseline']['intelligence']
        if not isinstance(intel,dict) or any(not intel.get(k) for k in ['in_combat','knowledge','planning','adaptation']):
            errors.append(f'{cid}: incomplete intelligence dimensions')
        for field,keys in [('abilities',['name','type','mechanism','visual','applications','limits']),
                           ('weaknesses',['name','mechanism','visible','discovery','mitigation']),
                           ('adaptations',['change','reason','power_impact']),
                           ('terms',['term','explanation'])]:
            for item in c[field]:
                if not isinstance(item,dict) or any(not item.get(k) for k in keys):
                    errors.append(f'{cid}: incomplete {field} entry')
        triggers=c['logic']['triggers']
        if any(not isinstance(t,dict) or any(not t.get(k) for k in ['situation','condition','action']) for t in triggers):
            errors.append(f'{cid}: incomplete trigger')
        elif len({(t['situation'],t['condition']) for t in triggers})<3:
            errors.append(f'{cid}: fewer than 3 distinct trigger situations')
        if not re.fullmatch(r'[a-z][a-z0-9_]+',cid): errors.append(f'{cid}: unsafe identifier')
        if len(re.findall(r'[\u3400-\u9fff]',c['biography']))<300: errors.append(f'{cid}: biography below 300 Chinese characters')
        if len(c['logic']['triggers'])<3: errors.append(f'{cid}: fewer than 3 triggers')
        if not c['evidence']: errors.append(f'{cid}: no evidence')
        for e in c['evidence']:
            f=files.get(e['path'])
            if not f or not 1<=e['start_line']<=e['end_line']<=f['lines']: errors.append(f'{cid}: bad evidence {e}')
        r=c['rating_input']
        for k in POSITIVE:
            if not 0<=r['positive'][k]<=10: errors.append(f'{cid}: invalid {k} score')
            if not r['positive_reasons'].get(k): errors.append(f'{cid}: missing {k} rationale')
        for k in ['self_limit','environment','volatility']:
            n=r['negative'][k]
            if not 0<=n['score']<=10: errors.append(f'{cid}: invalid negative {k}')
            if k!='volatility' and not (n['af']==1 or 0.5<=n['af']<=0.7 or 0.1<=n['af']<=0.3): errors.append(f'{cid}: invalid accessibility factor')
        if r['mastery'] not in ['不适用','被动触发','稍有掌握','基本掌握','完全掌握']: errors.append(f'{cid}: invalid mastery')
        if r['concept_level'] not in [0,1,2,3]:errors.append(f'{cid}: invalid concept level')
        if r['theoretical_tier'] not in TIERS:errors.append(f'{cid}: unknown theoretical tier')
        if not isinstance(r['ceiling'],dict) or any(not r['ceiling'].get(k) for k in ['description','tier','uncontrolled']):
            errors.append(f'{cid}: incomplete ceiling')
        elif r['ceiling']['tier']!=r['theoretical_tier']:
            errors.append(f'{cid}: ceiling tier and theoretical tier differ')
    covered=Counter(x['path'] for x in coverage)
    for path,count in covered.items():
        if path not in files or count!=1: errors.append(f'bad/duplicate coverage {path}')
    if not incomplete:
        for path in files.keys()-covered.keys(): errors.append(f'no coverage {path}')
    for entry in coverage:
        if entry['status'] not in ['pending','reviewed']:errors.append(f'unknown coverage status {entry["path"]}')
        if entry['status']!='reviewed' and not incomplete: errors.append(f'pending {entry["path"]}')
        for role in entry['included']:
            if role['card_id'] not in ids and not incomplete: errors.append(f'unresolved {role["card_id"]} in {entry["path"]}')
    if not incomplete:
        referenced={r['card_id'] for e in coverage for r in e['included']}
        for cid in ids-referenced:errors.append(f'card absent from coverage {cid}')
    for path,f in files.items():
        p=source/path
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=f['sha256']:
            errors.append(f'source changed {path}')
    return errors


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source',type=Path)
    ap.add_argument('--allow-incomplete',action='store_true')
    ap.add_argument('--check',action='store_true',help='Validate only, do not render')
    args=ap.parse_args()
    rules=read(ROOT/'data/character_rules.json');catalog=read(ROOT/'data/corpus_catalog.json')
    source=args.source or Path(catalog['source'])
    cards=[]; coverage=[]
    for batch in sorted((ROOT/'data/character_batches').iterdir()):
        if (batch/'cards.json').is_file(): cards.extend(complete_profile(c) for c in read(batch/'cards.json'))
        if (batch/'coverage.json').is_file(): coverage.extend(read(batch/'coverage.json'))
    errors=validate(cards,coverage,catalog,source,args.allow_incomplete)
    ratings=[]
    for c in cards:
        try: ratings.append(rating(c,rules))
        except (KeyError, ValueError, TypeError, StopIteration) as exc: errors.append(str(exc))
    report={'cards':len(cards),'source_files':len(catalog['files']),'reviewed':sum(x['status']=='reviewed' for x in coverage),'coverage_records':len(coverage),'errors':errors}
    write(ROOT/'reports/character_kb_validation.json',report)
    print(json.dumps(report,ensure_ascii=False,indent=2))
    if errors: raise SystemExit(1)
    if args.check:return
    dest=ROOT/'knowledge'; index=[]; aliases=defaultdict(list)
    byrating={r['id']:r for r in ratings}
    for c in sorted(cards,key=lambda c:c['id']):
        card={k:v for k,v in c.items() if k!='rating_input'}
        r=byrating[c['id']]
        write(dest/'characters'/f'{c["id"]}.json',card)
        write(dest/'characters'/f'{c["id"]}.md',markdown_card(c))
        write(dest/'ratings'/f'{c["id"]}.json',r)
        write(dest/'ratings'/f'{c["id"]}.md',markdown_rating(r,rules))
        index.append({'id':c['id'],'name':c['name'],'aliases':c['aliases'],'series':c['series'],'roles':c['roles'],'card':f'characters/{c["id"]}.json','rating':f'ratings/{c["id"]}.json','tier':r['display_tier'],'confidence':c['confidence']})
        for name in dict.fromkeys([c['name']]+c['aliases']):aliases[name].append(c['id'])
    identity_path=ROOT/'data/character_identity_map.json'
    identities=read(identity_path) if identity_path.exists() else {'redirects':{},'decisions':[]}
    write(dest/'index.json',{'schema_version':'1.0','complete':not args.allow_incomplete,'characters':index,'name_lookup':dict(aliases),'id_redirects':identities['redirects']})
    write(dest/'identity_map.json',identities)
    write(dest/'coverage.json',sorted(coverage,key=lambda c:c['path']))
    write(dest/'rules.json',rules)
    write(dest/'manifest.json',{'schema_version':'1.0','source_files':catalog['files'],'card_count':len(cards),'rating_count':len(ratings),'reviewed_books':report['reviewed'],'complete':not args.allow_incomplete,'build_command':'python tools/build_character_kb.py'})
    lines=['# 倪匡小说角色知识库','','每张角色卡均有独立的 JSON、可读卡片和另存的强度档案。原文不随知识库重复分发。','',f'当前角色 {len(cards)}，评级 {len(ratings)}，已核对文本 {report["reviewed"]}/{len(catalog["files"])}。','', '| 角色 | 系列 | 身份 | 强度 |', '|---|---|---|---|']
    for x in index:lines.append(f'| [{x["name"]}](characters/{x["id"]}.md) | {"、".join(x["series"])} | {"、".join(x["roles"])} | [{x["tier"]}](ratings/{x["id"]}.md) |')
    write(dest/'README.md','\n'.join(lines)+'\n')


if __name__=='__main__':main()
