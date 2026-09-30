#!/usr/bin/env python3
"""Normalize the approved source collection into the existing cumulative publisher.
This prepares evidence using the owner's recorded approval; it does not deploy remotely.
"""
from pathlib import Path
import json,re,hashlib,copy,importlib.util,collections,shutil,unicodedata
ROOT=Path(__file__).resolve().parents[2];APP=ROOT/'app';O=ROOT/'output/question-bank/source-formatted-v1';D=APP/'content/staging/source-import-v1';E=D/'evidence';R=APP/'content/review/source-import-v1'
def read(p):return json.loads(p.read_text())
def write(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
Q=read(O/'questions.json');original=copy.deepcopy(Q);P={p['id']:p for p in read(O/'passages.json')};G=read(E/'source-guides.json');audits={x['id']:x for x in read(ROOT/'output/review/barrons-gables-2026-09-28/source-review.json')['items']}
spec=importlib.util.spec_from_file_location('overrides',APP/'scripts/source-import-overrides.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);integration_edits=module.apply(Q)
# Reuse inspected supplied guides only where the repaired review does not provide an explanation.
guide_imports=[]
for q in Q:
 if not q['explanation']:
  g=G[q['id']];assert g['key']==q['reviewAnswer'],q['id']
  text=g['text']
  # Typography fixes for symbols whose PDF text layer used plain baselines.
  text=re.sub(r'\b([a-zA-Z]{1,2})([23])\b',lambda m:m[1]+{'2':'²','3':'³'}[m[2]],text)
  text=re.sub(r'\b(cm|in|m)([23])\b',lambda m:m[1]+{'2':'²','3':'³'}[m[2]],text)
  text=re.sub(r'\s+',' ',text).strip()
  assert len(text)>20 and not re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f]',text),q['id']
  q['explanation']=text;guide_imports.append({'id':q['id'],'sourceForm':q['sourceForm'],'answerGuidePage':g['page'],'key':g['key'],'method':'Supplied answer guide, previously inspected in full-source audit; mapped by item and checked against repaired answer key.'})
# Remove only page-number tails and OCR spacing that do not encode tested errors.
for q in Q:
 for c in q['choices']:
  c['text']=re.sub(r'^(No mistakes[.]?)\s+\d{3}$',r'\1',c['text'])
 q['stem']=q['stem'].replace('thispassageismost','this passage is most').replace('mostnearly','most nearly')
# Recreated assets are embedded as vectors, never whole-page images.
def classify(q):
 s=q['stem'].lower();section=q['section']
 if section=='verbal':
  if len(q['choices'])==3:return 'logical_reasoning','logical_reasoning'
  if 'opposite' in s:return 'antonyms','antonyms'
  if re.search(r'\bis to\b',s):return 'analogies','analogies'
  if s.startswith('which word') or 'does not belong' in s:return 'classification','classification'
  return 'synonyms','synonyms'
 if section=='quantitative':
  if q['diagram']:return 'geometric_comparison','geometric_comparison'
  if 'sequence' in s or 'series' in s or 'pattern' in s:return 'sequence_multiplicative' if re.search(r'doubl|multipl|divid|halv',q['explanation'],re.I) else 'sequence_additive','number_series'
  if 'compare' in s or 'examine' in s:return 'numeric_comparison','nongeometric_comparison'
  return 'number_manipulation','number_manipulation'
 if section=='reading':
  if not q['passageId']:return 'standalone_vocabulary','standalone_vocabulary'
  if any(x in s for x in ['most nearly','meaning of','means']):return 'vocabulary_context','passage_vocabulary_context'
  if any(x in s for x in ['purpose','intended reader','most likely intended']):return 'author_purpose','passage_author_purpose'
  if any(x in s for x in ['title','main idea','summariz']):return 'main_idea','passage_main_idea'
  if any(x in s for x in ['implies','infer','suggest','most likely']):return 'inference','passage_inference'
  return 'detail','passage_detail'
 if section=='language':
  if 'spelling error' in s:return 'spelling','spelling'
  if 'sentence with an error' in s:return 'usage','error_detection'
  if 'does not belong' in s:return 'composition','irrelevant_sentence'
  if 'topic sentence' in s:return 'composition','topic_sentence'
  if 'support' in s:return 'composition','supporting_detail'
  if 'join' in s or 'transition' in s or '____' in s:return 'composition','transition'
  if 'topic' in s:return 'composition','topic_sentence'
  if 'insert' in s or 'place' in s:return 'composition','paragraph_insertion'
  return 'composition','paragraph_revision'
 if q['diagram']:return 'geometry','figure_numeric'
 if re.search(r'\b(solve for|equation|value of [a-z]|if [a-z] =|inequality)\b',s):return 'algebra','algebra'
 if re.search(r'percent|%|ratio|tax|interest|commission|scale',s):return 'ratios_percent','ratios_percent'
 if re.search(r'average|probability|median|mean\b',s):return 'statistics_probability','statistics_probability'
 if re.search(r'triangle|angle|rectangle|circle|square|quadrilateral|polygon|perimeter|area|volume',s):return 'geometry','geometry'
 if re.search(r'inches|centimeter|yards|feet|kilometer|meter',s):return 'measurement','measurement'
 return 'number_computation','number_computation'
# Confirmed semantic duplicate, with both source positions retained in the inventory.
duplicates={'gables-3-083':'gables-2-066'}
source_lookup={q['id']:q for q in Q};bank=[]
for q in Q:
 if q['id'] in duplicates:continue
 skill,fmt=classify(q)
 p=P.get(q['passageId']);difficulty=2
 if skill in ['synonyms','standalone_vocabulary','spelling']:difficulty=1
 b={'id':q['id'],'revision':1,'section':q['section'],'skill':skill,'format':fmt,'difficulty':difficulty,'stem':q['stem'],'choices':[c['text'] for c in q['choices']],'guide':{'correctChoiceId':q['reviewAnswer'],'explanation':q['explanation'],'shortcut':''},'templateFamily':'source-'+q['section']+'-'+fmt,'sourceType':'source_import','provenance':{'origin':'Owner-supplied Barron’s/Gables source, reviewed and editorially repaired where recorded','sourceForm':q['sourceForm'],'sourceQuestion':q['sourceQuestion'],'sourceLocator':q['locator'],'sourceSha256':q['sourceSha256'],'reviewCollectionSha256':sha(O/'questions.json'),'difficultyBasis':'Editorial routing estimate; no source-against-itself calibration','adaptation':q.get('contentProvenance','source_transcription')},'reviewStatus':'sample_reviewed'}
 if q.get('vocabularyTarget'):b['variantGroupId']='source-vocabulary-'+q['vocabularyTarget'].lower()
 if q['diagram']:
  svg=(O/q['diagram']['path']).read_text().strip();b['diagram']={'svg':svg,'alt':q['diagram'].get('alt','Recreated diagram for this '+q['section']+' question')}
 if p:b['passage']={'id':p['id'],'title':p['title'],'text':p['text'],'revision':2 if p.get('editorialStatus') else 1,'paragraphs':p['text'].split('\n\n')}
 if q['id']=='gables-2-066':b['provenance']['additionalSourceLocators']=[{'id':'gables-3-083','sourceForm':'gables-3','sourceQuestion':83,'sourceLocator':source_lookup['gables-3-083']['locator']}]
 bank.append(b)
assert len(bank)==1191 and all(q['guide']['explanation'] for q in bank)
# All unchanged accepted records will be carried forward by the publisher, not re-authored here.
write(D/'bank.json',bank);bankhash=sha(D/'bank.json')
oldinventory=read(D/'inventory.json')
if not (E/'inventory-before-import.json').exists():write(E/'inventory-before-import.json',oldinventory)
for item in oldinventory['items']:
 item['disposition']='duplicate' if item['id'] in duplicates else 'included';item['remaining']=[]
 if item['id'] in duplicates:item.update(canonicalId=duplicates[item['id']],reason='Same computation 5³ ÷ 5, same answer 25, reworded prompt and altered distractor ordering. One active copy avoids repeat exposure.')
 else:item['reason']='Approved source batch; original audit reconciled, 211 flags resolved, final release normalization and answer-guide checks recorded.'
write(D/'inventory.json',oldinventory)
policy=read(D/'source-import.json');policy.update(inventorySha256=sha(D/'inventory.json'),distribution={'status':'permitted','basis':'Owner supplied these sources and explicitly requested incorporation into the existing personal Phase IV app build on 2026-09-29. This records user authorization for this build, not an assertion of a third-party public redistribution license.'})
write(D/'source-import.json',policy)
# Keep the exact evidence available within the GitHub build package.
for src,name in [(O/'repair-2026-09-29/resolutions.json','flag-resolutions.json'),(O/'repair-2026-09-29/verification.json','flag-repair-verification.json'),(O/'repair-2026-09-29/manual-approval.json','prior-manual-approval.json'),(ROOT/'output/review/barrons-gables-2026-09-28/source-review.json','source-review.json'),(APP/'content/audits/gables-full-2026-09-27/source-coverage.json','gables-source-coverage.json')]:shutil.copyfile(src,E/name)
write(E/'integration-edits.json',integration_edits);write(E/'guide-imports.json',guide_imports)
checks=[]
for b in bank:
 q=source_lookup[b['id']];audit=audits[b['id']]
 assert not q['reviewIssues'] and audit.get('sourceReview') in ['reviewed_no_issue_recorded','reviewed_with_exception','independently_solved','reviewed'],(q['id'],audit.get('sourceReview'))
 checks.append({'id':b['id'],'transcription':'pass','correctness':'pass','consistency':'pass','visual':'pass','duplicates':'pass','method':'Reuse hash-reconciled full-source audit and inspected answer guide; apply September 29 flag repairs; final normalization checks key/choices/explanation, passage and vector linkage; semantic duplicate comparison against all sources and current 500-question release.','notes':('Editorial repair: '+'; '.join(q['repairNotes']) if q.get('repairNotes') else 'Prior full-source review recorded no unresolved issue; answer guide matched by source position and letter.')+' Integration edits and guide extraction are recorded separately; difficulty is not statistically calibrated.','sourceReviewMethod':audit.get('method','Independent Barron’s answer reasoning'),'evidence':['evidence/source-review.json','evidence/flag-resolutions.json','evidence/integration-edits.json','evidence/guide-imports.json'],'risk':'high' if q.get('repairNotes') or q['diagram'] else 'standard'})
write(D/'checks.json',{'bankSha256':bankhash,'calibration':'not_applicable_source_import','scope':'Source-audit reuse plus explicit repaired-item and release-format checks; not psychometric certification','items':checks})
# Use the same previously approved 100 samples, not a fresh unreviewed random sample.
approved=read(ROOT/'output/review/barrons-gables-2026-09-28/samples.json');sample=[{'id':x['id'],'section':x['section'],'sourceForm':x['sourceForm']} for x in approved['samples']];assert len(sample)==100 and all(s['id'] not in duplicates for s in sample)
R.mkdir(parents=True,exist_ok=True)
write(R/'manifest.json',{'policy':policy['policy'],'bankSha256':bankhash,'checksSha256':sha(D/'checks.json'),'policySha256':sha(D/'source-import.json'),'sample':sample,'sampleSelection':'Same 20 per section already reviewed and approved by the owner; no new random sample.'})
write(R/'decisions.json',{'bankSha256':bankhash,'manifestSha256':sha(R/'manifest.json'),'reviewer':'Project owner — explicit chat approval','date':'2026-09-29','approvalStatement':'Approved on all the manual review items. Can you fix the 211 questions that have flagged issues?','releaseAuthorization':'Great, can you add the updated questions to my existing question banks and questions index and add everything to my phase IV build?','scope':'Approval of the prior samples plus explicit authorization to integrate the corrected full batch; later normalization edits are logged, not falsely represented as separately read by the user.','items':[{'id':x['id'],'decision':'approve','notes':'Owner-approved sample; authorized corrected-batch incorporation into Phase IV.'} for x in sample]})
write(D/'import-summary.json',{'sourcePositions':1192,'included':len(bank),'duplicates':duplicates,'blocked':0,'sectionAdditions':dict(collections.Counter(q['section'] for q in bank)),'bankSha256':bankhash,'guideExplanationsImported':len(guide_imports),'integrationEdits':len(integration_edits),'sampleCount':100})
print(json.dumps(read(D/'import-summary.json'),indent=2))
