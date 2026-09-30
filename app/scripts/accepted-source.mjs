// Source imports use the Phase IV 20-per-section policy, within the existing publisher.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {validateQuestion} from '../src/domain/contentSchema.mjs';
export const sourcePolicy='source-import-20-per-section-v1';
const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const insist=(ok,message)=>{if(!ok)throw new Error(message);};
export function acceptedSource(dir,reviewDir,root){
 const policy=read(path.join(dir,'source-import.json'));
 insist(policy.policy===sourcePolicy,'Unsupported source-import policy');
 const bank=read(path.join(dir,'bank.json')),sha=hash(path.join(dir,'bank.json'));
 insist(Array.isArray(bank)&&bank.length>0,'No checked source questions');
 const audit=read(path.join(dir,'checks.json')),manifest=read(path.join(reviewDir,'manifest.json')),decisions=read(path.join(reviewDir,'decisions.json'));
 insist([audit,manifest,decisions].every(x=>x.bankSha256===sha),'Stale source-import evidence');
 insist(manifest.policy===sourcePolicy&&manifest.checksSha256===hash(path.join(dir,'checks.json'))&&manifest.policySha256===hash(path.join(dir,'source-import.json')),'Source-import policy or checks changed');
 insist(decisions.manifestSha256===hash(path.join(reviewDir,'manifest.json')),'Source review manifest changed');
 insist(audit.calibration==='not_applicable_source_import','Source self-calibration must be explicitly exempted');
 const ids=new Set(bank.map(q=>q.id));insist(ids.size===bank.length,'Duplicate source IDs');
 insist(Array.isArray(audit.items)&&audit.items.length===bank.length&&new Set(audit.items.map(x=>x.id)).size===bank.length,'Incomplete source checks');
 for(const q of bank){validateQuestion(q);const item=audit.items.find(x=>x.id===q.id);insist(item&&['transcription','correctness','consistency','visual','duplicates'].every(k=>item[k]==='pass'),'Unresolved source checks for '+q.id);insist(typeof item.method==='string'&&item.method.trim()&&typeof item.notes==='string'&&item.notes.trim(),'Missing independent review method for '+q.id);insist(q.provenance?.sourceForm&&q.provenance?.sourceQuestion&&q.provenance?.sourceLocator,'Missing source locator for '+q.id);}
 const sampled=manifest.sample.map(x=>x.id);insist(new Set(sampled).size===sampled.length&&sampled.every(id=>ids.has(id)),'Invalid source sample IDs');
 for(const section of ['verbal','quantitative','reading','mathematics','language']){
  const items=bank.filter(q=>q.section===section);insist(items.length>=20,'Source import requires at least 20 checked items per section');
  const sample=bank.filter(q=>q.section===section&&sampled.includes(q.id));insist(sample.length===20,'Source review requires 20 questions per section');
  for(const form of new Set(items.map(q=>q.provenance.sourceForm)))insist(sample.some(q=>q.provenance.sourceForm===form),'Source sample omits '+section+' / '+form);
 }
 insist(decisions.reviewer?.trim()&&Number.isFinite(Date.parse(decisions.date))&&decisions.items?.length===100&&new Set(decisions.items.map(x=>x.id)).size===100&&decisions.items.every(x=>sampled.includes(x.id)&&x.decision==='approve'),'Human source sample approval is incomplete');
 const inventory=read(path.join(dir,'inventory.json'));insist(policy.inventorySha256===hash(path.join(dir,'inventory.json'))&&inventory.items.length===1192&&new Set(inventory.items.map(x=>x.id)).size===1192,'Source inventory is incomplete or changed');
 const imported=new Set();for(const item of inventory.items){insist(['included','duplicate','blocked'].includes(item.disposition),'Unreconciled source item '+item.id);if(item.disposition==='included'){insist(ids.has(item.id),'Included source item missing from bank');imported.add(item.id);}else insist(item.reason?.trim()&&(item.disposition!=='duplicate'||item.canonicalId),'Missing source disposition reason');}
 insist(imported.size===bank.length&&[...ids].every(id=>imported.has(id)),'Bank and import inventory differ');
 insist(policy.distribution?.status==='permitted'&&policy.distribution?.basis?.trim(),'Record source distribution eligibility before release');
 return {bank,sha,reviewed:new Set(sampled),evidence:{batchDir:path.relative(root,dir),reviewDir:path.relative(root,reviewDir),bankSha256:sha,decisionsSha256:hash(path.join(reviewDir,'decisions.json'))}};
}
