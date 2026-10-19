#!/usr/bin/env python3
"""Scientific replay with explicit original-provenance exclusions."""
from pathlib import Path
import hashlib,importlib.util,json,os,subprocess,sys,tempfile
BASE=Path(__file__).resolve().parent

def sha(b):return hashlib.sha256(b).hexdigest()
def load_module(path):
 spec=importlib.util.spec_from_file_location('unchanged_upper_checker',path)
 module=importlib.util.module_from_spec(spec);old=sys.dont_write_bytecode
 sys.dont_write_bytecode=True
 try:spec.loader.exec_module(module)
 finally:sys.dont_write_bytecode=old
 return module

def replay():
 candidate=BASE/'candidate';review=BASE/'review'
 with tempfile.TemporaryDirectory(prefix='upper-scientific-replay-') as temp:
  work=Path(temp);m=load_module(candidate/'verify_upper.py');m.ROOT=work
  positives=[];negatives=[];mixed=[];overlaps=[];partners=[]
  # Exactly the mathematical calls and ordering of original main, excluding
  # the private SOURCE_BINDINGS read and five original provenance checks.
  for q in [7,11,13,17,19,23]:
   F=m.OriginalFourier(q)
   if q in [7,11,13,17]:
    for d in [1,5,q,F.n]:positives.append(m.check_full_mask(F,m.positive_mask(F.n,d),d,True,'divisor_control'))
    for twisted in [False,True]:
     negatives.append(m.check_full_mask(F,m.negative_mask(F,twisted),3*q+2,False,'distinct_affine_maps' if twisted else 'common_fiber_map'))
   if q in [7,11]:
    mixed.append(m.mixed_cycle_controls(F));overlaps.append(m.overlap_controls(F));partners.append(m.partner_controls(q))
  outputs={'POSITIVE_CONTROLS.json':positives,'NEGATIVE_CONTROLS.json':negatives,'MIXED_CYCLE_CONTROLS.json':mixed,'OVERLAP_CERTIFICATES.json':overlaps,'PARTNER_CONTROLS.json':partners}
  comparisons=[]
  for name,value in outputs.items():
   m.write(name,value);b=(work/name).read_bytes();assert b==(candidate/name).read_bytes(),name
   comparisons.append({'file':name,'sha256':sha(b),'byte_identical':True})
  result={'status':'PASS','counts':dict(m.COUNTS),'positive_parameters':[[x['q'],x['degree']] for x in positives],'negative_parameters':[[x['q'],x['degree'],x['label']] for x in negatives],'arithmetic':'Exact integer original-index cyclotomic rational-basis reduction','floating_point_used':False,'external_writes':False,'scope':'Finite corroboration of a symbolic theorem; no exhaustive square-mask search'}
  expected=json.loads((candidate/'RESULTS.json').read_text());assert expected.pop('source_bindings_checked')==5
  assert result==expected
  independent=work/'independent';independent.mkdir()
  (independent/'independent_check.py').write_bytes((review/'independent_check.py').read_bytes())
  run=subprocess.run([sys.executable,str(independent/'independent_check.py')],capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
  assert run.returncode==0,run.stderr.decode()
  checks=[]
  for name,b in [('RESULTS.json',(independent/'RESULTS.json').read_bytes()),('RUN.stdout',run.stdout),('RUN.stderr',run.stderr)]:
   assert b==(review/name).read_bytes(),name
   checks.append({'file':name,'sha256':sha(b),'byte_identical':True})
  return {'status':'PASS','mode':'SCIENTIFIC_REPLAY_WITH_EXPLICIT_PROVENANCE_EXCLUSIONS','candidate_checker_sha256':sha((candidate/'verify_upper.py').read_bytes()),'review_checker_sha256':sha((review/'independent_check.py').read_bytes()),'candidate_scientific_files':comparisons,'candidate_results_all_nonprovenance_fields_identical':True,'candidate_counts':dict(m.COUNTS),'candidate_omitted_result_fields':{'source_bindings_checked':{'original_value':5,'freshly_checked':False}},'candidate_original_main_executed':False,'candidate_skipped_checks':['SOURCE_BINDINGS.json read','Five original dependency byte-length and SHA-256 checks'],'candidate_stdout_replayed':False,'review_original_main_executed':True,'review_complete_output_comparisons':checks,'historical_proof_checkers_replayed':False,'finite_controls_are_not_a_square_mask_census':True,'floating_point_used':False,'external_writes':False}
if __name__=='__main__':print(json.dumps(replay(),indent=2,sort_keys=True))
