from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parent
receipts=['FIELD_IRREDUCIBILITY.json','ARITHMETIC_CHECK.json','CONVOLUTION_BOUNDARY_CHECK.json','DEGREE31_LITERAL_RESULT.json','INDEPENDENT_LITERAL_RESULT.json','WITNESS_STRUCTURE.json','PREFIX_AUDIT.json','FIRST_HIT_REPLAY.json','MUTATION_CONTROLS.json','COLD_LITERAL_REPLAY.json','SOURCE_BINDING_CHECK.json']
for f in receipts:assert json.loads((R/f).read_text())['verdict']=='PASS',f
certificate=(R/'DEGREE31_LITERAL_CERTIFICATE.json').read_bytes();sha=hashlib.sha256(certificate).hexdigest()
assert sha=='20ff3730c3b42568062d6da7151939c23ffd0abdf1bd6a8d79c1abfb905de5ad'
status={'status':'CANDIDATE_ALL_CHECKS_PASS_AWAITING_SEPARATE_FINAL_REVIEW','degree':31,'field':'F53[u]/(u^31+2u+11)','N':13,'target':'16^(-k*t), negative and unnormalized','allocation':[7,1,1,7],'certificate_sha256':sha,'first_hit_trial':1113,'nonzero_nodes':1114,'nonzero_constant_candidates':1117,'seed':202610192024,'frozen_cap':100000,'all_receipts_pass':receipts,'inherited_lower_bound':True,'new_finite_attainment':True,'general_field_classification':False,'uniform_FFT_claim':False,'novelty_claim':False,'owner_closure':False,'priority_change':False,'external_writes':False}
(R/'STATUS.json').write_text(json.dumps(status,indent=2)+'\n')
exclude={'MANIFEST.json','search_degree31','verify_literal','arithmetic_probe'};rows=[]
for p in sorted(R.rglob('*')):
 if not p.is_file() or p.name in exclude or '__pycache__' in p.parts or p.suffix=='.pyc':continue
 b=p.read_bytes();rows.append({'path':str(p.relative_to(R)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob_sha1':hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()})
(R/'MANIFEST.json').write_text(json.dumps({'files':rows,'excluded':'This manifest, disposable compiled binaries and Python caches. All scientific sources, inert evidence and reports are included.'},indent=2)+'\n')
print(json.dumps({'files':len(rows),'certificate_sha256':sha,'manifest_sha256':hashlib.sha256((R/'MANIFEST.json').read_bytes()).hexdigest(),'report_sha256':hashlib.sha256((R/'REPORT.md').read_bytes()).hexdigest()},indent=2))
