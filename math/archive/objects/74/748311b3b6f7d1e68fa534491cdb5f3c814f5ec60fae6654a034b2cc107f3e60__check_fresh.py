#!/usr/bin/env python3
"""Fresh supplementary checks; no supplied project code is loaded or parsed."""
from fractions import Fraction
from itertools import combinations
from random import Random
from collections import deque
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
COUNTS = {}

def rank_mod2(a):
    basis = {}
    for row in a:
        z = sum((v & 1) << j for j, v in enumerate(row))
        while z:
            p = z.bit_length()-1
            if p in basis:
                z ^= basis[p]
            else:
                basis[p] = z
                break
    return len(basis)

def rank_rational(a):
    if not a or not a[0]:
        return 0
    a = [[Fraction(v) for v in row] for row in a]
    m, n, r = len(a), len(a[0]), 0
    for j in range(n):
        piv = next((i for i in range(r,m) if a[i][j]), None)
        if piv is None:
            continue
        a[piv],a[r] = a[r],a[piv]
        for i in range(r+1,m):
            if a[i][j]:
                t = a[i][j]/a[r][j]
                for z in range(j,n):
                    a[i][z] -= t*a[r][z]
        r += 1
        if r == m:
            break
    return r

def sub(a, rows, cols):
    return [[a[i][j] for j in cols] for i in rows]

def family(h):
    n = 2**(h+1)-1
    q = [[int(i==j) for j in range(n)] for i in range(n)]
    for j in range(1,n):
        q[(j-1)//2][j] = -1
    b = [[0]*n for _ in range(n)]
    for j in range(n):
        i = j
        while True:
            b[i][j] = 1
            if i == 0:
                break
            i = (i-1)//2
    return q,b

def matching(a):
    if not a:
        return 0
    owner = {}
    def augment(i, seen):
        for j,v in enumerate(a[i]):
            if not v or j in seen:
                continue
            seen.add(j)
            if j not in owner or augment(owner[j],seen):
                owner[j] = i
                return True
        return False
    return sum(augment(i,set()) for i in range(len(a)))

def width(a, r, c):
    return max([0]+[rank_mod2(sub(a,r[:k],c[k:])) for k in range(1,len(a))]
                      +[rank_mod2(sub(a,r[k:],c[:k])) for k in range(1,len(a))])

def graph(q):
    n = len(q)
    a = [[0]*(2*n) for _ in range(2*n)]
    for i in range(n):
        for j in range(n):
            if q[i][j]:
                a[i][n+j] = a[n+j][i] = 1
    return a

# Exact integer matrix inverse formula; support shape and degrees.
formula = []
for h in range(7):
    q,b = family(h)
    n = len(q)
    for i in range(n):
        for j in range(n):
            assert sum(q[i][k]*b[k][j] for k in range(n)) == int(i==j)
            assert sum(b[i][k]*q[k][j] for k in range(n)) == int(i==j)
    assert max(sum(bool(v) for v in row) for row in q) <= 3
    assert max(sum(bool(q[i][j]) for i in range(n)) for j in range(n)) <= 2
    g = graph(q)
    assert sum(map(sum,g))//2 == 2*n-1
    seen = {0}; todo = [0]
    while todo:
        v = todo.pop()
        for w,e in enumerate(g[v]):
            if e and w not in seen:
                seen.add(w); todo.append(w)
    assert len(seen)==2*n
    formula.append({'height':h,'n':n,'inverse_verified':True,'lift_tree_verified':True})
COUNTS['inverse_formula_families'] = len(formula)

# Exhaust all 2^(2N)=16,384 rectangular row/column restrictions for N=7.
q,b = family(2); n=len(q)
sets = [[i for i in range(n) if (mask>>i)&1] for mask in range(1<<n)]
rq = {}; rb = {}
for rm, rows in enumerate(sets):
    for cm, cols in enumerate(sets):
        x = sub(q,rows,cols); y=sub(b,rows,cols)
        q2 = rank_mod2(x); b2=rank_mod2(y)
        assert rank_rational(x)==q2==matching(x)
        assert rank_rational(y)==b2
        rq[rm,cm]=q2; rb[rm,cm]=b2
COUNTS['all_rectangles_n7'] = len(rq)
COUNTS['rational_rank_comparisons_n7'] = 2*len(rq)

# Exact minimax DP over balanced prefix pairs, covering ALL independent orders.
def exact_minimax(a, cache=None):
    n=len(a); allmask=(1<<n)-1
    masks=[[m for m in range(1<<n) if m.bit_count()==k] for k in range(n+1)]
    def rank(r,c):
        if cache is not None:
            return cache[r,c]
        return rank_mod2(sub(a,[i for i in range(n) if (r>>i)&1],
                              [j for j in range(n) if (c>>j)&1]))
    costs={}; dp={(0,0):0}; prev={}
    transitions=0
    for k in range(1,n+1):
        for r in masks[k]:
            ri=[i for i in range(n) if (r>>i)&1]
            for c in masks[k]:
                cj=[j for j in range(n) if (c>>j)&1]
                w=max(rank(r,allmask^c),rank(allmask^r,c))
                choices=[]
                for i in ri:
                    for j in cj:
                        p=(r^(1<<i),c^(1<<j))
                        choices.append((max(dp[p],w),i,j,p))
                        transitions+=1
                best=min(choices)
                dp[r,c]=best[0]; prev[r,c]=best[1:]
    r=c=allmask; ro=[]; co=[]
    while r:
        i,j,p=prev[r,c]; ro.append(i); co.append(j); r,c=p
    ro.reverse();co.reverse()
    result={'n':n,'minimum':dp[allmask,allmask],'row_order':ro,'column_order':co,
            'states':len(dp),'transitions':transitions}
    assert width(a,ro,co)==result['minimum']
    return result

exact = []
for h in range(3):
    q0,b0=family(h)
    x=exact_minimax(q0,rq if h==2 else None)
    y=exact_minimax(b0,rb if h==2 else None)
    assert x['minimum']==y['minimum']
    exact.append({'height':h,'Q':x,'inverse':y})
COUNTS['exact_independent_order_optimizations']=2*len(exact)

# Every balanced pair (not only one common ordering): swapped inverse-cut identity.
allmask=(1<<7)-1
balanced=0
for r in range(1<<7):
    for c in range(1<<7):
        if r.bit_count()==c.bit_count():
            assert rb[c,allmask^r]==rq[r,allmask^c]
            assert rb[allmask^c,r]==rq[allmask^r,c]
            balanced+=1
COUNTS['all_balanced_pairs_n7']=balanced

# Random independent orders; graph even-cut identity and odd-cut overhead.
rng=Random(202610100544)
random_cases=0;graph_cuts=0
for h,count in [(1,30),(2,100),(3,100),(4,30),(5,6)]:
    q,b=family(h);n=len(q);g=graph(q)
    for _ in range(count):
        r=list(range(n));c=list(range(n));rng.shuffle(r);rng.shuffle(c)
        s=width(q,r,c)
        assert s==width(b,c,r)
        order=[z for i,j in zip(r,c) for z in (i,n+j)]
        cutranks=[0]
        for k in range(1,2*n):
            cutranks.append(rank_mod2(sub(g,order[:k],order[k:])))
            graph_cuts+=1
        cutranks.append(0)
        for k in range(n+1):
            rhs=rank_mod2(sub(q,r[:k],c[k:]))+rank_mod2(sub(q,r[k:],c[:k]))
            assert cutranks[2*k]==rhs<=2*s
        assert max(cutranks)<=2*s+1
        assert all(abs(x-y)<=1 for x,y in zip(cutranks,cutranks[1:]))
        random_cases+=1
COUNTS['random_independent_order_pairs']=random_cases
COUNTS['random_lift_graph_cuts']=graph_cuts

# Preorder upper bound and integer lower-bound rounding, supplementary only.
preorder=[]
for h in range(7):
    q,b=family(h);n=len(q);order=[]
    def visit(v):
        if v>=n:return
        order.append(v);visit(2*v+1);visit(2*v+2)
    visit(0)
    s=width(q,order,order)
    assert s<=h and s==width(b,order,order)
    lower=(h+1)//4
    preorder.append({'height':h,'n':n,'proved_lower':lower,'preorder_width':s})
for h in range(1001):
    inner=(h+1)//2
    rounded=-(-(inner-1)//2)
    assert rounded==(h+1)//4
COUNTS['rounding_identities']=1001

result={'status':'PASS','purpose':'Supplementary finite checks; all-size theorem is analytic.',
        'method':'Fresh standard-library code only. No supplied program loaded or parsed.',
        'counts':COUNTS,'inverse_formula':formula,'exact_minimax':exact,
        'preorder_bounds':preorder}
(OUT/'CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
