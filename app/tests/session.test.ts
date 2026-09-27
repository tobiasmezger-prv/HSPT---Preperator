import {describe,it,expect} from 'vitest';
import {createSession,remaining,complete,selectQuestions} from '../src/domain/session';
import {legacyQuestions as questions} from '../src/data/questions.legacy';
describe('deadline and completion',()=>{
 it('anchors the five-minute deadline to wall time across backgrounding',()=>{const s=createSession(questions.slice(0,10),'timed','mixed',1000);expect(remaining(s,61000)).toBe(240000);expect(remaining(s,999999)).toBe(0);expect(complete(s,999999)).toMatchObject({status:'expired',completedAt:301000});});
 it('makes completion idempotent and preserves answers and flags',()=>{const s=createSession(questions.slice(0,10),'timed','mixed',1000);s.responses['dev-01'].answer='B';s.responses['dev-01'].flagged=true;const done=complete(s,10000);expect(complete(done,999999)).toBe(done);expect(done.responses['dev-01']).toMatchObject({answer:'B',flagged:true});expect(done.status).toBe('submitted');});
 it('never expires untimed sessions',()=>expect(remaining(createSession(questions,'untimed','mixed',0),999999)).toBeNull());
});
describe('development selection',()=>{
 it('selects ten distinct items covering all six skills',()=>{const q=selectQuestions(questions,'mixed');expect(q).toHaveLength(10);expect(new Set(q.map(x=>x.id)).size).toBe(10);expect(new Set(q.map(x=>x.skill)).size).toBe(6);expect(new Set(q.map(x=>x.templateFamily)).size).toBe(10);});
 it('prefers unseen items within skills',()=>{const q=selectQuestions(questions.slice(0,12),'sequence_additive',['dev-01'],()=>.5);expect(q[0].id).toBe('dev-02');});
 it('does not invent or duplicate items to fill a sparse skill bank',()=>{const q=selectQuestions(questions.slice(0,12),'odd_one_out');expect(q).toHaveLength(2);expect(q.every(x=>x.skill==='odd_one_out')).toBe(true);});
});
