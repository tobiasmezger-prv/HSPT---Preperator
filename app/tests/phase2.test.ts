import 'fake-indexeddb/auto';
import {beforeEach,describe,it,expect,vi} from 'vitest';
import {openDB,deleteDB} from 'idb';
import {loadProgress,loadBank,installBank,beginPractice,saveSession,mergeProgress,resetProgress} from '../src/domain/storage';
import {checkForBank,sha256} from '../src/domain/bankDelivery';
import {availableQuestions,pickFresh,type Exposure} from '../src/domain/freshSelection';
import {parseBackup} from '../src/domain/backup';
import {validateBank,type Bank,type Manifest} from '../src/domain/contentSchema.mjs';
import {createSession,complete} from '../src/domain/session';
import {gradeSession} from '../src/domain/scoring';
import released from '../public/content/banks/quantitative-v0001.json';
import manifest from '../content/releases/quantitative-v0001.manifest.json';
import type {Question,Session} from '../src/domain/types';
const bank=released as unknown as Bank;const m=manifest as Manifest;
const q=bank.questions;
async function release(id:string,questions:Question[]=q){const b={schemaVersion:1 as const,releaseId:id,questions};const text=JSON.stringify(b);return {bank:b,text,manifest:{...m,releaseId:id,bankUrl:`/content/banks/${id}.json`,checksum:await sha256(text),questionCount:questions.length}};}
const mockFetch=(r:Awaited<ReturnType<typeof release>>)=>vi.fn(async(url:any)=>new Response(url==='/content/manifest.json'?JSON.stringify(r.manifest):r.text)) as unknown as typeof fetch;
beforeEach(async()=>{await deleteDB('hspt-practice');});
describe('Phase II browser delivery and durable progress',()=>{
 it('migrates the original v1 database in place, preserving exact snapshots/deadlines and reconstructing exposure',async()=>{
  const db=await openDB('hspt-practice',1,{upgrade(db){db.createObjectStore('sessions',{keyPath:'id'});}});const s=createSession(q.slice(0,10),'timed','mixed',1000);s.responses[q[0].id].answer='A';await db.put('sessions',s);db.close();const p=await loadProgress();expect(p.sessions).toEqual([s]);expect(p.exposures).toHaveLength(10);expect(p.exposures[0].encounterCount).toBe(1);expect(p.sessions[0].deadlineAt).toBe(301000);
 });
 it('installs a validated bank, then an expanded release and rollback without touching history',async()=>{
  const first=await release('one');await checkForBank(mockFetch(first));const session=await beginPractice('mixed','untimed',10,false,1000);await saveSession(complete(session,2000));
  const extra={...q[0],id:'new-question',stem:q[0].stem+' Find the next term.'};const next=await release('two',[...q,extra]);await checkForBank(mockFetch(next));expect((await loadBank())?.bank.questions).toHaveLength(101);expect(availableQuestions(next.bank.questions,'mixed',(await loadProgress()).exposures,(await loadProgress()).sessions,3000).some(x=>x.id==='new-question')).toBe(true);
  await checkForBank(mockFetch(first));expect((await loadBank())?.manifest.releaseId).toBe('one');expect((await loadProgress()).sessions).toHaveLength(1);expect((await loadProgress()).exposures).toHaveLength(10);
 });
 it('preserves the last bank on network, checksum, incompatible schema and invalid question failures',async()=>{
  await installBank({bank,manifest:m});
  await expect(checkForBank(vi.fn().mockRejectedValue(new Error('offline')))).rejects.toThrow();
  const bad=await release('bad');bad.text+=' ';await expect(checkForBank(mockFetch(bad))).rejects.toThrow('checksum');
  const incompatible=await release('incompatible');(incompatible.manifest as any).schemaVersion=9;await expect(checkForBank(mockFetch(incompatible))).rejects.toThrow('manifest');
  const invalid=await release('invalid',[{...q[0],choices:['a','a','b','c']}]);await expect(checkForBank(mockFetch(invalid))).rejects.toThrow('choices');
  expect((await loadBank())?.manifest).toEqual(m);
 });
 it('rolls back bank installation and session assignment on storage failure',async()=>{
  await installBank({bank,manifest:m});const next=await release('quota');const original=IDBObjectStore.prototype.put;
  const spy=vi.spyOn(IDBObjectStore.prototype,'put').mockImplementation(function(this:IDBObjectStore,value:any,key?:IDBValidKey){if(this.name==='meta')throw new DOMException('Full','QuotaExceededError');return key===undefined?original.call(this,value):original.call(this,value,key);});
  await expect(installBank(next)).rejects.toThrow('Full');spy.mockRestore();expect((await loadBank())?.manifest.releaseId).toBe(m.releaseId);
  const failExposure=vi.spyOn(IDBObjectStore.prototype,'put').mockImplementation(function(this:IDBObjectStore,value:any,key?:IDBValidKey){if(this.name==='exposures')throw new DOMException('Full','QuotaExceededError');return key===undefined?original.call(this,value):original.call(this,value,key);});
  await expect(beginPractice('mixed','timed',10)).rejects.toThrow('Full');failExposure.mockRestore();expect((await loadProgress()).sessions).toHaveLength(0);expect((await loadProgress()).exposures).toHaveLength(0);
 });
 it('rejects changed immutable content without switching the active release',async()=>{
  await installBank({bank,manifest:m});await expect(installBank({bank,manifest:{...m,checksum:'0'.repeat(64)}})).rejects.toThrow('immutable');expect((await loadBank())?.manifest.checksum).toBe(m.checksum);
 });
 it('rechecks state transactionally for simultaneous tab starts and counts all assignments',async()=>{
  await installBank({bank,manifest:m});const [a,b]=await Promise.all([beginPractice('mixed','timed',10,false,1000),beginPractice('mixed','timed',10,false,1001)]);expect(a.id).toBe(b.id);const p=await loadProgress();expect(p.sessions).toHaveLength(1);expect(p.exposures).toHaveLength(10);expect(p.exposures.every(e=>e.encounterCount===1)).toBe(true);
 });
 it('does not start or record exposure when stale requested size no longer fits',async()=>{
  await installBank({bank,manifest:m});for(let i=0;i<10;i++){const s=await beginPractice('mixed','untimed',10,false,1000+i);await saveSession(complete(s,2000+i));}await expect(beginPractice('mixed','untimed',10,false,3000)).rejects.toThrow('Available');expect((await loadProgress()).sessions).toHaveLength(10);expect((await loadProgress()).exposures).toHaveLength(100);const review=await beginPractice('mixed','untimed',10,true,3000);expect(review.practiceKind).toBe('review');
 });
 it('keeps in-progress and completed snapshots unchanged after corrections and retirements',async()=>{
  await installBank({bank,manifest:m});const s=await beginPractice('mixed','untimed',10);const target=s.questions[0];const corrected=q.filter(x=>x.id!==s.questions[1].id).map(x=>x.id===target.id?{...x,revision:2,stem:'Corrected wording',guide:{...x.guide!,correctChoiceId:'A' as const}}:x);const r=await release('corrected',corrected);await checkForBank(mockFetch(r));const p=await loadProgress();expect(p.sessions[0].questions).toEqual(s.questions);expect(availableQuestions(corrected,'mixed',p.exposures,p.sessions).some(x=>x.id===target.id)).toBe(false);const done=complete(s);done.responses[target.id].answer=target.guide!.correctChoiceId;expect(gradeSession(done).correct).toBe(1);
 });
 it('merges answer changes from stale tabs and never reopens a completed session',async()=>{
  const initial=createSession(q.slice(0,2),'untimed','mixed');await saveSession(initial);const a=structuredClone(initial),b=structuredClone(initial);a.responses[q[0].id].answer='A';b.responses[q[1].id].answer='B';await saveSession(a,initial);await saveSession(b,initial);let s=(await loadProgress()).sessions[0];expect(s.responses[q[0].id].answer).toBe('A');expect(s.responses[q[1].id].answer).toBe('B');await saveSession(complete(s));await saveSession(initial);expect((await loadProgress()).sessions[0].status).toBe('submitted');
 });
 it('restores and deduplicates validated backups and resets progress separately from bank',async()=>{
  await installBank({bank,manifest:m});const s=await beginPractice('mixed','untimed',10);await saveSession(complete(s));const data=await loadProgress();const backup=parseBackup(JSON.stringify({format:'hspt-progress',version:1,exportedAt:new Date().toISOString(),...data}));await resetProgress();expect((await loadBank())?.manifest.releaseId).toBe(m.releaseId);await mergeProgress(backup.sessions,backup.exposures);await mergeProgress(backup.sessions,backup.exposures);expect(await loadProgress()).toEqual(data);
 });
 it('rejects malformed backups and importing a second unfinished test',async()=>{
  expect(()=>parseBackup('{"version":2}')).toThrow();const s=createSession(q.slice(0,2),'timed','mixed');const bad=structuredClone(s);bad.responses[q[0].id].answer='Z' as any;expect(()=>parseBackup(JSON.stringify({format:'hspt-progress',version:1,sessions:[bad],exposures:[]}))).toThrow();await saveSession(s);await expect(mergeProgress([{...s,id:'different'}],[])).rejects.toThrow('unfinished');expect((await loadProgress()).sessions).toHaveLength(1);
 });
});
describe('repeat policy and schema',()=>{
 it('requires both 14 days and five subsequent completed sessions',()=>{
  const e:Exposure={questionId:q[0].id,lastEncounteredAt:1000,lastSessionId:'old',encounterCount:1,outcomes:{}};const sessions=Array.from({length:5},(_,i)=>complete(createSession([q[1]],'untimed','mixed',2000+i),3000+i));
  expect(availableQuestions([q[0]],'mixed',[e],sessions,1000+14*86400000)).toHaveLength(1);expect(availableQuestions([q[0]],'mixed',[e],sessions.slice(0,4),1000+14*86400000)).toHaveLength(0);expect(availableQuestions([q[0]],'mixed',[e],sessions,1000+13*86400000)).toHaveLength(0);
 });
 it('prefers unseen, then least recently encountered, with unique variants where possible',()=>{
  const small=q.slice(0,4).map((x,i)=>({...x,templateFamily:'family'+i,variantGroupId:i<2?'same':String(i)}));const e=small.slice(0,2).map((x,i)=>({questionId:x.id,lastEncounteredAt:100+i,lastSessionId:'s'+i,encounterCount:1,outcomes:{}}));const picked=pickFresh(small,'mixed',e,[],3,true,1000,()=>.5);expect(picked.slice(0,2).map(x=>x.id).sort()).toEqual(small.slice(2).map(x=>x.id).sort());expect(picked[2].id).toBe(small[0].id);
 });
 it('rejects missing diagrams, unsupported types, duplicates and unaccepted records',()=>{
  expect(()=>validateBank(bank,m)).not.toThrow();for(const mutate of [(x:any)=>x.questions[0].format='future',(x:any)=>x.questions[0].acceptance=null,(x:any)=>x.questions[1].id=x.questions[0].id,(x:any)=>{delete x.questions.find((q:any)=>q.diagram).diagram;}]){const bad=structuredClone(bank);mutate(bad);expect(()=>validateBank(bad,m)).toThrow();}
 });
});
