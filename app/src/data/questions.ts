import bank from '../../content/staging/gables-v2/bank.json';
import type {Question} from '../domain/types';
const diagrams=import.meta.glob('../../content/staging/gables-v2/assets/*.svg',{query:'?raw',import:'default',eager:true}) as Record<string,string>;
// The batch passed a human sample review. The other 80 are not individually approved.
export const questions:Question[]=(bank as unknown as Question[]).map(q=>({...q,
 skill:q.format==='geometric_comparison'?'geometric_comparison':q.skill,
 reviewStatus:'sample_reviewed',
 diagram:q.visual?{svg:diagrams[`../../content/staging/gables-v2/assets/${q.id}.svg`],alt:q.visual.alt}:undefined
}));
export const activeSkills=[...new Set(questions.map(q=>q.skill))];
