"""Run the portable component checks, without rerunning timing experiments."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
CHECKS = [
    ('fft_route_barriers_research', 'audit.py'),
    ('fft_route_barriers_research', 'audit_numeric_shifts.py'),
    ('fft_route_barriers_research', 'independent_review_checks.py'),
    ('fft_resolvent_aggregate_research', 'run_audit.py'),
    ('fft_graph_feedback_research', 'run_audit.py'),
    ('fft_sparse_grading_research', 'run_audit.py'),
    ('fft_exact_decimation_research', 'run_audit.py'),
    ('fft_strong_scale_research', 'run_audit.py'),
    ('fft_native_energy_research', 'verify.py'),
    ('fft_surrogate_prefix_research', 'run_audit.py'),
    ('fft_surrogate_prefix_research', 'independent_review_checks.py'),
    ('fft_structured_phase_research', 'audit.py'),
]

def run_one(item):
    folder, script = item
    start = time.monotonic()
    result = subprocess.run([sys.executable, script], cwd=ROOT/folder,
                            capture_output=True, text=True)
    name = folder + '__' + Path(script).stem
    log = ROOT/'verification_logs'/f'{name}.txt'
    log.write_text(result.stdout + result.stderr)
    return dict(component=folder, script=script, exit_code=result.returncode,
                elapsed_seconds=round(time.monotonic()-start, 3),
                source_sha256=hashlib.sha256((ROOT/folder/script).read_bytes()).hexdigest(),
                log=str(log.relative_to(ROOT)))

def main():
    (ROOT/'verification_logs').mkdir(exist_ok=True)
    # Two jobs bound host contention. Recorded benchmark data are unchanged.
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(run_one, CHECKS))
    passed = all(row['exit_code'] == 0 for row in results)
    report = dict(status='PASS' if passed else 'FAIL', checks=results,
                  note='Integration and correctness checks; no timing benchmark rerun.')
    (ROOT/'verification_summary.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))
    return 0 if passed else 1

if __name__ == '__main__':
    raise SystemExit(main())
