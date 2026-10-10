import tempfile,pathlib,shutil,subprocess,json
p=pathlib.Path(__file__).parent
with tempfile.TemporaryDirectory() as td:
 d=pathlib.Path(td);(d/'source').mkdir()
 for f in ['check_independent.py','cut_certificate_own.cpp']:shutil.copyfile(p/f,d/f)
 for f in ['AFFINE_LAYOUT.json','EXACT_CERTIFICATES.json']:shutil.copyfile(p/'source'/f,d/'source'/f)
 subprocess.run(['python','check_independent.py'],cwd=d,capture_output=True,check=True)
 assert (d/'INDEPENDENT_RESULTS.json').read_bytes()==(p/'INDEPENDENT_RESULTS.json').read_bytes()
(p/'PORTABILITY.json').write_text(json.dumps({'status':'PASS','isolated_full_replay_byte_identical':True,'requirements':['Python standard library','C++17 compiler g++'],'source_code_executed':False},indent=2)+'\n');print('FULL ISOLATED REPLAY PASS')
