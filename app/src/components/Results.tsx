import {testDuration} from '../domain/testPlan';
import QuestionDiagram,{bankLabel} from './QuestionDiagram';
import {useState} from 'react';
import type {Session,Skill} from '../domain/types';
import {letters,skills,sections} from '../domain/types';
import {gradeSession,reviewItems} from '../domain/scoring';
import {formatTime} from './Test';
export default function Results({session,onHome,onPractice}:{session:Session;onHome:()=>void;onPractice:(skill:Skill)=>void}){
 const [all,setAll]=useState(false);
 const score=gradeSession(session);
 const items=reviewItems(session,all);
 return <section className="results">
  <span className="eyebrow">PRACTICE COMPLETE</span>
  <h1>{session.status==='expired'?'Time is up. Let’s review.':'A little practice. A little progress.'}</h1>
  <div className="score-card" aria-label="Practice results">
   <div className="score-main"><strong>{score.completeKey?`${score.correct} / ${score.total}`:'Grading unavailable'}</strong><span>{score.completeKey?`${score.percentage??0}% correct`:'Some questions are missing answer keys.'}</span></div>
   <dl className="score-details"><div><dt>Attempted</dt><dd>{score.attempted}</dd></div><div><dt>Incorrect</dt><dd>{score.incorrect}</dd></div><div><dt>Unanswered</dt><dd>{score.unanswered}</dd></div><div><dt>Time used</dt><dd>{formatTime(testDuration(session))}</dd></div></dl>
  </div>
  {session.parts&&<div className="metrics">{session.parts.map(part=>{const items=score.items.filter(i=>part.questionIds.includes(i.question.id));return <p key={part.section}><strong>{sections[part.section]}</strong><br/>{items.filter(i=>i.outcome==='correct').length}/{items.length} correct{part.expired?' · Time expired':''}</p>;})}</div>}
  <p className="fixture-caption">{bankLabel(session.questions)}</p>
  <div className="review-heading"><div><h2>Review your answers</h2><p>Incorrect and unanswered questions come first.</p></div><button aria-pressed={all} onClick={()=>setAll(v=>!v)}>{all?'Show errors & omissions':`Show all ${score.total} questions`}</button></div>
  {items.length===0&&<p className="review-empty">Every answer is correct. You can still explore the explanations by showing all questions.</p>}
  <div className="review-list">{items.map(({question:q,number,answer,outcome})=><article className="review-card" key={q.id}>
   <div className="review-meta"><span>Question {number} · {skills[q.skill]}</span><strong className={`outcome ${outcome}`}>{outcome==='unanswered'?'Unanswered':outcome==='incorrect'?'Incorrect':outcome==='correct'?'Correct':'Not graded'}</strong></div>
   <>{q.passage&&<aside className="reading-passage"><h4>{q.passage.title}</h4>{(q.passage.paragraphs??[q.passage.text]).map((text,index)=><p key={index}>{q.passage?.paragraphs&&<span className="paragraph-number">[{index+1}] </span>}{text}</p>)}</aside>}</><h3>{q.stem}</h3><QuestionDiagram question={q}/>
   <ul className="review-choices">{q.choices.map((choice,i)=><li key={letters[i]} className={q.guide?.correctChoiceId===letters[i]?'correct-choice':answer===letters[i]?'wrong-choice':''}><span><b>{letters[i]}.</b> {choice}</span><span className="choice-note">{q.guide?.correctChoiceId===letters[i]?'Correct answer':''}{answer===letters[i]?(q.guide?.correctChoiceId===letters[i]?' · Your answer':'Your answer'):''}</span></li>)}</ul>
   {answer===null&&<p className="unanswered-note">Your answer: Unanswered</p>}
   {q.guide?<><div className="explanation"><h4>Why this answer works</h4><p>{q.guide.explanation}</p></div>{q.guide.shortcut&&<div className="tip"><h4>Quick-solving tip</h4><p>{q.guide.shortcut}</p></div>}</>:<p className="notice">This saved question has no matching answer key. It has not been graded.</p>}
   <button className="text-button" onClick={()=>onPractice(q.skill)}>Practice this skill →</button>
  </article>)}</div>
  <button className="primary" onClick={onHome}>Back to home</button>
 </section>;
}
