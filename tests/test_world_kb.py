"""Meaningful failure cases for temporal state and source-integrity boundaries."""
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS=Path(__file__).resolve().parents[1]/'tools'
sys.path.insert(0,str(TOOLS))
from build_world_kb import ancestors, book_id, digest, topological_order, validate_evidence, verify_sources
from query_world import resolve_character, scene_package


def relation(a,b,kind='before',status='textual_fact'):
    return {'id':a+'_'+b,'source':a,'target':b,'relation':kind,'epistemic_status':status}


class WorldKnowledgeTests(unittest.TestCase):
    def test_partial_order_does_not_invent_connections(self):
        events=['past','revelation','future','independent']
        relations=[relation('past','revelation'),relation('revelation','future')]
        self.assertEqual(ancestors(['revelation'],events,relations),{'past','revelation'})
        self.assertNotIn('independent',ancestors(['future'],events,relations))

    def test_revelation_and_inference_are_not_strict_chronology(self):
        events=['ancient','claim','inferred','now']
        rs=[relation('ancient','claim','revealed_by'),relation('claim','now'),relation('inferred','now',status='synthesis')]
        self.assertEqual(ancestors(['now'],events,rs),{'claim','now'})
        self.assertEqual(ancestors(['now'],events,rs,True),{'claim','now','inferred'})

    def test_cycles_unknown_endpoints_and_unknown_scenes_rejected(self):
        with self.assertRaisesRegex(ValueError,'cycle'):
            topological_order(['a','b'],[relation('a','b'),relation('b','a')])
        with self.assertRaisesRegex(ValueError,'Unknown relation'):
            topological_order(['a'],[relation('a','b')])
        with self.assertRaisesRegex(ValueError,'Unknown event'):
            ancestors(['missing'],['a'],[])

    def test_scene_cannot_load_future_form_or_terminal_card(self):
        def event(i,state):
            return {'id':i,'character_ids':['eagle'],'state_after':state,'knowledge_boundary':'GM must assign knowledge'}
        timeline={'events':[event('bird','can fly'),event('human','cannot fly'),event('gone','left with companion')],
                  'relations':[relation('bird','human'),relation('human','gone')]}
        arcs=[{'character_id':'eagle','stages':[
            {'label':i,'event_ids':[i],'state':s,'rp_constraint':s} for i,s in [('bird','bird body'),('human','human body'),('gone','departed')]]}]
        result=scene_package(['human'],timeline,arcs,{'eagle':'鹰'})
        self.assertEqual(result['completed_event_ids'],['bird','human'])
        state=result['character_states'][0]
        self.assertEqual(state['frontier_event_ids'],['human'])
        self.assertEqual(state['state_updates'][0]['state_after'],'cannot fly')
        self.assertEqual([s['label'] for s in state['confirmed_history_stages']],['bird','human'])
        self.assertFalse(result['terminal_character_cards_loaded'])
        self.assertFalse(result['terminal_entity_states_loaded'])
        self.assertEqual(state['knowledge_assignment']['knows'],[])

    def test_incomparable_character_states_are_not_silently_overwritten(self):
        events=[{'id':i,'character_ids':['person'],'state_after':i,'knowledge_boundary':'unknown'} for i in ['a','b']]
        result=scene_package(['a','b'],{'events':events,'relations':[]},[],{'person':'人'})
        self.assertEqual(result['character_states'][0]['frontier_event_ids'],['a','b'])
        self.assertTrue(result['character_states'][0]['incomparable_frontiers'])

    def test_names_resolve_ambiguity_and_redirect(self):
        index={'characters':[{'id':'a','name':'同名','aliases':[]},{'id':'b','name':'同名','aliases':['称号']}],
               'id_redirects':{'old':'b'}}
        self.assertEqual(len(resolve_character('同名',index)),2)
        self.assertEqual(resolve_character('old',index)[0]['id'],'b')

    def test_line_ranges_and_source_hash_reject_drift(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            source=root/'01正文.txt'
            source.write_bytes('第一行\n第二行\n'.encode('utf-8'))
            f={'path':source.name,'sha256':digest(source.read_bytes()),'lines':2}
            catalog={'files':[f]}
            verify_sources(catalog,root)
            valid={'path':source.name,'start_line':1,'end_line':2,'supports':'注释'}
            validate_evidence(valid,{source.name:f})
            with self.assertRaisesRegex(ValueError,'range'):
                validate_evidence({**valid,'end_line':3},{source.name:f})
            source.write_bytes('修改正文\n第二行\n'.encode('utf-8'))
            with self.assertRaisesRegex(ValueError,'hash changed'):
                verify_sources(catalog,root)

    def test_duplicate_book_numbers_do_not_collide(self):
        self.assertNotEqual(book_id('卫斯理系列/002地底奇人.txt'),book_id('卫斯理系列/002卫斯理与白素.txt'))
        self.assertEqual(book_id('卫斯理系列/002地底奇人.txt'),book_id('卫斯理系列/002地底奇人.txt'))


if __name__=='__main__': unittest.main()
