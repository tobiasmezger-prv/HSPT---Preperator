"""Offline import gate and deterministic 20-of-100 sample review. Standard library only."""
import argparse, hashlib, json, math
from datetime import date
from collections import Counter,defaultdict
from pathlib import Path
SKILLS={'sequence_additive','sequence_multiplicative','numeric_comparison','number_manipulation','symbolic_pattern','odd_one_out'}
VERSION='sample-review-v1'
def fingerprint(value):
 return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def bank_hash(bank):return fingerprint(sorted(bank,key=lambda q:q['id']))
def validate(bank):
 errors=[]
 if not isinstance(bank,list) or not bank:return ['Expected a nonempty array of questions.']
 if len(bank)%100:errors.append('Submit complete 100-question batches; no silently truncated final batch.')
 ids=set();questions=set()
 for i,q in enumerate(bank):
  label=q.get('id',f'row-{i}') if isinstance(q,dict) else f'row-{i}'
  if not isinstance(q,dict):errors.append(f'{label}: expected object');continue
  for field in ['id','stem','templateFamily']:
   if not isinstance(q.get(field),str) or not q[field].strip():errors.append(f'{label}: missing {field}')
  if q.get('id') in ids:errors.append(f'{label}: duplicate ID')
  ids.add(q.get('id'))
  if q.get('skill') not in SKILLS:errors.append(f'{label}: unknown skill')
  if type(q.get('difficulty')) is not int or q['difficulty'] not in (1,2,3):errors.append(f'{label}: difficulty must be 1–3')
  c=q.get('choices')
  if not isinstance(c,list) or len(c)!=4 or any(not isinstance(x,str) or not x.strip() for x in c):errors.append(f'{label}: four nonempty choices required')
  elif len({x.strip().casefold() for x in c})!=4:errors.append(f'{label}: duplicate choices')
  else:
   key=fingerprint([q.get('stem','').strip().casefold(),sorted(x.strip().casefold() for x in c)])
   if key in questions:errors.append(f'{label}: duplicate question independent of choice order')
   questions.add(key)
  g=q.get('guide')
  if not isinstance(g,dict):errors.append(f'{label}: missing guide');continue
  if g.get('correctChoiceId') not in ['A','B','C','D']:errors.append(f'{label}: invalid answer key')
  for field in ['explanation','shortcut']:
   if not isinstance(g.get(field),str) or not g[field].strip():errors.append(f'{label}: missing {field}')
 return errors

def quotas(bank):
 counts=Counter(q['skill'] for q in bank)
 exact={s:20*n/len(bank) for s,n in counts.items()}
 result={s:max(1,math.floor(n)) for s,n in exact.items()}
 while sum(result.values())<20:
  s=max(result,key=lambda k:(exact[k]-result[k],k));result[s]+=1
 while sum(result.values())>20:
  s=max((k for k in result if result[k]>1),key=lambda k:(result[k]-exact[k],k));result[s]-=1
 return result

def sample(bank,audit):
 """One hundred only. Skill quotas, then mandatory format/difficulty coverage,
 risk picks, then hash-based picks; no ability to cherry-pick favorable IDs."""
 if len(bank)!=100:raise ValueError('Sample one 100-question batch at a time')
 digest=bank_hash(bank);capacity=quotas(bank);chosen=[];why={}
 lookup={r['id']:r for r in audit}
 def rank(q):return fingerprint([VERSION,digest,q['id']])
 def risk(q):return lookup[q['id']].get('risk',0)
 def eligible(predicate):return [q for q in bank if q['id'] not in why and capacity[q['skill']]>0 and predicate(q)]
 def take(q,reason):chosen.append(q);why[q['id']]=reason;capacity[q['skill']]-=1
 # Cover a geometric item and all difficulty levels, even if minority strata.
 predicates=[('geometric format',lambda q:lookup[q['id']].get('format')=='geometric_comparison')]
 predicates += [(f'difficulty {d}',lambda q,d=d:q['difficulty']==d) for d in sorted({q['difficulty'] for q in bank})]
 for reason,predicate in predicates:
  if any(predicate(q) for q in chosen):continue
  candidates=eligible(predicate)
  if candidates:take(sorted(candidates,key=lambda q:(-risk(q),rank(q)))[0],f'Coverage: {reason}')
 for skill in sorted(capacity):
  pool=lambda:eligible(lambda q:q['skill']==skill)
  # One explicitly high-risk item per skill; remaining picks diversify families.
  candidates=pool()
  if candidates:take(sorted(candidates,key=lambda q:(-risk(q),rank(q)))[0],'Risk-based check within skill')
  while capacity[skill]>0:
   families={q['templateFamily'] for q in chosen}
   candidates=pool()
   q=min(candidates,key=lambda q:(q['templateFamily'] in families,rank(q)))
   take(q,'Seeded pick within skill; prefer a new pattern family')
 assert len(chosen)==20 and len(why)==20
 if {q['difficulty'] for q in chosen}!={q['difficulty'] for q in bank}:raise ValueError('Cannot cover all difficulty strata within skill quotas; rebalance this batch before sampling.')
 return sorted(chosen,key=lambda q:q['id']),why

def gate(bank,evidence,audit,decisions=None):
 digest=bank_hash(bank);issues=[]
 if not evidence or evidence.get('bankHash')!=digest or evidence.get('status')!='passed':issues.append('Fresh mathematical-check receipt required for this exact bank revision.')
 elif len(evidence.get('checkedIds',[]))!=len(bank) or set(evidence.get('checkedIds',[]))!={q['id'] for q in bank}:issues.append('Mathematical receipt does not cover every question.')
 if not audit or audit.get('bankHash')!=digest:issues.append('Fresh item-by-item calibration audit required.')
 elif len(audit.get('items',[]))!=len(bank) or {r['id'] for r in audit.get('items',[])}!={q['id'] for q in bank}:issues.append('Calibration audit must cover every question.')
 if issues:return 'blocked',issues
 if any(r.get('disposition')=='reject' for r in audit['items']):return 'blocked',['Rejected content must be repaired or removed.']
 if any(r.get('questionHash')!=fingerprint(next(q for q in bank if q['id']==r['id'])) for r in audit['items']):return 'blocked',['Calibration item fingerprints are stale.']
 selected=[]
 for offset in range(0,len(bank),100):
  picked,_=sample(sorted(bank,key=lambda q:q['id'])[offset:offset+100],audit['items']);selected+=picked
 if not decisions:return 'pending_sample_review',issues
 if decisions.get('bankHash')!=digest or decisions.get('policyVersion')!=VERSION:issues.append('Human review is stale for this revision or policy.')
 if not decisions.get('reviewer','').strip():issues.append('Reviewer is required.')
 try:date.fromisoformat(decisions.get('reviewedAt',''))
 except (ValueError,TypeError):issues.append('Review date must be YYYY-MM-DD.')
 records=decisions.get('items',[])
 if len(records)!=len(selected) or {r.get('id') for r in records}!={q['id'] for q in selected}:issues.append('Review must cover precisely the fixed 20-per-100 sample.')
 for r in records:
  if r.get('decision')!='approve':issues.append(f"{r.get('id')}: review unfinished or defect found; affected-family review required.")
  if r.get('questionHash')!=fingerprint(next((q for q in selected if q['id']==r.get('id')),None)):issues.append(f"{r.get('id')}: stale question review.")
 if decisions.get('calibrationAcknowledged') is not True:issues.append('Reviewer must acknowledge the audit’s format/difficulty limitations.')
 if issues:return 'blocked',issues
 return 'sample_reviewed_for_skill_practice',[]

def write_packet(bank,audit,evidence,directory):
 directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
 digest=bank_hash(bank);picked=[];reasons={}
 for start in range(0,len(bank),100):
  batch=sorted(bank,key=lambda q:q['id'])[start:start+100]
  part,why=sample(batch,audit['items']);picked+=part;reasons.update(why)
 manifest={'policyVersion':VERSION,'bankHash':digest,'sampleIds':[q['id'] for q in picked],'reasons':reasons,'skillCounts':dict(Counter(q['skill'] for q in picked)),'difficultyCounts':dict(Counter(q['difficulty'] for q in picked))}
 (directory/'sample-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 template={'policyVersion':VERSION,'bankHash':digest,'reviewer':'','reviewedAt':'','calibrationAcknowledged':False,'items':[{'id':q['id'],'questionHash':fingerprint(q),'decision':'pending','notes':''} for q in picked]}
 # Never overwrite completed or partly filled reviewer decisions.
 target=directory/'decisions.json'
 if not target.exists():target.write_text(json.dumps(template,indent=2)+'\n')
 else:(directory/'decisions.template.json').write_text(json.dumps(template,indent=2)+'\n')
 md=['# Human review sample — 20 questions per 100','',f'Bank revision: `{digest[:12]}`. Policy: `{VERSION}`.','',
 'Solve these questions first, without consulting the answer key below. Record confusing wording, competing answers, difficulty, and any unhelpful tip. This is the fixed sample for this revision; do not swap out difficult or problematic questions.','',
 'The sample balances available skill categories, provisional difficulty levels, geometric content where present, and risk-based picks. See sample-manifest.json for its exact composition. It is not a random statistical certification or approval of every unsampled question.','',
 '## Questions','']
 for i,q in enumerate(picked,1):
  md += [f"### {i}. {q['id']}",'',q['stem'],'',*[f'{c}. {t}' for c,t in zip('ABCD',q['choices'])],'','Your answer: ____  Difficulty: easy / medium / hard  Time (optional): ____','']
 md+=['## Answer key and reviewer notes','', 'Check after solving. Approve, request a revision, or reject each item. A material defect blocks batch acceptance and triggers a check of the affected family.','']
 lookup={x['id']:x for x in audit['items']}
 for i,q in enumerate(picked,1):
  a=lookup[q['id']];g=q['guide']
  md += [f"### {i}. {q['id']} — {g['correctChoiceId']}",'',f"**Explanation:** {g['explanation']}",'',f"**Tip:** {g['shortcut']}",'',f"**Skill:** {q['skill']} · **Provisional difficulty:** {q['difficulty']}/3",'',f"**Why selected:** {reasons[q['id']]}",'',f"**Calibration note:** {a['note']}",'','Decision: approve / revise / reject','Reviewer notes: ____________________','']
 (directory/'SAMPLE_REVIEW.md').write_text('\n'.join(md))
 return manifest

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('bank');p.add_argument('--evidence',required=True);p.add_argument('--audit',required=True);p.add_argument('--output',required=True);p.add_argument('--decisions');p.add_argument('--require-accepted',action='store_true');args=p.parse_args()
 read=lambda path:json.loads(Path(path).read_text())
 bank=read(args.bank);errors=validate(bank)
 if errors:raise SystemExit('\n'.join(errors))
 evidence=read(args.evidence);audit=read(args.audit)
 status,issues=gate(bank,evidence,audit)
 if status=='blocked':raise SystemExit('\n'.join(issues))
 manifest=write_packet(bank,audit,evidence,args.output)
 if args.decisions:status,issues=gate(bank,evidence,audit,read(args.decisions))
 report={'status':status,'issues':issues,'bankHash':bank_hash(bank),'sampleCount':len(manifest['sampleIds']),'itemStatus':'Not individually human-approved unless separately recorded.'}
 (Path(args.output)/'gate-report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report,indent=2))
 if args.require_accepted and status!='sample_reviewed_for_skill_practice':raise SystemExit(1)
if __name__=='__main__':main()
