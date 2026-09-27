import type {Question,Session,Skill} from './types';
export type Exposure={questionId:string;lastEncounteredAt:number;lastSessionId:string;encounterCount:number;outcomes:Record<string,'correct'|'incorrect'|'unanswered'|'ungraded'>};
export const cooldown={days:14,completedSessions:5};
export function availableQuestions(bank:Question[],focus:Skill|'mixed',exposures:Exposure[],sessions:Session[],now=Date.now(),review=false){
 const byId=new Map(exposures.map(e=>[e.questionId,e]));
 const exposure=(q:Question)=>byId.get(q.id)??(q.provenance?.priorId?byId.get(q.provenance.priorId):undefined);
 return bank.filter(q=>focus==='mixed'||q.skill===focus).filter(q=>{const e=exposure(q);return !e||review||(now-e.lastEncounteredAt>=cooldown.days*86400000&&sessions.filter(s=>s.status!=='active'&&s.id!==e.lastSessionId&&s.startedAt>e.lastEncounteredAt).length>=cooldown.completedSessions);});
}
export function pickFresh(bank:Question[],focus:Skill|'mixed',exposures:Exposure[],sessions:Session[],count=10,review=false,now=Date.now(),random=Math.random){
 const byId=new Map(exposures.map(e=>[e.questionId,e]));const get=(q:Question)=>byId.get(q.id)??(q.provenance?.priorId?byId.get(q.provenance.priorId):undefined);
 let pool=availableQuestions(bank,focus,exposures,sessions,now,review).map(q=>({q,e:get(q),random:random()}));
 const result:Question[]=[];const families=new Set<string>(),variants=new Set<string>();const category=new Map<string,number>(),skillCounts=new Map<string,number>(),difficulty=new Map<number,number>();
 while(result.length<count&&pool.length){
  const unseen=pool.filter(x=>!x.e);let candidates=unseen.length?unseen:pool;
  const diverse=candidates.filter(x=>!families.has(x.q.templateFamily)&&(!x.q.variantGroupId||!variants.has(x.q.variantGroupId)));if(diverse.length)candidates=diverse;
  candidates.sort((a,b)=>{if(a.e&&b.e&&a.e.lastEncounteredAt!==b.e.lastEncounteredAt)return a.e.lastEncounteredAt-b.e.lastEncounteredAt;return (category.get(a.q.format??a.q.skill)??0)-(category.get(b.q.format??b.q.skill)??0)||(skillCounts.get(a.q.skill)??0)-(skillCounts.get(b.q.skill)??0)||(difficulty.get(a.q.difficulty??1)??0)-(difficulty.get(b.q.difficulty??1)??0)||a.random-b.random;});
  const q=candidates[0].q;result.push(q);families.add(q.templateFamily);if(q.variantGroupId)variants.add(q.variantGroupId);category.set(q.format??q.skill,(category.get(q.format??q.skill)??0)+1);skillCounts.set(q.skill,(skillCounts.get(q.skill)??0)+1);difficulty.set(q.difficulty??1,(difficulty.get(q.difficulty??1)??0)+1);pool=pool.filter(x=>x.q.id!==q.id);
 }
 return result;
}
