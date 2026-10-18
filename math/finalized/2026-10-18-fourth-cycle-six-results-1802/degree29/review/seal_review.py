#!/usr/bin/env python3
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
b=json.loads((R/'CANDIDATE_BINDING.json').read_text());a=json.loads((R/'ARITHMETIC.json').read_text());s=json.loads((R/'SUPPLEMENTAL.json').read_text());c=json.loads((R/'COLD_REPLAY.json').read_text())
assert all(x['verdict']=='PASS' for x in [b,a,s,c])
C=Path(b['candidate_directory']);assert sha(C/'MANIFEST.json')==b['candidate_manifest_sha256'] and sha(C/'DEGREE29_LITERAL_CERTIFICATE.json')==b['candidate_certificate_sha256']
for f in json.loads((C/'MANIFEST.json').read_text())['files']:
 p=C/f['path'];assert p.stat().st_size==f['bytes'] and sha(p)==f['sha256']
v={'verdict':'ACCEPT_SCOPE_LIMITED','date_utc':'2026-10-18','theorem':'B(F_(53^29))=16 in original N13 free-cross-singleton grammar, arbitrary legal beta and raw weights','field_modulus':'u^29+u+8 over F53','allocation':[7,1,1,7],'candidate_manifest_sha256':b['candidate_manifest_sha256'],'candidate_certificate_sha256':b['candidate_certificate_sha256'],'candidate_report_sha256':b['candidate_report_sha256'],'review_report_sha256':sha(R/'INDEPENDENT_REVIEW.md'),'arithmetic_sha256':sha(R/'ARITHMETIC.json'),'supplemental_sha256':sha(R/'SUPPLEMENTAL.json'),'cold_replay_sha256':sha(R/'COLD_REPLAY.json'),'literal_branch_inverses':208,'left_right_inverse_identities':416,'target_entries':169,'target_mismatches':0,'safe_packed_slot_bits':17,'ordinary_convolution_differentials':942,'radix16_negative_controls':'PASS: carry guard, raw convolution, reduced field product, executable differential rejection','GMP_exponent_controls':'PASS: all paths unbounded; ten powers; six truncation controls; fresh UBSan probe','lower_bound':'Inherited accepted field-uniform theorem; original lower-minor computation not rerun','search_first_hit_independently_reexecuted':False,'transfer':'29 divides d implies equality','sufficient_divisors':[2,3,5,7,11,13,17,19,23,29],'remaining_gcd_modulus':6469693230,'next_residual_degree':31,'scientific_correction_required':False,'external_writes':False,'additional_agents_created':False}
(R/'VERDICT.json').write_text(json.dumps(v,indent=2)+'\n')
files=[]
for p in sorted(R.rglob('*')):
 if p.is_file() and p.name!='MANIFEST.json' and '__pycache__' not in p.parts:
  files.append({'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':sha(p)})
# Nested candidate manifests remain mandatory sealed inputs.
for p in sorted(R.rglob('MANIFEST.json')):
 if p.parent!=R:files.append({'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':sha(p)})
files.sort(key=lambda x:x['path'])
manifest={'schema':'sha256-file-manifest-v1','excludes':['root MANIFEST.json','__pycache__'],'files':files}
(R/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
for f in json.loads((R/'MANIFEST.json').read_text())['files']:
 p=R/f['path'];assert p.stat().st_size==f['bytes'] and sha(p)==f['sha256']
print(json.dumps({'verdict':v['verdict'],'review_directory':str(R),'review_manifest_sha256':sha(R/'MANIFEST.json'),'review_manifest_entries':len(files),'review_report_sha256':v['review_report_sha256'],'arithmetic_sha256':v['arithmetic_sha256'],'verdict_sha256':sha(R/'VERDICT.json')},indent=2))
