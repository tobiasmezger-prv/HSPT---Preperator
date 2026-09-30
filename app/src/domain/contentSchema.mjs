export const schemaVersion=1;
const skills=["algebra", "analogies", "antonyms", "author_purpose", "capitalization", "classification", "composition", "detail", "evidence", "geometry", "grammar", "inference", "literary_interpretation", "logical_reasoning", "main_idea", "measurement", "number_computation", "number_concepts", "punctuation", "ratios_percent", "spelling", "standalone_vocabulary", "statistics_probability", "structure", "synonyms", "tone", "usage", "vocabulary_context"].concat(['math_practice','verbal_practice','reading_comprehension','language_usage','sequence_additive','sequence_multiplicative','numeric_comparison','number_manipulation','symbolic_pattern','odd_one_out','geometric_comparison']);
const formats={"verbal": ["analogies", "antonyms", "classification", "logical_reasoning", "synonyms"], "reading": ["passage_author_purpose", "passage_detail", "passage_evidence", "passage_inference", "passage_literary_interpretation", "passage_main_idea", "passage_structure", "passage_tone", "passage_vocabulary_context", "standalone_vocabulary"], "mathematics": ["algebra", "conceptual", "figure_numeric", "geometry", "measurement", "number_computation", "ratios_percent", "statistics_probability"], "language": ["concision", "concluding_sentence", "error_detection", "irrelevant_sentence", "paragraph_insertion", "paragraph_order", "paragraph_revision", "pronoun_clarity", "sentence_combining", "spelling", "supporting_detail", "topic_sentence", "transition"], "quantitative": ["number_series", "number_manipulation", "nongeometric_comparison", "geometric_comparison"]};
const assert=(ok,message)=>{if(!ok)throw new Error(message);};
const text=x=>typeof x==='string'&&x.trim().length>0;
export function validateQuestion(q,published=false){
 assert(q&&typeof q==='object'&&text(q.id)&&/^[a-zA-Z0-9_-]+$/.test(q.id)&&skills.includes(q.skill)&&text(q.stem)&&text(q.templateFamily),'Invalid question fields');
 assert(Array.isArray(q.choices)&&[3,4].includes(q.choices.length)&&q.choices.every(text)&&new Set(q.choices.map(x=>x.trim())).size===q.choices.length,'Invalid choices');
 if(q.passage)assert(text(q.passage.id)&&text(q.passage.title)&&text(q.passage.text),'Invalid passage');
 if(q.passage?.paragraphs)assert(Array.isArray(q.passage.paragraphs)&&q.passage.paragraphs.length>0&&q.passage.paragraphs.every(text),'Invalid passage paragraphs');
 if(q.dummy!==undefined)assert(q.dummy===true&&!published,'Dummy questions cannot be published');
 if(q.variantGroupId!==undefined)assert(text(q.variantGroupId),'Invalid variant group');
 if(q.revision!==undefined)assert(Number.isInteger(q.revision)&&q.revision>0,'Invalid question revision');
 if(q.guide||published)assert(q.guide&&'ABCD'.slice(0,q.choices.length).includes(q.guide.correctChoiceId)&&q.guide.correctChoiceId.length===1&&text(q.guide.explanation)&&(!q.guide.shortcut||text(q.guide.shortcut)),'Invalid answer guide');
 if(published){
  assert(Object.hasOwn(formats,q.section)&&[1,2,3].includes(q.difficulty)&&formats[q.section].includes(q.format)&&Number.isInteger(q.revision)&&q.revision>0,'Unsupported question schema or format');
  assert(q.section!=='reading'||(q.format==='standalone_vocabulary'?!q.passage:!!q.passage),'Missing or unexpected reading passage');
  assert(q.acceptance?.batchStatus==='sample_reviewed'&&text(q.acceptance.batchId)&&['approved','not_individually_reviewed'].includes(q.acceptance.individualStatus)&&q.provenance&&text(q.provenance.origin),'Missing acceptance/provenance');
  assert(!['geometric_comparison','figure_numeric'].includes(q.format)||!!q.diagram||!!q.image,'Missing visual diagram');
 }
 if(q.image)assert(text(q.image.alt)&&typeof q.image.dataUrl==='string'&&q.image.dataUrl.length<2000000&&/^data:image\/(png|jpeg);base64,[A-Za-z0-9+/]+={0,2}$/.test(q.image.dataUrl),'Invalid source image');
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
 if(m.sectionCounts){assert(Object.keys(m.sectionCounts).length===5,'Invalid section index');for(const section of Object.keys(formats))assert(m.sectionCounts[section]===b.questions.filter(q=>(q.section??'quantitative')===section).length,'Section index count mismatch');}
 const ids=new Set(),signatures=new Set();
 for(const q of b.questions){validateQuestion(q,true);assert(!ids.has(q.id),'Duplicate question ID');ids.add(q.id);const signature=JSON.stringify([q.stem.toLowerCase().replace(/\s+/g,' ').trim(),q.choices.map(x=>x.trim()).sort(),q.diagram?.svg??q.image?.dataUrl??'',q.passage?.text??'']);assert(!signatures.has(signature),'Duplicate question');signatures.add(signature);}
 return b;
}
