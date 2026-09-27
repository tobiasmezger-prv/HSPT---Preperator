import {it,expect} from 'vitest';
import {legacyQuestions as questions} from '../src/data/questions.legacy';
// Independent arithmetic checks, not human approval or HSPT content validation.
it('checks unique IDs, four distinct choices and one arithmetic answer per sample',()=>{
 const computed=[22+5,20+7,24*2,Math.max(3/5,.58,.59,.61),84/4,6*3+1,32,(35-9)/2,20/2,3/8,(4+7)*2,48];
 const evaluate=(s:string)=>s.endsWith('%')?Number(s.slice(0,-1))/100:s.includes('/')?Number(s.split('/')[0])/Number(s.split('/')[1]):Number(s);
 expect(new Set(questions.map(q=>q.id)).size).toBe(questions.length);
 questions.slice(0,12).forEach((q,i)=>{expect(q.choices).toHaveLength(4);expect(new Set(q.choices).size).toBe(4);expect(q.choices.filter(c=>Math.abs(evaluate(c)-computed[i])<1e-9)).toHaveLength(1);});
 expect(questions[6].choices.filter(c=>Number(c)%6!==0)).toEqual(['32']);
 expect(questions[11].choices.filter(c=>!Number.isInteger(Math.sqrt(Number(c))))).toEqual(['48']);
});
