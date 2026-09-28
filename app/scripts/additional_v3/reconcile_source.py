from pathlib import Path
import re,json,hashlib,base64
import pdfplumber
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'app/content/staging/additional-v3'
AUDIT=ROOT/'app/content/audits/gables-full-2026-09-27'
candidates=[p for p in (ROOT/'sources').glob('*.md') if p.stat().st_size>1000000]
source=next((p for p in candidates if 'All six uploaded PDFs' in p.open().read(200)),ROOT/'output/markdown/HSPT_ALL_SIX_PDFS.md')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
s=source.read_text();chunks=re.split(r'^### (.+) — PDF page (\d+) of (\d+)\n',s,flags=re.M)
assert (len(chunks)-1)//4==156
# Reuse the exact conversion functions, without executing their file-writing code.
code=Path('/private/tmp/convert_hspt_markdown.py').read_text().split("parts=['# HSPT")[0]
ns={};exec(code,ns)
old=json.loads((AUDIT/'sources.json').read_text())['documents'];oldmap={d['id']:d for d in old}
page_lookup={};index=1;docs=[];page_records=[]
for title,filename,key,count in ns['docs']:
 pdfpath=Path('/Users/tobiasmezger/Desktop')/filename
 assert sha(pdfpath)==oldmap[key]['sha256'],key
 with pdfplumber.open(pdfpath) as pdf:
  assert len(pdf.pages)==count
  for pnum,page in enumerate(pdf.pages,1):
   heading,number,total,body=chunks[index:index+4];index+=4
   assert heading==title and int(number)==pnum and int(total)==count
   trans=re.search(r'```text\n(.*?)\n```',body,re.S)[1]
   expected=ns['ocr_page'](key,pnum) if key.endswith('2') else ns['clean'](page.extract_text(layout=True,x_density=5,y_density=9) or '')
   assert trans==expected,(key,pnum,'transcription mismatch')
   im=base64.b64decode(re.search(r'src="data:image/jpeg;base64,([^"]+)"',body)[1],validate=True)
   cached=next(p for p in Path('/private/tmp/hspt-markdown-images').glob(Path(filename).stem+'-*.jpg') if int(p.stem.rsplit('-',1)[1])==pnum)
   assert im==cached.read_bytes(),(key,pnum,'image mismatch')
   loc=f'{title} — PDF page {pnum} of {count}';page_lookup[(key,pnum)]=loc
   page_records.append({'document':key,'page':pnum,'heading':loc,'textMatchesPdfConversion':True,'embeddedImageMatchesPdfRender':True,'imageSha256':hashlib.sha256(im).hexdigest()})
 docs.append({'id':key,'filename':filename,'pdfSha256':sha(pdfpath),'pages':count,'priorFullInspection':oldmap[key]['method']})
 print('Reconciled',key,count,'pages',flush=True)
ledger=json.loads((AUDIT/'source-coverage.json').read_text())
for q in ledger['items']:
 q['markdownQuestionHeading']=page_lookup.get(('test'+str(q['test']),q['questionPdfPage']))
 guide=q.get('answerGuide');q['markdownGuideHeading']=page_lookup.get(('answers'+str(q['test']),guide['page'])) if guide else None
 q['evidenceOrigin']='Reused full inspection from gables-full-2026-09-27, reconciled to this Markdown revision; not a new human approval.'
ledger.update(sourcePath=str(source.relative_to(ROOT)),sourceSha256=sha(source),reconciliation='All 156 text blocks match conversion from PDF/OCR inputs and all embedded page images match the PDF renders. Original six PDF hashes match full audit.',pageRecords=page_records)
(OUT/'source-coverage.json').write_text(json.dumps(ledger,indent=2)+'\n')
(OUT/'source-exceptions.json').write_bytes((AUDIT/'source-exceptions.json').read_bytes())
(OUT/'sources.json').write_text(json.dumps({'primaryMarkdown':str(source.relative_to(ROOT)),'markdownSha256':sha(source),'preferredSyncedPath':'sources/HSPT_ALL_SIX_PDFS.md','syncStatus':'using identical generated fallback; uploaded project copy not visible in local sources mirror' if source.parent.name!='sources' else 'synced','documents':docs,'coverage':{'pages':156,'questionPositions':894,'allSections':True},'priorAudit':'app/content/audits/gables-full-2026-09-27','exceptionsPreserved':True},indent=2)+'\n')
print('Reconciled full Markdown source to prior 894-position review.')
