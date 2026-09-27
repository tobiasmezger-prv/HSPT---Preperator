import type {Session} from './types';
import type {Exposure} from './freshSelection';
import {validateQuestion} from './contentSchema.mjs';
export type Backup={format:'hspt-progress';version:1;exportedAt:string;sessions:Session[];exposures:Exposure[]};
export function parseBackup(text:string):Backup{
 if(text.length>30_000_000)throw new Error('Backup exceeds 30 MB.');const b=JSON.parse(text);const fail=()=>{throw new Error('Invalid progress backup.');};
 if(b?.format!=='hspt-progress'||b.version!==1||!Array.isArray(b.sessions)||!Array.isArray(b.exposures)||b.sessions.length>10000)fail();
 const ids=new Set();for(const s of b.sessions){if(!s||typeof s.id!=='string'||!s.id||ids.has(s.id)||!['active','submitted','expired'].includes(s.status)||!['timed','untimed'].includes(s.mode)||!Number.isFinite(s.startedAt)||!Array.isArray(s.questions)||!s.questions.length||s.questions.length>100||!s.responses)fail();ids.add(s.id);
 if(s.mode==='timed'&&(!Number.isFinite(s.deadlineAt)||s.deadlineAt<s.startedAt))fail();if(s.status!=='active'&&(!Number.isFinite(s.completedAt)||s.completedAt<s.startedAt))fail();const qids=new Set();for(const q of s.questions){validateQuestion(q);if(qids.has(q.id))fail();qids.add(q.id);const r=s.responses[q.id];if(!r||!(r.answer===null||['A','B','C','D'].includes(r.answer))||typeof r.flagged!=='boolean'||!Number.isFinite(r.approximateActiveMs)||r.approximateActiveMs<0)fail();}}
 if(b.sessions.filter((s:Session)=>s.status==='active').length>1)fail();const eids=new Set();for(const e of b.exposures){if(!e||typeof e.questionId!=='string'||!e.questionId||eids.has(e.questionId)||!Number.isFinite(e.lastEncounteredAt)||typeof e.lastSessionId!=='string'||!Number.isInteger(e.encounterCount)||e.encounterCount<1||!e.outcomes||typeof e.outcomes!=='object'||Array.isArray(e.outcomes)||!Object.values(e.outcomes).every(x=>['correct','incorrect','unanswered','ungraded'].includes(x as string)))fail();eids.add(e.questionId);}
 return b;
}
