import 'fake-indexeddb/auto';
import {beforeEach,it,expect} from 'vitest';
import {deleteDB} from 'idb';
import {renderToStaticMarkup} from 'react-dom/server';
import release from '../public/content/banks/all-sections-v0003.json';
import manifest from '../content/releases/all-sections-v0003.manifest.json';
import prior from '../public/content/banks/all-sections-v0002.json';
import priorManifest from '../content/releases/all-sections-v0002.manifest.json';
import {validateBank,type Bank,type Manifest} from '../src/domain/contentSchema.mjs';
import {pickFresh} from '../src/domain/freshSelection';
import {presets,testOrder,planSession} from '../src/domain/testPlan';
import {installBank,loadProgress,beginPlannedPractice,abortPractice,saveSession} from '../src/domain/storage';
import {complete} from '../src/domain/session';
import QuestionDiagram from '../src/components/QuestionDiagram';
const bank=release as unknown as Bank,questions=bank.questions;
beforeEach(async()=>{await deleteDB('hspt-practice');});
it('appends 1191 checked source questions without changing any existing question or identifier',()=>{
 expect(()=>validateBank(bank,manifest as Manifest)).not.toThrow();
 expect(questions).toHaveLength(1691);
 const current=new Map(questions.map(q=>[q.id,q]));
 for(const q of prior.questions)expect(current.get(q.id)).toEqual(q);
 const added=questions.filter(q=>q.sourceType==='source_import');expect(added).toHaveLength(1191);
 expect(current.has('gables-3-083')).toBe(false);expect(current.has('gables-2-066')).toBe(true);
 expect(manifest.sectionCounts).toEqual({verbal:340,quantitative:307,reading:348,mathematics:356,language:340});
 expect(added.filter(q=>q.acceptance?.individualStatus==='approved')).toHaveLength(100);
});
it('ships complete text, valid guides, whole passages and safe vector diagrams without page scans',()=>{
 const added=questions.filter(q=>q.sourceType==='source_import');
 for(const q of added){expect(q.guide!.explanation.trim(),q.id).not.toBe('');expect(q.image,q.id).toBeUndefined();expect(q.stem,q.id).not.toMatch(/\[[^\]]*missing|Incomplete expression/);expect(q.guide!.explanation,q.id).not.toMatch(/PDF PAGE|\.indd|[\x00-\x08\x0b\x0c\x0e-\x1f]/);}
 const figures=added.filter(q=>q.diagram);expect(figures).toHaveLength(57);
 for(const q of figures){expect(q.diagram!.svg).not.toMatch(/<image|data:image\/|\.jpe?g/i);expect(renderToStaticMarkup(<QuestionDiagram question={q}/>)).toContain('data:image/svg+xml');}
 expect(new Set(added.filter(q=>q.passage).map(q=>q.passage!.id)).size).toBe(18);expect(added.filter(q=>q.passage)).toHaveLength(160);
});
it('selects exact Phase IV bursts and full sections with complete passage groups from the expanded release',()=>{
 for(let round=0;round<5;round++)for(const section of testOrder){
  const pool=questions.filter(q=>q.section===section);
  for(const kind of ['burst','section'] as const){const size=kind==='burst'?presets[section].burst:presets[section].questions,picked=pickFresh(pool,'mixed',[],[],size,false,1000);expect(picked).toHaveLength(size);expect(new Set(picked.map(q=>q.id)).size).toBe(size);
   for(const id of new Set(picked.filter(q=>q.passage).map(q=>q.passage!.id)))expect(picked.filter(q=>q.passage?.id===id).length).toBe(pool.filter(q=>q.passage?.id===id).length);
   const s=planSession([{section,questions:picked}],kind,'timed',1000);expect(s.deadlineAt).toBe(1000+(kind==='burst'?5:presets[section].minutes)*60000);
  }
 }
});
it('upgrades the actual previous release without losing progress or altering saved question snapshots',async()=>{
 await installBank({bank:prior as unknown as Bank,manifest:priorManifest as Manifest});
 const old=await beginPlannedPractice('quantitative','burst','timed',9,false,1000);await saveSession(complete(old,2000));const before=await loadProgress();
 await installBank({bank,manifest:manifest as Manifest});const after=await loadProgress();expect(after.sessions).toEqual(before.sessions);expect(after.exposures).toEqual(before.exposures);
 const full=await beginPlannedPractice('verbal','full','timed',298,false,3000);expect(full.questions).toHaveLength(298);expect(full.parts!.map(p=>p.questionIds.length)).toEqual([60,52,62,64,60]);
 const oldIds=new Set(old.questions.map(q=>q.id));expect(full.questions.some(q=>oldIds.has(q.id))).toBe(false);
 await abortPractice(full.id,4000);const next=await beginPlannedPractice('verbal','full','timed',298,false,5000);expect(next.questions.some(q=>full.questions.some(p=>p.id===q.id))).toBe(false);
});
