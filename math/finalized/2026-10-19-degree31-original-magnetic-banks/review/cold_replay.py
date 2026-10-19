#!/usr/bin/env python3
import hashlib,json,resource,shutil,subprocess,tempfile,time
from pathlib import Path
R=Path(__file__).resolve().parent
with tempfile.TemporaryDirectory(prefix='degree31-review-cold-') as tmp:
    t=Path(tmp)
    for name in ['literal_review.py','inputs/DEGREE31_LITERAL_CERTIFICATE.json']:
        shutil.copy2(R/name,t/Path(name).name)
    start=time.perf_counter()
    p=subprocess.run(['python','-I','literal_review.py','DEGREE31_LITERAL_CERTIFICATE.json','--quiet'],cwd=t,capture_output=True,text=True)
    (R/'COLD_REPLAY.log').write_text(p.stdout+p.stderr)
    if p.returncode: raise RuntimeError('cold standalone check failed')
    original=(R/'LITERAL_REVIEW.json').read_bytes();cold=(t/'LITERAL_REVIEW.json').read_bytes()
    if original!=cold: raise RuntimeError('cold mathematical receipt differs')
    out={'verdict':'PASS','standalone_inert_certificate_only':True,'byte_identical_receipt':True,
         'certificate_sha256':hashlib.sha256((t/'DEGREE31_LITERAL_CERTIFICATE.json').read_bytes()).hexdigest(),
         'receipt_sha256':hashlib.sha256(cold).hexdigest(),'elapsed_seconds':time.perf_counter()-start,
         'child_cpu_seconds':resource.getrusage(resource.RUSAGE_CHILDREN).ru_utime+resource.getrusage(resource.RUSAGE_CHILDREN).ru_stime,
         'peak_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
    (R/'COLD_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
