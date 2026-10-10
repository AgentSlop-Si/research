"""Portable verification of this continuation; no old benchmark reruns."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parent
CHECKS=[
    ('fft_rational_reuse_research','run_audit.py'),
    ('fft_rational_reuse_research','audit_fourier.py'),
    ('fft_rational_reuse_research','audit_defects.py'),
    ('fft_rational_reuse_research','audit_detector.py'),
    ('fft_tail_fusion_research','run_audit.py'),
    ('fft_tail_fusion_research','run_orbit_audit.py'),
    ('fft_multiparent_products_research','audit.py'),
    ('fft_polynomial_feedback_research','run_audit.py'),
    ('fft_crt_correction_research','run_audit.py'),
    ('fft_exact_recovery_research','run_audit.py'),
    ('fft_branch_fusion_research','run_audit.py'),
]

def run_one(item):
    folder,script=item
    start=time.monotonic()
    result=subprocess.run([sys.executable,script],cwd=ROOT/folder,capture_output=True,text=True)
    log=ROOT/'verification_logs'/f'{folder}__{Path(script).stem}.txt'
    log.write_text(result.stdout+result.stderr)
    return dict(component=folder,script=script,exit_code=result.returncode,
                elapsed_seconds=round(time.monotonic()-start,3),
                source_sha256=hashlib.sha256((ROOT/folder/script).read_bytes()).hexdigest(),
                log=str(log.relative_to(ROOT)))

def main():
    (ROOT/'verification_logs').mkdir(exist_ok=True)
    with ThreadPoolExecutor(max_workers=2) as pool:
        results=list(pool.map(run_one,CHECKS))
    passed=all(x['exit_code']==0 for x in results)
    report=dict(status='PASS' if passed else 'FAIL',checks=results,
                note='Correctness and portable integration only; elapsed times are not performance benchmarks.')
    (ROOT/'verification_summary.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
    return 0 if passed else 1

if __name__=='__main__':raise SystemExit(main())
