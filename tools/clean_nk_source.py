"""Conservative, hash-locked cleaning of the reviewed NK_Source snapshot.

prepare creates a byte-exact ZIP backup, UTF-8 preview, and removal log.
apply checks all originals and previews before changing individual source files.
restore verifies the current state and restores every original byte from the ZIP.
Only the files explicitly named in the review manifest are handled.
"""
import argparse
import collections
import hashlib
import json
import os
import re
import zipfile
from pathlib import Path

NAV = re.compile(r'(?:后一页|後一頁|前一页|前一頁|上一页|下一页|回目录|回目錄|回首页|回首頁|目\s*录)+$')
DECOR = re.compile(r'[-—─━═_=＊*＃#－~～☆★\s]{2,}')
END = re.compile(r'[\s—\-─一＜>〈〉<>（(﹝\[【︵]*(?:全[文书書篇]|本篇)?完[\s—\-─一＞>〈〉<>）)﹞\]】︶]*$')
SITE = re.compile(
    r'^(?:起点书缘|您下载的|欢迎访问[:：]|更多精采，更多好书|更多免费电子书|手机访问wap\.|'
    r'声明：本电子书|.*·潇湘书院·|阅读设置[:：]|9pt字体10pt字体|'
    r'坐拥书城扫描校对|清风免费电子书下载注：|更多精彩好书|更多免费txt电子书|注册回应人:|'
    r'倪匡科幻小说收集站|炽天使书城OCR小组|文学殿堂|黄金屋|'
    r'书剑梦（http|娱乐先锋|转载自科幻天空BBS|转自文学殿堂|'
    r'转自\s*百草园|百草园.*(?:扫校|扫描)|倪匡科幻屋\s*扫校|'
    r'(?:扫描|扫瞄|掃描|掃瞄|录入)[\s、&]*(?:校对|校正)?[：:﹕]|'
    r'扫描[＆&]排校[：:]|扫描\s*&\s*校对[：:]|本章特别感谢修罗朋友提供|'
    r'\d{4}[.\d()—-]+.*明报连载|'
    r'http://members\.spree\.com/sip/greenland/|转载请保留$|'
    r'本文由星际飞船|扫描输入，转载请保留全文。$)')
AUTHOR = re.compile(r'^(?:作者|原著)[：:]\s*倪匡(?:（原振侠系列）)?$')
EDITOR_NOTE = re.compile(r'[（(]一九八六年(?:加)?按[：:，,]')
WATERMARKS = ('本书由umdtxt.com提供下载','[网罗电子书：www.WRbook.com]')
MISSING_PAGE = '（原书残缺一页，请有书的朋友帮忙补全，谢谢！邮箱：allan9@netease.com）'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')


def safe_path(root, relative):
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()) or path == root.resolve():
        raise ValueError(f'Path outside root: {relative}')
    return path


def decode(raw):
    """No encoding guesses: this reviewed snapshot is in the GBK family.

    Invalid bytes are explicitly counted/logged, represented by U+FFFD, and
    preserved verbatim in originals.zip. Never ignore errors or invent words.
    """
    content = raw.decode('gb18030', errors='surrogateescape')
    damage = []
    offset = 0
    for c in content:
        b = c.encode('gb18030', errors='surrogateescape')
        if 0xdc80 <= ord(c) <= 0xdcff:
            damage.append({'byte_offset': offset, 'hex': b.hex()})
        offset += len(b)
    content = ''.join('\ufffd' if 0xdc80 <= ord(c) <= 0xdcff else c for c in content)
    return content.replace('\r\n','\n').replace('\r','\n'), damage


def clean(content, rule):
    lines = content.split('\n')
    events = []
    output = []
    counts = collections.Counter()
    ranges = rule.get('remove_ranges', [])
    for n, original in enumerate(lines, 1):
        if n < rule.get('start_line', 1) or n > rule.get('end_line',len(lines)) or any(a<=n<=b for a,b in ranges):
            if original.strip():
                events.append({'line':n,'reason':'reviewed_paratext','before':original,'after':''})
            continue
        # U+E4C6 is the legacy indentation glyph in this snapshot, not prose.
        s = original.replace('\x00','').replace('\ue4c6',' ').strip()
        if s != original:
            counts['whitespace_or_control_lines'] += 1
        reason = None
        for before,after in rule.get('literal_replacements',[]):
            if s==before:
                s=after
                events.append({'line':n,'reason':'reviewed_metadata','before':before,'after':after})
                counts['reviewed_metadata'] += 1
        for edit in rule.get('line_edits',[]):
            if n == edit['line']:
                if edit['keep_after'] not in s:
                    raise ValueError('Reviewed text boundary not found')
                s = s.split(edit['keep_after'],1)[1]
                events.append({'line':n,'reason':edit['reason'],'before':original,'after':s})
                counts[edit['reason']] += 1
        for watermark in (*WATERMARKS,MISSING_PAGE):
            if watermark in s:
                before = s
                s = s.replace(watermark,'').strip()
                events.append({'line':n,'reason':'inline_editor_or_watermark','before':before,'after':s})
                counts['inline_editor_or_watermark'] += 1
        # These two first chapters were glued to the author's dated signature.
        if rule['path'].endswith(('138财神宝库.txt','139一半一半.txt')) and n==rule['start_line']:
            s = s[s.index('第一部'):]
            title = '第一部阿尔卑斯保险库' if '138财神' in rule['path'] else '第一部又失手了'
            s = s.replace(title,title+'\n',1)
            reason = 'author_signature_glued_to_chapter'
            events.append({'line':n,'reason':reason,'before':original,'after':s})
            counts[reason] += 1
            reason = None
        if re.match(r'^倪匡-->',s) or s.startswith(('#page {','.tt3 {','.tt2 {','a {text-decoration:','a:hover {')) or s=='-->':
            reason = 'web_css_header'
        if reason:
            s = ''
        else:
            # Navigation may share the final narrative line. Keep that prose.
            nav = NAV.search(s)
            if nav and (nav.start()==0 or s[nav.start()-1].isspace()):
                s = s[:nav.start()].rstrip()
                reason = 'web_navigation'
            if SITE.match(s) or AUTHOR.fullmatch(s) or s in ('正文','——非人协会系列') or n<20 and s=='倪匡':
                s = ''
                reason = 'site_or_author_metadata'
            elif s in ('(待续)','（待续）') or re.fullmatch(r'第[一二三四五六七八九十0-9]+[章集]完[、，,]?(?:待续)?[。.]?',s):
                s = ''
                reason = 'continuation_marker'
            elif re.search(r'\s+原著[：:]\s*倪匡',s):
                s = re.split(r'\s+原著[：:]\s*倪匡',s)[0].rstrip()
                reason = 'chapter_scan_credit'
            # Decorations are allowed to become one blank section break.
            if DECOR.fullmatch(s):
                s = ''
                reason = 'decoration'
            else:
                s2 = re.sub(r'\s*[-—─━═_=＊*＃#－~～]{6,}\s*$', '', s)
                if s2 != s:
                    reason = 'decoration_suffix'
                    s = s2
            end = END.search(s)
            if end and (end.start()==0 or end.group().lstrip()[:1] in '（(﹝[【—-＜<︵'):
                s = s[:end.start()].rstrip()
                reason = 'end_marker'
        if reason:
            counts[reason] += 1
            events.append({'line':n,'reason':reason,'before':original,'after':s})
        if s or output and output[-1] != '':
            output.append(s)
    text = '\n'.join(output).strip()+'\n'
    # Remove only explicitly dated editorial additions, not narrative parentheses.
    for match in reversed(list(EDITOR_NOTE.finditer(text))):
        start = match.start()
        depth = 0
        end = None
        for pos in range(start,len(text)):
            if text[pos] in '（(':
                depth += 1
            elif text[pos] in '）)':
                depth -= 1
                if depth == 0:
                    end = pos+1
                    break
        if end is None or end-start > 1600:
            raise ValueError('Unterminated editorial note')
        events.append({'reason':'dated_editorial_note','before':text[start:end],'after':''})
        counts['dated_editorial_note'] += 1
        text = text[:start]+text[end:]
    text = re.sub(r'\n{3,}','\n\n',text).strip()+'\n'
    if not text.strip():
        raise ValueError('Unexpected empty novel')
    return text, events, dict(counts)


def prepare(source, review_path, run):
    review = json.loads(review_path.read_text(encoding='utf-8'))
    if run.exists():
        raise ValueError('Run directory already exists; use a new path to preserve backups')
    actual = {p.relative_to(source).as_posix() for p in source.rglob('*') if p.is_file()}
    expected = {r['path'] for r in review['files']}
    if actual != expected:
        raise ValueError(f'Inventory changed: missing={expected-actual}, extra={actual-expected}')
    raw_files = {}
    for rule in review['files']:
        path = safe_path(source,rule['path'])
        if path.is_symlink() or path.is_junction():
            raise ValueError(f'Linked file: {path}')
        raw = path.read_bytes()
        if sha(raw) != rule['sha256']:
            raise ValueError(f'Original changed: {path}')
        raw_files[rule['path']] = raw
    run.mkdir(parents=True)
    dump(run/'review.json',review)
    with zipfile.ZipFile(run/'originals.zip','x',compression=zipfile.ZIP_DEFLATED) as archive:
        for relative,raw in raw_files.items():
            archive.writestr(relative,raw)
    with zipfile.ZipFile(run/'originals.zip') as archive:
        for relative,raw in raw_files.items():
            if sha(archive.read(relative)) != sha(raw):
                raise ValueError(f'Backup verification failed: {relative}')
    reports = []
    with (run/'removals.jsonl').open('w',encoding='utf-8',newline='\n') as log:
        for rule in review['files']:
            relative = rule['path']
            raw = raw_files[relative]
            report = {'path':relative,'original_sha256':sha(raw),'original_bytes':len(raw),
                      'quality_notes':rule.get('quality_notes',[]),'change_notes':rule.get('change_notes',[])}
            if rule.get('exclude'):
                report.update(action='exclude',reason=rule['exclude'])
                target = safe_path(run/'excluded',relative)
                target.parent.mkdir(parents=True,exist_ok=True)
                if relative.endswith('.txt'):
                    content,damage = decode(raw)
                    target.write_bytes(content.encode('utf-8'))
                else:
                    target.write_bytes(raw)
            else:
                content,damage = decode(raw)
                result,events,counts = clean(content,rule)
                target = safe_path(run/'preview',relative)
                target.parent.mkdir(parents=True,exist_ok=True)
                result_raw = result.encode('utf-8')
                target.write_bytes(result_raw)
                for event in events:
                    log.write(json.dumps({'path':relative,**event},ensure_ascii=False)+'\n')
                pua = [{'line':i,'codepoints':sorted({f'U+{ord(c):04X}' for c in s if '\ue000'<=c<='\uf8ff'})}
                       for i,s in enumerate(result.splitlines(),1) if any('\ue000'<=c<='\uf8ff' for c in s)]
                report.update(action='clean',utf8_sha256=sha(result_raw),utf8_bytes=len(result_raw),
                              original_chars=len(content),clean_chars=len(result),
                              removed_chars=len(content)-len(result),rules=counts,
                              invalid_original_bytes=damage,remaining_pua_lines=pua,
                              replacement_characters=result.count('\ufffd'),
                              first_lines=result.splitlines()[:3],last_lines=result.splitlines()[-3:])
            reports.append(report)
    totals = {'original_files':len(reports),'novel_files':sum(r['action']=='clean' for r in reports),
              'excluded_files':sum(r['action']=='exclude' for r in reports),
              'original_bytes':sum(r['original_bytes'] for r in reports),
              'utf8_body_bytes':sum(r.get('utf8_bytes',0) for r in reports),
              'removed_chars_in_novels':sum(r.get('removed_chars',0) for r in reports),
              'originally_damaged_files':sum(bool(r.get('invalid_original_bytes')) for r in reports),
              'unrecoverable_byte_markers':sum(r.get('replacement_characters',0) for r in reports),
              'files_with_remaining_pua':sum(bool(r.get('remaining_pua_lines')) for r in reports)}
    dump(run/'report.json',{'source':str(source.resolve()),'summary':totals,'files':reports})
    print(json.dumps(totals,ensure_ascii=False,indent=2))


def commit(run, restore=False):
    report = json.loads((run/'report.json').read_text(encoding='utf-8'))
    source = Path(report['source']).resolve()
    prepared = []
    with zipfile.ZipFile(run/'originals.zip') as archive:
        for item in report['files']:
            relative = item['path']
            original = archive.read(relative)
            if sha(original) != item['original_sha256']:
                raise ValueError(f'Corrupt backup: {relative}')
            path = safe_path(source,relative)
            current = sha(path.read_bytes()) if path.exists() else None
            cleaned_sha = item.get('utf8_sha256')
            # This permits safe retries after an interruption, but not overwrites
            # of unrelated edits made since preparation/application.
            if current not in (item['original_sha256'],cleaned_sha):
                raise ValueError(f'File changed since review: {relative}')
            if restore:
                target = original
            elif item['action']=='clean':
                target = safe_path(run/'preview',relative).read_bytes()
                if sha(target) != cleaned_sha:
                    raise ValueError(f'Preview changed: {relative}')
                target.decode('utf-8',errors='strict')
            else:
                target = None
            prepared.append((path,target))
    for path,raw in prepared:
        if raw is None:
            # Explicit individual files only, after verified backups and bounds.
            path.unlink(missing_ok=True)
        else:
            path.parent.mkdir(parents=True,exist_ok=True)
            temp = path.with_name(path.name+'.nk-clean-tmp')
            with temp.open('xb') as file:
                file.write(raw)
            os.replace(temp,path)
            if sha(path.read_bytes()) != sha(raw):
                raise ValueError(f'Write verification failed: {path}')
    dump(run/('restored.json' if restore else 'applied.json'),{'verified_files':len(prepared),'source':str(source)})
    print(f'{"Restored" if restore else "Applied and verified"}: {len(prepared)} files')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='mode',required=True)
    prepare_parser = sub.add_parser('prepare')
    prepare_parser.add_argument('--source',type=Path,required=True)
    prepare_parser.add_argument('--review',type=Path,required=True)
    prepare_parser.add_argument('--run',type=Path,required=True)
    for command in ('apply','restore'):
        sub.add_parser(command).add_argument('--run',type=Path,required=True)
    args = parser.parse_args()
    if args.mode=='prepare':
        prepare(args.source,args.review,args.run)
    else:
        commit(args.run,restore=args.mode=='restore')


if __name__=='__main__':
    main()
