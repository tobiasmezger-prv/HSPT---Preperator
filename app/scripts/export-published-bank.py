"""Export owner-facing index and review packets from the exact active release."""
from pathlib import Path
import json,html,collections
A=Path(__file__).resolve().parents[1];ROOT=A.parent
m=json.loads((A/'public/content/manifest.json').read_text());q=json.loads((A/'public'/m['bankUrl'].lstrip('/')).read_text())['questions'];review=A/'content/review/source-import-v1';ids={s['id'] for s in json.loads((review/'manifest.json').read_text())['sample']};E=A/'content/staging/source-import-v1/evidence'
css='''*{box-sizing:border-box}body{margin:0;background:#f5f5f0;color:#173541;font:17px/1.65 -apple-system,BlinkMacSystemFont,Segoe UI,sans-serif}main{max-width:960px;margin:auto;padding:30px 20px}article{background:white;border:1px solid #d9e2df;border-radius:16px;padding:24px;margin:20px 0}.meta{font-size:13px;color:#536c66}.stem{font-size:20px;white-space:pre-line}.passage{background:#eef3ed;padding:18px;white-space:pre-line}img{display:block;max-width:100%;max-height:350px;margin:18px auto}a{color:#16686b}select,input{font:inherit;padding:9px;max-width:100%;border:1px solid #b8c9c5;border-radius:8px}.tools{display:flex;gap:10px;flex-wrap:wrap;position:sticky;top:0;background:#f5f5f0;padding:12px 0}li{margin:8px 0}.guide{font-size:15px;margin-top:15px}summary{cursor:pointer;font-weight:600}h1{line-height:1.25}@media(max-width:600px){main{padding:18px 12px}article{padding:20px 16px}.tools{position:static}}'''
def card(x):
 p=x.get('passage');s='<article id="'+x['id']+'" data-section="'+x['section']+'" data-source="'+x.get('provenance',{}).get('sourceForm','original')+'"><div class="meta">'+html.escape(x['id']+' · '+x['section'])+'</div>'
 if p:s+='<details class="passage"><summary>'+html.escape(p['title'])+'</summary><p>'+html.escape(p['text'])+'</p></details>'
 s+='<p class="stem">'+html.escape(x['stem'])+'</p>'
 if x.get('diagram'):s+=x['diagram']['svg'].replace('<svg ','<svg style="display:block;max-width:100%;max-height:350px;margin:20px auto" ',1)
 s+='<ol type="A">'+''.join('<li>'+html.escape(c)+'</li>' for c in x['choices'])+'</ol><details class="guide"><summary>Answer and explanation</summary><p><b>'+x['guide']['correctChoiceId']+'.</b> '+html.escape(x['guide']['explanation'])+'</p></details></article>'
 return s
script='''const cards=[...document.querySelectorAll('article')];function filter(){const s=document.getElementById('section').value,source=document.getElementById('source').value,term=document.getElementById('search').value.toLowerCase();let count=0;for(const c of cards){c.hidden=!!((s&&c.dataset.section!==s)||(source&&c.dataset.source!==source)||!c.textContent.toLowerCase().includes(term));if(!c.hidden)count++}document.getElementById('count').textContent=count+' questions shown'}document.querySelectorAll('input,select').forEach(e=>e.addEventListener('input',filter));const p=new URLSearchParams(location.search);for(const key of ['source','section'])if(p.has(key))document.getElementById(key).value=p.get(key);filter();'''
def page(title,items):
 tools='<div class="tools"><select id="section" aria-label="Section"><option value="">All sections</option>'+''.join('<option>'+s+'</option>' for s in m['sectionCounts'])+'</select><select id="source" aria-label="Source"><option value="">All sources</option>'+''.join('<option>'+s+'</option>' for s in ['original','gables-1','gables-2','gables-3','barrons-1'])+'</select><input id="search" aria-label="Search questions" placeholder="Search questions or ID"></div><p id="count"></p>'
 return '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+title+'</title><style>'+css+'</style><main><h1>'+title+'</h1><p>Phase IV · '+m['releaseId']+' · Approved sample review and authorized source import. Individual text and recreated diagrams. Original 500 questions preserved; 1,191 source additions and one recorded duplicate.</p>'+tools+''.join(card(x) for x in items)+'<script>'+script+'</script></main></html>'
(review/'all-questions.html').write_text(page('HSPT Phase IV · 1,691 questions',q))
for s in m['sectionCounts']:
 items=[x for x in q if x['id'] in ids and x['section']==s];assert len(items)==20
 (review/(s+'.html')).write_text(page(s.title()+' · 20 approved source samples',items))
 text=['# '+s.title()+' — approved source samples','Same previously approved 20-item sample, now in the active Phase IV release. Subsequent authorized normalization changes are logged in integration-edits.json.']
 for x in items:
  text+=['## '+x['id']]
  if x.get('passage'):text+=[x['passage']['title'],x['passage']['text']]
  text+=[x['stem']]
  if x.get('diagram'):text+=[x['diagram']['svg']]
  text+=['\n'.join('- **'+chr(65+i)+'.** '+c for i,c in enumerate(x['choices'])),'Answer: '+x['guide']['correctChoiceId']+'. '+x['guide']['explanation']]
 (review/(s+'.md')).write_text('\n\n'.join(text))
(review/'index.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Phase IV question index</title><style>'+css+'</style><main><h1>Phase IV question index</h1><p>Active release: '+m['releaseId']+' · 1,691 questions.</p><ul>'+''.join('<li>'+s.title()+': '+str(n)+' available · <a href="all-questions.html?section='+s+'">Browse section</a> · <a href="'+s+'.html">20 approved source samples</a></li>' for s,n in m['sectionCounts'].items())+'</ul><p><a href="all-questions.html">Browse all 1,691 questions</a></p><p>1,191 source questions appended to the original 500. One equivalent source question is represented by its canonical record. All 1,192 source positions are accounted for.</p></main></html>')
text='# Phase IV question bank index\n\nActive release: **'+m['releaseId']+'** · **1,691 questions**.\n\n| Section | Existing | Added | Available | Full section | Five-minute burst |\n|---|---:|---:|---:|---|---:|\n'
presets={'verbal':('60 / 18 min',17),'quantitative':('52 / 30 min',9),'reading':('62 / 25 min',12),'mathematics':('64 / 45 min',7),'language':('60 / 25 min',12)}
for s,n in m['sectionCounts'].items():text+=f'| {s.title()} | 100 | {n-100} | {n} | {presets[s][0]} | {presets[s][1]} |\n'
text+='\nFull test: 298 questions, 143 timed minutes.\n\n- [Browse the full bank and section samples](review/source-import-v1/index.html)\n- [Active app index](../public/content/manifest.json)\n- [Immutable cumulative bank](../public/content/banks/all-sections-v0003.json)\n- [Publication receipt](releases/all-sections-v0003.receipt.json)\n- [Source inventory and duplicate mapping](staging/source-import-v1/inventory.json)\n- [Recorded sample approval and integration authorization](review/source-import-v1/decisions.json)\n\nAll 500 existing records are unchanged. All 1,192 source positions are reconciled: 1,191 additions, one semantic duplicate (Gables 3 Q83 → Gables 2 Q66), zero blocked. Source difficulty labels are editorial estimates, not a calibration against Gables itself. Browser progress and cooldowns remain local; prior sessions retain their question snapshots. This release was activated locally; GitHub/Vercel deployment is separate.\n'
(A/'content/QUESTION_BANK_INDEX.md').write_text(text)
# Record candidate decisions without overstating an automated proof of semantic uniqueness.
candidates=json.loads((E/'duplicate-candidates.json').read_text())
for c in candidates:
 if {c['a'],c['b']}=={'gables-2-066','gables-3-083'}:c.update(decision='merge',canonicalId='gables-2-066',reason='Same computation 5 cubed divided by 5 and same answer, with superficial prompt/distractor changes.')
 elif c['choicesA']==['true','false','uncertain']:c.update(decision='retain',reason='Shared logical-reasoning task and response vocabulary; different named premises/context. Retained as practice variants, not claimed to teach a new reasoning principle.')
 else:c.update(decision='retain',reason='Compared stems: differing quantities, operations, or mathematical concept. Shared response numbers do not make these the same question.')
(E/'duplicate-review.json').write_text(json.dumps({'method':'Normalized prompt/choice comparisons against all source items and the existing release; 416 candidates, of which 411 share true/false/uncertain response boilerplate. Remaining five inspected; one same-computation duplicate merged. This is an editorial deduplication pass, not a proof of absence of all conceptual overlap.','items':candidates},ensure_ascii=False,indent=2))
print('Exported live bank index and five matching 20-question review packets.')
