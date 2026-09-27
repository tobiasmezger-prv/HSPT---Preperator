import type {Question,Session,Skill} from './types';
export function remaining(session:Session,now=Date.now()){return session.deadlineAt===undefined ? null : Math.max(0,session.deadlineAt-now);}
export function createSession(questions:Question[],mode:Session['mode'],skill:Skill|'mixed',now=Date.now()):Session {return {id:crypto.randomUUID(),mode,skill,questions,startedAt:now,deadlineAt:mode==='timed'?now+300000:undefined,status:'active',responses:Object.fromEntries(questions.map(q=>[q.id,{answer:null,flagged:false,approximateActiveMs:0}]))};}
export function complete(session:Session,now=Date.now()):Session {if(session.status!=='active')return session;const expired=remaining(session,now)===0;return {...session,status:expired?'expired':'submitted',completedAt:expired?session.deadlineAt:now};}
export function selectQuestions(bank:Question[],skill:Skill|'mixed',seen:string[]=[],random=Math.random):Question[]{
 const exposure=new Set(seen);
 const wasSeen=(q:Question)=>exposure.has(q.id)||!!(q.provenance?.priorId&&exposure.has(q.provenance.priorId));
 const eligible=bank.filter(q=>skill==='mixed'||q.skill===skill)
  .map(q=>({q,rank:random()})).sort((a,b)=>a.rank-b.rank).map(x=>x.q);
 const selected:Question[]=[];
 const ids=new Set<string>();
 const families=new Set<string>();
 const counts=new Map<string,number>();
 const category=(q:Question)=>q.format??q.skill;
 // Unseen status takes priority over coverage when a category is exhausted.
 // Within each pool, balance skills and avoid a second item from a family.
 for(const encountered of [false,true]){
  const pool=eligible.filter(q=>wasSeen(q)===encountered);
  for(const allowRepeatedFamily of [false,true]){
   while(selected.length<10){
    const candidates=pool.filter(q=>!ids.has(q.id)&&(allowRepeatedFamily||!families.has(q.templateFamily)));
    if(!candidates.length)break;
    candidates.sort((a,b)=>(counts.get(category(a))??0)-(counts.get(category(b))??0));
    const q=candidates[0];selected.push(q);ids.add(q.id);families.add(q.templateFamily);counts.set(category(q),(counts.get(category(q))??0)+1);
   }
  }
 }
 return selected;
}
