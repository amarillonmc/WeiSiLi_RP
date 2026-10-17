"""Verify every prepared or applied text against its cleanup report."""
import argparse
import json
import re
from pathlib import Path

from clean_nk_source import dump, sha

JUNK = re.compile(r'www[.．]|https?[:：]|umdtxt|WRbook|潇湘书院|起点书缘|'
                  r'注册回应人|文后语：|以下就是故事全文：|^倪匡-->|^#page \{',re.M)


def verify(run, preview=False):
    report=json.loads((run/'report.json').read_text(encoding='utf-8'))
    root=run/'preview' if preview else Path(report['source'])
    expected={r['path']:r for r in report['files'] if r['action']=='clean'}
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    if actual!=set(expected):
        raise ValueError(f'Unexpected inventory: missing={set(expected)-actual}, extra={actual-set(expected)}')
    contents={}
    for relative,item in expected.items():
        raw=(root/relative).read_bytes()
        if sha(raw)!=item['utf8_sha256']:
            raise ValueError(f'Hash mismatch: {relative}')
        text=raw.decode('utf-8',errors='strict')
        if not text.strip() or text.startswith('\ufeff') or '\r' in text or '\x00' in text or '\ue4c6' in text:
            raise ValueError(f'Encoding/control issue: {relative}')
        if '\n\n\n' in text or not text.endswith('\n') or any(line!=line.strip() for line in text.splitlines()):
            raise ValueError(f'Whitespace issue: {relative}')
        if JUNK.search(text):
            raise ValueError(f'Known web metadata remains: {relative}')
        contents[relative]=text
    snake=contents['亚洲之鹰罗开系列/06蛇神.txt']
    if re.findall(r'^\d{2}$',snake,re.M)!=[f'{n:02d}' for n in range(1,11)]:
        raise ValueError('Snake chapter order changed')
    safeguards={
        '亚洲之鹰罗开系列/13困兽.txt':'序言',
        '卫斯理系列/046头发.txt':'后  记',
        '卫斯理系列/059神仙.txt':'后记',
        '卫斯理系列/117双程.txt':'后记：一位物理学家的来信',
        '原振侠系列/02.迷路.txt':'楔子',
        '原振侠系列/25.黑白无常.txt':'前言',
    }
    for relative,marker in safeguards.items():
        if marker not in contents[relative]:
            raise ValueError(f'Story section missing: {relative}, {marker}')
    result={'verified_files':len(expected),'strict_utf8':True,'bom':False,'line_endings':'LF',
            'hashes_match':True,'known_web_metadata_matches':0,
            'snake_chapters':'01–10, each once','preserved_story_sections_checked':list(safeguards),
            'root':str(root.resolve())}
    dump(run/('preview_verification.json' if preview else 'source_verification.json'),result)
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run',type=Path,required=True)
    parser.add_argument('--preview',action='store_true')
    args=parser.parse_args()
    verify(args.run,args.preview)
