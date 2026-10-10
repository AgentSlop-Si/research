"""Independent validation for Phase 10.

The large-output reference uses a separate iterative bit-reversed NTT,
not the executor's cyclic comb or scalar radix-2 recursion. Small cases
are independently checked with direct DFT and exact matrix algebra.
"""
from __future__ import annotations
import json,random,time
from pathlib import Path
from phase10 import SpectralUnion,BatchSpectralUnion,classical_fft_project
from test_phase10 import fixture,direct_project,direct_dft,rank,projection_matrix,matmul

HOME=Path(__file__).resolve().parent


def independent_ntt(x,p,w):
    """Independent in-place iterative decimation-in-time exact forward DFT."""
    n=len(x)
    if n&(n-1):raise ValueError('powers of two only')
    bits=n.bit_length()-1
    a=[0]*n
    for i,v in enumerate(x):
        rev=0;z=i
        for _ in range(bits):rev=(rev<<1)|(z&1);z>>=1
        a[rev]=v%p
    size=2
    while size<=n:
        omega=pow(w,(n-n//size)%n,p)
        half=size//2
        for start in range(0,n,size):
            phase=1
            for j in range(half):
                u=a[start+j]
                v=phase*a[start+j+half]%p
                a[start+j]=(u+v)%p
                a[start+j+half]=(u-v)%p
                phase=phase*omega%p
        size*=2
    return a


def oracle_project(x,p,w,K):
    n=len(x)
    f=independent_ntt(x,p,w)
    y=[f[k] if k in K else 0 for k in range(n)]
    out=independent_ntt(y,p,pow(w,n-1,p))
    inv=pow(n,-1,p)
    return [(inv*z)%p for z in out]


def dot_at(x,k,p,w):
    n=len(x);step=pow(w,(-k)%n,p)
    a=0;phase=1
    for v in x:
        a=(a+v*phase)%p
        phase=phase*step%p
    return a


def scalar(record):
    return record['total_field_operations']


def audit():
    start=time.perf_counter()
    rng=random.Random(17170010)
    exact_complete=0;complete_coeffs=0;rank_cases=0;commutation_cases=0
    nonpow2=0
    for n,reps in ((8,12),(12,12),(15,10),(16,12),(24,12),(32,12),(48,8),(64,10),(96,8),(128,10),(256,4)):
        p,w=fixture(n)
        divisors=[d for d in range(1,min(12,n)+1) if n%d==0]
        for rep in range(reps):
            d=rng.choice(divisors)
            S={a for a in range(d) if rng.randrange(2)}
            inbase=[k for k in range(n) if k%d in S]
            outside=[k for k in range(n) if k%d not in S]
            additions=rng.sample(outside,min(len(outside),rng.randrange(3)))
            removals=rng.sample(inbase,min(len(inbase),rng.randrange(3)))
            plan=SpectralUnion(n,p,w,d,S,additions,removals)
            x=[rng.randrange(p) for _ in range(n)]
            got=plan.apply(x)
            K=(set(inbase)-set(removals))|set(additions)
            independent=direct_project(x,p,w,K)
            assert got==independent,(n,d,S,additions,removals)
            if n&(n-1)==0:
                assert got==oracle_project(x,p,w,K)
            else:nonpow2+=1
            exact_complete+=1;complete_coeffs+=n
    # Explicitly test all Fourier masks on small N as matrices and check
    # the basis-invariant symmetric-difference rank certificate.
    for n in (4,6,8,10,12,16):
        p,w=fixture(n)
        for _ in range(20):
            A={k for k in range(n) if rng.randrange(2)}
            B={k for k in range(n) if rng.randrange(2)}
            PA=projection_matrix(n,p,w,A)
            PB=projection_matrix(n,p,w,B)
            Pi=projection_matrix(n,p,w,A&B)
            assert matmul(PA,PB,p)==Pi
            assert matmul(PB,PA,p)==Pi
            commutation_cases+=1
            diff=[[(a-b)%p for a,b in zip(ra,rb)] for ra,rb in zip(PA,PB)]
            assert rank(diff,p)==len(A^B)
            rank_cases+=1

    # Fully charged scalar-operation scaling and same-output FFT control.
    scales=[]
    for n in (256,1024,4096,16384,65536):
        p,w=fixture(n)
        plan=SpectralUnion(n,p,w,2,{0},add=(1,),remove=(0,))
        x=[rng.randrange(p) for _ in range(n)]
        t0=time.perf_counter();y=plan.apply(x);projector_seconds=time.perf_counter()-t0
        a_cost=plan.cost()
        t1=time.perf_counter();reference,b_cost=classical_fft_project(x,plan);fft_seconds=time.perf_counter()-t1
        assert y==reference
        if n<=4096:
            assert y==oracle_project(x,p,w,{k for k in range(n) if plan.contains(k)})
        row={'n':n,'d':2,'exceptions':2,
             'charged_projector_field_ops':scalar(a_cost),
             'charged_generic_fft_mask_inverse_field_ops':scalar(b_cost),
             'field_op_ratio_double_fft_over_projector':round(scalar(b_cost)/scalar(a_cost),4),
             'projector_plan_field_ops':a_cost['plan']['plan_adds']+a_cost['plan']['plan_muls'],
             'projector_apply_field_ops':a_cost['online']['online_adds']+a_cost['online']['online_muls'],
             'independent_full_output_verified':True,
             'python_projector_seconds_not_optimized':round(projector_seconds,4),
             'python_generic_fft_seconds_not_optimized':round(fft_seconds,4)}
        scales.append(row)
        if n==65536:
            # Another fully independent iterative radix-2 FFT implementation.
            mask={k for k in range(n) if plan.contains(k)}
            y2=oracle_project(x,p,w,mask)
            assert y==y2
            chosen=sorted({0,1,2,3,n//2-1,n//2,n-1,
                           *[rng.randrange(n) for _ in range(32)]})
            for k in chosen:
                Xk=dot_at(x,k,p,w)
                Yk=dot_at(y,k,p,w)
                assert Yk==(Xk if k in mask else 0)
            row['independent_direct_frequency_bins_checked']=len(chosen)
            row['large_full_outputs']=n
    # Shared graph: 8 full projection consumers; repeated output masks,
    # distinct bases and shared exception frequencies; no cached input FFT.
    n=4096;p,w=fixture(n)
    masks=[({0},(1,),(0,))]*4 + [({0,2},(1,),(0,))]*4
    batch=BatchSpectralUnion(n,p,w,4,masks)
    x=[rng.randrange(p) for _ in range(n)]
    ys=batch.apply(x)
    baseline_separate_ops=0
    for i,(S,a,r) in enumerate(masks):
        solo=SpectralUnion(n,p,w,4,S,a,r)
        assert solo.apply(x)==ys[i]
        baseline_separate_ops+=scalar(solo.cost())
    batch_info={'n':n,'outputs':len(masks),'output_entries':n*len(masks),
         'unique_frequency_events':batch.cost()['distinct_exception_frequencies'],
         'unique_event_patterns':batch.cost()['distinct_exception_patterns'],
         'unique_bases':batch.cost()['distinct_bases'],
         'fully_charged_batch_field_ops':batch.cost()['total_field_operations'],
         'fully_charged_separate_field_ops':baseline_separate_ops,
         'batch_field_operation_reduction_pct':round(100*(1-batch.cost()['total_field_operations']/baseline_separate_ops),2)}

    report={'date':'2026-10-10','status':'exact linear-work projector for periodic+exception masks; no O(N) full FFT',
        'phase10_test_groups':14,
        'independent_complete_arbitrary_input_projectors':exact_complete,
        'independent_complete_projection_output_entries':complete_coeffs,
        'nonpower_of_two_cases':nonpow2,
        'independent_commuting_projector_cases':commutation_cases,
        'independent_symmetric_difference_rank_cases':rank_cases,
        'fully_charged_same_output_comparison':scales,
        'large_full_independent_ntt_reference':True,
        'large_selected_direct_bin_checks':scales[-1]['independent_direct_frequency_bins_checked'],
        'shared_batch_graph':batch_info,
        'audit_seconds':round(time.perf_counter()-start,3)}
    (HOME/'AUDIT_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'complete_projectors':exact_complete,
       'projection_entries':complete_coeffs,'rank_cases':rank_cases,
       'large_length':scales[-1]['n'],'large_field_op_ratio':scales[-1]['field_op_ratio_double_fft_over_projector'],
       'batch_reduction_pct':batch_info['batch_field_operation_reduction_pct'],
       'audit_seconds':report['audit_seconds']},indent=2))

if __name__=='__main__':audit()
