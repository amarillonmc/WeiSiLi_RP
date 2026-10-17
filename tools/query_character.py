"""Retrieve one small, standalone character record without loading the entire corpus."""
import argparse
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]/'knowledge'


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('name',help='Exact character ID, name, alias, or name fragment')
    p.add_argument('--rating',action='store_true',help='Return the separate strength assessment')
    p.add_argument('--markdown',action='store_true')
    a=p.parse_args()
    index=json.loads((ROOT/'index.json').read_text(encoding='utf-8'))
    a.name=index.get('id_redirects',{}).get(a.name,a.name)
    matches=[c for c in index['characters'] if a.name==c['id'] or a.name in [c['name']]+c['aliases']]
    if not matches:matches=[c for c in index['characters'] if any(a.name in n for n in [c['name']]+c['aliases'])]
    if len(matches)!=1:
        print(json.dumps({'matches':matches,'message':'Use an exact ID to distinguish names.'},ensure_ascii=False,indent=2))
        raise SystemExit(0 if matches else 1)
    rel=matches[0]['rating' if a.rating else 'card']
    path=ROOT/rel
    if a.markdown:path=path.with_suffix('.md')
    print(path.read_text(encoding='utf-8'))


if __name__=='__main__':main()
