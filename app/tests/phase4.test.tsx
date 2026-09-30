import 'fake-indexeddb/auto';
import {beforeEach,afterEach,it,expect,vi} from 'vitest';
import {deleteDB} from 'idb';
import {renderToStaticMarkup} from 'react-dom/server';
import {presets,testOrder,planSession,finishPart,advancePart,fullMinutes,sessionTitle} from '../src/domain/testPlan';
import {abort,complete,createSession} from '../src/domain/session';
import {abortPractice,beginPlannedPractice,installBank,saveSession,loadProgress,mergeProgress,deriveExposures} from '../src/domain/storage';
import {gradeSession} from '../src/domain/scoring';
import {parseBackup} from '../src/domain/backup';
import {availableQuestions,pickFresh} from '../src/domain/freshSelection';
import {validateQuestion,type Bank,type Manifest} from '../src/domain/contentSchema.mjs';
import type {Question,Session} from '../src/domain/types';
import ProgressSettings from '../src/components/ProgressSettings';
import bank from '../public/content/banks/all-sections-v0002.json';
import manifest from '../content/releases/all-sections-v0002.manifest.json';
const questions=bank.questions as unknown as Question[];
afterEach(()=>vi.restoreAllMocks());
beforeEach(async()=>{vi.spyOn(Date,'now').mockReturnValue(1000);await deleteDB('hspt-practice');await installBank({bank:bank as unknown as Bank,manifest:manifest as Manifest});});
it('uses actual HSPT counts, section deadlines and five-minute burst targets',()=>{
 expect(testOrder.map(s=>presets[s].burst)).toEqual([17,9,12,7,12]);expect(fullMinutes).toBe(143);
 for(const section of testOrder){const preset=presets[section],pool=questions.filter(q=>q.section===section);for(const kind of ['burst','section'] as const){const count=kind==='burst'?preset.burst:preset.questions;const picked=pickFresh(pool,'mixed',[],[],count);expect(picked).toHaveLength(count);const s=planSession([{section,questions:picked}],kind,'untimed',1000);expect(s.mode).toBe('timed');expect(s.actualQuestionCount).toBe(count);expect(s.deadlineAt).toBe(1000+(kind==='burst'?5:preset.minutes)*60000);expect(s.presetVersion).toBe('hspt-18min-v1');}}
});
it('keeps whole passages and finds an exact fit when greedy grouping cannot',()=>{
 const q=questions[0];const groups=[5,4,4].flatMap((size,g)=>Array.from({length:size},(_,i)=>({...q,id:`g${g}-${i}`,passage:{id:`p${g}`,title:'Passage',text:'Text'}})));
 expect(pickFresh(groups,'mixed',[],[],8,false,0,()=>0)).toHaveLength(8);expect(pickFresh(groups,'mixed',[],[],7,false,0,()=>0)).toHaveLength(5);
});
it('makes abort terminal across stale saves, timers and backup import and frees the next test',async()=>{
 const s=await beginPlannedPractice('verbal','full','timed',298,false,1000);const between=await saveSession(finishPart(s,2000),s);const ended=await abortPractice(s.id,3000);
 expect(ended.status).toBe('aborted');expect(ended.completedAt).toBeUndefined();expect(ended.deadlineAt).toBeUndefined();expect(await saveSession(advancePart(between,4000),between)).toEqual(ended);expect(await saveSession(complete(s,5000),s)).toEqual(ended);expect(()=>gradeSession(ended)).toThrow('no score');
 const progress=await loadProgress();expect(progress.exposures).toHaveLength(298);expect(progress.exposures.every(e=>!Object.keys(e.outcomes).length)).toBe(true);
 expect(parseBackup(JSON.stringify({format:'hspt-progress',version:1,...progress})).sessions[0]).toEqual(ended);
 await mergeProgress([s],deriveExposures([s]));expect((await loadProgress()).sessions[0].status).toBe('aborted');
 const next=await beginPlannedPractice('mathematics','burst','timed',7,false,5000);expect(next.id).not.toBe(s.id);
 const html=renderToStaticMarkup(<ProgressSettings view="progress" sessions={[ended]} installed={null} status="" checking={false} onCheck={()=>{}} onRefresh={async()=>{}} onReview={()=>{}}/>);expect(html).toContain('No completed practice yet.');expect(html).not.toContain('By skill');
});
it('aborts every mode without scoring or completed-session cooldown credit',async()=>{
 for(const kind of ['burst','section','full'] as const){await deleteDB('hspt-practice');await installBank({bank:bank as unknown as Bank,manifest:manifest as Manifest});const s=await beginPlannedPractice('quantitative',kind,'timed',9,false,1000);const ended=await abortPractice(s.id,2000);expect(abort(ended,3000)).toEqual(ended);expect(complete(ended,3000)).toEqual(ended);expect(parseBackup(JSON.stringify({format:'hspt-progress',version:1,sessions:[ended],exposures:[]})).sessions[0]).toEqual(ended);}
 const q=questions[0],old=createSession([q],'timed','mixed',0),ended=Array.from({length:5},(_,i)=>abort({...createSession([q],'timed','mixed',i+1)},100));expect(availableQuestions([q],'mixed',deriveExposures([old]),ended,20*86400000)).toHaveLength(0);
});
it('keeps historical untimed and preview snapshots unchanged',()=>{
 const old:Session={...createSession(questions.slice(0,10),'untimed','mixed',1000),testKind:'section',preview:true};const restored=parseBackup(JSON.stringify({format:'hspt-progress',version:1,sessions:[old],exposures:[]})).sessions[0];expect(restored).toEqual(old);expect(sessionTitle(restored)).toContain('preview');expect(restored.deadlineAt).toBeUndefined();
});
it('supports three real choices and refuses nonexistent answers in guides and backups',()=>{
 const q:Question={...questions[0],choices:['one','two','three'],guide:{...questions[0].guide!,correctChoiceId:'C'}};expect(()=>validateQuestion(q,true)).not.toThrow();expect(()=>validateQuestion({...q,guide:{...q.guide,correctChoiceId:'D'}})).toThrow();const s=createSession([q],'timed','mixed',1000);s.responses[q.id].answer='D';expect(()=>parseBackup(JSON.stringify({format:'hspt-progress',version:1,sessions:[s],exposures:[]}))).toThrow();
});
it('locks late answers after background expiry and keeps subsequent clocks stopped',async()=>{
 const s=await beginPlannedPractice('verbal','full','timed',298,false,1000);const q=s.questions[0];const late={...s,responses:{...s.responses,[q.id]:{...s.responses[q.id],answer:q.guide!.correctChoiceId}}};
 const stored=await saveSession(late,s,s.deadlineAt!+1000);expect(stored.stage).toBe('break');expect(stored.responses[q.id].answer).toBeNull();expect(stored.parts![0].completedAt).toBe(s.deadlineAt);expect(stored.parts![1].startedAt).toBeUndefined();expect(await saveSession(late,s,s.deadlineAt!+2000)).toEqual(stored);
});
it('rejects altered preset metadata without rewriting legacy sessions',async()=>{
 const s=await beginPlannedPractice('verbal','full','timed',298,false,1000);const parse=(value:Session)=>parseBackup(JSON.stringify({format:'hspt-progress',version:1,sessions:[value],exposures:[]}));expect(()=>parse({...s,durationMs:1})).toThrow();expect(()=>parse({...s,actualQuestionCount:50})).toThrow();expect(()=>parse({...s,deadlineAt:s.deadlineAt!+1})).toThrow();
});
