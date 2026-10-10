"""Reviewer-authored inert file/data reconciliation; no source imports."""
from pathlib import Path
import json,hashlib,re
P=Path(__file__).resolve().parent;M=Path('fft_research_master_20261009');I=Path('code_coverage_audit_0228/CODE_COVERAGE_INVENTORY.json')
rows=json.loads((P/'SOURCE_MANIFEST.json').read_text());byid={r['review_id']:r for r in rows};inv={r['sha256']:r for r in json.loads(I.read_text())}
hashof=lambda data:hashlib.sha256(data).hexdigest()
meta=[]
for r in rows:
 old=inv[r['sha256']];f=M/r['representative_path'];cache=Path(r['local_content']);snapshot=P/r['snapshot'];content=cache.read_bytes();stat=cache.stat()
 drift={k:{'batch':r.get(k),'frozen_inventory':old.get(k)}for k in ['size_bytes','representative_path','coverage_status','static_inspection_complete','recorded_execution','origin_class','root_archive_sha256s','containing_library_archive_ids']if r.get(k)!=old.get(k)}
 meta.append({'review_id':r['review_id'],'sha256':r['sha256'],'cache_hash':hashof(content),'snapshot_hash':hashof(snapshot.read_bytes()),'master_path':str(f),'master_exists':f.is_file(),'master_hash':hashof(f.read_bytes())if f.is_file()else None,'cache_size_bytes':len(content),'declared_size_bytes':r['size_bytes'],'cache_stat':{'mtime_ns':stat.st_mtime_ns,'mode':stat.st_mode},'batch_vs_frozen_metadata_drift':drift,'provenance_claim':'Occurrence/archive/Library pointers inherited from frozen inventory; no independent Library fetch or authorship verification in this review.'})
assert all(r['cache_hash']==r['snapshot_hash']==r['master_hash']==r['sha256']and r['cache_size_bytes']==r['declared_size_bytes']for r in meta)
(P/'SOURCE_PRESERVATION.json').write_text(json.dumps(meta,indent=2)+'\n')
selected={
'S01':['AUDIT_RESULTS.json','MIXED_RANK_AUDIT.txt','TEST_LOG.txt'],
'S05':['AUDIT_RESULTS.json','TEST_LOG.txt'],
'S08':['INDEPENDENT_RESULTS.json','SOURCE_RESULT_COMPARISON.json'],
'S09':['FIELD_BASIS_RESULTS.json','BENCH_RESULTS.json','PRECISION_RESULTS.json','TEST_RUN.log'],
'S14':['INDEPENDENT_RESULTS.json'],
'S16':['INDEPENDENT_RESULTS.json'],
'S17':['PHASE22_AUDIT.json','PHASE22_BENCHMARK.json'],
'S19':['INDEPENDENT_RESULTS.json','BENCHMARK_DIFFERENCE_CHECKS.json'],
'S20':['PHASE24_AUDIT.json','PHASE24_TESTS.log'],
'S22':['AUDIT_RESULTS.json','SPECTRAL_AUDIT_RESULTS.json','UNIVERSAL_IDENTITY_AUDIT.json','test_phase9.log','test_spectral.log'],
'S30':['AUDIT_RESULTS.json','TEST_LOG.txt'],
'S33':['RESULTS.json'],
'S34':['AUDIT_RESULTS.json','SCHMIDT_AUDIT.json','SCHMIDT_GENERAL_AUDIT.json','test_phase10.log'],
'S40':['RESULTS.json'],
'S42':['INDEPENDENT_RESULTS.json'],
'S43':['INDEPENDENT_RESULTS.json'],
'S44':['SOURCE_CERTIFICATE_COMPARISON.json','SOURCE_COMPARISON.log'],
'S45':['INDEPENDENT_RESULTS.json','INDEPENDENT_RUN.log']}
(P/'stored_evidence').mkdir(exist_ok=True);evidence=[]
for sid,names in selected.items():
 d=(M/byid[sid]['representative_path']).parent
 related=[r['review_id']for r in rows if (M/r['representative_path']).parent==d]
 for name in names:
  f=d/name;raw=f.read_bytes();rel=f'stored_evidence/{sid}__{name}';(P/rel).write_bytes(raw)
  record={'evidence_id':f'E{len(evidence)+1:02}','source_review_ids':related,'origin':str(f),'snapshot':rel,'sha256':hashof(raw),'size_bytes':len(raw),'classification':'Stored report/log claims only. Read as inert data, not rerun or adopted as current execution evidence. Adjacency is not proof of production by this exact source hash.'}
  if f.suffix=='.json':
   j=json.loads(raw);record['json_valid']=True
   if isinstance(j,dict):record['top_level_keys']=list(j)
  elif 'TEST' in name.upper()or name.startswith('test_'):
   t=raw.decode();match=re.search(r'Ran (\d+) tests?',t);record['reported_test_count']=int(match[1])if match else None;record['reports_OK']=bool(re.search(r'^OK\s*$',t,re.M))
  evidence.append(record)
(P/'STORED_EVIDENCE_INDEX.json').write_text(json.dumps(evidence,indent=2)+'\n')
# Data-only consistency summaries, not re-execution of mathematical checks.
report=[]
for e in evidence:
 if e['snapshot'].endswith('.json'):
  j=json.loads((P/e['snapshot']).read_text());s={'evidence_id':e['evidence_id'],'source_ids':e['source_review_ids'],'snapshot':e['snapshot'],'reported_status':j.get('status',j.get('result',j.get('passed',j.get('all_checks_passed'))))}
  for k in ['summary','finite_field_basis_checks','intertwining_matrix_entries','total_field_entries_checked','dense_impulses_verified','full_fresh_random_dfts','large_n','large_selected_bins_independently_checked','coefficients_independently_checked','independent_arbitrary_dft_coefficients_checked','spot_checked_large_output_coefficients','source_nonzero_minor_values_verified','source_multidegrees_verified','independent_rejection_witnesses','all_source_branch_sets_equal_independent_sets','source_haar_inverse_z1_guard','unresolved']:
   if k in j:s[k]=j[k]
  for k in ['rows','records','cases','scaling','branch_certificates','order_records','row_empty_witnesses']:
   if k in j and isinstance(j[k],list):s[k+'_length']=len(j[k])
  report.append(s)
(P/'STORED_EVIDENCE_RECONCILIATION.json').write_text(json.dumps({'boundary':'Source static correctness, stored reported checks, and fresh independent arithmetic are separate evidence levels. None of the stored scripts were executed, imported, compiled, or AST-parsed.','late_class_tests':{'S04':'Saved TEST_LOG lists all 11 tests including 3 later-defined tests; direct-script omission does not invalidate this stored module-discovery-compatible log.','S07':'Saved TEST_LOG lists all 13 tests including 2 later-defined tests; direct-script omission does not invalidate this stored module-discovery-compatible log.'},'reports':report},indent=2)+'\n')
print('preserved',len(meta),'sources and',len(evidence),'stored reports/logs; metadata drift rows',sum(bool(x['batch_vs_frozen_metadata_drift'])for x in meta))
for s in report:print(json.dumps(s)[:700])
