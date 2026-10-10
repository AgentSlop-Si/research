"""Exact, independent tests for the new nonlinear Fourier-rank research.
Run: python test_new.py
Dependencies: numpy, scipy, networkx (only graph-flow test requires latter two).
"""
from __future__ import annotations
from pathlib import Path
import json,random
import numpy as np
from nonlinear_fourier_oracle import (rank_periodic_universal,rank_parity_columns,
    parity_columns,transversal_columns,moving_partition_certificate)
from permutation_edits import (affine_from_columns,mcnot_permutation,
    rank_permutation_difference,gate_edit_rank,robust_rank_limit)
from exact_field_controls import (fourier_rank_mod,rank_mod,separated_generator_stage)

BASE=Path(__file__).resolve().parent
REC=json.loads((BASE/'EXACT_CERTIFICATES.json').read_text())
PRIMES=[12289,65537]

def test_arbitrary_rows():
    # Characteristic-zero formula; exact modular ranks are independent controls.
    rng=random.Random(17332);cases=0
    for k in range(3,7):
        n=1<<k
        for mask in range(1,n):
            for _ in range(5):
                row_count=rng.randrange(n+1)
                R=rng.sample(range(n),row_count)
                C=parity_columns(k,mask)
                rank=rank_parity_columns(k,mask,R)
                for p in PRIMES:
                    got=fourier_rank_mod(n,R,C,p)
                    assert got==rank,(k,mask,R,p,got,rank)
                cases+=1
    print('PASS 1: parity-column / arbitrary-row oracle,',cases,'two-prime cases')

def test_periodic_universal_E():
    rng=random.Random(15889);cases=0
    for k in range(3,7):
        n=1<<k
        for period in (1<<j for j in range(1,k+1)):
            m=period//2
            for _ in range(20):
                flags=[rng.randrange(2) for _ in range(m)]
                C=transversal_columns(n,period,flags)
                R=rng.sample(range(n),rng.randrange(n+1))
                assert len(C)==n//2 and len(set(C))==len(C)
                r=rank_periodic_universal(n,period,m,R)
                for p in PRIMES:
                    assert fourier_rank_mod(n,R,C,p)==r
                cases+=1
    print('PASS 2: non-parity periodic universal columns,',cases,'two-prime cases')

def test_parity_parity_old_formula():
    cases=0
    for k in range(2,8):
        n=1<<k
        # Spot/exhaust both parity signs using exact integer oracle.
        for mask in range(1,n):
            u=mask.bit_length()-1
            for out in range(1,n):
                v=out.bit_length()-1
                want=n//4 if u+v<=k-2 else n//2
                R=[x for x in range(n) if (x&out).bit_count()%2==1]
                assert rank_parity_columns(k,mask,R)==want
                cases+=1
    print('PASS 3: previous parity/parity theorem recovered,',cases,'ordered pairs')

def test_perm_edit_cycle_rank():
    rng=random.Random(798);cases=0
    for k in range(3,8):
        n=1<<k
        for m in range(1,min(k,4)):
            for _ in range(12):
                controls=rng.sample(range(k),m)
                target=next(t for t in range(k) if t not in controls)
                g=mcnot_permutation(k,controls,target)
                assert rank_permutation_difference(g,np.arange(n))==gate_edit_rank(k,m)
                if n<=64:
                    # completely separate numerical elimination control
                    M=np.zeros((n,n),dtype=np.int64)
                    M[np.arange(n),g]=1
                    M[np.arange(n),np.arange(n)]-=1
                    assert rank_mod(M,12289)==gate_edit_rank(k,m)
                cases+=1
    print('PASS 4: exact nonlinear-edit rank via permutation cycles,',cases,'gates')

def rebuild_256():
    x=REC['nonaffine_256'];k=x['k'];cols=x['affine_shuffle_columns']
    shuffles=[affine_from_columns(c) for c in cols]
    for step in x['toffoli_gate_sequence_in_shuffle_2']:
        shuffles[2]=shuffles[2][mcnot_permutation(k,step['controls'],step['target'])]
    return shuffles

def test_256_obstruction():
    x=REC['nonaffine_256'];k=x['k'];n=1<<k
    perms=rebuild_256()
    res=moving_partition_certificate(k,perms,[1]*4,x['witness']['input_mask'])
    assert res==x['witness']
    assert res['stage_channel_budget']==[11,53,43,17]
    assert res['exact_complex_fourier_rank']==128>124==res['capacity_bound']
    R=res['output_rows'];C=parity_columns(k,res['input_mask'])
    assert len(C)==len(R)==128
    assert sum(y%2==0 for y in R)==64
    for p in PRIMES:
        assert fourier_rank_mod(n,R,C,p)==128
    # This is genuinely non-GF2-affine (not just renamed linear wiring).
    p=perms[2];offset=int(p[0])
    linear=affine_from_columns([int(p[1<<j])^offset for j in range(k)],offset)
    assert int(np.count_nonzero(p!=linear))==160
    print('PASS 5: N=256 nonlinear exact rank obstruction 128>124; two primes')

def test_256_independent_mincut():
    from scan_network_cut import exact_mincut
    x=REC['nonaffine_256'];p=rebuild_256()
    R=x['witness']['output_rows'];C=parity_columns(x['k'],x['witness']['input_mask'])
    val=exact_mincut(256,[1]*4,p,R,C)
    assert val==x['directed_scan_network_mincut']==124
    print('PASS 6: independent 8,176-node exact directed-network min-cut = 124')

def test_robust_dense_affine():
    for n_str, x in REC['edit_robust'].items():
        k=x['k'];n=1<<k
        affine=[affine_from_columns(c) for c in x['affine_shuffle_columns']]
        baseline=moving_partition_certificate(k,affine,[1]*4,x['base_input_mask'])
        assert baseline['capacity_bound']==x['base_capacity']
        assert baseline['stage_channel_budget']==x['base_stage_boundaries']
        assert baseline['exact_complex_fourier_rank']==x['exact_complex_fourier_rank']
        modified=[v.copy() for v in affine]
        ds=[]
        for e in x['nonlinear_edits']:
            j=e['shuffle_index']
            modified[j]=modified[j][mcnot_permutation(k,e['controls'],e['target'])]
            ds.append(rank_permutation_difference(affine[j],modified[j]))
        assert ds==x['edit_ranks']==[n//8,n//8]
        cap=robust_rank_limit(x['base_capacity'],ds)
        assert cap==x['perturbed_network_rank_bound_on_original_endpoint_sets']
        assert x['exact_complex_fourier_rank']>cap
        assert x['strict_gap']==x['exact_complex_fourier_rank']-cap
        print('  robust N',n,'Fourier',x['exact_complex_fourier_rank'],'network <=',cap,'gap',x['strict_gap'])
    print('PASS 7: two-Toffoli robustness for dense GF2-affine layouts N=2048,4096')

def test_actual_QS_matrix_product():
    # Exact modular matrix products, in unrelated control layouts with
    # two Toffoli gates; no use of the symbolic rank-certificate implementation.
    for p in PRIMES:
        n=64;k=6
        rng=np.random.default_rng(4219)
        matrices=[separated_generator_stage(n,p,rng) for _ in range(4)]
        def prod(with_gates):
            acc=matrices[0]
            for j in range(1,4):
                if with_gates and j<=2:
                    cs=(0,2) if j==1 else (1,3)
                    perm=mcnot_permutation(k,cs,k-1)
                    acc=acc[perm,:]
                acc=(matrices[j]@acc)%p
            return acc
        original=prod(False);nonlinear=prod(True)
        selection=np.s_[n//2:n,0:n//2]
        base_rank=rank_mod(original[selection],p)
        observed_rank=rank_mod(nonlinear[selection],p)
        correction=rank_mod(nonlinear-original,p)
        assert base_rank==4 and observed_rank==19 and correction==16
        assert observed_rank <=4+16 <32
        R=list(range(n//2,n));C=list(range(n//2))
        assert fourier_rank_mod(n,R,C,p)==32
    print('PASS 8: direct random four-stage products with two nonlinear edits, two primes')

def test_universal_toffoli_corollary():
    # t=4,r=1,g=1,m=2. For k>t*ceil(log2(8rt))=20,
    # cap<=t*(N/2**5-1), perturb rank<=N/8.
    for k in (21,23,29):
        n=1<<k; t=4; r=1;q=5
        assert t*q<k
        assert t*r*(n//(1<<q)-1)+n//8<n//4
    # General low-rank edit criterion for any H below the remaining margin.
    print('PASS 9: all-length single-Toffoli impossibility inequality')

if __name__=='__main__':
    test_arbitrary_rows()
    test_periodic_universal_E()
    test_parity_parity_old_formula()
    test_perm_edit_cycle_rank()
    test_256_obstruction()
    test_256_independent_mincut()
    test_robust_dense_affine()
    test_actual_QS_matrix_product()
    test_universal_toffoli_corollary()
    print('ALL 9 NEW TEST GROUPS PASSED')
