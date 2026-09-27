import copy,json,tempfile,unittest
from pathlib import Path
from bank_pipeline import bank_hash,fingerprint,validate,sample,gate,write_packet,VERSION
ROOT=Path(__file__).resolve().parents[1]
class PipelineTests(unittest.TestCase):
 def setUp(self):
  self.bank=json.loads((ROOT/'content/imports/current-100.json').read_text())
  self.audit=json.loads((ROOT/'content/calibration/current-100.audit.json').read_text())
  self.evidence={'bankHash':bank_hash(self.bank),'status':'passed','checkedIds':[q['id'] for q in self.bank]}
 def decisions(self):
  selected,_=sample(self.bank,self.audit['items'])
  return {'policyVersion':VERSION,'bankHash':bank_hash(self.bank),'reviewer':'Test reviewer','reviewedAt':'2026-09-26','calibrationAcknowledged':True,'items':[{'id':q['id'],'questionHash':fingerprint(q),'decision':'approve'} for q in selected]}
 def test_fixed_twenty_and_coverage(self):
  chosen,_=sample(self.bank,self.audit['items'])
  self.assertEqual(len(chosen),20);self.assertEqual(len({q['id'] for q in chosen}),20)
  self.assertEqual(len({q['skill'] for q in chosen}),6);self.assertEqual({q['difficulty'] for q in chosen},{1,2,3})
  self.assertTrue(any(q['templateFamily'].startswith('geometry-') for q in chosen))
 def test_reorder_does_not_change_sample(self):
  self.assertEqual(sample(self.bank,self.audit['items']),sample(list(reversed(self.bank)),self.audit['items']))
 def test_schema_duplicate_and_missing_guide(self):
  self.assertEqual(validate(self.bank),[])
  broken=copy.deepcopy(self.bank);broken[1]=broken[0];self.assertTrue(validate(broken))
  broken=copy.deepcopy(self.bank);del broken[0]['guide'];self.assertTrue(validate(broken))
  self.assertTrue(validate(self.bank[:-1]))
 def test_pending_until_twenty_real_decisions(self):
  self.assertEqual(gate(self.bank,self.evidence,self.audit)[0],'pending_sample_review')
  decision=self.decisions();self.assertEqual(gate(self.bank,self.evidence,self.audit,decision)[0],'sample_reviewed_for_skill_practice')
  decision['items'][0]['decision']='revise';self.assertEqual(gate(self.bank,self.evidence,self.audit,decision)[0],'blocked')
 def test_stale_or_incomplete_checks_block(self):
  changed=copy.deepcopy(self.bank);changed[0]['guide']['shortcut']+=' Edit.'
  self.assertEqual(gate(changed,self.evidence,self.audit,self.decisions())[0],'blocked')
  self.evidence['checkedIds'].pop();self.assertEqual(gate(self.bank,self.evidence,self.audit)[0],'blocked')
 def test_rejected_item_blocks_even_before_human_review(self):
  self.audit['items'][0]['disposition']='reject';self.assertEqual(gate(self.bank,self.evidence,self.audit)[0],'blocked')
 def test_decisions_not_overwritten(self):
  with tempfile.TemporaryDirectory() as folder:
   write_packet(self.bank,self.audit,self.evidence,folder)
   target=Path(folder)/'decisions.json';target.write_text('{"human":"work in progress"}')
   write_packet(self.bank,self.audit,self.evidence,folder)
   self.assertEqual(json.loads(target.read_text()),{'human':'work in progress'})
 def test_two_hundreds_produce_forty(self):
  bank=copy.deepcopy(self.bank);audit=copy.deepcopy(self.audit)
  for q in self.bank:
   new=copy.deepcopy(q);new['id']='second-'+q['id'];new['stem']='Second batch: '+q['stem'];bank.append(new)
   old=next(r for r in self.audit['items'] if r['id']==q['id']);r={**old,'id':new['id'],'questionHash':fingerprint(new)};audit['items'].append(r)
  self.assertEqual(validate(bank),[])
  with tempfile.TemporaryDirectory() as folder:self.assertEqual(len(write_packet(bank,audit,self.evidence,folder)['sampleIds']),40)
if __name__=='__main__':unittest.main()
