"""Build evidence-backed TRPG modules; numerical rules are explicit adaptations.

Authored records are in data/trpg_modules. The corpus is read and hashed, never
changed or redistributed. Keyword screening is not literary review.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

from build_world_kb import book_id, title_of, verify_sources

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_VERSION = '1.1'
PROFILE = 'canon-separated-trpg-1.0'
MODULES = {
    'artifacts': ('artifacts_and_curses.json', 'items'),
    'hazards': ('hazards_and_taboos.json', 'hazards'),
    'bosses': ('apex_boss_movesets.json', 'bosses'),
    'scenarios': ('scenario_blueprints.json', 'scenarios'),
}
STATUSES = {'textual_fact', 'testimony', 'hypothesis', 'unresolved', 'mixed'}
CATEGORIES = {'alien_device', 'biological_agent', 'occult_curse', 'ancient_relic',
              'human_technology', 'human_alien_hybrid_technology', 'alien_material',
              'unknown_material', 'nonmaterial_life'}
PATTERNS = {
    'objects_and_access': r'仪器|装置|矿物|药物|解药|钥匙|密[码碼]|机件|微晶|椅子|金属片',
    'hazards_and_limits': r'陷阱|窒息|辐射|禁忌|失去知觉|失去知覺|失踪|失蹤|无法离开|無法離開|不能控制',
    'adversarial_actions': r'控制|支配|侵入|消灭|消滅|反噬|中毒|攻击|攻擊|威胁|威脅',
    'revelations_and_conflicts': r'真相|秘密|背叛|欺骗|欺騙|代价|代價|牺牲|犧牲|原来|原來',
}


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def encoded(value):
    return value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2) + '\n'


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def validate_records(records, files, character_ids):
    """Structural checks cannot prove a paraphrase is faithful to its citation."""
    seen = set()
    for r in records:
        ident = r.get('id', '')
        if not re.fullmatch(r'[a-z0-9_]+', ident) or ident in seen:
            raise ValueError('Duplicate/unsafe dossier id: ' + ident)
        seen.add(ident)
        if not nonempty(r.get('name')) or not nonempty(r.get('public_name')) or not any(k in r for k in ('artifact', 'hazard', 'boss', 'scenario')):
            raise ValueError('Empty dossier: ' + ident)
        books = r.get('source_books', [])
        if not books or len(set(books)) != len(books) or set(books) - files.keys():
            raise ValueError('Unknown/duplicate source book: ' + ident)
        c = r.get('canonical', {})
        for field in ('surface', 'mechanism', 'activation', 'price', 'counter', 'availability'):
            if not nonempty(c.get(field)):
                raise ValueError(f'{ident}: missing canonical.{field}')
        if c.get('mechanism_status') not in STATUSES or not isinstance(c.get('unknowns'), list):
            raise ValueError('Missing epistemic status/unknowns: ' + ident)
        if c.get('counter_status') not in STATUSES | {'derived_strategy'}:
            raise ValueError('Missing counter epistemic status: ' + ident)
        # Quantification in source passages (e.g. one to fifty thousand) is fine;
        # dice, checks and game heat cannot silently become source assertions.
        if re.search(r'\bd(?:20|30|40)\b|\bDC\s*\d|\[dice|热度\s*\d', json.dumps(c, ensure_ascii=False), re.I):
            raise ValueError('Game mechanic in canonical facts: ' + ident)
        evidence = r.get('evidence', [])
        if not evidence or {e.get('path') for e in evidence} != set(books):
            raise ValueError('Missing per-book evidence: ' + ident)
        for e in evidence:
            path, a, b = e.get('path'), e.get('start_line'), e.get('end_line')
            if path not in files or type(a) is not int or type(b) is not int or not 1 <= a <= b <= files[path]['lines']:
                raise ValueError('Invalid evidence range: ' + ident)
            if e.get('epistemic_status') not in STATUSES or not nonempty(e.get('supports')):
                raise ValueError('Unlabelled evidence: ' + ident)
        if set(r.get('character_ids', [])) - character_ids:
            raise ValueError('Unknown character link: ' + ident)
        for key in ('artifact', 'hazard', 'boss', 'scenario'):
            if key in r and (type(r[key].get('heat')) is not int or not 1 <= r[key]['heat'] <= 10):
                raise ValueError('Invalid adapted heat: ' + ident)
        if 'artifact' in r and r['artifact'].get('category') not in CATEGORIES:
            raise ValueError('Unknown category: ' + ident)
        if 'hazard' in r:
            h = r['hazard']
            if h['heat'] < 4 or any(not nonempty(h.get(k)) for k in ('dimensions','trigger','effect','warning')):
                raise ValueError('Incomplete hazard: ' + ident)
        if 'boss' in r:
            boss = r['boss']
            if boss['heat'] not in (6, 7) or boss.get('card_id') not in r['character_ids']:
                raise ValueError('Invalid boss link/heat: ' + ident)
            if any(not nonempty(boss.get(k)) for k in ('phase','hostility','barrier','display_name')) or not boss.get('moves'):
                raise ValueError('Missing boss deployment conditions: ' + ident)
            for move in boss['moves']:
                if any(not nonempty(move.get(k)) for k in ('name','basis','condition','defense','effect')):
                    raise ValueError('Unconditioned boss move: ' + ident)
        if 'scenario' in r:
            for field in ('layers','clues','goals'):
                values = r['scenario'].get(field, [])
                if len(values) != 3 or not all(nonempty(x) for x in values):
                    raise ValueError('Incomplete scenario ' + field + ': ' + ident)


def adapt(**fields):
    return dict(status='adaptation', balance_status='unplaytested', **fields)


def evidence_for(record, files):
    out = copy.deepcopy(record['evidence'])
    for e in out:
        e['source_sha256'] = files[e['path']]['sha256']
        e['provenance'] = {'kind': 'direct_source_review', 'scope': 'cited_passages_only'}
    return out


def common(record, files):
    return dict(dossier_id=record['id'], name=record['name'], public_name=record['public_name'], source_book=record['source_books'][0],
                source_books=record['source_books'], canonical=record['canonical'],
                character_ids=record['character_ids'], audience='gm',
                evidence=evidence_for(record, files),
                evidence_lines='; '.join(f"{e['path']}:L{e['start_line']}-L{e['end_line']}" for e in record['evidence']))


def convert(record, files):
    c, ident = record['canonical'], record['id']
    out = {}
    if 'artifact' in record:
        a = record['artifact']
        recoil = record.get('hazard', {}).get('effect', '代价以原著记录为边界；若要数值化，主持人须事先说明本场条件，不能补造治愈或必杀效果。')
        out['artifacts'] = dict(common(record, files), id='artifact_' + ident,
            category=a['category'], recommended_heat=a['heat'],
            surface_phenomenon_believes=c['surface'],
            true_mechanism_knows=f"【证据层级：{c['mechanism_status']}；非一律确证】{c['mechanism']}",
            the_key_activation=c['activation'], the_price_recoil=f"【原著】{c['price']}【改编】{recoil}",
            canonical_counter=f"【{c['counter_status']}】{c['counter']}",
            rule_adaptation=adapt(heat=a['heat'], recoil=recoil,
                three_rights={'body':record['name'], 'key':c['activation'], 'price':c['price'],
                             'ownership_assignment':'本体持有者、掌握条件者与承担代价者由场景分别分配；这种权利分配是改编。'}))
    if 'hazard' in record:
        h = record['hazard']
        suppression = adapt(suppressed_dimension=h['dimensions'],
            penalty='仅对描述中确实失效的专长加值归零；不改基础属性，也不削减未受影响的专长。',
            in_universe_reason=c['mechanism'], restores_when='实际排除或绕开该失效条件后恢复；不能仅靠热度下降宣布原著机制消失。')
        roll = adapt(dice_expression='d30+0', trigger_condition=h['trigger'],
                     target_defense='d20+相关属性；采用哪一项须在掷骰前按行动声明',
                     on_hit_effect=h['effect'], on_miss_effect='本次不推进状态，保留实际环境与已获得线索。',
                     frequency='同一触发原因每轮至多一次；已经触发的同一伤害不在别的模块重复结算。')
        out['hazards'] = dict(common(record, files), id='hazard_' + ident, min_heat=h['heat'],
            specialty_suppression_rule=suppression, active_hazard_roll=roll,
            canonical_escape=f"【{c['counter_status']}】{c['counter']}", public_warning=h['warning'],
            rule_adaptation=adapt(telegraph_before_trigger=True, automatic_death=False,
                design_note='环境主动骰是本扩展建议。未能读取论坛全文，不能据此宣称官方规则要求所有环境用 d30。'))
    if 'boss' in record:
        b = record['boss']
        expression = 'd40+0' if b['heat'] == 7 else 'd30+0'
        moves = []
        for m in b['moves']:
            voluntary = m['defense'].startswith('无对抗')
            moves.append(dict(move_name=m['name'], canonical_basis=m['basis'],
                dice=None if voluntary else f"[dice={b['display_name']}·{m['name']}]{expression}[/dice]",
                trigger_condition=m['condition'], target_defense=m['defense'] if voluntary else 'd20+' + m['defense'],
                on_hit_effect=m['effect'], rule_status='adaptation',
                on_miss_effect='不适用：此动作无对抗掷骰。' if voluntary else '不获得本次效果；现实条件和已付出的准备成本仍存在。'))
        out['bosses'] = dict(common(record, files), id='boss_' + ident, name=b['display_name'], encounter_name=record['name'], card_id=b['card_id'],
            heat_threshold=b['heat'], loaded_dice=expression, passive_barrier=b['barrier'], active_moves=moves,
            deployment=adapt(phase=b['phase'], hostility_condition=b['hostility'],
                strength_interpretation='热度是本场冲突压力与资源的改编，不修改原角色评级；友好角色不因达到热度自动敌对。'),
            canonical_weakness_counter={'discovery_dc':16, 'discovery_dc_status':'adaptation',
                'description':c['counter'], 'counter_status':c['counter_status'], 'unique_fatal_weakness':None,
                'unique_fatal_weakness_status':'本次回读未建立唯一死穴；不得把所有边界改写成同一种弱点。',
                'resolution':adapt(text='检定只帮助发现线索；实际满足阻断条件才使相关招式失效。不能仅掷出 DC 就把整张卡的 d40 改成 d20。')},
            rule_adaptation=adapt(dice=expression, frequency='默认每轮一次主动招式；同一触发不与环境模块重复扣状态。',
                modifier_reason='先用 +0，保留 d30/d40 的骰面差；未从小说推导额外 +3/+4，尚未实测平衡。'))
    if 'scenario' in record:
        s = record['scenario']
        assignments = [dict(id=key,slots=slots,objective=goal,knowledge='只收到本目标与主持人已揭露的线索，不自动知道后两层真相。')
                       for key,slots,goal in zip(('a','b','c'),(4,4,3),s['goals'])]
        out['scenarios'] = dict(common(record, files), id='scenario_' + ident, title=record['name']+'：调查与抉择',
            recommended_heat=s['heat'], three_layer_epistemic_trap=dict(zip(
                ('layer_1_hook','layer_2_twist','layer_3_core_truth'),s['layers'])),
            mutual_exclusive_agendas=[dict(faction_a=s['goals'][0],faction_b=s['goals'][1],faction_c=s['goals'][2],status='adaptation')],
            clue_progression=[dict(stage=i+1,clue=x,canon_status=c['mechanism_status'],
                release_condition='通过场景中相应的检查、证言或记录取得；失败可改变成本，不应永远封死唯一线索。') for i,x in enumerate(s['clues'])],
            rule_adaptation=adapt(player_count=11,assignments=assignments,
                conflict_focus='至少 A/B 在同一对象的保全、使用、处置或时机上冲突；C 提供知情、监督或第三种归属要求。',
                ending_branches=['满足 A 的目标并记录对 B/C 的代价','满足 B 的目标并记录对 A/C 的代价','达成新的协议，明确谁放弃了哪个原目标'],
                invention_boundary='三层编排、11 人分配、秘密目标和胜负条件均为改编；不宣称原书恰有三次反转或三派参赛者。'),
            canonical_end_state=c['availability'])
    return out


def scan_book(path):
    """Return line locations only; a hit is not an established mechanism."""
    lines = path.read_text(encoding='utf-8').splitlines()
    result = {}
    for key, pattern in PATTERNS.items():
        rx = re.compile(pattern)
        hits = [i for i,line in enumerate(lines,1) if rx.search(line)]
        sample = hits if len(hits) <= 8 else [hits[round(i*(len(hits)-1)/7)] for i in range(8)]
        result[key] = dict(matching_lines=len(hits), sample_line_numbers=sample)
    return result


def validate_rules_profile(policy):
    if policy.get('forum_verified') is not False or policy.get('schema_version') != SCHEMA_VERSION:
        raise ValueError('Rule provenance must be reviewed explicitly before changing this profile')


def build_bundle(root=ROOT, source=None):
    catalog = read(root/'data/corpus_catalog.json')
    source = Path(source or catalog['source'])
    verify_sources(catalog, source)
    files = {x['path']:x for x in catalog['files']}
    char_index = read(root/'knowledge/index.json')
    char_ids = {x['id'] for x in char_index['characters']}
    records = read(root/'data/trpg_modules/dossiers.json')
    policy = read(root/'data/trpg_modules/policy.json')
    corrections = read(root/'data/trpg_modules/guide_audit.json')
    validate_rules_profile(policy)
    validate_records(records, files, char_ids)
    record_ids = {r['id'] for r in records}
    audit_ids = set()
    for correction in corrections:
        if correction['id'] in audit_ids or set(correction['dossier_ids']) - record_ids:
            raise ValueError('Invalid guide audit references: ' + correction['id'])
        audit_ids.add(correction['id'])
    outputs, by_book, counts, all_rows = {}, {}, {}, []
    buckets = {key:[] for key in MODULES}
    for r in records:
        for kind, item in convert(r, files).items():
            buckets[kind].append(item)
            row = dict(id=item['id'],name=item['name'],kind=kind,
                       file=MODULES[kind][0],dossier_id=r['id'],source_books=r['source_books'],
                       character_ids=r['character_ids'], heat=r[{'artifacts':'artifact','hazards':'hazard','bosses':'boss','scenarios':'scenario'}[kind]]['heat'])
            all_rows.append(row)
            for book in r['source_books']:
                by_book.setdefault(book,[]).append(row['id'])
    for kind,(filename,key) in MODULES.items():
        counts[kind] = len(buckets[kind])
        outputs['knowledge/trpg_modules/'+filename] = dict(schema_version=SCHEMA_VERSION,
            extension_profile=PROFILE, audience='gm', rule_profile=policy, **{key:buckets[kind]})
    coverage = []
    for f in catalog['files']:
        path = f['path']
        dossiers = [r for r in records if path in r['source_books']]
        entry = dict(book_id=book_id(path),source_book=path,title=title_of(path),source_sha256=f['sha256'],
            keyword_screening=scan_book(source/path), module_ids=by_book.get(path,[]),
            review_status='cited_passages_reviewed' if dossiers else 'keyword_screened_only',
            extraction_complete=False,
            review_boundary='只回读所列片段，不代表本书通读或要素穷尽。' if dossiers else '只完成关键词筛查，尚无本扩展的已审核要素；不是没有奇物或危险。',
            dossier_ids=[r['id'] for r in dossiers],
            evidence=[e for r in dossiers for e in evidence_for(r,files) if e['path']==path])
        outputs[f'knowledge/trpg_modules/books/{book_id(path)}.json'] = entry
        coverage.append({k:v for k,v in entry.items() if k not in ('evidence','keyword_screening')})
    evidence_keys = {(e['path'],e['start_line'],e['end_line']) for r in records for e in r['evidence']}
    series = Counter(path.split('/')[0] for path in by_book)
    manifest = dict(schema_version=SCHEMA_VERSION, extension_profile=PROFILE,
        counts=counts, curated_dossiers=len(records), corpus_texts=len(files),
        keyword_screened_texts=len(files), directly_reviewed_texts=len(by_book),
        reviewed_series=dict(sorted(series.items())), unique_citation_ranges=len(evidence_keys),
        exhaustive_extraction=False, forum_verified=False,
        source_catalog_sha256=hashlib.sha256((root/'data/corpus_catalog.json').read_bytes()).hexdigest(),
        authored_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((root/'data/trpg_modules').glob('*.json'))},
        limitations=['全文关键词筛查不是全文精读；未审核文本保留为待扩展。',
            '四个模块中的骰面、DC、状态与秘密任务均未实测，不作为原作事实。',
            '只验证结构、引用行界与哈希，语义解释仍需人工回读。',
            '论坛正文无法取得，规则适配以用户提供指南为依据。'])
    outputs['knowledge/trpg_modules/index.json'] = dict(schema_version=SCHEMA_VERSION,modules=MODULES,
        records=all_rows, books=coverage, default_audience='gm')
    outputs['knowledge/trpg_modules/coverage.json'] = dict(summary=manifest,books=coverage)
    outputs['knowledge/trpg_modules/manifest.json'] = manifest
    outputs['knowledge/trpg_modules/guide_audit.json'] = dict(schema_version=SCHEMA_VERSION,findings=corrections)
    outputs['knowledge/trpg_modules/schema.json'] = read(root/'data/trpg_modules/schema.json')
    outputs['reports/trpg_kb_validation.json'] = dict(status='passed',counts=counts,
        source_hashes_verified=len(files),evidence_ranges_verified=len(evidence_keys),
        character_links_verified=True,canonical_game_separation_verified=True,
        exhaustive_extraction=False,forum_verified=False,
        note='这是构建时校验报告；--check 另逐文件比较生成结果。结构成功不证明所有文学解释正确。')
    lines=['# 原著依据与 TRPG 模块','',
        '四个 JSON 供主持人或 LLM 读取。先读 [使用说明](../../docs/trpg_modules_guide.md)，再按 ID 获取单项；完整文件含剧透和私密目标。','',
        f"本次 {len(records)} 个审核主题，产出奇物 {counts['artifacts']}、环境 {counts['hazards']}、对手 {counts['bosses']}、剧本 {counts['scenarios']} 条。",
        f"已筛查 {len(files)} 个文本，直接回读引用涉及 {len(by_book)} 个文本、{len(series)} 个系列；未宣称全文精读或穷尽。",'',
        '| 模块 | 文件 |','| --- | --- |']
    for kind,(filename,_) in MODULES.items():
        lines.append(f'| {kind} | [{filename}]({filename}) |')
    lines += ['', '[指南示例核对](guide_audit.json)｜[逐书覆盖](coverage.json)｜[机器索引](index.json)｜[原角色库](../README.md)｜[世界库](../world/README.md)', '',
              '## 主题索引','', '| 主题 | 模块 | 原著 |', '| --- | --- | --- |']
    for r in records:
        kinds=[kind for kind,key in (('奇物','artifact'),('环境','hazard'),('对手','boss'),('剧本','scenario')) if key in r]
        lines.append(f"| `{r['id']}`：{r['name']} | {'、'.join(kinds)} | {'、'.join(title_of(x) for x in r['source_books'])} |")
    outputs['knowledge/trpg_modules/README.md'] = '\n'.join(lines)+'\n'
    return outputs, manifest


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    outputs,manifest=build_bundle(source=args.source)
    if args.check:
        mismatched=[p for p,v in outputs.items() if not (ROOT/p).exists() or (ROOT/p).read_text(encoding='utf-8') != encoded(v)]
        # Refuse unnoticed stale generated files as well as missing/current ones.
        expected={p for p in outputs if p.startswith('knowledge/trpg_modules/')}
        actual={p.relative_to(ROOT).as_posix() for p in (ROOT/'knowledge/trpg_modules').rglob('*') if p.is_file()}
        mismatched += sorted(actual-expected)
        if mismatched:
            raise SystemExit('Generated output mismatch: '+', '.join(mismatched))
    else:
        for path,value in outputs.items():
            dest=ROOT/path
            dest.parent.mkdir(parents=True,exist_ok=True)
            dest.write_text(encoded(value),encoding='utf-8',newline='\n')
    print(json.dumps(dict(status='checked' if args.check else 'built',**manifest['counts'],
        keyword_screened_texts=manifest['keyword_screened_texts'],directly_reviewed_texts=manifest['directly_reviewed_texts']),ensure_ascii=False))


if __name__ == '__main__':
    main()
