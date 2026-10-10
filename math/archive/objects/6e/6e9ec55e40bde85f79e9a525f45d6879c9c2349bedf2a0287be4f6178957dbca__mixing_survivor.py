"""Seeded arithmetic-free shuffle candidates; 'survivor' means no known rank contradiction."""
import random
from moving_partition import search_parity, moving_partition_budget, mask_boundary
from interval_sweep import sweep_intervals

def random_linear_bit_map(k,rng,steps=None):
    """Return a uniformly unspecified but guaranteed-invertible GF(2) linear map.
    Random elementary row additions/swaps, NOT a uniform GL(k,2) sample.
    """
    n=1<<k
    if steps is None:steps=k*k*2
    cols=[1<<i for i in range(k)]
    for _ in range(steps):
        i,j=rng.sample(range(k),2)
        if rng.randrange(4)==0:
            a=(cols[i]>>i)&1
            # Swap output rows i,j across all generator columns
            cols=[c^(((c>>i)&1 ^ (c>>j)&1)*((1<<i)|(1<<j))) for c in cols]
        else:
            cols=[c ^ (((c>>j)&1)<<i) for c in cols]
    p=[]
    for x in range(n):
        y=0
        for i in range(k):
            if x>>i&1:y^=cols[i]
        p.append(y)
    assert sorted(p)==list(range(n))
    return p,cols

def make(k,seed=20261010):
    rng=random.Random(seed+17*k)
    pair=[random_linear_bit_map(k,rng) for _ in range(3)]
    return [x[0] for x in pair],[x[1] for x in pair]

if __name__=='__main__':
 for k in (6,7,8):
    n=1<<k;ps,cols=make(k)
    parity,trial=search_parity(k,ps,[1]*4)
    interval,num=sweep_intervals(k,ps)
    print('n',n,'shuffle bit columns',cols)
    print('  parity witnesses',len(parity),'evaluated ranks',trial,'interval witnesses',len(interval),'tested',num,flush=True)
