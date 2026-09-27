import {describe,it,expect} from 'vitest';
import {legacyQuestions as questions} from '../src/data/questions.legacy';
import authored from '../content/authored-drafts.json';
import {letters,skills} from '../src/domain/types';
import {selectQuestions} from '../src/domain/session';

// Arithmetic recomputed from each stem independently of the key and distractors.
// These checks do not constitute an independent human content review.
const oracle=[
 32-7,2.4+.4,24+10,22-7,24+3,8+3,7/4+1/2,23+9,29+11,30-10,18+7,8+13,6+7*4,33+5,4+5,18+4,
 54*3,15/3,23*2+1,95*3-1,.75/2,36*2,120*6,70*10,28*4,3*3,27*1.5,3*2**5,9/2+3,8*2,
 Math.min(.45,.5,.48,.405),Math.max(5/8,5/6,5/9,5/12),7/13,Math.max(.2*90,.3*70,.25*80,.1*190),.95,Math.max(.607,.67,.067,.617),Math.max(-.8,-.5,-.65,-.9),7/20,6*6-8*4,2*(9+3)/4,3/4-2/3,3/5,Math.min(.5**2,1/3,.3,.28),6**2/3**2,4/9,180-45-65-45,
 350/10,.15*80,18/.3,40*.8,35/5*3,15*3-12-16,7+3*8,19*6,3/8*64,15/5*8,72/3+1,157%6,52/4,(46+8)/2,(50-40)/40,3/4*1/2,
 5*4-2,(23-5)/2,3*4+3,7**2+2,3*4+7,14-18/2,9+5,5*6-1,2*(2*3+1)+1,(5+4)*3,8+5,2*(17-2*6),(2*7+3)-(2*3+7),Math.sqrt(32+4),
 21,100,48,8,145,9/16,46,8/7,27,35,7/15,54
];
function numeric(text:string):number{
 const s=text.replaceAll('−','-');
 if(s==='(1/2)²')return .25;
 if(s.includes('% of ')){const [a,b]=s.split('% of ');return Number(a)/100*Number(b);}
 if(s.endsWith('%'))return Number(s.slice(0,-1))/100;
 if(s.includes('/')){const [a,b]=s.split('/');return Number(a)/Number(b);}
 if(s.includes(':')){const [a,b]=s.split(':');return Number(a)/Number(b);}
 return Number(s);
}
function gcd(a:number,b:number):number{return b?gcd(b,a%b):a;}
function prime(n:number){if(n<2)return false;for(let d=2;d*d<=n;d++)if(n%d===0)return false;return true;}
describe('100-question draft bank',()=>{
 it('has exact size, complete metadata, distinct choices and no duplicated questions or IDs',()=>{
  expect(questions).toHaveLength(100);expect(new Set(questions.map(q=>q.id)).size).toBe(100);expect(new Set(questions.map(q=>JSON.stringify([q.stem,q.choices]))).size).toBe(100);
  for(const q of questions){expect(Object.keys(skills)).toContain(q.skill);expect([1,2,3]).toContain(q.difficulty);expect(q.reviewStatus).toBe('pending_human_review');expect(q.sourceType).toBe('original_draft');expect(q.choices).toHaveLength(4);expect(new Set(q.choices).size,q.id).toBe(4);if(q.templateFamily!=='fraction-equivalence-classification')expect(new Set(q.choices.map(numeric)).size,q.id).toBe(4);expect(letters).toContain(q.guide?.correctChoiceId);expect(q.guide!.explanation.length).toBeGreaterThan(30);expect(q.guide!.shortcut.length).toBeGreaterThan(20);}
 });
 it('independently recomputes all 88 added answer keys',()=>{
  expect(oracle).toHaveLength(88);
  questions.slice(12).forEach((q,i)=>{
   const answer=q.choices[letters.indexOf(q.guide!.correctChoiceId)];
   expect(answer,q.id).toBe(authored[i].answer);
   expect(numeric(answer),q.id).toBeCloseTo(oracle[i],10);
   expect(q.choices.filter(c=>Math.abs(numeric(c)-oracle[i])<1e-10),q.id).toHaveLength(1);
  });
 });
 it('checks the classification rule for every added odd-one-out item',()=>{
  const predicates=[(n:number)=>!prime(n),(n:number)=>!Number.isInteger(Math.cbrt(n)),(n:number)=>!Number.isInteger(Math.log2(n)),(n:number)=>36%n!==0,(n:number)=>n%9!==0,(n:number)=>n!==.75,(n:number)=>n%4!==0,(n:number)=>n>=1,(n:number)=>n%5!==1,(n:number)=>!Number.isInteger(Math.sqrt(n-1)),(_:number,s:string)=>{const [a,b]=s.split('/').map(Number);return gcd(a,b)===1;},(n:number)=>n%12!==0];
  questions.slice(88).forEach((q,i)=>{const matches=q.choices.filter(c=>predicates[i](numeric(c),c));expect(matches,q.id).toEqual([q.choices[letters.indexOf(q.guide!.correctChoiceId)]]);});
 });
 it('checks benchmark comparisons rather than only the named numerical value',()=>{
  for(const [id,predicate] of [
   ['quant-045',(n:number)=>n>.5],
   ['quant-047',(n:number)=>Math.abs(n-1)<.06],
   ['quant-057',(n:number)=>Math.abs(n-.5)<1/17]
  ] as const){const q=questions.find(q=>q.id===id)!;expect(q.choices.filter(c=>predicate(numeric(c))),id).toEqual([q.choices[letters.indexOf(q.guide!.correctChoiceId)]]);}
 });
 it('supports ten-question practice in every skill and balances mixed bursts',()=>{
  for(const skill of [...new Set(questions.map(q=>q.skill))]){expect(questions.filter(q=>q.skill===skill).length).toBeGreaterThanOrEqual(10);const picked=selectQuestions(questions,skill);expect(picked).toHaveLength(10);expect(picked.every(q=>q.skill===skill)).toBe(true);expect(new Set(picked.map(q=>q.id)).size).toBe(10);}
  for(let i=0;i<100;i++){const picked=selectQuestions(questions,'mixed');expect(new Set(picked.map(q=>q.skill)).size).toBe(6);expect(new Set(picked.map(q=>q.templateFamily)).size).toBe(10);for(const skill of Object.keys(skills))expect(picked.filter(q=>q.skill===skill).length).toBeLessThanOrEqual(2);}
 });
 it('uses all 100 unseen questions across ten bursts before repeating',()=>{
  const seen:string[]=[];for(let i=0;i<10;i++){const batch=selectQuestions(questions,'mixed',seen);expect(batch).toHaveLength(10);expect(batch.every(q=>!seen.includes(q.id))).toBe(true);seen.push(...batch.map(q=>q.id));}expect(new Set(seen).size).toBe(100);expect(selectQuestions(questions,'mixed',seen)).toHaveLength(10);
 });
});
