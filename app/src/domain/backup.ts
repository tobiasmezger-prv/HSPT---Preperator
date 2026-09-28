import type {Session} from './types';
import type {Exposure} from './freshSelection';
import {validateQuestion} from './contentSchema.mjs';
export type Backup={format:'hspt-progress';version:1;exportedAt:string;sessions:Session[];exposures:Exposure[]};
export function parseBackup(text:string):Backup{
 if(text.length>30_000_000)throw new Error('Backup exceeds 30 MB.');const b=JSON.parse(text);const fail=()=>{throw new Error('Invalid progress backup.');};
 if(b?.format!=='hspt-progress'||b.version!==1||!Array.isArray(b.sessions)||!Array.isArray(b.exposures)||b.sessions.length>10000)fail();
 const ids=new Set();for(const s of b.sessions){if(!s||typeof s.id!=='string'||!s.id||ids.has(s.id)||!['active','submitted','expired'].includes(s.status)||!['timed','untimed'].includes(s.mode)||!Number.isFinite(s.startedAt)||!Array.isArray(s.questions)||!s.questions.length||s.questions.length>100||!s.responses)fail();ids.add(s.id);
 if(s.mode==='timed'&&s.stage!=='break'&&(!Number.isFinite(s.deadlineAt)||s.deadlineAt<s.startedAt))fail();if(s.status!=='active'&&(!Number.isFinite(s.completedAt)||s.completedAt<s.startedAt))fail();const qids=new Set();for(const q of s.questions){validateQuestion(q);if(qids.has(q.id))fail();qids.add(q.id);const r=s.responses[q.id];if(!r||!(r.answer===null||['A','B','C','D'].includes(r.answer))||typeof r.flagged!=='boolean'||!Number.isFinite(r.approximateActiveMs)||r.approximateActiveMs<0)fail();}}
 for(const s of b.sessions){
  if(s.testKind!==undefined&&!['burst','section','full'].includes(s.testKind))fail();
  if(s.section!==undefined&&!['quantitative','mathematics','verbal','reading','language'].includes(s.section))fail();
  if(s.stage!==undefined&&!['questions','break'].includes(s.stage))fail();
  if(s.testKind==='full'||s.parts){
   if(s.testKind!=='full'||!Array.isArray(s.parts)||s.parts.length!==5||!Number.isInteger(s.partIndex)||s.partIndex<0||s.partIndex>=5)fail();
   const partIds=new Set<string>();const names=new Set<string>();
   for(const [i,part] of s.parts.entries()){
    if(!part||!['quantitative','mathematics','verbal','reading','language'].includes(part.section)||names.has(part.section)||!Array.isArray(part.questionIds)||!part.questionIds.length)fail();names.add(part.section);
    for(const id of part.questionIds){if(partIds.has(id)||!s.questions.some((q:any)=>q.id===id&&(q.section??'quantitative')===part.section))fail();partIds.add(id);}
    if(i<=s.partIndex&&!Number.isFinite(part.startedAt))fail();
    if((i<s.partIndex||s.stage==='break'||s.status!=='active')&&i<=s.partIndex&&(!Number.isFinite(part.completedAt)||part.completedAt<part.startedAt))fail();
   }
   if(partIds.size!==s.questions.length||s.stage==='break'&&(s.partIndex===4||s.deadlineAt!==undefined)||s.status!=='active'&&s.partIndex!==4)fail();
  }else if(s.stage==='break')fail();
 }
 if(b.sessions.filter((s:Session)=>s.status==='active').length>1)fail();const eids=new Set();for(const e of b.exposures){if(!e||typeof e.questionId!=='string'||!e.questionId||eids.has(e.questionId)||!Number.isFinite(e.lastEncounteredAt)||typeof e.lastSessionId!=='string'||!Number.isInteger(e.encounterCount)||e.encounterCount<1||!e.outcomes||typeof e.outcomes!=='object'||Array.isArray(e.outcomes)||!Object.values(e.outcomes).every(x=>['correct','incorrect','unanswered','ungraded'].includes(x as string)))fail();eids.add(e.questionId);}
 return b;
}
