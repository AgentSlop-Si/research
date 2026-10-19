#!/usr/bin/env python3
"""Fresh scientific replay; all skipped provenance checks are explicitly reported."""
from pathlib import Path
import contextlib,hashlib,importlib.util,io,json,os,subprocess,sys,tempfile
BASE=Path(__file__).resolve().parent

def sha(b):return hashlib.sha256(b).hexdigest()
def module_from(path,name):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec)
 old=sys.dont_write_bytecode;sys.dont_write_bytecode=True
 try:spec.loader.exec_module(m)
 finally:sys.dont_write_bytecode=old
 return m

def replay():
 candidate=BASE/'candidate';review=BASE/'review'
 with tempfile.TemporaryDirectory(prefix='fiveq-scientific-replay-') as temp:
  work=Path(temp);m=module_from(candidate/'verify_middle.py','original_candidate')
  m.ROOT=work
  positives,negatives,reductions,sweeps=[],[],[],[]
  # Same mathematical calls and loop parameters as the unchanged original main.
  # Its SOURCE_BINDINGS read and seven hash checks are deliberately not executed.
  for q in [7,11,13,17,19,23]:
   n,e5,eq,index=m.crt_data(q)
   if q in [7,11,13,17]:
    for degree in [1,5,q,n]:positives.append(m.gram_check(m.divisor_mask(n,degree),q,degree,True))
    negative=m.gram_check(m.near_mask(q,index),q,2*q+3,False)
    if q==7:negative['literal_original_index_rows']=[format(row,f'0{n}b')[::-1] for row in m.near_mask(q,index)]
    negatives.append(negative)
   if q in [7,11]:
    sweeps.append(m.primitive_sweep(q,index));reductions.append(m.reduction_controls(q,index))
  outputs={'POSITIVE_CONTROLS.json':positives,'NEGATIVE_CONTROLS.json':negatives,'PRIMITIVE_OVERLAP_CERTIFICATES.json':sweeps,'REDUCTION_CONTROLS.json':reductions}
  comparisons=[]
  for name,obj in outputs.items():
   m.save(name,obj);b=(work/name).read_bytes();assert b==(candidate/name).read_bytes(),name
   comparisons.append({'file':name,'sha256':sha(b),'byte_identical':True})
  result={'status':'PASS','counts':m.COUNTS,'positive_mask_parameters':[[x['N'],x['degree']] for x in positives],'negative_mask_parameters':[[x['N'],x['degree']] for x in negatives],'arithmetic':'Exact integer reduction in the original cyclotomic rational basis','scope':'Symbolic theorem supplemented by exact finite controls; no square-mask census','external_writes':False,'floating_point_used':False}
  expected=json.loads((candidate/'RESULTS.json').read_text());assert expected.pop('source_bindings_checked')==7
  assert result==expected,'Every non-provenance candidate result field must agree'
  independent=work/'independent';independent.mkdir();(independent/'independent_check.py').write_bytes((review/'independent_check.py').read_bytes())
  env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
  run=subprocess.run([sys.executable,str(independent/'independent_check.py')],capture_output=True,env=env)
  assert run.returncode==0,run.stderr.decode()
  checks=[]
  for name,b in [('RESULTS.json',(independent/'RESULTS.json').read_bytes()),('RUN.stdout',run.stdout),('RUN.stderr',run.stderr)]:
   assert b==(review/name).read_bytes(),name;checks.append({'file':name,'sha256':sha(b),'byte_identical':True})
  out={'status':'PASS','mode':'SCIENTIFIC_REPLAY_WITH_EXPLICIT_PROVENANCE_EXCLUSIONS','candidate_checker_sha256':sha((candidate/'verify_middle.py').read_bytes()),'review_checker_sha256':sha((review/'independent_check.py').read_bytes()),'candidate_scientific_files':comparisons,'candidate_results_all_nonprovenance_fields_identical':True,'candidate_counts':m.COUNTS,'candidate_omitted_result_fields':{'source_bindings_checked':{'original_value':7,'freshly_checked':False}},'candidate_original_main_executed':False,'candidate_skipped_checks':['SOURCE_BINDINGS.json read','Seven original dependency byte-length and SHA-256 checks'],'candidate_stdout_replayed':False,'review_original_main_executed':True,'review_complete_output_comparisons':checks,'historical_proof_checkers_replayed':False,'finite_controls_are_not_a_square_mask_census':True,'floating_point_used':False,'external_writes':False}
  return out
if __name__=='__main__':
 print(json.dumps(replay(),indent=2,sort_keys=True))
