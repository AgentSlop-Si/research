#!/usr/bin/env python3
"""Independent finite-field spot checks of the sparse-preconditioned
separation-rank obstruction. No result over a finite field is used as a
proof of Chebotarev full-spark over C.

Uses only the Python standard library.
"""
from __future__ import annotations
import argparse, json, math, random


def isprime(n):
    if n<2:return False
    for d in [2,3,5,7,11,13,17,19,23,29,31,37]:
        if n%d==0:return n==d
    d=41
    while d*d<=n:
        if n%d==0:return False
        d+=2
    return True


def field_for_length(p):
    for k in range(1000000, 1020000, 2):
        q=p*k+1
        if isprime(q):
            for a in range(2,100):
                w=pow(a,k,q)
                if w!=1 and pow(w,p,q)==1:
                    return q,w
    raise RuntimeError('field not found')


def rank_mod(mat,q):
    if not mat:return 0
    a=[[v%q for v in row] for row in mat]
    n,m=len(a),len(a[0]); r=0
    for c in range(m):
        pivot=next((i for i in range(r,n) if a[i][c]),None)
        if pivot is None:continue
        a[r],a[pivot]=a[pivot],a[r]
        inv=pow(a[r][c],-1,q)
        a[r][c:]=[(v*inv)%q for v in a[r][c:]]
        for i in range(r+1,n):
            if a[i][c]:
                t=a[i][c]
                a[i][c:]=[(x-t*y)%q for x,y in zip(a[i][c:],a[r][c:])]
        r+=1
        if r==n:break
    return r


def make_cycle(n,rng):
    order=list(range(n));rng.shuffle(order)
    succ=[None]*n
    for i,a in enumerate(order):succ[a]=order[(i+1)%n]
    pos=[None]*n
    for i,a in enumerate(order):pos[a]=i
    return succ,pos


def weights_non_singular(n,q,rng,zeros):
    w=[rng.randrange(1,q) if not zeros or rng.randrange(5) else 0 for _ in range(n)]
    prod=1
    for x in w:prod=prod*x%q
    if prod==1:w[0]=0
    return w


def green_matrix(succ,weights,q):
    n=len(succ);prod=1
    for x in weights:prod=prod*x%q
    assert prod!=1
    inv=pow((1-prod)%q,-1,q)
    g=[[0]*n for _ in range(n)]
    for i in range(n):
        j=i;v=inv
        for _ in range(n):
            g[i][j]=v
            v=v*weights[j]%q
            j=succ[j]
        assert j==i
    return g


def green_branch(n,q,rng,zeros):
    succ,pos=make_cycle(n,rng)
    g=green_matrix(succ,weights_non_singular(n,q,rng,zeros),q)
    rm=list(range(n));cm=list(range(n));rng.shuffle(rm);rng.shuffle(cm)
    ls=[rng.randrange(1,q) for _ in range(n)]
    rs=[rng.randrange(1,q) for _ in range(n)]
    return (g,rm,cm,ls,rs,[pos[rm[i]] for i in range(n)],[pos[cm[i]] for i in range(n)])


def green_cell(branch,r,c,q):
    g,rm,cm,ls,rs,_,_=branch
    return ls[r]*g[rm[r]][cm[c]]*rs[c]%q


def simultaneous_asymmetric_halving(initial_r,initial_c,branches):
    r=initial_r[:];c=initial_c[:]
    for b in branches:
        aorder,border=b[-2],b[-1]
        h,k=len(r)//2,len(c)//2
        if not h or not k:return [],[]
        rr=sorted(r,key=lambda i:aorder[i]);cc=sorted(c,key=lambda j:border[j])
        low_r,high_r=rr[:h],rr[-h:]
        low_c,high_c=cc[:k],cc[-k:]
        if max(aorder[x] for x in low_r)<min(border[y] for y in high_c):
            r,c=low_r,high_c
        else:
            assert max(border[y] for y in low_c)<min(aorder[x] for x in high_r)
            r,c=high_r,low_c
        assert (max(aorder[i] for i in r)<min(border[j] for j in c) or
                max(border[j] for j in c)<min(aorder[i] for i in r))
    return r,c


def product_sparse(a,b,q):
    out=[]
    for row in a:
        acc={}
        for k,v in row.items():
            for j,w in b[k].items():
                acc[j]=(acc.get(j,0)+v*w)%q
        out.append({k:v for k,v in acc.items() if v})
    return out


def sparse_operator(n,q,rng,t):
    product=[{i:1} for i in range(n)]
    for layer in range(t):
        succ,_=make_cycle(n,rng)
        weights=weights_non_singular(n,q,rng,layer%2==0)
        a=[{i:1,succ[i]:(-weights[i])%q} for i in range(n)]
        if layer:
            perm=list(range(n));rng.shuffle(perm)
            gauge=[{perm[i]:rng.randrange(1,q)} for i in range(n)]
            product=product_sparse(gauge,product,q)
        product=product_sparse(a,product,q)
    return product


def experiment(p,t,Q,seed):
    rng=random.Random(seed)
    q,root=field_for_length(p)
    s=2**t
    branch=[green_branch(p,q,rng,zeros=(i%2==1)) for i in range(Q)]
    a=sparse_operator(p,q,rng,t)
    assert max(map(len,a))<=s
    rr=list(range(p));rng.shuffle(rr)
    r,c=simultaneous_asymmetric_halving(rr[:p//s],list(range(p)),branch)
    m=p//(s*(2**Q));nc=p//(2**Q)
    assert len(r)==m and len(c)==nc and s*m<=nc
    # Sparsity of A and the chosen P[R,S] minor.
    S=sorted(set(j for i in r for j in a[i]))
    a_sub=[[a[i].get(j,0) for j in S] for i in r]
    arank=rank_mod(a_sub,q)
    # Full-spark check at the extracted S,C submatrix, over an auxiliary field.
    # Not a substitute for the characteristic-zero Chebotarev theorem.
    roots=[pow(root,i,q) for i in range(p)]
    f_sc=[[roots[(u*v)%p] for v in c] for u in S]
    f_rank=rank_mod(f_sc,q)
    af_sc=[[sum(a[i][u]*roots[(u*v)%p] for u in a[i])%q for v in c] for i in r]
    af_rank=rank_mod(af_sc,q)
    h_sc=[[sum(green_cell(b,i,j,q) for b in branch)%q for j in c] for i in r]
    h_rank=rank_mod(h_sc,q)
    # Rank-one separated rectangles are tested individually.
    term_ranks=[rank_mod([[green_cell(b,i,j,q) for j in c] for i in r],q) for b in branch]
    assert all(x<=1 for x in term_ranks)
    assert arank==m
    assert f_rank==len(S)
    assert af_rank==m
    assert h_rank<=Q
    assert m>Q,(p,t,Q,m)
    return dict(p=p,t=t,Q=Q,field=q,row_support_limit=s,
                certified_rows=m,certified_columns=nc,actual_support_union=len(S),
                left_sparse_rank=arank,restricted_fourier_rank=f_rank,
                preconditioned_fourier_rank=af_rank,green_sum_rank=h_rank,
                summand_ranks=term_ranks)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--repetitions',type=int,default=4)
    ap.add_argument('--json',type=str)
    args=ap.parse_args()
    cases=[(13,0,2),(29,1,2),(53,2,2),(101,1,3),(131,2,3),(257,3,3)]
    report=[]
    for case in cases:
        for j in range(args.repetitions):
            report.append(experiment(*case,seed=10000+1000*j+case[0]+case[1]*7+case[2]*13))
    result={'cases':len(report),'runs':report,'status':'PASS',
            'disclaimer':'Finite-field spot checks; complex full-spark relies on Chebotarev theorem, not on numerical tests.'}
    if args.json:
        with open(args.json,'w',encoding='utf-8') as f:json.dump(result,f,indent=2)
    for p,t,Q in cases:
        print(f'p={p:3} sparse-prefix t={t}, terminal Q={Q}, '
              f'm={p//(2**(t+Q))}, certificate={"PASS"}')
    print('Exact finite-field experiments:',len(report),'PASS')

if __name__=='__main__':main()
