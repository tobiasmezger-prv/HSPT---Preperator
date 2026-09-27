"""Build a human review artifact from the shipped questions and guides."""
import ast,json,re
from pathlib import Path
from collections import Counter
root=Path(__file__).resolve().parents[1]

def load_bank():
 text=(root/'src/data/questions.ts').read_text()
 guides=(root/'src/data/answers.ts').read_text()
 questions=[]
 for line in text.splitlines():
  if not line.lstrip().startswith("{id:'dev-"):continue
  item={k:re.search(k+r":'([^']*)'",line).group(1) for k in ['id','skill','stem','templateFamily']}
  item['choices']=ast.literal_eval(re.search(r'choices:(\[[^\]]*\])',line).group(1))
  guide_line=next(l for l in guides.splitlines() if "'"+item['id']+"':" in l)
  item['guide']={k:re.search(k+r":'([^']*)'",guide_line).group(1) for k in ['correctChoiceId','explanation','shortcut']}
  item['difficulty']=[1,2,1,2,1,1,1,2,1,2,2,1][len(questions)]
  questions.append(item)
 questions+=json.loads((root/'src/data/questions.expanded.json').read_text())
 assert len(questions)==100
 return questions
