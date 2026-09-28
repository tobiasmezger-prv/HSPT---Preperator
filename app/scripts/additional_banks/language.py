from common import add

def rows(skill,data):
 for line in data.strip().splitlines():
  stem,key,a,b,c,why,family,diff=line.split('|')
  add('language',skill,stem,key,[a,b,c],why,'Read the complete sentence and identify the convention being tested before comparing choices.',int(diff),family)
rows('grammar','''
Choose the word that completes the sentence in standard written English: Each of the baskets ___ a label.|has|have|are|were|Each is singular, so its verb is has; baskets is inside an of phrase.|each agreement|1
Choose the correct verb: The list of supplies ___ on the desk.|is|are|were|have been|The subject is the singular list, not the plural supplies.|intervening phrase|1
Choose the correct verb: Neither the coach nor the players ___ ready.|are|is|was|has been|With neither/nor, the verb agrees with the nearer subject, players.|nor proximity|2
Choose the correct verb: Neither the players nor the coach ___ ready.|is|are|were|have been|The nearer subject is the singular coach, so use is.|nor reversed proximity|2
Choose the correct pronoun: Maya and ___ carried the boxes.|I|me|my|mine|The pronoun is part of the subject, so use I.|compound subject pronoun|1
Choose the correct pronoun: The principal thanked Jordan and ___.|me|I|my|myself|The pronoun is an object of thanked, so use me.|compound object pronoun|1
Choose the correct pronoun: The decision is between you and ___.|me|I|my|myself|Between takes object pronouns, including me.|preposition object|1
Choose the correct verb form: By the time we arrived, the show had ___.|begun|began|begin|beginning|Had requires the past participle begun.|irregular participle|2
Choose the correct verb form: Yesterday, the child ___ across the field.|ran|run|running|runs|Yesterday calls for past tense, ran.|simple past|1
Choose the correct verb form: The announcement will ___ after lunch.|be made|made|making|been made|Future passive uses will be plus a past participle.|future passive|2
Choose the correct completion: If I ___ the captain, I would ask everyone to speak.|were|was being|am|be|A hypothetical condition uses were in this formal construction.|hypothetical condition|3
Choose the correct word: Of the two paths, this one is ___.|shorter|shortest|most short|more shorter|Use the comparative for two things; do not double it with more.|comparison of two|1
Choose the correct word: Of all five sketches, hers is the ___.|clearest|clearer|more clear|most clearest|The superlative compares all five; avoid a double superlative.|superlative|1
Choose the correct word: The musician played the difficult passage ___.|smoothly|smooth|smoothness|smoother than|An adverb modifies played; smoothly is the appropriate form.|adverb modifying verb|1
Choose the correct word: The soup tastes ___.|delicious|deliciously|deliciousness|more deliciously|Tastes is a linking verb here; an adjective describes the soup.|linking verb adjective|2
Choose the sentence without a dangling modifier.|Walking into the studio, I noticed the new mural.|Walking into the studio, the mural surprised me.|Walking into the studio, the lights were bright.|Walking into the studio, a desk blocked my view.|The subject I is the person walking. The other subjects cannot logically perform that action.|dangling modifier|3
Choose the sentence with parallel structure.|We enjoy hiking, swimming, and cycling.|We enjoy hiking, to swim, and cycling.|We enjoy to hike, swimming, and cycling.|We enjoy hiking, swimming, and to cycle.|All three objects use matching -ing forms.|parallel gerunds|2
Choose the complete sentence.|Although it was raining, the match continued.|Although it was raining.|Because of the sudden rain.|Running across the wet field.|Only the first choice contains an independent clause with a subject and finite verb.|sentence fragment|2
Choose the correct verb: The scissors ___ in the drawer.|are|is|was|has been|Scissors is grammatically plural in this sentence.|plural form noun|2
Choose the correct completion: The student ___ won the contest thanked her teacher.|who|whom|whose|which's|Who is the subject of won and refers to a person.|relative subject|2
''')
rows('usage','''
Choose the correct word: There were ___ mistakes in the second draft.|fewer|less|little|much|Mistakes are countable, so use fewer.|count quantity|1
Choose the correct word: We have ___ time than we expected.|less|fewer|many|few|Time is an uncountable quantity here, so use less.|mass quantity|1
Choose the correct word: Please ___ the folder on my desk.|lay|lie|lain|laying|Lay means put something down and takes folder as its object.|lay object|2
Choose the correct word: I need to ___ down for a few minutes.|lie|lay|laid|lain|Lie means recline and does not take an object; need to takes the base form.|lie intransitive|2
Choose the correct word: The sun will ___ at dawn.|rise|raise|rose|risen|Rise is intransitive; raise requires an object.|rise intransitive|1
Choose the correct word: Please ___ your hand before speaking.|raise|rise|rose|risen|Raise takes the object your hand.|raise transitive|1
Choose the correct word: The new schedule may ___ attendance.|affect|effect|effects|affection|Affect is the verb meaning influence; may requires the base form.|affect effect|2
Choose the correct word: The change had an immediate ___ on attendance.|effect|affect|affecting|effective|Effect is the noun meaning result, fitting after an immediate.|effect noun|2
Choose the correct word: Everyone ___ Elena arrived before noon.|except|accept|expect|access|Except means excluding. Accept means receive or agree to.|except accept|1
Choose the correct word: The coach offered useful ___.|advice|advise|advises|advising|Advice is the noun; advise is a verb.|advice noun|1
Choose the correct word: The counselor will ___ us about course choices.|advise|advice|advisory|advisement|Will takes a base-form verb, advise.|advise verb|1
Choose the correct word: I would rather read ___ watch television.|than|then|when|that|Rather ... than makes a comparison; then concerns time.|than then|1
Choose the correct word: Finish your outline; ___ write the essay.|then|than|that|them|Then indicates the next step in time.|then sequence|1
Choose the correct word: The hikers left ___ boots outside.|their|there|they're|theirs'|Their shows that the boots belong to the hikers.|their possession|1
Choose the correct word: ___ planning a neighborhood cleanup.|They're|Their|There|Theirs|They're expands to they are, which supplies the subject and verb.|they are contraction|1
Choose the correct word: The puppy chased ___ tail.|its|it's|its'|it is|Its is possessive; it's means it is or it has.|its possession|1
Choose the correct word: ___ likely to snow tonight.|It's|Its|Its'|It|It's expands to it is, producing a complete sentence.|it is contraction|1
Choose the correct word: I do not want to ___ the receipt.|lose|loose|loss|losing|Lose is the verb meaning misplace; loose means not tight.|lose loose|1
Choose the correct word: The museum is ___ the library and the theater.|between|among|during|through|Between identifies a position relative to two named places.|between two|1
Which revision removes the unclear pronoun? Original: When Lena met Priya, she was holding a violin. The writer means Priya held it.|When Lena met Priya, Priya was holding a violin.|When Lena met Priya, she held it.|She held a violin when Lena met Priya.|Lena met her while she held the violin.|Repeating Priya makes the intended person explicit; the other versions leave ambiguous pronouns.|pronoun clarity|3
''')
rows('punctuation','''
Choose the correctly punctuated sentence.|After the final bell rang, the students left.|After the final bell rang the students, left.|After, the final bell rang the students left.|After the final bell, rang the students left.|A comma separates an introductory dependent clause from the main clause.|introductory clause|1
Choose the correctly punctuated sentence.|I brought a notebook, a ruler, and a pencil.|I brought, a notebook a ruler and a pencil.|I brought a notebook a ruler, and, a pencil.|I brought a notebook; a ruler and a pencil.|Commas separate the three list items; no comma separates brought from its objects.|series commas|1
Choose the correctly punctuated sentence.|The bus was late, but we arrived on time.|The bus was late but, we arrived on time.|The bus, was late but we arrived on time.|The bus was late, but, we arrived on time.|A comma comes before but when it joins two independent clauses.|compound sentence|2
Choose the correctly punctuated sentence.|The trail was steep; we climbed slowly.|The trail was steep, we climbed slowly.|The trail; was steep we climbed slowly.|The trail was steep we climbed, slowly.|A semicolon can join related independent clauses without a conjunction.|semicolon clauses|2
Choose the correctly punctuated sentence.|Bring these supplies: paper, glue, and scissors.|Bring: paper, glue, and scissors.|Bring these: supplies paper, glue, and scissors.|Bring these supplies paper: glue, and scissors.|A colon follows the complete introduction Bring these supplies.|colon list|2
One student owns the notebook. Choose the correct phrase.|the student's notebook|the students' notebook|the students notebook|the student notebook's|Singular possession adds apostrophe-s to student.|singular possession|1
Several teachers share the lounge. Choose the correct phrase.|the teachers' lounge|the teacher's lounge|the teachers lounge's|the teachers lounge|The plural teachers already ends in s; add an apostrophe after it.|regular plural possession|1
Several children share the toys. Choose the correct phrase.|the children's toys|the childrens' toys|the childrens toys|the children toy's|The irregular plural children takes apostrophe-s.|irregular plural possession|2
Choose the correctly punctuated sentence.|Please, Nora, close the window.|Please Nora close, the window.|Please Nora, close, the window.|Please, Nora close the window.|The name of the person directly addressed is set off with commas.|direct address|2
Choose the correctly punctuated sentence.|"We are ready," said Theo.|"We are ready" said Theo.|"We are ready, said Theo."|"We are ready"; said Theo.|In American English, the comma is inside the closing quotation mark before the dialogue tag.|dialogue tag|2
Choose the correctly punctuated sentence.|Did you hear Mia say, "I finished"?|Did you hear Mia say, "I finished?"|Did you hear Mia say "I finished".|Did you hear Mia say, "I finished,"?|The entire sentence is a question, but the quotation is a statement, so the question mark goes outside.|quotation question scope|3
Choose the correct contraction for could not.|couldn't|could'nt|couldnt'|couldnt|The apostrophe marks the omitted o in not.|contraction apostrophe|1
Choose the sentence without a comma splice.|The gate was locked, so we used the side entrance.|The gate was locked, we used the side entrance.|The gate, was locked we used the side entrance.|The gate was locked we, used the side entrance.|The conjunction so correctly joins the independent clauses after a comma.|comma splice repair|2
The speaker has exactly one brother. Choose the correctly punctuated sentence.|My brother, Eli, repairs bicycles.|My brother Eli, repairs bicycles.|My brother, Eli repairs bicycles.|My, brother Eli repairs bicycles.|With one brother, Eli is supplementary identifying information set off by paired commas.|nonessential appositive|3
Choose the correctly punctuated sentence.|Yes, I can help after lunch.|Yes I, can help after lunch.|Yes I can, help after lunch.|Yes I can help, after lunch.|An introductory yes is followed by a comma; the other commas interrupt the sentence.|introductory response|1
''')
rows('capitalization','''
Choose the sentence with correct capitalization.|We will visit Oregon in July.|We will visit oregon in July.|We will visit Oregon in july.|we will visit Oregon in July.|Capitalize the sentence opening, the state name, and the month.|place month|1
Choose the sentence with correct capitalization.|My favorite subjects are English and science.|My favorite subjects are english and Science.|My favorite subjects are English and Science.|My favorite subjects are english and science.|English is a language name; science is a general subject, not a named course here.|school subjects|2
Choose the sentence with correct capitalization.|We drove south toward Phoenix.|We drove South toward Phoenix.|We drove south toward phoenix.|we drove South toward Phoenix.|A compass direction is lowercase here; the city is capitalized.|compass direction|2
Choose the sentence with correct capitalization.|On Friday, Dr. Patel will speak.|On friday, Dr. Patel will speak.|On Friday, dr. Patel will speak.|On Friday, Dr. patel will speak.|Capitalize the weekday, the title before a name, and the surname.|title and day|1
Choose the sentence with correct capitalization.|My aunt lives near Lake Erie.|My Aunt lives near Lake Erie.|My aunt lives near lake Erie.|My aunt lives near Lake erie.|Aunt after my is a common noun; both words in the lake's proper name are capitalized.|kinship common noun|2
Choose the sentence with correct capitalization.|We celebrate Thanksgiving in November.|We celebrate thanksgiving in November.|We celebrate Thanksgiving in november.|we celebrate thanksgiving in november.|The holiday and month are proper names.|holiday month|1
Choose the sentence with correct capitalization.|The French visitors toured the museum.|The french visitors toured the museum.|The French Visitors toured the Museum.|the French visitors toured the museum.|French is a proper adjective; visitors and museum are common nouns here.|proper adjective|1
Choose the sentence with correct capitalization.|"Please sit down," said the teacher.|"please sit down," said the teacher.|"Please sit down," Said the teacher.|"Please Sit Down," said the Teacher.|Capitalize the first word of a complete quotation; the following dialogue tag stays lowercase.|quotation opening|2
Choose the sentence with correct capitalization.|I asked Mom to read the letter.|i asked Mom to read the letter.|I asked mom to read the letter.|I Asked Mom to read the Letter.|I is always capitalized; Mom is used as a name without my or another determiner.|kinship name|2
Choose the sentence with correct capitalization.|The club meets on the first Tuesday of every month.|The Club meets on the first Tuesday of every Month.|The club meets on the first tuesday of every month.|the club meets on the first Tuesday of every month.|Tuesday is a proper name; club and month are common nouns.|weekday common nouns|1
''')
for line in '''
necessary|neccessary|necesary|nessesary|Necessary has one c and two s's.
separate|seperate|separrate|seperete|Separate has a in the second syllable.
definitely|definately|definitly|definetely|Definitely preserves the spelling definite before -ly.
privilege|priviledge|privelege|privillage|Privilege has no d and ends in -lege.
occasion|occassion|ocassion|ocasion|Occasion has two c's and one s.
recommend|recomend|reccommend|recommmend|Recommend has one c and two m's.
embarrass|embarass|embarras|embarres|Embarrass has two r's and two s's.
maintenance|maintainance|maintenence|maintanence|Maintenance uses -tenance, not the full spelling maintain.
accommodate|acommodate|accomodate|acomodate|Accommodate has two c's and two m's.
conscience|concience|consience|consciense|Conscience includes the sequence -science.
perseverance|perserverance|perseverence|persiverance|Perseverance ends in -ance and has no r after the first s.
argument|arguement|argumant|arguemant|Argument drops the final e of argue before -ment.
noticeable|noticable|noticeble|notiseable|Noticeable retains the e before -able.
beginning|begining|beggining|begginning|Beginning doubles the final n of begin, not the g.
independent|independant|independet|indipendent|Independent ends in -ent, not -ant.
'''.strip().splitlines():
 key,a,b,c,why=line.split('|')
 add('language','spelling','Which word is spelled correctly?',key,[a,b,c],why,'Check the whole word, especially doubled consonants and its ending.',2,'spelling-'+key)
rows('composition','''
Which sentence best introduces a paragraph about ways the school garden helps students learn?|The school garden serves as an outdoor classroom in several subjects.|The school cafeteria opens at noon.|Some students prefer winter to summer.|The garden gate was painted blue yesterday.|The correct topic sentence introduces learning benefits broadly; the others are unrelated or too narrow.|topic sentence garden|2
Which detail best supports the claim that a library should stay open later?|Students with after-school jobs often cannot arrive before the current closing time.|The library's bricks are red.|The library has two front doors.|The librarian enjoys hiking.|The job schedules explain why later hours would improve access.|support access claim|2
Which sentence is least relevant to a paragraph explaining how to repair a bicycle tire?|My cousin prefers blue bicycles.|First, locate the puncture.|Next, roughen the area around the hole.|Finally, apply and press down the patch.|Color preference does not explain the repair process.|irrelevant detail repair|1
Choose the best transition: The path was muddy. ___, we continued toward the shelter.|Nevertheless|For example|Similarly|In other words|Nevertheless signals continuing despite an obstacle.|concession transition|2
Choose the best transition: The power failed. ___, the elevators stopped working.|As a result|In contrast|For instance|Likewise|The second event is a consequence of the first.|result transition|1
Choose the most concise revision that preserves the meaning: The reason we left early was because a storm was approaching.|We left early because a storm was approaching.|We left early for the reason because a storm approached.|A storm was approaching and this was the reason why we left early.|The early departure happened due to the fact that a storm was approaching.|The revision removes redundant wording while retaining the cause.|redundancy cause|2
Choose the clearest revision: At this point in time, the team is currently practicing.|The team is practicing now.|At this current point in time, the team practices currently.|The team currently is now practicing at this point.|At this point the current team is practicing currently.|Now replaces two repetitive time expressions.|redundancy time|1
A paragraph describes sorting donated books by age level, labeling the shelves, and posting a borrowing guide. Which conclusion fits best?|These steps made the book corner easier for everyone to use.|The tallest shelf was made of pine.|Some novels are very long.|We should stop lending books altogether.|The conclusion unites the organizational steps around their benefit.|concluding sentence|2
Arrange the steps logically: 1. Bake the loaf. 2. Mix the ingredients. 3. Let the baked loaf cool. 4. Pour the batter into a pan.|2, 4, 1, 3|4, 2, 3, 1|2, 1, 4, 3|1, 3, 2, 4|Mix before pouring, pour before baking, and cool after baking.|process order|1
Which sentence uses the most precise language for a science report?|The sample's mass increased from 12 grams to 15 grams.|The sample got a bit bigger somehow.|The thing changed quite a lot.|It was much different afterward.|Numerical measurements specify the property and amount of change.|precision measurement|2
Which sentence maintains a formal tone in a letter requesting a new bus stop?|Please consider adding a stop near the community center.|Hey, put a stop by our place!|That route is totally ridiculous.|You guys need to fix this mess.|The polite, specific request suits a formal letter.|formal register|1
Combine the sentences without changing their meaning: The bridge is old. It remains safe.|Although the bridge is old, it remains safe.|Because the bridge is old, it is unsafe.|The bridge is safe only when it is new.|The bridge was old because it was safe.|Although expresses the contrast while retaining both facts.|combine contrast|2
Combine the sentences to show cause: The team practiced daily. Its passing improved because of this practice.|The team's passing improved because it practiced daily.|The team practiced daily although practice prevented improvement.|The team improved before it ever practiced.|The team's passing improved, but practice was unrelated.|The revision explicitly preserves the causal relationship.|combine cause|2
A paragraph argues that shade trees improve a playground. Which evidence most directly supports this claim?|On sunny days, children can rest in the cooler shaded areas.|The school mascot is a hawk.|The oldest classroom has four windows.|The playground fence was replaced in March.|The evidence connects shade to a practical playground benefit.|evidence relevance|1
Where should this sentence go? New sentence: Then she tested the repaired lamp. Paragraph: (1) Nia unplugged the lamp. (2) She replaced the damaged cord. (3) Satisfied that it worked, she returned it to the shelf.|Between sentences 2 and 3|Before sentence 1|Between sentences 1 and 2|After sentence 3|Testing follows repair and precedes being satisfied that it works.|sentence insertion|3
Which revision uses active voice and preserves the meaning? Original: The mural was painted by the art club.|The art club painted the mural.|The mural had been painted.|The art club was painted by the mural.|The mural will paint the art club.|The art club becomes the subject performing the same past action.|active voice|2
Which sentence best begins a paragraph comparing buses and bicycles for commuting?|Buses and bicycles offer different advantages for getting to school.|Yesterday I bought a new backpack.|A bicycle has two wheels.|The bus driver wears a blue shirt.|The sentence introduces both subjects and the comparison's purpose.|comparison introduction|2
A paragraph explains that a river path is popular because it is level, shaded, and close to homes. Which title fits best?|Why Neighbors Choose the River Path|How Rivers Are Formed|The History of Mountain Climbing|A Guide to Boat Engines|The title reflects the paragraph's explanation of the path's appeal.|informative title|1
Choose the revision that removes an unintended repeated idea: Every single participant received a free gift at no cost.|Every participant received a gift at no cost.|Every single participant received a free gift for free.|Every participant received a free gift at no cost whatsoever.|All participants each received a free gift without paying any cost.|Every single and free ... at no cost repeat meanings; the revision retains one expression for each.|redundancy gift|2
A writer says the school should install refill stations. Which sentence best acknowledges a reasonable objection while responding to it?|Installation costs money, but reusable bottles could reduce discarded plastic over time.|Anyone who disagrees is foolish.|There are no possible disadvantages.|The school colors are green and white.|The sentence recognizes cost and answers with a relevant benefit instead of ignoring opposition.|counterargument|3
''')
