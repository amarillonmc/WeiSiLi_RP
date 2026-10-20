"""Query TRPG modules by exact ID, keyword, book, character, or heat.

The player projection is deliberately small. It is a convenience for avoiding
spoilers, not an access-control boundary on a local knowledge repository.
"""
import argparse
import json
from pathlib import Path

from build_trpg_kb import MODULES, ROOT


def player_projection(item, kind):
    out={'id':item['id'],'name':item['public_name'],'kind':kind,'audience':'player'}
    if kind=='scenarios':
        out['hook']=item['three_layer_epistemic_trap']['layer_1_hook']
    elif kind=='artifacts':
        out['initial_belief']=item['surface_phenomenon_believes']
    # Even names may be spoilers; the GM must choose which ID is introduced.
    out['disclosure_note']='仅在主持人已决定公开该对象名称时使用；表象不保证为真。'
    return out


def search(root=ROOT, query='', kind=None, book=None, character=None, heat=None, audience='gm'):
    if audience not in {'gm','player'}:
        raise ValueError('Unknown audience')
    index=json.loads((root/'knowledge/trpg_modules/index.json').read_text(encoding='utf-8'))
    if audience=='player' and any(x is not None for x in (book,character,heat)):
        raise ValueError('Book, character and heat filters require --audience gm; use a disclosed exact ID for players.')
    rows=[row for row in index['records'] if not kind or row['kind']==kind]
    if book:
        rows=[row for row in rows if any(book.casefold() in p.casefold() for p in row['source_books'])]
    if character:
        rows=[row for row in rows if character in row['character_ids']]
    if heat is not None:
        rows=[row for row in rows if row['heat']<=heat]
    selected={row['id'] for row in rows}
    hits=[]
    for module,(filename,key) in MODULES.items():
        if kind and module!=kind:
            continue
        data=json.loads((root/'knowledge/trpg_modules'/filename).read_text(encoding='utf-8'))
        for item in data[key]:
            if item['id'] not in selected:
                continue
            visible=player_projection(item,module) if audience=='player' else item
            if not query or query.casefold() in json.dumps(visible,ensure_ascii=False).casefold():
                hits.append((module,visible))
    exact=[x for x in hits if x[1]['id']==query]
    if exact:
        return exact[0][1]
    if len(hits)==1:
        return hits[0][1]
    return {'matches':len(hits),'candidates':[
        dict(id=x['id'],name=x['name'],kind=k,**({'source_books':x['source_books']} if audience=='gm' else {}))
        for k,x in hits], 'hint':'用明确 ID 读取单条；候选不会自动拼成同一人或同一机制。'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('query',nargs='?',default='')
    p.add_argument('--kind',choices=MODULES)
    p.add_argument('--book')
    p.add_argument('--character',help='Exact existing character ID')
    p.add_argument('--heat',type=int,help='Maximum recommended heat, not an automatic spawn command')
    p.add_argument('--audience',choices=('gm','player'),default='gm')
    a=p.parse_args()
    try:
        result=search(query=a.query,kind=a.kind,book=a.book,character=a.character,heat=a.heat,audience=a.audience)
    except ValueError as e:
        p.error(str(e))
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
