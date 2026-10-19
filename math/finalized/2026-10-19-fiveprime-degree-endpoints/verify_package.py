#!/usr/bin/env python3
"""Exact export integrity/scope check, not an independent theorem prover."""
from pathlib import Path
import hashlib,json
BASE=Path(__file__).resolve().parent
EXPECTED={'source_ledger_sha256': 'e54f05c11938d719b705c95cfa01d457a36314371f94772a797cd784f3512fe8', 'original_manifest_sha256': {'candidate': '74d010baa9add435eae553526c372ca958dc979772bf1c0df624b342c2f9e42c', 'review': 'cfb3d53b2435d1343855c6d0b14ffa70054f8d18324dd7bd5f1e4f345dcfe2ca'}, 'projection_hashes': {'candidate/sources/accepted_middle_VERDICT.json': '8f026ffae9d68cf82e35d225c602aec16be8d726d337d59ee7f19b0b816c5d7c', 'candidate/sources/accepted_upper_VERDICT.json': 'b687b2e4ed48db603cdd9cce785886e6c2201e98ed095dbdca207ad9613230dd', 'review/AUTHOR_PACKET_INTEGRITY.json': 'b00b6bdd6090587df77d784aeaa1ac57838fc5a3414fff1b8cd1b3e0444526ea', 'review/author_rerun/sources/accepted_middle_VERDICT.json': '8f026ffae9d68cf82e35d225c602aec16be8d726d337d59ee7f19b0b816c5d7c', 'review/author_rerun/sources/accepted_upper_VERDICT.json': 'b687b2e4ed48db603cdd9cce785886e6c2201e98ed095dbdca207ad9613230dd', 'review/frozen_author_packet/sources/accepted_middle_VERDICT.json': '8f026ffae9d68cf82e35d225c602aec16be8d726d337d59ee7f19b0b816c5d7c', 'review/frozen_author_packet/sources/accepted_upper_VERDICT.json': 'b687b2e4ed48db603cdd9cce785886e6c2201e98ed095dbdca207ad9613230dd'}, 'omissions': ['candidate/SOURCE_BINDINGS.json', 'review/author_rerun/SOURCE_BINDINGS.json', 'review/frozen_author_packet/SOURCE_BINDINGS.json'], 'source_counts': {'exact_exports': 66, 'frozen_source_items': 76, 'omitted_items': 3, 'projected_exports': 7}, 'candidate_counts': {'arbitrary_five_row_line_set_tuples': 406250, 'canonical_cycle_union_supports': 67394, 'coverage_exception_sets': 90, 'endpoint_degree_equations': 495, 'exact_order5_overlap_cases': 4500, 'full_original_index_Gram_entries': 169500, 'literal_CRT_phase_products': 8475}, 'review_counts': {'canonical_actual_union_supports': 67394, 'canonical_full_support_guards': 2, 'corner_assignments': 34816, 'coverage_counts': 1350, 'fixed_b_exact_pair_sums': 6024, 'full_gram_entries': 169500, 'full_rank_crt_bases': 2, 'one_bit_cancellation_negative_controls': 119820, 'original_index_phase_products': 37950, 'prime_endpoint_arithmetic_cases': 495, 'primitive_root_zero_controls': 86912}}
def sha(b):return hashlib.sha256(b).hexdigest()
def read(name):return json.loads((BASE/name).read_text())
def record(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':sha(b)}
def safe(name):
 p=Path(name);assert not p.is_absolute() and '..' not in p.parts and str(p)==name
 return BASE/p
def verify():
 assert not any(p.is_symlink() for p in BASE.rglob('*'))
 inventory={str(p.relative_to(BASE)) for p in BASE.rglob('*') if p.is_file()}
 m=read('MANIFEST.json');seal=read('SEAL.json')
 assert sha((BASE/'MANIFEST.json').read_bytes())==seal['manifest_sha256']
 names=[x['path'] for x in m['files']]
 assert len(names)==len(set(names))==seal['manifest_entries']
 assert set(names)==inventory-{'MANIFEST.json','SEAL.json'}
 for x in m['files']:assert record(safe(x['path']))=={k:x[k] for k in ['bytes','sha256']},x['path']
 for name in inventory:
  assert not any(x in name.upper() for x in ['NATIVE','CELLDATA','SNAPSHOT','PAYLOAD']),name
  t=(BASE/name).read_text()
  forbidden=['/'+'workspace/','/'+'home/','/'+'tmp/','/'+'Users/','docs'+'.google.com/spreadsheets','file'+':/']
  assert not any(s in t for s in forbidden),name
 ledger=read('SOURCE_LEDGER.json');rows=ledger['files']
 assert sha((BASE/'SOURCE_LEDGER.json').read_bytes())==EXPECTED['source_ledger_sha256']
 assert len(rows)==EXPECTED['source_counts']['frozen_source_items']
 assert len({r['namespace']+'/'+r['source_path'] for r in rows})==len(rows)
 for ns,digest in EXPECTED['original_manifest_sha256'].items():
  assert record(BASE/ns/'MANIFEST.json')['sha256']==digest
  assert (BASE/ns/'SEAL.sha256').read_text().strip()==digest+'  MANIFEST.json'
  original=read(ns+'/MANIFEST.json')['files']
  entries=({p:{'sha256':h} for p,h in original.items()} if isinstance(original,dict) else {x['path']:x for x in original})
  subset={r['source_path']:r for r in rows if r['namespace']==ns}
  assert set(subset)==set(entries)|{'MANIFEST.json','SEAL.sha256'}
  for p,entry in entries.items():
   assert subset[p]['original']['sha256']==entry['sha256']
   if 'bytes' in entry:assert subset[p]['original']['bytes']==entry['bytes']
  for p in ['MANIFEST.json','SEAL.sha256']:assert subset[p]['original']==record(BASE/ns/p)
 omitted=[];projected={};exact=0
 for r in rows:
  key=r['namespace']+'/'+r['source_path'];safe(key)
  if r['mode']=='omitted':
   assert r['export_path'] is None and r['reason'] and not (BASE/key).exists();omitted.append(key)
  else:
   assert r['export_path']==key and record(BASE/key)==r['exported']
   if r['mode']=='exact':assert r['original']==r['exported'];exact+=1
   else:
    assert r['mode']=='administrative_projection' and r['projection']['scientific_fields_changed'] is False
    assert r['projection']['operations'] and all(o['scientific_fields_changed'] is False for o in r['projection']['operations'])
    projected[key]=r['exported']['sha256']
 assert omitted==EXPECTED['omissions'] and projected==EXPECTED['projection_hashes']
 assert exact==EXPECTED['source_counts']['exact_exports']
 omissions=read('OMISSIONS.json');assert omissions['counts']==EXPECTED['source_counts']
 assert omissions['omitted_entries']==[r for r in rows if r['mode']=='omitted']
 assert omissions['administrative_projections']==[r for r in rows if r['mode']=='administrative_projection']
 assert omissions['mathematical_text_values_checkers_and_data_changed'] is False
 assert omissions['original_candidate_main_runnable_in_export'] is False
 accepted=read('FINAL_ACCEPTANCE.json');v=read('review/VERDICT.json');scope=read('CLAIM_SCOPE.json');owner=read('OWNER_DISPOSITIONS.json')
 assert accepted['verdict']==v['verdict']=='PASS' and accepted['proof_repairs_required']==v['proof_repairs_required']==[]
 assert accepted['accepted_statement']==v['accepted_statement']==scope['accepted_statement']
 assert accepted['candidate_original_manifest_sha256']==v['candidate_manifest_sha256']==EXPECTED['original_manifest_sha256']['candidate']
 assert accepted['review_original_manifest_sha256']==EXPECTED['original_manifest_sha256']['review']
 assert accepted['candidate_original_report_sha256']==v['candidate_report_sha256']==record(BASE/'candidate/REPORT.md')['sha256']
 assert accepted['review_original_report_sha256']==record(BASE/'review/REVIEW.md')['sha256']
 verdict_row=next(r for r in rows if r['namespace']=='review' and r['source_path']=='VERDICT.json')
 assert accepted['review_original_verdict_sha256']==verdict_row['original']['sha256']
 assert accepted['review_exported_verdict_sha256']==record(BASE/'review/VERDICT.json')['sha256']
 assert v['candidate_bound_files_verified']==18 and v['original_source_bindings_verified']==4 and v['candidate_rerun_all_bound_files_byte_identical'] is True
 assert scope['excluded_degrees']==owner['newly_accepted_degrees']==['2q','3q','4q']
 assert scope['prime_condition']=='q>5 prime' and scope['arbitrary_row_dependent_supports'] and scope['pure_line_branch_treated']
 for field in ['full_classification_claim','other_degrees_changed','novelty_claim','FFT_improvement_claim']:assert scope[field] is False
 assert scope['historical_novelty']=='UNRESOLVED'
 assert scope['owner']==owner['owner']==v['owner']=='M-SPARSE-DEFECT'
 assert accepted['owner_status']==owner['status']==v['owner_status_unchanged']=='TO RESEARCH'
 assert accepted['priority']==owner['priority']==v['priority_unchanged']==42
 assert owner['native_state_changed'] is False and owner['score_change'] is False
 replay=read('SCIENTIFIC_REPLAY.json');rs=read('REPLAY_SCOPE.json')
 assert replay['status']=='PASS' and replay['candidate_counts']==EXPECTED['candidate_counts']
 assert replay['review_counts']==EXPECTED['review_counts']==v['independent_counts']
 assert replay['candidate_omitted_result_fields']==rs['candidate_omitted_result_fields']=={'counts.frozen_source_hashes':{'original_value':4,'freshly_checked':False}}
 assert replay['candidate_skipped_checks']==rs['candidate_skipped_checks']==['SOURCE_BINDINGS.json read','Four frozen historical-source byte-hash checks']
 assert replay['review_nondeterministic_fields']==rs['review_nondeterministic_fields']==['elapsed_seconds']
 for key in ['candidate_original_stdout_byte_replayed','review_original_stdout_byte_replayed','complete_original_provenance_replayed','historical_proof_checkers_replayed','external_writes']:assert replay[key] is False
 for key in ['candidate_results_and_stdout_match_after_exclusions','candidate_does_not_read_source_path','candidate_original_checker_unchanged','candidate_main_called_with_only_source_controls_skipped','review_original_main_executed','review_original_checker_unchanged','review_results_and_stdout_match_after_exclusions','review_stderr_byte_identical_and_empty']:assert replay[key] is True
 for key,ns in [('candidate_scientific_file_comparisons','candidate'),('review_scientific_file_comparisons','review')]:
  assert len(replay[key])==5
  for r in replay[key]:assert r['byte_identical'] and r['sha256']==record(BASE/ns/r['file'])['sha256']
 assert replay['candidate_checker_sha256']==record(BASE/'candidate/verify_endpoints.py')['sha256']
 assert replay['review_checker_sha256']==record(BASE/'review/check_endpoints_independently.py')['sha256']
 status=read('PUBLICATION_STATUS.json');assert status['state']=='LOCAL_STAGE_ONLY' and status['published'] is False and status['external_writes'] is False
 if (BASE/'PACKAGE_CONTROLS.json').exists():
  c=read('PACKAGE_CONTROLS.json');assert c['status']=='PASS' and c['positive_package_check_passed']
  assert len(c['negative_controls'])==10 and all(x['rejected'] for x in c['negative_controls'])
 return {'status':'PASS','manifest_entries':len(names),**EXPECTED['source_counts'],'owner':'M-SPARSE-DEFECT','priority':42,'external_writes':False}
if __name__=='__main__':print(json.dumps(verify(),indent=2,sort_keys=True))
