"""Regression cases for tier boundaries and the forum's two-stage rating rules."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from build_character_kb import rating
RULES=json.loads((ROOT/'data/character_rules.json').read_text(encoding='utf-8'))

def card(scores=(0,0,0,0,0,0),theory='纸',concept=0,mastery='不适用'):
    return {'id':'test_role','name':'测试角色','version':{},'evidence':[],'uncertainties':[],
        'rating_input':{'positive':dict(zip(['physical','energy','scope','sustain','range','combat'],scores)),
        'positive_reasons':{},'negative':{'self_limit':{'score':0,'af':1,'reason':''},
        'environment':{'score':0,'af':1,'reason':''},'volatility':{'score':0,'reason':''}},
        'concept_level':concept,'concept_reason':'test','theoretical_tier':theory,'mastery':mastery,
        'ceiling':{'description':'test','tier':theory,'uncontrolled':'test'},'rating_confidence':'high'}}

class RatingTests(unittest.TestCase):
    def test_half_point_crosses_integer_band(self):
        r=rating(card((7,0,0,0,0,0),'并'),RULES)
        self.assertEqual((r['raw_score'],r['rounded_score'],r['practical_tier']),(10.5,11,'并'))

    def test_all_band_edges(self):
        cases=[(10,'纸'),(11,'并'),(25,'并'),(26,'强'),(33,'强'),(34,'凶'),
               (40,'凶'),(41,'狂'),(55,'狂'),(56,'准神'),(70,'准神'),
               (71,'神下'),(80,'神下'),(81,'神中'),(90,'神中'),(91,'神上'),(100,'神上')]
        for total,tier in cases:
            with self.subTest(total=total):
                r=rating(card((total/10,)*6,tier,2),RULES)
                self.assertEqual(r['numeric_tier'],tier)

    def test_concept_gate_caps_high_numeric_score(self):
        r=rating(card((10,)*6,'准神',0),RULES)
        self.assertEqual((r['numeric_tier'],r['practical_tier']),('神上','准神'))

    def test_accessibility_only_scales_first_two_deductions(self):
        c=card((3,)*6,'强')
        c['rating_input']['negative']={'self_limit':{'score':10,'af':0.2,'reason':'rare'},
             'environment':{'score':4,'af':0.5,'reason':'specific'},'volatility':{'score':3,'reason':'variable'}}
        self.assertEqual(rating(c,RULES)['raw_score'],23)

    def test_mastery_does_not_flatten_practical_record(self):
        expected={'稍有掌握':'并顶','基本掌握':'强','完全掌握':'狂',
                  '被动触发':'并（被动触发；按常态计）','不适用':'并'}
        for mastery,label in expected.items():
            r=rating(card((2,)*6,'狂',0,mastery),RULES)
            self.assertEqual(r['display_tier'],label)
            self.assertEqual(r['practical_tier'],'并')

    def test_inconsistent_theory_is_rejected(self):
        with self.assertRaises(ValueError):rating(card((4,)*6,'纸'),RULES)
        with self.assertRaises(ValueError):rating(card((2,)*6,'神下',0),RULES)

    def test_minimum_score_is_representable(self):
        c=card()
        for n in c['rating_input']['negative'].values():n['score']=10
        self.assertEqual(rating(c,RULES)['rounded_score'],-30)

if __name__=='__main__':unittest.main()
