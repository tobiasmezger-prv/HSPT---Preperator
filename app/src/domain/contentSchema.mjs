export const schemaVersion=1;
const skills=['sequence_additive','sequence_multiplicative','numeric_comparison','number_manipulation','symbolic_pattern','odd_one_out','geometric_comparison'];
const formats=['number_series','number_manipulation','nongeometric_comparison','geometric_comparison'];
const assert=(ok,message)=>{if(!ok)throw new Error(message);};
const text=x=>typeof x==='string'&&x.trim().length>0;
export function validateQuestion(q,published=false){
 assert(q&&typeof q==='object'&&text(q.id)&&/^[a-zA-Z0-9_-]+$/.test(q.id)&&skills.includes(q.skill)&&text(q.stem)&&text(q.templateFamily),'Invalid question fields');
 assert(Array.isArray(q.choices)&&q.choices.length===4&&q.choices.every(text)&&new Set(q.choices.map(x=>x.trim())).size===4,'Invalid choices');
 if(q.variantGroupId!==undefined)assert(text(q.variantGroupId),'Invalid variant group');
 if(q.revision!==undefined)assert(Number.isInteger(q.revision)&&q.revision>0,'Invalid question revision');
 if(q.guide||published)assert(q.guide&&'ABCD'.includes(q.guide.correctChoiceId)&&q.guide.correctChoiceId.length===1&&text(q.guide.explanation)&&(!q.guide.shortcut||text(q.guide.shortcut)),'Invalid answer guide');
 if(published){
  assert(q.section==='quantitative'&&[1,2,3].includes(q.difficulty)&&formats.includes(q.format)&&Number.isInteger(q.revision)&&q.revision>0,'Unsupported question schema or format');
  assert(q.acceptance?.batchStatus==='sample_reviewed'&&text(q.acceptance.batchId)&&['approved','not_individually_reviewed'].includes(q.acceptance.individualStatus)&&q.provenance&&text(q.provenance.origin),'Missing acceptance/provenance');
  assert(q.format!=='geometric_comparison'||!!q.diagram,'Missing visual diagram');
 }
 if(q.diagram){
  assert(text(q.diagram.alt)&&text(q.diagram.svg)&&q.diagram.svg.length<100000,'Invalid diagram');
  const svg=q.diagram.svg;
  assert(svg.startsWith('<svg ')&&svg.endsWith('</svg>')&&!/<!|<\?|\bon\w+\s*=|href\s*=|url\s*\(|javascript:|data:/i.test(svg),'Unsafe diagram');
  const tags=[...svg.matchAll(/<\/?([\w:-]+)/g)].map(x=>x[1]);
  assert(tags.every(t=>['svg','title','rect','g','text','path','circle','line','polyline','polygon'].includes(t)),'Unsupported diagram element');
 }
 return q;
}
export function validateManifest(m){
 assert(m&&m.schemaVersion===1&&text(m.releaseId)&&/^[a-zA-Z0-9_-]+$/.test(m.releaseId)&&Number.isFinite(Date.parse(m.publishedAt)),'Unsupported manifest');
 assert(typeof m.bankUrl==='string'&&/^\/content\/banks\/[a-zA-Z0-9_-]+\.json$/.test(m.bankUrl),'Invalid bank URL');
 assert(Number.isInteger(m.questionCount)&&m.questionCount>0&&/^[a-f0-9]{64}$/.test(m.checksum),'Invalid bank count/checksum');return m;
}
export function validateBank(b,m){
 validateManifest(m);assert(b&&b.schemaVersion===1&&b.releaseId===m.releaseId&&Array.isArray(b.questions)&&b.questions.length===m.questionCount,'Bank does not match manifest');
 const ids=new Set(),signatures=new Set();
 for(const q of b.questions){validateQuestion(q,true);assert(!ids.has(q.id),'Duplicate question ID');ids.add(q.id);const signature=JSON.stringify([q.stem.toLowerCase().replace(/\s+/g,' ').trim(),q.choices.map(x=>x.trim()).sort(),q.diagram?.svg??'']);assert(!signatures.has(signature),'Duplicate question');signatures.add(signature);}
 return b;
}
