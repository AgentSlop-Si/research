#!/usr/bin/env python3
"""Read-only candidate/source integrity audit; only this review's output is written."""
import json,hashlib
from pathlib import Path
C=Path('/workspace/shared/alg036_thin_deficit_20261019_0125')
R=Path('/workspace/shared/alg036_thin_deficit_review_20261019_0128')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(C/'REPORT.md')=='ae348fde6e14b20f3bb7227a7c56c37d979136a5eed1540de933bf940e97b851'
assert sha(C/'MANIFEST.sha256')=='829f407ab9681470de0838856ee64eb9611e56214d6f893a2f1bc63e6f4776b5'
files=[]
for line in (C/'MANIFEST.sha256').read_text().splitlines():
    expected,rel=line.split('  ',1);p=C/rel
    actual=sha(p);assert expected==actual
    files.append({'file':rel,'sha256':actual,'bytes':p.stat().st_size})
assert {x['file'] for x in files}=={str(p.relative_to(C)) for p in C.rglob('*') if p.is_file() and p.name!='MANIFEST.sha256'}
sourcechecks=[]
for source in json.loads((C/'SOURCE_MANIFEST.json').read_text())['sources']:
    if 'source_path' not in source:continue
    original=Path(source['source_path']);copy=C/source['local_copy']
    assert original.read_bytes()==copy.read_bytes()
    assert sha(copy)==source['sha256'] and copy.stat().st_size==source['bytes']
    sourcechecks.append({'original':str(original),'copy':source['local_copy'],'sha256':sha(copy),'bytes':copy.stat().st_size})
# Integrity of accepted baseline and accepted review, without running their code.
baselines=[]
for root in [Path('/workspace/shared/alg036_endpoint_20261018_2053'),Path('/workspace/shared/alg036_endpoint_review_20261018_2112')]:
    checked=0
    for line in (root/'MANIFEST.sha256').read_text().splitlines():
        expected,rel=line.split('  ',1); assert sha(root/rel)==expected;checked+=1
    baselines.append({'directory':str(root),'manifest_sha256':sha(root/'MANIFEST.sha256'),'entries_verified':checked})
(R/'CANDIDATE_MANIFEST.sha256').write_bytes((C/'MANIFEST.sha256').read_bytes())
result={'status':'PASS','candidate_directory':str(C),'candidate_report_sha256':sha(C/'REPORT.md'),'candidate_manifest_sha256':sha(C/'MANIFEST.sha256'),'candidate_payload':files,'source_copy_checks':sourcechecks,'baseline_integrity':baselines,'candidate_modified':False,'historical_program_execution':False,'external_writes':False,'primary_source':{'url':'https://math.berkeley.edu/~mchrist/Papers/bcct11.pdf','independently_opened':True,'checked_printed_pages':[1,2,3,9,12],'checked_sections':['Definition 1.1','Example 1.6','Definition 2.1','Remark 2.2','Proposition 2.8'],'pdf_body_archived':False,'pdf_sha256':None,'verification_basis':'Author-hosted PDF read with web tool; real coisometry form and constant-one measurable-input assertion verified.'}}
print(json.dumps(result,indent=2,sort_keys=True))
