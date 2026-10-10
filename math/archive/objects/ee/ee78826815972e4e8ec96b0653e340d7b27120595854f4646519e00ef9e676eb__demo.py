"""Demonstration: the compiler derives dense and sparse kernels from the graph."""
import numpy as np
from scipy import fft
from algebra_fft import AlgebraFFT
from compiled_kernels import compile_prepared
from auto_dispatch import plan_auto

n=1024
rng=np.random.default_rng(7)
a_data=rng.standard_normal(n)/np.sqrt(n)
b_data=rng.standard_normal(n)/np.sqrt(n)
c_data=rng.standard_normal(n)/np.sqrt(n)
d_data=rng.standard_normal(n)/np.sqrt(n)
e=AlgebraFFT(n)
a,b,c,d=[e.signal(x) for x in (a_data,b_data,c_data,d_data)]
# This graph includes an input that appears three times.
root=e.add(e.mul(a,a,a), e.scale(e.mul(a,b),2),e.mul(c,d))
prepared=e.prepare(root,a,max_degree=3)
compiled=compile_prepared(prepared,backend='numba')
print('degree:',compiled.degree,'dense correction degrees:',compiled.dense_degrees,'symbolic sparse corrections:',list(zip(compiled.sparse_degrees,compiled.sparse_positions)))
print('generated function preview:\n',compiled.generated_source[:1400])
t,delta=99,0.02
out=compiled.single(t,delta)
changed=a_data.copy();changed[t]+=delta
reference=fft.irfft(fft.rfft(changed)**3+2*fft.rfft(changed)*fft.rfft(b_data)+fft.rfft(c_data)*fft.rfft(d_data),n=n)
print('max error to independent SciPy:',np.max(np.abs(out-reference)))
print('selected coefficients:',compiled.single(t,delta,[0,2,13,100]))
plan=plan_auto(prepared,expected_versions=20)
print('auto dispatch:',plan.mode,plan.reason)
