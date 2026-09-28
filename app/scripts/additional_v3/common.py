import json,copy,hashlib,random
from pathlib import Path
BASE=Path(__file__).resolve().parents[2]
OLD=BASE/'content/staging/additional-v2'
OUT=BASE/'content/staging/additional-v3'
OUT.mkdir(exist_ok=True)
banks={s:json.loads((OLD/f'{s}.json').read_text()) for s in ['verbal','reading','mathematics','language']}
original=copy.deepcopy(banks)
passages=[]
review_notes={}
def setq(s,n,skill,fmt,stem,key,wrong,why,tip,diff=2,family=None,**extra):
 old=original[s]['questions'][n-1]
 q=dict(id=old['id'],revision=old['revision']+1,section=s,skill=skill,format=fmt,difficulty=diff,templateFamily=family or f'{fmt}-{n}',stem=stem,choices=[key]+wrong,guide={'correctChoiceId':'A','explanation':why,'shortcut':tip},provenance={'origin':'original_agent_authored_draft','authoredAt':'2026-09-27','revisionReason':'full_corpus_format_and_editorial_revision'},calibrationReference='source-calibration.json#'+s,reviewStatus='pending_human_review',**extra)
 assert len(q['choices'])==4 and len(set(q['choices']))==4,(s,n)
 banks[s]['questions'][n-1]=q
 review_notes[q['id']]=why
 return q
def finalize():
 for s,b in banks.items():
  positions=list(range(4))*25
  random.Random('additional-v3-balanced-'+s).shuffle(positions)
  if s=='language':
   # Preserve the standard No error option in position D. Balance keys across the complete bank.
   fixed=list(range(3))*16+[0,1]
   random.Random('additional-v3-error-keys').shuffle(fixed)
   positions=fixed+[3]*16
   counts={p:positions.count(p) for p in range(4)}
   remaining=[p for p in range(4) for _ in range(25-counts[p])]
   random.Random('additional-v3-language-rest').shuffle(remaining)
   positions+=remaining
  for i,q in enumerate(b['questions']):
   key=q['choices']['ABCD'.index(q['guide']['correctChoiceId'])]
   wrong=[c for j,c in enumerate(q['choices']) if j!='ABCD'.index(q['guide']['correctChoiceId'])]
   random.Random('additional-v3-'+q['id']).shuffle(wrong)
   if q['format']=='error_detection' and key!='No error.':
    wrong.remove('No error.');wrong.append('No error.')
   wrong.insert(positions[i],key);q['choices']=wrong;q['guide']['correctChoiceId']='ABCD'[positions[i]]
   if q['revision']==original[s]['questions'][i]['revision']:q['revision']+=1
   q['calibrationReference']='source-calibration.json#'+s
  b.update(batchId=s+'-additional-v3',version=3)
  (OUT/f'{s}.json').write_text(json.dumps(b,indent=2,ensure_ascii=False)+'\n')
 (OUT/'reading-passages.json').write_text(json.dumps({'schemaVersion':'hspt-draft-1','passages':passages},indent=2,ensure_ascii=False)+'\n')
 (OUT/'author-review-notes.json').write_text(json.dumps(review_notes,indent=2,ensure_ascii=False)+'\n')
