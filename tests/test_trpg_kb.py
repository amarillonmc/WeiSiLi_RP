"""Reject evidence drift and prevent GM-only facts entering the player view."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from build_trpg_kb import convert, validate_records
from query_trpg import player_projection, search


class TrpgKnowledgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records=json.loads((ROOT/'data/trpg_modules/dossiers.json').read_text(encoding='utf-8'))
        cls.files={f['path']:f for f in json.loads((ROOT/'data/corpus_catalog.json').read_text(encoding='utf-8'))['files']}
        cls.characters={c['id'] for c in json.loads((ROOT/'knowledge/index.json').read_text(encoding='utf-8'))['characters']}

    def check(self,records):
        validate_records(records,self.files,self.characters)

    def test_rejects_invalid_or_missing_source_evidence(self):
        for mutate in (
            lambda r:r['evidence'][0].update(end_line=10**9),
            lambda r:r['evidence'][0].update(start_line=True),
            lambda r:r['evidence'][0].update(path='invented.txt'),
            lambda r:r.update(evidence=[]),
            lambda r:r['evidence'][0].update(supports=''),
        ):
            with self.subTest(mutate=mutate):
                r=copy.deepcopy(self.records[0]);mutate(r)
                with self.assertRaises(ValueError):self.check([r])

    def test_cannot_promote_dice_to_canonical_fact(self):
        r=copy.deepcopy(self.records[0])
        r['canonical']['mechanism']='原著证明每轮 d40 攻击。'
        with self.assertRaisesRegex(ValueError,'Game mechanic'):self.check([r])
        r=copy.deepcopy(self.records[0]);del r['canonical']['counter_status']
        with self.assertRaisesRegex(ValueError,'counter epistemic'):self.check([r])

    def test_boss_requires_existing_identity_and_deployment_conditions(self):
        original=next(r for r in self.records if 'boss' in r)
        r=copy.deepcopy(original);r['boss']['card_id']='yuanzhenxia_maxian'
        with self.assertRaisesRegex(ValueError,'boss link'):self.check([r])
        r=copy.deepcopy(original);r['boss']['phase']=''
        with self.assertRaisesRegex(ValueError,'deployment'):self.check([r])
        r=copy.deepcopy(original);r['boss']['moves'][0]['condition']=''
        with self.assertRaisesRegex(ValueError,'Unconditioned'):self.check([r])

    def test_ambiguous_names_return_candidates_and_exact_id_resolves(self):
        result=search(query='透明光')
        self.assertGreater(result['matches'],1)
        selected=search(query='artifact_transparent_mineral')
        self.assertEqual(selected['id'],'artifact_transparent_mineral')
        self.assertEqual(selected['canonical']['mechanism_status'],'mixed')

    def test_player_view_has_no_truth_evidence_or_agendas(self):
        r=next(r for r in self.records if r['id']=='ghost_parking')
        module=convert(r,self.files)['scenarios']
        player=player_projection(module,'scenarios')
        self.assertEqual(player['name'],'停车场失车案')
        self.assertNotIn('叙述者身份',json.dumps(player,ensure_ascii=False))
        self.assertNotIn('canonical',player)
        self.assertNotIn('evidence',player)
        self.assertNotIn('mutual_exclusive_agendas',player)
        self.assertNotIn('layer_3_core_truth',json.dumps(player))
        self.assertNotIn(module['three_layer_epistemic_trap']['layer_3_core_truth'],json.dumps(player,ensure_ascii=False))

    def test_player_search_does_not_match_hidden_truth_or_filters(self):
        hidden='银鱼波长'
        self.assertGreater(search(query=hidden)['matches'],0)
        self.assertEqual(search(query=hidden,audience='player')['matches'],0)
        with self.assertRaisesRegex(ValueError,'require --audience gm'):
            search(query='',book='血的诱惑',audience='player')

    def test_phase_limits_and_nonviolent_moves_survive_conversion(self):
        r=next(r for r in self.records if r['id']=='maxian_blood_link')
        b=convert(r,self.files)['bosses']
        self.assertEqual(b['card_id'],'yuanzhenxia_ma_xian')
        self.assertEqual(b['heat_threshold'],7)
        self.assertEqual(b['loaded_dice'],'d40+0')
        self.assertIsNone(b['active_moves'][1]['dice'])
        self.assertIsNone(b['canonical_weakness_counter']['unique_fatal_weakness'])
        self.assertEqual(b['deployment']['status'],'adaptation')
        self.assertIn('主动解咒之前',b['deployment']['phase'])

    def test_scenarios_keep_unknowns_and_eleven_private_assignments(self):
        for r in self.records:
            if 'scenario' not in r:continue
            s=convert(r,self.files)['scenarios']
            self.assertEqual(s['canonical']['mechanism_status'],r['canonical']['mechanism_status'])
            self.assertEqual(sum(x['slots'] for x in s['rule_adaptation']['assignments']),11)
            self.assertEqual(s['rule_adaptation']['status'],'adaptation')


if __name__=='__main__':unittest.main()
