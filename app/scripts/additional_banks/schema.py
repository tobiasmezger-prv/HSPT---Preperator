"""Shared authoring-only schema/loader. Never authorizes production publication."""
import hashlib
import json
from pathlib import Path

SECTIONS = {'verbal','reading','mathematics','language'}
FIELDS = ('id','section','skill','format','templateFamily','stem','provenance','calibrationReference')
def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def validate(bank, passages):
    assert bank['schemaVersion'] == 'hspt-draft-1'
    assert bank['section'] in SECTIONS
    seen=set(); signatures=set()
    for q in bank['questions']:
        assert all(q.get(k) for k in FIELDS), q.get('id')
        assert q['section']==bank['section'] and q['id'] not in seen
        seen.add(q['id'])
        assert q['revision']>=1 and q['difficulty'] in [1,2,3]
        assert q['reviewStatus']=='pending_human_review'
        assert len(q['choices'])==4 and all(isinstance(x,str) and x.strip() for x in q['choices'])
        # Letter case is the tested distinction in capitalization questions.
        normalize=(lambda x:x.strip()) if q['skill']=='capitalization' else (lambda x:x.casefold().strip())
        assert len(set(normalize(x) for x in q['choices']))==4, q['id']
        g=q['guide']; assert g['correctChoiceId'] in list('ABCD')
        assert g['explanation'].strip() and g['shortcut'].strip()
        signature=(q['stem'].casefold(),tuple(sorted(q['choices'])),q.get('passageId'))
        assert signature not in signatures,q['id']; signatures.add(signature)
        if q['section']=='reading' and q['format']=='standalone_vocabulary':
            assert q.get('targetWord')
            assert not any(k in q for k in ['passageId','passageRevision','evidenceParagraphs'])
        elif q['section']=='reading':
            p=passages[q['passageId']]
            assert q['passageRevision']==p['revision']
            assert all(isinstance(i,int) and 1<=i<=len(p['paragraphs']) for i in q['evidenceParagraphs'])
            assert q['evidenceParagraphs']
    return bank
def load(root):
    root=Path(root); m=json.loads((root/'manifest.json').read_text())
    assert m['schemaVersion']=='hspt-draft-1' and m['status']=='draft_not_for_publication'
    assert set(m['sections'])==SECTIONS
    def read(entry):
        path=(root/entry['file']).resolve()
        assert path.parent==root.resolve(), 'Unexpected path'
        assert digest(path)==entry['sha256'], 'Stale checksum'
        return json.loads(path.read_text())
    passages={p['id']:p for p in read(m['passages'])['passages']}
    result={}; ids=set()
    for section,entry in m['sections'].items():
        bank=validate(read(entry),passages)
        assert bank['section']==section and len(bank['questions'])==entry['questionCount']
        for q in bank['questions']:
            assert q['id'] not in ids; ids.add(q['id'])
        result[section]=bank
    return result,passages
