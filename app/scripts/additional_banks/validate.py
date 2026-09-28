"""Exact arithmetic + structural evidence, explicitly NOT editorial acceptance."""
import ast,collections,json,math,re
from fractions import Fraction as F
from pathlib import Path
from schema import load,digest
ROOT=Path(__file__).resolve().parents[2]/'content/staging/additional-v1'
def number(s):return F(s.replace('−','-').replace(',',''))
def evaluate(expression):
 def run(n):
  if isinstance(n,ast.Constant) and type(n.value) in (int,float):return F(str(n.value))
  if isinstance(n,ast.UnaryOp) and isinstance(n.op,(ast.USub,ast.UAdd)):
   return -run(n.operand) if isinstance(n.op,ast.USub) else run(n.operand)
  if isinstance(n,ast.BinOp):
   a,b=run(n.left),run(n.right)
   if isinstance(n.op,ast.Add):return a+b
   if isinstance(n.op,ast.Sub):return a-b
   if isinstance(n.op,ast.Mult):return a*b
   if isinstance(n.op,ast.Div):return a/b
   if isinstance(n.op,ast.Pow):
    assert b.denominator==1 and abs(b)<=10
    return a**int(b)
  if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and not n.keywords:
   a=[run(x) for x in n.args];name=n.func.id
   if name=='gcd':return F(math.gcd(*(int(x) for x in a)))
   if name=='lcm':return a[0]*a[1]/math.gcd(int(a[0]),int(a[1]))
   if name=='sqrt':
    x=a[0];num=math.isqrt(x.numerator);den=math.isqrt(x.denominator)
    assert F(num*num,den*den)==x
    return F(num,den)
   if name=='median':
    a.sort();n=len(a);return a[n//2] if n%2 else (a[n//2-1]+a[n//2])/2
   if name=='mode':
    c=collections.Counter(a);best=c.most_common();assert best[0][1]>best[1][1];return best[0][0]
   if name=='roundto':return F(math.floor(a[0]/a[1]+F(1,2)))*a[1]
   if name=='digit':return F(math.floor(a[0]*10**int(a[1]))%10)
   if name=='greatest_int_lt':
    coefficient,offset,bound=a;assert coefficient>0
    return F(math.ceil((bound-offset)/coefficient)-1)
  raise ValueError('Unsupported arithmetic expression')
 return run(ast.parse(expression,mode='eval').body)
def math_check(q):
 result=evaluate(q['oracleExpression']);values=[number(x) for x in q['choices']]
 assert len(set(values))==4,('Equivalent numerical choices',q['id'])
 matches=[i for i,x in enumerate(values) if x==result]
 assert matches==['ABCD'.index(q['guide']['correctChoiceId'])],(q['id'],result,matches)
 return {'id':q['id'],'result':str(result),'choiceValues':[str(v) for v in values],'status':'exact_expression_check_passed','limitation':'Stem-to-expression translation and explanation need editorial review.'}
def main():
 banks,passages=load(ROOT);report={'manifestSha256':digest(ROOT/'manifest.json'),'status':'structural_checks_passed_editorial_pending','sections':{},'releaseReady':False}
 audit=[];maths=[]
 for section,b in banks.items():
  qs=b['questions'];assert len(qs)==100
  c=collections.Counter(q['guide']['correctChoiceId'] for q in qs);assert set(c.values())=={25}
  skills=collections.Counter(q['skill'] for q in qs);diff=collections.Counter(q['difficulty'] for q in qs)
  lengths=[]
  for q in qs:
   key='ABCD'.index(q['guide']['correctChoiceId'])
   lens=[len(x) for x in q['choices']]
   if lens[key]>max(l for i,l in enumerate(lens) if i!=key):lengths.append(q['id'])
   if section=='mathematics':maths.append(math_check(q))
   audit.append({'id':q['id'],'structural':'passed','answerGuidePresence':'passed','editorial':'pending','semanticOriginality':'pending','humanReview':'pending','rendering':'pending','numericCheck':'exact_expression_check_passed' if section=='mathematics' else 'not_applicable'})
  report['sections'][section]={'count':len(qs),'skills':dict(skills),'difficulty':dict(diff),'answerPositions':dict(c),'largestFamily':max(collections.Counter(q['templateFamily'] for q in qs).values()),'correctAnswerStrictlyLongest':len(lengths),'longestAnswerIds':lengths,'warning':'Answer-length cueing, distractor plausibility, family variety and difficulty require editorial review.'}
 sizes=collections.Counter(q['passageId'] for q in banks['reading']['questions'])
 assert set(sizes)==set(passages)
 dp={0:[]}
 for pid,count in sizes.items():
  for total,group in list(dp.items())[::-1]:
   if total+count<=62 and total+count not in dp:dp[total+count]=group+[pid]
 assert 62 in dp
 report['readingAssembly']={'completePassageGroups':dict(sizes),'example62QuestionPassages':dp[62],'passageWordCounts':{k:sum(len(p.split()) for p in v['paragraphs']) for k,v in passages.items()},'limitation':'Arithmetic assembly only; not an approved timed form. A ten-question burst cannot be made from these complete 6/7-item groups; use a disclosed 6/7-item group or add reviewed shorter groups.'}
 def write(name,data):(ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
 write('validation.json',report);write('item-audit.json',{'manifestSha256':report['manifestSha256'],'items':audit})
 write('mathematics-checks.json',{'bankSha256':digest(ROOT/'mathematics.json'),'method':'Separately implemented AST interpreter using exact fractions; evaluates all four numerical choices. Author-supplied model expressions are not independent semantic proof.','items':maths})
 # Automated exact matching against the accepted local bank, and long phrase triage against extracted sources.
 old=json.loads((ROOT.parents[2]/'public/content/banks/quantitative-v0001.json').read_text())
 norm=lambda s:' '.join(re.findall(r'\w+',s.casefold()))
 oldstems={norm(q['stem']) for q in old['questions']}
 source=Path('/private/tmp/hspt-gables');texts={n:norm((source/(n+'-full.txt')).read_text()) for n in ['test1','test3'] if (source/(n+'-full.txt')).exists()}
 flags=[];logs=[]
 for b in banks.values():
  for q in b['questions']:
   hits=[]
   if norm(q['stem']) in oldstems:hits.append('exact_normalized_stem_in_accepted_quantitative_bank')
   words=norm(q['stem']).split()
   for name,txt in texts.items():
    if any(' '.join(words[i:i+12]) in txt for i in range(max(0,len(words)-11))):hits.append(name+':12_word_stem_match')
   if hits:flags.append({'id':q['id'],'flags':hits})
   logs.append({'id':q['id'],'automatedFlags':hits,'semanticReview':'pending','scannedTest2Comparison':'pending','resolution':'not_cleared_for_release'})
 write('overlap-log.json',{'manifestSha256':report['manifestSha256'],'status':'triage_only_semantic_review_pending','sourcesScanned':list(texts),'missingTextSource':'test2 (scanned PDF; visual full comparison still required)','flags':flags,'items':logs})
 print(json.dumps({'counts':{s:r['count'] for s,r in report['sections'].items()},'mathChecks':len(maths),'reading62Assembly':True,'overlapTriageFlags':len(flags),'releaseReady':False}))
if __name__=='__main__':main()
