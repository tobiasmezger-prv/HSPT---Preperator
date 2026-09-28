import type {Question,Session,Section,TestKind} from './types';
import {sections} from './types';
import {createSession,complete} from './session';
export const testOrder:Section[]=['verbal','quantitative','reading','mathematics','language'];
export function questionSection(q:Question):Section{return q.section??'quantitative';}
export function sessionTitle(s:Session){return s.testKind==='full'?'Full test preview':`${sections[s.section??'quantitative']} · ${s.testKind==='section'?'Section preview':s.mode==='timed'?'5-minute practice':'Untimed practice'}`;}
export function planSession(groups:{section:Section;questions:Question[]}[],kind:TestKind,mode:Session['mode'],now=Date.now()):Session{
 const questions=groups.flatMap(g=>g.questions);if(!questions.length||groups.some(g=>!g.questions.length))throw new Error('Every section needs available questions.');
 return {...createSession(questions,mode,'mixed',now),testKind:kind,section:groups[0].section,preview:kind!=='burst'||questions.some(q=>q.dummy),parts:kind==='full'?groups.map((g,i)=>({section:g.section,questionIds:g.questions.map(q=>q.id),...(i===0?{startedAt:now}:{})})):undefined,partIndex:kind==='full'?0:undefined,stage:'questions'};
}
export function visibleSession(s:Session):Session{if(!s.parts)return s;const part=s.parts[s.partIndex??0];return {...s,section:part.section,questions:s.questions.filter(q=>part.questionIds.includes(q.id)),responses:Object.fromEntries(part.questionIds.map(id=>[id,s.responses[id]]))};}
export function finishPart(s:Session,now=Date.now()):Session{
 if(s.status!=='active'||s.stage==='break')return s;
 if(!s.parts)return complete(s,now);
 const index=s.partIndex??0,expired=s.deadlineAt!==undefined&&now>=s.deadlineAt;
 const parts=s.parts.map((p,i)=>i===index?{...p,completedAt:expired?s.deadlineAt:now,expired}:p);
 if(index===parts.length-1)return {...complete(s,now),parts};
 return {...s,parts,stage:'break',deadlineAt:undefined};
}
export function advancePart(s:Session,now=Date.now()):Session{
 if(s.status!=='active'||s.stage!=='break'||!s.parts)return s;
 const index=(s.partIndex??0)+1;if(!s.parts[index])return s;
 return {...s,partIndex:index,section:s.parts[index].section,stage:'questions',deadlineAt:s.mode==='timed'?now+300000:undefined,parts:s.parts.map((p,i)=>i===index?{...p,startedAt:now}:p)};
}

export function testDuration(s:Session){return s.parts?s.parts.reduce((total,p)=>total+(p.startedAt!==undefined&&p.completedAt!==undefined?Math.max(0,p.completedAt-p.startedAt):0),0):Math.max(0,(s.completedAt??s.startedAt)-s.startedAt);}
