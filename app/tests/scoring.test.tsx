import {describe,it,expect} from 'vitest';
import {renderToStaticMarkup} from 'react-dom/server';
import {createSession,complete} from '../src/domain/session';
import {gradeSession,reviewItems,withGuide} from '../src/domain/scoring';
import {legacyQuestions as questions} from '../src/data/questions.legacy';
import {letters} from '../src/domain/types';
import Results from '../src/components/Results';
const fixture=()=>complete(createSession(questions.slice(0,3),'untimed','mixed',0),12000);
describe('grading',()=>{
 it('separates correct, incorrect and unanswered, using total for percentage',()=>{const s=fixture();s.responses['dev-01'].answer='C';s.responses['dev-02'].answer='A';expect(gradeSession(s)).toMatchObject({correct:1,incorrect:1,unanswered:1,attempted:2,total:3,percentage:33});expect(reviewItems(s).map(i=>i.number)).toEqual([2,3]);expect(reviewItems(s,true).map(i=>i.number)).toEqual([2,3,1]);});
 it('handles perfect scores and entirely unanswered practice',()=>{const s=fixture();expect(gradeSession(s)).toMatchObject({correct:0,incorrect:0,unanswered:3,percentage:0});s.questions.forEach(q=>s.responses[q.id].answer=q.guide!.correctChoiceId);expect(gradeSession(s)).toMatchObject({correct:3,incorrect:0,unanswered:0,percentage:100});expect(reviewItems(s)).toHaveLength(0);});
 it('refuses review during active practice',()=>expect(()=>gradeSession(createSession(questions,'timed','mixed'))).toThrow('Finish practice'));
 it('grades expired sessions with the same deterministic rules',()=>{const s=fixture();s.status='expired';s.responses['dev-01'].answer='C';expect(gradeSession(s).correct).toBe(1);expect(gradeSession(s)).toEqual(gradeSession(s));});
 it('recovers exact old snapshots but does not apply a mismatched key',()=>{const {guide,...old}=questions[0];expect(withGuide(old).guide).toEqual(guide);expect(withGuide({...old,stem:'Changed question'}).guide).toBeUndefined();const s=fixture();s.questions[0]={...old,stem:'Changed question'};s.responses[old.id].answer='C';expect(gradeSession(s)).toMatchObject({completeKey:false,percentage:null,correct:0,incorrect:0});});
 it('renders omissions, explanations and tips, excluding correct items by default',()=>{const s=fixture();s.responses['dev-01'].answer='C';s.responses['dev-02'].answer='A';const html=renderToStaticMarkup(<Results session={s} onHome={()=>{}} onPractice={()=>{}}/>);expect(html).toContain('Your answer: Unanswered');expect(html).toContain('Quick-solving tip');expect(html).toContain(questions[1].guide!.explanation);expect(html).not.toContain(questions[0].stem);expect(html).toContain('Correct answer');expect(html).toContain('Practice this skill');});
 it('matches every keyed answer to independently computed arithmetic',()=>{const expected=[27,27,48,.61,21,19,32,13,10,.375,22,48];questions.slice(0,12).forEach((q,i)=>{const text=q.choices[letters.indexOf(q.guide!.correctChoiceId)];const value=text.includes('/')?Number(text.split('/')[0])/Number(text.split('/')[1]):Number(text);expect(value).toBeCloseTo(expected[i]);expect(q.guide!.explanation.length).toBeGreaterThan(30);expect(q.guide!.shortcut.length).toBeGreaterThan(20);});});
});
