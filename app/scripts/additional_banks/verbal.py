from common import add

def vocabulary(skill,data):
 for line in data.strip().splitlines():
  word,key,a,b,c,meaning=line.split('|')
  opposite=skill=='antonyms'
  add('verbal',skill,f'Which word is most nearly {"opposite in meaning to" if opposite else "a synonym for"} {word.upper()}?',key,[a,b,c],f'{word.capitalize()} means {meaning}. {key.capitalize()} is the {"opposite" if opposite else "closest meaning"}; the other choices do not express that relationship.', 'Decide the meaning first, then check whether the question asks for a synonym or an opposite.',2,f'{skill}-{word}')
vocabulary('synonyms','''
meticulous|careful|hurried|wealthy|uneasy|extremely attentive to detail
reluctant|unwilling|eager|forgetful|distant|hesitant or unwilling
concise|brief|confusing|friendly|ancient|expressed in few words
obsolete|outdated|delicate|valuable|ordinary|no longer current or in use
impartial|unbiased|incomplete|impatient|unusual|fair and free from favoritism
resilient|tough|careless|fragile|motionless|able to recover after difficulty
frugal|economical|generous|reckless|cheerful|careful to avoid waste
candid|frank|timid|polished|secretive|honest and direct
vigilant|watchful|drowsy|confused|talkative|alert to possible danger
plausible|believable|certain|impossible|unpleasant|apparently reasonable or believable
coax|persuade|punish|ignore|announce|gently persuade
scrutinize|examine|decorate|discard|remember|examine closely
alleviate|ease|predict|increase|conceal|make less severe
replenish|refill|remove|measure|divide|fill up again
prohibit|forbid|permit|suggest|describe|formally forbid
nimble|agile|noisy|heavy|patient|quick and light in movement
sturdy|strong|elegant|hollow|flexible|solidly built and strong
tranquil|peaceful|crowded|sudden|colorful|calm and peaceful
elaborate|detailed|plain|accidental|expensive|complex and carefully developed
sparse|scattered|dense|precise|level|thinly distributed
feasible|possible|impressive|essential|finished|capable of being done
abrupt|sudden|gradual|regular|polite|unexpectedly sudden
conspicuous|noticeable|hidden|familiar|temporary|easy to see or notice
wary|cautious|confident|angry|weary|alert to possible problems
verify|confirm|doubt|invent|delay|establish that something is true
''')
vocabulary('antonyms','''
scarce|plentiful|rare|costly|hidden|in short supply
rigid|flexible|straight|solid|narrow|stiff and resistant to bending
temporary|permanent|brief|timely|uncertain|lasting for a limited time
expand|shrink|stretch|extend|open|become larger
conceal|reveal|cover|protect|collect|hide from view
optimistic|pessimistic|hopeful|certain|energetic|expecting a favorable result
humble|arrogant|modest|quiet|poor|not boastful about one's importance
transparent|opaque|clear|fragile|colorless|allowing objects to be seen through it
voluntary|compulsory|generous|helpful|intentional|done by choice
initial|final|early|brief|original|occurring at the beginning
permit|forbid|allow|request|offer|allow
mitigate|worsen|reduce|measure|ignore|make less severe
diligent|negligent|careful|exhausted|skilled|showing steady care and effort
include|exclude|gather|contain|combine|have as a part
hostile|friendly|angry|formal|distant|unfriendly or antagonistic
approximate|exact|nearby|rough|large|close to but not precisely correct
perilous|safe|risky|remote|exciting|dangerous
abundant|scarce|ample|varied|useful|present in a large quantity
accelerate|decelerate|hasten|continue|depart|increase speed
unanimous|divided|complete|loud|certain|in full agreement
superficial|thorough|shallow|visible|simple|limited to the surface or lacking depth
reinforce|weaken|support|repair|repeat|make stronger
legible|unreadable|written|neat|lengthy|clear enough to read
seldom|frequently|rarely|recently|quietly|not often
wane|increase|fade|pause|vanish|decrease in strength or extent
''')
# Relation is explained independently of distractor placement.
for line in '''
index : book :: legend : ?|map|voyage|library|sentence|An index helps a reader locate information in a book; a legend helps a reader interpret symbols on a map.|reference aid to document
thermometer : temperature :: odometer : ?|distance|pressure|speed|direction|A thermometer measures temperature; an odometer measures distance traveled.|instrument to quantity
bud : blossom :: caterpillar : ?|butterfly|nest|leaf|antenna|A bud develops into a blossom; a caterpillar develops into a butterfly.|developmental stage
editor : manuscript :: mechanic : ?|engine|garage|wrench|driver|An editor works to improve a manuscript; a mechanic works to repair an engine.|worker to object
stanza : poem :: scene : ?|play|audience|actor|costume|A stanza is a structural part of a poem; a scene is a structural part of a play.|part to whole
insulate : heat loss :: waterproof : ?|water penetration|water temperature|surface color|air pressure|Insulating reduces heat loss; waterproofing prevents water penetration.|action to prevented effect
tentative : definite :: doubtful : ?|certain|careful|puzzled|curious|Tentative and definite contrast uncertainty and certainty, as doubtful and certain do.|opposites
orchard : fruit :: quarry : ?|stone|water|trees|grain|An orchard is a source of fruit; a quarry is a source of stone.|source to product
whisper : speak :: stroll : ?|walk|race|rest|wander|Whispering is a quiet way of speaking; strolling is a leisurely way of walking.|manner of action
blueprint : building :: outline : ?|essay|pencil|dictionary|paragraph mark|A blueprint plans a building; an outline plans an essay.|plan to product
fragile : shatter :: flammable : ?|ignite|freeze|bend|dissolve|Something fragile is easily shattered; something flammable is easily ignited.|property to tendency
seed : sow :: evidence : ?|present|forget|assume|suspect|One sows a seed and presents evidence; preserve object-to-action order.|object to appropriate action
opaque : light :: soundproof : ?|sound|wall|echo chamber|darkness|An opaque material blocks light; soundproof material blocks sound.|barrier property
composer : score :: choreographer : ?|dance|orchestra|theater|instrument|A composer creates a musical score; a choreographer creates a dance.|creator to creation
anecdote : story :: sonnet : ?|poem|author|novel|rhyme|An anecdote is a kind of story; a sonnet is a kind of poem.|type to category
expand : expansion :: decide : ?|decision|decisive|deciding|decided|Expansion names the act or result of expanding; decision names the act or result of deciding.|verb to noun
compass : direction :: balance scale : ?|mass|distance|volume|time|A compass indicates direction; a balance scale compares masses.|tool to measured property
rough : smooth :: uneven : ?|level|steep|coarse|narrow|Rough contrasts with smooth; uneven contrasts with level.|opposites
preface : beginning :: epilogue : ?|ending|conflict|author|chapter|A preface appears at the beginning of a book; an epilogue appears at its end.|book element to position
sieve : separate :: clamp : ?|hold|cut|polish|measure|A sieve separates materials; a clamp holds objects firmly.|tool to function
'''.strip().splitlines():
 stem,key,a,b,c,why,family=line.split('|')
 add('verbal','analogies','Complete the analogy: '+stem,key,[a,b,c],why,'Describe the first relationship in a short sentence and preserve its direction.',2,family)
for line in '''
Which word is not a unit of length?|liter|meter|inch|mile|A liter measures volume; the others measure length.|measurement category
Which word is not a musical instrument?|melody|oboe|cello|trombone|A melody is a sequence of notes, not an instrument.|music category
Which word is not a type of precipitation?|breeze|rain|sleet|hail|A breeze is moving air; rain, sleet and hail fall from clouds.|weather category
Which word is not a written account of someone's life?|atlas|biography|memoir|autobiography|An atlas is a collection of maps; the other words name life accounts.|book category
Which word is not a synonym for repair?|damage|mend|restore|fix|Damage means harm; the others mean to put something right.|repair meanings
Which word does not describe a lack of sound?|clamorous|silent|hushed|noiseless|Clamorous means noisy, whereas the others describe quiet.|sound meanings
Which word is not a polygon?|sphere|hexagon|triangle|pentagon|A sphere is a three-dimensional curved solid; the others are plane polygons.|shape category
Which word is not a means of fastening objects?|cushion|rivet|staple|bolt|A cushion provides padding; the others can fasten objects.|object function
Which word is not a form of running water?|glacier|brook|stream|river|A glacier is a mass of ice; the others are flowing bodies of liquid water.|water category
Which word is not a synonym for hesitation?|readiness|reluctance|indecision|uncertainty|Readiness indicates preparedness; the others can indicate hesitation.|attitude meanings
Which word is not a tool used to cut material?|anvil|shears|saw|knife|An anvil is a working surface; the others have cutting edges.|tool function
Which word is not a body part of a bird?|gill|beak|wing|feather|Birds breathe with lungs rather than gills.|animal category
Which word is not a synonym for praise?|rebuke|commendation|tribute|acclaim|A rebuke expresses disapproval; the others express admiration.|evaluation meanings
Which word is not a way of preserving food?|serving|freezing|drying|canning|Serving presents food for eating rather than preserving it.|process purpose
Which activity primarily prepares performers for a later presentation?|rehearsal|recital|concert|show|A rehearsal is preparation for a performance; the others name performances.|activity purpose
'''.strip().splitlines():
 stem,key,a,b,c,why,family=line.split('|')
 add('verbal','classifications',stem,key,[a,b,c],why,'Identify the stated category, then test each choice against it.',1,family)
for line in '''
Every item in the blue bin is recyclable. This jar is in the blue bin. Which conclusion must follow?|This jar is recyclable.|Every recyclable item is in the blue bin.|Every jar is in the blue bin.|No item outside the bin is recyclable.|The jar belongs to the group whose members are all recyclable. The rule does not run backward.|class membership|1
No members of the chess club are on the sailing team. Kira is on the sailing team. What must be true?|Kira is not in the chess club.|Kira dislikes chess.|Every sailor is a student.|Kira belongs to no other club.|The two named groups do not overlap; nothing is said about preferences or other clubs.|disjoint sets|2
Some museum guides speak Japanese. Every museum guide wears a badge. What must be true?|Some badge wearers speak Japanese.|All badge wearers speak Japanese.|All Japanese speakers are guides.|No guide speaks any other language.|The guides who speak Japanese also wear badges. Some cannot be changed to all.|existential intersection|2
A workshop runs only if at least six people register. The workshop ran. What must be true?|At least six people registered.|Exactly six people attended.|Every registered person attended.|Fewer than six people registered.|Running requires six registrations; attendance and exact totals are not specified.|necessary condition|2
Whenever the alarm sounds, the caretaker checks the panel. The caretaker did not check the panel today. What follows from these statements?|The alarm did not sound today.|The alarm is broken.|The caretaker checked another room.|The alarm sounded once today.|If the alarm had sounded, the stated rule would require a panel check. The cause of the silence is unknown.|contrapositive|3
Only sealed envelopes enter the sorting machine. Envelope R entered the machine. What must be true?|Envelope R was sealed.|Every sealed envelope entered.|Envelope R contained a letter.|No envelope was rejected.|Entry requires sealing; the statement does not require all sealed envelopes to enter.|only condition|2
All cedar boxes are wooden. Some wooden boxes are painted. Which conclusion is justified?|The statements do not determine whether any cedar box is painted.|All cedar boxes are painted.|No cedar box is painted.|All painted boxes are cedar.|The painted wooden boxes might include cedar boxes, but the statements do not say so.|undetermined overlap|3
The red folder must be filed before the green folder. The blue folder must be filed after the green folder. Which folder must be filed first among these three?|red|green|blue|The order cannot be determined.|The constraints give red before green before blue.|ordering|1
Four runners finish with no ties. Uma finishes ahead of Vic; Vic ahead of Wes; and Tia behind Uma but ahead of Vic. Who finishes second?|Tia|Uma|Vic|Wes|The order is Uma, Tia, Vic, Wes.|ordering insertion|2
A badge is either round or square, never both. Every round badge is gold. This badge is not gold. Which conclusion follows?|It is square.|It is round.|It is silver.|It is both round and square.|A round badge would be gold. Therefore it is not round and must be the other permitted shape.|exhaustive alternatives|3
Exactly one of two switches, A and B, is on. Switch A is off. What must be true?|Switch B is on.|Both switches are off.|Switch B is off.|Switch A is broken.|With exactly one on and A off, B must be on. A switch being off does not mean it is broken.|exclusive choice|1
Every volunteer who handles animals has completed training. Noel is a volunteer who has not completed training. What must be true?|Noel does not handle animals.|Noel cannot ever complete training.|Noel does not volunteer.|Every trained volunteer handles animals.|Animal handling requires training, so the stated lack of training rules out that role.|restricted implication|2
A route uses the tunnel or the bridge, or both. The route does not use the tunnel. What follows?|The route uses the bridge.|The bridge is shorter.|The route uses neither.|The route uses two bridges.|At least one of the two is used. Excluding the tunnel leaves the bridge.|inclusive alternative|1
Every brass key opens cabinet A. Key P does not open cabinet A. Which conclusion must follow?|Key P is not brass.|Key P opens cabinet B.|No key opens cabinet A.|Every nonbrass key opens cabinet A.|A brass key would open A; P does not, so P cannot be brass.|material implication|2
All members of the mural team are artists. No artists on the team are absent today. Which conclusion must follow?|No member of the mural team is absent today.|All artists belong to the mural team.|No student is absent today.|The mural team has exactly ten members.|Each team member is an artist on the team and therefore is not absent. The statements give no team size.|qualified universal|3
'''.strip().splitlines():
 stem,key,a,b,c,why,family,diff=line.split('|')
 add('verbal','logical_reasoning',stem,key,[a,b,c],why,'Use only the stated facts. Do not reverse an implication or change some into all.',int(diff),family)
