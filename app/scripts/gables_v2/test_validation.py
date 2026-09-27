import unittest,json,copy
from pathlib import Path
from validate import check,OUT
class Checks(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.bank=json.loads((OUT/'bank.json').read_text());cls.proofs=json.loads((OUT/'proofs.json').read_text())
 def test_all_100(self):
  for q in self.bank:
   with self.subTest(id=q['id']):check(q,self.proofs[q['id']])
 def test_wrong_key_rejected_for_every_item(self):
  for source in self.bank:
   q=copy.deepcopy(source);q['guide']['correctChoiceId']='ABCD'[('ABCD'.index(q['guide']['correctChoiceId'])+1)%4]
   with self.subTest(id=q['id']),self.assertRaises(AssertionError):check(q,self.proofs[q['id']])
 def test_wrong_earlier_sequence_term_rejected(self):
  q=self.bank[2];p=copy.deepcopy(self.proofs[q['id']]);p['terms'][2]=25
  with self.assertRaises(AssertionError):check(q,p)
 def test_wrong_second_output_rejected(self):
  q=copy.deepcopy(self.bank[2]);i='ABCD'.index(q['guide']['correctChoiceId']);q['choices'][i]='231, 229'
  with self.assertRaises(AssertionError):check(q,self.proofs[q['id']])
 def test_equivalent_numeric_options_rejected(self):
  q=copy.deepcopy(self.bank[86]);i='ABCD'.index(q['guide']['correctChoiceId']);q['choices'][(i+1)%4]='2/6'
  with self.assertRaises(AssertionError):check(q,self.proofs[q['id']])
 def test_diagram_tamper_rejected(self):
  for i in [84,88,92,96]:
   q=copy.deepcopy(self.bank[i]);v=q['visual']
   if v['type']=='grids':v['panels'][0]['shaded'].append(1)
   elif v['type']=='bars':v['values'][0]+=1
   elif v['type']=='rectangles':v['panels'][0]['width']+=1
   else:v['known']+=1
   with self.subTest(id=q['id']),self.assertRaises(AssertionError):check(q,self.proofs[q['id']])
if __name__=='__main__':unittest.main()
