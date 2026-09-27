"""Read-only evidence gate; never creates human approval or releases content."""
import json,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];S=ROOT/'content/staging/gables-v2';R=ROOT/'content/review/gables-v2'
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def gate():
 bank=json.loads((S/'bank.json').read_text());math=json.loads((S/'validation.json').read_text());audit=json.loads((S/'item-audit.json').read_text());visual=json.loads((S/'visual-review.json').read_text());m=json.loads((R/'manifest.json').read_text());d=json.loads((R/'decisions.json').read_text());sha=H(S/'bank.json')
 assert all(x['bankSha256']==sha for x in [math,audit,visual,m,d]),'Stale evidence'
 assert json.loads((S/'editorial-review.json').read_text())['reviewedBankSha256']==sha
 for k,file in [('auditSha256','item-audit.json'),('mathSha256','validation.json'),('editorialSha256','editorial-review.json'),('visualSha256','visual-review.json')]:assert m[k]==H(S/file)
 assert all(H(S/'assets'/name)==val for name,val in visual['assets'].items())
 assert {x['id'] for x in math['checkedItems']}=={x['id'] for x in bank}=={x['id'] for x in audit['items']}
 assert all(x['status']=='pass' for x in math['checkedItems'])
 assert d['manifestSha256']==H(R/'manifest.json')
 assert len(m['sample'])==len(d['items'])==20 and len({x['id'] for x in d['items']})==20
 assert {x['id'] for x in d['items']}=={x['id'] for x in m['sample']}
 assert not json.loads((S/'overlap-log.json').read_text())['unresolvedIdentifiedMatches']
 reviewed=bool(d['reviewer'] and d['date']) and all(x['decision']=='approve' for x in d['items'])
 integration=json.loads((S/'integration.json').read_text()) if (S/'integration.json').exists() else None
 integrated=bool(integration and integration['bankSha256']==sha and integration['status']=='integrated for local testing')
 return {'integration':'integrated for local testing' if integrated else 'pending','batch':'gables-v2','bankSha256':sha,'contentEvidence':'passed','humanSample':'approved' if reviewed else 'pending or requires revision','releaseReady':False,'remainingGates':([] if reviewed else ['Human decisions for all 20 sampled questions'])+([] if integrated else ['App diagram integration and grading/selection checks'])+['Browser and iPad rendering verification'],'note':'This gate never certifies app integration or deploys. Unsampled items are not individually human-approved.'}
if __name__=='__main__':
 result=gate();print(json.dumps(result,indent=2));(S/'acceptance.json').write_text(json.dumps(result,indent=2)+'\n')
 if '--require-reviewed' in sys.argv and result['humanSample']!='approved':sys.exit(2)
