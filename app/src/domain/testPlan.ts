import type {Question,Session,Section,TestKind} from './types';
import {sections} from './types';
import {createSession,complete} from './session';
export const testOrder:Section[]=['verbal','quantitative','reading','mathematics','language'];
export function questionSection(q:Question):Section{return q.section??'quantitative';}
export const presetVersion='hspt-18min-v1';
export const presets:Record<Section,{questions:number;minutes:number;burst:number}>={verbal:{questions:60,minutes:18,burst:17},quantitative:{questions:52,minutes:30,burst:9},reading:{questions:62,minutes:25,burst:12},mathematics:{questions:64,minutes:45,burst:7},language:{questions:60,minutes:25,burst:12}};
export const fullQuestionCount=testOrder.reduce((n,s)=>n+presets[s].questions,0);
export const fullMinutes=testOrder.reduce((n,s)=>n+presets[s].minutes,0);
export function targetCount(section:Section,kind:TestKind){return kind==='burst'?presets[section].burst:presets[section].questions;}
export function sessionTitle(s:Session){return s.testKind==='full'?(s.preview?'Full test preview':'Full practice test'):`${sections[s.section??'quantitative']} · ${s.testKind==='section'?(s.preview?'Section preview':'Full section'):s.mode==='timed'?'5-minute practice':'Untimed practice'}`;}
export function planSession(groups:{section:Section;questions:Question[]}[],kind:TestKind,_mode:Session['mode'],now=Date.now()):Session{
 const questions=groups.flatMap(g=>g.questions);
 if(!questions.length||new Set(questions.map(q=>q.id)).size!==questions.length||groups.some(g=>!g.questions.length||g.questions.some(q=>questionSection(q)!==g.section)))throw new Error('Every section needs unique available questions.');
 if(kind==='full'&&(groups.length!==5||groups.some((g,i)=>g.section!==testOrder[i])))throw new Error('A full test needs all five sections in order.');
 if(kind!=='full'&&groups.length!==1)throw new Error('Choose one section.');
 if(groups.some(g=>kind==='burst'?g.questions.length>presets[g.section].burst:g.questions.length!==presets[g.section].questions))throw new Error('Available questions do not match this test preset.');
 const durationMs=(kind==='burst'?5:presets[groups[0].section].minutes)*60000;
 return {...createSession(questions,'timed','mixed',now),presetVersion,actualQuestionCount:questions.length,durationMs,deadlineAt:now+durationMs,testKind:kind,section:groups[0].section,preview:questions.some(q=>q.dummy),parts:kind==='full'?groups.map((g,i)=>({section:g.section,questionIds:g.questions.map(q=>q.id),durationMs:presets[g.section].minutes*60000,...(i===0?{startedAt:now}:{})})):undefined,partIndex:kind==='full'?0:undefined,stage:'questions'};
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
 return {...s,partIndex:index,section:s.parts[index].section,stage:'questions',durationMs:s.parts[index].durationMs??300000,deadlineAt:s.mode==='timed'?now+(s.parts[index].durationMs??300000):undefined,parts:s.parts.map((p,i)=>i===index?{...p,startedAt:now}:p)};
}

export function testDuration(s:Session){return s.parts?s.parts.reduce((total,p)=>total+(p.startedAt!==undefined&&p.completedAt!==undefined?Math.max(0,p.completedAt-p.startedAt):0),0):Math.max(0,(s.completedAt??s.startedAt)-s.startedAt);}
