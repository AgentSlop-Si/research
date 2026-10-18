#!/usr/bin/env python3
"""Independent exact controls. No candidate or previous checker is imported/run.
Determinants use a subset dynamic program and literal cyclotomic long division.
All ranks certified are characteristic-zero ranks, never numerical/modular ones.
"""
from pathlib import Path
from collections import defaultdict, Counter
from itertools import combinations, product
from fractions import Fraction
from functools import lru_cache
from math import gcd, isqrt
import json, random, time, hashlib
P=Path(__file__).resolve().parent
CAND=(Path(__file__).resolve().parent / '../candidate')
rng=random.Random(928904202610181753)
start=time.monotonic(); counts=Counter(); out={}

def clean(d):return {x:y for x,y in d.items() if y}

def determinant_polynomial(n, rows, cols):
    k=len(rows); assert k==len(cols)
    states={0:{0:1}}
    for row in rows:
        nxt={}
        for mask,poly in states.items():
            for j,col in enumerate(cols):
                if mask>>j&1:continue
                dest=nxt.setdefault(mask|(1<<j),defaultdict(int))
                sign=(-1)**(mask>>(j+1)).bit_count()
                for e,a in poly.items():dest[(e+row*col)%n]+=sign*a
        states={m:clean(poly) for m,poly in nxt.items()}
    return states[(1<<k)-1]

def remainder(p,m,pol):
    n=p**m;step=n//p;degree=n-step;d=defaultdict(int,pol)
    # Literal monic polynomial long division by 1+X^step+...+X^degree.
    for e in range(n-1,degree-1,-1):
        a=d.get(e,0)
        if a:
            for j in range(p):d[e-degree+j*step]-=a
    return clean(d)

def det(p,m,rows,cols):
    counts[f'exact_order_p{m}_minors']+=1
    return remainder(p,m,determinant_polynomial(p**m,rows,cols))

def basis(p,m,rows,cols):
    found=[]
    for row in rows:
        test=found+[row]
        if any(det(p,m,test,cc) for cc in combinations(cols,len(test))):found=test
        if len(found)==len(cols):return found
    return found

@lru_cache(None)
def divisors(n):
    ds=[]
    for d in range(1,isqrt(n)+1):
        if n%d==0:
            ds.append(d)
            if d*d!=n:ds.append(n//d)
    return tuple(sorted(ds))

def prime(n):return n>=2 and len(divisors(n))==2

# Hash check first and again at end; candidate packet remains unmodified.
sources=json.loads((P/'SOURCES.json').read_text())
def hashes():
    for s in sources['verified']:
        b=(P/s['path']).read_bytes()
        assert len(b)==s['bytes'] and hashlib.sha256(b).hexdigest()==s['sha256']
hashes()

# All threshold row sets at order nine, all column supports, k<=3.
small={}
for k in (1,2,3):
    num=0
    for rows in combinations(range(9),3*(k-1)+1):
        for cols in combinations(range(9),k):
            assert len(basis(3,2,rows,cols))==k
            num+=1
    small[str(k)]=num
out['all_F9_threshold_sets']=small
# Every four-column support at F25; concentrated boundary row set.
rows=[y+5*z for y in (0,2,4) for z in range(5)]+[11]
assert len(set(rows))==16
for cols in combinations(range(25),4):assert len(basis(5,2,rows,cols))==4
out['F25_four_supports']=12650
print('Exhaustive square-order support controls passed',flush=True)

# Literal short support polynomials, including sharp zero-bound examples.
polytests=0;sharpzeros=0
for p in (3,5,7,11,13,17):
    n=p*p
    for k in range(1,min(5,p)+1):
        # Product of k-1 linear factors in X^p, coefficients in Q(zeta_p).
        for shift in (0,1):
            zero=0
            for x in range(n):
                poly={0:1}
                for j in range(k-1):
                    new=defaultdict(int)
                    for e,a in poly.items():
                        new[(e+p*x)%n]+=a
                        new[(e+p*(j+shift))%n]-=a
                    poly=clean(new)
                zero+=not remainder(p,2,poly)
            assert zero==(k-1)*p
            sharpzeros+=1
        for _ in range(20):
            freqs=rng.sample(range(n),k)
            coeff=[(rng.choice((-2,-1,1,2)),rng.randrange(n)) for _ in freqs]
            zero=0
            for x in range(n):
                poly=defaultdict(int)
                for v,(a,e) in zip(freqs,coeff):poly[(v*x+e)%n]+=a
                zero+=not remainder(p,2,poly)
            assert zero<=(k-1)*p
            polytests+=1
out['short_support_polynomials']=polytests
out['sharp_short_support_zero_examples']=sharpzeros

# Independent rich-fiber samples of both strengthened two-class branches.
# Find exact four-minors among four rows chosen separately on their p² blocks.
direct={}
for p in (5,7,11,13,17,23,29):
    dd={}
    for branch,sizes,want in [('3+1',(2*p+1,p),(3,1)),('2+2',(p+1,2*p),(2,2))]:
        for trial in range(140):
            yy=rng.sample(range(p),2); vv=rng.sample(range(p*p),3)
            rr=[]
            for y,size,k in zip(yy,sizes,want):
                aa=rng.sample(range(p*p),size)
                bb=basis(p,2,aa,vv[:k]);assert len(bb)==k
                rr.extend(y+p*a for a in bb)
            # Representatives themselves need not be among selected columns.
            cc=[]
            for v in vv:
                lifts=rng.sample(range(1,p),2)
                cc.extend(v+p*p*w for w in lifts)
            cert=next((list(c) for c in combinations(cc,4) if det(p,3,rr,c)),None)
            assert cert is not None
        dd[branch]=140
    direct[str(p)]=dd
out['rich_fiber_two_class_samples']=direct

# General direct-sum case, including s=3/4, without assuming rank <=3:
# choose each block to have t independent rows. The square st minor must be full rank.
general=0
for p in (5,7,11):
    for s,t in ((1,4),(2,2),(2,3),(3,1),(3,2),(4,1)):
        for _ in range(12):
            yy=rng.sample(range(p),s);tt=rng.sample(range(p*p),t)
            rr=[]
            for y in yy:
                a=rng.sample(range(p*p),min(p*p,(t-1)*p+1))
                bb=basis(p,2,a,tt);assert len(bb)==t
                rr.extend(y+p*u for u in bb)
            cc=[v+p*p*w for v in tt for w in rng.sample(range(1,p),s)]
            assert det(p,3,rr,cc)
            general+=1
out['general_direct_sum_square_minors']=general
print('Rich-fiber and general direct sums passed',flush=True)

# Verify every retained target certificate with our separate determinant engine.
certs=json.loads((CAND/'TARGET_MINOR_CERTIFICATES.json').read_text())
for v in certs:
    got=det(v['p'],3,v['rows'],v['columns'])
    assert got and got=={int(k):a for k,a in v['nonzero_remainder'].items()}
assert len(certs)==400
out['candidate_target_certificates_rechecked']=len(certs)

# Exhaustive occupancy/size logic and projective equivalence controls.
occ={};splits={};proj=0
for p in (5,7,11,13,17,19,23):
    occ[str(p)]=0
    for sizes in product(range(1,p+1),repeat=4):
        if sum(sizes)>3*p:
            assert sum(v>=2 for v in sizes)>=3 and max(sizes)>=3
            occ[str(p)]+=1
    splits[str(p)]=0
    for a in range(1,p*p+1):
        for b in range(1,p*p+1):
            if a+b>3*p:
                assert max(a,b)>2*p or min(a,b)>p
                splits[str(p)]+=1
    n=p**3
    for d in (1,p,p*p,n):
        if d>p:assert n//d<=p
    for _ in range(70):
        # Random C in a subgroup coset; actual generated difference subgroup,
        # and hence projective equivalence, checked rather than assumed.
        scale=rng.choice((1,p,p*p));c0=rng.randrange(n)
        c=[(c0+scale*j)%n for j in rng.sample(range(n//scale),min(6,n//scale))]
        g=gcd(n,*((v-c[0])%n for v in c))
        # H has order n/g, its annihilator has order g.
        for _ in range(20):
            r,r2=rng.sample(range(n),2)
            eq=all((r-r2)*(v-c[0])%n==0 for v in c)
            assert eq==((r-r2)%(n//g)==0)
            proj+=1
out['four_fiber_occupancies']=occ;out['two_class_splits']=splits
out['projective_equivalence_pairs']=proj

# Genuine rank-three examples and sharp density through prime 997.
primes=[p for p in range(5,1000) if prime(p)]
for p in primes:
    assert det(p,3,[0,p,2*p],[0,1,2])
    assert Fraction(3,3*p)+Fraction(3,p*p)==Fraction(p+3,p*p)
    assert 3*p*p*p==3*(p**3)
    for _ in range(6):
        rr=rng.sample(range(p*p),4)
        cc=rng.sample([v+p*p*w for v in (0,1,2) for w in range(p)],4)
        assert not det(p,3,[p*r for r in rr],cc)
out['sharp_family_primes']=len(primes)

p=13;n=p**3;d=min(v+n//v for v in divisors(n));base=Fraction(d,n)
e2=min(2*v+n//v for v in divisors(n) if v<n)
assert (d,e2,n*d)==(182,195,399854)
assert Fraction(e2,n)>base+Fraction(1,676)
assert Fraction(16,169)>base+Fraction(1,676)
assert Fraction(16,n)>(base+Fraction(1,676))**2
shapes=0;minimum=None;minimizers=[];old_obstructions=[]
for a in range(1,4*p+1):
    for b in range(a,min(n,3*n//a)+1):
        density=Fraction(3*(a+b),a*b)
        if a<=3*p:
            assert density>=Fraction(16,169)
            shapes+=1
            if minimum is None or density<minimum:minimum=density;minimizers=[(a,b)]
            elif density==minimum:minimizers.append((a,b))
        elif density<=base:old_obstructions.append((a,b))
assert minimizers==[(39,169)] and len(old_obstructions)==12
out['target_density']={'rank_one':str(base),'rank_two':str(Fraction(e2,n)),'rank_three':str(minimum),'minimizing_scalar_shapes':minimizers,'shapes':shapes,'eliminated_old_obstructions':old_obstructions,'higher_rank_area_penalty':'1/676'}

# Independent tiling orientation: 13 row cosets of size 169,
# 169 column cosets of size 13. Exact once coverage and all phase conditions.
coverage=bytearray(n*n);cost=0;tiles=0
for rowcoset in range(p):
    rows=range(rowcoset,n,p)
    for colcoset in range(p*p):
        cols=range(colcoset,n,p*p)
        for r in rows:
            for c in cols:
                assert (r-rowcoset)*(c-colcoset)%n==0
                pos=r*n+c;assert not coverage[pos];coverage[pos]=1
        tiles+=1;cost+=len(rows)+len(cols)
assert all(coverage) and tiles==n and cost==n*d
out['explicit_transposed_tiling']={'tiles':tiles,'entries':len(coverage),'cost':cost}

# Independent census: build prime-divisor sieve rather than per-divisor prime tests.
limit=10000;spf=list(range(limit+1))
for q in range(2,isqrt(limit)+1):
    if spf[q]==q:
        for v in range(q*q,limit+1,q):
            if spf[v]==v:spf[v]=q
old=[];new=[]
for v in range(2,limit+1):
    dn=min(x+v//x for x in divisors(v));z=v;pp=[]
    while z>1:
        q=spf[z];pp.append(q)
        while z%q==0:z//=q
    covered=dn*dn<12*v or max(pp)**2>v or v==1331
    q=isqrt(v//11)
    covered=covered or (v==11*q*q and q>11 and spf[q]==q)
    if not covered:
        old.append(v)
        if v!=2197:new.append(v)
assert old[0]==2197 and new[0]==2873
assert 2873==13**2*17 and min(x+2873//x for x in divisors(2873))==186
assert 12*2873<186**2<16*2873
expected=json.loads((CAND/'RESULTS.json').read_text())['domain_census_through_10000']
assert old==expected['previous_residuals'] and new==expected['remaining_residuals']
out['domain_census']={'limit':limit,'previous_residuals':old,'remaining_residuals':new,'all_lengths_through':2872,'next_N':2873,'next_D':186}
print('Target density, full partition, and census passed',flush=True)

# Independent symbolic polynomial-remainder verification includes vanishing cases.
import sympy as sp
X=sp.Symbol('X');checks=0
for p in (3,5,7,11,13):
    for m in (1,2,3):
        n=p**m;phi=sp.Poly(sp.cyclotomic_poly(n,X),X)
        for k in range(2,min(4,p)+1):
            for nullcase in (False,True):
                rows=rng.sample(range(n),k);cols=rng.sample(range(n),k)
                if nullcase and m>1:
                    rows=[p**(m-1)*v for v in range(k)]
                    cols=[p*v for v in range(k)]
                poly=determinant_polynomial(n,rows,cols)
                actual=sp.Poly.from_dict({(e,):a for e,a in poly.items()},X).rem(phi)
                dct={} if actual.is_zero else {e[0]:int(a) for e,a in actual.terms()}
                assert dct==remainder(p,m,poly)
                checks+=1
out['symbolic_remainder_crosschecks']=checks
hashes();out['hashes_verified_before_and_after']=len(sources['verified'])
out['exact_counts']=dict(counts);out['status']='all_passed';out['elapsed_seconds']=round(time.monotonic()-start,3)
(P/'RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print('ALL PASSED',json.dumps({'elapsed_seconds':out['elapsed_seconds'],'counts':dict(counts),'next_residual':2873}),flush=True)
