"""Review-owned final deduplication, preservation, and package sealing; no supplied code execution."""
from pathlib import Path
import json,hashlib
O=Path(__file__).resolve().parent; S=Path('[local workspace]')
def sha(raw):return hashlib.sha256(raw).hexdigest()
def read(p):return json.loads(p.read_bytes())
sources=read(O/'SOURCE_INDEX.json');targets={r['row']['sha256'] for r in sources}
initial=read(O/'DEDUP_SCAN.json');scan=[];hits=[]
paths=[S/'post_v22_review_registry_0308/ADDITIVE_CODE_COVERAGE.json']+sorted(S.rglob('COVERAGE.json'))
for p in paths:
 if O in p.parents:continue
 raw=p.read_bytes();d=json.loads(raw);scan.append({'path':str(p),'sha256':sha(raw),'bytes':len(raw)})
 for h in targets:
  if h.encode() in raw:hits.append({'path':str(p),'sha256':h,'note':'Conservative full-string match; requires manual scope classification before credit.'})
inv=read(O/'input_manifests/CODE_COVERAGE_INVENTORY.json');ix={r['sha256']:r for r in inv}
assert not hits,hits
assert all(not ix[h]['static_inspection_complete'] for h in targets)
initial['final_scan_manifests']=scan;initial['final_scan_raw_hash_matches']=hits;initial['dedup_method']='Exact SHA-256 only; frozen per-row static_inspection_complete plus additive/completed coverage objects and conservative raw hash string scan. No basename, AST similarity, or execution-log substitution.';initial['assigned_prior_covered_count']=0;initial['assigned_new_coverage_credit_count']=7
(O/'DEDUP_SCAN.json').write_text(json.dumps(initial,indent=2)+'\n')
findings={1:['F03'],2:['F03','F04'],3:['F02'],4:['F05'],5:['F05'],6:['F06'],7:['F01','F07']}
rows=[]
for s in sources:
 r=s['row'];i=s['index'];name=Path(r['representative_path']).name
 snapshot=O/s['snapshot'];assert sha(snapshot.read_bytes())==r['sha256']
 review=f'per_source/{i:02d}_{name}.md';assert (O/review).exists()
 rows.append({'sha256':r['sha256'],'name':name,'representative_path':r['representative_path'],'assigned_batch':s['batch'],'bytes':r['size_bytes'],'lines':s['lines'],'fully_read_line_intervals':[[1,s['lines']]],'full_static_inspection':True,'static_inspection_complete':True,'source_executed':False,'source_executed_in_review':False,'source_imported':False,'source_compiled':False,'source_parsed':False,'inspection_method':'Complete inert first-to-last source read plus correctness, guards, complexity, dependencies, and saved evidence-impact review.','new_coverage_credit':True,'prior_full_coverage_package':None,'snapshot':s['snapshot'],'review_file':review,'finding_ids':findings[i]})
coverage={'assigned_batches':[p.name for p in sorted((O/'input_manifests').glob('02_*.json'))],'assigned_batch_hashes':7,'fully_read_hashes_this_review':7,'new_full_read_hashes':7,'new_coverage_credit_count':7,'previously_covered_hashes':0,'total_source_bytes_read':sum(r['bytes'] for r in rows),'total_source_lines_read':sum(r['lines'] for r in rows),'all_assigned_source_reads_complete':True,'all_research_material_checks_finished':False,'dependency_closure_complete':False,'source_execution':'none','central_registry_modified':False,'scope_note':'Seven assigned exact hashes only. Contextual dependencies receive no extra credit. Static review and stored-artifact consistency do not imply test execution, dependency closure, unrestricted theorem acceptance, or global completion.','rows':rows}
(O/'COVERAGE.json').write_text(json.dumps(coverage,indent=2)+'\n')
rec=read(O/'PRESERVATION_RECEIPT.json')
for r in rec['inputs']:
 current=Path(r['path']).read_bytes();r['sha256_after']=sha(current);r['preserved']=r['sha256_after']==r['sha256_before']
 if not r['preserved']:
  assert r['path']==str(S/'post_v22_review_registry_0308/ADDITIVE_CODE_COVERAGE.json'),r['path']
  r['change_classification']='Concurrent registry update by another task; this review did not write the registry.'
  (O/'input_manifests/ADDITIVE_CODE_COVERAGE_FINAL.json').write_bytes(current)
rec.update({'final_verification_complete':True,'all_recorded_inputs_byte_identical':all(r['preserved'] for r in rec['inputs']),'all_assigned_source_and_batch_inputs_byte_identical':True,'concurrent_registry_drift_recorded':any(not r['preserved'] for r in rec['inputs']),'originals_modified':False,'central_registry_modified':False,'supplied_source_executed':False,'supplied_source_imported':False,'supplied_source_compiled':False,'supplied_source_syntax_parsed':False,'review_owned_helpers_executed':['build_review_metadata.py','write_reports.py','finalize_review.py'],'scope':'Recorded inputs were read/hash-checked and copied as inert bytes. ZIP members were read with standard-library zipfile; no archive program was loaded or executed.'})
(O/'PRESERVATION_RECEIPT.json').write_text(json.dumps(rec,indent=2)+'\n')
files=[p for p in sorted(O.rglob('*')) if p.is_file() and p.name not in ['SHA256SUMS.txt']]
(O/'SHA256SUMS.txt').write_text(''.join(f'{sha(p.read_bytes())}  {p.relative_to(O)}\n' for p in files))
print(json.dumps({'files_sealed':len(files),'sources':len(rows),'new_credit':7,'bytes':coverage['total_source_bytes_read'],'lines':coverage['total_source_lines_read'],'final_dedup_manifests':len(scan),'inputs_preserved':len(rec['inputs']),'assigned_source_and_batch_inputs_unchanged':True,'concurrent_registry_drift':any(not r['preserved'] for r in rec['inputs'])},indent=2))
