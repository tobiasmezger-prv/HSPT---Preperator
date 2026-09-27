import expanded from './questions.expanded.json';
import {answers} from './answers';
import type {Question} from '../domain/types';
// Original practice drafts. No item is represented as independently human-reviewed.
const fixture:Question[]=[
 {id:'dev-01',skill:'sequence_additive',stem:'What number comes next?  7, 12, 17, 22, …',choices:['25','26','27','29'],templateFamily:'constant-addition'},
 {id:'dev-02',skill:'sequence_additive',stem:'What number comes next?  2, 5, 9, 14, 20, …',choices:['25','26','27','28'],templateFamily:'increasing-differences'},
 {id:'dev-03',skill:'sequence_multiplicative',stem:'What number comes next?  3, 6, 12, 24, …',choices:['30','36','42','48'],templateFamily:'doubling'},
 {id:'dev-04',skill:'numeric_comparison',stem:'Which value is greatest?',choices:['3/5','0.58','59%','0.61'],templateFamily:'mixed-comparison'},
 {id:'dev-05',skill:'number_manipulation',stem:'What is 25% of 84?',choices:['18','21','24','28'],templateFamily:'quarter'},
 {id:'dev-06',skill:'symbolic_pattern',stem:'Each pair follows the rule “multiply the input by 3, then add 1.”  2 → 7, 4 → 13, 6 → ?',choices:['16','18','19','21'],templateFamily:'mapping'},
 {id:'dev-07',skill:'odd_one_out',stem:'Which number is not a multiple of 6?',choices:['18','24','32','42'],templateFamily:'multiples'},
 {id:'dev-08',skill:'number_manipulation',stem:'A number is doubled, then 9 is added. The result is 35. What was the original number?',choices:['12','13','17','22'],templateFamily:'reverse-operations'},
 {id:'dev-09',skill:'sequence_multiplicative',stem:'What number comes next?  160, 80, 40, 20, …',choices:['5','8','10','15'],templateFamily:'halving'},
 {id:'dev-10',skill:'numeric_comparison',stem:'Which fraction is equal to 0.375?',choices:['3/4','3/8','5/8','1/3'],templateFamily:'fraction-equivalence'},
 {id:'dev-11',skill:'symbolic_pattern',stem:'The symbol ★ means “add the two numbers, then double the sum.” What is 4 ★ 7?',choices:['18','22','28','32'],templateFamily:'symbol-operation'},
 {id:'dev-12',skill:'odd_one_out',stem:'Which number is not a perfect square?',choices:['16','25','36','48'],templateFamily:'squares'}
];

export const legacyQuestions:Question[]=[...fixture.map((q,i)=>({...q,section:'quantitative' as const,difficulty:([1,2,1,2,1,1,1,2,1,2,2,1] as const)[i],reviewStatus:'pending_human_review' as const,sourceType:'original_draft' as const,guide:answers[q.id]})),...expanded as Question[]];
