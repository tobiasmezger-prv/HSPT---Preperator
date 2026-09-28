import unittest,copy,json,sys,contextlib,io,tempfile,shutil
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'additional_banks'))
from schema import validate,load
from validate import math_check
with contextlib.redirect_stdout(io.StringIO()):import package
R=package.OUT
class RevisionTests(unittest.TestCase):
 def test_all_sections_load_with_checksums(self):
  b,p=load(R);self.assertEqual({s:len(x['questions']) for s,x in b.items()},{s:100 for s in package.banks});self.assertEqual(len(p),8)
 def test_sample_repeatable_and_order_independent(self):
  for s,b in package.banks.items():
   a,am=package.sample(s,b['questions']);z,zm=package.sample(s,list(reversed(b['questions'])))
   self.assertEqual(a,z);self.assertEqual(am,zm);self.assertEqual(len(a),20)
 def test_reading_groups_whole_and_standalone(self):
  qs,_=package.sample('reading',package.banks['reading']['questions'])
  from collections import Counter
  counts=Counter(q.get('passageId') for q in qs)
  self.assertEqual(counts.pop(None),4);self.assertEqual(sorted(counts.values()),[8,8])
 def test_every_format_skill_and_level_sampled(self):
  for s,b in package.banks.items():
   qs,_=package.sample(s,b['questions'])
   for field in ['format','skill','difficulty']:self.assertEqual({q[field] for q in qs},{q[field] for q in b['questions']})
 def test_math_has_new_formats_in_sample(self):
  qs,_=package.sample('mathematics',package.banks['mathematics']['questions'])
  self.assertGreaterEqual(sum(bool(q.get('diagram')) for q in qs),5)
  self.assertGreaterEqual(sum(q['format']=='conceptual' for q in qs),3)
 def test_error_sets_keep_no_error_last(self):
  for q in package.banks['language']['questions'][:66]:self.assertEqual(q['choices'][3],'No error.')
  qs,_=package.sample('language',package.banks['language']['questions']);self.assertEqual(sum(q.get('noErrorCorrect',False) for q in qs),2)
 def test_missing_standalone_target_rejected(self):
  b=copy.deepcopy(package.banks['reading']);del b['questions'][64]['targetWord']
  with self.assertRaises(AssertionError):validate(b,package.passages)
 def test_stale_passage_revision_rejected(self):
  b=copy.deepcopy(package.banks['reading']);b['questions'][0]['passageRevision']=99
  with self.assertRaises(AssertionError):validate(b,package.passages)
 def test_wrong_figure_key_rejected(self):
  q=copy.deepcopy(package.banks['mathematics']['questions'][55]);q['guide']['correctChoiceId']='ABCD'[('ABCD'.index(q['guide']['correctChoiceId'])+1)%4]
  with self.assertRaises(AssertionError):math_check(q)
 def test_figure_asset_change_invalidates_sample_hash(self):
  section='mathematics';qs=package.banks[section]['questions'];_,before=package.sample(section,qs)
  with tempfile.TemporaryDirectory() as d:
   dest=Path(d);shutil.copy(R/'mathematics.json',dest/'mathematics.json');shutil.copytree(R/'assets',dest/'assets')
   asset=dest/qs[55]['diagram']['file'];asset.write_text(asset.read_text()+'\n')
   old=package.OUT
   try:
    package.OUT=dest;_,after=package.sample(section,qs)
   finally:package.OUT=old
  self.assertNotEqual(before['seed'],after['seed'])
 def test_packets_have_inline_figures_and_separate_answers(self):
  text=(R/'review/all-sections-80.html').read_text()
  self.assertEqual(text.count('data-decision='),80)
  self.assertNotIn('<script src=',text);self.assertNotIn('<img src="http',text)
  self.assertGreaterEqual(text.count('<svg '),5)
  self.assertGreater(text.index('<details class="answers"'),text.index('id="language"'))
 def test_every_source_position_accounted_for(self):
  d=json.loads((R/'source-coverage.json').read_text());self.assertEqual(len(d['pageRecords']),156)
  self.assertEqual({(q['test'],q['question']) for q in d['items']},{(t,n) for t in [1,2,3] for n in range(1,299)})
 def test_human_decisions_are_pending(self):
  for s in package.banks:
   d=json.loads((R/f'review/{s}-decisions.json').read_text());self.assertEqual(len(d['decisions']),20)
   self.assertTrue(all(x['decision']=='pending' for x in d['decisions']))
if __name__=='__main__':unittest.main()
