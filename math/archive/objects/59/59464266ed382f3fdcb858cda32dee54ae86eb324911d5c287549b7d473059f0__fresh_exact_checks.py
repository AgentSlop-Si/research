#!/usr/bin/env python3
"""New independent controls, 2026-10-10. Standard library only.
No supplied program is executed, imported, compiled, or AST-parsed.
"""
import itertools
import json
import random
from fractions import Fraction
from pathlib import Path

OUT = Path(__file__).resolve().parent
RNG = random.Random(10520452)
COUNTS = {}
def bump(k, n=1): COUNTS[k] = COUNTS.get(k, 0) + n

def rank(a,p):
    a=[list(row) for row in a]
    if not a: return 0
    n=len(a[0]); k=0
    for j in range(n):
        z=next((i for i in range(k,len(a)) if a[i][j]%p),None)
        if z is None: continue
        a[z],a[k]=a[k],a[z]
        s=pow(a[k][j],-1,p); a[k]=[x*s%p for x in a[k]]
        for i in range(k+1,len(a)):
            s=a[i][j]%p
            if s: a[i]=[(x-s*y)%p for x,y in zip(a[i],a[k])]
        k+=1
        if k==len(a): break
    return k

def inverse(a,p):
    n=len(a); b=[list(row)+[int(i==j) for j in range(n)] for i,row in enumerate(a)]
    for j in range(n):
        z=next((i for i in range(j,n) if b[i][j]%p),None)
        if z is None: return None
        b[z],b[j]=b[j],b[z]
        s=pow(b[j][j],-1,p); b[j]=[x*s%p for x in b[j]]
        for i in range(n):
            s=b[i][j]%p
            if i!=j and s: b[i]=[(x-s*y)%p for x,y in zip(b[i],b[j])]
    return [row[n:] for row in b]

def sub(a,rows,cols): return [[a[i][j] for j in cols] for i in rows]

def components(adj,removed=()):
    left=set(range(len(adj)))-set(removed); out=[]
    while left:
        s=left.pop(); c={s}; queue=[s]
        while queue:
            u=queue.pop()
            for v in adj[u]&left:
                left.remove(v); c.add(v); queue.append(v)
        out.append(c)
    return out

def lift(q,qi):
    n=len(q); h=[[0]*(2*n) for _ in range(2*n)]; hi=[[0]*(2*n) for _ in range(2*n)]
    for i in range(n):
        for j in range(n):
            h[i][n+j]=h[n+j][i]=q[i][j]
            hi[n+i][j]=hi[j][n+i]=qi[i][j]
    adj=[{j for j,x in enumerate(row) if x} for row in h]
    return h,hi,adj

def decomposition(adj):
    # Independent degree-two elimination, with direct decomposition validation.
    work=[set(z) for z in adj]; remaining=set(range(len(adj))); bags=[]; order=[]
    while remaining:
        v=next((v for v in sorted(remaining) if len(work[v]&remaining)<=2),None)
        assert v is not None
        ns=work[v]&remaining
        bags.append({v}|ns); order.append(v)
        if len(ns)==2:
            x,y=sorted(ns); work[x].add(y); work[y].add(x)
        remaining.remove(v)
    loc={v:i for i,v in enumerate(order)}; tree=[set() for _ in range(len(bags)+1)]; bags.append(set())
    for i,v in enumerate(order):
        parent=min((loc[x] for x in bags[i]-{v}),default=len(order))
        assert parent>i
        tree[i].add(parent); tree[parent].add(i)
    assert max(map(len,bags))<=3
    assert len(components(tree))==1 and sum(map(len,tree))==2*(len(tree)-1)
    for u in range(len(adj)):
        for v in adj[u]: assert any({u,v}<=b for b in bags)
        ids={i for i,b in enumerate(bags) if u in b}; seen=set(); queue=[next(iter(ids))]
        while queue:
            t=queue.pop()
            if t in seen: continue
            seen.add(t); queue.extend((tree[t]&ids)-seen)
        assert seen==ids
    return bags,tree,loc

def separator(adj,marked):
    bags,tree,loc=decomposition(adj); weights=[0]*len(tree)
    for v in marked: weights[loc[v]]+=1
    total=len(marked)
    for t in range(len(tree)):
        if all(2*sum(weights[i] for i in c)<=total for c in components(tree,{t})):
            x=bags[t]
            assert len(x)<=3
            assert all(2*len(c&marked)<=total for c in components(adj,x))
            bump('weighted_separator_checks')
            return x
    raise AssertionError('no centroid')

def verify_nullity(h,hi,adj,p,x):
    cs=components(adj,x); a=set(); b=set()
    for c in cs:
        (a if RNG.randrange(2) else b).update(c)
    assert not any(adj[u]&b for u in a)
    ac=sorted(set(range(len(h)))-a); bc=sorted(set(range(len(h)))-b)
    actual=rank(sub(hi,sorted(a),sorted(b)),p)
    comp=rank(sub(h,bc,ac),p)
    assert actual==comp+len(a)+len(b)-len(h)
    assert comp<=2*len(x) and actual<=len(x)
    bump('inverse_separator_rank_checks')
    if a and rank(sub(h,sorted(a),sorted(a)),p)<len(a): bump('singular_A_principal_blocks')
    if b and rank(sub(h,sorted(b),sorted(b)),p)<len(b): bump('singular_B_principal_blocks')

def selection(q,qi,p,rows,cols,rmap,cmap):
    n=len(q); m=len(rows); assert m==len(cols) and m>=12
    h,hi,adj=lift(q,qi)
    rm={n+rmap[i]:i for i in rows}; cm={cmap[j]:j for j in cols}
    assert len(rm)==m and len(cm)==m and not set(rm)&set(cm)
    x=separator(adj,set(rm)|set(cm)); verify_nullity(h,hi,adj,p,x)
    red=set(sorted(set(rm)-x)[:m-3]); blue=set(sorted(set(cm)-x)[:m-3]); t=m-3
    cs=components(adj,x); weights=[len(c&(red|blue)) for c in cs]
    assert len(red)==len(blue)==t and sum(weights)==2*t and max(weights)<=m
    big=next((i for i,w in enumerate(weights) if 3*w>=t),None)
    if big is not None: a=set(cs[big])
    else:
        a=set(); w=0
        for c,ww in zip(cs,weights):
            a|=c; w+=ww
            if 3*w>=t: break
    b=set(range(2*n))-x-a
    assert 3*len(a&(red|blue))>=t and 3*len(b&(red|blue))>=t
    cross=[(red&a,blue&b),(red&b,blue&a)]
    aa,bb=max(cross,key=lambda z:min(map(len,z)))
    assert 6*min(len(aa),len(bb))>=t
    k=t//6
    rr=[rm[v] for v in sorted(aa)[:k]]; cc=[cm[v] for v in sorted(bb)[:k]]
    assert rank(sub(qi,[rmap[i] for i in rr],[cmap[j] for j in cc]),p)<=3
    bump('one_step_color_selections')
    return rr,cc

def random_q(n,p):
    while True:
        q=[[0]*n for _ in range(n)]; nodes=list(range(n)); RNG.shuffle(nodes); edges=[]
        pos=0
        while pos<n:
            size=RNG.randint(1,min(12,n-pos)); block=nodes[pos:pos+size]; pos+=size
            k=1 if p==2 or size==1 or RNG.randrange(2)==0 else RNG.randint(2,size)
            if k==1: edges.append([(block[0],RNG.randrange(1,p))])
            else:
                for j in range(k): edges.append([(block[j],RNG.randrange(1,p)),(block[(j+1)%k],RNG.randrange(1,p))])
            for j in range(k,size): edges.append([(block[j],RNG.randrange(1,p)),(block[RNG.randrange(j)],RNG.randrange(1,p))])
        RNG.shuffle(edges)
        for j,e in enumerate(edges):
            for i,w in e: q[i][j]=w
        qi=inverse(q,p)
        if qi is not None: return q,qi

# Complete enumeration of actual column supports, including all singleton values.
for n,p in [(1,2),(2,2),(3,2),(4,2),(1,3),(2,3),(3,3)]:
    columns=[]
    for k in [1,2]:
        for supp in itertools.combinations(range(n),k):
            for vals in itertools.product(range(1,p),repeat=k):
                c=[0]*n
                for i,w in zip(supp,vals): c[i]=w
                columns.append(c)
    for cs in itertools.product(columns,repeat=n):
        q=[list(z) for z in zip(*cs)]; bump('exhaustive_matrices')
        qi=inverse(q,p)
        if qi is None: continue
        bump('exhaustive_invertible_matrices')
        h,hi,adj=lift(q,qi)
        for c in components(adj): assert sum(len(adj[v]&c) for v in c)//2<=len(c)
        if max(sum(bool(x) for x in row) for row in q)>2: bump('high_row_degree_exhaustive')
        # One random two-color marking each; all n^2 entries separately verify lift.
        for i in range(n):
            for j in range(n): assert hi[n+i][j]==qi[i][j]
        m=RNG.randrange(1,n+1)
        marked=set(RNG.sample(range(n),m))|set(n+i for i in RNG.sample(range(n),m))
        x=separator(adj,marked); verify_nullity(h,hi,adj,p,x)
        bump('lift_orientation_entries',n*n)
print('exhaustive matrix and graph controls passed',flush=True)

# General (not necessarily symmetric) inverse identity, all index pairs for tiny matrices.
for n in range(1,5):
    for repeat in range(15):
        p=RNG.choice([2,3,5,7])
        while True:
            a=[[RNG.randrange(p) for j in range(n)] for i in range(n)]; ai=inverse(a,p)
            if ai is not None: break
        sets=[{i for i in range(n) if mask>>i&1} for mask in range(1<<n)]
        for i in sets:
            for j in sets:
                ic=set(range(n))-i; jc=set(range(n))-j
                assert rank(sub(ai,sorted(i),sorted(j)),p)==rank(sub(a,sorted(jc),sorted(ic)),p)+len(i)+len(j)-n
                bump('general_nullity_identities')
print('complement orientation controls passed',flush=True)

for t in range(1,201):
    for a in range(t+1):
        for b in range(t+1):
            if 3*(a+b)<t or 3*(2*t-a-b)<t: continue
            assert 6*max(min(a,t-b),min(t-a,b))>=t
            bump('exhaustive_two_color_count_cases')
for trial in range(180):
    n=RNG.randint(12,48); p=RNG.choice([2,3,5,7,17,101]); q,qi=random_q(n,p)
    rows=list(range(n)); cols=list(range(n)); rmap=list(range(n)); cmap=list(range(n)); RNG.shuffle(rmap); RNG.shuffle(cmap)
    m=RNG.randint(12,n); rows=RNG.sample(rows,m); cols=RNG.sample(cols,m)
    rr,cc=selection(q,qi,p,rows,cols,rmap,cmap)
    ls=[RNG.randrange(p) for _ in range(n)]; rs=[RNG.randrange(p) for _ in range(n)]
    ls[0]=0; rs[-1]=0  # Both endpoint matrices are genuinely singular.
    b=[[ls[i]*qi[rmap[i]][cmap[j]]*rs[j]%p for j in cc] for i in rr]
    assert rank(b,p)<=3; bump('zero_endpoint_scale_controls')
print('color and routed one-step controls passed',flush=True)

for trial in range(18):
    n=96; p=101; rows=list(range(n)); cols=list(range(n)); bank=[]
    for stage in range(2):
        q,qi=random_q(n,p); rmap=list(range(n)); cmap=list(range(n)); RNG.shuffle(rmap); RNG.shuffle(cmap)
        ls=[RNG.randrange(p) for _ in range(n)]; rs=[RNG.randrange(p) for _ in range(n)]
        bank.append((qi,rmap,cmap,ls,rs))
        rows,cols=selection(q,qi,p,rows,cols,rmap,cmap)
        for bi,ri,ci,l,r in bank:
            bb=[[l[i]*bi[ri[i]][ci[j]]*r[j]%p for j in cols] for i in rows]
            assert rank(bb,p)<=3; bump('nested_branch_rank_controls')
    summed=[[sum(l[i]*bi[ri[i]][ci[j]]*r[j] for bi,ri,ci,l,r in bank)%p for j in cols] for i in rows]
    assert rank(summed,p)<=6; bump('independent_two_branch_sums')
print('nested independent-branch controls passed',flush=True)

for q in [1,2,3,4,7,20,100,1000]:
    for r in range(1,101):
        for diagonal in [False,True]:
            n=(16 if diagonal else 4)*q*r*36**r+1
            m=n//2 if diagonal else n
            m0=m
            for j in range(r):
                assert m>=4*q
                m=(m-q)//6
                exact_lower=Fraction(m0,6**(j+1))-Fraction(q+6,5)*(1-Fraction(1,6**(j+1)))
                assert m>=exact_lower
            assert m>=Fraction(n,(4 if diagonal else 2)*6**r)
            assert Fraction(m*m,n)>q*r
            bump('threshold_recurrence_cases')
for m in range(200001):
    assert (m-3)//6>=Fraction(m,6)-Fraction(3,2)
    bump('base_rounding_cases')
print('all exact controls passed',flush=True)
result={'status':'PASS','seed':10520452,'scope':'Fresh standard-library exact arithmetic controls only; the complex norm theorem is analytic. No supplied code executed/imported/compiled/AST-parsed.','counts':COUNTS}
(OUT/'exact_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
