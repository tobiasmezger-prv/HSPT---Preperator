import {testOrder,questionSection,planSession} from './testPlan';
import {openDB} from 'idb';
import type {Session,Skill} from './types';
import {validateBank,type Bank,type Manifest} from './contentSchema.mjs';
import {pickFresh,type Exposure} from './freshSelection';
import {createSession} from './session';
export type InstalledBank={manifest:Manifest;bank:Bank};
export function deriveExposures(sessions:Session[],extra:Exposure[]=[]):Exposure[]{
 const map=new Map<string,Exposure>();
 for(const s of [...sessions].sort((a,b)=>a.startedAt-b.startedAt))for(const q of s.questions){const prior=map.get(q.id);const answer=s.responses[q.id]?.answer;const outcome=!answer?'unanswered':!q.guide?'ungraded':answer===q.guide.correctChoiceId?'correct':'incorrect';map.set(q.id,{questionId:q.id,lastEncounteredAt:s.startedAt,lastSessionId:s.id,encounterCount:(prior?.encounterCount??0)+1,outcomes:{...prior?.outcomes,...(s.status==='active'?{}:{[s.id]:outcome})}});}
 for(const e of extra){const p=map.get(e.questionId);if(!p)map.set(e.questionId,e);else map.set(e.questionId,{...(p.lastEncounteredAt>=e.lastEncounteredAt?p:e),encounterCount:Math.max(p.encounterCount,e.encounterCount),outcomes:{...e.outcomes,...p.outcomes}});}
 return [...map.values()];
}
export const database=()=>new Promise<Awaited<ReturnType<typeof openDB>>>((resolve,reject)=>{let blocked=false;const request=openDB('hspt-practice',2,{blocked(){blocked=true;reject(new Error('Close other HSPT tabs and retry so saved progress can be upgraded.'));},upgrade(db,old,_new,tx){
 if(old<1)db.createObjectStore('sessions',{keyPath:'id'});
 if(old<2){db.createObjectStore('banks',{keyPath:'manifest.releaseId'});db.createObjectStore('meta');db.createObjectStore('exposures',{keyPath:'questionId'});void tx.objectStore('sessions').getAll().then(sessions=>Promise.all(deriveExposures(sessions).map(e=>tx.objectStore('exposures').put(e)))).catch(()=>{try{tx.abort();}catch{}});}
},blocking(_old,_new,event){(event.target as IDBDatabase)?.close();}});void request.then(db=>{if(blocked)db.close();else resolve(db);},reject);});
async function access<T>(work:(db:Awaited<ReturnType<typeof database>>)=>Promise<T>):Promise<T>{const db=await database();try{return await work(db);}finally{db.close();}}
async function write<T>(stores:string[],work:(tx:any)=>Promise<T>):Promise<T>{return access(async db=>{const tx=db.transaction(stores,'readwrite');void tx.done.catch(()=>{});try{const result=await work(tx);await tx.done;return result;}catch(e){try{tx.abort();}catch{}await tx.done.catch(()=>{});throw e;}});}
async function exposuresIn(tx:any){const sessions=await tx.objectStore('sessions').getAll();const extra=await tx.objectStore('exposures').getAll();for(const e of deriveExposures(sessions,extra))await tx.objectStore('exposures').put(e);}
export async function saveSession(session:Session,base?:Session):Promise<Session>{return write(['sessions','exposures'],async tx=>{
 const existing=await tx.objectStore('sessions').get(session.id);if(existing?.status!=='active'&&existing)return existing;
 if(existing?.parts&&((existing.partIndex??0)>(base?.partIndex??session.partIndex??0)||(base&&existing.stage!==base.stage)||(!base&&existing.stage==='break'&&session.stage==='questions'&&existing.partIndex===session.partIndex)))return existing;
 const merged=existing&&base?{...session,questions:existing.questions,responses:Object.fromEntries(existing.questions.map((q:any)=>{const old=existing.responses[q.id],next=session.responses[q.id],before=base.responses[q.id];return [q.id,{answer:next.answer!==before?.answer?next.answer:old.answer,flagged:next.flagged!==before?.flagged?next.flagged:old.flagged,approximateActiveMs:Math.max(next.approximateActiveMs,old.approximateActiveMs)}];}))}:session;
 await tx.objectStore('sessions').put(merged);await exposuresIn(tx);return merged;
});}
export async function loadSessions():Promise<Session[]>{return access(db=>db.getAll('sessions'));}
export async function loadProgress(){return access(async db=>{const tx=db.transaction(['sessions','exposures']);return {sessions:await tx.objectStore('sessions').getAll() as Session[],exposures:await tx.objectStore('exposures').getAll() as Exposure[]};});}
export async function loadBank():Promise<InstalledBank|null>{return access(async db=>{const tx=db.transaction(['banks','meta']);const id=await tx.objectStore('meta').get('activeBank');return id?(await tx.objectStore('banks').get(id)??null):null;});}
export async function installBank(value:InstalledBank){return write(['banks','meta'],async tx=>{const old=await tx.objectStore('banks').get(value.manifest.releaseId);if(old&&old.manifest.checksum!==value.manifest.checksum)throw new Error('An immutable release changed.');await tx.objectStore('banks').put(value);await tx.objectStore('meta').put(value.manifest.releaseId,'activeBank');});}
export async function beginPractice(focus:Skill|'mixed',mode:Session['mode'],count:number,review=false,now=Date.now()):Promise<Session>{return write(['sessions','exposures','banks','meta'],async tx=>{
 const sessions=await tx.objectStore('sessions').getAll() as Session[];const active=sessions.find(s=>s.status==='active');if(active)return active;
 const release=await tx.objectStore('meta').get('activeBank');const installed=release?await tx.objectStore('banks').get(release) as InstalledBank|undefined:undefined;if(!installed)throw new Error('Download a question bank first.');validateBank(installed.bank,installed.manifest);
 const exposures=await tx.objectStore('exposures').getAll() as Exposure[];const picked=pickFresh(installed.bank.questions,focus,exposures,sessions,count,review,now);if(picked.length<count||!picked.length)throw new Error('Available questions changed. Review the updated practice options.');
 const s={...createSession(picked,mode,focus,now),bankRelease:release,practiceKind:review?'review' as const:'ordinary' as const};await tx.objectStore('sessions').put(s);for(const e of deriveExposures([...sessions,s],exposures))await tx.objectStore('exposures').put(e);return s;
});}
export async function mergeProgress(sessions:Session[],exposures:Exposure[]){return write(['sessions','exposures'],async tx=>{
 const existing=await tx.objectStore('sessions').getAll() as Session[];const ids=new Set(existing.map(s=>s.id));const additions=sessions.filter(s=>!ids.has(s.id));if([...existing,...additions].filter(s=>s.status==='active').length>1)throw new Error('Finish the current unfinished practice before importing another unfinished session.');
 for(const s of additions)await tx.objectStore('sessions').put(s);const current=await tx.objectStore('exposures').getAll() as Exposure[];for(const e of deriveExposures([...existing,...additions],[...current,...exposures]))await tx.objectStore('exposures').put(e);return additions.length;
});}
export async function probeStorage(){return write(['meta'],async tx=>{await tx.objectStore('meta').put(Date.now(),'storageProbe');await tx.objectStore('meta').delete('storageProbe');});}
export async function resetProgress(){return write(['sessions','exposures'],async tx=>{await tx.objectStore('sessions').clear();await tx.objectStore('exposures').clear();});}
export type Preferences={timerVisible:boolean};
export function loadPreferences():Preferences{try{return {timerVisible:JSON.parse(localStorage.getItem('hspt-preferences')||'{}').timerVisible!==false};}catch{return {timerVisible:true};}}
export function savePreferences(p:Preferences){try{localStorage.setItem('hspt-preferences',JSON.stringify(p));}catch{/* Preferences are optional. */}}

// Reserve every part together; all tabs observe the same unfinished test.
export async function beginPlannedPractice(section:import('./types').Section,kind:import('./types').TestKind,mode:Session['mode'],count:number,review=false,now=Date.now(),focus:Skill|'mixed'='mixed'):Promise<Session>{
 return write(['sessions','exposures','banks','meta'],async tx=>{
  const sessions=await tx.objectStore('sessions').getAll() as Session[];
  const active=sessions.find(s=>s.status==='active');if(active)return active;
  const release=await tx.objectStore('meta').get('activeBank');
  const installed=release?await tx.objectStore('banks').get(release) as InstalledBank:undefined;
  if(installed)validateBank(installed.bank,installed.manifest);
  if(!installed)throw new Error('Download a question bank first.');
  const pool=installed.bank.questions;
  const exposures=await tx.objectStore('exposures').getAll() as Exposure[];
  const groups=(kind==='full'?testOrder:[section]).map(part=>{const candidates=pool.filter(q=>questionSection(q)===part);let picked=pickFresh(candidates,kind==='burst'?focus:'mixed',exposures,sessions,kind==='full'?10:count,review,now);if(picked.length<(kind==='full'?10:count)||!picked.length)throw new Error('Available questions changed. Choose review or a shorter practice.');return {section:part,questions:picked};});
  const s={...planSession(groups,kind,mode,now),skill:kind==='burst'?focus:'mixed',bankRelease:release,practiceKind:review?'review' as const:'ordinary' as const};
  await tx.objectStore('sessions').put(s);for(const e of deriveExposures([...sessions,s],exposures))await tx.objectStore('exposures').put(e);return s;
 });
}
