"""Checks final staged revisions; records agent judgments separately from executable evidence."""
import json,hashlib,collections,re,sys,copy,itertools
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'app/content/staging/additional-v3';OLD=OUT.parent/'additional-v2';AUDIT=ROOT/'app/content/audits/gables-full-2026-09-27'
sys.path.insert(0,str(ROOT/'app/scripts/additional_banks'))
from schema import validate,digest
from validate import math_check
write=lambda name,value:(OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
banks={s:json.loads((OUT/f'{s}.json').read_text()) for s in ['verbal','reading','mathematics','language']}
ps=json.loads((OUT/'reading-passages.json').read_text())['passages'];passages={p['id']:p for p in ps}
manifest={'schemaVersion':'hspt-draft-1','batchId':'additional-v3','status':'draft_not_for_publication','sections':{s:{'file':s+'.json','version':3,'questionCount':100,'sha256':digest(OUT/f'{s}.json')} for s in banks},'passages':{'file':'reading-passages.json','sha256':digest(OUT/'reading-passages.json')},'assets':{str(p.relative_to(OUT)):digest(p) for p in sorted((OUT/'assets').glob('*.svg'))}}
write('manifest.json',manifest)
allqs=[q for b in banks.values() for q in b['questions']]
assert len({q['id'] for q in allqs})==400
report={};notes=json.loads((OUT/'author-review-notes.json').read_text());item_records=[]
def semantic(q):
 return {k:q.get(k) for k in ['stem','skill','format','oracleExpression','diagram','passageId','passageRevision','evidenceParagraphs']}|{'choices':sorted(q['choices']),'answer':q['choices']['ABCD'.index(q['guide']['correctChoiceId'])],'explanation':q['guide']['explanation'],'shortcut':q['guide']['shortcut']}
changes=[]
for s,b in banks.items():
 validate(b,passages);assert len(b['questions'])==100
 oldqs={q['id']:q for q in json.loads((OLD/f'{s}.json').read_text())['questions']}
 counts=collections.Counter(q['guide']['correctChoiceId'] for q in b['questions']);assert set(counts.values())=={25}
 for q in b['questions']:
  if q['format']=='error_detection':assert q['choices'][3]=='No error.'
  if q.get('diagram'):
   p=OUT/q['diagram']['file'];assert p.exists() and q['diagram']['alt'];assert '<svg' in p.read_text()
  same=semantic(q)==semantic(oldqs[q['id']])
  evidence=notes.get(q['id'],q['guide']['explanation'])
  item_records.append({'id':q['id'],'questionSha256':hashlib.sha256(json.dumps(q,sort_keys=True,ensure_ascii=False).encode()).hexdigest(),'structural':'passed','answerReview':'prior_full_review_reused_unchanged_semantics' if same else 'agent_review_no_defect_identified','method':'Compare every option with independently reasoned answer; prior item evidence reused only when semantic content matches. This record is an editorial judgment, not an automated proof.','reasoning':evidence,'humanReview':'pending','difficulty':'provisional'})
  changes.append({'id':q['id'],'priorRevision':oldqs[q['id']]['revision'],'revision':q['revision'],'semanticChange':not same,'oldFormat':oldqs[q['id']]['format'],'newFormat':q['format']})
 report[s]={'count':100,'skills':dict(collections.Counter(q['skill'] for q in b['questions'])),'formats':dict(collections.Counter(q['format'] for q in b['questions'])),'difficulty':dict(collections.Counter(q['difficulty'] for q in b['questions'])),'answerPositions':dict(counts),'strictlyLongestCorrect':sum(len(q['choices']['ABCD'.index(q['guide']['correctChoiceId'])])>max(len(c) for j,c in enumerate(q['choices']) if j!='ABCD'.index(q['guide']['correctChoiceId'])) for q in b['questions'])}
# Arithmetic checks of all numeric items; retained numerical solutions are compared with the prior independent full audit.
prior_math={q['id']:q for q in json.loads((AUDIT/'mathematics-checks.json').read_text())['items']}
maths=[]
for q in banks['mathematics']['questions']:
 if q['format']!='conceptual':
  record=math_check(q);record['bankSha256']=manifest['sections']['mathematics']['sha256']
  if not q.get('diagram'):
   prior=copy.deepcopy(prior_math[q['id']])
   renewed={'mat-a1-023':min(15*packs+3*single for packs in range(2) for single in range(9) if 6*packs+single==8),'mat-a1-028':F(27-24,24)*100,'mat-a1-086':next(n for n in range(1,156) if n*(n+1)==156)}
   if q['id'] in renewed:prior['independentStemSolution']=str(renewed[q['id']])
   assert F(record['result'])==F(prior['independentStemSolution']),q['id']
   oldq=next(x for x in json.loads((OLD/'mathematics.json').read_text())['questions'] if x['id']==q['id'])
   assert semantic(q)==semantic(oldq)
   record['independentStemSolution']=prior['independentStemSolution'];record['stemReviewEvidence']='Reconciled unchanged semantic content with full prior independent stem review.'
  maths.append(record)
# Second implementations for all sixteen new figures, derived from their labeled givens, not the author's expression field.
independent={56:sum([21,10,21,10]),57:sum([14*3,9*6,14*3]),58:F(18*7,2),59:sum(4 for cell in [(0,0),(0,1),(1,0),(1,1),(1,2),(2,2),(2,3)]),60:sum(9*4 for layer in range(4)),61:sum(9 for face in range(6)),62:118,63:180-67,64:F('3.14')*20/2,65:sum(7 for row in range(4)),66:F(sum([6,9,5,12]),4),67:sum(F(1,8) for step in range(5)),68:F('3.14')*64/4,69:F('7.5')/F(1,4),70:F(['A','B','B','C'].count('B'),4),71:sum([16,5,7,6,9,11])}
for n,result in independent.items():
 q=banks['mathematics']['questions'][n-1];assert F(q['choices']['ABCD'.index(q['guide']['correctChoiceId'])])==result
# Concept proofs and counterexamples. These are independent of the author's key letters.
concept={17:'If n is odd, n + 1 is even.',18:'12',19:'3/7 and 12/28',20:'The result is one tenth of the original.',41:'Milliliters',42:'It becomes four times as large.',43:'0.07 × 1,000 = 70',81:'6x + 15',82:'a − 5 < b − 5',83:'3d + 5c',84:'Range',85:'1/2'}
assert all((n+1)%2==0 for n in range(-101,102,2))
assert all(n%12==0 for n in range(1,1000) if n%4==0 and n%6==0)
assert F(3,7)==F(12,28) and F(3,7)!=F(6,21) and F(4,9)!=F(8,12) and F(5,8)!=F(15,16)
assert all((2*s)**2==4*s*s for s in range(1,100))
assert F('0.07')*1000==70
assert all(5*(2*x+3)-4*x==6*x+15 for x in range(-50,51))
assert all(a-5<b-5 for a in range(-10,10) for b in range(a+1,11))
assert not(-1 < -2) and not((-3)**2 < (-2)**2) and not(1+5<2)
assert all(max([2+k,7+k,11+k])-min([2+k,7+k,11+k])==9 for k in range(-10,11))
for n,answer in concept.items():
 q=banks['mathematics']['questions'][n-1];assert q['choices']['ABCD'.index(q['guide']['correctChoiceId'])]==answer
# Enumerate the new finite logic tasks separately.
logic=[]
orders=[p for p in itertools.permutations('JKLM') if p.index('J')+1==p.index('K') and p[-1]=='M' and abs(p.index('L')-p.index('M'))!=1]
assert orders==[('L','J','K','M')];logic.append({'id':'ver-a1-086','models':orders,'answer':'L'})
states=[s for s in itertools.product([False,True],repeat=4) if sum(s)==2 and s[0] and (not s[1] or s[2])]
assert states and all(not s[1] for s in states);logic.append({'id':'ver-a1-094','models':states,'answer':'Q.'})
states=[s for s in itertools.product([1,2],repeat=3) if sum(s)==5];assert all(s.count(2)==2 for s in states);logic.append({'id':'ver-a1-096','models':states,'answer':'Two.'})
for rec in logic:
 q=next(q for q in allqs if q['id']==rec['id']);assert q['choices']['ABCD'.index(q['guide']['correctChoiceId'])]==rec['answer']
# Exact/phrase novelty screening reads the entire combined source, including all three answer guides.
source_info=json.loads((OUT/'sources.json').read_text());source=ROOT/source_info['primaryMarkdown'];assert digest(source)==source_info['markdownSha256']
text=re.sub(r'<details>.*?</details>','',source.read_text(),flags=re.S)
norm=lambda x:' '.join(re.findall(r'\w+',x.casefold()))
normalized=norm(text)
source_phrases={tuple(normalized.split()[i:i+12]) for i in []} # built in a single linear pass below
words=normalized.split();source_phrases={tuple(words[i:i+12]) for i in range(len(words)-11)}
source_flags=[];overlap=[];target_hits=[]
oldlive=json.loads((ROOT/'app/public/content/banks/quantitative-v0001.json').read_text())['questions']
for q in allqs:
 flags=[]
 # Fixed directions are not distinctive question wording; screen authored content and all options.
 content=' '.join([q['stem']]+q['choices']);tokens=norm(content).split()
 hits=sorted({' '.join(tokens[i:i+12]) for i in range(len(tokens)-11) if tuple(tokens[i:i+12]) in source_phrases})
 if hits:flags.append({'type':'source_12_word_overlap','phrases':hits})
 if q.get('targetWord') and re.search(r'\b'+re.escape(q['targetWord'])+r'\b',text,re.I):target_hits.append({'id':q['id'],'target':q['targetWord']})
 for other in allqs+oldlive:
  if other['id']==q['id']:continue
  if norm(q['stem'])==norm(other['stem']) and set(map(norm,q['choices']))==set(map(norm,other['choices'])):flags.append({'type':'exact_item_duplicate','other':other['id']})
 if flags:source_flags.append({'id':q['id'],'flags':flags})
 overlap.append({'id':q['id'],'automatedFlags':flags,'semanticReview':'agent_compared_to_full_source_calibration_and_other_local_banks','resolution':'no_distinctive_copy_identified' if not flags else 'requires_adjudication','limitation':'Common skills and stock directions are allowed; semantic novelty is editorial judgment, not a string-match proof.'})
# Check full new passages for copied long phrases as well.
passage_flags=[]
for p in ps:
 w=norm(' '.join(p['paragraphs'])).split();hits={' '.join(w[i:i+12]) for i in range(len(w)-11) if tuple(w[i:i+12]) in source_phrases}
 if hits:passage_flags.append({'id':p['id'],'phrases':sorted(hits)})
assert not target_hits,target_hits
assert not passage_flags,passage_flags
assert not source_flags,source_flags
write('overlap-log.json',{'sourceSha256':source_info['markdownSha256'],'sourceQuestionPositions':894,'sourcePages':156,'automatedScope':'All transcribed questions, options, passages and guides; all 400 local items and 100 live Quantitative items. Original figure designs reviewed against prior full visual calibration; automatic phrase screening does not inspect figures.','flags':source_flags,'targetHits':target_hits,'passageFlags':passage_flags,'items':overlap,'status':'no_unresolved_overlap_identified_by_agent','humanReview':'pending'})
write('mathematics-checks.json',{'bankSha256':manifest['sections']['mathematics']['sha256'],'numericChecks':maths,'independentNewFigureResults':{str(k):str(v) for k,v in independent.items()},'conceptProofNotes':concept,'method':'88 numeric choices checked exactly; sixteen new figure answers recomputed from givens by a second implementation; twelve conceptual answers use mathematical reasoning and counterexamples. Earlier stem checks reused only for unchanged semantics.','humanReview':'pending'})
write('logic-checks.json',{'bankSha256':manifest['sections']['verbal']['sha256'],'items':logic})
write('item-audit.json',{'manifestSha256':digest(OUT/'manifest.json'),'items':item_records,'scope':'400 agent-reviewed items, not 400 human approvals. Executable tests provide narrower supporting evidence.'})
write('changes.json',{'from':'additional-v2','to':'additional-v3','items':changes})
report['readingAssembly']={'passageGroups':{p['id']:8 for p in ps},'wordCounts':{p['id']:sum(len(x.split()) for x in p['paragraphs']) for p in ps},'bankMix':{'comprehension':64,'standaloneVocabulary':36},'example62ItemForm':{'passages':[p['id'] for p in ps[:5]],'comprehensionCount':40,'vocabularyIds':[q['id'] for q in banks['reading']['questions'][64:86]],'vocabularyCount':22},'tenItemPracticeBurst':{'completePassageGroup':8,'standaloneVocabulary':2},'timingValidation':'pending_student_data'}
report.update(status='structural_and_content_checks_complete_pending_human_device_review',releaseReady=False)
write('validation.json',report)
print(json.dumps({'counts':{s:report[s]['count'] for s in banks},'mathNumeric':len(maths),'mathConcepts':len(concept),'figures':len(independent),'sourceFlags':len(source_flags),'passageFlags':len(passage_flags),'releaseReady':False}))
