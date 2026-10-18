"""Fresh source-pinned resource-capped local launcher."""
import hashlib,json,os,resource,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
SOURCES=('outer_wrapper.py','sparse_output.py','production_scalar.py','regression.py','launch.py')
def hashes():return {x:hashlib.sha256((ROOT/x).read_bytes()).hexdigest() for x in SOURCES}
def limits():
    resource.setrlimit(resource.RLIMIT_CPU,(120,125))
    resource.setrlimit(resource.RLIMIT_AS,(512*1024*1024,512*1024*1024))
    resource.setrlimit(resource.RLIMIT_FSIZE,(32*1024*1024,32*1024*1024))
    resource.setrlimit(resource.RLIMIT_NOFILE,(64,64))
def main():
    before=hashes();start=time.monotonic();timed_out=False
    try:
        r=subprocess.run([sys.executable,'-B',str(ROOT/'regression.py')],cwd=ROOT,env={**os.environ,'PYTHONHASHSEED':'0','PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,text=True,timeout=180,preexec_fn=limits)
        code,out,err=r.returncode,r.stdout,r.stderr
    except subprocess.TimeoutExpired as e:
        timed_out=True;code=None;out=str(e.stdout or '');err=str(e.stderr or '')
    receipt={'returncode':code,'timeout':timed_out,'elapsed_seconds':time.monotonic()-start,'stdout':out,'stderr':err,
       'caps':{'wall_seconds':180,'cpu_soft_seconds':120,'cpu_hard_seconds':125,'address_space_bytes':512*1024*1024,'file_size_bytes':32*1024*1024,'open_files':64},
       'pre_source_sha256':before,'post_source_sha256':hashes(),'source_unchanged':before==hashes()}
    (ROOT/'PROCESS_EXIT.json').write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n')
    print(json.dumps(receipt,sort_keys=True,indent=2))
    return 0 if code==0 and not timed_out and receipt['source_unchanged'] else 1
if __name__=='__main__':raise SystemExit(main())
