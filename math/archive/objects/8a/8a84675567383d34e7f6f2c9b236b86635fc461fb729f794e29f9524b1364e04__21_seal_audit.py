#!/usr/bin/env python3
"""Independent static provenance and seal creation. No source execution."""
from pathlib import Path
import json,hashlib,ast
b=Path(__file__).resolve().parent.parent;a=b/'audit'
validation=[]
for d in [b/'extracted/delta/hero17_delta_graph',b/'extracted/tensor_copy/hero17_tensor_union']:
 m=json.loads((d/'MANIFEST.json').read_text());records=[];ents=m['files']
 if isinstance(ents,dict):ents=[dict(name=name,**ent) for name,ent in ents.items()]
 for ent in ents:
  name=ent.get('name',ent.get('path'));p=d/name;data=p.read_bytes()
  records.append({'name':name,'bytes_ok':len(data)==ent.get('bytes',len(data)),'sha256_ok':hashlib.sha256(data).hexdigest()==ent['sha256']})
 assert all(v['bytes_ok'] and v['sha256_ok'] for v in records)
 testnames=[]
 for p in d.glob('test_*.py'):
  tr=ast.parse(p.read_text())
  for node in ast.walk(tr):
   if isinstance(node,ast.ClassDef):
    testnames += [p.name+':'+node.name+'.'+f.name for f in node.body if isinstance(f,ast.FunctionDef) and f.name.startswith('test_')]
 validation.append({'directory':str(d.relative_to(b)),'entries':records,'test_method_count':len(testnames),'test_methods':testnames,'execution':'not run'})
(a/'SOURCE_STATIC_VALIDATION.json').write_text(json.dumps(validation,indent=2)+'\n')
source_records=[{'library_file_id':'[private-id]','filename':'fft_hero17_delta_graph_newton_union_2026-10-10.zip','bytes':49735,'sha256':'88a25130e3da7faa44af8511ad2dafb20f5e6ab9b07c74b47f945d4d66daca50','status':'new source; independently audited as text/data','source_location':'originals/fft_hero17_delta_graph_newton_union_2026-10-10.zip'}, {'library_file_id':'[private-id]','filename':'fft_hero17_tensor_fiber_graph_union_2026-10-10 (1).zip','bytes':36422,'sha256':'67e831c40b1f516abb15dd676a1034291b9f9474497717e2a36af0613ba55a26','status':'exact byte duplicate; prior audit inherited, not new execution','source_location':'originals/fft_hero17_tensor_fiber_graph_union_2026-10-10 (1).zip','duplicate_of':{'library_file_id':'[private-id]','filename':'fft_hero17_tensor_fiber_graph_union_2026-10-10.zip','prior_integration':'additions/1954/'}}]
(b/'source_records.json').write_text(json.dumps(source_records,indent=2)+'\n')
ledger={'status':'complete bounded audit','uploaded_code_executed':False,'master_modified':False,'library_written':False,'claims':[
 {'claim':'Fixed-order selected-factor Newton raw-input recognizer and all-output executor','status':'accepted with supplied-field/root, fixed-order/balance/event-budget contract'},
 {'claim':'Greedy budgeted optional-reset recognizer covers every B-anchor representation','status':'refuted by explicit 16-coordinate witness; accepted outputs remain sound'},
 {'claim':'Complete B-anchor event-budget selection','status':'independently proved repair, not applied to supplied code'},
 {'claim':'Default selector covers all eligible divisors and orders','status':'not supported; explicit N=12 witness'},
 {'claim':'Shipped fused dispatcher includes new Delta/Newton or Toeplitz work','status':'false; dispatcher and chirp engine unchanged'},
 {'claim':'Graph first-variation reconstruction','status':'accepted; independently strengthened to fixed higher differences and no M-squared guard'},
 {'claim':'Rank and first-variation output guards are complementary','status':'proved on actual one-mode/two-mode sparse-input convolution families'},
 {'claim':'Exact supported-vector cardinality','status':'strengthened source upper bound to equality for specified Q,M,d with no resets'},
 {'claim':'Arbitrary fresh all-output linear-time DFT or novelty','status':'not established; excluded'}],
 'new_artifacts':['AUDIT_REPORT.md','EXTENSIONS_AND_FUSION.md','independent_checks.py','independent_results.json','independent_run.log','source_comparison.json','SOURCE_STATIC_VALIDATION.json'],
 'inherited_only':'Earlier tensor/fiber and graph audits are read-only antecedents; duplicate source record is retained. No prior code was executed.',
 'safe_integration':'All files in this sealed directory are task artifacts, supplied source bytes or provenance. Integrate proofs as scoped independent extensions; do not claim uploaded implementation repairs.'}
(a/'CLAIM_LEDGER.json').write_text(json.dumps(ledger,indent=2)+'\n')
refs=[Path('materials_1954/tensor_audit/AUDIT_REPORT.md'),Path('materials_1954/tensor_audit/EXTENSION_AND_FUSION.md'),Path('materials_1954/graph_audit/GRAPH_UNION_AUDIT_AND_RANK_FUSION.md'),Path('fft_research_master_20261009/GROWING_RANK_CHIRP_COROLLARY.md')]
(a/'PRIOR_REFERENCE_HASHES.json').write_text(json.dumps([{'reference':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'access':'read only'} for p in refs],indent=2)+'\n')
items=[]
for p in sorted(b.rglob('*')):
 if p.is_file() and p.name not in ['SHA256SUMS','SEALED_MANIFEST.json']:
  items.append({'path':str(p.relative_to(b)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
manifest={'audit_date_utc':'2026-10-09','status':'sealed; all independent checks PASS','file_count':len(items),'files':items,'source_records':'source_records.json','report':'audit/AUDIT_REPORT.md','extension':'audit/EXTENSIONS_AND_FUSION.md','source_execution':'none','master_writes':'none','library_writes':'none'}
(b/'SEALED_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
items.append({'path':'SEALED_MANIFEST.json','sha256':hashlib.sha256((b/'SEALED_MANIFEST.json').read_bytes()).hexdigest()})
(b/'SHA256SUMS').write_text(''.join(f"{i['sha256']}  {i['path']}\n" for i in sorted(items,key=lambda i:i['path'])))
print('Source manifests:',[(x['directory'],len(x['entries']),x['test_method_count']) for x in validation]);print('Sealed',len(items),'files')
