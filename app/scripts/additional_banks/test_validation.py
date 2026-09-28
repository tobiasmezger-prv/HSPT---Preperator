import copy,json,tempfile,unittest
from pathlib import Path
from schema import load,validate,digest
from validate import math_check,evaluate,ROOT
from package_review import pick
class DraftValidationTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.banks,cls.passages=load(ROOT)
 def test_all_banks_are_100(self):
  self.assertEqual({s:len(b['questions']) for s,b in self.banks.items()},{s:100 for s in ['verbal','reading','mathematics','language']})
 def test_wrong_mathematical_key_rejected(self):
  q=copy.deepcopy(self.banks['mathematics']['questions'][0]);q['guide']['correctChoiceId']='ABCD'[('ABCD'.index(q['guide']['correctChoiceId'])+1)%4]
  with self.assertRaises(AssertionError):math_check(q)
 def test_equivalent_numeric_distractor_rejected(self):
  q=copy.deepcopy(self.banks['mathematics']['questions'][0]);k='ABCD'.index(q['guide']['correctChoiceId']);q['choices'][(k+1)%4]=q['choices'][k]+'.0'
  with self.assertRaises(AssertionError):math_check(q)
 def test_missing_passage_rejected(self):
  b=copy.deepcopy(self.banks['reading']);b['questions'][0]['passageId']='missing'
  with self.assertRaises(KeyError):validate(b,self.passages)
 def test_stale_passage_revision_rejected(self):
  b=copy.deepcopy(self.banks['reading']);b['questions'][0]['passageRevision']=99
  with self.assertRaises(AssertionError):validate(b,self.passages)
 def test_stale_manifest_checksum_rejected(self):
  with tempfile.TemporaryDirectory() as folder:
   path=Path(folder)
   for name in ['manifest.json','reading-passages.json','verbal.json','reading.json','mathematics.json','language.json']:(path/name).write_bytes((ROOT/name).read_bytes())
   with (path/'verbal.json').open('a') as out:out.write(' ')
   with self.assertRaises(AssertionError):load(path)
 def test_sample_repeatable_and_covered(self):
  for section,b in self.banks.items():
   qs=b['questions'];a=pick(qs,'fixed',section);z=pick(qs,'fixed',section)
   self.assertEqual(a,z);self.assertEqual(len(a),20)
   for field in ['skill','difficulty','format']:self.assertEqual({q[field] for q in a},{q[field] for q in qs})
   if section=='reading':self.assertEqual(len({q['passageId'] for q in a}),16)
 def test_capitalization_choices_remain_distinct(self):
  validate(self.banks['language'],self.passages)
 def test_expression_rejects_code(self):
  with self.assertRaises(ValueError):evaluate("__import__('os').system('echo unwanted')")
 def test_duplicate_ids_rejected(self):
  b=copy.deepcopy(self.banks['verbal']);b['questions'][1]['id']=b['questions'][0]['id']
  with self.assertRaises(AssertionError):validate(b,self.passages)
if __name__=='__main__':unittest.main()
