#!/usr/bin/env python3
"""Dual-sweep and diagonal-gauge exact controls; no parameter search."""
from pathlib import Path
import json,random
HERE=Path(__file__).resolve().parent
p=97;rng=random.Random(9211)

def route(m):
    n=m*m;counts=[0]*(n+1);area=[(i//m+1)*(i%m+1) for i in range(n)]
    for a in area:counts[a]+=1
    offsets=[];v=0
    for c in counts:offsets.append(v);v+=c
    order=[0]*n
    for i,a in enumerate(area):order[offsets[a]]=i;offsets[a]+=1
    sigma=[0]*n
    for k,i in enumerate(order):sigma[i]=order[n-1-k]
    return sigma

def solve(x,m,q,transpose=False):
    n=m*m;y=[0]*n
    if not transpose:
        for i in range(n):
            t,u=divmod(i,m)
            y[i]=(x[i]+(pow(q,u,p)*y[i-m] if t else 0)+(y[i-1] if u else 0))%p
    else:
        for i in range(n-1,-1,-1):
            t,u=divmod(i,m)
            y[i]=(x[i]+(pow(q,u,p)*y[i+m] if t+1<m else 0)+(y[i+1] if u+1<m else 0))%p
    return y

def stage(x,m,q,alpha,beta,transpose=False):
    sigma=route(m);qi=pow(q,-1,p)
    a=solve(x,m,q,transpose)
    if not transpose:
        tmp=solve(x[::-1],m,qi);b=[tmp[i] for i in sigma]
    else:
        tmp=solve([x[i] for i in sigma],m,qi,True);b=tmp[::-1]
    return [(alpha*u+beta*v)%p for u,v in zip(a,b)]

def normalize(T,F,r,c):
    n=len(T)
    if any(T[r][j]==0 for j in range(n)) or any(T[i][c]==0 for i in range(n)):
        return {'status':'reference_zero_impossible','valid':False}
    E=[F[r][j]*pow(T[r][j],-1,p)%p for j in range(n)]
    D=[F[i][c]*pow(T[i][c]*E[c]%p,-1,p)%p for i in range(n)]
    U=[[D[i]*T[i][j]*E[j]%p for j in range(n)] for i in range(n)]
    assert D[r]==1 and U[r]==F[r] and all(U[i][c]==F[i][c] for i in range(n))
    mismatch=sum(U[i][j]!=F[i][j] for i in range(n) for j in range(n))
    cross_mismatch=0
    for i in range(n):
        for j in range(n):
            a=T[i][j]*T[r][c]*pow(T[i][c]*T[r][j]%p,-1,p)%p
            b=F[i][j]*F[r][c]*pow(F[i][c]*F[r][j]%p,-1,p)%p
            assert (U[i][j]==F[i][j])==(a==b)
            cross_mismatch+=a!=b
    assert mismatch==cross_mismatch
    return {'status':'normalized','valid':mismatch==0,'mismatches':mismatch,'cross_ratio_mismatches':cross_mismatch}

cases=[];gauge_controls=[]
for m,q in [(2,22),(4,8)]:
    n=m*m;assert pow(q,n,p)==1 and pow(q,n//2,p)!=1
    perm=list(range(n));rng.shuffle(perm);diag=[rng.randrange(1,p) for i in range(n)]
    def C(x,tr=False):
        if not tr:return [diag[i]*x[perm[i]]%p for i in range(n)]
        y=[0]*n
        for i,j in enumerate(perm):y[j]=diag[i]*x[i]%p
        return y
    F=[[pow(q,-i*j,p) for j in range(n)] for i in range(n)]
    for alpha,beta,gamma,delta in [(1,1,1,2),(0,1,1,2),(1,0,2,1),(1,-1,1,-1),(1,2,0,1),(1,1,1,0),(0,0,1,1),(1,1,0,0)]:
        def Tapply(x,tr=False):
            if not tr:return stage(C(stage(x,m,q,alpha,beta)),m,pow(q,-1,p),gamma,delta)
            return stage(C(stage(x,m,pow(q,-1,p),gamma,delta,True),True),m,q,alpha,beta,True)
        columns=[Tapply([int(i==j) for i in range(n)]) for j in range(n)]
        T=[[columns[j][i] for j in range(n)] for i in range(n)]
        x=[rng.randrange(p) for _ in range(n)];u=Tapply(x);v=Tapply(x,True)
        assert u==[sum(T[i][j]*x[j] for j in range(n))%p for i in range(n)]
        assert v==[sum(T[j][i]*x[j] for j in range(n))%p for i in range(n)]
        row0=Tapply([1]+[0]*(n-1),True);col0=Tapply([1]+[0]*(n-1))
        assert row0==T[0] and col0==[T[i][0] for i in range(n)]
        cases.append({'m':m,'N':n,'couplings':[alpha,beta,gamma,delta],
                      'forward_and_transpose_exact':True,'linear_cost_reference_extraction_matches_dense':True,
                      'normalization':normalize(T,F,0,0)})
    L=[rng.randrange(1,p) for _ in range(n)];R=[rng.randrange(1,p) for _ in range(n)]
    positive=[[F[i][j]*L[i]*R[j]%p for j in range(n)] for i in range(n)]
    assert normalize(positive,F,0,0)['valid']
    negative=[row[:] for row in positive];negative[-1][-1]=negative[-1][-1]*2%p
    assert normalize(negative,F,0,0)['mismatches']==1
    interior_zero=[row[:] for row in positive];interior_zero[-1][-1]=0
    assert normalize(interior_zero,F,0,0)['mismatches']==1
    for i,j in [(0,0),(0,n-1),(n-1,0)]:
        bad=[row[:] for row in positive];bad[i][j]=0
        assert normalize(bad,F,0,0)['status']=='reference_zero_impossible'
    gauge_controls.append({'N':n,'positive_rank_one_gauge':True,'single_entry_corruption_detected':True,
                           'interior_zero_detected':True,'three_reference_zero_branches_rejected':True})
result={'field':'F97','family_controls':cases,'gauge_controls':gauge_controls,
        'scope':'Exact controls for application and conditional diagonal normalization only; no Fourier construction search or parameter synthesis claim.'}
(HERE/'NORMALIZATION_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
