"""Run the inspected exact attempt with measured resource and wall limits."""
import json, pathlib, subprocess, sys, time, resource
ROOT=pathlib.Path(__file__).resolve().parent
started=time.monotonic()
with (ROOT/'ELIMINATION.log').open('w') as out:
    p=subprocess.Popen([sys.executable,str(ROOT/'attempt_elimination.py')],stdout=out,stderr=subprocess.STDOUT)
    timed_out=False
    try:p.wait(timeout=210)
    except subprocess.TimeoutExpired:
        timed_out=True;p.kill();p.wait()
result={'returncode':p.returncode,'wall_seconds':time.monotonic()-started,'wall_timeout':timed_out,
        'child_cpu_seconds':resource.getrusage(resource.RUSAGE_CHILDREN).ru_utime+resource.getrusage(resource.RUSAGE_CHILDREN).ru_stime,
        'child_max_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
(ROOT/'RESOURCE_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
