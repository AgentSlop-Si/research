#!/usr/bin/env python3
"""Reviewer-owned checks. No uploaded module is imported or executed.
Run: python independent_offset_checks.py --output independent_results.json
Python 3 + NumPy. Exact Fraction checks are labelled separately from numerics.
"""
import argparse, cmath, hashlib, json, math
from fractions import Fraction as F
from pathlib import Path
import numpy as np


def grid(n, q):
    js = [(2*k*q+n)//(2*n) for k in range(n)]
    nums = [k*q-n*j for k,j in enumerate(js)]
    return js,nums


def constructive_classes(n,q):
    """Deterministic linear-time replacement for sort-based validation."""
    if n < 1 or q < n: raise ValueError('require q >= n >= 1')
    L=n//math.gcd(n,q)
    return [(r*q-n*((2*r*q+n)//(2*n)), list(range(r,n,L))) for r in range(L)]


def exact_rank(A):
    a=[list(map(F,row)) for row in A]; rank=0
    for c in range(len(a[0]) if a else 0):
        p=next((r for r in range(rank,len(a)) if a[r][c]),None)
        if p is None: continue
        a[rank],a[p]=a[p],a[rank]; v=a[rank][c]
        a[rank]=[x/v for x in a[rank]]
        for r in range(len(a)):
            if r != rank:
                t=a[r][c];a[r]=[x-t*y for x,y in zip(a[r],a[rank])]
        rank+=1
    return rank


def chev(x,R):
    row=[F(1)]
    if R>1: row.append(x)
    for _ in range(2,R):row.append(2*x*row[-1]-row[-2])
    return row


def unit_average(q,c):
    # Exact normalized Ramanujan sum, calculated by integer Mobius formula.
    g=math.gcd(q,c); h=q//g
    fac=[];t=h;p=2; square=False
    while p*p<=t:
        if t%p==0:
            t//=p;fac.append(p)
            if t%p==0:square=True
            while t%p==0:t//=p
        p+=1
    if t>1:fac.append(t)
    if square:return F(0)
    phi_h=h
    for p in fac:phi_h=phi_h//p*(p-1)
    return F((-1)**len(fac),phi_h)


def exact_covariance(q,m):
    ds=[set(u-t for t in range(m) if t!=u) for u in range(m)]
    return [[sum((unit_average(q,d*(j-i)) for d in ds[i%m]&ds[j%m]),F(0))/q
             for j in range(q)] for i in range(q)]


def matrix_product(a,b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))),F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def dft_matrix(n):
    return np.array([[cmath.exp(-2j*math.pi*k*t/n)/math.sqrt(n)
                      for t in range(n)] for k in range(n)])


def projected_operator(q,m,a,beta):
    # Direct block rank-one projection. No FFT/scan implementation used.
    P=np.zeros((q,q),complex)
    for r in range(q//m):
        s=np.array([cmath.exp(2j*math.pi*(a*(t*(t-1)//2)+(a*m*r+beta)*t)/q
                             +1j*math.pi*(q%2)*t/q) for t in range(m)])
        P[r*m:(r+1)*m,r*m:(r+1)*m]=np.outer(s.conj(),s)
    return P


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',default='independent_results.json')
    args=parser.parse_args();res={};count=0
    for n in range(1,201):
        qs=set(range(n,3*n+1)) if n<=50 else set()
        for p in (2,3,5,7):
            q=1
            while q<n:q*=p
            qs.add(q)
        for q in qs:
            js,nums=grid(n,q);L=n//math.gcd(n,q)
            assert len(set(nums))==L
            assert all(0<=j<q for j in js)
            assert all(js[k+1]>js[k] for k in range(n-1))
            assert all(-n<=2*num<n for num in nums)
            classes=constructive_classes(n,q)
            assert sum(len(ks) for _,ks in classes)==n
            assert all(nums[k]==num for num,ks in classes for k in ks)
            assert len(set(num for num,_ in classes))==L
            # Exact identity of frequency rationals, independent of roots.
            assert all(F(j,q)+F(num,n*q)==F(k,n) for k,(j,num) in enumerate(zip(js,nums)))
            count+=1
    res['exact_grid_cases']=count
    even=[F(k*9,6)-round(F(k*9,6)) for k in range(6)]
    res['ties_even_counterexample']={'N':6,'Q':9,'claimed_L':2,'actual_classes':list(map(str,sorted(set(even))))}
    assert len(set(even))==3
    exact=[]
    for q,m in [(4,2),(8,2),(9,3),(16,4),(25,5),(27,3),(32,4),(81,9)]:
        C=exact_covariance(q,m);C2=matrix_product(C,C)
        assert all(C2[i][j]==F(m,q)*C[i][j] for i in range(q) for j in range(q))
        trace=sum(C[i][i] for i in range(q));rank=int(trace/F(m,q))
        assert rank==q-q//m
        exact.append({'Q':q,'M':m,'projector_identity':'C^2=(M/Q) C exact','rank':rank})
    res['exact_covariance_certificates']=exact
    ranks=[]
    for n,R in [(127,8),(255,10),(511,12)]:
        q=n+1;js,nums=grid(n,q)
        # a=1 is a legal cycle: index-zero output is before/at the cut.
        later=list(dict.fromkeys(num for j,num in zip(js,nums) if j>0))[:R]
        rank=exact_rank([chev(F(2*num,n),R) for num in later]);assert rank==R
        ranks.append({'N':n,'Q':q,'R':R,'later_offset_numerators':later,'rank':rank})
    res['exact_post_cut_rank_certificates']=ranks
    numerical=[]
    for n,q,m in [(6,9,3),(7,8,2),(12,16,4),(18,27,3),(20,25,5)]:
        js,nums=grid(n,q);U=dft_matrix(q);V=dft_matrix(n)
        mod=np.array([[cmath.exp(-2j*math.pi*t*num/(n*q)) for t in range(n)] for num in nums])
        means=np.zeros((n,n),complex); covs=np.zeros((n,n,n),complex);states=0
        for a in range(1,q):
            if math.gcd(a,q)!=1:continue
            for beta in range(q):
                B=U@projected_operator(q,m,a,beta)
                T=math.sqrt(q/n)*B[js,:n]*mod
                E=T-V; means+=T
                for k in range(n):covs[k]+=np.outer(E[k].conj(),E[k])
                states+=1
        means/=states;covs/=states
        mean_error=float(np.max(np.abs(means-V)))
        bound=m/n;opmax=max(float(np.linalg.eigvalsh(C)[-1]) for C in covs)
        assert mean_error<1e-12
        assert opmax<=bound*(1+1e-11)
        # Exact modulation identity checked numerically too.
        identity_error=float(np.max(np.abs(math.sqrt(q/n)*U[js,:n]*mod-V)))
        assert identity_error<1e-12
        numerical.append({'N':n,'Q':q,'M':m,'states':states,
          'operator_mean_max_entry_error':mean_error,'max_covariance_eigenvalue':opmax,
          'variance_operator_bound':bound,'operator_bound_ratio':opmax/bound,
          'modulation_identity_max_error':identity_error})
    res['numerical_all_state_lift_operator_checks']=numerical
    res['status']='PASS';res['execution_scope']='Only this reviewer-owned script executed; uploaded source never imported or executed.'
    Path(args.output).write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
if __name__=='__main__':main()
