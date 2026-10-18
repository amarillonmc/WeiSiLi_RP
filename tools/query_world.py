"""Retrieve a world entry, source-book dossier, character history or partial RP state."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from build_world_kb import ancestors, topological_order

ROOT = Path(__file__).resolve().parents[1]
WORLD = ROOT/'knowledge/world'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def resolve_character(name, index):
    name = index.get('id_redirects', {}).get(name, name)
    exact = [c for c in index['characters'] if name == c['id'] or name in [c['name'], *c['aliases']]]
    return exact or [c for c in index['characters'] if any(name in n for n in [c['name'], *c['aliases']])]


def attach_evidence(record, registry):
    return {**record,'evidence':[registry[eid] for eid in record.get('evidence_ids',[])]}


def scene_package(selected, timeline, arcs, character_names, character_ids=None, include_inferred=False):
    """Never loads terminal character cards or terminal entity descriptions.

    The result is a GM state aid. Temporal availability does not establish who
    witnessed an event or was told its secrets. Incomparable frontier states are
    returned together, rather than silently imposing an invented global clock.
    """
    events = {e['id']:e for e in timeline['events']}
    relations = timeline['relations']
    known = ancestors(selected, events, relations, include_inferred)
    order = [i for i in topological_order(events, relations, include_inferred) if i in known]
    requested = list(character_ids or sorted({cid for i in selected for cid in events[i].get('character_ids',[])}))
    states = []
    for cid in requested:
        relevant = {i for i in known if cid in events[i].get('character_ids',[])}
        superseded = set()
        for event in relevant:
            superseded |= (ancestors([event], events, relations, include_inferred)-{event}) & relevant
        frontier = sorted(relevant-superseded)
        usable = []
        for arc in arcs:
            if arc['character_id'] != cid: continue
            for stage in arc['stages']:
                if set(stage['event_ids']) <= known:
                    usable.append({'label':stage['label'],'event_ids':stage['event_ids'],
                                   'state':stage['state'],'rp_constraint':stage['rp_constraint']})
        states.append({'character_id':cid,'name':character_names.get(cid,cid),
            'frontier_event_ids':frontier,
            'state_updates':[{'event_id':i,'state_after':events[i]['state_after'],
                              'knowledge_boundary':events[i]['knowledge_boundary']} for i in frontier],
            'confirmed_history_stages':usable,
            'incomparable_frontiers':len(frontier)>1,
            'knowledge_assignment':{'knows':[],'believes':[],'suspects':[]},
            'notice':'frontier给出当前约束；history只供回溯，不叠加旧身体或旧资源。空白知情表等待按亲历和传讯确认。'})
    return {'schema_version':'1.0','audience':'GM_state_not_character_memory',
        'selected_completed_event_ids':list(selected),'completed_event_ids':order,
        'inferred_order_enabled':include_inferred,
        'inferred_relations_used':[r['id'] for r in relations if include_inferred and
            r['relation']=='before' and r['epistemic_status']!='textual_fact' and r['source'] in known and r['target'] in known],
        'character_states':states,
        'history_events':[events[i] for i in order],
        'events_not_in_completed_set_count':len(events)-len(known),
        'terminal_character_cards_loaded':False,'terminal_entity_states_loaded':False,
        'scenario_overrides':[],
        'limits':['未选中且无先后证据的支线保持未知，不能因缺席就判定尚未发生。',
                  '知识随亲历或传讯分配，不能把读者真相自动写进角色记忆。',
                  '多个不可比较的状态需要GM选择或明确并存，不能按列表最后一项覆盖。']}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('query',nargs='?',help='ID, title or keyword; without a query show a compact catalog')
    p.add_argument('--kind',choices=['rules','entities','events','arcs','issues','bridges','relations'])
    p.add_argument('--book',help='Exact source path, book ID, title or fragment')
    p.add_argument('--character',help='Character name, alias or canonical ID')
    p.add_argument('--scene',help='Event ID already completed in the scenario')
    p.add_argument('--after',action='append',default=[],help='Additional explicitly completed event ID (repeatable)')
    p.add_argument('--include-inferred',action='store_true',help='Opt into project-inferred chronological edges')
    p.add_argument('--markdown',action='store_true',help='Readable record; scenes are returned as JSON')
    p.add_argument('--limit',type=int,default=20)
    args=p.parse_args()
    if args.limit<1: p.error('--limit must be positive')
    if args.after and not args.scene: p.error('--after requires --scene')
    if args.include_inferred and not args.scene: p.error('--include-inferred requires --scene')
    if args.book and (args.scene or args.character): p.error('--book cannot be combined with --scene or --character')
    if args.query and (args.scene or args.character or args.book): p.error('Use one of positional query, --book, or --character/--scene')
    try:
        index=read(WORLD/'index.json')
        registry=read(WORLD/'evidence.json')['entries']
        char_index=read(ROOT/'knowledge/index.json')
        cids=None
        if args.character:
            candidates=resolve_character(args.character,char_index)
            if len(candidates)!=1:
                print(json.dumps({'matches':candidates,'message':'请用确切角色 ID 区分；没有自动选择同名人物。'},ensure_ascii=False,indent=2))
                return 2 if candidates else 1
            cids=[candidates[0]['id']]
        if args.scene:
            timeline=read(WORLD/'timeline.json')
            arcs=[read(WORLD/e['file']) for e in index['sections']['arcs']]
            result=scene_package([args.scene,*args.after],timeline,arcs,
                {c['id']:c['name'] for c in char_index['characters']},cids,args.include_inferred)
            eids={eid for e in result['history_events'] for eid in e.get('evidence_ids',[])}
            result['evidence']={eid:registry[eid] for eid in sorted(eids)}
        elif args.character:
            history=read(WORLD/'character_history_index.json')['characters'][cids[0]]
            result={'audience':'GM_reference_may_contain_later_events',**history,
                'arcs':[attach_evidence(read(WORLD/'arcs'/f'{a}.json'),registry) for a in history['arc_ids']],
                'books':[b for b in index['books'] if b['id'] in history['book_evidence']]}
        else:
            query=args.book or args.query
            sections=[args.kind] if args.kind else [s for s in index['sections'] if s!='books']
            pool=index['books'] if args.book else [e for s in sections for e in index['sections'][s]]
            if not query:
                result={'stats':read(WORLD/'manifest.json')['stats'],
                        'sections':{s:len(v) for s,v in index['sections'].items()},
                        'usage':'按词检索；--book 取逐书证据；--character 取经历；--scene 生成部分历史状态。'}
            else:
                matches=[e for e in pool if query in (e['id'],e['title'],e.get('source_path'),*e.get('aliases',[]))]
                if not matches:
                    matches=[e for e in pool if query.casefold() in json.dumps(read(WORLD/e['file']),ensure_ascii=False).casefold()]
                if len(matches)!=1:
                    print(json.dumps({'matches':matches[:args.limit],'total_matches':len(matches),
                        'message':'请用确切 ID 读取单条；候选只是检索相关，不表示同名即同物。'},ensure_ascii=False,indent=2))
                    return 0 if matches else 1
                entry=matches[0]
                if args.markdown:
                    print((WORLD/entry['file']).with_suffix('.md').read_text(encoding='utf-8'))
                    return 0
                result=read(WORLD/entry['file'])
                if args.book:
                    result['evidence']={f['evidence_id']:registry[f['evidence_id']] for f in result['evidence_fragments']}
                else: result=attach_evidence(result,registry)
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return 0
    except (OSError,KeyError,ValueError) as exc:
        p.exit(1,f'World query failed: {exc}\n')


if __name__=='__main__': raise SystemExit(main())
