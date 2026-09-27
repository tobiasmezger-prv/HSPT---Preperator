import {describe,it,expect} from 'vitest';
import {renderToStaticMarkup} from 'react-dom/server';
import {questions,activeSkills} from '../src/data/questions';
import bank from '../content/staging/gables-v2/bank.json';
import {createSession,complete,selectQuestions} from '../src/domain/session';
import {gradeSession} from '../src/domain/scoring';
import Results from '../src/components/Results';
import QuestionDiagram from '../src/components/QuestionDiagram';
import decisions from '../content/review/gables-v2/decisions.json';
describe('Gables bank integration',()=>{
 it('imports exactly the reviewed content and preserves all keys and explanations',()=>{
  expect(questions).toHaveLength(100);expect(decisions.items).toHaveLength(20);expect(decisions.items.every(x=>x.decision==='approve')).toBe(true);
  questions.forEach((q,i)=>{expect(q.stem).toBe(bank[i].stem);expect(q.choices).toEqual(bank[i].choices);expect(q.guide).toEqual(bank[i].guide);expect(q.reviewStatus).toBe('sample_reviewed');});
 });
 it('renders all 16 self-contained accessible diagrams without answer explanations',()=>{
  const visual=questions.filter(q=>q.diagram);expect(visual).toHaveLength(16);
  for(const q of visual){expect(q.diagram!.svg).toContain('<svg');expect(q.diagram!.alt.length).toBeGreaterThan(20);const html=renderToStaticMarkup(<QuestionDiagram question={q}/>);expect(html).toContain('data:image/svg+xml');expect(html).toContain('alt=');expect(html).not.toContain(q.guide!.explanation);}
 });
 it('grades every answer format correctly and includes the diagram in result review',()=>{
  const s=complete(createSession(questions,'untimed','mixed',0),1000);
  for(const q of questions)s.responses[q.id].answer=q.guide!.correctChoiceId;
  expect(gradeSession(s)).toMatchObject({correct:100,percentage:100,completeKey:true});
  const q=questions.find(q=>q.diagram)!;s.responses[q.id].answer=null;
  const html=renderToStaticMarkup(<Results session={s} onHome={()=>{}} onPractice={()=>{}}/>);expect(html).toContain('data:image/svg+xml');expect(html).toContain('Human sample reviewed');expect(html).toContain(renderToStaticMarkup(<p>{q.guide!.explanation}</p>));
 });
 it('supports every offered focus and covers all four formats in fresh mixed bursts',()=>{
  expect(activeSkills).not.toContain('symbolic_pattern');expect(activeSkills).not.toContain('odd_one_out');
  for(const skill of activeSkills){const batch=selectQuestions(questions,skill);expect(batch).toHaveLength(10);expect(batch.every(q=>q.skill===skill)).toBe(true);}
  for(let i=0;i<100;i++){const batch=selectQuestions(questions,'mixed');expect(batch).toHaveLength(10);expect(new Set(batch.map(q=>q.format)).size).toBe(4);expect(new Set(batch.map(q=>q.templateFamily)).size).toBe(10);}
 });
 it('uses 100 unseen items before repeating and remembers unchanged prior-bank exposures',()=>{
  const seen:string[]=[];for(let n=0;n<10;n++){const batch=selectQuestions(questions,'mixed',seen);expect(batch.every(q=>!seen.includes(q.id))).toBe(true);seen.push(...batch.map(q=>q.id));}expect(new Set(seen).size).toBe(100);
  const prior=questions.find(q=>q.provenance?.priorId==='dev-01')!;
  const batch=selectQuestions(questions,'mixed',['dev-01'],()=>.5);expect(batch.map(q=>q.id)).not.toContain(prior.id);
 });
 it('keeps snapshot diagrams and answer keys stable through save-style serialization',()=>{
  const s=createSession(questions.filter(q=>q.diagram),'timed','mixed',1000);const saved=JSON.parse(JSON.stringify(s));expect(saved.questions).toEqual(s.questions);expect(saved.deadlineAt).toBe(301000);
 });
});
