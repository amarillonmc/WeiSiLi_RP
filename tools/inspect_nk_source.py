"""Read-only encoding and boundary inventory for the original NK corpus."""
import argparse
import collections
import hashlib
import json
from pathlib import Path


def decode(raw):
    if raw.startswith(b'\xef\xbb\xbf'):
        return 'utf-8-sig', raw.decode('utf-8-sig')
    if raw.startswith((b'\xff\xfe', b'\xfe\xff')):
        return 'utf-16', raw.decode('utf-16')
    for encoding in ('utf-8', 'gb18030', 'big5'):
        try:
            return encoding, raw.decode(encoding)
        except UnicodeDecodeError:
            pass
    raise ValueError('No strict decoder succeeded')


def inventory(root):
    items = []
    for path in sorted(root.rglob('*')):
        if not path.is_file():
            continue
        raw = path.read_bytes()
        item = {'path': path.relative_to(root).as_posix(), 'bytes': len(raw),
                'sha256': hashlib.sha256(raw).hexdigest()}
        if path.suffix.lower() == '.txt':
            try:
                encoding, content = decode(raw)
                lines = content.replace('\r\n', '\n').replace('\r', '\n').split('\n')
                item.update(encoding=encoding, chars=len(content), lines=lines)
            except ValueError:
                errors = {}
                for encoding in ('utf-8', 'gb18030', 'gbk', 'big5'):
                    try:
                        raw.decode(encoding)
                    except UnicodeDecodeError as error:
                        errors[encoding] = {'offset':error.start, 'hex':raw[max(0,error.start-8):error.end+8].hex()}
                content = raw.decode('gb18030', errors='surrogateescape')
                lines = content.replace('\r\n', '\n').replace('\r', '\n').split('\n')
                item.update(encoding='gb18030-damaged', errors=errors, chars=len(content), lines=lines)
        items.append(item)
    return items


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    items = inventory(args.root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(json.dumps(items, ensure_ascii=False, indent=2).encode('utf-8', errors='backslashreplace'))
    print(json.dumps({'files':len(items), 'bytes':sum(x['bytes'] for x in items),
                      'encodings':dict(collections.Counter(x.get('encoding','binary') for x in items)),
                      'series':dict(collections.Counter(x['path'].split('/')[0] for x in items))},
                     ensure_ascii=False, indent=2))
    for item in items:
        if item.get('errors'):
            print(json.dumps({k:v for k,v in item.items() if k != 'lines'}, ensure_ascii=False))
    print('Control bytes:', dict(collections.Counter(c for item in items for line in item.get('lines',[]) for c in line if ord(c)<32 and c!='\t')))


if __name__ == '__main__':
    main()
