"""Construct witnesses for heterogeneous scan ranks and bit-boundary budgets."""
from fractions import Fraction
from parity_oracle import pullback_mask, trace_witness, boundary, parity_block_rank
from gf2_depth_certificate import gf2_null_vector


def derive(k, shuffles, orders, bit_quotas):
    """One exact no-go witness whenever sum quotas < k and sum(r/2^q)<=1/4.

    Each permutation acts as an invertible GF(2)-linear index map, supplied by
    lists of its basis-image columns. Affine shifts are allowed: they only
    switch parity signs, not boundaries or block ranks.
    """
    t=len(orders)
    assert t==len(bit_quotas)==len(shuffles)+1
    assert sum(bit_quotas)<k
    assert all(q>=1 for q in bit_quotas)
    assert sum((Fraction(r,1<<q) for r,q in zip(orders,bit_quotas)),Fraction(0))<=Fraction(1,4)
    images=[1<<i for i in range(k)]
    equations=[]
    for j in range(t):
        for bit in range(bit_quotas[j]):
            equations.append(sum(((images[i]>>bit)&1)<<i for i in range(k)))
        if j<t-1:
            images=[pullback_mask(x,shuffles[j]) for x in images]
    mask=gf2_null_vector(equations,k)
    assert mask is not None
    stage_masks=[mask]
    for columns in shuffles:
        stage_masks.append(pullback_mask(stage_masks[-1],columns))
    assert all((m&((1<<q)-1))==0 for m,q in zip(stage_masks,bit_quotas))
    cap=sum(r*boundary(m,k) for r,m in zip(orders,stage_masks))
    rank=parity_block_rank(k,mask,stage_masks[-1])
    assert cap < (1<<k)//4 <= rank
    return {'k':k,'N':1<<k,'stage_orders':orders,'quotas':bit_quotas,
            'input_mask':mask,'stage_masks':stage_masks,
            'stage_boundaries':[boundary(m,k) for m in stage_masks],
            'capacity':cap,'exact_complex_fourier_rank':rank, 'gap':rank-cap}
