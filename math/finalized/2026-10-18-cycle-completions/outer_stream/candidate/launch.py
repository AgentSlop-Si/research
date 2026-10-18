"""Fresh local test launcher. Caps and hashes are process evidence only."""
from pathlib import Path
import hashlib,json,os,resource,subprocess,sys,time
ROOT=Path(__file__).resolve().parent
SOURCES=('production_scalar.py','outer_wrapper.py','sparse_output.py','full_transfer.py','true_interval_oracle.py','test_full_transfer.py')
def hashes():return {n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in SOURCES}
def limits():
    resource.setrlimit(resource.RLIMIT_CPU,(180,185))
    resource.setrlimit(resource.RLIMIT_AS,(512*1024*1024,)*2)
    resource.setrlimit(resource.RLIMIT_FSIZE,(32*1024*1024,)*2)
    resource.setrlimit(resource.RLIMIT_NOFILE,(64,64))
pre=hashes();start=time.monotonic()
try:
    proc=subprocess.run([sys.executable,'-B','test_full_transfer.py'],cwd=ROOT,
        stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=240,preexec_fn=limits)
    code=proc.returncode;out,err=proc.stdout,proc.stderr;timed_out=False
except subprocess.TimeoutExpired as exc:
    code=None;out=str(exc.stdout or '');err=str(exc.stderr or '');timed_out=True
post=hashes()
(ROOT/'RUN.stdout').write_text(out);(ROOT/'RUN.stderr').write_text(err)
receipt={'exit_code':code,'timed_out':timed_out,'wall_seconds':time.monotonic()-start,
         'max_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
         'limits':{'cpu_soft_seconds':180,'cpu_hard_seconds':185,'wall_seconds':240,
                   'address_space_bytes':512*1024*1024,'file_size_bytes':32*1024*1024,'file_descriptors':64},
         'source_hashes_before':pre,'source_hashes_after':post,'sources_unchanged':pre==post}
(ROOT/'PROCESS_EXIT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2));print(out);print(err,file=sys.stderr)
if code!=0 or pre!=post or timed_out:sys.exit(1)
