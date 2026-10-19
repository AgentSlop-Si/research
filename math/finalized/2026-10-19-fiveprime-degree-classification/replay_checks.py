"""Run exact original scientific controls with only provenance verification replaced."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import importlib.util,tempfile,contextlib,io,json,sys,hashlib
from verify_package import verify
ROOT=Path(__file__).resolve().parent

def main():
 before=verify(ROOT)
 source=ROOT/'review/independent_check.py'
 assert hashlib.sha256(source.read_bytes()).hexdigest()=='898ba533706aa6cc9cf63d3f68a8cd69c528f7ee6619f3cd47d281284a9aaab6'
 spec=importlib.util.spec_from_file_location('accepted_independent_synthesis_controls',source)
 module=importlib.util.module_from_spec(spec);sys.dont_write_bytecode=True;spec.loader.exec_module(module)
 expected=json.loads((ROOT/'review/RESULTS.json').read_text())
 with tempfile.TemporaryDirectory(prefix='fiveq_synthesis_replay_') as tmp:
  module.HERE=Path(tmp)
  module.integrity=lambda originals=False: {'portable_export':True,'seven_dependencies_verified':verify(ROOT)['seven_logical_dependencies_verified'],'original_private_provenance_replayed':False}
  stdout=io.StringIO()
  with contextlib.redirect_stdout(stdout):module.main()
  fresh=json.loads((Path(tmp)/'RESULTS.json').read_text())
  old={k:v for k,v in expected.items() if k!='integrity'}
  new={k:v for k,v in fresh.items() if k!='integrity'}
  assert new==old,'Scientific results changed'
  console=json.loads(stdout.getvalue());assert console['counts']==expected['counts'] and console['verdict']=='PASS'
 after=verify(ROOT);assert before==after
 out={'verdict':'PASS','unchanged_checker_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'overrides':['HERE: temporary output directory','integrity: verify public package instead of omitted original provenance'],'scientific_main_and_functions_unchanged':True,'scientific_results_equal_after_removing_only_integrity':True,'compared_results_fields':sorted(new),'counts':fresh['counts'],'original_stdout_byte_replayed':False,'original_private_provenance_replayed':False,'full_historical_component_checkers_rerun':False,'frozen_evidence_unchanged':True,'network_required':False}
 print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
