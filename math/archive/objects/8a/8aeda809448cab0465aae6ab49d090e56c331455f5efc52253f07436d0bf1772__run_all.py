"""Reproduce focused new checks; keep historical benchmarks and logs separate."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import importlib.util
import json
import os
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'verification'
OUT.mkdir(exist_ok=True)
CASES = [
    ('energy_exact', 'fft_energy_pruned_research', ['exact_small_audit.py'], None, None),
    ('graph_compiler', 'fft_sparse_surrogate_bridge/graph', ['run_audit.py'], None, None),
    ('fast_kernel_resolvents', 'fft_qweyl_resolvent_research', ['run_audit.py'], None, None),
    ('highest_tail_fusion', 'fft_qweyl_fusion_research', ['run_audit.py'], None, None),
    ('rational_degree', 'fft_qweyl_rational_degree', ['run_audit.py'], None, None),
    ('finite_tail', 'fft_qweyl_tail_research', ['run_audit.py'], None, None),
    ('cyclic_regularization', 'fft_cyclic_regularization_research', ['run_audit.py'], None, None),
    ('earlier_anchor_comparator', 'fft_transparent_fusion_research', ['run_audit.py'], None, None),
    ('scalar_prefixes', 'fft_constructive_review_new', ['scalar_prefix_checks.py'], None, None),
    ('source_height', 'inputs/constructive_theorem', ['-m', 'unittest', '-v', 'test_height_certificate.py'], None, None),
    ('energy_numeric', 'fft_energy_pruned_research', ['run_audit.py'], 'numpy', None),
    ('surrogate_v1_adapter', 'fft_sparse_surrogate_bridge/review', ['check_review.py'], 'numpy', 'inputs/sparse_surrogate'),
    ('surrogate_v2_fixes', 'fft_sparse_surrogate_bridge/review/v2', ['check_v2.py'], 'numpy', 'inputs/sparse_surrogate_v2'),
    ('source_surrogate_v1', 'inputs/sparse_surrogate', ['-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_sparse_surrogate.py', '-v'], 'numpy', 'inputs/sparse_surrogate'),
    ('source_surrogate_v2', 'inputs/sparse_surrogate_v2', ['-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_sparse_surrogate_v2.py', '-v'], 'numpy', 'inputs/sparse_surrogate_v2'),
]


def run(case):
    name, directory, args, dependency, extra = case
    record = dict(name=name, cwd=directory, command=[sys.executable, *args])
    if dependency and importlib.util.find_spec(dependency) is None:
        return dict(record, status='SKIPPED', reason='Missing dependency: '+dependency)
    env = os.environ.copy()
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    env['OPENBLAS_NUM_THREADS'] = '1'
    env['OMP_NUM_THREADS'] = '1'
    if extra:
        env['PYTHONPATH'] = str(ROOT/extra)
    start = time.monotonic()
    try:
        result = subprocess.run([sys.executable, *args], cwd=ROOT/directory,
            env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        (OUT/(name+'.log')).write_text(result.stdout)
        record.update(status='PASS' if result.returncode == 0 else 'FAIL',
            returncode=result.returncode, seconds=time.monotonic()-start,
            log='verification/'+name+'.log')
    except OSError as exc:
        record.update(status='FAIL', reason=str(exc))
    print(name+': '+record['status'], flush=True)
    return record


if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(run, CASES))
    result = dict(status='FAIL' if any(r['status']=='FAIL' for r in results)
        else ('PASS_WITH_SKIPS' if any(r['status']=='SKIPPED' for r in results) else 'PASS'),
        suites=results,
        not_rerun=[{'suite':'Supplied 13-test independent conditioning suite',
                    'reason':'SymPy unavailable during review; historical source results are not fresh results'},
                   {'suite':'Timing benchmarks','reason':'Captured cold timings preserved; this run is correctness verification'}])
    (OUT/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print('Overall: '+result['status'])
    raise SystemExit(1 if result['status']=='FAIL' else 0)
