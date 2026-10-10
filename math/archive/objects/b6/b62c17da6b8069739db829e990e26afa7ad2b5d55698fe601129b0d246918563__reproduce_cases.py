"""Run four bounded issue repros against original or patched source.

python reproduce_cases.py --source '/path/to/cost_aware_fft(1).py'
The included, unchanged Phase4 phase.py supplies the compatible dependency.
No performance benchmarking or source mutation is performed.
"""
import argparse
import importlib.util
import json
import sys
import tracemalloc
from pathlib import Path

import numpy as np
from scipy import fft

parser = argparse.ArgumentParser()
parser.add_argument('--source', type=Path, default=Path(__file__).with_name('cost_aware_fft.py'))
args = parser.parse_args()
spec = importlib.util.spec_from_file_location('review_target', args.source)
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)

x = np.arange(8.)
want = fft.rfft(x + np.eye(1, 8, 1)[0]*2)
got = m.sparse_from_known_changes(fft.rfft(x), 8, [(1, 2.)], method='auto')
print('spectrum_only_auto', json.dumps({'dc_actual': got[0].real,
      'dc_expected': want[0].real, 'max_abs_error': float(np.max(np.abs(got-want)))}))

e = m.RelationFFT(max_temp_bytes=256)
s = e.register(np.arange(16.)).edit(3, 1.)
try:
    p = e.calibrate(s, repeats=2)
    print('calibration', json.dumps({'completed': True, 'eligible_methods': list(p.median_seconds)}))
except MemoryError as exc:
    print('calibration', json.dumps({'completed': False, 'error': str(exc)}))

e = m.RelationFFT(max_phase_bytes=32784)
p = e._phase_vector(4096, 7, 2049)
owner = p
while isinstance(owner.base, np.ndarray):
    owner = owner.base
print('phase_cache', json.dumps({'limit': e.max_phase_bytes,
      'reported': e.memory_report()['internal_phase_cache_bytes'],
      'cached': bool(e._phase), 'returned_phase_backing_bytes': owner.nbytes}))

n, k = 65536, 8
e = m.RelationFFT(max_temp_bytes=16*n+8*(n//k), max_phase_bytes=0)
s = e.register(np.zeros(n))
for p in range(k):
    s.edit(p+1, p+.25)
tracemalloc.start()
try:
    got = s.spectrum(method='pruned')
    current, peak = tracemalloc.get_traced_memory()
    print('pruned_memory', json.dumps({'admitted': True, 'budget': e.max_temp_bytes,
          'peak_traced_bytes': peak, 'peak_minus_returned_output': peak-got.nbytes}))
except MemoryError as exc:
    print('pruned_memory', json.dumps({'admitted': False, 'budget': e.max_temp_bytes, 'error': str(exc)}))
finally:
    tracemalloc.stop()
