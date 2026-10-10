"""Portable checks for this continuation only; earlier benchmarks stay historical."""
from concurrent.futures import ThreadPoolExecutor
import hashlib,json
from pathlib import Path
import subprocess,sys,time

ROOT=Path(__file__).resolve().parent
CHECKS=[
    ('fft_recurrence_extension_research','audit.py'),
    ('fft_recurrence_extension_research','independent_checks.py'),
    ('fft_qlinear_recurrence_research','run_audit.py'),
    ('fft_joint_decode_research','run_audit.py'),
    ('fft_joint_decode_research','run_hybrid_audit.py'),
    ('fft_joint_decode_research','review_edge_checks.py'),
    ('fft_joint_sideinfo_research','run_audit.py'),
    ('fft_joint_sideinfo_research/tensor','run_audit.py'),
    ('fft_inverse_support_research','run_audit.py'),
]


def run_one(item):
    folder,script=item;start=time.monotonic()
    result=subprocess.run([sys.executable,script],cwd=ROOT/folder,capture_output=True,text=True)
    log=ROOT/'verification_logs'/f'{folder.replace("/","_")}__{Path(script).stem}.txt'
    log.write_text(result.stdout+result.stderr)
    return dict(component=folder,script=script,exit_code=result.returncode,
                elapsed_seconds=round(time.monotonic()-start,3),
                source_sha256=hashlib.sha256((ROOT/folder/script).read_bytes()).hexdigest(),
                log=str(log.relative_to(ROOT)))


def main():
    (ROOT/'verification_logs').mkdir(exist_ok=True)
    with ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(run_one,CHECKS))
    passed=all(r['exit_code']==0 for r in results)
    report=dict(status='PASS' if passed else 'FAIL',checks=results,
                note='New correctness and integration checks; elapsed times are not performance benchmarks.')
    (ROOT/'verification_summary.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2));return 0 if passed else 1


if __name__=='__main__':raise SystemExit(main())
