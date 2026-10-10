"""Constructive all-length depth obstruction for GF(2)-linear interstage layouts.

For N=2**k and t order-r quasiseparable scans, if
k > t*ceil(log2(4*r*t)), some nonzero input parity mask gives
complex Fourier rank >= N/4 yet a moving-partition capacity < N/4.
This is a theorem about binary-linear permutations; not all permutations.
"""
from __future__ import annotations
import random
import math
from parity_oracle import pullback_mask, trace_witness


def random_invertible_columns(k: int, rng: random.Random):
    """Build a reproducible invertible GF(2) map from elementary row moves."""
    columns = [1 << i for i in range(k)]
    for _ in range(2*k*k):
        i,j=rng.sample(range(k),2)
        if rng.randrange(4)==0:
            mask=(1<<i)|(1<<j)
            columns=[c ^ (((((c>>i)&1) ^ ((c>>j)&1))) * mask) for c in columns]
        else:
            columns=[c ^ (((c>>j)&1)<<i) for c in columns]
    return columns


def gf2_null_vector(constraints: list[int], k: int):
    """Find nonzero solution to parity(row & x)=0, or None."""
    pivots={}
    for line in constraints:
        x=line
        while x:
            bit=x.bit_length()-1
            if bit in pivots:
                x ^= pivots[bit]
            else:
                pivots[bit]=x
                break
    free=next((i for i in range(k) if i not in pivots),None)
    if free is None:
        return None
    x=1<<free
    for p in sorted(pivots):
        if (pivots[p]&x).bit_count()&1:
            x ^= 1<<p
    assert x and all(((c&x).bit_count()&1)==0 for c in constraints)
    return x


def construct_witness(k: int, columns_per_shuffle: list[list[int]], r=1):
    t=len(columns_per_shuffle)+1
    q=(4*r*t-1).bit_length()
    if k<=t*q:
        return {'guarantee':False, 'k':k,'t':t,'r':r,'q':q}
    # The k basis input masks are transformed through the t stage layouts.
    basis=[1<<i for i in range(k)]
    constraints=[]
    for j in range(t):
        for low_bit in range(q):
            row=sum((((basis[i]>>low_bit)&1)<<i) for i in range(k))
            constraints.append(row)
        if j<t-1:
            basis=[pullback_mask(mask,columns_per_shuffle[j]) for mask in basis]
    mask=gf2_null_vector(constraints,k)
    assert mask is not None
    result=trace_witness(k,columns_per_shuffle,mask)
    assert all((m&((1<<q)-1))==0 for m in result['masks'])
    assert result['capacity'] <= t*((1 << (k-q))-1)*r
    assert result['capacity']< (1<<k)//4 <=result['complex_fourier_rank']
    return {'guarantee':True,'k':k,'t':t,'r':r,'q':q,
            **result}


if __name__=='__main__':
    for t in (2,3,4,5,6):
        r=1;q=(4*r*t-1).bit_length();k=t*q+1
        cols=[random_invertible_columns(k,random.Random(90000+t*100+j)) for j in range(t-1)]
        witness=construct_witness(k,cols,r)
        print(f't={t} k={k} N=2^{k} q={q} mask={witness["input_mask"]} '
              f'cap={witness["capacity"]} rank={witness["complex_fourier_rank"]} '
              f'gap={witness["gap"]}',flush=True)
