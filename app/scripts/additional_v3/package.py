import json,hashlib,random,collections,itertools,html,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'app/content/staging/additional-v3';REVIEW=OUT/'review';REVIEW.mkdir(exist_ok=True)
LABELS={'verbal':'Verbal Skills','reading':'Reading','mathematics':'Mathematics','language':'Language'}
banks={s:json.loads((OUT/f'{s}.json').read_text()) for s in LABELS};passages={p['id']:p for p in json.loads((OUT/'reading-passages.json').read_text())['passages']}
hashfile=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
POLICY='full-corpus-v3-risk-format-complete-reading-groups-1'
E=html.escape

def sample(section,qs):
 sha=hashfile(OUT/f'{section}.json');dep=hashfile(OUT/'reading-passages.json') if section=='reading' else ''
 assets=json.dumps({q['id']:hashfile(OUT/q['diagram']['file']) for q in qs if q.get('diagram')},sort_keys=True)
 seed=hashlib.sha256((sha+dep+assets+POLICY).encode()).hexdigest();rng=random.Random(seed);ordered=sorted(qs,key=lambda q:q['id']);rng.shuffle(ordered);rank={q['id']:i for i,q in enumerate(ordered)}
 selected=[]
 def add(q):
  if q not in selected:selected.append(q)
 def risk(q):return q['difficulty']+2*bool(q.get('diagram'))+int(q.get('noErrorCorrect',False))+int(q['format']=='conceptual')
 def choose(candidates):
  if section=='language' and sum(q.get('noErrorCorrect',False) for q in selected)>=2 and any(not q.get('noErrorCorrect',False) for q in candidates):candidates=[q for q in candidates if not q.get('noErrorCorrect',False)]
  families={q['templateFamily'] for q in selected}
  return min(candidates,key=lambda q:(q['templateFamily'] in families,-risk(q),rank[q['id']]))
 if section=='reading':
  groups={p:[q for q in qs if q.get('passageId')==p] for p in passages}
  required={q['format'] for q in qs if q.get('passageId')}
  pairs=[]
  for a,b in itertools.combinations(groups,2):
   combined=groups[a]+groups[b]
   if {q['format'] for q in combined}==required and passages[a]['genre']!=passages[b]['genre'] and max(sum(len(x.split()) for x in passages[p]['paragraphs']) for p in [a,b])>=300:pairs.append((a,b))
  assert pairs,'Need a covered complete-passage pair'
  pairs.sort(key=lambda pair:(-sum(risk(q) for p in pair for q in groups[p]),sum(rank[q['id']] for p in pair for q in groups[p])))
  for p in pairs[0]:
   for q in groups[p]:add(q)
  vocab=[q for q in ordered if q['format']=='standalone_vocabulary']
  for d in sorted({q['difficulty'] for q in vocab}):add(choose([q for q in vocab if q['difficulty']==d]))
  while len(selected)<20:add(choose([q for q in vocab if q not in selected]))
 else:
  # New formats and every skill/difficulty are explicit constraints, rather than hoping random picks cover them.
  for field in ['format','skill','difficulty']:
   for value in sorted({q[field] for q in qs},key=str):
    if not any(q[field]==value for q in selected):add(choose([q for q in qs if q[field]==value]))
  if section=='mathematics':
   for pred,minimum in [(lambda q:bool(q.get('diagram')),5),(lambda q:q['format']=='conceptual',3)]:
    while sum(pred(q) for q in selected)<minimum:add(choose([q for q in qs if pred(q) and q not in selected]))
  if section=='language':
   while sum(q.get('noErrorCorrect',False) for q in selected)<2:add(choose([q for q in qs if q.get('noErrorCorrect',False) and q not in selected]))
  assert len(selected)<=20,(section,len(selected))
  totals=collections.Counter(q['skill'] for q in qs)
  while len(selected)<20:
   counts=collections.Counter(q['skill'] for q in selected)
   candidates=[q for q in qs if q not in selected and not (section=='language' and sum(x.get('noErrorCorrect',False) for x in selected)>=2 and q.get('noErrorCorrect',False))]
   add(min(candidates,key=lambda q:(counts[q['skill']]/totals[q['skill']],q['templateFamily'] in {x['templateFamily'] for x in selected},-risk(q),rank[q['id']])))
 selected.sort(key=lambda q:q['id'])
 for field in ['format','skill','difficulty']:assert {q[field] for q in selected}=={q[field] for q in qs},(section,field)
 assert len(selected)==20
 return selected,dict(policy=POLICY,seed=seed,bankSha256=sha,passageSha256=dep or None,assetHashes=json.loads(assets),questionIds=[q['id'] for q in selected],skills=dict(collections.Counter(q['skill'] for q in selected)),formats=dict(collections.Counter(q['format'] for q in selected)),difficulty=dict(collections.Counter(q['difficulty'] for q in selected)),purpose='fixed_human_review_pending',selectionNotes='Risk-prioritized, seeded tie breaks, skill/format/difficulty coverage. Reading uses two complete eight-question groups plus four standalone vocabulary items; this intentionally overweights comprehension in a 20-item sample to avoid splitting passages. Not a timed exam form. Language deliberately overrepresents composition to cover every new format. Math includes at least five figures and three conceptual items.')
CSS='''*{box-sizing:border-box}body{margin:0;background:#eef3f5;color:#183747;font:17px/1.65 system-ui,-apple-system,sans-serif}main{max-width:960px;margin:auto;padding:36px 24px 80px}h1,h2,h3{line-height:1.2}h1{font-size:42px;letter-spacing:-1.5px}h2{font-size:29px;margin-top:44px}h3{font-size:20px}a{color:#075f78}nav{display:flex;gap:18px;flex-wrap:wrap;margin:16px 0}.eyebrow{font-size:12px;text-transform:uppercase;letter-spacing:.15em;color:#496876}.summary{background:#d8eceb;padding:22px;border-radius:14px}.notice{border-left:4px solid #b07819;padding:10px 18px;background:#fff4d9}.card,.passage{background:#fff;border:1px solid #d1dfe4;border-radius:14px;padding:26px;margin:20px 0}.passage{border-top:5px solid #2a7c80}.meta{color:#5b6c75;font-size:13px}.choices{list-style-type:upper-alpha;padding-left:30px}.choices li{padding:7px 8px}svg{display:block;width:100%;max-width:580px;height:auto;margin:16px auto}.figure-note{text-align:center;font-size:13px;color:#5b6c75}.review-controls{border-top:1px solid #dde6e9;margin-top:22px;padding-top:16px;display:grid;grid-template-columns:180px 1fr;gap:14px}label{display:block;font-size:14px}select,input,textarea,button{font:inherit;border:1px solid #9bb4c0;border-radius:6px;padding:9px;background:white;color:#183747;max-width:100%}select,textarea{width:100%}textarea{min-height:65px;font-size:15px}button{cursor:pointer;background:#165f68;color:white;border:0}button.secondary{background:white;color:#165f68;border:1px solid #165f68}details.answers{border:1px solid #9bb4c0;padding:20px;border-radius:12px;margin-top:45px;background:white}summary{cursor:pointer;font-weight:650}.answer{padding:16px 0;border-bottom:1px solid #dce5e9}.grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}.grid .card{margin:0}.toolbar{display:flex;align-items:end;gap:16px;flex-wrap:wrap;background:white;padding:20px;border-radius:12px}.progress{font-size:14px;color:#496876}pre{white-space:pre-wrap}.short-list li{margin-bottom:7px}.section-cover{border-top:3px solid #165f68;margin-top:48px;padding-top:24px}@media(max-width:600px){main{padding:22px 14px}h1{font-size:33px}.card,.passage{padding:18px}.grid,.review-controls{grid-template-columns:1fr}.toolbar{align-items:stretch}}@media print{body{background:white;font-size:11pt}main{max-width:none;padding:0}.no-print,nav,button,.toolbar{display:none!important}.card{break-inside:avoid;border:0;padding:12px 0}.passage{border:1px solid #aaa}.review-controls{display:none}.section-cover{break-before:page}.answers{break-before:page}details.answers{display:block}svg{max-width:430px}.notice{background:white}}'''
JS='''const DATA=JSON.parse(document.getElementById('review-data').textContent);const STORE='hspt-review-'+DATA.packetHash;let saved={reviewer:'',decisions:{}};try{saved=JSON.parse(localStorage.getItem(STORE))||saved}catch(e){}const nameField=document.getElementById('reviewer');if(nameField){nameField.value=saved.reviewer||'';nameField.addEventListener('input',()=>{saved.reviewer=nameField.value;persist()})}function persist(){try{localStorage.setItem(STORE,JSON.stringify(saved))}catch(e){document.getElementById('progress').textContent='Browser storage unavailable; export your decisions before closing.';return}refresh()}function refresh(){const done=DATA.items.filter(q=>saved.decisions[q.id]?.decision&&saved.decisions[q.id].decision!=='pending').length;document.getElementById('progress').textContent=done+' of '+DATA.items.length+' decisions recorded on this browser.'}document.querySelectorAll('[data-decision]').forEach(el=>{const id=el.dataset.decision;el.value=saved.decisions[id]?.decision||'pending';el.addEventListener('change',()=>{saved.decisions[id]={...saved.decisions[id],decision:el.value,date:new Date().toISOString()};persist()})});document.querySelectorAll('[data-notes]').forEach(el=>{const id=el.dataset.notes;el.value=saved.decisions[id]?.notes||'';el.addEventListener('input',()=>{saved.decisions[id]={...saved.decisions[id],notes:el.value};persist()})});document.getElementById('export')?.addEventListener('click',()=>{const payload={packetHash:DATA.packetHash,policy:DATA.policy,reviewer:saved.reviewer,manifests:DATA.manifests,decisions:DATA.items.map(q=>({id:q.id,section:q.section,decision:saved.decisions[q.id]?.decision||'pending',notes:saved.decisions[q.id]?.notes||'',date:saved.decisions[q.id]?.date||null}))};const url=URL.createObjectURL(new Blob([JSON.stringify(payload,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download='hspt-v3-review-decisions.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)});document.getElementById('print')?.addEventListener('click',()=>{document.querySelectorAll('details.answers').forEach(d=>d.open=true);window.print()});if(document.getElementById('progress'))refresh();'''
def shell(title,body,data=None):
 extra='' if data is None else '<script id="review-data" type="application/json">'+json.dumps(data,ensure_ascii=False).replace('<','\\u003c')+'</script><script>'+JS+'</script>'
 return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+E(title)+'</title><style>'+CSS+'</style></head><body><main>'+body+'</main>'+extra+'</body></html>'
def controls():return '<div class="toolbar no-print"><label>Your name<br><input id="reviewer" autocomplete="name" placeholder="Reviewer name"></label><button id="export">Export review decisions</button><button class="secondary" id="print">Print questions and answers</button><span id="progress" class="progress"></span></div>'
def question_section(section,qs,reviewable):
 h=[f'<section class="section-cover" id="{section}"><div class="eyebrow">{E(LABELS[section])} · revision 3</div><h2>{len(qs)} questions</h2>'];md=[f'# {LABELS[section]} — {len(qs)} questions'];current=None
 for n,q in enumerate(qs,1):
  if q.get('passageId') and q['passageId']!=current:
   current=q['passageId'];p=passages[current]
   h.append('<article class="passage"><h3>'+E(p['title'])+'</h3><p class="meta">Original '+E(p['genre'])+' · '+str(sum(len(x.split()) for x in p['paragraphs']))+' words</p>')
   md+=['',f'## {p["title"]}']
   for j,para in enumerate(p['paragraphs'],1):h.append(f'<p><span class="meta">[{j}]</span> {E(para)}</p>');md.append(f'[{j}] {para}')
   h.append('</article>')
  h.append(f'<article class="card" id="{q["id"]}"><p class="meta">{q["id"]} · {E(q["skill"].replace("_"," "))} · provisional level {q["difficulty"]}</p><h3>{n}. {E(q["stem"])}</h3>');md+=['',f'### {n}. {q["id"]}',q['stem']]
  if q.get('diagram'):
   svg=(OUT/q['diagram']['file']).read_text();h.extend([svg,'<p class="figure-note">Use the labels; figure not drawn to scale.</p>']);md+=[svg,'Use the labels; figure not drawn to scale.']
  h.append('<ol class="choices">'+''.join('<li>'+E(c)+'</li>' for c in q['choices'])+'</ol>');md += [f'{"ABCD"[i]}. {c}' for i,c in enumerate(q['choices'])]
  if reviewable:h.append(f'<div class="review-controls no-print"><label>Decision<select data-decision="{q["id"]}" aria-label="Decision for {q["id"]}"><option value="pending">Not reviewed</option><option value="approve">Approve</option><option value="revise">Needs revision</option><option value="reject">Reject</option></select></label><label>Notes<textarea data-notes="{q["id"]}" aria-label="Notes for {q["id"]}" placeholder="Clarity, answer choices, explanation, difficulty, or layout"></textarea></label></div>')
  h.append('</article>')
 h.append('</section>');return ''.join(h),'\n\n'.join(md)
def answers(section,qs):
 h=[f'<h2>{LABELS[section]} — answer guide</h2>'];md=[f'# {LABELS[section]} — answer guide']
 for n,q in enumerate(qs,1):
  g=q['guide'];correct=q['choices']['ABCD'.index(g['correctChoiceId'])];ev=' Supporting paragraphs: '+', '.join(map(str,q['evidenceParagraphs']))+'.' if q.get('evidenceParagraphs') else ''
  h.append(f'<div class="answer"><h3>{n}. {q["id"]} — {g["correctChoiceId"]}</h3><p><strong>{E(correct)}</strong></p><p>{E(g["explanation"]+ev)}</p><p><strong>Tip:</strong> {E(g["shortcut"])}</p></div>')
  md.extend([f'## {n}. {q["id"]} — {g["correctChoiceId"]}',correct,g['explanation']+ev,'Tip: '+g['shortcut']])
 return ''.join(h),'\n\n'.join(md)
INTRO='<p class="summary">Solve each question before opening the answer guide. Then check the answer, explanation, distractors, clarity, difficulty, and layout. Select Approve, Needs revision, or Reject, and add any notes.</p><p class="notice">Human review is pending. Your decisions stay in this browser until you export them. This packet is a review selection, not a timed exam. Student timing and actual iPad checks remain pending.</p>'
chosen={};manifests={}
for s,b in banks.items():
 qs,m=sample(s,b['questions']);chosen[s]=qs;manifests[s]=m
 (REVIEW/f'{s}-sample.json').write_text(json.dumps(m,indent=2)+'\n')
 decisions={'bankSha256':m['bankSha256'],'passageSha256':m['passageSha256'],'assetHashes':m['assetHashes'],'policy':POLICY,'decisions':[{'id':q['id'],'decision':'pending','reviewer':None,'date':None,'notes':''} for q in qs]}
 f=REVIEW/f'{s}-decisions.json'
 if f.exists():
  prior=json.loads(f.read_text())
  if any(prior.get(k)!=decisions.get(k) for k in ['bankSha256','passageSha256','assetHashes','policy']) or [x['id'] for x in prior['decisions']]!=[x['id'] for x in decisions['decisions']]:
   archive=REVIEW/(s+'-decisions.superseded-'+hashfile(f)[:12]+'.json')
   if not archive.exists():archive.write_bytes(f.read_bytes())
   f.write_text(json.dumps(decisions,indent=2)+'\n')
 else:f.write_text(json.dumps(decisions,indent=2)+'\n')
 for count,items in [(20,qs),(100,b['questions'])]:
  h,md=question_section(s,items,count==20);ans,amd=answers(s,items)
  packet_hash=hashlib.sha256((json.dumps(m,sort_keys=True)+str(count)).encode()).hexdigest()
  data={'packetHash':packet_hash,'policy':POLICY,'manifests':{s:m},'items':[{'id':q['id'],'section':s} for q in items]} if count==20 else None
  body='<nav><a href="index.html">All sections</a><a href="#answers">Answer guide</a></nav><h1>'+E(LABELS[s])+'</h1>'+INTRO+(controls() if count==20 else '')+h+'<details class="answers" id="answers"><summary>Open the separate answer guide</summary>'+ans+'</details>'
  (REVIEW/f'{s}-{count}.html').write_text(shell(f'{LABELS[s]} — {count} questions, revision 3',body,data))
  (REVIEW/f'{s}-{count}.md').write_text(md+'\n\n---\n\n'+amd+'\n')
sections=[];guides=[];mds=[];amds=[]
for s in banks:
 h,md=question_section(s,chosen[s],True);a,amd=answers(s,chosen[s]);sections.append(h);guides.append(a);mds.append(md);amds.append(amd)
packet_hash=hashlib.sha256(json.dumps(manifests,sort_keys=True).encode()).hexdigest()
data={'packetHash':packet_hash,'policy':POLICY,'manifests':manifests,'items':[{'id':q['id'],'section':s} for s in banks for q in chosen[s]]}
body='<div class="eyebrow">HSPT question bank review · revision 3</div><h1>Your 80-question review packet</h1><p>20 questions from each revised 100-question bank.</p><nav>'+''.join(f'<a href="#{s}">{LABELS[s]}</a>' for s in banks)+'<a href="#answers">Answer guides</a></nav>'+INTRO+controls()+''.join(sections)+'<details class="answers" id="answers"><summary>Open all four answer guides</summary>'+''.join(guides)+'</details>'
(REVIEW/'all-sections-80.html').write_text(shell('HSPT — 80-question review packet',body,data))
(REVIEW/'all-sections-80.md').write_text('# HSPT — revised review packet\n\n20 questions per section. Human review pending.\n\n'+'\n\n'.join(mds)+'\n\n---\n\n# Separate answer guides\n\n'+'\n\n'.join(amds)+'\n')
intro='<div class="eyebrow">HSPT · revised banks · v3</div><h1>Ready for your review</h1><p class="summary">400 revised questions. Four fixed samples of 20. Original figures appear directly in the packets, and each answer guide is separate from the questions.</p><p><a href="all-sections-80.html">Open the combined 80-question review packet →</a></p><div class="grid">'
for s in banks:intro+=f'<article class="card"><h2>{LABELS[s]}</h2><p><a href="{s}-20.html">Review 20 questions</a></p><p><a href="{s}-100.html">Browse the complete 100</a></p></article>'
intro+='</div><h2>What changed</h2><ul class="short-list"><li>Reading: 64 comprehension questions across eight varied passages, plus 36 standalone vocabulary questions.</li><li>Language: 66 error-detection sets, including genuine no-error cases; 17 spelling and 17 composition questions.</li><li>Mathematics: 16 original figures and 12 conceptual questions within the 100-item bank.</li><li>Verbal: closer distractors, more varied reasoning, and renewed answer checks.</li></ul><p class="notice">The live Quantitative bank is unchanged. Approval, actual iPad review, and app integration remain pending. No publication or deployment has occurred.</p><p><a href="../REPORT.md">Checks and limitations</a> · <a href="all-sections-80.md">Markdown version</a></p>'
(REVIEW/'index.html').write_text(shell('HSPT — revised question banks',intro))
print(json.dumps({s:{'count':len(chosen[s]),'ids':m['questionIds'],'formats':m['formats']} for s,m in manifests.items()},indent=2))
