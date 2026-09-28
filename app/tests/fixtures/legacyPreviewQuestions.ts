import type {Question,Section,Skill,Choice} from '../../src/domain/types';
// Deliberately unpublished, unreviewed UI fixtures. Never include in a released bank.
type Row=[string,[string,string,string,string],Choice,string];
const rows:Record<Exclude<Section,'quantitative'>,Row[]>={
 mathematics:[
 ['What is 3/4 + 1/8?',['4/12','7/8','1/2','5/8'],'B','Convert 3/4 to 6/8, then add 1/8.'],
 ['Solve: 3x + 5 = 20.',['3','4','5','6'],'C','Subtract 5 and divide by 3.'],
 ['A rectangle is 8 cm long and 5 cm wide. What is its area?',['13 cm²','26 cm²','40 cm²','80 cm²'],'C','Multiply length by width: 8 × 5 = 40.'],
 ['A $60 jacket is discounted by 20%. What is its sale price?',['$12','$40','$48','$52'],'C','Twenty percent of 60 is 12; subtract 12.'],
 ['What is the mean of 4, 6, 8, and 10?',['6','7','8','9'],'B','The sum is 28; divide by four.'],
 ['Two angles of a triangle are 50° and 60°. What is the third angle?',['60°','70°','80°','90°'],'B','Triangle angles total 180°; subtract 110°.'],
 ['What is 2.5 × 0.4?',['0.1','1','10','100'],'B','25 × 4 = 100, with two decimal places.'],
 ['A bag has 3 red and 2 blue marbles. What is the probability of drawing a blue marble?',['1/5','2/5','3/5','2/3'],'B','Two of the five marbles are blue.'],
 ['What is the perimeter of a square with side length 9 m?',['18 m','27 m','36 m','81 m'],'C','A square has four equal sides: 4 × 9.'],
 ['A car travels 120 miles in 3 hours. What is its average speed?',['30 mph','40 mph','60 mph','360 mph'],'B','Divide distance by time: 120 ÷ 3.']],
 verbal:[
 ['Which word is closest in meaning to cautious?',['Careful','Cheerful','Quick','Noisy'],'A','Cautious means careful about possible risk.'],
 ['Which word is opposite in meaning to scarce?',['Rare','Hidden','Abundant','Fragile'],'C','Abundant means plentiful, the opposite of scarce.'],
 ['Bird is to nest as bee is to _____.',['Web','Hive','Den','Shell'],'B','A nest houses birds; a hive houses bees.'],
 ['Which word does not belong?',['Violin','Flute','Trumpet','Hammer'],'D','The first three are musical instruments.'],
 ['All glips are blue. This object is a glip. What must be true?',['It is round','It is blue','All blue objects are glips','It is large'],'B','The rule applies to every glip, including this one.'],
 ['Which word is closest in meaning to brief?',['Short','Difficult','Distant','Bright'],'A','Brief means short in duration or length.'],
 ['Doctor is to patient as teacher is to _____.',['School','Book','Student','Lesson'],'C','A doctor serves patients; a teacher teaches students.'],
 ['Which word is opposite in meaning to expand?',['Grow','Stretch','Increase','Shrink'],'D','To shrink is to become smaller.'],
 ['Mia is taller than Leo. Leo is taller than Sam. Who is shortest?',['Mia','Leo','Sam','Cannot be determined'],'C','Sam is shorter than Leo, who is shorter than Mia.'],
 ['Which word best completes the sentence? The directions were so _____ that everyone understood them.',['Clear','Distant','Heavy','Silent'],'A','Clear directions are easy to understand.']],
 reading:[
 ['Why did Nora initially doubt the garden would succeed?',['The lot was shaded','The soil was dry and hard','No one brought seeds','The lot was too small'],'B','The opening describes dry, hard soil and Nora’s doubt.'],
 ['What did the neighbors do before planting?',['Sold vegetables','Built a greenhouse','Removed litter and added compost','Painted the fence'],'C','The passage states that they cleared litter and mixed compost into the soil.'],
 ['Why did Nora record rainfall?',['To decide when to water','To predict the winter','To count visitors','To measure plant height'],'A','Her notebook helped the group decide when extra water was needed.'],
 ['What does the passage suggest about Nora?',['She dislikes working with others','She changes her opinion when she sees results','She is an expert gardener at first','She prefers buying food'],'B','She begins doubtful but later sees the garden thrive.'],
 ['Which title best captures the passage?',['A Garden Built Together','The Driest Summer','A Trip to the Market','The Missing Notebook'],'A','The passage centers on neighbors working together to create a garden.'],
 ['Why did the library introduce a tool-lending shelf?',['To replace books','To help people borrow tools they rarely need','To sell old equipment','To teach every trade'],'B','The passage explains that many tools are needed only occasionally.'],
 ['What must borrowers do before taking a tool home?',['Buy a toolbox','Attend a weekly meeting','Read the safety guide','Donate a book'],'C','Borrowers must read the safety guide before taking tools home.'],
 ['What does “modest” mean in the description of the collection?',['Small','Expensive','Unusual','Broken'],'A','The collection began with just a few tools.'],
 ['Which detail shows that the program expanded?',['The library kept its books','Borrowers returned tools','More residents donated equipment','The shelf was near the entrance'],'C','Donations increased the collection.'],
 ['What is the main idea of the passage?',['Tools are better than books','Sharing useful equipment can benefit a community','Every home needs a drill','Libraries should charge more'],'B','The passage describes a community borrowing useful equipment.']],
 language:[
 ['Which sentence uses correct subject–verb agreement?',['The dogs runs outside.','The dog run outside.','The dogs run outside.','The dogs running outside.'],'C','Plural “dogs” takes “run.”'],
 ['Which word correctly completes the sentence? _____ going to the museum tomorrow.',['Their','There','They’re','Theirs'],'C','They’re means they are.'],
 ['Which sentence is punctuated correctly?',['After lunch we, went outside.','After lunch, we went outside.','After, lunch we went outside.','After lunch we went, outside.'],'B','The comma follows the introductory phrase.'],
 ['Which word is spelled correctly?',['Necessary','Neccessary','Necesary','Necessery'],'A','Necessary has one c and two s letters.'],
 ['Which is a complete sentence?',['Because it was raining.','Under the old bridge.','The children waited inside.','Running toward the bus.'],'C','It has a subject, a verb, and a complete thought.'],
 ['Which sentence uses an apostrophe correctly for one girl?',['The girls coat is blue.','The girl’s coat is blue.','The girls’ coat’s is blue.','The girl coat’s is blue.'],'B','Girl’s indicates a coat belonging to one girl.'],
 ['Choose the correct word: She sang _____.',['Beautiful','Beautifully','Beauty','Beautify'],'B','The adverb beautifully describes how she sang.'],
 ['Which sentence uses capitalization correctly?',['We visited Boston in July.','We visited boston in July.','We visited Boston in july.','we visited Boston in July.'],'A','The sentence opening, city, and month are capitalized.'],
 ['Which sentence is in the past tense?',['I walk to school.','I will walk to school.','I am walking to school.','I walked to school.'],'D','Walked is the past-tense form.'],
 ['Which transition signals a contrast?',['Therefore','Similarly','However','Furthermore'],'C','However introduces a contrasting idea.']]
};
const skill:Record<Exclude<Section,'quantitative'>,Skill>={mathematics:'math_practice',verbal:'verbal_practice',reading:'reading_comprehension',language:'language_usage'};
const passages=[{id:'preview-garden',title:'The neighborhood garden',text:'When Nora first saw the empty lot, its soil was dry and hard. She doubted that vegetables could grow there. On Saturday, neighbors removed litter and mixed compost into the soil. They planted beans and tomatoes, then divided the watering duties. Nora kept a notebook of rainfall so the group could decide when extra water was needed. By midsummer, green vines covered the stakes. Nora carried the first ripe tomatoes to a neighbor who could no longer work outdoors. She realized that the garden had grown more than food: it had given the neighbors a reason to work together.'},{id:'preview-library',title:'Something new to borrow',text:'The town library added a tool-lending shelf near its entrance. Residents could borrow a drill or a set of gardening tools instead of buying equipment they might use only once. The collection was modest at first, with just a few tools. Borrowers had to read a safety guide before taking anything home and return each item clean. As the program became popular, more residents donated equipment. The library continued lending books, but the new shelf offered another way for people to share useful resources.'}];
export const previewQuestions:Question[]=Object.entries(rows).flatMap(([section,items])=>items.map(([stem,choices,correctChoiceId,explanation],i)=>({id:`preview-${section}-${i+1}`,section:section as Section,skill:skill[section as keyof typeof skill],stem,choices,guide:{correctChoiceId,explanation,shortcut:''},templateFamily:`preview-${section}-${i+1}`,revision:1,difficulty:1 as const,dummy:true,reviewStatus:'pending_human_review' as const,sourceType:'original_draft' as const,...(section==='reading'?{passage:passages[i<5?0:1]}:{})})));
