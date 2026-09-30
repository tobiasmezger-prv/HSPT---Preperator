"""Inventory the two Markdown collections without treating OCR or old audits as new approval."""
from pathlib import Path
import hashlib,json,re
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'app/content/staging/source-import-v1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def section(n):
    return next(s for limit,s in [(60,'verbal'),(112,'quantitative'),(174,'reading'),(238,'mathematics'),(298,'language')] if n<=limit)
def write(name,obj):
    p=OUT/name
    if p.exists():
        raise SystemExit(f'Refusing to overwrite staged review work: {p}')
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def main():
    OUT.mkdir(parents=True,exist_ok=True)
    if (OUT/'inventory.json').exists():raise SystemExit('Inventory already exists; reconcile changes explicitly instead of overwriting review work.')
    gables=ROOT/'output/markdown/HSPT_ALL_SIX_PDFS.md'
    barrons=ROOT/'output/HSPT Prep Barrons/HSPT Prep Barrons.md'
    prior=ROOT/'app/content/staging/additional-v3/source-coverage.json'
    ledger=json.loads(prior.read_text())
    gs=gables.read_text();bs=barrons.read_text()
    blocks=re.split(r'^### (.+) — PDF page (\d+) of (\d+)\n',gs,flags=re.M)
    pages=[]
    for i in range(1,len(blocks),4):
        heading,page,total,body=blocks[i:i+4];text=re.search(r'```text\n(.*?)\n```',body,re.S)
        pages.append({'heading':heading,'page':int(page),'text':text[1] if text else '', 'locator':f'{heading} — PDF page {page} of {total}'})
    assert len(pages)==156
    ghash=sha(gables)
    matches=ledger.get('sourceSha256')==ghash
    items=[]
    for item in ledger['items']:
        t,n=item['test'],item['question'];page=next(p for p in pages if p['heading']==f'Test {t} — Questions' and p['page']==item['questionPdfPage'])
        items.append({'id':f'gables-{t}-{n:03}','sourceForm':f'gables-{t}','sourceQuestion':n,'section':section(n),'sourcePath':str(gables.relative_to(ROOT)),'sourceSha256':ghash,'locator':page['locator'],'sourceKey':item.get('answerGuide',{}).get('letter'),'priorAuditReusable':matches,'knownExceptions':item.get('exceptions',[]),'disposition':'pending_checks','remaining':['normalize stem/choices/passages/figures','check scan fidelity','independently verify answer/explanation and consistency','deduplicate against both sources and live bank']})
    # Retain the page locator around every numbered Barron's transcription.
    clean=re.sub(r'<img[^>]+>','',bs)
    positions=list(re.finditer(r'^\*\*(\d+)\.\*\*\s*',clean,re.M))
    assert len(positions)==298 and [int(x[1]) for x in positions]==list(range(1,299))
    extracted=[]
    for i,m in enumerate(positions):
        n=int(m[1]);headings=list(re.finditer(r'^### (.+)$',clean[:m.start()],re.M));locator=headings[-1][1]
        end=positions[i+1].start() if i+1<len(positions) else clean.find('<a id="answer-key"',m.end())
        if end<0:end=len(clean)
        raw=clean[m.end():end].split('\n### ')[0].split('\n<a id=')[0].strip()
        items.append({'id':f'barrons-1-{n:03}','sourceForm':'barrons-1','sourceQuestion':n,'section':section(n),'sourcePath':str(barrons.relative_to(ROOT)),'sourceSha256':sha(barrons),'locator':locator,'sourceKey':None,'disposition':'pending_checks','remaining':['transcribe key from embedded answer-key image','normalize and check scan fidelity','independently verify answer/explanation and consistency','deduplicate against both sources and live bank']})
        extracted.append({'id':f'barrons-1-{n:03}','locator':locator,'rawTranscription':raw})
    assert len(items)==1192 and len({q['id'] for q in items})==1192
    write('inventory.json',{'expected':1192,'calibration':'not_applicable_source_import','items':items})
    write('source-pages.json',{'gables':pages,'barronsQuestions':extracted})
    write('source-import.json',{'policy':'source-import-20-per-section-v1','inventorySha256':sha(OUT/'inventory.json'),'distribution':{'status':'unrecorded','basis':''},'sources':[{'path':str(p.relative_to(ROOT)),'sha256':sha(p)} for p in [gables,barrons]],'priorGablesAuditHashMatches':matches})
    write('bank.json',[])
    (OUT/'STATUS.md').write_text('''# Phase IV source import — staged inventory

All 1,192 source positions are inventoried: Gables 894 and Barron’s 298. The live bank still contains its original 500 questions.

This is an inventory, not a completed import or correctness review. `source-pages.json` retains text and page locators; embedded images remain in the two reference Markdown files. `bank.json` is intentionally empty until source questions have been normalized and checked. No approval records or ready-for-approval samples have been fabricated.

Next: normalize every item (including passages and figures), inspect scans and keys, independently check answers/explanations, resolve known defects and duplicates, and record item-level evidence. Then generate five 20-question review packets for user approval. After approval, the existing release tool appends **all** checked unique source questions, including unsampled questions, and updates section counts and the overall index. No additional Gables self-calibration is required.
''')
    print(f'Inventoried {len(items)} source positions; prior Gables audit hash matches: {matches}. No live questions changed.')
if __name__=='__main__':main()
