import json,hashlib,collections
from pathlib import Path
R=Path(__file__).resolve().parents[3];O=R/'app/content/staging/additional-v3'
read=lambda f:json.loads((O/f).read_text())
write=lambda f,d:(O/f).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
src=read('sources.json');coverage=read('source-coverage.json');val=read('validation.json');changes=read('changes.json')
sections={}
for s,(lo,hi) in {'verbal':(1,60),'quantitative':(61,112),'reading':(113,174),'mathematics':(175,238),'language':(239,298)}.items():
 records=[q for q in coverage['items'] if q['section']==s]
 sections[s]={'completeSourceRange':{'tests':[1,2,3],'questionNumbers':[lo,hi],'positions':len(records)},'references':[{'test':q['test'],'question':q['question'],'questionHeading':q['markdownQuestionHeading'],'guideHeading':q['markdownGuideHeading'],'exceptions':q['exceptions']} for q in records]}
sections['verbal'].update(design='25 synonyms, 25 antonyms, 20 analogies, 15 classifications, 15 logical reasoning. Closer distractors and diverse finite constraints; preserve analogy direction and word sense.',deliberateDeparture='Editorial practice-bank allocation rather than a claimed publisher weighting.')
sections['reading'].update(design='64 comprehension items in eight complete 8-item passage groups; 36 standalone vocabulary items. Literary fiction, technical explanation, argument, document comparison, archival exposition and quantitative exposition. Passage lengths 135–386 words.',calibration='Observed source ratio is 40 comprehension : 22 standalone vocabulary per 62-question section. 64:36 is a rounded 100-item equivalent. A 62-item form can use five complete groups plus 22 vocabulary items.',deliberateDeparture='Eight-item passage groups are an authoring choice; the 20-item human sample uses 16 comprehension plus 4 vocabulary to keep groups whole. Timing is unvalidated.')
sections['mathematics'].update(design='16 labeled SVG figure questions, 12 conceptual items, 72 retained numerical practice items. Original geometry, graphs, number line and spinner tasks.',deliberateDeparture='Sixteen figures and twelve conceptual items are editorial allocations, not counted source percentages.')
sections['language'].update(design='66 three-sentence error sets, 17 spelling and 17 composition questions. Sixteen error sets have a genuine No error key. No error stays in D; complete-bank key positions are balanced.',calibration='Source forms use 40 error sets, 10 spelling, 10 composition. 66:17:17 rounds that ratio to 100.',deliberateDeparture='The review sample overweights composition to cover eleven subtypes, while retaining all language skills and two No error cases.')
sections['quantitative'].update(design='No content change. Accepted live bank and prior human decisions preserved.',status='Included in full-source ledger and overlap checks, outside this four-bank revision.')
write('source-calibration.json',{'primaryMarkdown':src['primaryMarkdown'],'sourceSha256':src['markdownSha256'],'sourceCoverageFile':'source-coverage.json','method':'Prior full 894-position inspection reused after exact reconciliation of all 156 Markdown transcriptions and images to the six PDFs. Revised content reviewed against full-set findings and screened against the complete Markdown text; no website sample substituted.','sections':sections,'limits':['Third-party forms do not establish the current official STS blueprint.','Known errors and missing print remain exceptions.','Difficulty and timing remain editorial estimates.']})
(O/'PLAN.md').write_text('''# Additional question banks — revision 3 design record

Apply the root QUESTION_BANK_CREATION_PROCESS.md version 3.0. Preserve sources/ and prior drafts. This revision is staged for human review and does not authorize publication.

Scope: 100 Verbal, 100 Reading, 100 Mathematics and 100 Language questions. Quantitative remains unchanged. See source-calibration.json for full source ranges, locators, design choices and deliberate deviations.

Reading: 64 comprehension and 36 standalone vocabulary questions; eight original passages of eight questions each. Language: 66 error sets, 17 spelling and 17 composition questions. Mathematics: 16 original SVG figures and 12 conceptual questions within the 100. Verbal: five main families, closer alternatives and varied logical constraints.

All 400 questions receive structural and agent editorial checks. Mathematical and finite-logic checks are separate executable evidence. Prior evidence is reused only for unchanged semantic content. Source exceptions remain visible. Human review stays pending.

Review selection is checksum-bound and deterministic. Every skill, format and provisional level is represented. Reading preserves two entire passage groups. Mathematics includes at least five figures and three conceptual items. Language includes two genuine No error cases and all composition formats. These risk-oriented samples are not representative timed forms.

Open review/index.html or review/all-sections-80.html. Solve first, then open the separate answer guides. Record approve/revise/reject and notes; export decisions from the browser. Passing checks does not invent human approval.
''')
semantic=collections.Counter(x['id'][:3] for x in changes['items'] if x['semanticChange']);longest={s:val[s]['strictlyLongestCorrect'] for s in ['verbal','reading','mathematics','language']}
(O/'REPORT.md').write_text(f'''# Revised HSPT banks — ready for human review

Revision: additional-v3. Date: 2026-09-27. **400 staged questions checked; 80 human decisions pending.** No production bank, project source, deployment or past approval was changed.

## Delivered

- Four banks of 100 with keys, explanations and tips.
- Reading: 64 comprehension items, 36 standalone vocabulary items, eight original passages of 135–386 words. Complete-group 40+22 assembly is documented in validation.json.
- Language: 66 error sets (16 genuinely error-free), 17 spelling and 17 composition questions; eleven composition subtypes.
- Mathematics: 16 original accessible figures and 12 conceptual items; 88 numerical items total.
- Verbal: closer distractors, meaning distinctions, stronger classifications and varied logical constraints.
- [Combined 80-question review packet](review/all-sections-80.html), four 20-question packets, complete 100-question packets, and separate answer guides. Review decisions can be saved locally in the browser and exported.

All item revisions advanced because choice order and evidence were renewed. Semantic changes: {dict(semantic)}. Earlier versions and decisions remain preserved.

## Full source calibration

Primary file used: `{src['primaryMarkdown']}`. SHA-256: `{src['markdownSha256']}`.

The uploaded sources/ copy is not visible in this local mirror. The authorized identical generated fallback was used. All **156 text blocks and embedded page images** were reconciled to the six original PDFs, whose hashes match the prior full audit. Its **894 positions across every section** and 36 exception groups remain in the ledgers. This reuses a documented full review; missing source text is not marked verified and no new human source audit is claimed.

Full-set findings drive the revised formats. Complete Markdown text, including all guides, was screened for distinctive phrase overlap; fresh vocabulary/spelling targets and passages were checked. No unresolved automatic flags remain. Agent comparison identified no distinctive copied question or figure. Novelty and natural-language correctness remain editorial judgments, not universal proofs.

## Checks

- 400 complete records with distinct choices, correct key mapping, stable IDs, valid passage dependencies and diagram paths, and checksum-bound manifests.
- 25 A, B, C and D keys in each bank. Language preserves No error in D.
- 88 numerical items: exact evaluation of every choice. Sixteen new figures have separate calculations from givens. Retained content is reconciled with prior independent stem solutions; three previously revised numerical items were solved again separately.
- 12 conceptual math answers: reasoning and counterexamples, plus finite-domain checks where useful. Three new finite Verbal constraint problems have enumerated models; all remaining logical answers have recorded reasoning.
- Every revised Verbal, Reading and Language item: agent review of meanings, conventions, passage evidence, competing choices, explanations and tips. Every new passage and its dependent questions were reviewed together. This is separate from executable checks.
- Strictly-longest correct options: {longest}. Reading decreased from 57/100 in the original bank to {longest['reading']}/100. This indicator alone does not establish distractor quality.
- Exactly 20 reproducible review items per bank, covering all skills, formats and available levels. Reading uses two full passage groups plus four vocabulary questions. Language overrepresents composition to cover its new subtypes. Samples are not timed forms.

## Rendering and interface

All sixteen diagrams were visually inspected in browser galleries. Two crowded labels were corrected and checked again. SVG figures are embedded directly. Desktop layout and 390 px/820 px iframe layouts were inspected with no horizontal overflow. These are browser-size checks, not actual iPad/Safari certification.

Decision save/reload behavior was checked on an isolated test copy, never on the deliverable's human decisions. Export payload and regression results are recorded in delivery-checks.json. All deliverable decisions remain pending.

## Before release

1. Your 20-question review per revised bank and resolution of findings.
2. Actual iPad/Safari usability checks and student timing/difficulty evidence.
3. Versioned app integration and release checks after acceptance. The current app does not automatically ingest these staged formats.

The identified format gaps have been addressed. The result is original practice content under review, not an official or empirically equated exam.

## Evidence

See sources.json, source-coverage.json, source-exceptions.json, source-calibration.json, changes.json, item-audit.json, overlap-log.json, mathematics-checks.json, logic-checks.json, validation.json, visual-review.json, acceptance.json and review/*-sample.json.
''')
write('acceptance.json',{'batchId':'additional-v3','status':'pending_human_review','humanDecisionsRequired':80,'humanDecisionsReceived':0,'releaseReady':False,'deviceReview':'actual_iPad_Safari_pending','integration':'not_performed','deployment':'not_performed'})
write('visual-review.json',{'manifestSha256':hashlib.sha256((O/'manifest.json').read_bytes()).hexdigest(),'figures':[{'id':f'mat-a1-{n:03}','status':'agent_browser_visual_check_passed','checks':['labels legible','geometry consistent with marked givens','no solution revealed','accessible description supplied']} for n in range(56,72)],'fixes':['Moved cube-net side label clear of the net.','Shortened tank water-level label to avoid edge collision.','Aligned transversal slope with the marked angles before final inspection.'],'responsiveChecks':[{'width':390,'scrollWidth':390},{'width':820,'scrollWidth':820}],'method':'Browser figure galleries and final packet. Same-origin iframe widths used because viewport override did not take effect.','actualDeviceCheck':'pending','humanReview':'pending'})
print('Reports written; semantic changes:',dict(semantic))
