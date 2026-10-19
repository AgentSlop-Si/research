#!/usr/bin/env python3
"""Fresh mathematical replay with explicit provenance/timing exclusions."""
from pathlib import Path
import contextlib, hashlib, importlib.util, io, json, os, subprocess, sys, tempfile
BASE=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def read(path):return json.loads(path.read_text())
def replay():
    author=BASE/'candidate';review=BASE/'review'
    with tempfile.TemporaryDirectory(prefix='endpoint-scientific-replay-') as name:
        temp=Path(name);work=temp/'author';work.mkdir()
        spec=importlib.util.spec_from_file_location('unchanged_endpoint_checker',author/'verify_endpoints.py')
        module=importlib.util.module_from_spec(spec);old=sys.dont_write_bytecode
        sys.dont_write_bytecode=True
        try:spec.loader.exec_module(module)
        finally:sys.dont_write_bytecode=old
        module.HERE=work
        # This is the sole skipped original function. It hashes frozen copies;
        # it does not access original source_path locations. Historical verdict
        # copies have disclosed administrative projections in this export.
        module.source_controls=lambda:None
        captured=io.StringIO()
        with contextlib.redirect_stdout(captured):module.main()
        comparisons=[]
        scientific=['DEGREE_CONTROLS.json','POSITIVE_CONTROLS.json','NEGATIVE_CONTROLS.json',
                    'SUPPORT_CONTROLS.json','ARBITRARY_LINE_SET_CONTROLS.json']
        for file in scientific:
            b=(work/file).read_bytes();assert b==(author/file).read_bytes(),file
            comparisons.append({'file':file,'sha256':sha(b),'byte_identical':True})
        actual=read(work/'RESULTS.json');expected=read(author/'RESULTS.json')
        assert expected['counts'].pop('frozen_source_hashes')==4
        assert actual==expected
        original_stdout=json.loads((author/'RUN.stdout').read_text())
        assert original_stdout['counts'].pop('frozen_source_hashes')==4
        assert json.loads(captured.getvalue())==original_stdout==expected
        independent=temp/'independent';independent.mkdir()
        checker=independent/'check_endpoints_independently.py'
        checker.write_bytes((review/checker.name).read_bytes())
        run=subprocess.run([sys.executable,str(checker)],capture_output=True,
                           env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
        assert run.returncode==0,run.stderr.decode()
        review_comparisons=[]
        for file in ['FULL_GRAM_CONTROLS.json','CANONICAL_CONTROLS.json','CANCELLATION_CONTROLS.json',
                     'FIXED_B_CONTROLS.json','ARITHMETIC_CONTROLS.json']:
            b=(independent/file).read_bytes();assert b==(review/file).read_bytes(),file
            review_comparisons.append({'file':file,'sha256':sha(b),'byte_identical':True})
        new=read(independent/'RESULTS.json');old_result=read(review/'RESULTS.json')
        new.pop('elapsed_seconds');old_result.pop('elapsed_seconds');assert new==old_result
        out=json.loads(run.stdout);old_out=json.loads((review/'RUN.stdout').read_text())
        out.pop('elapsed_seconds');old_out.pop('elapsed_seconds');assert out==old_out==new
        assert run.stderr==(review/'RUN.stderr').read_bytes()==b''
        return {'status':'PASS','candidate_checker_sha256':sha((author/'verify_endpoints.py').read_bytes()),
                'review_checker_sha256':sha((review/'check_endpoints_independently.py').read_bytes()),
                'candidate_scientific_file_comparisons':comparisons,
                'candidate_results_and_stdout_match_after_exclusions':True,
                'candidate_omitted_result_fields':{'counts.frozen_source_hashes':{'original_value':4,'freshly_checked':False}},
                'candidate_skipped_checks':['SOURCE_BINDINGS.json read','Four frozen historical-source byte-hash checks'],
                'candidate_does_not_read_source_path':True,'candidate_original_checker_unchanged':True,
                'candidate_main_called_with_only_source_controls_skipped':True,
                'candidate_original_stdout_byte_replayed':False,'candidate_counts':dict(module.COUNT),
                'review_original_main_executed':True,'review_original_checker_unchanged':True,
                'review_scientific_file_comparisons':review_comparisons,
                'review_results_and_stdout_match_after_exclusions':True,
                'review_nondeterministic_fields':['elapsed_seconds'],'review_original_stdout_byte_replayed':False,
                'review_stderr_byte_identical_and_empty':True,'review_counts':new['counts'],
                'complete_original_provenance_replayed':False,'historical_proof_checkers_replayed':False,
                'finite_controls_are_not_a_square_mask_census':True,'external_writes':False}
if __name__=='__main__':print(json.dumps(replay(),indent=2,sort_keys=True))
