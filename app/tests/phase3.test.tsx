import 'fake-indexeddb/auto';
import {beforeEach,it,expect} from 'vitest';
import {deleteDB} from 'idb';
import {renderToStaticMarkup} from 'react-dom/server';
import {previewQuestions} from './fixtures/legacyPreviewQuestions';
import {validateQuestion,type Bank,type Manifest} from '../src/domain/contentSchema.mjs';
import {beginPlannedPractice,installBank,loadProgress,saveSession} from '../src/domain/storage';
import {finishPart,advancePart,visibleSession,testOrder,testDuration} from '../src/domain/testPlan';
import {parseBackup} from '../src/domain/backup';
import {gradeSession} from '../src/domain/scoring';
import {bankLabel} from '../src/components/QuestionDiagram';
import Results from '../src/components/Results';
import bank from '../public/content/banks/all-sections-v0002.json';
import manifest from '../content/releases/all-sections-v0002.manifest.json';
beforeEach(async()=>{await deleteDB('hspt-practice');await installBank({bank:bank as unknown as Bank,manifest:manifest as Manifest});});
it('keeps historical dummy snapshots readable but unpublishable',()=>{
 for(const section of ['mathematics','verbal','reading','language']){const items=previewQuestions.filter(q=>q.section===section);expect(items).toHaveLength(10);for(const q of items){expect(()=>validateQuestion(q)).not.toThrow();expect(()=>validateQuestion(q,true)).toThrow();expect(q.dummy).toBe(true);}}
 expect(new Set(previewQuestions.map(q=>q.id)).size).toBe(40);expect(previewQuestions.filter(q=>q.section==='reading').every(q=>q.passage?.text)).toBe(true);expect(bankLabel(previewQuestions)).toContain('not fully checked');
});
it('reserves five sections atomically and reuses an active test across tabs',async()=>{
 const [a,b]=await Promise.all([beginPlannedPractice('quantitative','full','timed',50),beginPlannedPractice('verbal','burst','timed',10)]);expect(a.id).toBe(b.id);expect(a.questions).toHaveLength(50);expect(a.parts?.map(p=>p.section)).toEqual(testOrder);expect((await loadProgress()).exposures).toHaveLength(50);expect(visibleSession(a).questions).toHaveLength(10);const reading=a.questions.filter(q=>q.section==='reading');expect(reading.filter(q=>q.passage)).toHaveLength(8);expect(new Set(reading.filter(q=>q.passage).map(q=>q.passage!.id)).size).toBe(1);
});
it('preserves answers through expiry, saved breaks, backups and per-section deadlines',async()=>{
 let s=await beginPlannedPractice('quantitative','full','timed',50,false,1000);
 const first=s.questions[0];s.responses[first.id].answer=first.guide!.correctChoiceId;s=await saveSession(s);
 const old=s;s=await saveSession(finishPart(s,301000),s);expect(s.stage).toBe('break');expect(s.status).toBe('active');expect(s.deadlineAt).toBeUndefined();expect(s.parts![0].expired).toBe(true);
 const data=await loadProgress();expect(parseBackup(JSON.stringify({format:'hspt-progress',version:1,...data})).sessions[0]).toEqual(s);
 expect(await saveSession({...old,responses:{...old.responses}},old)).toEqual(s);expect(await saveSession(old)).toEqual(s);
 let before=s;s=await saveSession(advancePart(s,900000),before);expect(s.partIndex).toBe(1);expect(s.deadlineAt).toBe(1200000);expect(s.responses[first.id].answer).toBe(first.guide!.correctChoiceId);
 expect((await saveSession(advancePart(before,950000),before)).deadlineAt).toBe(1200000);
 for(let i=1;i<5;i++){before=s;s=await saveSession(finishPart(s,900020+i*20),before);if(i<4){before=s;s=await saveSession(advancePart(s,900030+i*20),before);}}
 expect(s.status).toBe('submitted');expect(testDuration(s)).toBeLessThan(s.completedAt!-s.startedAt);expect(gradeSession(s).total).toBe(50);expect(gradeSession(s).correct).toBe(1);
 expect(renderToStaticMarkup(<Results session={s} onHome={()=>{}} onPractice={()=>{}}/>)).not.toContain('Dummy questions');
});
it('exhausts the real 100-item section without repeats and allows explicit review',async()=>{
 const ids=new Set<string>();
 for(let i=0;i<10;i++){const s=await beginPlannedPractice('language','section','untimed',10,false,1000+i*100);for(const q of s.questions){expect(ids.has(q.id)).toBe(false);ids.add(q.id);}await saveSession(finishPart(s,1050+i*100),s);}
 expect(ids.size).toBe(100);
 await expect(beginPlannedPractice('language','burst','timed',10,false,3000)).rejects.toThrow('Available questions');
 const review=await beginPlannedPractice('language','burst','timed',10,true,3000);expect(review.questions).toHaveLength(10);expect(review.practiceKind).toBe('review');
});
it('rejects broken full-test metadata in backups',async()=>{
 const s=await beginPlannedPractice('reading','full','timed',50);s.partIndex=8;expect(()=>parseBackup(JSON.stringify({format:'hspt-progress',version:1,sessions:[s],exposures:[]}))).toThrow();
});
