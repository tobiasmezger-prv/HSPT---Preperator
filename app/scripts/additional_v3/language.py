from common import setq,original
TIP='Check each complete sentence. Choose No error only when all three sentences follow standard written American English.'
# Every row contains one erroneous sentence, two independently acceptable sentences, and the specific repair.
rows='''
grammar|A bundle of cables were hanging behind the desk.|Several empty drawers were left open.|The technician has labeled each connector.|Bundle is singular: a bundle was hanging. The other sentences have agreement and complete predicates.|2
 grammar|The results of the experiment supports our prediction.|A chart summarizes the observations.|Both partners signed the report.|The plural subject results requires support; experiment is inside an of phrase.|2
 grammar|Either the ushers or the manager have the spare tickets.|The manager keeps them in a locked drawer.|Each usher knows where the drawer is.|With either/or here, the nearer subject manager is singular, so use has.|2
 grammar|The librarian gave Ava and I a tour.|Ava and I visited the new library.|The librarian invited us to return.|The verb gave needs object pronouns: Ava and me. I is correct in the subject of the other sentence.|2
 grammar|Them are the photographs selected for the exhibit.|Those photographs were taken at dawn.|We selected three views of the harbor.|A subject demonstrative is needed: Those are the photographs, not Them are.|1
 grammar|By noon, the workers had chose a new route.|They had studied the weather report.|The earlier route crossed an exposed ridge.|Had takes the past participle chosen, not the simple past chose.|2
 grammar|Yesterday, we have seen the finished model.|We saw the plans last Tuesday.|We have seen several earlier versions.|A finished time marked by yesterday takes saw, not have seen in standard usage.|2
 grammar|If the bell rings, everyone will leaves the room.|The exit is marked above the door.|Everyone should walk calmly to the stairs.|Will requires the base form leave; the plural everyone issue does not arise because everyone is singular but modal verbs do not take -s.|1
 grammar|The climber moved cautious along the ledge.|The ledge was narrow and uneven.|A guide waited near the turn.|Moved needs the adverb cautiously; cautious is an adjective.|1
 grammar|The second solution is more simpler than the first.|Both solutions produce the same result.|The class compared the two methods.|Use simpler alone; more simpler is a double comparative.|1
 grammar|Of the four proposals, this is the less expensive.|We considered four different designs.|The smallest design uses recycled wood.|Comparison among four requires least expensive, not less expensive.|2
 grammar|The club enjoys drawing, painting, and to sculpt.|Its members meet after school.|Their finished works fill two display cases.|Use sculpting to maintain the parallel -ing series.|2
 grammar|After packing the instruments, the bus was ready to leave.|The players stored their cases carefully.|The driver checked the luggage compartment.|The introductory phrase makes the bus the packer. Name the people: After packing the instruments, the players boarded the bus.|3
 grammar|The student which designed the poster won a prize.|The poster included a clear map.|Several teachers praised the design.|Use who or that for the student here, not which.|2
 grammar|Because the bridge was closed.|We followed the marked detour.|The longer route took another ten minutes.|The because clause is dependent and stands as a fragment; attach it to an independent clause.|1
 punctuation|The doors opened, the crowd moved inside.|The ushers checked the tickets.|We waited until our row was called.|Two independent clauses are joined only by a comma. Use a period, semicolon, or comma with an appropriate conjunction.|2
 punctuation|The band was ready however, the curtain remained closed.|The audience waited quietly.|A stagehand checked the curtain cord.|However is not a coordinating conjunction. Use The band was ready; however, the curtain remained closed.|3
 punctuation|Before the guests arrived we set the table.|The plates were blue.|We placed a folded napkin beside each plate.|Set off the introductory dependent clause: Before the guests arrived, we set the table.|1
 punctuation|The sculpture, stands beside the fountain.|Its surface reflects the afternoon light.|Visitors often pause beside it.|A comma must not separate the simple subject sculpture from its predicate stands.|1
 punctuation|Our equipment includes: gloves, ropes, and helmets.|We checked the equipment before leaving.|Each helmet had an adjustable strap.|Do not put a colon between includes and its direct objects. Our equipment includes gloves, ropes, and helmets.|2
 punctuation|We packed pencils notebooks and folders.|The folders were green.|Each notebook had a sturdy cover.|Separate the three items with commas: pencils, notebooks, and folders. The final serial comma is optional; the missing first separator is not.|1
 punctuation|The three dancers costumes were ready.|Each dancer had a different role.|Their shoes waited beside the stage.|The costumes belong to the three dancers: dancers' costumes requires the plural possessive apostrophe.|2
 punctuation|The womens' relay starts at noon.|The men's relay follows it.|Several teams have registered.|Women is already plural and takes apostrophe-s: women's relay.|2
 punctuation|Its' handle is cracked.|The lid still fits.|It's a useful container despite the damage.|The possessive pronoun is its, without an apostrophe. It's in the other sentence correctly means it is.|1
 punctuation|The visitor asked "Where is the gallery?"|The guide pointed toward the stairs.|The gallery opens at ten.|Use a comma before the direct quotation: The visitor asked, "Where is the gallery?"|2
 punctuation|"Please wait here, said the attendant.|The visitors formed a short line.|The attendant checked each ticket.|Close the quotation after the comma: "Please wait here," said the attendant.|1
 punctuation|We could'nt hear the final announcement.|The speakers near the door were working.|An usher repeated the message for us.|Couldn't places the apostrophe where the o in not is omitted; could'nt is misplaced.|1
 punctuation|Mina please hand me the blue folder.|The folder contains the final schedule.|I will put it beside the register.|Direct address needs a comma: Mina, please hand me the blue folder.|1
 punctuation|We visited the harbor; and watched the boats.|The wind had dropped by noon.|Several fishing boats returned together.|The second part has no subject and is not an independent clause; omit the semicolon.|2
 punctuation|The reason for the delay is, that a signal failed.|The crew is repairing the signal.|Passengers may wait inside the station.|The comma wrongly separates is from its following complement; omit it.|2
 capitalization|We visited the aquarium last saturday.|The tour began at noon.|Our guide described the feeding schedule.|Days of the week are capitalized: Saturday.|1
 capitalization|The delegation included two brazilian students.|Both students spoke English.|They described their school to us.|A nationality adjective is capitalized: Brazilian.|1
 capitalization|My uncle lives in new Mexico.|He moved there last year.|His house is near a mountain trail.|Both words in the state name are capitalized: New Mexico.|1
 capitalization|The ceremony will take place in september.|Invitations will arrive next month.|The school orchestra will perform.|Months are capitalized: September.|1
 capitalization|Our principal, dr. Chen, welcomed the visitors.|The visitors toured the classrooms.|They met several student guides.|An abbreviated title before a name is capitalized: Dr. Chen.|1
 capitalization|The hikers crossed the pacific coast trail shown on our local map.|They carried plenty of water.|The marked route ended at a beach.|Pacific, naming the ocean in this phrase, requires a capital P. The generic local coast trail is not supplied as a formal trail name.|2
 capitalization|My cousin studies spanish and mathematics.|Her favorite class meets in the morning.|She practices the language with a friend.|A language name is capitalized: Spanish. The general subject mathematics stays lowercase.|1
 capitalization|"The room is ready," Said the assistant.|The guests carried their bags upstairs.|The assistant checked the next reservation.|The dialogue tag continues the sentence, so said is lowercase.|2
 usage|The conductor asked us to remain quite during the solo.|We listened without speaking.|The soloist stood near the piano.|The intended word is quiet, meaning silent; quite is a different word.|1
 usage|The fog made it difficult to sea the harbor.|We waited until the view improved.|The captain checked the weather.|The verb is see; sea names a body of water.|1
 usage|Please insure that the cabinet is locked, meaning make certain it is locked.|The keys are in the office.|The cabinet contains the spare supplies.|In this deliberately explicit distinction, ensure means make certain. To avoid regional overlap this item is replaced before finalization.|2
 usage|We should have went to the earlier meeting.|The later meeting ended after sunset.|Several neighbors stayed to help.|Have requires the participle gone, not went.|2
 usage|She did good on the written examination.|Her preparation was thorough.|The teacher returned the papers on Friday.|When good means performing successfully here, the standard adverb is well: did well.|2
 usage|This route is different then the one on the map.|The map shows a path along the river.|We asked a guide which route to use.|Then concerns time; comparison here calls for than or a rephrasing with different from.|2
 usage|The two organizations shared a common principal: equal access.|Their leaders signed the agreement.|The new service opens next week.|A governing belief is a principle; principal has other senses such as chief or a school administrator.|2
 usage|The speaker accepted our complement on her clear explanation.|She thanked us after the talk.|Several listeners asked further questions.|An expression of praise is a compliment; a complement completes something.|2
 usage|The invitation was addressed to himself, although the sentence has no antecedent for that reflexive pronoun.|The invitation arrived yesterday.|It included directions to the hall.|This artificial metalinguistic sentence is replaced before finalization.|3
 grammar|A number of volunteers was waiting outside.|The number of available seats was small.|Several volunteers offered to stand.|A number of meaning several takes the plural verb were. The number of is singular and correctly takes was.|3
 grammar|Neither answer are correct.|Both answers use the wrong unit.|The class will review the conversion.|The singular subject neither answer requires is, not are.|2
 grammar|The package, along with its instructions, were missing.|The other packages were on the shelf.|A clerk searched the storage room.|Along with does not make the singular subject package plural; use was missing.|2
'''
lines=rows.strip().splitlines();assert len(lines)==50
# Remove contestable regional usage and awkward meta-language rather than force an answer.
lines[40]='usage|The photographer sat the camera on a tripod.|The tripod stood on a level floor.|We waited while the lens was adjusted.|Use set, meaning placed, for the camera. Sat is the past of sit and does not take camera as an object here.|2'
lines[46]='grammar|The instructions were wrote on the back of the card.|The card was inside the box.|A diagram showed how the parts fit.|The passive were needs the past participle written, not wrote.|2'
lines[35]='capitalization|The ferry crossed the atlantic Ocean.|The passengers watched from the deck.|The crossing took several days.|Both words in the proper name Atlantic Ocean are capitalized.|1'
for n,line in enumerate(lines,1):
 skill,bad,a,b,why,diff=line.split('|')
 setq('language',n,skill.strip(),'error_detection','Which sentence contains an error? If all three sentences are correct in standard written American English, choose No error.',bad,[a,b,'No error.'],why,TIP,int(diff),'error-'+str(n),noErrorCorrect=False)
none='''
grammar|Neither answer is complete.|Both students have revised their work.|The teacher has read each revision.|Neither is singular, both students is plural, and teacher is singular; all verbs agree.|2
 grammar|The committee has announced its decision.|We have received the notice.|A copy is posted beside the door.|Each subject agrees with its verb, and all sentences are complete.|1
 grammar|The coach asked Sam and me to stay.|Sam and I waited near the track.|The coach spoke to us after practice.|Me and us are objects; I is part of the subject. All cases are correct.|2
 grammar|By evening, the snow had fallen steadily for hours.|The roads were covered.|The crew had already begun clearing them.|Fallen and begun are correct participles after had; roads correctly takes were.|2
 punctuation|The sky darkened, but the game continued.|When the rain began, we left the field.|The referee blew the whistle.|The coordinating conjunction and introductory dependent clause are punctuated correctly.|2
 punctuation|The cupboard held three items: a bowl, a jug, and a tray.|The bowl was empty.|The jug contained water.|The colon follows a complete introduction, and the list is properly separated.|2
 punctuation|"Who is next?" asked the assistant.|I raised my hand.|The assistant called my name.|The question mark belongs inside the quoted question; the following tag stays lowercase.|2
 capitalization|We traveled west from Boston.|My cousin studies German.|The meeting is on Thursday.|The direction is generic and lowercase; Boston, German and Thursday are proper names.|2
 capitalization|My grandmother visits in December.|I asked Grandma to bring her photographs.|We keep the pictures in a wooden box.|The kinship word after my is generic; Grandma used as a name and December are capitalized.|2
 usage|The books are lying on the table.|Please lay the folder beside them.|Yesterday, I laid the map there too.|Lying is intransitive; lay takes folder as object; laid is the past form for placing an object.|3
 usage|The trail leads farther into the woods.|We need fewer bags this time.|There is less water in this bottle.|Farther describes physical distance; fewer modifies countable bags; less modifies water.|2
 punctuation|It's the dog's bowl.|Its rim is chipped.|The dog still uses it.|It's means it is; dog's is singular possessive; its is a possessive pronoun without an apostrophe.|2
 grammar|The runner who won the race thanked her coach.|Her teammates cheered loudly.|Each teammate received a ribbon.|Who is the subject of won; loudly is an adverb; each takes singular received without any agreement conflict.|2
 grammar|To reach the shelter, the hikers followed the marked route.|They wanted to arrive before dark.|The leader checked the distance.|The hikers are the implied travelers in the introductory infinitive phrase; the remaining sentences are complete.|2
 punctuation|The road was blocked; we took another route.|The delay was brief.|We arrived before the performance began.|The semicolon joins independent clauses, and no extra comma is required in the final integrated time clause.|2
 usage|The new plan will affect our schedule.|Its effect may be small.|We will assess the change after a week.|Affect correctly means influence; effect means result. Both fit their contexts.|2
'''
for n,line in enumerate(none.strip().splitlines(),51):
 skill,a,b,c,why,diff=line.split('|')
 setq('language',n,skill.strip(),'error_detection','Which sentence contains an error? If all three sentences are correct in standard written American English, choose No error.','No error.',[a,b,c],why,TIP,int(diff),'no-error-'+str(n),noErrorCorrect=True)
assert n==66
# Keep previously checked fresh spelling targets, use familiar four-option spelling presentation.
for n,old in enumerate(original['language']['questions'][65:80],67):
 key=old['choices']['ABCD'.index(old['guide']['correctChoiceId'])]
 wrong=[c for c in old['choices'] if c!=key]
 setq('language',n,'spelling','spelling','Which word is spelled correctly?',key,wrong,old['guide']['explanation'],'Check every syllable and any doubled consonants.',2,'spelling-'+key,targetWord=key)
for n,line in enumerate(['itinerary|itenerary|itinerery|itinarary|Itinerary uses i-ti-ner-ar-y.','questionnaire|questionaire|questionnair|questionnare|Questionnaire has two n letters and ends in -aire.'],82):
 key,a,b,c,why=line.split('|');setq('language',n,'spelling','spelling','Which word is spelled correctly?',key,[a,b,c],why,'Check the whole word rather than accepting its familiar beginning.',2,'spelling-'+key,targetWord=key)
# Short original paragraph tasks; prompts carry complete context so no hidden passage dependency exists.
rows='''
paragraph_order|Arrange these sentences into the clearest sequence: (1) Finally, attach a label to each pot. (2) Place soil in the empty pots. (3) Once the soil is in place, press one seed into each pot.|2, 3, 1|3, 2, 1|1, 2, 3|2, 1, 3|Sentence 3 depends on soil placed in 2; Finally signals the last step in 1.|1
paragraph_order|Arrange these sentences into the clearest paragraph: (1) This covering kept dust off the model. (2) Before leaving, Ren placed a cloth over the model. (3) The next morning, the clean model was ready for display.|2, 1, 3|1, 2, 3|3, 1, 2|2, 3, 1|This covering refers back to the cloth in 2; the next morning follows the protective action and its purpose.|2
paragraph_insertion|Paragraph: (1) Our class collected used crayons. (2) We sorted them by color. (3) The molds then went into a warm oven. Insert: “Next, we placed the sorted pieces in small molds.” Where does it belong?|Between sentences 2 and 3.|Before sentence 1.|Between sentences 1 and 2.|After sentence 3.|Sorted pieces depends on 2, and the molds in 3 needs the newly introduced molds.|2
paragraph_insertion|Paragraph: (1) A label on the box was unreadable. (2) No one knew which room should receive it. (3) We checked the shipping record. Insert: “The ink had washed away during the storm.” Where does it best belong?|Between sentences 1 and 2.|Before sentence 1.|Between sentences 2 and 3.|After sentence 3.|The ink sentence explains the unreadable label before the consequence is stated.|2
irrelevant_sentence|Which sentence should be removed from this paragraph about preparing a telescope for observation? (1) We set the tripod on firm ground. (2) We checked that its legs were secure. (3) My jacket has a silver zipper. (4) Then we attached the telescope.|Sentence 3.|Sentence 1.|Sentence 2.|Sentence 4.|The jacket detail does not develop the preparation sequence; the other sentences do.|1
irrelevant_sentence|Which sentence least supports a paragraph arguing for covered bicycle parking? (1) A roof would keep seats dry. (2) Shade would protect parked bicycles from direct sun. (3) A cover could make parking more useful in bad weather. (4) Our town has several steep hills.|Sentence 4.|Sentence 1.|Sentence 2.|Sentence 3.|Hill steepness does not directly support a cover over parked bicycles.|2
topic_sentence|Which sentence best introduces these details? “Visitors can listen to a translated description. Large-print labels are available. A raised model lets visitors explore the object's shape by touch.”|The exhibit offers several ways to access its information.|The exhibit has replaced all its printed labels.|The exhibit concentrates on the history of translation.|The exhibit is designed mainly to display raised models.|The details share access through different modes; the other choices narrow or contradict the set.|2
concluding_sentence|Paragraph: “Our repair log records each fault, the attempted solution, and the result. Before opening a machine, we consult earlier entries. This often prevents us from repeating an unsuccessful fix.” Which conclusion fits best?|A careful record makes earlier experience useful in later repairs.|Repair work is easier when every machine uses identical parts.|The most important repairs should be omitted from the log.|New machines have fewer faults than machines used for years.|Only the first conclusion follows the paragraph's point about learning from logged experience.|2
transition|Choose the best transition: “The smaller tent weighs less. ___, the larger tent offers more space for equipment.”|On the other hand|As a result|For the same reason|For example|The sentences contrast advantages; the second is neither a result nor an example of the first.|1
transition|Choose the best transition: “The first trial used only one sample. ___, the result should be treated as preliminary.”|Therefore|Nevertheless|Similarly|Meanwhile|The limited evidence is a reason for treating the result as preliminary.|2
sentence_combining|Choose the clearest combination without changing the meaning: “The plaque was small. Its lettering could be read from the doorway.”|Although the plaque was small, its lettering could be read from the doorway.|Because the plaque was small, its lettering could not be read from the doorway.|The plaque was small so that its lettering could be read only nearby.|The plaque was small, and the doorway could be read from its lettering.|Although preserves the contrast and both original facts; the others reverse or distort them.|2
sentence_combining|Combine without changing the time relationship: “The guests arrived. We had already moved the chairs indoors.”|Before the guests arrived, we had moved the chairs indoors.|After the guests arrived, we moved the chairs indoors.|The guests arrived while we were starting to move the chairs indoors.|We would move the chairs indoors if the guests arrived.|Already and had moved place the chair move before the arrival.|2
pronoun_clarity|Revise to make clear that Daria, not Mei, found the missing card: “Daria told Mei that she had found the missing card.”|Daria told Mei, “I found the missing card.”|Daria told her that she had found the missing card.|She told Mei that Daria's card had been found.|Daria told Mei that the card she wanted was missing.|The direct quotation assigns I to Daria and preserves the act of telling Mei.|2
concision|Which revision removes redundancy while preserving meaning? “The two partners cooperated together to finish the mural.”|The two partners cooperated to finish the mural.|The two partners agreed that the mural was finished.|The two partners finished the mural independently.|The mural was finished before the partners cooperated.|Cooperated already means worked together; the other revisions change the facts.|1
supporting_detail|Claim: “Moving the sign to eye level made it easier for visitors to find the room.” Which detail most directly supports it?|After the move, fewer visitors asked where the room was.|The sign had been painted by a local artist.|The room's chairs were replaced during the summer.|Many visitors preferred the sign's blue background.|Fewer requests for directions bear directly on finding the room; the other details do not test that claim.|2
paragraph_revision|Paragraph: “The box is lightweight. It carries a heavy load. It is easy to lift when empty.” Which revision best reduces repetition while retaining all three ideas?|The lightweight box is easy to lift when empty yet can carry a heavy load.|The box is lightweight because a heavy load makes it easy to lift.|The box carries a heavy load and is always easy to lift.|The empty box cannot carry a heavy load because it is lightweight.|The correct version preserves the empty-box condition and the contrast with capacity.|3
paragraph_order|Arrange these sentences into the clearest paragraph: (1) That result led us to test a second material. (2) The first cover tore during the wind test. (3) The second cover remained intact under the same conditions.|2, 1, 3|1, 3, 2|3, 2, 1|2, 3, 1|That result refers to the tear in 2 and motivates testing the second material whose result appears in 3.|2
'''
for n,line in enumerate(rows.strip().splitlines(),84):
 fmt,stem,key,a,b,c,why,diff=line.split('|')
 setq('language',n,'composition',fmt,stem,key,[a,b,c],why,'Identify the paragraph’s purpose and preserve its meaning, references, and sequence.',int(diff),fmt+'-'+str(n))
assert n==100
# Fresh spelling targets after whole-corpus text screening.
for n,line in [(69,'fluorescent|flourescent|fluorescant|fluorecent|Fluorescent begins fluor- and ends -escent.'),(79,'liaison|liason|liaision|lieaison|Liaison contains the sequence l-i-a-i-s-o-n.'),(80,'auxiliary|auxilary|auxillary|auxilliary|Auxiliary has one l and the sequence -iliary.')]:
 key,a,b,c,why=line.split('|');setq('language',n,'spelling','spelling','Which word is spelled correctly?',key,[a,b,c],why,'Check the internal vowel sequence as well as doubled consonants.',3,'spelling-'+key,targetWord=key)
# Comparable correct sentences prevent length from reliably identifying the error.
from common import banks
expanded={
1:'The technician has carefully labeled every connector behind the desk.',
3:'Each usher knows exactly where the manager keeps the remaining tickets.',
5:'Those photographs were taken from the harbor wall just before sunrise.',
7:'We have seen several earlier versions during our visits to the workshop.',
9:'The narrow ledge curved around the cliff before reaching a sheltered platform.',
11:'We considered four different designs before discussing their likely costs.',
13:'The players stored their instrument cases carefully in the compartment under the bus.',
17:'A stagehand checked the curtain cord while the audience waited quietly in the hall.',
19:'Its polished surface reflects the changing afternoon light from the fountain.',
21:'Each notebook had a sturdy cover designed to protect the pages inside.',
23:'Several teams from neighboring schools have registered for the afternoon races.',
25:'The guide pointed toward the stairs leading to the gallery on the second floor.',
29:'Several fishing boats returned together just as the afternoon wind began to drop.',
30:'Passengers may wait inside the station while the crew repairs the damaged signal.',
32:'Both students spoke English during their presentation about life at their school.',
34:'The school orchestra will perform a new arrangement during the opening ceremony.',
37:'She practices the language with a friend who lives in the same apartment building.',
39:'We listened without speaking as the soloist began the most difficult passage.',
41:'We waited beside the camera while the photographer adjusted the lens and checked the light.',
45:'Their leaders signed the agreement after discussing access to the new service.',
47:'A diagram inside the box showed how the separate parts fit into the finished model.',
49:'The class will review the conversion before attempting another question about units.',
50:'A clerk searched the storage room while the other packages remained on the shelf.'}
for n,sentence in expanded.items():
 q=banks['language']['questions'][n-1]
 similarities={i:len(set(q['choices'][i].lower().split()) & set(sentence.lower().split())) for i in [1,2]}
 q['choices'][max(similarities,key=similarities.get)]=sentence
