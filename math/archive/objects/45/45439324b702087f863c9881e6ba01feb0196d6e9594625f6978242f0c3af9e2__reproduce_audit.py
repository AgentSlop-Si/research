"""Bounded independent implementation repros; no writes to reviewed sources."""
import argparse
import json
import sys
import tracemalloc
import warnings
from pathlib import Path

import numpy as np
from scipy import fft

p = argparse.ArgumentParser()
p.add_argument('--source', type=Path, default=Path(__file__).parent/'original_copy')
args = p.parse_args()
sys.path.insert(0, str(args.source.resolve()))
from cost_aware_fft import RelationFFT, sparse_from_known_changes
from persistent_chain import ChainEngine
from relational_convolution import RelationalConvolver, subscribe_convolution

def emit(name, **values):
    print(json.dumps(dict(case=name, **values)), flush=True)

x=np.arange(8.)
want=fft.rfft(x+np.eye(1,8,1)[0]*2.)
got=sparse_from_known_changes(fft.rfft(x),8,[(1,2.)],method='auto')
emit('spectrum_only_auto', actual_dc=float(got[0].real), expected_dc=float(want[0].real),
     max_abs_error=float(np.max(abs(got-want))))

e=RelationFFT(max_temp_bytes=256)
s=e.register(np.arange(16.)).edit(3,1.)
try:
    profile=e.calibrate(s,repeats=2)
    emit('calibration_budget', completed=True, methods=list(profile.median_seconds))
except MemoryError as exc:
    emit('calibration_budget', completed=False, error=str(exc))

e=RelationFFT()
s=e.register(np.arange(8.)).edit(1,2.)
for cached in (False,True):
    if cached:s.spectrum('native',cache_output=True)
    for method in ('reuse','zero','linear'):
        try:
            s.spectrum(method)
            emit('invalid_method_cache_bypass', cached=cached, method=method, accepted=True)
        except ValueError:
            emit('invalid_method_cache_bypass', cached=cached, method=method, accepted=False)

e=RelationFFT(max_phase_bytes=32784)
phase=e._phase_vector(4096,7,2049)
owner=phase
while isinstance(owner.base,np.ndarray):owner=owner.base
emit('phase_cache_budget', budget=e.max_phase_bytes,
     reported=e.memory_report()['internal_phase_cache_bytes'], retained_bytes=owner.nbytes,
     cached=bool(e._phase))

n,k=65536,8
e=RelationFFT(max_temp_bytes=16*n+8*(n//k),max_phase_bytes=0)
s=e.register(np.zeros(n))
for j in range(k):s.edit(j+1,j+.25)
tracemalloc.start()
try:
    out=s.spectrum('pruned')
    _,peak=tracemalloc.get_traced_memory()
    emit('pruned_work_arrays', admitted=True,budget=e.max_temp_bytes,
         traced_peak=peak,peak_minus_output=peak-out.nbytes)
except MemoryError as exc:
    emit('pruned_work_arrays',admitted=False,budget=e.max_temp_bytes,error=str(exc))
finally:tracemalloc.stop()

e=RelationFFT()
a=e.register([0.,0.]).edit(0,1e308)
b=e.register([1e-308,0.])
sub=subscribe_convolution(RelationalConvolver().product(a,b),[0])
before=sub.values().copy()
try:
    sub.edit('left',0,1e308)
except ValueError as exc:
    emit('subscription_rejected_edit', error=str(exc), before=before.tolist(),
         after=sub.values().tolist(), snapshot=[sub.snapshot_view().at(0)], events=sub.events)

e=ChainEngine()
single=e.chain([e.seed([1.])])
v=single
for _ in range(1099):v=v.convolve_with(single)
for action in ('factor','edit'):
    try:
        out=v.factor(0) if action=='factor' else v.edit(0,0,.25)
        emit('sequential_composition',factors=v.root.size, action=action, completed=True)
    except RecursionError as exc:
        emit('sequential_composition',factors=v.root.size, action=action, completed=False,error=str(exc))
balanced=e.chain([single.factor(0)]*1100)
emit('balanced_composition_control',factors=balanced.root.size,value=balanced.edit(0,0,.25).dense().tolist())

with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter('always')
    try:
        seed=ChainEngine().seed(np.array([1+2j,3+4j]))
        emit('complex_input', accepted=True, signal=seed.values().tolist(),warnings=[str(x.message) for x in w])
    except ValueError as exc:
        emit('complex_input', accepted=False, error=str(exc))

e1,e2=RelationFFT(),RelationFFT()
a,b=e1.register([1.,2.]),e2.register([3.,4.])
try:
    e1.combine([a,b],[1.,1.])
    emit('cross_engine_combine_control',rejected=False)
except ValueError as exc:
    emit('cross_engine_combine_control',rejected=True,error=str(exc))

c1,c2=ChainEngine(),ChainEngine()
v1=c1.chain([c1.seed([1.,2.])]);v2=c2.chain([c2.seed([3.,4.])])
emit('cross_engine_sharing_diagnostic',same_object=v1.root is v2.root,
     reported=v1.count_reused_nodes(v2))
