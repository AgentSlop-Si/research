#!/usr/bin/env python3
"""Export integrity and scope validation, not an independent theorem prover."""
from pathlib import Path
import hashlib,json,re
BASE=Path(__file__).resolve().parent
EXPECTED_MANIFESTS={'candidate':'07099cb8e9a7feb83c206e4d74a9c382bfed04ef0dd3389c75fd0942235cee27','review':'9f2519b25f72c653fc88180a8c80713d729a2809419e92675a7c1674130da048'}
EXPECTED_PROJECTIONS={'candidate/DEVELOPMENT_NOTES.md': '51f16a484421de0af7762e47a04e8d81cce8a12d8d6f37a395774fcf712a1596', 'candidate/sources/accepted_middle_VERDICT.json': '8f026ffae9d68cf82e35d225c602aec16be8d726d337d59ee7f19b0b816c5d7c', 'review/SOURCE_COPY_CHECK.json': 'c6df55509aa8afe84f431616fa53cd113997b619ae2d5a8122a1a3b811d99f7d', 'review/VERDICT.json': 'b687b2e4ed48db603cdd9cce785886e6c2201e98ed095dbdca207ad9613230dd', 'review/candidate_rerun/DEVELOPMENT_NOTES.md': '51f16a484421de0af7762e47a04e8d81cce8a12d8d6f37a395774fcf712a1596', 'review/candidate_rerun/sources/accepted_middle_VERDICT.json': '8f026ffae9d68cf82e35d225c602aec16be8d726d337d59ee7f19b0b816c5d7c'}
EXPECTED_OMISSIONS=set(['candidate/SOURCE_BINDINGS.json', 'review/candidate_rerun/SOURCE_BINDINGS.json'])
EXPECTED_COUNTS={'canonical_mixed_cycle_supports':56524,'coverage_exceptional_row_counts':90,'full_Gram_entries':188400,'interval_degree_reductions':16,'mixed_fiber_packing_obstructions':16,'original_CRT_phase_products':37950,'partner_selection_checks':260270,'primitive_overlap_checks':601600,'same_group_balance_checks':135200}
def sha(b):return hashlib.sha256(b).hexdigest()
def read(name):return json.loads((BASE/name).read_text())
def rec(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':sha(b)}
def safe(rel):
 p=Path(rel);assert not p.is_absolute() and '..' not in p.parts and str(p)==rel
 return BASE/p

def verify():
 assert not any(p.is_symlink() for p in BASE.rglob('*'))
 inventory={str(p.relative_to(BASE)) for p in BASE.rglob('*') if p.is_file()}
 m=read('MANIFEST.json');seal=read('SEAL.json')
 assert sha((BASE/'MANIFEST.json').read_bytes())==seal['manifest_sha256']
 names=[x['path'] for x in m['files']]
 assert len(names)==len(set(names))==seal['manifest_entries']
 assert set(names)==inventory-{'MANIFEST.json','SEAL.json'}
 for row in m['files']:assert rec(safe(row['path']))=={k:row[k] for k in ['bytes','sha256']},row['path']
 for key,name in [('final_acceptance_sha256','FINAL_ACCEPTANCE.json'),('source_ledger_sha256','SOURCE_LEDGER.json')]:
  assert seal[key]==rec(BASE/name)['sha256']
 forbidden=['/'+'workspace/','/'+'tmp/','/'+'home/','/'+'Users/','/'+'mnt/','docs'+'.google.com/spreadsheets','file'+':/']
 for rel in inventory:
  t=(BASE/rel).read_text();assert not any(x in t for x in forbidden),rel
 ledger=read('SOURCE_LEDGER.json');rows=ledger['files']
 assert len(rows)==57 and len({r['namespace']+'/'+r['source_path'] for r in rows})==57
 for ns,digest in EXPECTED_MANIFESTS.items():
  assert rec(BASE/ns/'MANIFEST.json')['sha256']==digest
  assert (BASE/ns/'SEAL.sha256').read_text()==digest+'  MANIFEST.json\n'
  original=read(ns+'/MANIFEST.json');subset={r['source_path']:r for r in rows if r['namespace']==ns}
  assert set(subset)=={r['path'] for r in original['files']}|{'MANIFEST.json','SEAL.sha256'}
  for r in original['files']:assert subset[r['path']]['original']=={k:r[k] for k in ['bytes','sha256']}
  for rel in ['MANIFEST.json','SEAL.sha256']:assert subset[rel]['original']==rec(BASE/ns/rel)
  packet=next(p for p in ledger['packets'] if p['namespace']==ns)
  assert packet['original_manifest']==rec(BASE/ns/'MANIFEST.json')
  assert packet['manifest_entries']==len(original['files']) and packet['inventory_entries']==len(subset)
 seen_omissions=set();seen_projections=set();exact=0
 for r in rows:
  key=r['namespace']+'/'+r['source_path'];safe(key)
  if r['mode']=='omitted':
   assert r['export_path'] is None and r['reason'] and not (BASE/key).exists();seen_omissions.add(key)
  else:
   assert r['export_path']==key and rec(BASE/key)==r['exported']
   if r['mode']=='exact':assert r['original']==r['exported'];exact+=1
   else:
    assert r['mode']=='administrative_projection' and r['projection']['scientific_fields_changed'] is False
    assert r['exported']['sha256']==EXPECTED_PROJECTIONS[key];seen_projections.add(key)
 assert exact==49 and seen_omissions==EXPECTED_OMISSIONS and seen_projections==set(EXPECTED_PROJECTIONS)
 omissions=read('OMISSIONS.json')
 assert omissions['counts']=={'frozen_source_items':57,'exact_exports':49,'projected_exports':6,'omitted_items':2}
 assert omissions['omitted_entries']==[r for r in rows if r['mode']=='omitted']
 assert omissions['administrative_projections']==[r for r in rows if r['mode']=='administrative_projection']
 assert omissions['mathematical_text_values_checkers_and_data_changed'] is False
 accepted=read('FINAL_ACCEPTANCE.json');v=read('review/VERDICT.json');scope=read('CLAIM_SCOPE.json');owner=read('OWNER_DISPOSITIONS.json')
 assert accepted['verdict']==v['verdict']=='PASS' and v['proof_repairs_required']==[]
 assert 'candidate_path' not in v
 assert accepted['candidate_original_manifest_sha256']==v['candidate_manifest_sha256']==EXPECTED_MANIFESTS['candidate']
 assert accepted['review_original_manifest_sha256']==EXPECTED_MANIFESTS['review']
 assert accepted['candidate_original_report_sha256']==v['candidate_report_sha256']==rec(BASE/'candidate/REPORT.md')['sha256']
 assert accepted['review_original_report_sha256']==rec(BASE/'review/REVIEW.md')['sha256']
 assert accepted['review_original_verdict_sha256']==next(r for r in rows if r['namespace']=='review' and r['source_path']=='VERDICT.json')['original']['sha256']
 assert accepted['review_exported_verdict_sha256']==rec(BASE/'review/VERDICT.json')['sha256']
 assert accepted['accepted_statement']==v['accepted_statement']
 assert v['candidate_bound_files_verified']==19 and v['candidate_bound_bytes_verified']==131877 and v['original_source_copies_verified']==5
 assert v['candidate_rerun_byte_identical'] is True
 assert v['independent_checks']=={'crt_phase_products':8475,'primitive_overlaps':618500,'partner_selections':41732,'positive_full_gram_entries':67800,'negative_full_gram_entries':16950,'q_values':[7,11,13]}
 assert scope['owner']==owner['owner']==v['owner']=='M-SPARSE-DEFECT'
 assert scope['new_claim']=='No binary original fixed-Fourier equality mask exists for N=5q, prime q>5, integer 3q<d<4q.'
 assert scope['new_interval']=='3q<d<4q' and scope['prime_condition']=='q>5 prime'
 for field in ['endpoint_claim','full_classification_claim','novelty_claim','FFT_improvement_claim']:assert scope[field] is False
 assert scope['historical_novelty']=='UNRESOLVED' and scope['finite_controls_are_not_a_square_mask_census'] is True
 assert accepted['owner_status']==owner['status']==v['owner_status']=='TO RESEARCH'
 assert accepted['priority']==owner['priority']==v['priority']==42
 assert owner['score_change'] is False and owner['native_state_changed'] is False
 replay=read('SCIENTIFIC_REPLAY.json');rs=read('REPLAY_SCOPE.json')
 assert replay['status']=='PASS' and replay['candidate_counts']==EXPECTED_COUNTS
 assert replay['candidate_original_main_executed'] is False and replay['review_original_main_executed'] is True
 assert replay['candidate_results_all_nonprovenance_fields_identical'] is True
 assert replay['candidate_omitted_result_fields']==rs['candidate_omitted_result_fields']=={'source_bindings_checked':{'original_value':5,'freshly_checked':False}}
 assert replay['candidate_skipped_checks']==rs['skipped_candidate_checks']==['SOURCE_BINDINGS.json read','Five original dependency byte-length and SHA-256 checks']
 for key in ['candidate_stdout_replayed','historical_proof_checkers_replayed','floating_point_used','external_writes']:assert replay[key] is False
 for key,rel in [('candidate_checker_sha256','candidate/verify_upper.py'),('review_checker_sha256','review/independent_check.py')]:assert replay[key]==rec(BASE/rel)['sha256']
 assert len(replay['candidate_scientific_files'])==5 and len(replay['review_complete_output_comparisons'])==3
 for key,ns in [('candidate_scientific_files','candidate'),('review_complete_output_comparisons','review')]:
  for r in replay[key]:assert r['byte_identical'] is True and r['sha256']==rec(BASE/ns/r['file'])['sha256']
 if (BASE/'PACKAGE_CONTROLS.json').exists():
  c=read('PACKAGE_CONTROLS.json');assert c['status']=='PASS' and c['positive_package_check_passed'] is True
  assert len(c['negative_controls'])==10 and all(x['rejected'] for x in c['negative_controls'])
 status=read('PUBLICATION_STATUS.json');assert status['state']=='LOCAL_STAGE_ONLY' and status['published'] is False and status['external_writes'] is False
 return {'status':'PASS','public_manifest_entries':len(names),'frozen_source_items':57,'exact_exports':49,'projected_exports':6,'omitted_items':2,'historical_omitted_entries_verified_in_public':False,'owner':'M-SPARSE-DEFECT','priority':42,'external_writes':False}
if __name__=='__main__':print(json.dumps(verify(),indent=2,sort_keys=True))
