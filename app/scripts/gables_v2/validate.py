"""Independent exact-rational checker: checks every option, term and diagram input."""
import ast,json,hashlib,operator,math
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; OUT=ROOT/'content/staging/gables-v2'
def calc(s,env=None):
 env=env or {}
 def ev(n):
  if isinstance(n,ast.Constant):return F(str(n.value))
  if isinstance(n,ast.Name):return env[n.id]
  if isinstance(n,ast.UnaryOp):return -ev(n.operand) if isinstance(n.op,ast.USub) else ev(n.operand)
  if isinstance(n,ast.BinOp):return {ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv,ast.FloorDiv:operator.floordiv,ast.Mod:operator.mod,ast.Pow:operator.pow}[type(n.op)](ev(n.left),ev(n.right))
  if isinstance(n,ast.BoolOp):return (all if isinstance(n.op,ast.And) else any)(ev(x) for x in n.values)
  if isinstance(n,ast.Compare):
   vals=[ev(n.left)]+[ev(x) for x in n.comparators]
   return all({ast.Eq:operator.eq,ast.Lt:operator.lt,ast.Gt:operator.gt}[type(op)](vals[i],vals[i+1]) for i,op in enumerate(n.ops))
  raise ValueError(ast.dump(n))
 return ev(ast.parse(str(s),mode='eval').body)
def numeric(s):
 s=str(s).replace('−','-').replace('$','').strip()
 if s.endswith('%'):return calc(s[:-1])/100
 return calc(s)
def series(p):
 terms=[None if x is None else numeric(x) for x in p['terms']]; r=p['rule'];par=p['params'];n=len(terms)+(0 if None in terms else p.get('output',1));a=[]
 for i in range(n):
  if r=='cube_plus_one':v=F((i+1)**3+1)
  elif i==0 or (i==1 and r in ['branches','multiply_branches','mixed_branches','sum_previous']):v=terms[i]
  elif r=='cycle':v=a[-1]+numeric(par[(i-1)%len(par)])
  elif r=='gaps':v=a[-1]+numeric(par[0])+(i-1)*numeric(par[1])
  elif r=='paired_gaps':v=a[-1]+par[0]+((i-1)//2)*par[1]
  elif r=='multiply':v=a[-1]*numeric(par)
  elif r=='affine':v=a[-1]*par[0]+par[1]
  elif r=='branches':v=a[-2]+par[i%2]
  elif r=='multiply_branches':v=a[-2]*par[i%2]
  elif r=='mixed_branches':v=a[-2]*numeric(par[0]) if i%2==0 else a[-2]+numeric(par[1])
  elif r=='sum_previous':v=a[-1]+a[-2]
  elif r=='multiply_cycle':v=a[-1]*numeric(par[(i-1)%len(par)])
  elif r=='rising_multiply':v=a[-1]*(par+i-1)
  elif r=='op_cycle':
   op,x=par[(i-1)%len(par)];v=a[-1]*x if op=='mul' else a[-1]+x
  else:raise ValueError(r)
  a.append(v)
  if i<len(terms) and terms[i] is not None:assert v==terms[i],(i,v,terms[i])
 return a[terms.index(None)] if None in terms else tuple(a[len(terms):]) if p.get('output',1)>1 else a[-1]
def visual_expected(v,check):
 if v['type']=='grids':
  for g in v['panels']:assert len(set(g['shaded']))==len(g['shaded']) and all(0<=x<g['rows']*g['cols'] for x in g['shaded'])
  totals=[g['rows']*g['cols'] for g in v['panels']];counts=[len(g['shaded']) for g in v['panels']]
  if check=='fractions':return {g['label']:F(c,t) for g,c,t in zip(v['panels'],counts,totals)}
  if check=='target':return F(totals[0]*2,3)-counts[0]
  if check=='combined':return F(sum(counts),sum(totals))
  if check=='erase':return F(counts[0]-2,totals[0])
 if v['type']=='bars':
  a=v['values'];assert all(0<=x<=v['maximum'] for x in a) and v['maximum']%v['tick']==0
  if check=='bars':return dict(zip(v['labels'],map(F,a)))
  if check=='barTransfer':return dict(zip(v['labels'],map(F,[a[0],a[1]-2,a[2]+2])))
  if check=='barTotal':return 30-sum(a)
  if check=='barMean':return a[1]-F(sum(a),len(a))
 if v['type']=='rectangles':
  gs=v['panels'];areas=[g['width']*g['height'] for g in gs];per=[2*(g['width']+g['height']) for g in gs]
  if check=='rectangles':return dict(zip(['PP','QP','PA','QA'],per+areas))
  if check=='perimeterGap':return per[1]-per[0]
  if check=='areaRatio':return F(areas[0],areas[1])
  if check=='squareSide':assert math.isqrt(areas[0])**2==areas[0];return math.isqrt(areas[0])
 if v['type']=='angles':
  k=v['known']
  if check=='straight':return 180-k
  if check=='right':return 90-k
  if check=='three':return 180-sum(k)
  if check=='ratio':return F(90*max(k),sum(k))
 raise ValueError(check)
def check(q,p):
 assert len(q['choices'])==len(set(q['choices']))==4
 assert q['guide']['explanation'] and q['guide']['shortcut']
 kind=p['kind'];env=None
 if kind=='series':expected=series(p)
 elif kind=='numeric':expected=calc(p['expression'])
 elif kind=='alphanumeric':
  ts=p['terms'];start=ord(ts[0][0]);assert all(t==chr(start+i*p['letterStep'])+str((i+1)**2) for i,t in enumerate(ts));expected=chr(start+len(ts)*p['letterStep'])+str((len(ts)+1)**2)
 elif kind=='relations':env={k:calc(v) for k,v in p['values'].items()};expected=True
 else:raise ValueError(kind)
 if 'visualCheck' in p:assert visual_expected(q['visual'],p['visualCheck'])==(env if env is not None else expected)
 if kind=='relations':actual=[calc(x,env) for x in p['predicates']]
 elif q['answerFormat']=='numeric_pair':actual=[tuple(numeric(x) for x in c.split(',')) for c in q['choices']]
 elif kind=='alphanumeric':actual=q['choices']
 else:actual=[numeric(x) for x in q['choices']]
 if kind!='relations':assert len(set(actual))==4,'Equivalent answer choices'
 matches=[i for i,v in enumerate(actual) if v==expected]
 assert matches==['ABCD'.index(q['guide']['correctChoiceId'])],(expected,actual,q['guide'])
 return {'id':q['id'],'status':'pass','expected':str(expected),'checks':['all choices','exact answer','all supplied terms' if kind=='series' else 'independent expression/predicates']+(['diagram data'] if 'visualCheck' in p else [])}
def run():
 bank=json.loads((OUT/'bank.json').read_text());proof=json.loads((OUT/'proofs.json').read_text());results=[]
 assert len(bank)==100 and len({q['id'] for q in bank})==100
 assert len({''.join(q['stem'].lower().split()) for q in bank})==100
 for q in bank:
  assert all(q.get(k) for k in ['id','section','skill','format','templateFamily','stem','provenance','reviewStatus','answerFormat'])
  assert q['difficulty'] in [1,2,3]
  assert q['reviewStatus']=='pending_human_review'
  if 'visual' in q:assert q['visual'].get('alt')
 for q in bank:
  try:results.append(check(q,proof[q['id']]))
  except Exception as e:raise AssertionError((q['id'],q['stem'],e)) from e
 digest=hashlib.sha256((OUT/'bank.json').read_bytes()).hexdigest()
 receipt={'bankSha256':digest,'status':'100/100 passed automatic mathematical checks; human review pending','checkedItems':results,'limits':'Arithmetic and intended rules are checked. Difficulty and natural-language interpretation remain editorial judgments; finite sequences cannot have mathematically unique continuations without a rule convention.'}
 (OUT/'validation.json').write_text(json.dumps(receipt,indent=2)+'\n');print(receipt['status']);return receipt
if __name__=='__main__':run()
