import hashlib,json,os,resource,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
CANDIDATE=Path(__file__).resolve().parent / '../candidate'
def source_hashes():
 return {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'independent_structural_tests.py',*[CANDIDATE/n for n in ('outer_wrapper.py','sparse_output.py','production_scalar.py','MANIFEST.json')]]}
def limits():
 resource.setrlimit(resource.RLIMIT_CPU,(120,125));resource.setrlimit(resource.RLIMIT_AS,(512*1024*1024,512*1024*1024));resource.setrlimit(resource.RLIMIT_FSIZE,(32*1024*1024,32*1024*1024));resource.setrlimit(resource.RLIMIT_NOFILE,(64,64))
before=source_hashes();start=time.monotonic()
r=subprocess.run([sys.executable,'-B',str(ROOT/'independent_structural_tests.py')],cwd=ROOT,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONHASHSEED':'0'},capture_output=True,text=True,timeout=180,preexec_fn=limits)
receipt={'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'elapsed_seconds':time.monotonic()-start,'source_hashes_before':before,'source_hashes_after':source_hashes(),'caps':{'wall_seconds':180,'cpu_soft_seconds':120,'cpu_hard_seconds':125,'address_space_bytes':512*1024*1024,'file_size_bytes':32*1024*1024,'open_files':64}}
assert receipt['source_hashes_before']==receipt['source_hashes_after']
(ROOT/'PROCESS_EXIT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(json.dumps(receipt,indent=2,sort_keys=True))
sys.exit(r.returncode)
