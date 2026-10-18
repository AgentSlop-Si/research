#!/usr/bin/env python3
"""Seal final source/evidence bytes, excluding disposable executables and caches."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parent
for n in ['ARITHMETIC_CHECK.json','CONVOLUTION_BOUNDARY_CHECK.json','DEGREE29_LITERAL_RESULT.json','INDEPENDENT_LITERAL_RESULT.json','SOURCE_REBUILD_CHECK.json','WITNESS_STRUCTURE.json','COLD_REPLAY.json']:
 assert json.loads((R/n).read_text())['verdict']=='PASS',n
v=json.loads((R/'NONSTABLE_CANDIDATE.json').read_text())
status={'status':'CANDIDATE_COMPLETE_PENDING_EXTERNAL_INDEPENDENT_REVIEW','date_utc':'2026-10-18','theorem':'B(F_(53^29))=16 in original N13 free-cross-singleton grammar with arbitrary legal beta and raw weights','allocation':[7,1,1,7],'field_modulus':'u^29+u+8 over F53','field_order_bits':167,'target':'negative unnormalized Fourier F[k,t]=16^(-kt)','construction_checks':'PASS: C++ Gauss-Jordan and separate ordinary-convolution Python backward recurrence','field_proof':'PASS: twenty-nine Frobenius remainders and degree-prime gcd criterion','packed_boundary_resolution':'ordinary-convolution literal checker; independent radix17 differential audit and radix16 corruption controls before discovery','exponent_boundary_resolution':'unbounded GMP mpz_class; ten power checks and six truncation controls','cold_replay':'PASS: fresh rebuild, two Python literal checks, UBSan, exact failed prefix and first hit','first_split_trial':v['trial'],'recurrence_candidates':v['candidates'],'transfer':'29 divides d implies B(F_(53^d))=16','sufficient_divisors':[2,3,5,7,11,13,17,19,23,29],'residual_coverage_gcd_modulus':6469693230,'next_residual_degree':31,'lower_bound':'inherited accepted field-uniform theorem, not recomputed','certificate_sha256':hashlib.sha256((R/'DEGREE29_LITERAL_CERTIFICATE.json').read_bytes()).hexdigest(),'external_writes':False,'extra_agents_created':False,'no_finite_extrapolation':True}
(R/'STATUS.json').write_text(json.dumps(status,indent=2)+'\n')
exclude={'MANIFEST.json','arithmetic_probe','verify_literal','search_degree29'}
files=[]
for p in sorted(R.rglob('*')):
 if not p.is_file() or p.name in exclude or '__pycache__' in p.parts:continue
 b=p.read_bytes();files.append({'path':str(p.relative_to(R)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
manifest={'schema':'sha256-file-manifest-v1','excludes':['MANIFEST.json','disposable compiled binaries','__pycache__'],'files':files}
(R/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'verdict':'SEALED','files':len(files),'manifest_sha256':hashlib.sha256((R/'MANIFEST.json').read_bytes()).hexdigest(),'certificate_sha256':status['certificate_sha256']},indent=2))
