// Run only after normalization and independent checks; never produces approval decisions.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {sourcePolicy} from './accepted-source.mjs';
import {validateQuestion} from '../src/domain/contentSchema.mjs';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const dir=path.resolve(root,process.argv[2]??'content/staging/source-import-v1');
const out=path.resolve(root,process.argv[3]??'content/review/source-import-v1');
const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
try{
 const bank=read(path.join(dir,'bank.json')),checks=read(path.join(dir,'checks.json')),sha=hash(path.join(dir,'bank.json'));
 if(checks.bankSha256!==sha||checks.items.length!==bank.length||new Set(checks.items.map(x=>x.id)).size!==bank.length||bank.some(q=>{validateQuestion(q);const c=checks.items.find(x=>x.id===q.id);return !c||['transcription','correctness','consistency','visual','duplicates'].some(k=>c[k]!=='pass');}))throw new Error('Complete all-item checks before generating the user review sample.');
 if(fs.existsSync(out))throw new Error('Review folder already exists. Preserve decisions and use a new revision folder.');
 const sections=['verbal','quantitative','reading','mathematics','language'],packets=[],sample=[];
 for(const section of sections){
  const pool=bank.filter(q=>q.section===section);if(pool.length<20)throw new Error('Fewer than 20 checked questions in '+section);
  const rank=q=>crypto.createHash('sha256').update(sha+q.id).digest('hex');
  const sorted=[...pool].sort((a,b)=>rank(a).localeCompare(rank(b)));const chosen=[];
  const add=q=>{if(q&&!chosen.includes(q))chosen.push(q);};
  for(const form of [...new Set(pool.map(q=>q.provenance.sourceForm))].sort())add(sorted.find(q=>q.provenance.sourceForm===form));
  for(const field of ['format','skill','difficulty'])for(const value of [...new Set(pool.map(q=>q[field]))].sort())if(chosen.length<20&&!chosen.some(q=>q[field]===value))add(sorted.find(q=>q[field]===value));
  for(const q of sorted.filter(q=>q.image||q.diagram||checks.items.find(x=>x.id===q.id)?.risk==='high'))if(chosen.length<20)add(q);
  for(const q of sorted)if(chosen.length<20)add(q);
  if(chosen.length!==20)throw new Error('Invalid sample');
  sample.push(...chosen.map(q=>({id:q.id,section,sourceForm:q.provenance.sourceForm})));
  let text=`# ${section} — 20-question source-import review sample\n\nThese 20 questions sample the full checked ${pool.length}-question section import. Approval covers all checked items, not just these 20. Solve first, then consult the separate answer section.\n\n`;
  for(const [i,q] of chosen.entries()){
   text+=`## ${i+1}. ${q.id}\n\nSource: ${q.provenance.sourceForm}, ${q.provenance.sourceLocator}, question ${q.provenance.sourceQuestion}.\n\n`;
   if(q.passage)text+=`### ${q.passage.title}\n\n${q.passage.text}\n\n`;
   text+=q.stem+'\n\n';
   if(q.image)text+=`<img alt=${JSON.stringify(q.image.alt)} src=${JSON.stringify(q.image.dataUrl)} />\n\n`;
   if(q.diagram)text+=q.diagram.svg+'\n\n';
   text+=q.choices.map((x,i)=>`${'ABCD'[i]}. ${x}`).join('\n\n')+'\n\nDecision: approve / revise / reject. Notes: ______\n\n';
  }
  text+='---\n\n# Answers and explanations\n\n'+chosen.map((q,i)=>`## ${i+1}. ${q.id} — ${q.guide.correctChoiceId}\n\n${q.guide.explanation}\n\n${q.guide.shortcut??''}`).join('\n\n');packets.push([section+'.md',text]);
 }
 const manifest={policy:sourcePolicy,bankSha256:sha,checksSha256:hash(path.join(dir,'checks.json')),policySha256:hash(path.join(dir,'source-import.json')),sample};
 fs.mkdirSync(out,{recursive:true});for(const [name,text] of packets)fs.writeFileSync(path.join(out,name),text);
 fs.writeFileSync(path.join(out,'manifest.json'),JSON.stringify(manifest,null,2)+'\n');
 fs.writeFileSync(path.join(out,'decisions.json'),JSON.stringify({bankSha256:sha,manifestSha256:hash(path.join(out,'manifest.json')),reviewer:'',date:'',items:sample.map(x=>({id:x.id,decision:'pending',notes:''}))},null,2)+'\n');
 console.log('Created five 20-question review packets. User approval is still pending.');
}catch(e){console.error(e.message);process.exitCode=1;}
