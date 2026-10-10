#!/usr/bin/env python3
"""Independent verification of dyadic-coset Fourier/Green cut theorem.
Requires numpy; all combinatorial certificates use exact integers.
Finite-field matrix ranks use exact modular Gaussian elimination.
"""
from __future__ import annotations
import json, math, random
from collections import defaultdict
import numpy as np


def rank_mod(rows, q):
    a=[list(map(lambda x:x%q,row)) for row in rows]
    if not a:return 0
    R,C=len(a),len(a[0]); rank=0
    for col in range(C):
        pivot=next((i for i in range(rank,R) if a[i][col]%q), None)
        if pivot is None:continue
        a[rank],a[pivot]=a[pivot],a[rank]
        inv=pow(a[rank][col],-1,q)
        for j in range(col,C):a[rank][j]=a[rank][j]*inv%q
        for i in range(rank+1,R):
            coeff=a[i][col]
            if coeff:
                for j in range(col,C):a[i][j]=(a[i][j]-coeff*a[rank][j])%q
        rank+=1
        if rank==R:break
    return rank


def primitive_root(q):
    p=q-1
    fs=[];n=p;d=2
    while d*d<=n:
        if n%d==0:
            fs.append(d)
            while n%d==0:n//=d
        d+=1
    if n>1:fs.append(n)
    return next(g for g in range(2,q) if all(pow(g,p//r,q)!=1 for r in fs))


def coset_spectrum(n,d):
    assert n%d==0 and 1<d<=n
    m=n//d;g=math.gcd(d,m)
    return sorted([1.0]*(m-m//g) + [math.sqrt(1-g/d)]*(m//g),reverse=True)


def all_exit_counts(n, edges):
    """Every directed coset cut at ALL binary scales in O(n+edges) time.
    For (u,v) edge, add +1 to its leaf and -1 at the LSB-trie LCA,
    then sum children upward. Node (r,a) has index (2**r-1)+a.
    Optional edge triple (u,v,is_active) skips zero weights.
    """
    assert n>=2 and n&(n-1)==0
    k=n.bit_length()-1
    diff=[0]*(2*n-1)
    tz=[0]*n
    for d in range(2,n,2):tz[d]=1+tz[d//2]
    active=0
    for e in edges:
        u,v=e[:2]
        if len(e)>2 and not e[2]: continue
        if u==v:raise ValueError('Not a Hamiltonian-cycle edge')
        t=tz[(u-v)%n]  # common low bits, lookup charged at O(n) preprocessing
        lca=(1<<t)-1+(u% (1<<t))
        leaf=n-1+u
        diff[leaf]+=1
        diff[lca]-=1
        active+=1
    for r in range(k,0,-1):
        start=(1<<r)-1
        parent=(1<<(r-1))-1
        mask=(1<<(r-1))-1
        for a in range(1<<r):
            diff[parent+(a&mask)]+=diff[start+a]
    assert diff[0]==0
    return diff,active


def random_cycle(n,rng):
    order=list(range(n));rng.shuffle(order)
    p=[0]*n
    for j,u in enumerate(order):p[u]=order[(j+1)%n]
    return p


def exact_green_matrix(perm, weights, q):
    n=len(perm)
    lam=1
    for w in weights:lam=lam*w%q
    assert lam!=1
    inv=pow((1-lam)%q,-1,q)
    g=[[0]*n for _ in range(n)]
    for i in range(n):
        j=i;v=inv
        for t in range(n):
            g[i][j]=v
            v=v*weights[j]%q
            j=perm[j]
        assert j==i
    return g


def matmul(a,b,q):
    n=len(a);z=[[0]*n for _ in range(n)]
    for i in range(n):
        for k in range(n):
            if a[i][k]:
                for j in range(n):z[i][j]=(z[i][j]+a[i][k]*b[k][j])%q
    return z


def subrank(a,S,T,q):return rank_mod([[a[i][j] for j in T] for i in S],q)


def run():
    rng=random.Random(20261010)
    result={'seed':20261010,'numeric_singular_spectra':0,'numeric_max_abs_error':0.0,
            'trie_bruteforce_cut_tests':0,'finite_field_green_cross_ranks':0,
            'finite_field_two_stage_bound_checks':0,'finite_field_fourier_coset_ranks':0,
            'example':{},'word_ram_certificate_complexity':'O(n + E)'}
    for n in (8,12,16,18,20,24,28,32,36,40,48,60,64,72):
        omega=np.exp(-2j*np.pi/n)
        U=omega**(np.arange(n)[:,None]*np.arange(n)[None,:])/np.sqrt(n)
        for d in range(2,n+1):
            if n%d:continue
            m=n//d
            for a in {0,1% d,(d//2)%d}:
                A=[a+d*j for j in range(m)]
                outside=[j for j in range(n) if j not in set(A)]
                sigma=np.linalg.svd(U[np.ix_(A,outside)],compute_uv=False)
                pred=coset_spectrum(n,d)
                diff=max(abs(x-y) for x,y in zip(sorted(sigma,reverse=True),pred)) if m else 0
                result['numeric_max_abs_error']=max(diff,result['numeric_max_abs_error'])
                assert diff<2e-11,(n,d,a,sigma,pred,diff)
                result['numeric_singular_spectra']+=1
    for n in (8,16,32,64,128):
        k=n.bit_length()-1
        for trial in range(10):
            e=[]
            for j in range(1+rng.randrange(1,6)):
                p=random_cycle(n,rng)
                e.extend((u,p[u],rng.randrange(5)!=0) for u in range(n))
            got,act=all_exit_counts(n,e)
            assert act==sum(int(ei[2]) for ei in e)
            for r in range(k+1):
                for a in range(1<<r):
                    brute=sum(1 for u,v,z in e if z and u%(1<<r)==a and v%(1<<r)!=a)
                    assert got[(1<<r)-1+a]==brute,(n,trial,r,a,brute,got[(1<<r)-1+a])
                    result['trie_bruteforce_cut_tests']+=1
    for n,q in ((8,97),(16,97),(32,97)):
        generator=primitive_root(q)
        omega=pow(generator,(q-1)//n,q)
        F=[[pow(omega,i*j,q) for j in range(n)] for i in range(n)]
        for d in (2,4,8):
            if n%d:continue
            m=n//d;g=math.gcd(d,m)
            predicted=m if g<d else m-m//g
            for a in range(d):
                A=[a+d*j for j in range(m)]
                B=[j for j in range(n) if j not in set(A)]
                assert subrank(F,A,B,q)==predicted,(n,q,d,a)
                result['finite_field_fourier_coset_ranks']+=1
        for trial in range(7):
            GG=[];edges=[];perm_list=[]
            for z in range(4):
                p=random_cycle(n,rng)
                w=[rng.randrange(q) for _ in range(n)]
                if math.prod(w)%q==1:w[0]=0
                G=exact_green_matrix(p,w,q)
                perm_list.append(p);GG.append(G)
                edges.extend((u,p[u],w[u]!=0) for u in range(n))
                for r in range(1,n.bit_length()):
                    d=1<<r; a=rng.randrange(d)
                    A=[a+d*j for j in range(n//d)]
                    B=[j for j in range(n) if j not in set(A)]
                    crossing=sum(w[u]!=0 and p[u] not in A for u in A)
                    assert subrank(G,A,B,q)==crossing,(n,q,trial,z,r,a)
                    result['finite_field_green_cross_ranks']+=1
            stageA=[[(GG[0][i][j]+GG[1][i][j])%q for j in range(n)] for i in range(n)]
            stageB=[[(GG[2][i][j]+GG[3][i][j])%q for j in range(n)] for i in range(n)]
            M=matmul(stageA,stageB,q)
            cuts,_=all_exit_counts(n,edges)
            for r in range(1,n.bit_length()):
                d=1<<r
                for a in range(d):
                    A=[a+d*j for j in range(n//d)]
                    B=[j for j in range(n) if j not in set(A)]
                    budget=cuts[d-1+a]
                    rankM=subrank(M,A,B,q)
                    assert rankM<=budget,(n,trial,r,a,rankM,budget)
                    result['finite_field_two_stage_bound_checks']+=1
    # Multi-scale p-adic mixing identity: sum of all dyadic coset exits
    # equals sum over edges of the number of scales they cross.
    result['multiscale_identity_cases']=0
    for n in (16,32,64,128):
        k=n.bit_length()-1
        R=k//2
        for trial in range(6):
            ed=[]
            for _ in range(4):
                p=random_cycle(n,rng)
                ed.extend((u,p[u],rng.randrange(7)!=0) for u in range(n))
            cut,_=all_exit_counts(n,ed)
            left=sum(max(0,R-(((u^v)&-(u^v)).bit_length()-1)) for u,v,z in ed if z)
            right=sum(cut[(1<<r)-1+a] for r in range(1,R+1) for a in range(1<<r))
            assert left==right,(n,trial,left,right)
            result['multiscale_identity_cases']+=1
    # Explicit sharp nonexpanding family: each parity class occupies a single run of the cycles
    n=64; A=list(range(0,n,2)); B=list(range(1,n,2))
    order=A+B
    perm={order[j]:order[(j+1)%n] for j in range(n)}
    ed=[(u,perm[u],True) for u in range(n)]*4
    counts,_=all_exit_counts(n,ed)
    d=2;m=n//2;g=math.gcd(d,m)
    cut_budget=counts[d-1]  # even coset a=0
    exact_required=m-m//g
    assert cut_budget==4 and exact_required==16
    result['example']={'n':64,'coset':'even indices','two_stages_two_green_terms_each':True,
                       'green_branches':4,'budget':cut_budget,'exact_fourier_rank':exact_required,
                       'certified_operator_norm_error_at_least':1.0}
    return result

if __name__=='__main__':
    r=run()
    with open('fft_dyadic_green_20261010/RESULTS.json','w') as f:json.dump(r,f,indent=2)
    print(json.dumps(r,indent=2))
