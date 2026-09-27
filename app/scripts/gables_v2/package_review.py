"""Deterministic format/risk-stratified sample and portable review packet."""
import json,hashlib,html,collections,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];STAGE=ROOT/'content/staging/gables-v2';OUT=ROOT/'content/review/gables-v2';OUT.mkdir(exist_ok=True,parents=True)
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
bank=json.loads((STAGE/'bank.json').read_text());byid={q['id']:q for q in bank};digest=H(STAGE/'bank.json')
editorial=json.loads((STAGE/'editorial-review.json').read_text())
assert editorial['reviewedBankSha256']==digest, 'Content changed: repeat editorial/source review and record new evidence first.'
visual_review=json.loads((STAGE/'visual-review.json').read_text())
assert visual_review['bankSha256']==digest
assert all(H(STAGE/'assets'/name)==sha for name,sha in visual_review['assets'].items()), 'Diagrams changed: repeat visual inspection.'
refs={
'number_series':['Test 1 Q61, 68, 71, 83, 94, 97, 105; question PDF pp6–10; paired guide pp5–8','Test 2 Q62–63, 69, 71–72, 76, 79, 81, 86, 89–90, 93, 95, 99, 101, 104, 106, 108; question PDF pp6–10; guide pp3–6','Test 3 Q62, 65, 69–70, 75, 77, 80, 84, 91, 93, 97, 100–101, 105, 107; question PDF pp6–11; guide pp5–8'],
'number_manipulation':['Test 1 Q62–63, 66, 69–70, 74, 78, 81, 84–85, 90, 93, 96, 102–103, 108–109, 112; question PDF pp6–11; guide pp5–8','Test 2 Q61, 66–67, 73–74, 80, 83, 85, 88, 92, 97, 100, 103, 107, 109, 111–112; question PDF pp6–11; guide pp3–6','Test 3 Q61, 64, 67–68, 71, 73, 78, 81, 83, 86, 90, 94–95, 102, 104, 108–109, 111; question PDF pp6–11; guide pp5–8'],
'nongeometric_comparison':['Test 1 Q72–73, 77, 86, 89, 95, 99, 104, 110; question PDF pp7–11; guide pp5–8','Test 2 Q65, 70, 75, 82, 87, 94, 98, 105; question PDF pp6–10; guide pp3–6','Test 3 Q63, 74, 76, 85, 88, 96, 98, 103, 110; question PDF pp6–11; guide pp5–8'],
'geometric_comparison':['Test 1 Q64, 67, 79, 82, 92, 98, 106, 111; question PDF pp6–11; guide pp5–8','Test 2 Q64, 68, 77–78, 84, 91, 96, 102, 110; question PDF pp6–11; guide pp3–6','Test 3 Q66, 72, 79, 82, 92, 99, 106, 112; question PDF pp6–11; guide pp5–8']}
briefs={'number_series':'Infer changes or interleaved rules; use all supplied terms. Missing terms, pairs and letter-number outputs broaden the prior next-number-only bank.', 'number_manipulation':'Translate concise verbal arithmetic; preserve the requested order and finish all operations. Foundation computations retained; contextual variants extend rather than reproduce source stems.', 'nongeometric_comparison':'Evaluate labeled quantities and choose one true relationship; use fractions, decimals, powers, order of operations and signs.', 'geometric_comparison':'Read original equal-cell grids, scaled bars, dimensioned rectangles or marked angles. These are editorial extensions of visual reasoning, not reproductions of the reference geometry.'}
audit=[]
changes=json.loads((STAGE/'changes.json').read_text())
for q,c in zip(bank,changes):
 audit.append({'id':q['id'],'format':q['format'],'difficulty':q['difficulty'],'skillBrief':briefs[q['format']],'referenceScope':refs[q['format']],'priorBank':c,'novelty':{'method':'agent-assisted comparison with all three quantitative source sections and existing 100; arithmetic similarities are not automatically substantive matches','finding':'no additional substantive match identified; common skill/format overlap retained','visual':'new programmatic geometry, labels and shading' if 'visual' in q else 'not applicable'},'editorialCheck':'stem, key, worked explanation and tip reviewed; difficulty provisional','sequenceCheck':'intended rule fits all terms; checked constant differences/ratios, changing gaps and alternating branches where applicable; no equally natural different offered answer identified' if q['format']=='number_series' else 'not applicable'})
(STAGE/'item-audit.json').write_text(json.dumps({'bankSha256':digest,'checker':'Codex agent-assisted editorial review','items':audit},indent=2)+'\n')
sourcebase='https://gablestutoring.com/wp-content/uploads/2020/08/'
sources=[]
for n,qf,af,title,qp,ap in [(1,'HSPT-Test-3.pdf','HSPT-TEST-3-Answers.pdf','Catholic High School Entrance Exams For Dummies, printed Practice Test 1','188–193','221–224'),(2,'HSPT-TEST-4-1.pdf','HSPT-TEST-4-Answers.pdf','Peterson’s, printed Practice Test 5','448–453','476–479'),(3,'HSPT-TEST-5.pdf','HSPT-TEST-5-Answers.pdf','Catholic High School Entrance Exams For Dummies, printed Practice Test 2','246–251','279–282')]:
 sources.append({'webLabel':f'Test {n}','title':title,'questionUrl':sourcebase+qf,'answerUrl':sourcebase+af,'scope':'Quantitative Q61–112','questionPrintedPages':qp,'answerPrintedPages':ap,'accessDate':'2026-09-26','questionPdfSha256':H(Path(f'/tmp/hspt-gables/test{n}.pdf')),'answerPdfSha256':H(Path(f'/tmp/hspt-gables/answers{n}.pdf'))})
(STAGE/'sources.json').write_text(json.dumps({'page':'https://gablestutoring.com/practice-tests/','sources':sources,'exceptions':['Test 3 Q87: independently identified question/guide disagreement; excluded as correctness template.','Test 3 Q89: numerically equal choices; avoid representation-dependent ambiguity.'],'inspection':'Quantitative question sections and paired answer explanations, including scanned pages and relevant figures. Not a certification of reference answer keys.'},indent=2)+'\n')
(STAGE/'overlap-log.json').write_text(json.dumps({'bankSha256':digest,'resolved':[{'oldId':'dev-03','source':'Test 1 Q68','newId':'gb2-003','resolution':'Replace doubling prefix with alternating multiplication/decrement and two requested outputs.'},{'oldId':'quant-038','source':'Test 3 Q75','newId':'gb2-030','resolution':'Replace fractional progression with independently interleaved decreasing and increasing branches.'}],'scope':'All 100 compared editorially with all three source sections. Generic arithmetic and conventional sequence families remain shared. No exhaustive semantic-plagiarism guarantee.','unresolvedIdentifiedMatches':[]},indent=2)+'\n')
# Prespecified high-risk picks, plus deterministic within-format selection.
forced={'number_series':['gb2-003','gb2-017','gb2-030','gb2-032'],'number_manipulation':['gb2-056','gb2-062'],'nongeometric_comparison':['gb2-079'],'geometric_comparison':['gb2-085','gb2-092','gb2-093','gb2-100']}
quotas={'number_series':6,'number_manipulation':6,'nongeometric_comparison':4,'geometric_comparison':4}
selected=[];reasons={}
for fmt,quota in quotas.items():
 picks=list(forced[fmt]);reasons.update({i:'Prespecified format/risk coverage' for i in picks})
 candidates=sorted([q for q in bank if q['format']==fmt and q['id'] not in picks],key=lambda q:hashlib.sha256(('gables-v2-sample-policy-1|'+digest+'|'+q['id']).encode()).hexdigest())
 # Ensure each format represented includes foundation if the format has it and capacity remains.
 if len(picks)<quota and not any(byid[i]['difficulty']==1 for i in picks):
  foundation=next((q for q in candidates if q['difficulty']==1),None)
  if foundation:picks.append(foundation['id']);reasons[foundation['id']]='Foundation difficulty coverage'
 for q in candidates:
  if len(picks)==quota:break
  if q['id'] not in picks:picks.append(q['id']);reasons[q['id']]='Content-hash-seeded selection within format'
 selected.extend(picks)
selected.sort();sample=[byid[i] for i in selected]
assert len(sample)==20 and len(set(selected))==20
assert {q['difficulty'] for q in sample}=={1,2,3}
assert {q['answerFormat'] for q in sample}=={q['answerFormat'] for q in bank}
assert {q['visual']['type'] for q in sample if 'visual'in q}=={'grids','bars','rectangles','angles'}
assert len({q['templateFamily'] for q in sample})==20
manifest={'policy':'gables-v2-sample-policy-1','bankSha256':digest,'auditSha256':H(STAGE/'item-audit.json'),'mathSha256':H(STAGE/'validation.json'),'editorialSha256':H(STAGE/'editorial-review.json'),'visualSha256':H(STAGE/'visual-review.json'),'quotas':quotas,'forced':forced,'sample':[{'number':n,'id':q['id'],'reason':reasons[q['id']],'difficulty':q['difficulty'],'answerFormat':q['answerFormat'],'visual':q.get('visual',{}).get('type')} for n,q in enumerate(sample,1)]}
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
decisions={'bankSha256':digest,'manifestSha256':H(OUT/'manifest.json'),'reviewer':None,'date':None,'items':[{'id':q['id'],'decision':'pending','notes':''} for q in sample]}
if (OUT/'decisions.json').exists():
 existing=json.loads((OUT/'decisions.json').read_text());assert existing['bankSha256']==digest and existing['manifestSha256']==decisions['manifestSha256'],'Review evidence changed: archive or use a new revision.'
 decisions=existing
(OUT/'decisions.json').write_text(json.dumps(decisions,indent=2)+'\n')
e=html.escape
intro='Review draft • Gables-calibrated revision • 20 of 100 questions'
body=[f'<h1>HSPT quantitative review</h1><p class="lead">{intro}</p><p>Solve the questions first, then open the answer key below. For each item, check clarity, one defensible answer, difficulty, explanation, tip, and diagram where present. Reply with the question number and approve / revise / reject, plus any notes. This is a review sample, not a scored full test.</p><p>Mix: 6 sequences · 6 manipulations · 4 numerical comparisons · 4 visual questions. Difficulty labels are provisional.</p><a href="#answers">Go to answers and explanations</a>']
md=['# HSPT quantitative review — updated 20','',intro,'','Solve first; the separate answer section follows all 20 questions. Review each for correctness, clarity, uniqueness, difficulty, explanation, tip, and diagram. Reply with question number: approve / revise / reject and notes.','']
for n,q in enumerate(sample,1):
 body.append(f'<article><h2>{n}. <small>{q["id"]}</small></h2><p class="stem">{e(q["stem"])}</p>');md += [f'## {n}. {q["id"]}','',q['stem'],'']
 if 'visual'in q:
  svg=(STAGE/'assets'/f'{q["id"]}.svg').read_text();body.append(svg);md += [f'![{q["visual"]["alt"]}](assets/{q["id"]}.svg)',''];(OUT/'assets').mkdir(exist_ok=True);(OUT/'assets'/f'{q["id"]}.svg').write_text(svg)
 body.append('<ol type="A">'+''.join(f'<li>{e(c)}</li>' for c in q['choices'])+'</ol><p class="review">Your answer: ____ &nbsp; Approve / Revise / Reject &nbsp; Notes: ____________________</p></article>');md += [f'{letter}. {c}' for letter,c in zip('ABCD',q['choices'])]+['','Your answer: ____ · Approve / Revise / Reject · Notes:','']
body.append('<section id="answers"><h1>Answers, steps, and tips</h1><p>Use this section after solving. An approval should include the explanation and tip, not just the answer.</p>');md += ['---','','# Answers, steps, and tips','']
for n,q in enumerate(sample,1):
 g=q['guide'];choice=q['choices']['ABCD'.index(g['correctChoiceId'])];d={1:'Foundation',2:'Intermediate',3:'Stretch'}[q['difficulty']]
 body.append(f'<article><h2>{n}. {g["correctChoiceId"]} — {e(choice)}</h2><p><small>{q["id"]} · {d}</small></p><p>{e(g["explanation"])}</p><p><strong>Tip:</strong> {e(g["shortcut"])}</p></article>');md += [f'## {n}. {g["correctChoiceId"]} — {choice}','',f'{q["id"]} · {d}','',g['explanation'],'',f'**Tip:** {g["shortcut"]}','']
body.append(f'</section><footer>Batch gables-v2 · SHA-256 {digest}<br>Pending human review. Not deployed. References were used for calibration only.</footer>')
style='body{font-family:Arial,sans-serif;color:#172b40;max-width:760px;margin:40px auto;padding:0 24px;line-height:1.6}h1{line-height:1.2}h2{font-size:22px}small,.review,footer{color:#526277;font-size:14px}.lead{font-size:18px}.stem{white-space:pre-line;font-size:19px}article{border-top:1px solid #cbd5e1;padding:18px 0;break-inside:avoid}li{padding:5px 8px;font-size:18px}svg{width:100%;max-width:600px;height:auto;display:block;margin:16px auto}#answers{margin-top:100px;break-before:page}footer{overflow-wrap:anywhere;margin-top:50px}@media print{body{margin:0;max-width:none}a{display:none}.review{margin-top:20px}article{padding:12px 0}}'
(OUT/'REVIEW_20.html').write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Updated 20-question HSPT review</title><style>'+style+'</style></head><body>'+''.join(body)+'</body></html>')
(OUT/'REVIEW_20.md').write_text('\n'.join(md)+'\n')
formats=collections.Counter(q['format'] for q in bank);diff=collections.Counter(q['difficulty'] for q in bank);keys=collections.Counter(q['guide']['correctChoiceId'] for q in bank)
retained=sum(c['action']=='retained/rechecked' for c in changes)
report=f'''# Gables revision — first 100

Status: **content checks complete; human sample pending; app integration/release pending**.

- {retained} prior items retained and rechecked; {100-retained} replacement/new items. Stable new revision IDs preserve the old bank.
- Mix: {dict(formats)}.
- Provisional difficulty: {dict(diff)} (1 foundation, 2 intermediate, 3 stretch).
- Answer letters: {dict(keys)}; shuffled deterministically, not a repeating ABCD cycle.
- All 100 independently checked using exact fractions, all-choice evaluation, full sequence-term checks, relational truth tables and diagram-data assertions. Explanations/tips received an agent editorial pass.
- All three Gables quantitative sections and matching explanations used as format calibration; see sources.json and item-audit.json. This allocation is editorial, not official weighting or a counted source blueprint. Difficulty is not psychometrically calibrated.
- Two known source overlaps replaced (overlap-log.json). Common arithmetic and conventional patterns are retained; no further substantive matches identified by agent-assisted review. This is not automated semantic-plagiarism certification.
- All 16 original diagrams rendered and visually inspected on two contact sheets. Grid counts, bar scales, dimensions, angle labels and accessible descriptions checked. This is static asset QA, not iPad app QA.
- Fixed sample: 6 series, 6 manipulation, 4 numerical comparison, 4 visual. It covers all three difficulty levels, all answer formats, four visual types, distinct families and both known-overlap replacements.
- The app's live content has not changed. The app does not yet render these declarative diagrams. Integration, ten-question selection across the revised format mix, live scoring/rendering checks and iPad verification are release gates after review. Thus this batch is not release-ready.

## Evidence

Bank SHA-256: `{digest}`.

See validation.json, item-audit.json, overlap-log.json, sources.json, assets/contact-1.png and assets/contact-2.png. The review directory contains the portable HTML, Markdown plus assets, reproducible manifest and blank decisions. No human approval has been inferred.

## Review and acceptance

Review all 20. Return approve/revise/reject with notes by packet number or item ID. Any wrong answer, ambiguity, invalid tip, rendering defect or substantive source overlap blocks acceptance and triggers inspection of the whole affected family. Do not mark the other 80 individually human-approved. Final batch acceptance also requires the integration gates above.
'''
(STAGE/'REPORT.md').write_text(report)
with zipfile.ZipFile(OUT/'HSPT_REVIEW_20.zip','w',zipfile.ZIP_DEFLATED) as z:
 for path in [OUT/'REVIEW_20.html',OUT/'REVIEW_20.md',OUT/'manifest.json',OUT/'decisions.json',*sorted((OUT/'assets').glob('*.svg'))]:z.write(path,path.relative_to(OUT))
print('Review sample:',', '.join(selected));print('Retained:',retained,'New/replaced:',100-retained)
