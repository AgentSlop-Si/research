"""Independent Phase 8 cross-checks, with direct modular reference DFTs.

Not a proof of asymptotic novelty. Includes random fresh inputs, exact matrix
identities, cyclotomic enumeration, and one large selected-bin reference.
"""
import json
import random
import time
from pathlib import Path
from phase8 import (fixture,roots_table,eval_radix2_remainder,
                    eval_generic_remainder,crt_bridge_certificate,
                    root_poly_mod,remainder_transfer,exhaustive_root_split,
                    enumerate_crt_transfer_supports,radix2_symbolic_merges,
                    unitary_entropy_audit,schur_cut_certificate,
                    dense_star,lut_gate_bound)

HERE=Path(__file__).resolve().parent

def direct_one(x,k,p,w):
    # Completely distinct input scanning implementation: sequential power update.
    accum=0;phase=1;step=pow(w,(-k)%len(x),p)
    for item in x:
        accum=(accum+item*phase)%p
        phase=phase*step%p
    return accum

def direct_vector(x,p,w):return [direct_one(x,k,p,w) for k in range(len(x))]

def independent_rank(M,p):
    a=[list(row) for row in M];r=0;m=len(a);n=len(a[0]) if a else 0
    for col in range(n):
        hit=None
        for i in range(r,m):
            if a[i][col]%p:
                hit=i;break
        if hit is None:continue
        a[r],a[hit]=a[hit],a[r]
        factor=pow(a[r][col],p-2,p)
        for row in range(r+1,m):
            if a[row][col]:
                q=a[row][col]*factor%p
                for j in range(col,n):
                    a[row][j]=(a[row][j]-q*a[r][j])%p
        r+=1
    return r

def independent_crt_factorization(n,p,w,split):
    m=n//2;B=tuple(j for j in range(n) if j not in split)
    roots=roots_table(n,p,w)
    RA=remainder_transfer(root_poly_mod(split,roots,p),p)
    RB=remainder_transfer(root_poly_mod(B,roots,p),p)
    # For every low/high monomial coefficient, verify its two remainders,
    # then evaluation using entirely direct Horner at every root.
    rng=random.Random(n+len(split))
    for _ in range(9):
        x=[rng.randrange(p) for _ in range(n)]
        low=x[:m];high=x[m:]
        L=[(low[i]+sum(RA[i][j]*high[j] for j in range(m)))%p for i in range(m)]
        R=[(low[i]+sum(RB[i][j]*high[j] for j in range(m)))%p for i in range(m)]
        for labels,poly in ((split,L),(B,R)):
            for k in labels:
                z=roots[-k%n]
                val=0
                for a in reversed(poly):val=(val*z+a)%p
                assert val==direct_one(x,k,p,w)
    diff=[[(RB[i][j]-RA[i][j])%p for j in range(m)] for i in range(m)]
    assert independent_rank(diff,p)==m
    return True


def main():
    start=time.time();rng=random.Random(17170008)
    complete=0;coeffs=0;ops=[]
    for n,reps in ((4,15),(8,15),(16,15),(32,15),(64,10),(128,10),(256,8)):
        p,w=fixture(n)
        for trial in range(reps):
            x=[rng.randrange(p) for _ in range(n)]
            got,ledger=eval_radix2_remainder(x,p,w)
            expect=direct_vector(x,p,w)
            assert got==expect,(n,trial)
            complete+=1;coeffs+=n
            if trial==0:
                ops.append({'n':n,'p':p,**ledger.record(),
                            'total_scalar_ops':ledger.adds+ledger.muls+ledger.root_prep_muls})

    partition_checks=0
    for n in (8,16,32):
        p,w=fixture(n)
        examples=[tuple(range(0,n,2)),tuple(range(n//2))]
        if n==16:examples += [(0,1,2,3,4,8,10,12), (0,1,2,4,5,7,11,14)]
        for split in examples:
            assert independent_crt_factorization(n,p,w,split)
            partition_checks+=1

    n=16;p,w=fixture(n)
    comparisons={}
    x=[rng.randrange(p) for _ in range(n)]
    reference=direct_vector(x,p,w)
    for policy in ('subgroup','contiguous','noncoset16'):
        got,ledger=eval_generic_remainder(x,p,w,policy)
        assert got==reference
        comparisons[policy]={**ledger.record(),'total_charged_scalar_ops':
                              ledger.adds+ledger.muls+ledger.root_prep_muls+
                              ledger.plan_adds+ledger.plan_muls}

    poly8=exhaustive_root_split(8)
    poly16=exhaustive_root_split(16)
    finite16=enumerate_crt_transfer_supports(16,p,w)
    # Check all class-16 balanced split differences independently, not only samples.
    from itertools import combinations
    roots=roots_table(16,p,w);all_rank_checks=0
    for A in combinations(range(16),8):
        B=tuple(j for j in range(16) if j not in A)
        if A>B:continue
        RA=remainder_transfer(root_poly_mod(A,roots,p),p)
        RB=remainder_transfer(root_poly_mod(B,roots,p),p)
        diff=[[(RB[i][j]-RA[i][j])%p for j in range(8)] for i in range(8)]
        assert independent_rank(diff,p)==8
        all_rank_checks+=1

    symbolic=[radix2_symbolic_merges(n,*fixture(n)) for n in (8,16,32,64)]
    entropy=[unitary_entropy_audit(n) for n in (8,16,32)]
    schur=[schur_cut_certificate(n,*fixture(n)) for n in (8,16,32)]
    star=[]
    for n in (8,16,32):
        p,w=fixture(n)
        M,count=dense_star(n,p)
        assert independent_rank(M,p)==n
        star.append({'n':n,'additive_gates':count,'all_entries_nonzero':all(v!=0 for row in M for v in row)})

    # Large exact execution, selected independent direct O(n)-per-bin references.
    n=65536;p,w=fixture(n)
    x=[rng.randrange(p) for _ in range(n)]
    got,ledger=eval_radix2_remainder(x,p,w)
    selected=sorted({0,1,2,3,n//2,n-1, *[rng.randrange(n) for _ in range(30)]})
    assert all(got[k]==direct_one(x,k,p,w) for k in selected)

    report={'date':'2026-10-10','result':'NO universal O(N) FFT',
            'new_regression_tests':13,
            'full_fresh_random_dfts':complete,'full_coefficients_independently_checked':coeffs,
            'large_n':n,'large_selected_bins_independently_checked':len(selected),
            'large_field_size':p,'large_ledger':ledger.record(),
            'independent_crt_factorization_cases':partition_checks,
            'all_balanced_16_splits_verified_bridge_full_rank':all_rank_checks,
            'cyclotomic_n8':poly8,'cyclotomic_n16':poly16,
            'finite_field_transfer_n16':finite16,
            'executor_scalar_ledger':ops,'root_division_cost_n16':comparisons,
            'symbolic_union':symbolic,'unitary_entropy_prior_art':entropy,
            'schur_sharpness':schur,'linear_dense_star_counterexample':star,
            'finite_field_truth_table': [lut_gate_bound(z,fixture(z)[0],table_exponent=3) for z in (16,64,256,1024)],
            'audit_seconds':round(time.time()-start,3)}
    (HERE/'AUDIT_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in (
        'full_fresh_random_dfts','full_coefficients_independently_checked',
        'large_n','large_selected_bins_independently_checked',
        'all_balanced_16_splits_verified_bridge_full_rank','audit_seconds')},indent=2))
    return report

if __name__=='__main__':main()
