"""Build a human review artifact from the shipped questions and guides."""
import ast,json,re
from pathlib import Path
from collections import Counter
root=Path(__file__).resolve().parents[1]
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
counts=Counter(q['skill'] for q in questions)
out=['# Quantitative practice bank — review edition','',
'**Status: 100 original drafts; arithmetic checks passed; independent human approval pending.**','',
'This bank supports mixed and skill-focused 10-question practice. It is not an official test, a validated full-section simulation, or a claim of official topic weights. No source questions were copied. Difficulty labels are provisional editorial judgments, not calibrated measurements.','',
'## Coverage','',*['- '+k.replace('_',' ')+': '+str(v) for k,v in counts.items()],'',
'## Reference basis','',
'The publisher describes number series, number manipulation, and geometric and nongeometric comparisons. The PRD’s symbolic and odd-one-out categories are supplemental reasoning practice. Four geometric comparison problems are included under numerical comparisons; this text-first bank does not provide a comprehensive visual-geometry curriculum.','',
'- [STS: HSPT overview](https://www.ststesting.com/hp_int_sts.pdf)',
'- [Peterson’s: HSPT sections](https://www.petersons.com/blog/hspt-sections-and-their-importance-gearing-up-for-test-day/)','',
'## Optional full-bank reference','',
'The normal review is now 20 selected questions per 100, not all 100. Use [the fixed sample](review/current-100/SAMPLE_REVIEW.md) and [the import process](QUESTION_IMPORT_PROCESS.md). This full listing remains an optional reference for investigating issues.','',
'Approval records belong here or in a separate review record. A checkbox alone does not automatically change the shipped bank’s pending status. After review, reconcile the approved content with the app and rerun validation.','']
for i,q in enumerate(questions):
 if i%20==0:out+=['## Batch '+str(i//20+1)+' (questions '+str(i+1)+'–'+str(min(i+20,100))+')','']
 out+=['### '+str(i+1)+'. '+q['id'],'',q['stem'],'',*['- '+c+'. '+v for c,v in zip('ABCD',q['choices'])],'',
 '**Key:** '+q['guide']['correctChoiceId']+' — '+q['choices']['ABCD'.index(q['guide']['correctChoiceId'])],'',
 '**Explanation:** '+q['guide']['explanation'],'','**Quick tip:** '+q['guide']['shortcut'],'',
 '**Skill:** '+q['skill']+' · **Difficulty:** '+str(q['difficulty'])+'/3 · **Family:** '+q['templateFamily'],'',
 '- [ ] Independently solved; one defensible answer; explanation and tip checked.',
 '- Reviewer / date / edits: ____________________','']
(root/'content/QUESTION_BANK_REVIEW.md').write_text('\n'.join(out))
print(dict(counts))
