import random
banks={s:[] for s in ['verbal','reading','mathematics','language']}
passages=[]
def add(section,skill,stem,answer,wrong,explanation,tip,difficulty=2,family=None,**extra):
    n=len(banks[section])+1
    choices=[str(answer)]+[str(x) for x in wrong]
    assert len(choices)==4 and len(set(choices))==4,(section,n,choices)
    # Balanced positions without a visible ABCD cycle. Choices are deterministic.
    positions=list(range(4))*25
    random.Random('additional-v1-'+section).shuffle(positions)
    pos=positions[n-1]; choices[0],choices[pos]=choices[pos],choices[0]
    q=dict(id=f'{section[:3]}-a1-{n:03}',revision=1,section=section,skill=skill,
           format=skill,difficulty=difficulty,templateFamily=family or skill,
           stem=stem,choices=choices,guide=dict(correctChoiceId='ABCD'[pos],explanation=explanation,shortcut=tip),
           provenance=dict(origin='original_agent_authored_draft',authoredAt='2026-09-27'),
           calibrationReference='PLAN.md#calibration-sources',reviewStatus='pending_human_review',**extra)
    banks[section].append(q)
    return q
