"""Independently coded Phase-6 arithmetic audit.

Computes roots, Fourier tensor, finite-field rank and reference DFT from scratch.
Imports only the *candidate executor* / gauge constructor for oracle comparisons.
"""
import json
import random
from math import gcd
from pathlib import Path

import numpy as np
from phase6 import charged_two_axis_fft, endpoint_gauges, endpoint_sparse_core

HERE=Path(__file__).resolve().parent


def isprime(n):
    if n<2: return False
    for d in range(2,int(n**0.5)+1):
        if n%d==0:return False
    return True


def factor(n):
    out=[];k=2
    while k*k<=n:
        if n%k==0:
            out.append(k)
            while n%k==0:n//=k
        k+=1
    if n>1:out.append(n)
    return out


def field_root(n):
    for c in range(1,4000):
        p=c*n+1
        if not isprime(p):continue
        for g in range(2,p):
            w=pow(g,(p-1)//n,p)
            if all(pow(w,n//d,p)!=1 for d in factor(n)):
                return p,w
    raise RuntimeError(n)


def modular_rank(table,p):
    if not table:return 0
    a=[list(row) for row in table];n=len(a);m=len(a[0]);r=0
    for c in range(m):
        pr=None
        for i in range(r,n):
            if a[i][c]%p:
                pr=i;break
        if pr is None:continue
        a[r],a[pr]=a[pr],a[r]
        z=pow(a[r][c],p-2,p)
        for j in range(c,m):a[r][j]=(a[r][j]*z)%p
        for i in range(r+1,n):
            v=a[i][c]
            if v:
                for j in range(c,m): a[i][j]=(a[i][j]-v*a[r][j])%p
        r+=1
        if r==n:break
    return r


def direct_field_dft(signal,p,omega,frequency):
    n=len(signal)
    ratio=pow(omega,(-frequency)%n,p)
    z=1;result=0
    for value in signal:
        result=(result+value*z)%p
        z=z*ratio%p
    return result


def audit():
    rng=random.Random(172663)
    results={'status':'PASS','model':'exact Fp where p ≡ 1 mod N, plus float64 SVD checks',
             'raw_tensor_coefficients_checked':0,
             'independent_modular_rank_checks':0,
             'exact_sparse_core_coefficients_checked':0,
             'sparse_core_random_gauge_cases':0,
             'independent_arbitrary_dft_coefficients_checked':0,
             'spot_checked_large_output_coefficients':0,
             'fft_butterfly_counts':{},
             'matrix_cut_profiles':[],
             'unitary_singular_value_max_discrepancy':0.0,
             'warning':'No uniform sub-FFT upper bound, no new lower bound for unrestricted circuits'}
    for Q,M in [(2,2),(2,3),(3,2),(3,4),(4,3),(4,4),(6,4),(8,8)]:
        N=Q*M; p,w=field_root(N)
        f=lambda s,h,t,u:pow(w,-((h+M*s)*(t+Q*u))%N,p)
        # Three genuinely different unfoldings, directly from raw exponent.
        direct=[[f(s,h,t,u) for t in range(Q) for u in range(M)]
                 for s in range(Q) for h in range(M)]
        crossed=[[f(s,h,t,u) for h in range(M) for u in range(M)]
                  for s in range(Q) for t in range(Q)]
        alternate=[[f(s,h,t,u) for h in range(M) for t in range(Q)]
                    for s in range(Q) for u in range(M)]
        ranks=[modular_rank(X,p) for X in (direct,crossed,alternate)]
        assert ranks==[N,min(Q,M),N],(Q,M,ranks)
        results['raw_tensor_coefficients_checked']+=N*N
        results['independent_modular_rank_checks']+=3
        results['matrix_cut_profiles'].append({'Q':Q,'M':M,'N':N,'ranks':ranks,'field_prime':p})
        A,B,core=endpoint_sparse_core(Q,M,p,w)
        for a in range(Q):
            for h in range(M):
                for t in range(Q):
                    for b in range(M):
                        # Direct summation over both *external* basis coordinates.
                        observed=sum(A[a][s]*f(s,h,t,u)*B[b][u]
                                     for s in range(Q) for u in range(M))%p
                        expected=pow(w,-h*t%N,p) if a==t and b==h else 0
                        assert observed==expected==core[a][h][t][b]
                        results['exact_sparse_core_coefficients_checked']+=1
    for Q,M in [(2,3),(3,4),(4,4)]:
        N=Q*M;p,w=field_root(N)
        for _ in range(18):
            def sample(dim):
                while True:
                    a=[[rng.randrange(p) for j in range(dim)] for i in range(dim)]
                    if modular_rank(a,p)==dim:return a
            A=sample(Q);B=sample(M)
            core,P,R=endpoint_gauges(Q,M,p,w,A,B)
            count=sum(x!=0 for a in core for row in a for col in row for x in col)
            sP=sum(z!=0 for row in P for z in row)
            sR=sum(z!=0 for row in R for z in row)
            assert count==sP*sR>=N
            # Spot-check basis change from raw tensor, no use of endpoint factorization.
            for _ in range(12):
                a=rng.randrange(Q);h=rng.randrange(M);t=rng.randrange(Q);b=rng.randrange(M)
                brute=sum(A[a][s]*pow(w,-((h+M*s)*(t+Q*u))%N,p)*B[b][u]
                          for s in range(Q) for u in range(M))%p
                assert core[a][h][t][b]==brute
            results['sparse_core_random_gauge_cases']+=1
    for q,m in [(2,2),(2,4),(4,4),(4,8),(8,8),(16,16)]:
        N=q*m;p,w=field_root(N)
        for _ in range(7):
            x=[rng.randrange(p) for _ in range(N)]
            output,count=charged_two_axis_fft(x,q,m,p,w)
            assert count['butterflies']==(N//2)*(N.bit_length()-1)
            for k in range(N):
                assert direct_field_dft(x,p,w,k)==output[k],(N,k)
                results['independent_arbitrary_dft_coefficients_checked']+=1
        results['fft_butterfly_counts'][str(N)]={'butterflies':count['butterflies'],
                                                'butterflies_per_output':count['butterflies']/N,
                                                'central_nonzeros':N,
                                                'original_tensor_nonzeros':N*N}
    for N in (1024,4096,16384,65536):
        M=int(N**0.5)
        Q=N//M
        assert Q*M==N and Q==M
        p,w=field_root(N)
        x=[rng.randrange(p) for _ in range(N)]
        output,count=charged_two_axis_fft(x,Q,M,p,w)
        assert len(output)==N and count['butterflies']==N*(N.bit_length()-1)//2
        for k in rng.sample(range(N),16):
            assert output[k]==direct_field_dft(x,p,w,k)
            results['spot_checked_large_output_coefficients']+=1
        results['fft_butterfly_counts'][str(N)]={'butterflies':count['butterflies'],
                                                 'butterflies_per_output':count['butterflies']/N,
                                                 'central_nonzeros':N,
                                                 'original_tensor_nonzeros':N*N}
    # Exhaust all endpoint bases in GL(2,F_5): 480 × 480 = 230,400 pairs.
    # Algebraically evaluate supports of A F_2 and F_2 B^T directly.
    p=5; F=[[1,1],[1,4]]
    support_hist={}
    invertible_count=0
    for a00 in range(p):
        for a01 in range(p):
            for a10 in range(p):
                for a11 in range(p):
                    if (a00*a11-a01*a10)%p==0:
                        continue
                    invertible_count+=1
                    A=((a00,a01),(a10,a11))
                    count=sum((sum(A[i][k]*F[k][j] for k in range(2))%p)!=0
                              for i in range(2) for j in range(2))
                    support_hist[count]=support_hist.get(count,0)+1
    assert invertible_count==480 and support_hist=={2:32,3:256,4:192},support_hist
    endpoint_pair_hist={str(a*b):endpoint_pair_count for a,b,endpoint_pair_count in []}
    endpoint_pair_hist={}
    for ca,na in support_hist.items():
        for cb,nb in support_hist.items():
            k=str(ca*cb)
            endpoint_pair_hist[k]=endpoint_pair_hist.get(k,0)+na*nb
    assert sum(endpoint_pair_hist.values())==480**2
    assert endpoint_pair_hist['4']==1024
    results['exhaustive_GL2_F5_gauge_pairs']=480**2
    results['exhaustive_GL2_F5_minimum_support_pairs']=1024
    results['exhaustive_GL2_F5_support_histogram']=endpoint_pair_hist
    # Independent numeric partial-Fourier and 4-leg SVD (no module helpers).
    for q,m in [(2,3),(3,4),(4,4),(8,8)]:
        n=q*m
        U=np.array([[np.exp(-2j*np.pi*(h+m*s)*(t+q*u)/n)/np.sqrt(n)
                     for t in range(q) for u in range(m)]
                    for s in range(q) for h in range(m)]).reshape(q,m,q,m)
        cut=U.transpose(0,2,1,3).reshape(q*q,m*m)
        sing=np.linalg.svd(cut,compute_uv=False)
        partial=np.array([[np.exp(-2j*np.pi*h*t/n) for h in range(m)] for t in range(q)])
        ref=np.linalg.svd(partial,compute_uv=False)
        diff=np.max(abs(sing[:min(q,m)]-ref))
        assert diff<2e-12
        results['unitary_singular_value_max_discrepancy']=max(results['unitary_singular_value_max_discrepancy'],float(diff))
    (HERE/'AUDIT_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
    return results

if __name__=='__main__':
    print(json.dumps(audit(),indent=2))
