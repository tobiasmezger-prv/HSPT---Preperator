"""Export the current bank and record the editorial comparison to public examples.
This is a bank-specific audit, not a universal automatic HSPT classifier.
"""
import json
from pathlib import Path
from collections import Counter
from bank_source import load_bank
from bank_pipeline import bank_hash, fingerprint
root=Path(__file__).resolve().parents[1]
bank=load_bank()
for q in bank:
 q.setdefault('section','quantitative');q.setdefault('reviewStatus','pending_human_review');q.setdefault('sourceType','original_draft')
sources={
 'STS':{'url':'https://www.ststesting.com/hp_int_sts.pdf','locator':'PDF page 5 / printed page 1, Description of the Subtests','role':'Official category definition; no public item difficulty calibration'},
 'TM':{'url':'https://www.testingmom.com/tests/high-school-placement-test-hspt-overview/hspt-practice-questions-by-subtest/hspt-quantitative-skills-practice-questions/','locator':'Public Quantitative sample items 1–4','role':'Third-party original examples; not released current exam questions'},
 'TV':{'url':'https://thetutorverse.com/hspt/','locator':'Quantitative Comparison, Number Series, and Word Problem sample headings','role':'Third-party original examples; note duplicated Roman numeral in webpage comparison stem'}
}
# Editorial assessment made against the sources, separate from arithmetic tests.
recommend={
 'quant-041':(2,'The rule is supplied; only two operations are required, so a hard label overstates the reasoning demand.'),
 'quant-055':(2,'Square a familiar fraction and compare four values; provisional medium is more defensible than hard.'),
 'quant-071':(2,'A standard one-part/three-part total problem; medium unless student timing suggests otherwise.'),
 'quant-074':(2,'One fraction multiplication after parsing the context; medium rather than hard.'),
 'quant-084':(2,'Two explicitly ordered machine steps do not demand difficult pattern discovery.'),
 'quant-086':(2,'Substitute the circle value and solve one simple equation; medium rather than hard.'),
 'quant-085':(1,'The digit-sum rule is supplied and requires only one addition.'),
 'quant-081':(1,'The row rule is supplied and the required operation is one addition.'),
 'quant-079':(1,'Direct substitution followed by multiplication and addition; a foundation item.'),
 'quant-078':(1,'A small perfect square plus a constant; foundation rather than medium.'),
}
items=[]
for q in bank:
 s=q['skill'];f=q['templateFamily'];risk=1;notes=[]
 if s.startswith('sequence_'):
  fmt='number_series';alignment='close';refs=['STS','TM','TV']
  notes=['Matches the concise four-choice continuation or missing-term format of public series examples.']
  if q['id'] in {'quant-025','quant-040','quant-041'}:
   alignment='partial';notes=['Explicit rule or nth-term prompt trains computation more than discovering the pattern; retain as foundation practice, not a full format match.'];risk=2
  if f in {'interleaved-arithmetic','three-step-cycle','alternating-geometric-branches','increasing-multipliers','three-halves-ratio'}:
   notes.append('Useful stretch reasoning; ask the sample reviewer to check the intended simplest rule and mental workload.');risk=3
 elif s=='numeric_comparison':
  fmt='geometric_comparison' if f.startswith('geometry-') else 'nongeometric_comparison';alignment='partial';refs=['STS','TM','TV'];risk=3
  notes=['Practices a relevant quantity comparison, but choices are values rather than relationships among labeled expressions.']
  if fmt=='geometric_comparison':notes=['Relevant geometric quantities, but text-only computation does not exercise reading and comparing figures. Add diagram-based relationship items before claiming section fidelity.'];risk=4
  if f in {'equivalent-percent','fraction-equivalence','ratio-comparison','fraction-gap'}:notes.append('Also functions as arithmetic/conversion practice; category label alone does not establish format fidelity.')
 elif s=='number_manipulation':
  fmt='number_manipulation';alignment='close';refs=['STS','TM','TV']
  notes=['Relevant verbal or arithmetic manipulation. Preserve compact wording and distractors for omitted or reversed steps.']
  if q['difficulty']==1:notes.append('Foundation-level warm-up; not evidence of exam-average difficulty.');risk=2
 else:
  fmt='supplemental_reasoning';alignment='supplemental';refs=['STS','TM','TV'];risk=3
  notes=['Related numerical reasoning, but this standalone format is not established as a core category by the consulted references. Keep as supplemental practice; do not use equal category quotas for an exam simulation.']
  if s=='symbolic_pattern':notes.append('Explicit symbol definitions make many items scaffolded arithmetic; consider concise verbal manipulation for an exam-style rewrite.')
 if q['id'] in recommend:notes.append(recommend[q['id']][1]);risk=max(risk,3)
 items.append({'id':q['id'],'questionHash':fingerprint(q),'format':fmt,'alignment':alignment,'risk':risk,'currentDifficulty':q['difficulty'],'recommendedDifficulty':recommend.get(q['id'],(q['difficulty'],''))[0],'difficultyBasis':'editorial, uncalibrated; public examples provide no item-level psychometric data','note':' '.join(notes),'referenceIds':refs,'disposition':'retain_for_skill_practice'})
audit={'bankHash':bank_hash(bank),'auditVersion':'public-example-calibration-v1','sources':sources,'scope':'Format and editorial demand comparison of all 100 items; not comparison to secure current exam items or empirical difficulty equating.','examSimulationReady':False,'items':items}
(root/'content/imports/current-100.json').write_text(json.dumps(bank,ensure_ascii=False,indent=2)+'\n')
(root/'content/calibration/current-100.audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
md=['# Calibration audit of all 100 questions','',
'**Gables follow-up:** The canonical [question-bank creation process](../../../QUESTION_BANK_CREATION_PROCESS.md), sections 2–3, supersedes the original reference policy below. It records Gables source pairings, the dev-03 and quant-038 overlap holds, and source-key exceptions. This export does not perform the new Gables novelty or visual checks.','',
'## Conclusion','',
'This bank is usable for foundational skill practice, but it is not yet a faithful full-section simulation. This review compared all 100 local items to the public examples below; it did not obtain or validate against secure current HSPT forms. Third-party practice examples are format references, not official difficulty norms.','',
'## Evidence and source quality','',
'- [STS interpretive manual](https://www.ststesting.com/hp_int_sts.pdf), printed page 1: publisher-defined scope includes series, manipulation, and geometric/nongeometric comparison. Official scope is authoritative; it does not give an item-level difficulty target for this bank.',
'- [TestingMom public samples](https://www.testingmom.com/tests/high-school-placement-test-hspt-overview/hspt-practice-questions-by-subtest/hspt-quantitative-skills-practice-questions/): inspected four prompts, including relational answer choices and a two-step percentage manipulation. The geometry item references figures; no claim is made here about inspecting the underlying image’s measurements.',
'- [Tutorverse public samples](https://thetutorverse.com/hspt/): inspected the series, labeled-quantity comparison, and verbal manipulation examples. The comparison stem has a duplicated Roman numeral on the webpage, illustrating why an online example is not an unquestionable answer-key authority.','',
'No questions or explanations were copied. Sources were used to compare structure, not to import their content. The linked answer-explanation PDF was discovered but not used as a question bank because it is not a complete set of question stems.','',
'## Findings','',
'| Dimension | Current bank | Assessment |',
'|---|---|---|',
'| Series | 34 | Strongest format match; 3 give a rule or ask for a position instead of simple pattern discovery. |',
'| Numerical comparison | 18, including 4 geometry items | Relevant skills, but no diagram items and no labeled-expression relationship choices. |',
'| Manipulation | 18 | Relevant; mix of warm-ups and multi-step work. Some read like ordinary mathematics exercises. |',
'| Symbolic / odd-one-out | 30 | Supplemental reasoning, not evidenced as standalone core categories by these sources. |',
'| Current difficulty labels | '+str(dict(sorted(Counter(q['difficulty'] for q in bank).items())))+' | Editorial labels, not measured HSPT difficulty. Ten specific ratings warrant a lower provisional level. |','',
'Our inference is that the bank is generally more scaffolded than an exam-style mix, not that every item is too easy. Simple sequences do appear in published examples. Genuine difficulty calibration requires observed student accuracy and time under comparable conditions; neither source supplies item statistics.','',
'## Recommended next revision (not silently applied)','',
'1. Introduce original comparison items with labeled quantities and relational answer choices, including actual geometric diagrams. Validate each relationship independently so exactly one choice is true.',
'2. Retain symbolic and classification exercises as supplemental practice. For a future exam-style pool, an editorial starting mix could be 34 series / 32 manipulation / 18 nongeometric comparison / 16 geometric comparison per 100. This is a proposed practice mix, not an official blueprint.',
'3. Revisit the ten flagged difficulty labels. Use easy = familiar one-step or explicit short rule; medium = infer a pattern or translate two steps; hard = genuinely combined or interleaved reasoning. Track observed performance later without inferring standardized scores.',
'4. Keep short questions, avoid teaching the intended rule in an inference question, and use distractors that correspond to plausible mistakes. Preserve original wording rather than paraphrasing online questions.',
'5. Human-review the fixed 20-item sample. Do not call the other 80 individually human-approved. No runtime question, key, or difficulty was changed by this audit.','',
'## Item-by-item audit','',
'| ID | Format match | Difficulty now → proposed | Assessment |',
'|---|---|---|---|']
for x in items:md.append(f"| {x['id']} | {x['alignment']} / {x['format']} | {x['currentDifficulty']} → {x['recommendedDifficulty']} | {x['note']} |")
(root/'content/calibration/CALIBRATION_REPORT.md').write_text('\n'.join(md)+'\n')
print('Audited 100 items:',dict(Counter(x['alignment'] for x in items)))
