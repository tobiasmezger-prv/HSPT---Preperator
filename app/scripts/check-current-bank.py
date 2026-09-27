"""Issue a checksum-bound receipt only after current-bank arithmetic tests pass."""
import json,os,subprocess,sys
from pathlib import Path
from bank_pipeline import bank_hash
root=Path(__file__).resolve().parents[1]
# Refresh export and bank-specific audit from current content before checking.
subprocess.run([sys.executable,str(root/'scripts/calibrate-current-bank.py')],check=True)
node=os.environ.get('HSPT_NODE','node')
subprocess.run([node,str(root/'node_modules/vitest/vitest.mjs'),'run','tests/bank.test.ts','tests/fixture.test.ts'],cwd=root,check=True)
bank=json.loads((root/'content/imports/current-100.json').read_text())
receipt={'bankHash':bank_hash(bank),'status':'passed','checkedIds':[q['id'] for q in bank],'method':'Current-bank Vitest arithmetic, key, classification and uniqueness checks; not human approval or a general natural-language solver.','command':'vitest run tests/bank.test.ts tests/fixture.test.ts'}
(root/'content/calibration/current-100.math.json').write_text(json.dumps(receipt,indent=2)+'\n')
