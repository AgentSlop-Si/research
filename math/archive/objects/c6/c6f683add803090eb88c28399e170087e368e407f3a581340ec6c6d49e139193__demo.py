from algebra_fft import AlgebraFFT
from two_edit_engine import prepare_two
from scipy import fft
import numpy as np

N=32768
rng=np.random.default_rng(42)
a,b,c,d=[rng.normal(size=N)/np.sqrt(N) for _ in range(4)]
e=AlgebraFFT(N)
A,B,C,D=[e.signal(x) for x in (a,b,c,d)]
y=e.add(e.mul(A,A,B),e.mul(A,B),e.mul(B,B),e.mul(C,D))
plan=prepare_two(e,y,A,B)
pa,alpha,pb,beta=123,.02,400,-.03
ans=plan.update(pa,alpha,pb,beta)
a2=a.copy();b2=b.copy();a2[pa]+=alpha;b2[pb]+=beta
fa,fb,fc,fd=[fft.rfft(x) for x in (a2,b2,c,d)]
ref=fft.irfft(fa*fa*fb+fa*fb+fb*fb+fc*fd,n=N)
print('Expression: A*A*B + A*B + B*B + C*D')
print('Symbolic jet degrees:',plan.symbolic_terms)
print('Dense correction kernels:',len(plan.dense_a),'Sparse point terms:',len(plan.sparse_a))
print('AOT shape matched:',plan.shape_available)
print('Precomputed memory bytes:',plan.memory_bytes)
print('Max difference from independent SciPy:',np.max(np.abs(ans-ref)))
print('Selected output coefficients:',plan.update(pa,alpha,pb,beta,indices=[0,1,N-1]))
