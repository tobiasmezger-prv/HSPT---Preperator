#!/usr/bin/env node
// Owner-only file workflow. No credentials, publishing API, or child data.
import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';import {fileURLToPath} from 'node:url';
import {validateBank,validateManifest} from '../src/domain/contentSchema.mjs';
const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const hash=s=>crypto.createHash('sha256').update(s).digest('hex');const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));const digest=p=>hash(fs.readFileSync(p));const fail=s=>{throw new Error(s);};
const publicDir=path.join(ROOT,'public');const content=path.join(publicDir,'content');const records=path.join(ROOT,'content/releases');
function target(url){if(!/^\/content\/banks\/[\w-]+\.json$/.test(url))fail('Unsafe manifest target');return path.join(publicDir,url);}
export function validateRelease(m){validateManifest(m);const p=target(m.bankUrl);if(!fs.existsSync(p))fail('Manifest bank is missing');if(digest(p)!==m.checksum)fail('Checksum mismatch');const b=read(p);validateBank(b,m);return b;}
function accepted(batchDir,reviewDir){
 const bankPath=path.join(batchDir,'bank.json'),sha=digest(bankPath),bank=read(bankPath);if(!Array.isArray(bank)||bank.length%100!==0||!bank.length)fail('Accepted batches must contain complete hundreds');
 const math=read(path.join(batchDir,'validation.json')),audit=read(path.join(batchDir,'item-audit.json')),editorial=read(path.join(batchDir,'editorial-review.json')),visual=read(path.join(batchDir,'visual-review.json')),overlap=read(path.join(batchDir,'overlap-log.json')),manifest=read(path.join(reviewDir,'manifest.json')),decisions=read(path.join(reviewDir,'decisions.json'));
 if([math,audit,visual,overlap,manifest,decisions].some(x=>x.bankSha256!==sha)||editorial.reviewedBankSha256!==sha)fail('Stale acceptance evidence');
 for(const [field,file] of [['mathSha256','validation.json'],['auditSha256','item-audit.json'],['editorialSha256','editorial-review.json'],['visualSha256','visual-review.json']])if(manifest[field]!==digest(path.join(batchDir,file)))fail('Evidence checksum mismatch');
 if(decisions.manifestSha256!==digest(path.join(reviewDir,'manifest.json')))fail('Review manifest mismatch');
 const same=(xs)=>xs.length===bank.length&&new Set(xs).size===bank.length&&bank.every(q=>xs.includes(q.id));
 if(!same(math.checkedItems.map(q=>q.id))||math.checkedItems.some(q=>q.status!=='pass')||!same(audit.items.map(q=>q.id)))fail('Incomplete mathematical/editorial checks');
 const ids=manifest.sample.map(q=>q.id);if(ids.length!==bank.length/5||new Set(ids).size!==ids.length||!ids.every(id=>bank.some(q=>q.id===id)))fail('Invalid review sample');
 if(!decisions.reviewer||!decisions.date||decisions.items.length!==ids.length||new Set(decisions.items.map(x=>x.id)).size!==ids.length||!decisions.items.every(x=>ids.includes(x.id)&&x.decision==='approve'))fail('Human sample approval is incomplete');
 if(overlap.unresolvedIdentifiedMatches.length)fail('Unresolved source overlap');
 for(const q of bank)if(q.visual){const file=path.join(batchDir,'assets',q.id+'.svg');if(visual.assets[q.id+'.svg']!==digest(file))fail('Diagram inspection is stale');}
 return {bank,sha,reviewed:new Set(ids),evidence:{batchDir:path.relative(ROOT,batchDir),reviewDir:path.relative(ROOT,reviewDir),bankSha256:sha,decisionsSha256:digest(path.join(reviewDir,'decisions.json'))}};
}
function convert(q,batch,dir,revision){return {...q,revision,skill:q.format==='geometric_comparison'?'geometric_comparison':q.skill,reviewStatus:'sample_reviewed',acceptance:{batchId:path.basename(dir),batchStatus:'sample_reviewed',individualStatus:batch.reviewed.has(q.id)?'approved':'not_individually_reviewed'},diagram:q.visual?{svg:fs.readFileSync(path.join(dir,'assets',q.id+'.svg'),'utf8'),alt:q.visual.alt}:q.diagram};}
function contentKey(q){return JSON.stringify([q.section,q.skill,q.format,q.difficulty,q.stem,q.choices,q.guide,q.templateFamily,q.variantGroupId??null,q.diagram??null]);}
function immutable(file,text){if(fs.existsSync(file)&&fs.readFileSync(file,'utf8')!==text)fail('Immutable file already exists with different content: '+file);fs.mkdirSync(path.dirname(file),{recursive:true});if(!fs.existsSync(file))fs.writeFileSync(file,text);}
function proposal(id){if(!/^[\w-]+$/.test(id??''))fail('Supply --release with a safe release ID');return path.join(records,id+'.manifest.json');}
function authorize(m){const record=read(path.join(records,m.releaseId+'.receipt.json'));if(record.bankChecksum!==m.checksum)fail('Release receipt mismatch');for(const e of record.acceptedBatches){const a=accepted(path.join(ROOT,e.batchDir),path.join(ROOT,e.reviewDir));if(a.sha!==e.bankSha256||digest(path.join(ROOT,e.reviewDir,'decisions.json'))!==e.decisionsSha256)fail('Accepted source changed');}if(!record.acceptedBatches.length)fail('No accepted batch evidence');return record;}
const args=process.argv.slice(2),command=args.shift(),options={};for(let i=0;i<args.length;i+=2){if(!args[i].startsWith('--')||args[i+1]===undefined)fail('Use --option value');options[args[i].slice(2)]=args[i+1];}
try{
 if(command==='build'){
  const id=options.release,out=proposal(id);const dir=path.resolve(ROOT,options.batch??''),review=path.resolve(ROOT,options.review??'');const batch=accepted(dir,review);
  const currentFile=path.join(content,'manifest.json');const current=fs.existsSync(currentFile)?read(currentFile):null;const prior=current?validateRelease(current):{questions:[]};const previous=current?authorize(current):null;
  const map=new Map(prior.questions.map(q=>[q.id,q]));const revisions=new Set((options.revise??'').split(',').filter(Boolean)),retire=new Set((options.retire??'').split(',').filter(Boolean));let added=0,revised=0;
  for(const q of batch.bank){const old=map.get(q.id);let next=convert(q,batch,dir,q.revision??1);if(retire.has(q.id))continue;if(old){if(contentKey(next)===contentKey(old))continue;if(!revisions.has(q.id)||q.revision!==old.revision+1)fail(`Collision ${q.id}: explicit --revise and revision ${old.revision+1} required`);revised++;}else{if(next.revision!==1)fail('New IDs start at revision 1');added++;}map.set(q.id,next);}
  for(const id of revisions)if(!prior.questions.some(q=>q.id===id)||!batch.bank.some(q=>q.id===id))fail('Unknown revision ID '+id);
  for(const id of retire)if(!map.delete(id))fail('Unknown retirement '+id);
  const bank={schemaVersion:1,releaseId:id,questions:[...map.values()]};const text=JSON.stringify(bank,null,2)+'\n';const manifest={schemaVersion:1,releaseId:id,publishedAt:new Date().toISOString(),bankUrl:`/content/banks/${id}.json`,questionCount:bank.questions.length,checksum:hash(text)};validateBank(bank,manifest);
  // Refuse duplicate immutable names before writing anything.
  if(fs.existsSync(out)||fs.existsSync(target(manifest.bankUrl)))fail('Release ID already used. Choose a new immutable ID.');
  const sources=[...(previous?.acceptedBatches??[]),batch.evidence];const receipt={releaseId:id,bankChecksum:manifest.checksum,acceptedBatches:[...new Map(sources.map(e=>[e.bankSha256,e])).values()],changes:{added,revised,retired:retire.size,total:bank.questions.length}};
  immutable(target(manifest.bankUrl),text);immutable(out,JSON.stringify(manifest,null,2)+'\n');immutable(path.join(records,id+'.receipt.json'),JSON.stringify(receipt,null,2)+'\n');console.log(JSON.stringify(receipt.changes));console.log('Candidate built. Preview/publish require explicit activation; existing manifest unchanged.');
 }else if(command==='validate'){
  const file=options.release?proposal(options.release):path.join(content,'manifest.json');const m=read(file);const b=validateRelease(m);authorize(m);for(const file of fs.readdirSync(records).filter(x=>x.endsWith('.manifest.json'))){const retained=read(path.join(records,file));validateRelease(retained);authorize(retained);}console.log(`Valid accepted release ${m.releaseId}: ${b.questions.length} questions`);
 }else if(['preview','publish','rollback'].includes(command)){
  const m=read(proposal(options.release));validateRelease(m);authorize(m);fs.mkdirSync(content,{recursive:true});fs.writeFileSync(path.join(content,'manifest.json.tmp'),JSON.stringify(m,null,2)+'\n');fs.renameSync(path.join(content,'manifest.json.tmp'),path.join(content,'manifest.json'));console.log(`${command}: local manifest now points to ${m.releaseId}. No remote deployment performed. Commit this change on your preview/production branch and deploy via GitHub → Vercel.`);
 }else fail('Usage: node scripts/content-release.mjs build|validate|preview|publish|rollback --release ID [--batch content/staging/BATCH --review content/review/BATCH --revise IDs --retire IDs]');
}catch(e){console.error(e.message);process.exitCode=1;}
