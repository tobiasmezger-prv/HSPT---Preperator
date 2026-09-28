import {it,expect} from 'vitest';
import bank from '../public/content/banks/all-sections-v0002.json';
import previous from '../public/content/banks/quantitative-v0001.json';
import manifest from '../public/content/manifest.json';
import {validateBank,validateQuestion,type Bank,type Manifest} from '../src/domain/contentSchema.mjs';
import {pickFresh,availableQuestions,type Exposure} from '../src/domain/freshSelection';
import {sections,type Section,type Skill} from '../src/domain/types';
import {planSession} from '../src/domain/testPlan';
import {parseBackup} from '../src/domain/backup';
import {gradeSession} from '../src/domain/scoring';
const questions=(bank as unknown as Bank).questions;
const reading=questions.filter(q=>q.section==='reading');
it('publishes exactly 100 real questions per section and preserves Quantitative verbatim',()=>{
 expect(()=>validateBank(bank,manifest as Manifest)).not.toThrow();
 expect(questions.filter(q=>q.section==='quantitative')).toEqual(previous.questions);
 for(const section of Object.keys(sections)){const qs=questions.filter(q=>q.section===section);expect(qs).toHaveLength(100);expect(qs.filter(q=>q.acceptance?.individualStatus==='approved')).toHaveLength(20);expect(qs.every(q=>!q.dummy&&q.reviewStatus==='sample_reviewed'&&q.guide)).toBe(true);}
 expect(reading.filter(q=>q.passage)).toHaveLength(64);expect(new Set(reading.filter(q=>q.passage).map(q=>q.passage!.id)).size).toBe(8);
 expect(questions.filter(q=>q.section==='mathematics'&&q.diagram)).toHaveLength(16);
});
it('keeps complete passage groups, two vocabulary items, and cooldown together',()=>{
 const picked=pickFresh(reading,'mixed',[],[],10,false,1000,()=>.5);
 expect(picked).toHaveLength(10);expect(picked.filter(q=>q.passage)).toHaveLength(8);expect(new Set(picked.filter(q=>q.passage).map(q=>q.passage!.id)).size).toBe(1);
 const seen:Exposure[]=[{questionId:picked[0].id,lastEncounteredAt:1000,lastSessionId:'old',encounterCount:1,outcomes:{}}];
 const available=availableQuestions(reading,'mixed',seen,[],2000);
 expect(available.some(q=>q.passage?.id===picked[0].passage!.id)).toBe(false);
 const fresh=pickFresh(reading,'mixed',seen,[],10,false,2000,()=>.5);expect(fresh).toHaveLength(10);expect(fresh[0].passage!.id).not.toBe(picked[0].passage!.id);
 expect(pickFresh(reading,'mixed',seen,[],10,true,2000,()=>.5)).toHaveLength(10);
});
it('offers complete eight-item focused comprehension sets and independent vocabulary',()=>{
 for(const skill of new Set(reading.filter(q=>q.passage).map(q=>q.skill))){const picked=pickFresh(reading,skill as Skill,[],[],10);expect(picked).toHaveLength(8);expect(picked.some(q=>q.skill===skill)).toBe(true);expect(new Set(picked.map(q=>q.passage!.id)).size).toBe(1);}
 expect(pickFresh(reading,'standalone_vocabulary',[],[],10).every(q=>!q.passage)).toBe(true);
 expect(pickFresh(reading,'main_idea',[],[],7)).toHaveLength(0);
});
it('snapshots and grades every new skill, passage and figure through backup round-trip',()=>{
 for(const section of Object.keys(sections)){const qs=questions.filter(q=>q.section===section);const s=planSession([{section:section as Section,questions:qs}],'burst','untimed',1000);for(const q of qs)s.responses[q.id].answer=q.guide!.correctChoiceId;s.status='submitted';s.completedAt=2000;const restored=parseBackup(JSON.stringify({format:'hspt-progress',version:1,sessions:[s],exposures:[]})).sessions[0];expect(restored).toEqual(s);expect(gradeSession(restored).correct).toBe(100);}
});
it('rejects missing passages, missing figures and cross-section formats',()=>{
 const q=reading.find(q=>q.passage)!;expect(()=>validateQuestion({...q,passage:undefined},true)).toThrow();
 const figure=questions.find(q=>q.section==='mathematics'&&q.diagram)!;expect(()=>validateQuestion({...figure,diagram:undefined},true)).toThrow();
 expect(()=>validateQuestion({...q,format:'synonyms'},true)).toThrow();
});
