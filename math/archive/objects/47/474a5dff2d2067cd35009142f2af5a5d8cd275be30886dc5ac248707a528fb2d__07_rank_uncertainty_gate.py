"""Reproducible exact finite-field audits for two-sided Fourier tail-rank theorem.
THEOREM: if B=F_n C[:,perm], C invertible, lower rank(C)<=r1,
upper rank(B)<=r2, then for every t the last-t columns J=perm[-t:]
require r1+r2>=min(t,n-1-max(J)). The first-t output columns give
mirror bound r1_upper+r2_lower>=min(t,min(perm[:t])).
Proof uses exact subspace dimensions and Fourier Vandermonde kernels.
"""
from __future__ import annotations
import sys,random,json
from pathlib import Path
ROOT=Path(__file__).parent
from prior_loader import activate;activate();import _bootstrap
from dual_support import primitive_root
from triple_gate import modrank
from universal_gate import det

def matmul(A,B,p):
    return [[sum(A[i][k]*B[k][j] for k in range(len(B)))%p for j in range(len(B[0]))]
        for i in range(len(A))]

def permutation_profile(perm):
    n=len(perm)
    out=[]
    for t in range(1,n):
        upper=min(t,n-1-max(perm[-t:]))
        lower=min(t,min(perm[:t]))
        out.append(dict(t=t,upper_requirement=upper,lower_requirement=lower))
    return out

def audit(samples=12):
    rng=random.Random(20261009)
    total=0;reports=[]
    for n in (8,16,32,64):
        for p in (12289,65537):
            z=primitive_root(p,n)
            F=[[pow(z,i*k,p) for k in range(n)] for i in range(n)]
            choices=sorted(set([1,2,3,4,5,7,min(n-1,11)]))
            tested=0
            for t in choices:
                H=[[pow(z,r*k,p) for r in range(1,t+1)] for k in range(n)]
                # Fourier high t frequencies project to zero in first n-t rows.
                Y=matmul(F[:n-t],H,p)
                assert all(not v for row in Y for v in row)
                for a in (0,2,5,n//2,n-2):
                    ell=n-1-a
                    rankT=modrank(H[a+1:],p)
                    assert rankT==min(t,ell),(n,p,t,a,rankT)
                    tested+=1
                for _ in range(samples):
                    X=[[rng.randrange(p) for _ in range(t)] for _ in range(n)]
                    if modrank(X,p)!=t:continue
                    rx=modrank(matmul(F[:n-t],X,p),p)
                    a=rng.randrange(n)
                    ell=n-1-a
                    rt=modrank(X[a+1:],p) if ell else 0
                    assert rx+rt>=min(t,ell), (n,p,t,a,rx,rt)
                    tested+=1
            # Bottom left mirror: low t Fourier modes, F transform supported 0..t-1.
            for t in choices:
                H=[[pow(z,(-r*k)%(n),p) for r in range(t)] for k in range(n)]
                Y=matmul(F[t:],H,p)
                assert all(not v for row in Y for v in row)
                for a in (0,2,5,n//2,n-2):
                    assert (modrank(H[:a],p) if a else 0)==min(t,a)
                    tested+=1
            reports.append(dict(n=n,p=p,z=z,exact_checks=tested))
            total+=tested
            print(reports[-1],flush=True)
    P8=[7,0,6,3,4,1,2,5]
    assert max(max(x['upper_requirement'],x['lower_requirement']) for x in permutation_profile(P8))==2
    profiles=[]
    for n in (8,16,32,64):
        perm=P8 if n==8 else [n-1,0,n-2]+[k for k in range(1,n-1) if k not in (1,2,5,n-2)]+[1,2,5]
        assert sorted(perm)==list(range(n))
        profile=permutation_profile(perm)
        bound=max(max(x['upper_requirement'],x['lower_requirement']) for x in profile)
        row=dict(n=n,t3=profile[2],last_three=perm[-3:],total_rank_required=bound)
        profiles.append(row)
    assert [r['total_rank_required'] for r in profiles]==[2,3,3,3]
    print('Permutation profiles',profiles,flush=True)
    for n,p,expected in [(16,12289,1099),(16,65537,121),(32,12289,2858),(64,12289,4461)]:
        z=primitive_root(p,n)
        M=[[pow(z,r*k,p) for r in (1,2,3)] for k in (6,7,8)]
        assert det(M,p)==expected
    return dict(exact_finite_field_audits=reports,total_rank_checks=total,
                permutation_profiles=profiles,
                theorem='min(t,n-1-max(perm[-t:])) <= rank_lower(C)+rank_upper(B); min(t,min(perm[:t])) <= rank_upper(C)+rank_lower(B)',
                scope='B=F*C[:,perm], C invertible, B,C quasiseparable with given rank bounds; exact arbitrary complex coefficients; no runtime improvement.')

if __name__=='__main__':
    out=audit()
    (ROOT/'RANK_UNCERTAINTY_TESTS.json').write_text(json.dumps(out,indent=2)+'\n')
