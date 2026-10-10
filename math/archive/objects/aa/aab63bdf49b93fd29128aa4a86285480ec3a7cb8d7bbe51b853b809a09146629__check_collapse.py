#!/usr/bin/env python3
"""Independent exact modular checks of the bounded-fragmentation collapse.
Newly authored; no uploaded modules are imported or executed.
"""
import json, math, pathlib, random

ROOT = pathlib.Path(__file__).resolve().parent
P = 1009
RNG = random.Random(202610092247)

def rank(a):
    if not a: return 0
    a = [[x % P for x in row] for row in a]
    rr = 0
    for j in range(len(a[0])):
        piv = next((i for i in range(rr, len(a)) if a[i][j]), None)
        if piv is None: continue
        a[rr], a[piv] = a[piv], a[rr]
        inv = pow(a[rr][j], -1, P)
        a[rr] = [x * inv % P for x in a[rr]]
        for i in range(rr + 1, len(a)):
            c = a[i][j]
            if c: a[i] = [(x - c*y) % P for x,y in zip(a[i], a[rr])]
        rr += 1
        if rr == len(a): break
    return rr

def block(a, rows, cols): return [[a[i][j] for j in cols] for i in rows]
def mm(a,b):
    bt = list(zip(*b))
    return [[sum(x*y for x,y in zip(row,col)) % P for col in bt] for row in a]
def ident(n): return [[int(i==j) for j in range(n)] for i in range(n)]
def perm(p): return [[int(i==p[j]) for j in range(len(p))] for i in range(len(p))]
def tr(a): return list(map(list,zip(*a)))

def qs(n,r):
    """Sum of r scalar-transition QS1 generators, with transition zeros."""
    a = [[0]*n for _ in range(n)]
    for i in range(n): a[i][i] = RNG.randrange(P)
    for component in range(r):
        u,v,g,h = [[RNG.randrange(P) for _ in range(n)] for _ in range(4)]
        lower = [RNG.randrange(P) if RNG.randrange(5) else 0 for _ in range(n)]
        upper = [RNG.randrange(P) if RNG.randrange(5) else 0 for _ in range(n)]
        for j in range(n):
            val = v[j]
            for i in range(j+1,n):
                a[i][j] = (a[i][j] + u[i]*val) % P
                val = val*lower[i] % P
            val = h[j]
            for i in range(j-1,-1,-1):
                a[i][j] = (a[i][j] + g[i]*val) % P
                val = val*upper[i] % P
    return a

def cut_ranks(a):
    n = len(a)
    return [(rank(block(a,range(k),range(k,n))),rank(block(a,range(k,n),range(k)))) for k in range(1,n)]

subset_checks = 0
for n in range(2,9):
    for r in [0,1,2]:
        a = qs(n,r)
        assert max(map(max,cut_ranks(a))) <= r
        for mask in range(1,2**n-1):
            k = [i for i in range(n) if mask>>i&1]
            kc = [i for i in range(n) if not mask>>i&1]
            boundaries = sum(((mask>>i)&1) != ((mask>>(i+1))&1) for i in range(n-1))
            assert rank(block(a,k,kc)) <= boundaries*r
            assert rank(block(a,kc,k)) <= boundaries*r
            subset_checks += 2

affine_cases = []
collapse_checks = 0
for n in [8,16,32,40,64]:
    for multiplier in [1,3,5,7]:
        if math.gcd(multiplier,n) != 1: continue
        q = [(multiplier*j)%n for j in range(n)]
        qm = perm(q)
        for r in [0,1,2]:
            s2 = qs(n,r)
            c = mm(mm(qm,s2),tr(qm))
            ranks = cut_ranks(c)
            actual = max(map(max,ranks))
            bound = (2*multiplier-1)*r
            for t in range(1,n):
                k = [i for i in range(n) if q[i]<t]
                boundaries = sum((q[i]<t) != (q[i+1]<t) for i in range(n-1))
                assert k[0] == 0
                assert boundaries <= 2*multiplier-1
                assert max(ranks[t-1]) <= boundaries*r
            assert actual <= bound
            affine_cases.append({'N':n,'multiplier':multiplier,'stage_order':r,'conjugate_order':actual,'certified_bound':bound})
            if n<=32 and multiplier==3:
                s1,s3,s4 = qs(n,1),qs(n,1),qs(n,1)
                p1 = list(range(n)); p3=list(range(n))
                RNG.shuffle(p1);RNG.shuffle(p3)
                p1m,p3m = perm(p1),perm(p3)
                t = mm(s3,c)
                left = mm(mm(mm(mm(mm(mm(s4,p3m),s3),qm),s2),p1m),s1)
                right = mm(mm(mm(mm(s4,p3m),t),mm(qm,p1m)),s1)
                assert left==right
                assert max(map(max,cut_ranks(t))) <= 1+bound
                collapse_checks += 1

out = {'field':P,'subset_direction_checks':subset_checks,'affine_cases':affine_cases,
       'exact_four_to_three_word_checks':collapse_checks,
       'max_A3_order_for_QS1':max(c['conjugate_order'] for c in affine_cases if c['multiplier']==3 and c['stage_order']==1),
       'zero_transitions_included':True,'uploaded_code_executed':False}
(ROOT/'EXACT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
