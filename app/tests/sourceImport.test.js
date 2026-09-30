import {it,expect} from 'vitest';
import fs from 'node:fs';import path from 'node:path';import os from 'node:os';import crypto from 'node:crypto';import {spawnSync} from 'node:child_process';
import {acceptedSource,sourcePolicy} from '../scripts/accepted-source.mjs';
import {validateBank} from '../src/domain/contentSchema.mjs';
const app=path.resolve(import.meta.dirname,'..');
const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
it('accepts all checked source questions after 100 sample approvals and rejects stale or incomplete evidence',()=>{
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),'hspt-source-test-')),review=path.join(dir,'review');
 try{
  const current=JSON.parse(fs.readFileSync(path.join(app,'public/content/banks/all-sections-v0002.json'),'utf8'));
  const sections=['verbal','quantitative','reading','mathematics','language'];
  const bank=sections.flatMap(section=>current.questions.filter(q=>q.section===section).slice(0,40).map((q,i)=>({...q,provenance:{origin:'test fixture only',sourceForm:['gables-1','gables-2','gables-3','barrons-1'][i%4],sourceQuestion:i+1,sourceLocator:'Test fixture page'}})));
  const write=(name,x)=>fs.writeFileSync(path.join(dir,name),JSON.stringify(x,null,2)+'\n');
  write('bank.json',bank);const sha=hash(path.join(dir,'bank.json'));
  write('inventory.json',{items:[...bank.map(q=>({id:q.id,disposition:'included'})),...Array.from({length:992},(_,i)=>({id:'blocked-'+i,disposition:'blocked',reason:'Synthetic blocked test fixture'}))]});
  write('source-import.json',{policy:sourcePolicy,inventorySha256:hash(path.join(dir,'inventory.json')),distribution:{status:'permitted',basis:'Synthetic test fixtures only'}});
  write('checks.json',{bankSha256:sha,calibration:'not_applicable_source_import',items:bank.map(q=>({id:q.id,transcription:'pass',correctness:'pass',consistency:'pass',visual:'pass',duplicates:'pass',method:'Synthetic acceptance-gate test',notes:'Not a content approval record'}))});
  const result=spawnSync(process.execPath,[path.join(app,'scripts/prepare-source-review.mjs'),dir,review],{encoding:'utf8'});expect(result.status,result.stderr).toBe(0);
  expect(()=>acceptedSource(dir,review,app)).toThrow('approval is incomplete');
  const decisions=JSON.parse(fs.readFileSync(path.join(review,'decisions.json'),'utf8'));expect(decisions.items).toHaveLength(100);decisions.reviewer='Synthetic test';decisions.date='2026-09-28';decisions.items.forEach(x=>x.decision='approve');fs.writeFileSync(path.join(review,'decisions.json'),JSON.stringify(decisions));
  const accepted=acceptedSource(dir,review,app);expect(accepted.bank).toHaveLength(200);expect(accepted.reviewed.size).toBe(100);
  fs.appendFileSync(path.join(dir,'checks.json'),' ');expect(()=>acceptedSource(dir,review,app)).toThrow('checks changed');
 }finally{fs.rmSync(dir,{recursive:true,force:true});}
});
it('checks section index counts against the complete bank',()=>{
 const bank=JSON.parse(fs.readFileSync(path.join(app,'public/content/banks/all-sections-v0002.json'),'utf8')),m=JSON.parse(fs.readFileSync(path.join(app,'content/releases/all-sections-v0002.manifest.json'),'utf8'));const sectionCounts={verbal:100,quantitative:100,reading:100,mathematics:100,language:100};expect(()=>validateBank(bank,{...m,sectionCounts})).not.toThrow();expect(()=>validateBank(bank,{...m,sectionCounts:{...sectionCounts,verbal:20}})).toThrow('Section index');
});
