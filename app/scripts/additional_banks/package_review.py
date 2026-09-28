"""Produce inspectable drafts, not a formal approval packet before editorial gates."""
import collections,hashlib,html,json,random
from pathlib import Path
from schema import load,digest
ROOT=Path(__file__).resolve().parents[2]/'content/staging/additional-v1'
LABELS={'verbal':'Verbal Skills','reading':'Reading','mathematics':'Mathematics','language':'Language'}
CSS='''body{font:18px/1.6 system-ui,sans-serif;color:#172b3a;background:#f1f5f7;margin:0}main{max-width:880px;margin:auto;padding:32px 24px 80px}h1,h2,h3{line-height:1.2}h1{font-size:38px}a{color:#005c88}.banner{background:#fff0c2;border-left:5px solid #b97500;padding:16px 20px;border-radius:8px}.card,.passage{background:white;padding:24px;margin:22px 0;border:1px solid #dce5e9;border-radius:12px}.meta{color:#536875;font-size:14px}.choices{list-style-type:upper-alpha;padding-left:30px}.choices li{padding:5px 0}.passage{border-left:5px solid #1e7980}.passage p{margin:16px 0}.answer{border-top:1px solid #dce5e9;padding:20px 0}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:16px}.grid .card{margin:0}.badge{font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:#8d5600}nav{display:flex;gap:18px;flex-wrap:wrap}code{overflow-wrap:anywhere}p,li{overflow-wrap:anywhere}@media(max-width:600px){main{padding:20px 14px}h1{font-size:30px}.card,.passage{padding:18px}}@media print{body{background:white;font-size:11pt}main{max-width:none;padding:0}.card{break-inside:avoid;border:0;padding:8px 0}.answers{break-before:page}nav{display:none}.passage{border:1px solid #999}}'''
ESC=html.escape
NOTICE='Draft for inspection only. Editorial, full source-originality, rendering and human-review gates are not complete. This packet cannot approve publication.'
def pick(qs,seed,section):
 rng=random.Random(seed);ordered=list(qs);rng.shuffle(ordered);selected=[]
 def take(q):
  if q not in selected:selected.append(q)
 # Reading sample includes all 16 passages, with a rotating skill preference.
 if section=='reading':
  groups=collections.defaultdict(list)
  for q in ordered:groups[q['passageId']].append(q)
  for pid in sorted(groups):
   candidates=groups[pid]
   seen=collections.Counter(x['skill'] for x in selected)
   take(min(candidates,key=lambda q:(seen[q['skill']],-q['difficulty'])))
 # Cover every skill, difficulty and format before filling the quota.
 for field in ['skill','difficulty','format']:
  for value in sorted({q[field] for q in qs},key=str):
   if not any(q[field]==value for q in selected):
    take(next(q for q in ordered if q[field]==value))
 assert len(selected)<=20
 while len(selected)<20:
  counts=collections.Counter(q['skill'] for q in selected)
  families={q['templateFamily'] for q in selected}
  candidates=[q for q in ordered if q not in selected]
  totals=collections.Counter(q['skill'] for q in qs)
  take(min(candidates,key=lambda q:(counts[q['skill']]/totals[q['skill']],q['templateFamily'] in families)))
 assert {q['skill'] for q in selected}=={q['skill'] for q in qs}
 assert {q['difficulty'] for q in selected}=={q['difficulty'] for q in qs}
 assert {q['format'] for q in selected}=={q['format'] for q in qs}
 return sorted(selected,key=lambda q:q['id'])
def page(title,body):return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+ESC(title)+'</title><style>'+CSS+'</style></head><body><main>'+body+'</main></body></html>'
def packet(title,qs,passages):
 h=['<nav><a href="index.html">All banks</a><a href="#answers">Answer guide</a></nav>',f'<h1>{ESC(title)}</h1>',f'<p class="banner">{NOTICE} Questions appear first; answers are separate below.</p>']
 md=[f'# {title}',NOTICE,'Questions first; answer guide follows.'];current=None
 for i,q in enumerate(qs,1):
  if q.get('passageId') and q['passageId']!=current:
   p=passages[q['passageId']];current=p['id']
   h.append(f'<section class="passage"><h2>{ESC(p["title"])}</h2><div class="meta">{p["id"]} · original {p["genre"]}</div>')
   md.extend(['',f'## Passage: {p["title"]}'])
   for j,para in enumerate(p['paragraphs'],1):
    h.append(f'<p><span class="meta">[{j}]</span> {ESC(para)}</p>');md.append(f'[{j}] {para}\n')
   h.append('</section>')
  h.append(f'<section class="card" id="{q["id"]}"><div class="meta">{q["id"]} · {q["skill"].replace("_"," ")} · provisional level {q["difficulty"]}</div><h3>{i}. {ESC(q["stem"])}</h3><ol class="choices">'+''.join('<li>'+ESC(c)+'</li>' for c in q['choices'])+'</ol></section>')
  md.extend(['',f'### {i}. {q["id"]}',q['stem']]+[f'{"ABCD"[j]}. {c}' for j,c in enumerate(q['choices'])])
 h.append('<section class="answers" id="answers"><h2>Answer guide</h2><p>Solve first. Check correctness, ambiguity, difficulty, distractors, explanation, tip and presentation.</p>');md.extend(['','---','# Answer guide'])
 for i,q in enumerate(qs,1):
  g=q['guide'];evidence=' Supporting paragraphs: '+', '.join(map(str,q['evidenceParagraphs']))+'.' if q.get('evidenceParagraphs') else ''
  h.append(f'<div class="answer"><h3>{i}. {q["id"]}: {g["correctChoiceId"]}</h3><p>{ESC(g["explanation"]+evidence)}</p><p><strong>Tip:</strong> {ESC(g["shortcut"])}</p></div>')
  md.extend(['',f'## {i}. {q["id"]}: {g["correctChoiceId"]}',g['explanation']+evidence,'Tip: '+g['shortcut']])
 h.append('</section>')
 return page(title,''.join(h)),'\n\n'.join(md)+'\n'
def main():
 banks,passages=load(ROOT);review=ROOT/'review';review.mkdir(exist_ok=True)
 links=[]
 for section,bank in banks.items():
  qs=bank['questions'];sha=digest(ROOT/(section+'.json'))
  # Passage changes also invalidate Reading selections and decisions.
  dep=digest(ROOT/'reading-passages.json') if section=='reading' else ''
  seed=hashlib.sha256((sha+dep+'draft-inspection-v1').encode()).hexdigest()
  chosen=pick(qs,seed,section)
  manifest={'purpose':'provisional_inspection_not_formal_acceptance','policy':'draft-inspection-v1','bankSha256':sha,'passageSha256':dep or None,'seed':seed,'questionIds':[q['id'] for q in chosen],'skills':dict(collections.Counter(q['skill'] for q in chosen)),'formats':sorted({q['format'] for q in chosen}),'difficulty':dict(collections.Counter(q['difficulty'] for q in chosen))}
  (review/(section+'-sample.json')).write_text(json.dumps(manifest,indent=2)+'\n')
  decisions={'bankSha256':sha,'passageSha256':dep or None,'purpose':manifest['purpose'],'decisions':[{'id':q['id'],'decision':'pending','reviewer':None,'date':None,'notes':''} for q in chosen]}
  # Never overwrite any human decisions, even if content changed.
  target=review/(section+'-decisions.json')
  if not target.exists():target.write_text(json.dumps(decisions,indent=2)+'\n')
  (review/(section+'-decisions.template.json')).write_text(json.dumps(decisions,indent=2)+'\n')
  for suffix,questions in [('100',qs),('20',chosen)]:
   title=f'{LABELS[section]} — {len(questions)} draft questions'
   htmlbody,md=packet(title,questions,passages)
   (review/f'{section}-{suffix}.html').write_text(htmlbody)
   (review/f'{section}-{suffix}.md').write_text(md)
  links.append(f'<article class="card"><span class="badge">100 drafts · review pending</span><h2>{LABELS[section]}</h2><p><a href="{section}-100.html">Read all 100 questions</a></p><p><a href="{section}-20.html">Inspect the fixed 20-question sample</a></p></article>')
 intro='<span class="badge">HSPT · additional banks · draft v1</span><h1>400 questions, four new banks</h1><p>Original drafts with answers, explanations and tips. Reading includes 16 original passages.</p><p class="banner">'+NOTICE+'</p><div class="grid">'+''.join(links)+'</div><h2>What has been checked</h2><p>100 items per bank; four distinct choices; complete answer guides; balanced answer positions; valid passage references; exact numerical expression checks for all 100 Mathematics items. These checks do not certify natural-language correctness.</p><h2>Before approval</h2><p>Complete section calibration, item-level editorial and semantic originality review, rendering/iPad checks, and the formal human sample. Reading answer-length cues and weak distractors need attention. Mathematics is currently text-only. The 20-question packets are provisional inspection samples, not acceptance evidence.</p><p><a href="../REPORT.md">Status and limitations</a> · <a href="../manifest.json">Draft manifest</a></p>'
 (review/'index.html').write_text(page('HSPT additional question banks',intro))
 print('Packaged four full banks and four reproducible 20-question inspection samples; human decisions remain pending.')
if __name__=='__main__':main()
