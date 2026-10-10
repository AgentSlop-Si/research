"""Exact Jacobian test for phase freedom in two weighted, noncommuting
Green resolvents.  Nonzero 4x4 Jacobian minor certifies local algebraic
dominance of a 2x5 Fourier cross-ratio map. NOT a Fourier factorization.
"""
from __future__ import annotations
import json
from phase40_holonomy import random_problem, normalize_gauge, weighted_green_apply

def dense_green(c,w,p):
    n=len(c);cols=[]
    for j in range(n):
        e=[0]*n;e[j]=1
        cols.append(weighted_green_apply(c,w,e,p))
    return [[cols[j][i] for j in range(n)] for i in range(n)]

def small_rank(A,p):
    A=[row[:] for row in A];r=0
    for j in range(len(A[0])):
        k=next((t for t in range(r,len(A)) if A[t][j]),None)
        if k is None:continue
        A[r],A[k]=A[k],A[r]
        d=pow(A[r][j],p-2,p)
        for t in range(r+1,len(A)):
            factor=A[t][j]*d%p
            for h in range(j,len(A[0])):
                A[t][h]=(A[t][h]-factor*A[r][h])%p
        r+=1
        if r==len(A):break
    return r

def jacobian(n,p,seed=40040):
    c,w=random_problem(n,p,seed)
    gauge=normalize_gauge(n,c,w,p)
    cn=[gauge['edge_weights'][j*n:(j+1)*n] for j in range(2)]
    gs=[dense_green(c[j],cn[j],p) for j in range(2)]
    M=[[(gs[0][i][j]+gs[1][i][j])%p for j in range(n)] for i in range(n)]
    assert all(M[r][j]!=0 for r in (0,1) for j in range(5))
    # R_j=M[0,j]*M[1,0]/(M[1,j]*M[0,0]), j=1,...,4.
    def dlog(j,edge):
        G=gs[edge.cycle];v,u=edge.target,edge.source
        def df(r,col):return G[r][v]*G[u][col]%p
        def term(r,col):return df(r,col)*pow(M[r][col],p-2,p)%p
        return (term(0,j)+term(1,0)-term(1,j)-term(0,0))%p
    # Tree weights are fixed 1. Non-tree weights are independent variables.
    J=[[dlog(j,gauge['edges'][k]) for k in gauge['chord']] for j in range(1,5)]
    return {'N':n,'prime':p,'chord_variables':n+1,
            'cross_ratios':4,'jacobian_rank':small_rank(J,p),
            'matrix_entries_nonzero':True,
            'matrix':J,'cycles':c,'weights':cn,'chords':gauge['chord']}

if __name__=='__main__':
    for p in (998244353,2013265921):
        for n in (8,16,32):
            a=jacobian(n,p)
            print(json.dumps({k:v for k,v in a.items() if k not in ('matrix','cycles','weights','chords')}))

def det_mod(A,p):
    a=[list(map(int,r)) for r in A];n=len(a);ans=1
    for j in range(n):
        i=next((r for r in range(j,n) if a[r][j]),None)
        if i is None:return 0
        if i!=j:a[i],a[j]=a[j],a[i];ans=(-ans)%p
        pivot=a[j][j];ans=ans*pivot%p
        inv=pow(pivot,p-2,p)
        for r in range(j+1,n):
            q=a[r][j]*inv%p
            for s in range(j+1,n):a[r][s]=(a[r][s]-q*a[j][s])%p
            a[r][j]=0
    return ans

def common_minor(n):
    import itertools
    p1,p2=998244353,2013265921
    x1=jacobian(n,p1);x2=jacobian(n,p2)
    assert x1['cycles']==x2['cycles'] and x1['chords']==x2['chords']
    for idx in itertools.combinations(range(n+1),4):
        A=[[r[k] for k in idx] for r in x1['matrix']]
        B=[[r[k] for k in idx] for r in x2['matrix']]
        a=det_mod(A,p1);b=det_mod(B,p2)
        if a and b:
            return {'N':n,'chord_indices':list(idx),
                    'edge_indices':[x1['chords'][k] for k in idx],
                    'modular_determinants':{str(p1):int(a),str(p2):int(b)},
                    'same_integer_weights_and_graphs':True,
                    'full_rank_4_over_char_zero_certified':True}
    raise AssertionError('No shared nonzero minor')
