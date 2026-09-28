"""Record the full agent review and stage corrections; never publish or approve.

The judgments below are editorial findings from reading the six source PDFs and
all local questions. This program records them; it does not simulate that review.
Source PDFs/OCR remain temporary reference inputs, outside the deliverable.
"""
import collections, copy, hashlib, html, json, re, sys
from pathlib import Path
from fractions import Fraction
from schema import load, digest
from validate import math_check, number
import package_review

APP=Path(__file__).resolve().parents[2]
AUDIT=APP/'content/audits/gables-full-2026-09-27'
OLD=APP/'content/staging/additional-v1'
NEW=APP/'content/staging/additional-v2'
TMP=Path('/private/tmp/hspt-full-audit')
PDF=Path('/private/tmp/hspt-gables')
SECTIONS=[('verbal',1,60),('quantitative',61,112),('reading',113,174),('mathematics',175,238),('language',239,298)]
URL='https://gablestutoring.com/wp-content/uploads/2020/08/'
FILES={'test1':'HSPT-Test-3.pdf','answers1':'HSPT-TEST-3-Answers.pdf','test2':'HSPT-TEST-4-1.pdf','answers2':'HSPT-TEST-4-Answers.pdf','test3':'HSPT-TEST-5.pdf','answers3':'HSPT-TEST-5-Answers.pdf'}
def write(path,data):
 path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def section(n):return next(s for s,a,b in SECTIONS if a<=n<=b)

# Each entry is an exception, not a proposed replacement for the hosted PDF.
issues=[]
def source(t,qs,kind,note,confidence='confirmed'):
 issues.append({'id':f'S{len(issues)+1:03}','test':t,'questions':qs,'kind':kind,'finding':note,'confidence':confidence})
source(1,[89],'multiple_valid_options','B and C express the same equality in reverse order; both quantities are 256.')
source(1,[211],'multiple_valid_options','The premise gives x > 4. Both C (x squared > 16) and D (x squared > 5) follow.')
source(1,[240],'multiple_errors','Both A (subject pronoun) and B (incorrect past participle after have) contain errors.')
source(1,[278],'multiple_errors','The extra word in the time phrase creates an additional error beyond the keyed capitalization error.')
source(1,[287],'explanation_error','The explanation incorrectly says equipment has no t; the word has a final t, but no extra t after p.')
source(1,[197],'explanation_error','Associativity changes grouping, not the order of addends.')
source(1,[104],'overgeneralized_rule','The square-versus-double shortcut is not valid for every number other than 2; the actual positive value in this item does satisfy it.')
source(1,[1,29,58],'weak_semantic_match','The keyed associations are loose: pepper/salt is not a strict antonym pair; the selected meanings for irrevocable and upstart are imperfect. Avoid these as lexical authorities.','editorial_caution')
source(1,[258,271,276],'usage_caution','The explanations make overly rigid claims about following dependent clauses or pronoun case after than. Context and accepted modern usage matter.','editorial_caution')
source(1,[88,97],'representation_convention','The intended answer depends on a Roman/Arabic or subscript/superscript pattern. Preserve representation when inspecting; equal numerical values alone cannot resolve it.','editorial_caution')
source(2,[7,9,14,27,32,34,42,45,46,50,54,56,57,59],'missing_printed_text','The exclusion word is absent from the hosted question image. The intended odd-one-out task is inferable from the guide, but the printed stem is incomplete.')
source(2,[35,37,39,40,43,44,48,51,53],'missing_printed_text','The word specifying the opposite-meaning task is absent from the hosted question image.')
source(2,[98],'uncheckable_printed_item','Quantity labels/variables are absent. Do not certify the answer from an inferred reconstruction.')
source(2,[175,194,296],'missing_printed_text','A missing exclusion word changes the meaning of the printed task.')
source(2,[186,197,204,207,212,214,217,218,223,225,229,231,233,235,237],'missing_printed_text','Italic mathematical variables or terms disappear in the hosted PDF. Some numerical work remains recoverable, but the complete printed task is not certified.')
source(2,[242],'missing_printed_text','The title whose typography is being tested is missing from option A.')
source(2,list(range(143,153)),'missing_passage_text','Italic text is missing in the witchcraft passage/questions, including the word referenced by Q148. Mark the affected passage group as limited rather than silently restoring it.')
source(2,[113],'ambiguous_scope','The keyed outer core answer depends on comparing it with an individual mantle layer; the question can also be read as referring to the whole mantle.','editorial_caution')
source(2,[135],'key_disagreement','C is better supported by the passage: glaciers erode the terrain and move material. The keyed D introduces a claim about ice being full of fertile soil.','strong_editorial_disagreement')
source(2,[162],'key_disagreement','The noun exploit most nearly means a deed, option B. A journey (keyed D) is not its general meaning.')
source(2,[53],'ambiguous_options','Keep and maintain can both oppose abandon, in addition to the missing task word.','editorial_caution')
source(2,[55],'unstated_condition','Two diagonal movements do not guarantee due north unless their east/west components cancel; the northward component alone is certain.','editorial_caution')
source(2,[228],'printed_number_disagreement','The printed multiplicand uses a decimal point, while the guide calculates with a whole number three orders of magnitude larger. Use neither as an unchecked oracle.','visual_print_caution')
source(2,[226],'explanation_typo','The guide displays .013 in the multiplication setup but uses .093 in the working and intended result.')
source(2,[209],'unstated_condition','The interest calculation requires the rate and interest to refer to the same period; the duration is not specified.','editorial_caution')
source(2,[243,252,269],'usage_caution','Permission with can, viewpoint-dependent bring/take, and singular they cannot be rejected categorically under current standard usage.','editorial_caution')
source(3,[87],'wrong_key','The successive operations are divide by 2, add 4, divide by 2; the next term is 37 (B). The guide instead subtracts 4 and keys D.')
source(3,[89],'equivalent_options','C and D are equal numerical values. A representation convention is being used without explicitly requesting that representation.')
source(3,[217],'multiple_valid_options','The premise gives x > 3. Both B (x cubed > 27) and C (x cubed > 9) follow.')
source(3,[235],'notation_error','The stated equation gives P = 5, hence P% = .05. The question asks for P% while keying 5; the guide repeats this notation error.')
source(3,[139],'source_fact_error','Carrying capacity concerns a sustainable population limit, not a combined density-and-diversity definition. A passage-based answer can match this text without being scientifically accurate.')
source(3,[141],'source_fact_error','Deciduous refers to seasonal shedding, not merely having leaves. The guide uses an inadequate definition.')
source(3,[145],'ambiguous_scope','The passage moves between population density and total capacity; this makes the comparison of biomes unreliable.','editorial_caution')
source(3,[103,177,198],'overgeneralized_rule','The square/double, decimal-shift, and distributivity explanations overstate their domains. Squaring is not always larger than doubling; zero-count shifting applies to powers of ten; division can distribute across a sum in its numerator.')
source(3,[215],'unstated_condition','The interest amount has no stated duration. The keyed principal assumes the stated rate applies to that entire period.','editorial_caution')
source(3,[242],'explanation_error','Affect can be a noun in psychology. Effect is correct in this sentence, but the guide gives an overbroad part-of-speech rule.')

def source_register():
 from pypdf import PdfReader
 catalog=[];coverage=[];pages_by_doc={};keys_by_test={}
 for name,filename in FILES.items():
  pdf=PDF/(name+'.pdf');reader=PdfReader(pdf);scanned=name.endswith('2')
  pages=[p.extract_text() or '' for p in reader.pages]
  if scanned:
   pages=['\n'.join(x['text'] for x in json.loads((TMP/name/f'page-{i}.json').read_text())) for i in range(1,len(pages)+1)]
  pages_by_doc[name]=pages
  catalog.append({'id':name,'webLabel':'Test '+name[-1]+(' answers' if name.startswith('answers') else ''),'url':URL+filename,'sha256':digest(pdf),'pages':len(pages),'accessDate':'2026-09-27','method':'all pages visually inspected; OCR used as reading aid' if scanned else 'all pages text-read; mathematical symbols and figures visually inspected','printedIdentity':'Peterson practice test 5' if scanned else 'Dummies practice test '+('1' if name.endswith('1') else '2')})
  if name.startswith('answers'):
   keys={}
   for page,text in enumerate(pages,1):
    for m in re.finditer(r'(?m)^\s*(\d(?:\s*\d){0,2})\.\s*(?:The correct answer is\s*\()?([ABCD])(?:\)|\.|\s|$)',text):
     n=int(re.sub(r'\s','',m[1]))
     if 1<=n<=298:keys.setdefault(n,{'letter':m[2],'page':page})
   keys_by_test[int(name[-1])]=keys
 for t in [1,2,3]:
  testpages=pages_by_doc['test'+str(t)]
  loc={}
  for p,text in enumerate(testpages,1):
   for m in re.finditer(r'(?m)^\s*(\d(?:\s*\d){0,2})\.\s',text):
    n=int(re.sub(r'\s','',m[1]))
    if 1<=n<=298:loc.setdefault(n,p)
  # Known spatial/spacing extraction failures, checked on the page images.
  if t==1:loc.update({100:10,107:11})
  if t==2:loc.update({22:2,79:8,85:8,88:8,95:9,129:14,136:14,147:16,180:19})
  for n in range(1,299):
   found=[x['id'] for x in issues if x['test']==t and n in x['questions']]
   key=keys_by_test[t].get(n)
   coverage.append({'test':t,'question':n,'section':section(n),'questionPdfPage':loc.get(n),'answerGuide':key,'inspection':'reviewed_with_exception' if found else 'reviewed_no_issue_recorded','exceptions':found,'scope':'stem/options/guide inspected; not an official certification; missing printed content is not reconstructed'})
 return catalog,coverage

def stage_revisions():
 banks,passages=load(OLD);changes=[]
 def edit(sec,n,reason,**fields):
  q=banks[sec]['questions'][n-1]
  before=copy.deepcopy(q)
  for k,v in fields.items():
   if k=='explanation':q['guide']['explanation']=v
   elif k=='shortcut':q['guide']['shortcut']=v
   else:q[k]=v
  q['revision']=2
  changes.append({'id':q['id'],'reason':reason,'before':before,'after':copy.deepcopy(q)})
 def replace(sec,n,reason,stem,correct,wrong,explanation,family,oracle=None):
  key='ABCD'.index(banks[sec]['questions'][n-1]['guide']['correctChoiceId'])
  choices=list(wrong);choices.insert(key,correct)
  fields=dict(stem=stem,choices=choices,explanation=explanation,templateFamily=family)
  if oracle is not None:fields['oracleExpression']=oracle
  edit(sec,n,reason,**fields)
 for n,word,correct,wrong,meaning in [
  (1,'COVET','desire',['conceal','purchase','reject'],'To covet something is to desire it strongly; it does not mean that one has purchased or hidden it.'),
  (20,'INERT','inactive',['weightless','invisible','valuable'],'Inert describes something that does not move or act; inactive is the closest meaning.'),
  (22,'REPRIEVE','postponement',['punishment','request','celebration'],'A reprieve is a temporary delay or relief, especially a postponement of punishment.'),
  (21,'TENTATIVE','uncertain',['definite','lengthy','immediate'],'Tentative means not yet settled or definite; uncertain is the closest choice.')]:
  replace('verbal',n,'Replace a vocabulary target already encountered in source material.',f'Which word is most nearly a synonym for {word}?',correct,wrong,meaning,'synonyms-'+word.lower())
 for n,word,correct,wrong,meaning in [
  (43,'DORMANT','active',['hidden','sleeping','delayed'],'Dormant means inactive for a time. Active is its opposite.'),
  (26,'AUTHENTIC','counterfeit',['unusual','valuable','ancient'],'Authentic means genuine. Counterfeit means made to imitate something genuine and is the opposite.'),
  (28,'DURABLE','fragile',['lasting','heavy','useful'],'Durable things withstand wear or damage; fragile things are easily damaged.'),
  (32,'BENEVOLENT','malicious',['generous','distant','uncertain'],'Benevolent describes goodwill; malicious describes an intention to cause harm.'),
  (36,'ASCEND','descend',['pause','approach','wander'],'Ascend means move upward; descend means move downward.'),
  (46,'DOCILE','defiant',['calm','patient','compliant'],'Docile describes willingness to follow guidance; defiant describes resistance to it.')]:
  replace('verbal',n,'Replace a source-exposed or repeated local vocabulary relationship.',f'Which word is most nearly opposite in meaning to {word}?',correct,wrong,meaning,'antonyms-'+word.lower())
 replace('verbal',92,'Replace the recognizable source syllogism structure.','Only volunteers who complete training may lead a tour. Iris led a tour, and Theo has not completed training. Assuming the rule was followed, which statement must be true?','Iris completed training, and Theo may not lead a tour.',['Every trained volunteer has led a tour.','Theo may lead a tour if Iris joins him.','Iris was the only volunteer who completed training.'],'Leading a tour requires training, so Iris completed it. Theo lacks the required training and is not permitted to lead. Training alone does not prove anyone has actually led a tour.','necessary-condition-and-exclusion')
 edit('language',18,'The explanation referred to the first choice after options had been shuffled.',explanation='The sentence about the match continuing contains the independent clause “the match continued.” The other choices lack an independent clause.')
 edit('language',27,'Effect is also a verb; specify the intended meaning.',stem='Choose the word meaning influence: The new schedule may ___ attendance.')
 for n,kind in [(46,'singular'),(47,'plural'),(48,'plural')]:
  q=banks['language']['questions'][n-1]
  edit('language',n,'Explicitly test possessive form; avoid ambiguity with attributive nouns.',stem=q['stem'].replace('correct phrase',f'correct {kind} possessive phrase'))
 spelling=[(66,'rhythm',['rythm','rhythum','rhythem'],'Rhythm is spelled r-h-y-t-h-m.'),(67,'cylinder',['cylindar','cillinder','cylender'],'Cylinder has one l and ends in -der.'),(69,'miniature',['minature','miniture','miniatuer'],'Miniature includes the sequence mini-a-ture.'),(71,'mischievous',['mischevious','mischievious','mischivous'],'Mischievous ends in -vous, with no extra i after v.'),(73,'broccoli',['brocolli','broccolli','brocoli'],'Broccoli has two c letters and one l.'),(77,'lantern',['lanturn','lanterrn','lantarn'],'Lantern is spelled l-a-n-t-e-r-n.'),(80,'obstacle',['obsticle','obstacel','obstacal'],'Obstacle ends in -acle.')]
 for n,word,wrong,explanation in spelling:
  if word=='conscience':explanation='Conscience is spelled c-o-n-s-c-i-e-n-c-e; it includes sc after the first n.'
  replace('language',n,'Replace a spelling target/close derivative already seen in the source tests.','Which word is spelled correctly?',word,wrong,explanation,'spelling-'+word)
 edit('mathematics',45,'Ask directly for the numeric unit used by the choices.',stem='A play begins at 6:45 p.m. and lasts 1 hour 50 minutes. How many minutes after 8:00 p.m. does it end?')
 edit('mathematics',88,'Make the scope of the square unambiguous.',stem='If y = 2 × x² − 3, what is y when x = −2?')
 for n in [96,100]:
  q=banks['mathematics']['questions'][n-1]
  edit('mathematics',n,'State equal selection probabilities.',stem=q['stem']+' Each counter remaining in the bag is equally likely to be chosen on each draw.')
 replace('mathematics',23,'Replace the five-to-eight notebook reskin of gb2-046.','A pack of 6 notebooks costs $15, while a single notebook costs $3. What is the least cost in dollars to buy exactly 8 notebooks?','21',['20','24','30'],'One pack and two singles cost 15 + 2 × 3 = 21 dollars. Eight singles cost 24 dollars; two packs would buy more than eight notebooks.','pack-and-single-unit-pricing','15+2*3')
 replace('mathematics',28,'Replace the same 25-percent growth relationship used by gb2-051.','A club grew from 24 members to 30 members, then lost 3 members. What is the overall percentage increase from the original membership?','12.5',['10','20','25'],'The final membership is 27, a gain of 3 from the original 24. The percentage increase is 3/24 × 100 = 12.5.','growth-followed-by-loss','(30-3-24)/24*100')
 replace('mathematics',64,'Replace the identical 68-degree straight-angle problem in gb2-097.','Two parallel lines are crossed by a transversal. One angle measures 76 degrees. What is the measure, in degrees, of its corresponding angle at the other intersection?','76',['38','104','152'],'Corresponding angles formed by a transversal crossing parallel lines are equal, so the other angle is 76 degrees.','corresponding-angles','76')
 replace('mathematics',85,'Replace the identical fixed-fee equation in gb2-066.','A taxi charges $8 for the first 2 miles and $3 for each additional mile. A ride costs $23. How many miles was the ride?','7',['5','9','11'],'After the first two miles, 23 − 8 = 15 dollars pays for 5 additional miles. The total distance is 2 + 5 = 7 miles.','included-distance-plus-additional-rate','2+(23-8)/3')
 replace('mathematics',86,'Replace the identical consecutive-number item in gb2-047.','Two consecutive positive integers have a product of 156. What is the smaller integer?','12',['11','13','14'],'The neighboring factors 12 and 13 have product 156, so the smaller integer is 12. The other proposed smaller values give different products.','consecutive-factor-pair','12')
 passage=passages['passage-a1-01'];passage['paragraphs'][1]=passage['paragraphs'][1].replace('from different piles','from the same pile');passage['revision']=2
 for q in banks['reading']['questions']:
  if q['passageId']==passage['id']:edit('reading',int(q['id'][-3:]),'Renew passage dependency after correcting contradictory color sorting.',passageRevision=2)
 NEW.mkdir(parents=True,exist_ok=True)
 for sec,b in banks.items():
  b.update(batchId=sec+'-additional-v2',version=2,status='draft_not_for_publication')
  write(NEW/(sec+'.json'),b)
 write(NEW/'reading-passages.json',{'schemaVersion':'hspt-draft-1','passages':list(passages.values())})
 manifest={'schemaVersion':'hspt-draft-1','batchId':'additional-v2','status':'draft_not_for_publication','sections':{s:{'file':s+'.json','version':2,'questionCount':100,'sha256':digest(NEW/(s+'.json'))} for s in banks},'passages':{'file':'reading-passages.json','sha256':digest(NEW/'reading-passages.json')}}
 write(NEW/'manifest.json',manifest);write(NEW/'changes.json',{'parent':'additional-v1','changes':changes,'passageCorrection':'passage-a1-01 revision 2: silver screws now come from the same color pile.'})
 plan=(OLD/'PLAN.md').read_text().replace('draft v1','revised draft v2')
 plan=plan[:plan.index('All six PDFs were opened')]+ 'All six PDFs have now been fully inspected, including every scanned page in the second pair. See [the full audit](../../audits/gables-full-2026-09-27/REPORT.md) for coverage, source defects, all-item answer checks and corrections. The original allocation above is retained as skill practice; the audit identifies required changes before an exam-style claim. No difficulty census or human/device approval is implied.\n'
 (NEW/'PLAN.md').write_text(plan)
 sources=json.loads((OLD/'sources.json').read_text())
 for item in sources['sources']:item['status']='full_inspection_completed_with_documented_exceptions'
 sources['audit']='../../audits/gables-full-2026-09-27/sources.json'
 write(NEW/'sources.json',sources)
 return banks,passages,changes

# Independently solved from the visible v1 stems; not read from oracleExpression.
EXPECTED='693 424 864 42 1 27 11/8 11/18 3/10 3/2 4.358 5.64 .18 8.4 17 24 14 36 47600 2 3/5 9 28 84 30 48 48.6 25 12 28 27 70 70 36 70 6 231 45 60 20 34 2750 1080 1350 35 255 67 14 40 14 40 1 6 72 .09 40 54 121 63 88 45 120 96 112 53 65 68 44 78.5 10 102 96 15 8 5 25 9 9 7 7 11 8 -15 13 7 25 40 5 6 5 11 8 10.5 16 10 3/10 1/3 1/4 86 1/15'.split()

def main():
 AUDIT.mkdir(parents=True,exist_ok=True)
 live=APP/'public/content/banks/quantitative-v0001.json';live_before=digest(live)
 original,oldpassages=load(OLD)
 assert len(EXPECTED)==100
 math_results=[]
 for q,expected in zip(original['mathematics']['questions'],EXPECTED):
  assert number(q['choices']['ABCD'.index(q['guide']['correctChoiceId'])])==Fraction(expected),q['id']
  r=math_check(q);r['independentStemSolution']=expected;r['stemToExpressionReview']='checked';math_results.append(r)
 import importlib.util
 spec=importlib.util.spec_from_file_location('quant_check',APP/'scripts/gables_v2/validate.py');quant=importlib.util.module_from_spec(spec);spec.loader.exec_module(quant)
 qs=json.loads(live.read_text())['questions'];proofs=json.loads((APP/'content/staging/gables-v2/proofs.json').read_text())
 quantitative=[quant.check(q,proofs[q['id']]) for q in qs]
 catalog,coverage=source_register()
 write(AUDIT/'sources.json',{'landingPage':'https://gablestutoring.com/practice-tests/','documents':catalog,'secondaryChecks':['https://www.ahdictionary.com/word/search.html?q=affect','https://www.merriam-webster.com/dictionary/exploit','https://www.merriam-webster.com/dictionary/deciduous','https://www.nps.gov/teachers/classrooms/carrying-capacity.htm']})
 write(AUDIT/'source-exceptions.json',issues)
 write(AUDIT/'source-coverage.json',{'totalQuestionPositions':894,'totalPdfPages':sum(x['pages'] for x in catalog),'items':coverage,'limits':'Inspection covers all positions, not a sample. Missing print is recorded as a defect, not silently reconstructed. No-issue-recorded is an agent finding, not publisher certification. Some answer-guide italics are missing throughout Test 2.'})
 banks,passages,changes=stage_revisions();changed={x['id']:x['reason'] for x in changes}
 rows=[]
 for sec,b in {'quantitative':{'questions':qs},**original}.items():
  for q in b['questions']:
   note=changed.get(q['id'])
   rows.append({'id':q['id'],'section':sec,'reviewedRevision':q['revision'],'reviewedAnswer':q['guide']['correctChoiceId'],'answerReview':'intended_answer_confirmed_with_revision_needed' if note else 'no_answer_error_identified','explanationReview':'corrected_in_v2' if q['id']=='lan-a1-018' else 'reviewed','revisionReason':note,'sourceComparison':'all_three_tests_and_guides','semanticOriginality':'replaced_or_reworded_in_v2' if note and ('Replace' in note) else 'no_distinctive_source_reskin_identified','evidenceParagraphs':q.get('evidenceParagraphs'),'bankCalibration':'existing_quantitative_bank' if sec=='quantitative' else 'skill_practice_only_pending_calibration','humanApproval':'not_granted_by_this_audit'})
 write(AUDIT/'local-item-audit.json',{'scope':500,'method':'Agent read every stem, four choices, explanation and tip. Reading checked against all 16 passages; arithmetic independently solved and exact-checked; 16 quantitative figures visually inspected. This file records that review, not an automated semantic proof.','inputHashes':{'quantitative':live_before,**{s:digest(OLD/(s+'.json')) for s in original}},'items':rows})
 write(AUDIT/'mathematics-checks.json',{'items':math_results,'independentSolutions':'The 100 expected values were entered from a separate stem-solving pass; the author-expression evaluator was then cross-checked.'})
 write(AUDIT/'quantitative-checks.json',{'bankSha256':live_before,'items':quantitative,'visualIds':[q['id'] for q in qs if q.get('visual')],'visualMethod':'Both saved contact sheets inspected; labeled dimensions, cell counts, bars and angle markings matched the stems and independent results.'})
 corrected,ps=load(NEW)
 v2math=[math_check(q) for q in corrected['mathematics']['questions']]
 write(NEW/'mathematics-checks.json',{'bankSha256':digest(NEW/'mathematics.json'),'items':v2math})
 write(NEW/'acceptance.json',{'status':'not_approved','releaseReady':False,'reason':'Audit corrections complete; broader format calibration and distractor work remain. Human and device review are pending. No previous human decisions apply to changed revisions.'})
 write(NEW/'item-audit.json',{'audit':'../../audits/gables-full-2026-09-27/local-item-audit.json','revisions':len(changes),'status':'agent_answer_review_complete_calibration_not_complete'})
 write(NEW/'validation.json',{'manifestSha256':digest(NEW/'manifest.json'),'counts':{s:len(b['questions']) for s,b in corrected.items()},'answerPositions':{s:dict(collections.Counter(q['guide']['correctChoiceId'] for q in b['questions'])) for s,b in corrected.items()},'arithmeticChecks':len(v2math),'releaseReady':False})
 assert digest(live)==live_before
 write(AUDIT/'summary.json',{'sourceTests':3,'answerPdfs':3,'pdfPages':sum(x['pages'] for x in catalog),'sourcePositions':len(coverage),'localItems':len(rows),'localItemsRevised':len(changes),'sourceExceptionGroups':len(issues),'numericItemsChecked':200,'liveBankUnchanged':True,'releaseReady':False})
 report(catalog,coverage,changes,rows)
 package_review.ROOT=NEW
 package_review.NOTICE='Revised skill-practice draft after the full six-PDF audit. Answer review is complete; exam-format calibration, distractor improvements, device checks and human approval remain pending. Not approved for publication.'
 package_review.main()
 for sec in corrected:
  target=NEW/'review'/f'{sec}-decisions.json'
  decisions=json.loads(target.read_text())
  if all(x['decision']=='pending' and x['reviewer'] is None for x in decisions['decisions']):
   target.write_bytes((NEW/'review'/f'{sec}-decisions.template.json').read_bytes())
 # The generic v1 index text is inappropriate for the completed audit.
 links=''.join(f'<li><a href="{s}-100.html">{s.title()}: all 100 revised questions</a></li>' for s in corrected)
 (NEW/'review/index.html').write_text(package_review.page('HSPT revised banks',f'<h1>400 revised questions</h1><p class="banner">{package_review.NOTICE}</p><ul>{links}</ul><p><a href="../../../audits/gables-full-2026-09-27/REPORT.md">Full audit report</a></p>'))
 print(json.dumps(json.loads((AUDIT/'summary.json').read_text()),indent=2))

def report(catalog,coverage,changes,rows):
 findings='\n'.join(f"- **{x['id']} — Test {x['test']}, Q{', '.join(map(str,x['questions']))}:** {x['finding']} ({x['confidence']})" for x in issues)
 docs='\n'.join(f"| {x['webLabel']} | {x['pages']} | [{FILES[x['id']]}]({x['url']}) |" for x in catalog)
 revisions='\n'.join(f"| {x['id']} | {x['reason']} |" for x in changes)
 text=f'''# Full Gables comparison and independent answer review

Date: 2026-09-27. Reviewer: Codex agent. This is a full inspection, not a sampled check and not human acceptance.

## Result

All three complete tests and all three matching answer guides were inspected across all five sections: **894 source question positions, 156 PDF pages**. All **500 local questions** were read and their intended answers checked, including explanations and tips. This includes 100 live Quantitative questions and 400 staged Verbal, Reading, Mathematics and Language questions.

The review found source errors and ambiguities, local wording/explanation defects, familiar vocabulary targets, repeated local problems, and substantial section-format gaps. **The new banks are not ready to be called full-test-calibrated or published.**

The existing live Quantitative bank was left unchanged. A corrected **additional-v2** draft preserves 100 questions in each additional section. **{len(changes)} question records were revised**, including six dependencies on one corrected reading passage. The original additional-v1 files and prior decisions were preserved.

## Coverage and method

| Section | Positions per source test | Across three tests | Local items |
|---|---:|---:|---:|
| Verbal | 1–60 | 180 | 100 |
| Quantitative | 61–112 | 156 | 100 |
| Reading | 113–174 | 186 | 100 |
| Mathematics | 175–238 | 192 | 100 |
| Language | 239–298 | 180 | 100 |

| Document | PDF pages | Source |
|---|---:|---|
{docs}

The first and third pairs were text-read in full, with visual checks of the quantitative/mathematical notation and diagrams. Every page of the scanned second pair was visually inspected, with OCR as a reading aid. Missing italics, variables and task words are defects in the hosted images, not merely extraction failures. Such items are **not certified** by reconstructing them from the guide.

Every local stem, all four choices, the explanation and the tip received an agent review. Reading answers were checked against the entire relevant passage, including the cited paragraph evidence. Verbal and Language answers were checked for meaning, logical entailment and standard written usage. Mathematics received a separate 100-answer stem-solving pass plus exact rational checks of every option. Quantitative received exact checks of every option, every sequence term and the supplied figure data, plus visual inspection of all 16 figures. No local intended key was found wrong; however, the original wording of flagged items was not reliably single-answer, and one explanation named the wrong choice position.

Full coverage does not imply infallibility. The item ledger's “no error identified” records the agent's judgment, not an independent human or publisher certification. Source answer-letter extraction is supporting indexing only; missing fields remain null rather than invented. Reference passages' historical/scientific claims are not a general-purpose fact-checked encyclopedia.

## Local corrections

| Item | Change |
|---|---|
{revisions}

Passage-a1-01 now takes the two silver screws from the same pile, consistent with the preceding color sort. All six dependent questions refer to passage revision 2. The Language fragment explanation now identifies the actual independent clause instead of referring to a pre-shuffle position. Affect/effect and possessive prompts specify what they test. The squared-expression notation and random-selection assumptions are explicit.

Originality was checked semantically against all three source tests, with phrase/target searches used only as aids. Common arithmetic operations and grammar rules are permitted; a familiar target or distinctive reskin is not. Source-exposed vocabulary/spelling targets and a familiar syllogism were replaced. Cross-bank review also replaced Mathematics items repeating the notebook unit-price setup, 25-percent growth relationship, 68-degree angle, fixed-fee equation, and consecutive-number problem already in Quantitative. This review does not prove universal novelty against every publication.

## Remaining calibration work

| Bank | Finding | Required before an exam-style claim |
|---|---|---|
| Verbal | Intended answers check out after corrections; distractors and difficulty remain editorial estimates. | Strengthen plausible distractors and diversify reasoning without recognizable source reskins. |
| Reading | All 100 items are passage-based; source sections contain 40 comprehension + 22 standalone vocabulary questions. Local passages are uniformly short (about 155–176 words), and many questions have conspicuously weak alternatives. The correct option is strictly longest in 57 of 100 original items. | Add standalone vocabulary, vary passage length/genre/demand and revise weak distractors. Rebuild timed forms with complete passage groups. |
| Mathematics | All 100 intended numerical answers check out. The bank is text-only; reference tests use figures and more conceptual multiple-choice questions. | Add original, verified diagrams and concept questions; recheck affected items and layouts. |
| Language | The bank mainly asks for correct completions/forms. Each reference section begins with 40 sentence-error items, then 10 spelling and 10 composition items. | Add error-detection sets with a genuine no-error option; strengthen composition editing and paragraph questions. |
| Quantitative | All 100 answers and 16 figures checked; no new key defect identified. | Existing approval is not changed by this audit. Difficulty remains unvalidated by student performance. |

The source counts describe these three practice tests, not an official current STS blueprint. The new draft is suitable for further review as **skill practice**, not yet as a representative full exam. Human acceptance and iPad/device layout checks remain pending; the audit does not invent either approval.

## Source exceptions and cautions

{findings}

For linguistic cross-checks, see [American Heritage on affect/effect](https://www.ahdictionary.com/word/search.html?q=affect), [Merriam-Webster on exploit](https://www.merriam-webster.com/dictionary/exploit), and [deciduous](https://www.merriam-webster.com/dictionary/deciduous). For the population concept, see [National Park Service carrying capacity](https://www.nps.gov/teachers/classrooms/carrying-capacity.htm). The hosted answer guides are comparison material, not unquestionable authorities.

## Audit files

- `source-coverage.json`: all 894 positions, source locators and exception links.
- `source-exceptions.json`: source errors, ambiguities and missing print.
- `local-item-audit.json`: all 500 local item results, input hashes and revision reasons.
- `mathematics-checks.json`: 100 independent stem solutions cross-checked with exact arithmetic.
- `quantitative-checks.json`: 100 numerical/relational checks and the 16 visual IDs.
- `sources.json`: all six URLs, identities, page counts and PDF hashes.
- `../../staging/additional-v2/changes.json`: before/after records for every changed question.

No deployment, source-PDF edits, live-bank edits, or human approval occurred.
'''
 (AUDIT/'REPORT.md').write_text(text)
 (NEW/'REPORT.md').write_text('# Revised additional banks\n\nFull six-PDF review completed; answer/wording corrections staged. These remain skill-practice drafts, not calibrated full-test banks.\n\nSee [the full audit](../../audits/gables-full-2026-09-27/REPORT.md) for all 500 item results, source exceptions, changes and remaining gates.\n')

if __name__=='__main__':main()
