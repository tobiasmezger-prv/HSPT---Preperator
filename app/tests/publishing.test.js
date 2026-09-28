import {it,expect} from 'vitest';
import {mkdtempSync,cpSync,mkdirSync,readFileSync,writeFileSync,rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join,resolve} from 'node:path';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
it('owner workflow builds immutable accepted releases, validates targets, activates and rolls back; refuses stale approval',()=>{
 const root=mkdtempSync(join(tmpdir(),'hspt-release-test-'));const app=fileURLToPath(new URL('..',import.meta.url));
 try{
  for(const path of ['scripts','src/domain','content/staging','content/review'])mkdirSync(join(root,path),{recursive:true});
  cpSync(join(app,'scripts/content-release.mjs'),join(root,'scripts/content-release.mjs'));
  cpSync(join(app,'scripts/accepted-additional.mjs'),join(root,'scripts/accepted-additional.mjs')); 
  cpSync(join(app,'src/domain/contentSchema.mjs'),join(root,'src/domain/contentSchema.mjs'));
  cpSync(join(app,'content/staging/gables-v2'),join(root,'content/staging/gables-v2'),{recursive:true});cpSync(join(app,'content/review/gables-v2'),join(root,'content/review/gables-v2'),{recursive:true});
  const run=(...args)=>spawnSync(process.execPath,[join(root,'scripts/content-release.mjs'),...args],{encoding:'utf8'});
  const build=(id,...args)=>run('build','--release',id,'--batch','content/staging/gables-v2','--review','content/review/gables-v2',...args);
  expect(build('first').status).toBe(0);expect(run('publish','--release','first').status).toBe(0);expect(run('validate').status).toBe(0);expect(build('first').status).not.toBe(0);
  expect(build('second','--retire','gb2-001').status).toBe(0);expect(run('preview','--release','second').status).toBe(0);expect(JSON.parse(readFileSync(join(root,'public/content/manifest.json'),'utf8')).questionCount).toBe(99);
  expect(run('rollback','--release','first').status).toBe(0);expect(JSON.parse(readFileSync(join(root,'public/content/manifest.json'),'utf8')).questionCount).toBe(100);
  const file=join(root,'content/staging/gables-v2/bank.json');writeFileSync(file,readFileSync(file,'utf8')+' ');expect(build('stale').status).not.toBe(0);
 }finally{rmSync(root,{recursive:true,force:true});}
});
