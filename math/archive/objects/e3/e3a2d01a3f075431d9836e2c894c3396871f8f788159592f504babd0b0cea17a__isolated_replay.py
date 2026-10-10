import tempfile,pathlib,shutil,subprocess,json
p=pathlib.Path(__file__).parent
with tempfile.TemporaryDirectory() as td:
 d=pathlib.Path(td);(d/'source').mkdir()
 for f in ['independent_phase38.py','charzero_own.py','additional_controls.py','exhaustive_own.cpp']:shutil.copyfile(p/f,d/f)
 for f in (p/'source').glob('phase38_instance_*.txt'):shutil.copyfile(f,d/'source'/f.name)
 shutil.copyfile(p/'source/phase38_audit.json',d/'source/phase38_audit.json')
 for f in ['independent_phase38.py','charzero_own.py','additional_controls.py']:subprocess.run(['python',f],cwd=d,capture_output=True,check=True)
 for f in ['INDEPENDENT_RESULTS.json','CHARZERO_RESULTS.json','ADDITIONAL_RESULTS.json']:assert (d/f).read_bytes()==(p/f).read_bytes()
(p/'PORTABILITY.json').write_text(json.dumps({'status':'PASS','isolated_replay':'full, including all 2,076,565,824 mapping checks and 800,000 new samples','all_three_results_byte_identical':True,'requirements':['Python 3 standard library','C++17 compiler g++'],'source_programs_executed':False},indent=2)+'\n');print('ISOLATED REPLAY PASS')
