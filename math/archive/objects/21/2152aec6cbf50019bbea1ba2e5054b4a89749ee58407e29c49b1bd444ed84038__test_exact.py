"""Independent regression suite for exact parity-rank and GF2 depth gates."""
from __future__ import annotations
import random,sys,json
from pathlib import Path
import numpy as np
from parity_oracle import *
from gf2_depth_certificate import random_invertible_columns, gf2_null_vector, construct_witness
from heterogeneous_certificate import derive
from build_certificates import legacy_columns
BASE=Path(__file__).resolve().parent
PRIMES=(12289,65537)

# The prior source is used solely for independent finite-field rank checks.
prior=str(BASE/'prior_helpers')
if prior not in sys.path:sys.path.insert(0,prior)
from moving_partition import fourier_block_rank, parity_set


def test_pair_counts():
    for k in range(2,15):
        n=1<<k
        cnt=sum(parity_block_rank(k,a,b)==n//4 for a in range(1,n) for b in range(1,n)) if k<=7 else None
        if cnt is not None:assert cnt==deficient_pair_count(k)
        assert deficient_pair_count(k)==(k-2)*(n//2)+1
    print('PASS 1 exact deficient-mask counting, exhaustive through N=128')


def test_modular_ranks():
    for k in range(2,7):
        n=1<<k
        sets=[[x for x in range(n) if ((x&a).bit_count()&1)==0] for a in range(1,n)]
        rs=[[y for y in range(n) if ((y&b).bit_count()&1)==1] for b in range(1,n)]
        for p in PRIMES:
            for a in range(1,n):
                for b in range(1,n):
                    assert fourier_block_rank(n,rs[b-1],sets[a-1],p)==parity_block_rank(k,a,b),(k,a,b,p)
    print('PASS 2 exhaustive parity ranks in two fields through N=64')


def test_sign_independence():
    for k in (3,4):
        n=1<<k
        rng=random.Random(322)
        for _ in range(30):
            a=rng.randrange(1,n);b=rng.randrange(1,n)
            rank=parity_block_rank(k,a,b)
            for x_sign in (0,1):
                for y_sign in (0,1):
                    C=[x for x in range(n) if ((x&a).bit_count()&1)==x_sign]
                    R=[y for y in range(n) if ((y&b).bit_count()&1)==y_sign]
                    assert fourier_block_rank(n,R,C,12289)==rank
    print('PASS 3 all parity offsets/signs for sampled cases')


def test_modular_false_negative_control():
    C=[0,1,2,3,4,13,6,7]
    R=[0,1,2,3,4,6,7,12]
    assert set(c%8 for c in C)==set(range(8)) # universal sampling C
    assert fourier_block_rank(16,R,C,12289)==7
    assert fourier_block_rank(16,R,C,65537)==8
    print('PASS 4 modular ranks can understate complex ranks; control reproduced')


def test_legacy_columns():
    # Independent reproduction of basis data from prior (including random-seed convention).
    from mixing_survivor import make
    for k in (6,7,8,9,10):
        _,old=make(k,20261016)
        assert legacy_columns(k)==old
    print('PASS 5 exact reproduction of earlier mixing candidates')


def test_certificates():
    rec=json.loads((BASE/'EXACT_CERTIFICATES.json').read_text())
    for name,w in rec['legacy_layout_witnesses'].items():
        k=int(name).bit_length()-1
        assert legacy_columns(k)==w['three_GF2_shuffle_columns']
        masks=[w['input_mask']]
        for cols in w['three_GF2_shuffle_columns']:
            masks.append(pullback_mask(masks[-1],cols))
        assert masks==w['masks']
        assert [boundary(x,k) for x in masks]==w['stage_capacities']
        assert sum(w['stage_capacities'])==w['capacity']
        assert parity_block_rank(k,masks[0],masks[-1])==w['complex_fourier_rank']
        assert w['gap']==w['complex_fourier_rank']-w['capacity']
        if int(name)>256:assert w['gap']>0
    for name,w in rec['universal_GF2_depth_witnesses'].items():
        k=w['k'];t=w['t'];q=w['q'];m=w['input_mask']
        assert k>t*q and q==(4*w['r']*t-1).bit_length()
        masks=[m]
        for cols in w['GF2_shuffle_columns']:
            masks.append(pullback_mask(masks[-1],cols))
        assert masks==w['masks']
        assert all(x%(1<<q)==0 for x in masks)
        assert sum(boundary(x,k) for x in masks)==w['capacity']
        assert w['capacity']<w['complex_fourier_rank']
    w=rec['heterogeneous_example']
    res=derive(w['k'],w['GF2_shuffle_columns'],w['stage_orders'],w['quotas'])
    assert res['stage_masks']==w['stage_masks']
    assert res['capacity']==w['capacity']
    print('PASS 6 archived certificates reconstructed (uniform and heterogeneous)')


def test_two_prime_witnesses():
    rec=json.loads((BASE/'EXACT_CERTIFICATES.json').read_text())['legacy_layout_witnesses']
    for n in (512,1024):
        w=rec[str(n)];k=n.bit_length()-1
        C=[j for j in range(n) if ((j&w['input_mask']).bit_count()&1)==0]
        R=[j for j in range(n) if ((j&w['output_mask']).bit_count()&1)==1]
        assert w['capacity']<w['complex_fourier_rank']==n//2
        for p in PRIMES:
            assert fourier_block_rank(n,R,C,p)==n//2
    print('PASS 7 N=512/1024 strict contradictions verified in two fields')


def test_kernel_synthesis():
    rng=random.Random(8543)
    for k in (6,8,11,17,20):
        t=3;q=4
        cols=[random_invertible_columns(k,rng) for _ in range(t-1)]
        if k>t*q:
            proof=construct_witness(k,cols)
            assert proof['gap']>0
        else:
            # Validate GF2 solver without demanding an existing kernel.
            vec=gf2_null_vector([1<<i for i in range(k)],k)
            assert vec is None
    print('PASS 8 exact GF2 nullspace construction and depth-witness generation')


def test_random_mixing_summary():
    from mixer_experiment import evaluate
    observed=evaluate(ks=(8,9,10,11,12),count=50)
    stored=json.loads((BASE/'MIXER_EXPERIMENT.json').read_text())
    assert observed==stored
    print('PASS 9 independent reproducibility of five random mixer ensembles')


def test_boundary_formula():
    for k in range(2,12):
        n=1<<k
        rng=random.Random(k)
        for _ in range(100):
            a=rng.randrange(1,n)
            b=sum(((x&a).bit_count()&1)!=(((x+1)&a).bit_count()&1) for x in range(n-1))
            assert boundary(a,k)==b
    print('PASS 10 scan-boundary formula compared to explicit transitions')


if __name__ == '__main__':
    test_pair_counts()
    test_modular_ranks()
    test_sign_independence()
    test_modular_false_negative_control()
    test_legacy_columns()
    test_certificates()
    test_two_prime_witnesses()
    test_kernel_synthesis()
    test_random_mixing_summary()
    test_boundary_formula()
    print('ALL 10/10 NEW TEST GROUPS PASS')
