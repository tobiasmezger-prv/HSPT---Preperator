import {legacyQuestions} from '../data/questions.legacy';
import type {Question, Session} from './types';

// Upgrade only exact snapshots from the original fixture. Never grade changed
// content using an answer key merely because its ID happens to match.
export function withGuide(q:Question):Question {
 if(q.guide)return q;
 const original=legacyQuestions.find(item=>item.id===q.id && item.stem===q.stem && item.skill===q.skill && JSON.stringify(item.choices)===JSON.stringify(q.choices));
 return original?.guide?{...q,guide:original.guide}:q;
}
export function gradeSession(session:Session){
 if(session.status==='active')throw new Error('Finish practice before reviewing answers.');
 const items=session.questions.map((raw,index)=>{
  const question=withGuide(raw);
  const answer=session.responses[question.id]?.answer??null;
  const outcome=answer===null?'unanswered':!question.guide?'ungraded':answer===question.guide.correctChoiceId?'correct':'incorrect';
  return {question,number:index+1,answer,outcome};
 });
 const correct=items.filter(i=>i.outcome==='correct').length;
 const incorrect=items.filter(i=>i.outcome==='incorrect').length;
 const unanswered=items.filter(i=>i.outcome==='unanswered').length;
 const total=items.length;
 const completeKey=items.every(i=>!!i.question.guide);
 return {items,total,correct,incorrect,unanswered,attempted:total-unanswered,completeKey,percentage:completeKey&&total?Math.round(correct/total*100):null};
}
export function reviewItems(session:Session,all=false){
 const items=gradeSession(session).items;
 return [...items.filter(i=>i.outcome!=='correct'),...(all?items.filter(i=>i.outcome==='correct'):[])];
}
