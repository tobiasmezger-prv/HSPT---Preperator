#!/usr/bin/env python3
"""Build a source-only GitHub handoff; never uploads or deploys."""
from pathlib import Path
import hashlib, shutil, zipfile
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'output/github'
NAME='HSPT-Phase-IV-v0.4.0'
DEST=OUT/NAME
roots=['app','.github','.gitignore','README.md','RELEASE_NOTES.md','GITHUB_UPLOAD.md','HSPT_iPad_Prep_PRD.md','HSPT_Phase_III_PRD.md','QUESTION_BANK_CREATION_PROCESS.md']
excluded={'node_modules','dist','__pycache__','.git','.pnpm-store'}
files=[]
for name in roots:
 p=ROOT/name
 for f in sorted(p.rglob('*')) if p.is_dir() else [p]:
  rel=f.relative_to(ROOT)
  if not f.is_file() or any(x in excluded for x in rel.parts):continue
  if f.name=='.DS_Store' or f.name.startswith('.env') or f.suffix in {'.pyc','.tsbuildinfo','.zip'}:continue
  if f.name.startswith(('qa-','figure-check-')):continue
  files.append(f)
# Preserve previous delivery outputs and all project/source files.
if DEST.exists():
 raise SystemExit('Delivery folder already exists; choose a new version or preserve it before rebuilding.')
DEST.mkdir(parents=True)
lines=[]
for f in files:
 rel=f.relative_to(ROOT); target=DEST/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(f,target)
 lines.append(hashlib.sha256(target.read_bytes()).hexdigest()+'  '+rel.as_posix())
(DEST/'PACKAGE_CONTENTS.sha256').write_text('\n'.join(lines)+'\n')
archive=OUT/(NAME+'-GitHub.zip')
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for f in sorted(DEST.rglob('*')):
  if f.is_file():z.write(f,f.relative_to(OUT))
(OUT/(archive.name+'.sha256')).write_text(hashlib.sha256(archive.read_bytes()).hexdigest()+'  '+archive.name+'\n')
print(f'{len(files)} source files; {archive.stat().st_size:,} bytes; {archive}')
