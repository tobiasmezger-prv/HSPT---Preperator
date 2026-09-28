// Import the exact reviewed draft. Keep authored revisions separate from published revisions.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const digest=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const requireThat=(ok,message)=>{if(!ok)throw new Error(message);};
export function acceptedAdditional(dir,reviewDir,root){
 const approval=read(path.join(reviewDir,'decisions.json'));
 requireThat(approval.schemaVersion==='additional-acceptance-1'&&approval.status==='sample_reviewed'&&approval.reviewer&&approval.date,'Incomplete additional-bank approval');
 const manifest=read(path.join(dir,'manifest.json'));
 const required=['manifest.json','validation.json','item-audit.json','visual-review.json','overlap-log.json','mathematics-checks.json','logic-checks.json','source-calibration.json','source-coverage.json','source-exceptions.json','sources.json','author-review-notes.json','reading-passages.json'];
 const sections=['verbal','reading','mathematics','language'];
 required.push(...sections.flatMap(s=>[`${s}.json`,`review/${s}-sample.json`]),...Object.keys(manifest.assets));
 for(const file of required){requireThat(!file.includes('..')&&!path.isAbsolute(file),'Unsafe evidence path');requireThat(approval.files[file]===digest(path.join(dir,file)),'Stale acceptance evidence: '+file);}
 const same=(a,b)=>a.length===b.length&&new Set(a).size===a.length&&a.every(id=>b.includes(id));
 const passages=read(path.join(dir,'reading-passages.json')).passages;
 const reviewed=new Set(),bank=[];
 for(const section of sections){
  const entry=manifest.sections[section],file=path.join(dir,`${section}.json`);
  requireThat(entry.sha256===digest(file),'Stale section manifest');
  const draft=read(file).questions;
  requireThat(draft.length===100&&draft.every(q=>q.section===section),'Incomplete section');
  const sample=read(path.join(dir,`review/${section}-sample.json`));
  requireThat(sample.bankSha256===entry.sha256&&sample.questionIds.length===20&&same(sample.questionIds,approval.sampleIds[section])&&sample.questionIds.every(id=>draft.some(q=>q.id===id)),'Stale sample');
  if(section==='reading')requireThat(sample.passageSha256===digest(path.join(dir,'reading-passages.json')),'Stale passage review');
  for(const [asset,sha] of Object.entries(sample.assetHashes))requireThat(digest(path.join(dir,'assets',asset+'.svg'))===sha,'Stale sample figure');
  sample.questionIds.forEach(id=>reviewed.add(id));
  for(const q of draft){
   const {diagram,passageId,passageRevision,oracleExpression,...fields}=q;
   const next={...fields,revision:1,sourceType:'original_reviewed',provenance:{...q.provenance,origin:'original_agent_authored',authoringRevision:q.revision}};
   if(diagram)next.diagram={svg:fs.readFileSync(path.join(dir,diagram.file),'utf8').trim(),alt:diagram.alt};
   if(passageId){const passage=passages.find(p=>p.id===passageId&&p.revision===passageRevision);requireThat(passage,'Missing reviewed passage');next.passage={id:passage.id,revision:passage.revision,title:passage.title,paragraphs:passage.paragraphs,text:passage.paragraphs.join('\n\n')};}
   bank.push(next);
  }
 }
 requireThat(same(approval.items.map(x=>x.id),[...reviewed])&&approval.items.every(x=>x.decision==='approve'),'Human sample approval incomplete');
 const audit=read(path.join(dir,'item-audit.json')),visual=read(path.join(dir,'visual-review.json')),overlap=read(path.join(dir,'overlap-log.json')),math=read(path.join(dir,'mathematics-checks.json')),coverage=read(path.join(dir,'source-coverage.json'));
 requireThat(audit.manifestSha256===digest(path.join(dir,'manifest.json'))&&same(audit.items.map(x=>x.id),bank.map(q=>q.id))&&audit.items.every(x=>x.structural==='passed'&&['agent_review_no_defect_identified','prior_full_review_reused_unchanged_semantics'].includes(x.answerReview)),'Incomplete item audit');
 requireThat(visual.manifestSha256===digest(path.join(dir,'manifest.json'))&&same(visual.figures.map(x=>x.id),bank.filter(q=>q.diagram).map(q=>q.id))&&visual.figures.every(x=>x.status==='agent_browser_visual_check_passed'),'Incomplete figure review');
 requireThat(!overlap.flags.length&&!overlap.targetHits.length&&!overlap.passageFlags.length&&same(overlap.items.map(x=>x.id),bank.map(q=>q.id))&&overlap.items.every(x=>x.resolution==='no_distinctive_copy_identified'),'Unresolved source overlap');
 requireThat(math.bankSha256===manifest.sections.mathematics.sha256&&math.numericChecks.length===88&&math.numericChecks.every(x=>x.status==='exact_expression_check_passed'),'Incomplete math evidence');
 requireThat(coverage.totalQuestionPositions===894&&coverage.items.length===894&&coverage.totalPdfPages===156,'Incomplete source coverage');
 const sha=digest(path.join(dir,'manifest.json'));
 return {bank,sha,reviewed,evidence:{kind:'additional-v3',batchDir:path.relative(root,dir),reviewDir:path.relative(root,reviewDir),bankSha256:sha,decisionsSha256:digest(path.join(reviewDir,'decisions.json'))}};
}
