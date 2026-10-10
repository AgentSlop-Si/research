"""Exact two-Weyl-intertwiner middle-monomial gate for fixed outer matrices.

Given invertible A,B, decide if A*(diagonal*permutation)*B intertwines BOTH
T<->V. For generic cases signatures uniquely determine the only candidate
permutation; for duplicate signatures a bounded exhaustive fallback is used.
Never labels an unsearched large case impossible.
"""
from __future__ import annotations
from collections import Counter,defaultdict
from itertools import permutations,product
from math import factorial
from field_core import P,conjugate_pair,monomial,matmul,defect_count


def vertex_signatures(pair):
    X,Y=pair;n=len(X)
    # Diagonal similarity invariant under one common gauge, permutes vertices.
    # Cross-operators make this stronger than checking either operator alone.
    sig=[]
    for i in range(n):
        diagXX=sum(X[i][k]*X[k][i] for k in range(n))%P
        diagXY=sum(X[i][k]*Y[k][i] for k in range(n))%P
        diagYX=sum(Y[i][k]*X[k][i] for k in range(n))%P
        diagYY=sum(Y[i][k]*Y[k][i] for k in range(n))%P
        sig.append((X[i][i],Y[i][i],diagXX,diagXY,diagYX,diagYY))
    return sig


def solve_gauge(U,W,perm):
    """Find q != 0 so U_s[i,j] = q[i]/q[j] W_s[p(i),p(j)] for s=1,2."""
    n=len(perm)
    graph=[[] for _ in range(n)]
    for X,Y in zip(U,W):
        for i in range(n):
            for j in range(n):
                x=X[i][j]; y=Y[perm[i]][perm[j]]
                if bool(x)!=bool(y):return None
                if x:
                    ratio=x*pow(y,-1,P)%P  # q[i]/q[j]
                    graph[j].append((i,ratio))
                    graph[i].append((j,pow(ratio,-1,P)))
    q=[None]*n
    for seed in range(n):
        if q[seed] is not None:continue
        q[seed]=1;stack=[seed]
        while stack:
            i=stack.pop()
            for j,scale in graph[i]:
                cand=q[i]*scale%P
                if q[j] is None:
                    q[j]=cand;stack.append(j)
                elif q[j]!=cand:return None
    assert all(v is not None and v!=0 for v in q)
    assert all(X[i][j]*q[j]%P==q[i]*Y[perm[i]][perm[j]]%P
               for X,Y in zip(U,W) for i in range(n) for j in range(n))
    return q


def gate(U,W,max_permutations=100000):
    sU=vertex_signatures(U);sW=vertex_signatures(W);n=len(sU)
    if Counter(sU)!=Counter(sW):
        return dict(status='impossible',reason='joint vertex-signature multisets differ',
                    candidate_permutations=0)
    buckets=defaultdict(list)
    for j,s in enumerate(sW):buckets[s].append(j)
    groups=sorted(((tuple(i for i,s in enumerate(sU) if s==label),tuple(indices))
                   for label,indices in buckets.items()),key=lambda x:x[0])
    permutations_count=1
    for rows,cols in groups:permutations_count*=factorial(len(rows))
    if permutations_count>max_permutations:
        return dict(status='inconclusive',reason='duplicate vertex signatures; exhaustive search exceeds cap',
                    candidate_permutations=permutations_count)
    ntried=0
    options=[list(permutations(cols)) for rows,cols in groups]
    for block_choice in product(*options):
        perm=[-1]*n
        for (rows,_),col_order in zip(groups,block_choice):
            for row,col in zip(rows,col_order):perm[row]=col
        ntried+=1
        q=solve_gauge(U,W,perm)
        if q is not None:
            return dict(status='possible',reason='same monomial conjugates both Weyl operators',
                        candidate_permutations=permutations_count,checked=ntried,
                        perm=perm,q=q)
    return dict(status='impossible',reason='exhaustive joint-gauge contradictions',
                candidate_permutations=permutations_count,checked=ntried)


def audit_outer(A,B,cap=100000):
    U,W=conjugate_pair(A,B)
    result=gate(U,W,max_permutations=cap)
    if result['status']=='possible':
        # This checks both intertwining relations and can also accept F(aI+bJ).
        C=monomial(result['q'],result['perm'])
        M=matmul(A,matmul(C,B))
        assert defect_count(M)==(0,0)
    return result
