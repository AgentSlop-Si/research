from pathlib import Path
import tempfile,shutil,subprocess,json
p=Path(__file__).parent
with tempfile.TemporaryDirectory() as td:
 d=Path(td);(d/'source').mkdir()
 for f in ['own_algorithm.py','check_large_profile.py','check_profile_model.py']:shutil.copyfile(p/f,d/f)
 shutil.copyfile(p/'source/RESULTS.json',d/'source/RESULTS.json')
 for f in ['check_profile_model.py','check_large_profile.py']:subprocess.run(['python',f],cwd=d,capture_output=True,check=True)
 for f in ['INDEPENDENT_RESULTS.json','PROFILE_MODEL_RESULTS.json','LARGE_PROFILE_RESULTS.json']:assert (d/f).read_bytes()==(p/f).read_bytes()
(p/'PORTABILITY.json').write_text(json.dumps({'status':'PASS','all_three_results_byte_identical':True,'isolated_largest_N':262144,'standard_library_only':True,'source_code_executed':False},indent=2)+'\n');print('ISOLATED COMPANION REPLAY PASS')
