from common import banks,setq,review_notes
# Related but non-equivalent distractors, with explicit distinctions recorded for review.
rows='''
1|desire|purchase|admire|request|Covet means desire strongly. Admiration, purchase and a request can occur without coveting.|2
2|unwilling|unable|uncertain|unprepared|Reluctant means unwilling or hesitant to act; ability, certainty and preparation are different issues.|2
3|brief|blunt|incomplete|precise|Concise means expressed in few words. A statement can be precise or blunt while remaining lengthy; incomplete means missing content.|2
4|outdated|damaged|unpopular|uncommon|Obsolete means no longer current or in use; damage, rarity and unpopularity alone do not make something obsolete.|2
5|unbiased|uninvolved|indecisive|uninformed|Impartial means free of favoritism. A person may be informed and involved yet impartial.|2
6|able to recover|unable to bend|slow to change|difficult to notice|Resilient describes recovery after stress or difficulty, not rigid resistance to all change.|2
7|economical|impoverished|ungenerous|unambitious|Frugal means avoiding waste. It does not establish poverty, lack of generosity, or lack of ambition.|2
8|frank|impolite|confident|informal|Candid means honest and direct; candor does not require rudeness, confidence, or informality.|2
9|watchful|suspicious|restless|fearful|Vigilant means alert and watchful; fear or suspicion may accompany it but is not its definition.|2
10|believable|proven|probable beyond doubt|widely repeated|Plausible means apparently reasonable or believable, without proof or certainty.|2
11|persuade gently|order firmly|promise repeatedly|explain fully|To coax is to persuade gently, rather than command or simply give an explanation.|2
12|examine closely|glance briefly|summarize fairly|memorize exactly|To scrutinize is to inspect closely; it need not involve memorizing or summarizing.|2
13|ease|eliminate|conceal|postpone|Alleviate means make less severe, not necessarily remove, hide, or delay.|2
14|refill|replace|restore order|redistribute|Replenish means fill or supply again. Replacing a container or distributing its contents is different.|2
15|forbid|discourage|criticize|regulate|Prohibit means disallow. Regulation or discouragement may stop short of a ban.|2
16|agile|restless|hasty|lightweight|Nimble means quick and skillful in movement; haste, restlessness or low weight alone is insufficient.|1
17|strong|rigid|bulky|heavy|Sturdy means strongly built. Something can be heavy or rigid without being strong.|1
18|peaceful|isolated|drowsy|motionless|Tranquil means calm and peaceful, not necessarily remote, sleepy, or still.|1
19|detailed|expensive|impressive|decorative|As an adjective, elaborate means complex or carefully detailed. Cost or decoration alone does not define it.|2
20|inactive|unresponsive to praise|invisible|weightless|Inert means inactive or lacking motion; the narrower distractor does not capture the general sense.|2
21|provisional|doubtful of others|unplanned|immediate|Tentative means not yet final or certain, hence provisional; it need not be unplanned.|2
22|temporary relief|complete acquittal|formal warning|permanent immunity|A reprieve is a postponement of punishment or temporary relief; it need not remove blame or give permanent immunity.|3
23|noticeable|famous|colorful|unusual|Conspicuous means easy to notice; fame, color and unusualness are possible causes rather than definitions.|2
24|cautious|weary|distrustful of everyone|indecisive|Wary means alert to possible danger and cautious. Weary concerns tiredness; the other descriptions are too specific.|2
25|confirm|assume|endorse|repeat|Verify means establish truth or accuracy. Endorsement and repetition do not establish it.|2
26|counterfeit|antique|unusual|costly|Authentic means genuine; counterfeit means made to pass as genuine. Age, rarity and price are not opposites.|2
27|flexible|brittle|straight|durable|Rigid means stiff or resistant to bending; flexible is the opposite. Brittleness concerns breaking.|1
28|fragile|heavy|replaceable|weatherproof|Durable means able to last or withstand wear; fragile contrasts with that resistance. Replaceability does not imply fragility.|2
29|shrink|extend|spread|inflate|Expand means become larger; shrink means become smaller. The other options describe enlargement.|1
30|reveal|disguise|shelter|retain|Conceal means hide; reveal means make known or visible. Shelter and retain do not oppose hiding.|1
31|pessimistic|realistic|cautious|uncertain|Optimistic expects favorable outcomes; pessimistic expects unfavorable ones. Realism or caution is not inherently pessimistic.|2
32|malicious|indifferent|unselfish|reserved|Benevolent means wishing good; malicious means intending harm. Indifference lacks the opposite positive intention to harm.|3
33|opaque|translucent|colorless|reflective|Transparent allows a clear view through; opaque blocks it. Translucent transmits light diffusely and is not the strongest opposite.|2
34|compulsory|unpaid|deliberate|temporary|Voluntary means freely chosen; compulsory means required. Unpaid or deliberate actions can be voluntary.|2
35|final|recent|central|preliminary|Initial concerns the beginning; final concerns the end. Recent concerns how long ago something happened.|1
36|descend|retreat|approach|wander|Ascend means move upward; descend means move downward. Retreat is backward movement rather than necessarily downward.|1
37|worsen|maintain|ignore|disguise|Mitigate means make less severe; worsen means make more severe. Inaction does not itself name that opposite change.|2
38|negligent|inexperienced|exhausted|unhurried|Diligent means showing steady care; negligent means failing to take proper care. Fatigue or inexperience does not establish negligence.|2
39|exclude|separate|collect|divide|Include means have as a part; exclude means keep out. Separating or dividing can leave things included in a larger set.|1
40|friendly|formal|distant|neutral|Hostile means antagonistic; friendly is the opposite. Neutral and distant lack hostility without expressing friendliness.|2
41|exact|rounded|estimated|nearby|Approximate means close but not exact; exact supplies the opposite. Rounded and estimated can be approximate.|1
42|safe|familiar|ordinary|predictable|Perilous means dangerous. Familiarity or predictability does not make something safe.|2
43|active|hidden|developing slowly|asleep|Dormant means inactive, often temporarily; active is the opposite. Slow development is still activity, but is a narrower and less direct choice.|2
44|decelerate|stop suddenly|maintain speed|change direction|Accelerate means increase speed in this everyday sense; decelerate means reduce it, without requiring an abrupt stop.|2
45|divided|silent|incomplete|uncertain|Unanimous means fully in agreement; divided contrasts disagreement. Silence or uncertainty does not establish division.|2
46|defiant|independent|quiet|reserved|Docile means readily guided or taught; defiant actively resists. Independence alone does not imply defiance.|2
47|weaken|replace|remove|reshape|Reinforce means make stronger; weaken means make less strong. Replacement or reshaping need not weaken anything.|2
48|unreadable|unpublished|handwritten|unfamiliar|Legible means clear enough to read; unreadable is the opposite in that sense.|1
49|frequently|occasionally|recently|promptly|Seldom means rarely, so frequently is the opposite. Occasionally is closer to an infrequent rate.|1
50|increase|pause|persist|fluctuate|Wane means decrease in strength or extent; increase reverses that direction. Fluctuation includes both directions.|2
'''
for line in rows.strip().splitlines():
 n,key,a,b,c,why,diff=line.split('|');n=int(n);old=banks['verbal']['questions'][n-1]
 stem=old['stem']
 if n==19:stem='As an adjective describing a design, which word is closest in meaning to ELABORATE?'
 if n==44:stem='In a description of speed, which word is most nearly opposite in meaning to ACCELERATE?'
 setq('verbal',n,old['skill'],old['format'],stem,key,[a,b,c],why,'Decide the word’s meaning before checking whether a synonym or an opposite is requested.',int(diff),old['templateFamily'])
# Strengthen relationship distractors without changing the valid relationship.
updates={51:('Complete the analogy: glossary : unfamiliar terms :: legend : ?','map symbols',['travel distances','place names','page numbers'],'A glossary explains unfamiliar terms; a map legend explains its symbols. Distances and names can appear on maps without being what the legend primarily defines.'),
57:('Complete the analogy: murmur : shout :: drizzle : ?','downpour',['mist','cloud','puddle'],'Murmur and shout contrast low and high intensity of voice; drizzle and downpour contrast light and heavy rain.'),
60:('Complete the analogy: blueprint : building :: outline : ?','essay',['paragraph','revision','index'],'The first item is a plan for the second: a blueprint plans a building, and an outline plans an essay.'),
66:('Complete the analogy: approve : approval :: refuse : ?','refusal',['refutable','refusing','refused'],'Approval and refusal are nouns naming the respective acts; the other options are an adjective or inflected verb forms.'),
68:('Complete the analogy: telescope : distant :: microscope : ?','minute',['nearby','transparent','hidden'],'A telescope helps observe distant objects; a microscope helps observe minute, or very small, objects. Nearness alone is not the defining contrast.'),
70:('Complete the analogy: hinge : pivot :: axle : ?','rotate',['accelerate','balance','slide'],'A hinge permits pivoting movement; an axle provides an axis for rotation. Acceleration, balance and sliding are different functions.')}
for n,(stem,key,wrong,why) in updates.items():setq('verbal',n,'analogies','analogies',stem,key,wrong,why,'State the relationship, then keep the same direction and degree of specificity.',2,'analogy-revised-'+str(n))
# More demanding classifications: identify a relationship shared by three, rather than spotting an unrelated object.
rows='''
75|Which word differs from the others in its relation to certainty?|conjecture|proof|confirmation|verification|Conjecture is a proposed explanation without established proof; the others support or establish a claim.|2
77|Which item differs from the others in the kind of feature it describes?|symmetry|length|width|height|Length, width and height are dimensions; symmetry is a relationship between parts of a shape.|2
78|Which word differs from the others in how a statement is presented?|implication|declaration|assertion|announcement|An implication conveys something indirectly; the others name explicit statements.|3
80|Which word differs from the others in its relation to an earlier event?|forecast|recollection|reminiscence|retrospect|A forecast concerns what may happen later; the others concern looking back.|2
81|Which word differs from the others in its role in an argument?|conclusion|premise|evidence|reason|Premises, evidence and reasons support an argument; a conclusion is the claim drawn from that support.|2
82|Which term differs from the others in its relationship to the whole?|appendix|chapter|section|paragraph|An appendix is supplementary material; the others name divisions within the main text. The question concerns structural role, not physical attachment.|3
84|Which word differs from the others in the direction of change it expresses?|recede|advance|approach|progress|Recede means move back or away; the others describe forward or nearer movement.|2
85|Which term differs from the others in when it occurs relative to a performance?|encore|audition|rehearsal|warm-up|An encore follows a completed performance; the others prepare for or precede a performance.|2
'''
for line in rows.strip().splitlines():
 n,stem,key,a,b,c,why,diff=line.split('|');setq('verbal',int(n),'classification','classification',stem,key,[a,b,c],why,'Identify the precise shared relationship; do not choose only by how familiar a word feels.',int(diff),'classification-revised-'+n)
# Replace repeated implication drills with varied constraints. Model enumerations are added in the independent checker.
rows='''
86|Four display cases, J, K, L, and M, stand in a row. J is immediately left of K. M is at the right end. L is not next to M. Which case is at the left end?|L|J|K|M|M is fourth. J and K must occupy the second and third positions, leaving L first; putting J,K first would leave L beside M.|3|ordering
87|All members of Group R belong to Group S. No member of Group S belongs to Group T. Which statement must be true?|No member of R belongs to T.|Every member of S belongs to R.|Every person outside T belongs to S.|Some member of T belongs to R.|R lies entirely within S, and S has no overlap with T, so R and T cannot overlap. Reversals are unsupported.|2|set_exclusion
88|Some entries are poems. All poems in the collection are unsigned. Which conclusion must follow?|Some entries are unsigned.|All unsigned entries are poems.|All entries are unsigned.|No signed entry is a story.|At least one entry is a poem and therefore unsigned; nothing identifies all unsigned entries or all stories.|2|existential
89|A box contains exactly one token: red, green, or blue. It is not red. If it is green, its label is striped. The label is not striped. What color is the token?|Blue.|Green.|Red.|The color cannot be determined.|Not striped rules out green; not red rules out red. The exhaustive third option is blue.|3|elimination
90|An exhibit opens only if both the lights and the alarm have been tested. The lights were tested, but the alarm was not. If the rule is followed, what follows?|The exhibit does not open.|The exhibit opens with fewer visitors.|The lights must be tested again.|Testing the lights also tested the alarm.|Both tests are necessary. The missing alarm test rules out opening; none of the other claims is stated.|2|necessary_conjunction
93|Five cards numbered 1 through 5 are arranged in a row. Card 2 is before card 4, card 4 is before card 1, and card 3 is after card 1. Which of these orders could be used?|2, 5, 4, 1, 3|4, 2, 5, 1, 3|2, 4, 3, 1, 5|2, 1, 4, 5, 3|The required chain is 2 before 4 before 1 before 3; 5 is unrestricted. Only the first listed candidate respects the full chain.|3|possible_order
94|Exactly two of four lamps, P, Q, R, and S, are on. P is on. If Q is on, R must be on. Which lamp must be off?|Q.|R.|S.|P.|Turning Q on forces R on and would create three lit lamps with P, contradicting exactly two. Either R or S can be the second lamp.|3|count_constraint
95|A parcel goes by rail or by road, but not both. Road parcels require a blue label. This parcel has no blue label. What must be true if all rules were followed?|It goes by rail.|It goes by both routes.|It has a red label.|It cannot be delivered.|No blue label rules out road. The exhaustive rail-or-road choice then forces rail; no other label color is specified.|2|exclusive_route
96|Each of three folders contains either one sheet or two sheets. Together they contain five sheets. How many folders contain two sheets?|Two.|One.|Three.|It cannot be determined.|Three single sheets give three. The two additional sheets must go into two different folders because no folder can contain more than two.|2|finite_distribution
98|Lena is older than Mo but younger than Paz. Rin is younger than Mo. Who must be the oldest of these four?|Paz.|Lena.|Mo.|Rin.|The statements give Paz older than Lena older than Mo older than Rin.|1|ordering_chain
99|Every green card has a triangle. Some cards with triangles also have dots. Which conclusion is justified?|The facts do not establish whether any green card has dots.|Every green card has dots.|No green card has dots.|Every dotted card is green.|The dotted triangle cards may or may not include green cards. The facts leave that overlap open.|3|undetermined_overlap
100|A display uses either three or four panels. Each panel has exactly two hooks. A count finds seven hooks. Which conclusion follows?|At least one stated fact about the display is incorrect.|The display must have four panels.|One panel must have no hooks.|The display must have three panels.|The stated rules allow six or eight hooks, never seven. They do not identify which statement fails or establish a specific defect.|3|consistency
'''
for line in rows.strip().splitlines():
 n,stem,key,a,b,c,why,diff,family=line.split('|');setq('verbal',int(n),'logical_reasoning','logical_reasoning',stem,key,[a,b,c],why,'Use only the stated conditions. Check every candidate against all of them.',int(diff),family)
for q in banks['verbal']['questions']:
 review_notes.setdefault(q['id'],q['guide']['explanation'])
# One consistent classification tag for the same presentation.
for q in banks['verbal']['questions']:
 if q['skill']=='classifications':q['skill']='classification';q['format']='classification'
