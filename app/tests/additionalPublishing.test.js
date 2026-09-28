import {it,expect} from 'vitest';
import {readFileSync,cpSync,mkdtempSync,rmSync,writeFileSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
it('revalidates approval and rejects changed questions, passages, figures or decisions',()=>{
 const root=mkdtempSync(join(tmpdir(),'hspt-additional-'));const app=fileURLToPath(new URL('..',import.meta.url));
 try{
  for(const item of ['scripts','src/domain','content/releases','content/review','content/staging/gables-v2','content/staging/additional-v3','public/content'])cpSync(join(app,item),join(root,item),{recursive:true});
  const run=()=>spawnSync(process.execPath,[join(root,'scripts/content-release.mjs'),'validate'],{encoding:'utf8'});
  expect(run().status).toBe(0);
  for(const file of ['content/staging/additional-v3/verbal.json','content/staging/additional-v3/reading-passages.json','content/staging/additional-v3/assets/mat-a1-056.svg','content/review/additional-v3/decisions.json']){const dest=join(root,file),before=readFileSync(dest,'utf8');writeFileSync(dest,before+' ');expect(run().status).not.toBe(0);writeFileSync(dest,before);}
 }finally{rmSync(root,{recursive:true,force:true});}
});

it('imports the approved text, keys, figures and passages without editorial changes',()=>{
 const app=fileURLToPath(new URL('..',import.meta.url)),read=p=>JSON.parse(readFileSync(join(app,p),'utf8'));
 const runtime=read('public/content/banks/all-sections-v0002.json').questions;
 const base='content/staging/additional-v3/';const passages=read(base+'reading-passages.json').passages;
 for(const section of ['verbal','reading','mathematics','language'])for(const q of read(base+section+'.json').questions){
  const published=runtime.find(x=>x.id===q.id);
  for(const key of ['id','section','skill','format','difficulty','templateFamily','stem','choices','guide'])expect(published[key]).toEqual(q[key]);
  expect(published.provenance.authoringRevision).toBe(q.revision);expect(published.revision).toBe(1);
  if(q.diagram){expect(published.diagram.svg).toBe(readFileSync(join(app,base,q.diagram.file),'utf8').trim());expect(published.diagram.alt).toBe(q.diagram.alt);}
  if(q.passageId){const p=passages.find(x=>x.id===q.passageId);expect(published.passage.paragraphs).toEqual(p.paragraphs);expect(published.passage.revision).toBe(q.passageRevision);}
 }
});
