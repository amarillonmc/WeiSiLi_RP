"""Build the sourced world model, partial timeline and all-text evidence dossiers.

Only the standard library is required. Source text is verified, never copied into
the output. Authored data lives in data/worldbuilding, not in generated files.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from collections import Counter, defaultdict, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = ('rules', 'entities', 'events', 'relations', 'arcs', 'issues', 'bridges')
STATUSES = {'textual_fact', 'testimony', 'hypothesis', 'unresolved', 'synthesis', 'adaptation'}
LABELS = {'rules':'世界规则', 'entities':'机构、地点与争夺目标', 'events':'关键事件',
          'relations':'时间与揭露关系', 'arcs':'角色经历与成长', 'issues':'争议与未决项', 'bridges':'跨系列连接'}


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def encode(value):
    return value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2) + '\n'


def digest(value):
    return hashlib.sha256(value).hexdigest()


def book_id(path):
    """Path-based identity: changing source contents does not silently change IDs."""
    return 'book_' + digest(path.encode('utf-8'))[:12]


def title_of(path):
    stem = Path(path).stem.strip()
    title = re.sub(r'^\d+[.．\s]*', '', stem).strip()
    # The source-cleanup report confirms this filename/body-title discrepancy.
    return '血美人' if title == '学美人' else title


def topological_order(events, relations, include_inferred=True):
    """Deterministic display order only; unrelated nodes are NOT simultaneous."""
    ids = {e['id'] if isinstance(e, dict) else e for e in events}
    adjacent = defaultdict(set)
    degree = dict.fromkeys(ids, 0)
    for r in relations:
        if r['source'] not in ids or r['target'] not in ids:
            raise ValueError(f"Unknown relation endpoint: {r['id']}")
        if r['relation'] != 'before':
            continue
        if not include_inferred and r['epistemic_status'] != 'textual_fact':
            continue
        if r['target'] not in adjacent[r['source']]:
            adjacent[r['source']].add(r['target'])
            degree[r['target']] += 1
    queue = deque(sorted(k for k, d in degree.items() if d == 0))
    out = []
    while queue:
        current = queue.popleft()
        out.append(current)
        for target in sorted(adjacent[current]):
            degree[target] -= 1
            if degree[target] == 0:
                queue.append(target)
    if len(out) != len(ids):
        raise ValueError('Temporal cycle: ' + ', '.join(sorted(k for k, d in degree.items() if d)))
    return out


def ancestors(selected, events, relations, include_inferred=False):
    """A strict history closure; revelations alone do not assert temporal edges."""
    ids = {e['id'] if isinstance(e, dict) else e for e in events}
    if set(selected) - ids:
        raise ValueError('Unknown event IDs: ' + ', '.join(sorted(set(selected) - ids)))
    before = defaultdict(set)
    for r in relations:
        if r['relation'] == 'before' and (include_inferred or r['epistemic_status'] == 'textual_fact'):
            before[r['target']].add(r['source'])
    known, pending = set(selected), list(selected)
    while pending:
        for predecessor in before[pending.pop()] - known:
            known.add(predecessor)
            pending.append(predecessor)
    return known


def validate_evidence(e, files):
    if e.get('path') not in files:
        raise ValueError(f"Unknown evidence path: {e.get('path')}")
    a, b = e.get('start_line'), e.get('end_line')
    if type(a) is not int or type(b) is not int or not 1 <= a <= b <= files[e['path']]['lines']:
        raise ValueError(f"Invalid line range: {e['path']} {a}:{b}")
    if not isinstance(e.get('supports'), str) or not e['supports'].strip():
        raise ValueError(f"Empty evidence annotation: {e['path']}")


def validate_authored(data, files, characters):
    seen = set()
    for section in SECTIONS:
        for item in data[section]:
            ident = item['id']
            if not re.fullmatch(r'[a-z0-9_]+', ident) or ident in seen:
                raise ValueError('Duplicate or unsafe ID: ' + ident)
            seen.add(ident)
            if not item.get('evidence') and not (section == 'issues' and ident == 'issue_shared_world') and not (
                    section == 'bridges' and item.get('connection_level') == 'user_unification_assumption'):
                raise ValueError('Missing evidence: ' + ident)
            for e in item.get('evidence', []):
                validate_evidence(e, files)
                origin = e.get('provenance', {})
                if origin.get('kind') not in {'direct_source_review', 'existing_character_annotation'}:
                    raise ValueError('Missing provenance: ' + ident)
                if origin.get('kind') == 'existing_character_annotation':
                    cid = origin.get('character_id')
                    if cid not in characters or not any(all(e[k] == old[k] for k in
                            ('path', 'start_line', 'end_line', 'supports')) for old in characters[cid]['evidence']):
                        raise ValueError('Inherited evidence has changed: ' + ident)
            for cid in item.get('character_ids', []) + ([item['character_id']] if 'character_id' in item else []):
                if cid not in characters:
                    raise ValueError(f'{ident}: unknown character {cid}')
            status = item.get('epistemic_status')
            if status is not None and status not in STATUSES:
                raise ValueError(f'{ident}: invalid epistemic status {status}')
    event_ids = {e['id'] for e in data['events']}
    for event in data['events']:
        for field in ('summary', 'state_before', 'state_after', 'knowledge_boundary'):
            if not event.get(field):
                raise ValueError(f"{event['id']}: missing {field}")
        if event['time'].get('calendar_date') is not None:
            raise ValueError('This edition has no verified absolute event dates: ' + event['id'])
    for entity in data['entities']:
        if entity['mechanism']['epistemic_status'] not in STATUSES or entity['rp_use']['status'] != 'adaptation':
            raise ValueError('Unlabelled mechanism or RP suggestion: ' + entity['id'])
        for field in ('access_conditions', 'limits', 'last_known_state'):
            if not entity.get(field):
                raise ValueError(f"{entity['id']}: missing {field}")
    for arc in data['arcs']:
        if not arc['stages']:
            raise ValueError('Empty arc: ' + arc['id'])
        for stage in arc['stages']:
            if not stage['event_ids'] or set(stage['event_ids']) - event_ids:
                raise ValueError('Invalid arc stage: ' + arc['id'])
    for relation in data['relations']:
        if relation['relation'] not in {'before', 'revealed_by'}:
            raise ValueError('Invalid relation: ' + relation['id'])
    topological_order(data['events'], data['relations'])


def verify_sources(catalog, source):
    for f in catalog['files']:
        p = source / f['path']
        raw = p.read_bytes()
        if digest(raw) != f['sha256']:
            raise ValueError('Source hash changed; re-review citations: ' + f['path'])
        if len(raw.decode('utf-8').splitlines()) != f['lines']:
            raise ValueError('Source line count changed: ' + f['path'])
    actual = {p.relative_to(source).as_posix() for p in source.rglob('*.txt')}
    expected = {f['path'] for f in catalog['files']}
    if actual != expected:
        raise ValueError(f'Source catalog mismatch: extra={sorted(actual-expected)}, missing={sorted(expected-actual)}')


def render_record(item, registry):
    out = [f"# {item['title']}", '', f"标识：`{item['id']}`｜类别：{item['section']}", '']
    labels = {'summary':'内容', 'statement':'归纳', 'epistemic_status':'认识层级', 'mechanism':'机制与证据层级',
              'access_conditions':'接触和使用条件', 'limits':'边界', 'last_known_state':'最后明确状态（不保证跨系列同期）',
              'rp_use':'RP 用法（改编建议）', 'rp_application':'演绎应用', 'time':'时间定位',
              'state_before':'事件前', 'state_after':'事件后', 'knowledge_boundary':'谁知道、何时知道的边界',
              'interpretation':'成长解读', 'stages':'阶段（同一角色的整理顺序，不是世界总时钟）',
              'claims':'存在张力的材料', 'handling':'项目处理约定', 'claim':'连接依据',
              'connection_level':'连接强度', 'reason':'关系依据', 'relation':'关系类型', 'source':'起点', 'target':'终点'}

    def human(value):
        if isinstance(value, str): return value
        if value is None: return '未知／未指定'
        if isinstance(value, list): return '；'.join(human(v) for v in value)
        if isinstance(value, dict): return '；'.join(f'{k}：{human(v)}' for k,v in value.items())
        return str(value)

    for key, label in labels.items():
        if key in item:
            out += [f'## {label}', '']
            value = item[key]
            if isinstance(value, list): out += ['- ' + human(v) for v in value]
            else: out += [human(value)]
            out += ['']
    if item.get('character_ids') or item.get('character_id'):
        out += ['## 关联角色', '']
        for cid in item.get('character_ids', []) + ([item['character_id']] if 'character_id' in item else []):
            out += [f'- [{cid}](../../characters/{cid}.md)']
        out += ['']
    out += ['## 证据', '', '行号基于清理后的本地正文；此处保存定位注释，不分发原文。', '']
    for eid in item['evidence_ids']:
        e = registry[eid]
        origins = '、'.join('本轮正文回读' if p['kind']=='direct_source_review' else
                           f"继承角色注释 {p['character_id']}" for p in e['provenance'])
        out += [f"- `{e['path']}:{e['start_line']}-{e['end_line']}`：{e['supports']}（{origins}；`{eid}`）"]
    return '\n'.join(out) + '\n'


def build_bundle(root=ROOT, source=None):
    catalog = read(root/'data/corpus_catalog.json')
    files = {f['path']: f for f in catalog['files']}
    source = Path(source or catalog['source'])
    verify_sources(catalog, source)
    card_paths = sorted((root/'knowledge/characters').glob('*.json'))
    characters = {p.stem:read(p) for p in card_paths}
    character_index = read(root/'knowledge/index.json')
    coverage = read(root/'knowledge/coverage.json')
    covered = {c['path']:c for c in coverage}
    if set(covered) != set(files) or len(covered) != len(coverage):
        raise ValueError('Character coverage does not match corpus catalog')
    data = {section:read(root/'data/worldbuilding'/f'{section}.json') for section in SECTIONS}
    policy = read(root/'data/worldbuilding/policy.json')
    if {c['id'] for c in character_index['characters']} != set(characters):
        raise ValueError('Character index/card files disagree')
    validate_authored(data, files, characters)
    registry = {}

    def register(e, origin=None):
        validate_evidence(e, files)
        key = '|'.join(str(e[k]) for k in ('path','start_line','end_line','supports'))
        eid = 'evidence_' + digest(key.encode('utf-8'))[:16]
        p = origin or e['provenance']
        if eid not in registry:
            registry[eid] = {k:e[k] for k in ('path','start_line','end_line','supports')}
            registry[eid].update(id=eid,book_id=book_id(e['path']),source_sha256=files[e['path']]['sha256'],provenance=[])
        if p not in registry[eid]['provenance']:
            registry[eid]['provenance'].append(p)
        return eid

    book_facts = defaultdict(dict)
    histories = {}
    for cid, card in characters.items():
        by_book = defaultdict(list)
        for e in card['evidence']:
            eid = register(e, {'kind':'existing_character_annotation','character_id':cid})
            bid = book_id(e['path'])
            fact = book_facts[bid].setdefault(eid, {'evidence_id':eid,'statement':e['supports'],
                    'annotation_character_ids':[], 'classification':'inherited_evidence_annotation'})
            if cid not in fact['annotation_character_ids']: fact['annotation_character_ids'].append(cid)
            if eid not in by_book[bid]: by_book[bid].append(eid)
        histories[cid] = {'id':cid,'name':card['name'],'arc_ids':[], 'curated_event_ids':[],
            'book_evidence':dict(by_book),'character_card':f'../characters/{cid}.json',
            'notice':'这些是证据出现位置；注释关联人物不自动等于事件见证者，书目顺序不等于成长顺序。'}

    records = {}
    book_links = defaultdict(lambda:defaultdict(list))
    for section in SECTIONS:
        records[section] = []
        for raw in data[section]:
            item = copy.deepcopy(raw)
            evidence = item.pop('evidence', [])
            item.update(schema_version='1.0',section=section)
            item.setdefault('title', item.get('reason', item['id']))
            item['evidence_ids'] = list(dict.fromkeys(register(e) for e in evidence))
            item['book_ids'] = sorted({book_id(e['path']) for e in evidence})
            records[section].append(item)
            for bid in item['book_ids']: book_links[bid][section].append(item['id'])
            if section=='arcs': histories[item['character_id']]['arc_ids'].append(item['id'])
            if section=='events':
                for cid in item.get('character_ids',[]): histories[cid]['curated_event_ids'].append(item['id'])

    outputs = {'policy.json':policy, 'evidence.json':{'schema_version':'1.0','entries':registry},
               'character_history_index.json':{'schema_version':'1.0','characters':histories},
               'timeline.json':{'schema_version':'1.0','events':records['events'],'relations':records['relations'],
                    'notice':'before为偏序；没有路径的事件先后未知。展示顺序不是原作总年表。'},
               'scene_template.json':{'schema_version':'1.0','mode':'historical',
                    **{key:[] for key in policy['scene_fields']},
                    'notice':'先定已完成事件，再逐角色确认身体、知识及资源；终局部署不能自动回填。'}}
    index = {'schema_version':'1.0','policy':'policy.json','timeline':'timeline.json','evidence':'evidence.json',
             'character_histories':'character_history_index.json','sections':{},'books':[],
             'retrieval_notice':'注释是证据定位，不等于完整剧情；场景状态使用有证据的事件偏序。'}
    for section, items in records.items():
        index['sections'][section] = []
        for item in items:
            rel = f"{section}/{item['id']}.json"
            outputs[rel] = item
            outputs[rel[:-5]+'.md'] = render_record(item, registry)
            index['sections'][section].append({'id':item['id'],'title':item['title'],'file':rel,
                'kind':item['kind'] if 'kind' in item else section,
                'book_ids':item['book_ids'],'character_ids':item.get('character_ids',[])+
                    ([item['character_id']] if 'character_id' in item else [])})
    all_curated = set()
    direct_books = {e['book_id'] for e in registry.values() if any(p['kind']=='direct_source_review' for p in e['provenance'])}
    coverage_rows = []
    for path, f in files.items():
        bid = book_id(path)
        links = dict(book_links[bid])
        if any(links.get(s) for s in ('entities','events','rules')): all_curated.add(bid)
        facts = sorted(book_facts[bid].values(),key=lambda x:(registry[x['evidence_id']]['start_line'],x['evidence_id']))
        title = title_of(path)
        filename_title = re.sub(r'^\d+[.．\s]*', '', Path(path).stem.strip()).strip()
        row = {'id':bid,'title':title,'aliases':[] if filename_title==title else [filename_title],
               'series':path.split('/')[0],'source_path':path,
               'file':f'books/{bid}.json','inherited_fact_count':len(facts),'curated_links':links,
               'direct_source_review':bid in direct_books}
        index['books'].append(row)
        dossier = {'schema_version':'1.0',**row,'source_sha256':f['sha256'],'source_lines':f['lines'],
            'coverage_type':'all_text_evidence_index', 'chronology':{'calendar_date':None,'book_order_is_chronology':False},
            'characters':covered[path]['included'], 'excluded_character_decisions':covered[path]['excluded'],
            'evidence_fragments':facts,
            'notice':'逐书事件证据入口：继承已有角色卡注释，不是本轮重读全文的完整剧情梗概；注释中没有写出的因果、目击关系及日期不得自动补出。'}
        outputs[row['file']] = dossier
        md = [f"# {row['title']}",'',f"原文：`{path}`｜{f['lines']} 行｜`{bid}`",'',dossier['notice'],'',
              '## 另行整理的关联条目','']
        for section, ids in links.items():
            if section == 'relations': continue
            md += [f"- {LABELS[section]}：" + '、'.join(f'[{i}](../{section}/{i}.md)' for i in ids)]
        md += ['', '## 事件证据片段', '']
        for fact in facts:
            e=registry[fact['evidence_id']]
            names='、'.join(characters[c]['name'] for c in fact['annotation_character_ids'])
            md += [f"- L{e['start_line']}–{e['end_line']}：{fact['statement']}（注释来源角色：{names}）"]
        outputs[f'books/{bid}.md'] = '\n'.join(md)+'\n'
        coverage_rows.append({'book_id':bid,'path':path,'indexed':True,'inherited_fact_count':len(facts),
            'curated_world_link':bid in all_curated,'direct_source_review':bid in direct_books,
            'full_text_reread_this_pass':False})
    index['sections']['books'] = index['books']
    outputs['index.json'] = index
    stats={'source_text_count':len(files),'indexed_text_count':len(coverage_rows),
           'character_history_count':len(histories),'evidence_count':len(registry),
           'inherited_annotation_count':sum(len(v) for v in book_facts.values()),
           'books_linked_to_curated_world_entries':len(all_curated),
           'books_with_direct_source_review':len(direct_books),
           **{s+'_count':len(v) for s,v in records.items()}}
    outputs['coverage.json']={'schema_version':'1.0','stats':stats,'books':coverage_rows,
        'exhaustive_world_extraction':False,'all_texts_indexed':len(files)==len(coverage_rows),
        'notice':'索引全覆盖不等于全部世界观条目、事件和原文已重新精读；细分覆盖字段不互相替代。'}
    readme=['# 统一世界与时间线知识库','',
        '按同一世界前提组织 336 个文本。先读 [世界与演绎说明](../../docs/worldbuilding_guide.md)，再按场景检索。', '',
        f"全量逐书证据入口 {len(files)}；重点事件 {len(records['events'])}；世界规则 {len(records['rules'])}；机构与争夺目标 {len(records['entities'])}；成长线 {len(records['arcs'])}。",'',
        '全部文本复用已有角色证据；另行整理与直接回读的数量见 [coverage.json](coverage.json)。没有声称本轮重读全部正文或穷尽一切设定。','',
        '## 核心入口','',
        '- [检索索引](index.json)、[事件偏序](timeline.json)、[来源证据](evidence.json)',
        '- [统一前提与证据口径](policy.json)、[场景状态模板](scene_template.json)、[全部角色的经历入口](character_history_index.json)','']
    for section in ('rules','entities','events','arcs','bridges','issues'):
        readme += [f'## {LABELS[section]}','']
        readme += [f"- [{item['title']}]({section}/{item['id']}.md)" for item in records[section]]
        readme += ['']
    readme += ['## 全部文本的事件证据入口','','表中顺序只是目录顺序，不代表时间。','']
    for row in index['books']:
        readme += [f"- {row['series']}／[{row['title']}]({row['file'][:-5]}.md)（{row['inherited_fact_count']} 条定位注释）"]
    outputs['README.md']='\n'.join(readme)+'\n'
    inputs=[root/'data/corpus_catalog.json',root/'knowledge/index.json',root/'knowledge/coverage.json',*card_paths,
            *sorted((root/'data/worldbuilding').glob('*.json')),root/'tools/build_world_kb.py']
    outputs['manifest.json']={'schema_version':'1.0','stats':stats,'source_files':catalog['files'],
        'input_hashes':{p.relative_to(root).as_posix():digest(p.read_bytes()) for p in inputs},
        'output_hashes':{name:digest(encode(v).encode('utf-8')) for name,v in outputs.items()},
        'all_texts_indexed':True,'exhaustive_world_extraction':False,
        'build_command':'python -X utf8 tools/build_world_kb.py'}
    return outputs, stats


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=Path,help='Alternative directory containing the same catalogued source snapshot')
    p.add_argument('--check',action='store_true',help='Validate source, references, graph and exact generated output without writing')
    args=p.parse_args()
    try:
        outputs,stats=build_bundle(source=args.source)
        dest=ROOT/'knowledge/world'
        if args.check:
            drift=[name for name,v in outputs.items() if not (dest/name).exists() or (dest/name).read_bytes()!=encode(v).encode('utf-8')]
            if drift: raise ValueError('Generated output missing/stale: '+', '.join(drift[:12]))
        else:
            for name,value in outputs.items():
                path=dest/name
                path.parent.mkdir(parents=True,exist_ok=True)
                path.write_text(encode(value),encoding='utf-8',newline='\n')
            report={'valid':True,'stats':stats,'checks':['source SHA-256 and exact inventory','line bounds',
                'inherited annotation provenance','unique IDs and character references','event and arc references',
                'acyclic before graph','explicit uncertainty and adaptation labels'],
                'limitations':['Structure does not prove interpretation.','All-text indexing is not exhaustive world extraction.']}
            (ROOT/'reports/world_kb_validation.json').write_text(encode(report),encoding='utf-8',newline='\n')
        print(json.dumps({'valid':True,'mode':'check' if args.check else 'build',**stats},ensure_ascii=False,indent=2))
    except (ValueError,KeyError,OSError,UnicodeError) as exc:
        p.exit(1,f'World KB validation failed: {exc}\n')


if __name__=='__main__': main()
