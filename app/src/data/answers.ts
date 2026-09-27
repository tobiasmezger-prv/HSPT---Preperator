import type {Choice} from '../domain/types';
export type AnswerGuide = {correctChoiceId:Choice;explanation:string;shortcut:string};
// Development content: mathematically checked, awaiting independent human review.
export const answers:Record<string,AnswerGuide> = {
 'dev-01':{correctChoiceId:'C',explanation:'Each term increases by 5: 7 + 5 = 12, 12 + 5 = 17, and 17 + 5 = 22. Add 5 again to get 27.',shortcut:'Check the gaps between consecutive terms. If they stay the same, add that gap once more.'},
 'dev-02':{correctChoiceId:'C',explanation:'The differences are 3, 4, 5, and 6. The next difference is 7, so 20 + 7 = 27.',shortcut:'If the gaps change, write the gaps as a second sequence. Here they increase by 1.'},
 'dev-03':{correctChoiceId:'D',explanation:'Each number is twice the previous number. Doubling 24 gives 48.',shortcut:'When the gaps grow quickly, check multiplication before looking for an addition rule.'},
 'dev-04':{correctChoiceId:'D',explanation:'Write all four values as decimals: 3/5 = 0.60, 0.58 stays 0.58, 59% = 0.59, and 0.61 stays 0.61. The greatest is 0.61.',shortcut:'Compare hundredths: 60, 58, 59, and 61. Use the same form for every value.'},
 'dev-05':{correctChoiceId:'B',explanation:'25% is one quarter. Divide 84 by 4 to get 21.',shortcut:'For 25%, halve the number twice: 84 → 42 → 21.'},
 'dev-06':{correctChoiceId:'C',explanation:'Apply the stated rule to 6: multiply by 3 to get 18, then add 1 to get 19.',shortcut:'Follow the operations in their stated order: multiply first, then add.'},
 'dev-07':{correctChoiceId:'C',explanation:'18 = 6 × 3, 24 = 6 × 4, and 42 = 6 × 7. But 32 is not divisible by 6, so it is the odd one out.',shortcut:'A multiple of 6 must be even and divisible by 3. The digits of 32 add to 5, which is not divisible by 3.'},
 'dev-08':{correctChoiceId:'B',explanation:'Undo the last operation first: 35 − 9 = 26. Then undo doubling: 26 ÷ 2 = 13. Check: 13 × 2 + 9 = 35.',shortcut:'Work backward with inverse operations, in reverse order.'},
 'dev-09':{correctChoiceId:'C',explanation:'Each term is half the previous term: 160 → 80 → 40 → 20. Half of 20 is 10.',shortcut:'Check whether each term is multiplied or divided by the same number.'},
 'dev-10':{correctChoiceId:'B',explanation:'0.375 = 375/1000. Dividing numerator and denominator by 125 gives 3/8.',shortcut:'Remember that 1/8 = 0.125. Three eighths is 3 × 0.125 = 0.375.'},
 'dev-11':{correctChoiceId:'B',explanation:'The symbol tells you to add first, then double: 4 + 7 = 11, and 11 × 2 = 22.',shortcut:'Replace the unfamiliar symbol with the stated rule: 2 × (4 + 7).'},
 'dev-12':{correctChoiceId:'D',explanation:'16 = 4², 25 = 5², and 36 = 6². The number 48 lies between 6² = 36 and 7² = 49, so it is not a perfect square.',shortcut:'Recall the nearby square numbers. Being close to 49 does not make 48 a square.'}
};
