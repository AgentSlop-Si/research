#!/usr/bin/env python3
"""Verify public export integrity and explicit scope; not a theorem prover."""
from pathlib import Path
import hashlib,json,re
BASE=Path(__file__).resolve().parent
EXPECTED_MANIFESTS={'candidate':'bea917d6ee709f4c7ad1265dff18c4caa10a76776b4934ebb8fb2c3ddaacaa27','review':'2ce99963551a6d1f4f8ad8ff43655c01c2db34039c13f1d7ea5f98a44cb99009'}
EXPECTED_COUNTS={'crt_pairs':37950,'degree_values':16,'full_gram_entries':157000,'partner_selections':15368,'primitive_overlap_cases':486720,'union_support_cases':34784}
EXPECTED_PROJECTIONS={'candidate/sources/accepted_quantitative_gap_REPORT.md': '5769020df6dcf5c8d714f8da9b0cbadb62f2cffa68a9edd51fc8925bf4e0315d', 'review/VERDICT.json': '8f026ffae9d68cf82e35d225c602aec16be8d726d337d59ee7f19b0b816c5d7c', 'review/candidate_rerun/sources/accepted_quantitative_gap_REPORT.md': '5769020df6dcf5c8d714f8da9b0cbadb62f2cffa68a9edd51fc8925bf4e0315d'}
EXPECTED_OMISSIONS={'candidate/SOURCE_BINDINGS.json','candidate/sources/accepted_first_interior_VERDICT.json','candidate/sources/accepted_q7_boundary_VERDICT.json','review/candidate_rerun/SOURCE_BINDINGS.json','review/candidate_rerun/sources/accepted_first_interior_VERDICT.json','review/candidate_rerun/sources/accepted_q7_boundary_VERDICT.json'}

def sha(b):return hashlib.sha256(b).hexdigest()
def read(name):return json.loads((BASE/name).read_text())
def record(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':sha(b)}
def safe(path):
 p=Path(path);assert not p.is_absolute() and '..' not in p.parts and str(p)==path;return BASE/p

def verify():
 allpaths={str(p.relative_to(BASE)) for p in BASE.rglob('*') if p.is_file()}
 assert not any(p.is_symlink() for p in BASE.rglob('*')),'No symlinks permitted'
 m=read('MANIFEST.json');seal=read('SEAL.json')
 assert sha((BASE/'MANIFEST.json').read_bytes())==seal['manifest_sha256']
 names=[r['path'] for r in m['files']];assert len(names)==len(set(names))==seal['manifest_entries']
 assert set(names)==allpaths-{'MANIFEST.json','SEAL.json'},'Public inventory must be exact'
 for r in m['files']:assert record(safe(r['path']))=={k:r[k] for k in ['bytes','sha256']},r['path']
 for key,path in [('final_acceptance_sha256','FINAL_ACCEPTANCE.json'),('source_ledger_sha256','SOURCE_LEDGER.json')]:assert sha((BASE/path).read_bytes())==seal[key]
 # Build disallowed machine-location signatures without embedding those locations.
 forbidden=['/'+'workspace/','/'+'Users/','/'+'home/','/'+'tmp/','/'+'mnt/','docs'+'.google.com/spreadsheets','file'+':/']
 for rel in allpaths:
  data=(BASE/rel).read_text()
  assert not any(x in data for x in forbidden),'Private locator in '+rel
  assert not re.search(r'[A-Za-z]:\\\\(?:Users|Temp)\\\\',data),'Machine locator in '+rel
 ledger=read('SOURCE_LEDGER.json');rows=ledger['files'];assert len(rows)==50
 keys=[r['namespace']+'/'+r['source_path'] for r in rows];assert len(set(keys))==50
 assert set(r['namespace'] for r in rows)==set(EXPECTED_MANIFESTS)
 original_manifests={}
 for ns,digest in EXPECTED_MANIFESTS.items():
  assert sha((BASE/ns/'MANIFEST.json').read_bytes())==digest
  assert (BASE/ns/'SEAL.sha256').read_text()==digest+'  MANIFEST.json\n'
  sm=read(ns+'/MANIFEST.json');original_manifests[ns]=sm
  subset={r['source_path']:r for r in rows if r['namespace']==ns}
  assert set(subset)=={r['path'] for r in sm['files']}|{'MANIFEST.json','SEAL.sha256'}
  for original in sm['files']:
   assert subset[original['path']]['original']=={k:original[k] for k in ['bytes','sha256']}
  for name in ['MANIFEST.json','SEAL.sha256']:assert subset[name]['original']==record(BASE/ns/name)
  packet=next(x for x in ledger['packets'] if x['namespace']==ns)
  assert packet['original_manifest']==record(BASE/ns/'MANIFEST.json')
  assert packet['original_manifest_entries']==len(sm['files']) and packet['inventory_entries']==len(subset)
 omission_keys=set();projection_keys=set()
 for row in rows:
  source_key=row['namespace']+'/'+row['source_path'];safe(source_key)
  mode=row['mode'];assert mode in ['exact','omitted','administrative_projection']
  if mode=='omitted':
   assert row['export_path'] is None and row['reason'] and not (BASE/source_key).exists();omission_keys.add(source_key)
  else:
   assert row['export_path']==source_key
   assert record(BASE/source_key)==row['exported']
   if mode=='exact':assert row['exported']==row['original']
   else:
    assert row['projection']['scientific_fields_changed'] is False
    assert row['exported']['sha256']==EXPECTED_PROJECTIONS[source_key]
    projection_keys.add(source_key)
 assert omission_keys==EXPECTED_OMISSIONS
 assert projection_keys==set(EXPECTED_PROJECTIONS)
 omissions=read('OMISSIONS.json')
 assert omissions['counts']=={'frozen_source_items':50,'exact_exports':41,'projected_exports':3,'omitted_items':6}
 assert omissions['omitted_entries']==[r for r in rows if r['mode']=='omitted']
 assert omissions['administrative_projections']==[r for r in rows if r['mode']=='administrative_projection']
 assert omissions['core_middle_interval_proof_review_checkers_and_data_omitted'] is False
 assert omissions['historical_dependency_material_omitted'] is True
 accepted=read('FINAL_ACCEPTANCE.json');v=read('review/VERDICT.json')
 assert accepted['verdict']==v['verdict']=='PASS' and 'candidate_directory' not in v
 assert accepted['candidate_original_manifest_sha256']==EXPECTED_MANIFESTS['candidate']==v['candidate_manifest_sha256']
 assert accepted['review_original_manifest_sha256']==EXPECTED_MANIFESTS['review']
 assert accepted['candidate_original_report_sha256']==record(BASE/'candidate/REPORT.md')['sha256']==v['candidate_report_sha256']
 assert accepted['review_original_report_sha256']==record(BASE/'review/REVIEW.md')['sha256']
 assert accepted['review_original_verdict_sha256']==next(r for r in rows if r['namespace']=='review' and r['source_path']=='VERDICT.json')['original']['sha256']
 assert accepted['review_exported_verdict_sha256']==record(BASE/'review/VERDICT.json')['sha256']
 assert accepted['scope']==v['scope']=='For every prime q>5, N=5q, binary R, and D[r,c]=R[r,c]*zeta_N**(r*c), no D*D=dI or DD*=dI exists at integer 2q<d<3q.'
 assert v['proof_repairs_required']==[] and v['candidate_manifest_files_verified']==20 and v['source_copy_bindings_verified']==7
 assert v['independent_exact_primitive_overlap_checks']==618500 and v['independent_crt_phase_checks']==8475 and v['independent_positive_full_gram_entries']==16950
 assert accepted['owner_status']==v['owner_status_unchanged']=='TO RESEARCH' and accepted['priority']==v['priority_unchanged']==42
 scope=read('CLAIM_SCOPE.json');owner=read('OWNER_DISPOSITIONS.json')
 assert scope['owner']==owner['owner']==v['owner']=='M-SPARSE-DEFECT'
 assert scope['new_claim']=='No binary original fixed-Fourier equality mask exists for N=5q, prime q>5, integer 2q<d<3q.'
 assert scope['new_interval']=='2q<d<3q' and scope['prime_condition']=='q>5 prime'
 assert scope['outside_scope']==v['outside_scope']
 assert scope['finite_controls_are_not_a_square_mask_census'] is True
 assert scope['novelty_claim'] is False and scope['FFT_improvement_claim'] is False
 assert scope['inherited_consequences']==['Delta_(5q,5q-d)>sqrt(d/(5q))','Delta_(5q,5q-d)^2 >= d/(5q)+1/[50*q*d**(4*q-5)]']
 assert owner['status']=='TO RESEARCH' and owner['priority']==42 and owner['native_state_changed'] is False
 replay=read('SCIENTIFIC_REPLAY.json')
 assert replay['status']=='PASS' and replay['candidate_counts']==EXPECTED_COUNTS
 assert replay['candidate_original_main_executed'] is False and replay['review_original_main_executed'] is True
 assert replay['candidate_results_all_nonprovenance_fields_identical'] is True
 assert replay['candidate_omitted_result_fields']=={'source_bindings_checked':{'original_value':7,'freshly_checked':False}}
 assert replay['candidate_skipped_checks']==['SOURCE_BINDINGS.json read','Seven original dependency byte-length and SHA-256 checks']
 assert replay['candidate_stdout_replayed'] is False and replay['historical_proof_checkers_replayed'] is False
 assert replay['floating_point_used'] is False and replay['external_writes'] is False
 for key,prefix,script in [('candidate_checker_sha256','candidate','verify_middle.py'),('review_checker_sha256','review','independent_check.py')]:assert replay[key]==record(BASE/prefix/script)['sha256']
 assert len(replay['candidate_scientific_files'])==4 and len(replay['review_complete_output_comparisons'])==3
 for key,ns in [('candidate_scientific_files','candidate'),('review_complete_output_comparisons','review')]:
  for r in replay[key]:assert r['byte_identical'] is True and r['sha256']==record(BASE/ns/r['file'])['sha256']
 if (BASE/'PACKAGE_CONTROLS.json').exists():
  controls=read('PACKAGE_CONTROLS.json');assert controls['status']=='PASS' and controls['positive_package_check_passed'] is True
  assert len(controls['negative_controls'])==10 and all(x['rejected'] for x in controls['negative_controls'])
 status=read('PUBLICATION_STATUS.json');assert status['state']=='LOCAL_STAGE_ONLY' and status['external_writes'] is False and status['published'] is False
 return {'status':'PASS','public_manifest_entries':len(names),'frozen_source_items':50,'exact_exports':41,'projected_exports':3,'omitted_items':6,'historical_omitted_entries_verified_in_public':False,'owner':'M-SPARSE-DEFECT','priority':42,'external_writes':False}
if __name__=='__main__':print(json.dumps(verify(),indent=2,sort_keys=True))
