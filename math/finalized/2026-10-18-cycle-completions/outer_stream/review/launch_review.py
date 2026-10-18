from pathlib import Path
import subprocess,sys,resource,time,os,json,hashlib
root=Path(__file__).resolve().parent
paths=[root/'independent_review.py',*sorted((root/'runtime').glob('*.py'))]
def digests():return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
before=digests()
def limits():
    resource.setrlimit(resource.RLIMIT_CPU,(150,160))
    resource.setrlimit(resource.RLIMIT_AS,(768*1024**2,768*1024**2))
    resource.setrlimit(resource.RLIMIT_FSIZE,(32*1024**2,32*1024**2))
    resource.setrlimit(resource.RLIMIT_NOFILE,(64,64))
start=time.monotonic()
with (root/'RUN.stdout').open('w') as out,(root/'RUN.stderr').open('w') as err:
    try:
        p=subprocess.run([sys.executable,'-B',str(root/'independent_review.py')],cwd=root,stdout=out,stderr=err,timeout=240,preexec_fn=limits,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
        code=p.returncode
    except subprocess.TimeoutExpired:code='WALL_TIMEOUT'
result={'exit_code':code,'wall_seconds':time.monotonic()-start,'max_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'source_hashes_before':before,'source_hashes_after':digests(),'limits':{'cpu_soft_seconds':150,'cpu_hard_seconds':160,'wall_seconds':240,'address_space_bytes':768*1024**2,'file_size_bytes':32*1024**2,'descriptors':64}}
(root/'PROCESS_EXIT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
raise SystemExit(0 if code==0 and before==digests() else 1)
