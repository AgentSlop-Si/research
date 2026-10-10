import numpy as np
from scipy import fft
from persistent_chain import ChainEngine

n=4096
engine=ChainEngine(max_complement_bytes=32*1024**2)
factors=[]
for pos in (1,3,5,11,17):
    a=np.zeros(n);a[0]=1.;a[pos]=.15
    factors.append(engine.seed(a))
original=engine.chain(factors)
branch_1=original.edit(2,201,2.)
branch_2=original.edit(2,201,-1.5).shift(2,7)
for title,version in [('Original',original),('Branch 1',branch_1),('Branch 2',branch_2)]:
    query=version.frequencies([0,2,13,17])
    dense=version.dense()
    np.testing.assert_allclose(query, fft.fft(dense)[[0,2,13,17]],atol=1e-8)
    print(title,'bins:',np.round(query,3))
    print(title,'first 10 outputs:',np.round(dense[:10],5))
print('Structural sharing:',original.count_reused_nodes(branch_1))
print('Memory:',engine.memory_report())
