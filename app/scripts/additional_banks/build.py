"""Reproduce the original draft banks; never overwrites human decisions."""
import json
from pathlib import Path
import verbal,reading,mathematics,language
from common import banks,passages
from schema import validate,digest
ROOT=Path(__file__).resolve().parents[2]/'content/staging/additional-v1'
def write(name,obj):
 (ROOT/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')

def main():
 ROOT.mkdir(parents=True,exist_ok=True)
 pmap={p['id']:p for p in passages}
 write('reading-passages.json',dict(schemaVersion='hspt-draft-1',passages=passages))
 m=dict(schemaVersion='hspt-draft-1',batchId='additional-v1',status='draft_not_for_publication',sections={},passages={'file':'reading-passages.json','sha256':digest(ROOT/'reading-passages.json')})
 for section,questions in banks.items():
  assert len(questions)==100
  b=dict(schemaVersion='hspt-draft-1',batchId=f'{section}-additional-v1',section=section,version=1,status='draft_not_for_publication',questions=questions)
  validate(b,pmap)
  filename=section+'.json';write(filename,b)
  m['sections'][section]={'file':filename,'version':1,'questionCount':len(questions),'sha256':digest(ROOT/filename)}
 write('manifest.json',m)
 print('Wrote four 100-question draft banks and',len(passages),'original passages.')
if __name__=='__main__':main()
