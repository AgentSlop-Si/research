"""Independent Phase 9 audit: direct polynomial evaluation, Cauchy solves,
random raw inputs, exact large split, and fully charged DFT comparison.
No external Python packages. Earlier-stage checks are run separately.
"""
import itertools
import json
import math
import random
import time
from pathlib import Path
from phase9 import (fixture,ExchangeBridge,AdaptiveExchangeBridge,Ledger,
                    correction_rank_certificate,combined_scalar_cost,
                    full_dft_via_hybrid_children,classical_dif_fft)

HERE=Path(__file__).resolve().parent

def direct_eval(a,z,p):
    s=0
    for v in reversed(a):s=(s*z+v)%p
    return s

def eval_at_raw_root(x,k,p,w):
    n=len(x)
    z=pow(w,(-k)%n,p)
    return direct_eval(x,z,p)

def check_full_remainder(x,bridge):
    n=bridge.n;m=n//2;p=bridge.p;w=bridge.w
    a,b=bridge.pair(x[:m],x[m:])
    for group,v in ((bridge.A,a),(bridge.B,b)):
        for k in group:
            z=pow(w,(-k)%n,p)
            assert direct_eval(v,z,p)==eval_at_raw_root(x,k,p,w)
    return a,b

def scalar(snapshot):
    return sum(snapshot.get(k,0) for k in ('plan_muls','plan_adds','online_muls','online_adds'))

def independently_rank(M,p):
    W=[row.copy() for row in M]
    if not W:return 0
    rows=len(W);cols=len(W[0]);r=0
    for col in range(cols):
        pivot=None
        for rr in range(r,rows):
            if W[rr][col]%p:
                pivot=rr;break
        if pivot is None:continue
        W[pivot],W[r]=W[r],W[pivot]
        q=pow(W[r][col],p-2,p)
        for rr in range(r+1,rows):
            c=(W[rr][col]*q)%p
            if c:
                for j in range(col,cols):
                    W[rr][j]=(W[rr][j]-c*W[r][j])%p
        r+=1
        if r==rows:break
    return r

def audit():
    start=time.perf_counter()
    rng=random.Random(17170009)
    complete=0;checked=0;recovered=0;hybrid_full=0
    samples=[]
    for n,reps in ((4,12),(8,12),(16,12),(32,12),(64,8),(128,4)):
        p,w=fixture(n)
        for j in range(reps):
            A=rng.sample(list(range(n)),n//2)
            bridge=AdaptiveExchangeBridge(n,p,w,A)
            x=[rng.randrange(p) for _ in range(n)]
            a,b=check_full_remainder(x,bridge.bridge)
            # In independent check, bridge internal ordering may be reversed,
            # but its partition still covers every root, so count all N checks.
            lo,hi=bridge.bridge.invert_pair(a,b)
            assert lo+hi==x
            complete+=1;checked+=n;recovered+=1
        if n<=64:
            for i in range(3):
                a=[rng.randrange(p) for _ in range(n//2)]
                bridge=AdaptiveExchangeBridge(n,p,w,rng.sample(list(range(n)),n//2))
                x=[rng.randrange(p) for _ in range(n)]
                out,cost=full_dft_via_hybrid_children(x,bridge.bridge)
                target,baseline=classical_dif_fft(x,p,w)
                assert out==target
                hybrid_full+=1
                if not i:
                    samples.append({'n':n,'swaps':bridge.effective_swaps,
                                    'total_hybrid_scalar_work':combined_scalar_cost(cost),
                                    'classical_radix2_scalar_work':scalar(baseline.snapshot())})

    rank_cases=0
    for n in (4,8,16,32,64):
        p,w=fixture(n);m=n//2
        for t in range(m+1):
            for rep in range(2 if n<=32 else 1):
                e=rng.sample(list(range(0,n,2)),t)
                o=rng.sample(list(range(1,n,2)),t)
                b=ExchangeBridge(n,p,w,e,o)
                cert=correction_rank_certificate(b)
                assert cert['joint_rank']==min(m,2*t)
                rank_cases+=1

    # Reflection/commutator theorem verified with an independent rank routine.
    commutator_cases=0
    for n in (4,8,16,32):
        p,w=fixture(n);m=n//2
        I=[[int(i==j) for j in range(m)] for i in range(m)]
        def mm(A,B):
            return [[sum(A[i][k]*B[k][j] for k in range(m))%p
                     for j in range(m)] for i in range(m)]
        for t in range(m+1):
            e=rng.sample(list(range(0,n,2)),t)
            o=rng.sample(list(range(1,n,2)),t)
            b=ExchangeBridge(n,p,w,e,o)
            RA=[[0]*m for _ in range(m)]
            RB=[[0]*m for _ in range(m)]
            for j in range(m):
                h=[0]*m;h[j]=1
                out_a,out_b=b.pair([0]*m,h)
                for i in range(m):
                    RA[i][j]=out_a[i];RB[i][j]=out_b[i]
            AB=mm(RA,RB);BA=mm(RB,RA)
            target=2*min(t,m-t)
            assert mm(RA,RA)==I and mm(RB,RB)==I
            for M,k in (
                ([[(RA[i][j]-RB[i][j])%p for j in range(m)] for i in range(m)],m),
                ([[(RA[i][j]+RB[i][j])%p for j in range(m)] for i in range(m)],target),
                ([[(AB[i][j]-BA[i][j])%p for j in range(m)] for i in range(m)],target),
                ([[(AB[i][j]+I[i][j])%p for j in range(m)] for i in range(m)],target),
            ):
                assert independently_rank(M,p)==k,(n,t,k)
            commutator_cases+=1

    # Independent exhaustive combinatorial histogram for N=16.
    m=8
    swaps=[0]*(m+1)
    for A in itertools.combinations(range(2*m),m):
        swaps[sum(k%2 for k in A)]+=1
    assert swaps==[math.comb(m,t)**2 for t in range(m+1)]

    # Fully charged arithmetic growth of the one-swap child transfer.
    scale=[]
    large=None
    for n in (256,1024,4096,16384,65536):
        p,w=fixture(n);m=n//2
        b=ExchangeBridge(n,p,w,[0],[1])
        x=[rng.randrange(p) for _ in range(n)]
        a,c=b.pair(x[:m],x[m:])
        L1=b.online_ledger()
        lo,hi=b.invert_pair(a,c)
        assert lo+hi==x
        L2=b.online_ledger()
        # Correctness spot-check: evaluate both child remainders at roots,
        # compare directly with polynomial evaluations of original fresh x.
        chosen=sorted({0,1,2,3,n-1,n//2, *[rng.randrange(n) for _ in range(24)]})
        for k in chosen:
            z=pow(w,(-k)%n,p)
            child=a if k in b.A else c
            assert direct_eval(child,z,p)==direct_eval(x,z,p)
        row={'n':n,'t':1,
             'plan_scalar':scalar(b.plan_ledger),
             'plan_inversions':b.plan_ledger['plan_invs'],
             'forward_scalar':scalar(L1),
             'inverse_scalar':scalar(L2)-scalar(L1),
             'selected_coefficients_checked':len(chosen),
             'plan_plus_forward':scalar(b.plan_ledger)+scalar(L1)}
        scale.append(row)
        if n==65536:large=row

    # Full 65,536-point exact DFT through the exotic split. This still
    # invokes conventional half-size FFTs and remains O(N log N).
    n=65536;p,w=fixture(n);m=n//2
    raw=[rng.randrange(p) for _ in range(n)]
    bridge=ExchangeBridge(n,p,w,[0],[1])
    got,hybrid_ledgers=full_dft_via_hybrid_children(raw,bridge)
    reference,ref_log=classical_dif_fft(raw,p,w)
    assert got==reference
    chosen=sorted({0,1,2,3,n//2,n-1,*[rng.randrange(n) for _ in range(32)]})
    for k in chosen:
        assert got[k]==eval_at_raw_root(raw,k,p,w)

    # Comparison with Phase 8's explicit non-coset direct-division routine,
    # for the SAME root split (t=2, N=16). Optional only when source present.
    predecessor=None
    try:
        import sys
        sys.path.insert(0,str(HERE.parent/'hero17_phase8_multistage'))
        from phase8 import eval_generic_remainder
        n=16;p,w=fixture(n)
        x=[rng.randrange(p) for _ in range(n)]
        split=(0,1,2,3,4,8,10,12)
        b=AdaptiveExchangeBridge(n,p,w,split)
        y,log=full_dft_via_hybrid_children(x,b.bridge)
        z,older=eval_generic_remainder(x,p,w,policy='noncoset16')
        assert y==z
        predecessor={'n':16,'root_set_A':list(split),'swaps':b.effective_swaps,
                     'this_hybrid_scalar':combined_scalar_cost(log),
                     'phase8_naive_polynomial_division_scalar':older.adds+older.muls+older.plan_adds+older.plan_muls+older.root_prep_muls,
                     'classical_radix2_scalar':scalar(classical_dif_fft(x,p,w)[1].snapshot())}
    except ImportError:pass

    report={
        'date':'2026-10-10',
        'status':'NO universal O(N) FFT; one-split rank-t bridge O(tN) after charged prep',
        'phase9_test_groups':15,
        'independent_full_child_remainder_pairs':complete,
        'full_root_evaluations_independently_checked':checked,
        'inverse_pairs_checked':recovered,
        'hybrid_full_dfts_checked_small':hybrid_full,
        'independent_correction_rank_checks':rank_cases,
        'independent_involution_commutator_rank_cases':commutator_cases,
        'all_balanced_n16_splits_histogram_by_t':swaps,
        'all_balanced_n16_splits_total':sum(swaps),
        'single_swap_scaling':scale,
        'large_65536_dft_all_bins_verified_against_classical':True,
        'large_65536_dft_selected_bins_checked_directly':len(chosen),
        'large_hybrid_including_plan_scalar':combined_scalar_cost(hybrid_ledgers),
        'large_classical_including_plan_scalar':scalar(ref_log.snapshot()),
        'smaller_comparisons':samples,
        'same_split_phase8_comparison':predecessor,
        'audit_seconds':round(time.perf_counter()-start,3)}
    (HERE/'AUDIT_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('independent_full_child_remainder_pairs',
        'full_root_evaluations_independently_checked',
        'hybrid_full_dfts_checked_small',
        'independent_correction_rank_checks',
        'independent_involution_commutator_rank_cases',
        'all_balanced_n16_splits_total',
        'large_65536_dft_selected_bins_checked_directly',
        'audit_seconds')},indent=2))
    return report

if __name__=='__main__':audit()
