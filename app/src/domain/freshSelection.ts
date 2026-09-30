import type {Question,Session,Skill} from './types';
export type Exposure={questionId:string;lastEncounteredAt:number;lastSessionId:string;encounterCount:number;outcomes:Record<string,'correct'|'incorrect'|'unanswered'|'ungraded'>};
export const cooldown={days:14,completedSessions:5};
export function availableQuestions(bank:Question[],focus:Skill|'mixed',exposures:Exposure[],sessions:Session[],now=Date.now(),review=false){
 const byId=new Map(exposures.map(e=>[e.questionId,e]));
 const exposure=(q:Question)=>byId.get(q.id)??(q.provenance?.priorId?byId.get(q.provenance.priorId):undefined);
 const eligible=bank.filter(q=>{const e=exposure(q);return !e||review||(now-e.lastEncounteredAt>=cooldown.days*86400000&&sessions.filter(s=>(s.status==='submitted'||s.status==='expired')&&s.id!==e.lastSessionId&&s.startedAt>e.lastEncounteredAt).length>=cooldown.completedSessions);});
 const ids=new Set(eligible.map(q=>q.id));
 // A passage is available only as a complete group. A skill focus includes its context questions.
 return eligible.filter(q=>{if(!q.passage)return focus==='mixed'||q.skill===focus;const group=bank.filter(x=>x.passage?.id===q.passage!.id);return group.every(x=>ids.has(x.id))&&(focus==='mixed'||group.some(x=>x.skill===focus));});
}
export function pickFresh(bank:Question[],focus:Skill|'mixed',exposures:Exposure[],sessions:Session[],count=10,review=false,now=Date.now(),random=Math.random):Question[]{
 const byId=new Map(exposures.map(e=>[e.questionId,e]));const get=(q:Question)=>byId.get(q.id)??(q.provenance?.priorId?byId.get(q.provenance.priorId):undefined);
 let pool=availableQuestions(bank,focus,exposures,sessions,now,review).map(q=>({q,e:get(q),random:random()}));
 if(pool.some(x=>x.q.passage)){
  const groups=new Map<string,typeof pool>();
  for(const x of pool)if(x.q.passage){const key=x.q.passage.id;groups.set(key,[...(groups.get(key)??[]),x]);}
  const ranked=[...groups.values()].sort((a,b)=>Number(a.some(x=>x.e))-Number(b.some(x=>x.e))||Math.max(0,...a.map(x=>x.e?.lastEncounteredAt??0))-Math.max(0,...b.map(x=>x.e?.lastEncounteredAt??0))||a[0].random-b[0].random);
  // Whole passage groups and individual vocabulary items form a bounded subset sum.
  // Keep the best-ranked first solution for each size; choose the largest exact fit.
  const singles=pool.filter(x=>!x.q.passage).sort((a,b)=>Number(!!a.e)-Number(!!b.e)||a.random-b.random).map(x=>[x]);
  const units=[...ranked,...singles].sort((a,b)=>Number(a.some(x=>x.e))-Number(b.some(x=>x.e)));const fits=new Map<number,Question[]>([[0,[]]]);
  for(const unit of units)for(const [size,chosen] of [...fits.entries()].sort((a,b)=>b[0]-a[0])){
   const next=size+unit.length;if(next<=count&&!fits.has(next))fits.set(next,[...chosen,...unit.map(x=>x.q).sort((a,b)=>a.id.localeCompare(b.id))]);
  }
  return fits.get(Math.max(...fits.keys()))??[];
 }
 const result:Question[]=[];const families=new Set<string>(),variants=new Set<string>();const category=new Map<string,number>(),skillCounts=new Map<string,number>(),difficulty=new Map<number,number>();
 while(result.length<count&&pool.length){
  const unseen=pool.filter(x=>!x.e);let candidates=unseen.length?unseen:pool;
  const diverse=candidates.filter(x=>!families.has(x.q.templateFamily)&&(!x.q.variantGroupId||!variants.has(x.q.variantGroupId)));if(diverse.length)candidates=diverse;
  candidates.sort((a,b)=>{if(a.e&&b.e&&a.e.lastEncounteredAt!==b.e.lastEncounteredAt)return a.e.lastEncounteredAt-b.e.lastEncounteredAt;return (category.get(a.q.format??a.q.skill)??0)-(category.get(b.q.format??b.q.skill)??0)||(skillCounts.get(a.q.skill)??0)-(skillCounts.get(b.q.skill)??0)||(difficulty.get(a.q.difficulty??1)??0)-(difficulty.get(b.q.difficulty??1)??0)||a.random-b.random;});
  const q=candidates[0].q;result.push(q);families.add(q.templateFamily);if(q.variantGroupId)variants.add(q.variantGroupId);category.set(q.format??q.skill,(category.get(q.format??q.skill)??0)+1);skillCounts.set(q.skill,(skillCounts.get(q.skill)??0)+1);difficulty.set(q.difficulty??1,(difficulty.get(q.difficulty??1)??0)+1);pool=pool.filter(x=>x.q.id!==q.id);
 }
 return result;
}
