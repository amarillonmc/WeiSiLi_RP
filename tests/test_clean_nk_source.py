import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from clean_nk_source import clean, commit, decode, dump, prepare, sha


class TextCleaningTests(unittest.TestCase):
    def body(self, text, **rule):
        return clean(text, {'path':'novel.txt', **rule})[0]

    def test_css_header_without_closing_comment_does_not_eat_story(self):
        text='倪匡-->妖偶-->一 <!--\n第一章\n她推开门，走了进去。\n回目录'
        self.assertEqual(self.body(text), '第一章\n她推开门，走了进去。\n')

    def test_navigation_is_removed_without_losing_attached_prose(self):
        self.assertEqual(self.body('她笑了。   后一页\n前一页\n回目录'), '她笑了。\n')
        text='他翻到下一页。\n亮声说：“请看下一页！”'
        self.assertEqual(self.body(text), text+'\n')

    def test_end_markers_do_not_remove_words_ending_in_wan(self):
        self.assertEqual(self.body('这话还没说完\n她笑了。 （完）\n（全文完）'),
                         '这话还没说完\n她笑了。\n')

    def test_inline_watermark_keeps_both_halves(self):
        self.assertEqual(self.body('他用力一[网罗电子书：www.WRbook.com]推。'), '他用力一推。\n')

    def test_reviewed_range_keeps_fictional_prefaces(self):
        text='整合者说明\n序言\n白素将那封信递给我。\n后记\n事情仍在继续。'
        self.assertEqual(self.body(text,start_line=2), '序言\n白素将那封信递给我。\n后记\n事情仍在继续。\n')

    def test_reader_intro_glued_to_story(self):
        result=self.body('网友介绍。以下就是故事全文：故事正文。',
                         line_edits=[{'line':1,'keep_after':'以下就是故事全文：','reason':'reader_introduction'}])
        self.assertEqual(result, '故事正文。\n')

    def test_author_signature_glued_to_first_chapter(self):
        result=clean('倪匡二〇〇一年第一部阿尔卑斯保险库由于钱财的关系。',
                     {'path':'卫斯理系列/138财神宝库.txt','start_line':1})[0]
        self.assertEqual(result, '第一部阿尔卑斯保险库\n由于钱财的关系。\n')

    def test_dated_editorial_note_preserves_narrative_parentheses(self):
        text='他停下来（他正在听）。\n（一九八六年加按：重印说明（补充）。）\n她走了。'
        self.assertEqual(self.body(text), '他停下来（他正在听）。\n\n她走了。\n')

    def test_damaged_byte_is_explicit_and_offset_is_exact(self):
        raw='正文'.encode('gb18030')+b'\xff'+b'A'
        text,damage=decode(raw)
        self.assertEqual(text, '正文\ufffdA')
        self.assertEqual(damage,[{'byte_offset':4,'hex':'ff'}])

    def test_legacy_indentation_removed_but_unknown_pua_kept(self):
        self.assertEqual(self.body('\ue4c6\ue4c6正文\ue001\x00\n\n\n尾声'), '正文\ue001\n\n尾声\n')


class BackupAndApplyTests(unittest.TestCase):
    def fixture(self, root):
        source=root/'source';source.mkdir()
        originals={'novel.txt':'小说正文\r\n（全文完）'.encode('gb18030'),
                   '序.txt':'编辑说明'.encode('gb18030'),'photo.jpg':b'original image bytes'}
        rules=[]
        for name,raw in originals.items():
            (source/name).write_bytes(raw)
            rule={'path':name,'sha256':sha(raw)}
            if name!='novel.txt':rule['exclude']='non-body'
            rules.append(rule)
        review=root/'review.json';dump(review,{'files':rules})
        run=root/'run'
        prepare(source,review,run)
        return source,run,originals

    def test_apply_retry_and_restore_are_byte_exact(self):
        with tempfile.TemporaryDirectory() as tmp, contextlib.redirect_stdout(io.StringIO()):
            source,run,originals=self.fixture(Path(tmp))
            commit(run);commit(run)
            self.assertEqual({p.name for p in source.iterdir()},{'novel.txt'})
            self.assertEqual((source/'novel.txt').read_bytes(),'小说正文\n'.encode('utf-8'))
            commit(run,restore=True)
            self.assertEqual({p.name:p.read_bytes() for p in source.iterdir()},originals)

    def test_changed_preview_aborts_before_any_source_mutation(self):
        with tempfile.TemporaryDirectory() as tmp, contextlib.redirect_stdout(io.StringIO()):
            source,run,originals=self.fixture(Path(tmp))
            (run/'preview'/'novel.txt').write_text('unreviewed change',encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'Preview changed'):commit(run)
            self.assertEqual({p.name:p.read_bytes() for p in source.iterdir()},originals)

    def test_changed_original_aborts_before_any_source_mutation(self):
        with tempfile.TemporaryDirectory() as tmp, contextlib.redirect_stdout(io.StringIO()):
            source,run,originals=self.fixture(Path(tmp))
            (source/'novel.txt').write_bytes(b'user edit')
            with self.assertRaisesRegex(ValueError,'File changed'):commit(run)
            self.assertEqual((source/'novel.txt').read_bytes(),b'user edit')
            self.assertEqual((source/'序.txt').read_bytes(),originals['序.txt'])


if __name__=='__main__':
    unittest.main()
