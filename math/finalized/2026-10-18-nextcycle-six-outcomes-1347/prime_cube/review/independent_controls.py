#!/usr/bin/env python3
"""Independent characteristic-zero controls; imports no author checker."""
import itertools as it
import json, random, time, hashlib
from collections import Counter
from fractions import Fraction
from pathlib import Path

HERE=Path(__file__).resolve().parent
START=time.time()
RNG=random.Random(202610181342)
P={}
for k in (2,3,4,5):
    P[k]=[(s,(-1)**sum(s[i]>s[j] for i in range(k) for j in range(i+1,k))) for s in it.permutations(range(k))]

def det_poly(rows,cols,n):
    out=Counter()
    for s,sgn in P[len(rows)]:
        out[sum(rows[i]*cols[s[i]] for i in range(len(rows)))%n]+=sgn
    return {e:c for e,c in out.items() if c}

def zero_cyclotomic(poly,p,m):
    # Exact reduction by Phi_(p^m)=sum_t X^(t p^(m-1)).
    n=p**m; step=n//p
    return all(len({poly.get(b+t*step,0) for t in range(p)})==1 for b in {e%step for e in poly})

def nonsingular(rows,cols,p,m=3):
    return not zero_cyclotomic(det_poly(rows,cols,p**m),p,m)

def mixed_B(rows,cols,p):
    # Use only permutations assigning the exceptional row to the second pair.
    t=rows[3]; q=cols[2]%p; n=p*p
    out=Counter()
    for s,sgn in P[4]:
        if s[3] not in (2,3):continue
        exponent=sum(rows[i]*cols[s[i]] for i in range(4))-t*q
        assert exponent%p==0
        out[(exponent//p)%n]+=sgn
    return {e:c for e,c in out.items() if c}

def mixed_formula(rows,cols,p):
    u=[x//p for x in rows[:3]]; t=rows[3]
    v=[x//p for x in cols[:2]]; q=cols[2]%p
    w=[(x-q)//p for x in cols[2:]]
    out=Counter(); n=p*p
    for i in range(3):
        remain=[j for j in range(3) if j!=i]
        minor=det_poly([u[j] for j in remain],v,p)
        for e,c in minor.items():
            out[(p*e+u[i]*q+t*w[1]+p*u[i]*w[0])%n]+=(-1)**i*c
            out[(p*e+u[i]*q+t*w[0]+p*u[i]*w[1])%n]-=(-1)**i*c
    return {e:c for e,c in out.items() if c}

def check_mixed(rows,cols,p):
    B=mixed_B(rows,cols,p)
    assert B==mixed_formula(rows,cols,p)
    assert not zero_cyclotomic(B,p,2)
    assert nonsingular(rows,cols,p)
    t=rows[3];q=cols[2]%p
    X={q*(x//p)%p for x in rows[:3]}
    shifts=[t*((x-q)//p)%p for x in cols[2:]]
    S=[{(x+s)%p for x in X} for s in shifts]
    assert S[0]^S[1]
    return len(S[0]^S[1])

counts=Counter(); sample_by_prime={}
# Exhaust the canonical first two-digit B/B, B/C and C/C controls at p=5.
p=5
B=[tuple(p*x for x in U)+(1,) for U in it.combinations(range(p),3)]
C=[tuple(p*x for x in U)+tuple(1+p*x for x in W)
   for U in it.combinations(range(p),2) for W in it.combinations(range(p),2)]
BQ=[tuple(p*x for x in U)+(q,) for U in it.combinations(range(p),3) for q in range(1,p)]
CQ=[tuple(p*x for x in U)+tuple(q+p*x for x in W)
    for U in it.combinations(range(p),2) for W in it.combinations(range(p),2) for q in range(1,p)]
for name, RR, CC in [('BB',B,BQ),('BC',B,CQ),('CC',C,CQ)]:
    for rows in RR:
        for cols in CC:
            assert nonsingular(rows,cols,p),(name,rows,cols)
            if name=='BC':check_mixed(rows,cols,p)
            counts['exhaustive_'+name]+=1
# Each possible four-point column subset modulo p^2 against universal and all-one-class rows.
for cols in it.combinations(range(25),4):
    assert nonsingular((0,1,2,3),cols,5)
    assert nonsingular((0,5,10,15),cols,5)
    counts['exhaustive_U_or_A']+=2

# Structured samples exercise all three base-p digits, including arbitrary lifts.
def lifted(p,k):
    return [x+p*RNG.randrange(p) for x in RNG.sample(range(p),k)]
def bset(p):
    u=lifted(p,3); t=RNG.choice([x for x in range(1,p**3) if x%p])
    return tuple(p*x for x in u)+(t,)
def cset(p):
    u=lifted(p,2);w=lifted(p,2);q=RNG.randrange(1,p)
    return tuple(p*x for x in u)+tuple(q+p*x for x in w)
for p in (5,7,11,13,17,19,23):
    sample_by_prime[p]=Counter()
    for j in range(1000):
        for typ,rows,cols in [('BB',bset(p),bset(p)),('BC',bset(p),cset(p)),('CC',cset(p),cset(p))]:
            assert len({x%(p*p) for x in rows})==4
            assert len({x%(p*p) for x in cols})==4
            assert nonsingular(rows,cols,p),(p,typ,rows,cols)
            if typ=='BC':check_mixed(rows,cols,p)
            sample_by_prime[p][typ]+=1
            counts['lifted_'+typ]+=1

# Exhaust the finite translation fact; independently count unmatched residues.
minimum_symdiff={}
for p in (5,7,11,13,17,19,23):
    least=p
    for XX in it.combinations(range(p),3):
        X=set(XX)
        for shift in range(1,p):
            d=len(X^{(x+shift)%p for x in X})
            assert d>0
            least=min(least,d)
            counts['translation_cases']+=1
    minimum_symdiff[p]=least
# A nonprime boundary control: a proper 3-set can be translation invariant.
assert {0,3,6}=={(x+3)%9 for x in (0,3,6)}
# The p=3 boundary invalidates the proper-subset step (not a theorem counterexample).
assert set(range(3))=={(x+1)%3 for x in range(3)}

# Exhaust all possible distributions of five selected mod-p^2 classes.
for p in (5,7,11,13,17,19,23):
    for profile in it.combinations_with_replacement(range(p),5):
        co=Counter(profile);sizes=sorted(co.values(),reverse=True)
        if len(co)>=4:typ='U'
        elif sizes[0]>=4:typ='A'
        elif sizes[0]==3:typ='B'
        else:
            assert sizes.count(2)>=2
            typ='C'
        counts['selection_'+typ]+=1

# Additional direct universal-minor controls for k up to p.
for p,m in ((5,1),(5,2),(5,3),(7,1),(7,2),(7,3),(11,3)):
    n=p**m
    for k in (2,3,4,5):
        if k>p:continue
        for j in range(100):
            rows=[x+p*RNG.randrange(n//p) for x in RNG.sample(range(p),k)]
            cols=RNG.sample(range(n),k)
            assert nonsingular(rows,cols,p,m),(p,m,k,rows,cols)
            counts['universal_lemma']+=1

# Actual Fourier rank-three four-direction negative controls, over Q(zeta).
negative_controls=[]
for p in (3,5,7,11,13,17):
    rows=cols=[0,p*p,2*p*p,1]
    assert zero_cyclotomic(det_poly(rows,cols,p**3),p,3)
    minor=det_poly([0,p*p,1],[0,p*p,1],p**3)
    assert not zero_cyclotomic(minor,p,3)
    expected={0:-1,p*p:2,2*p*p:-1}
    assert minor==expected
    # Index 0 makes a proportionality factor 1; index 1 distinguishes each pair.
    assert len(set(rows))==4 and 0 in cols and 1 in cols
    assert len(set(cols))==4 and 0 in rows and 1 in rows
    negative_controls.append({'p':p,'rank':3,'row_directions':4,'column_directions':4})

# Separate symbolic polynomial-division cross-check of the cyclotomic criterion.
import sympy as sp
x=sp.Symbol('x')
for p in (3,5,7,11):
    phi=sp.Poly(sp.cyclotomic_poly(p**3,x),x,domain=sp.ZZ)
    for j in range(6):
        if j==0:
            rows=cols=[0,p*p,2*p*p,1]
        else:
            rows=RNG.sample(range(p**3),4);cols=RNG.sample(range(p**3),4)
        co=det_poly(rows,cols,p**3)
        poly=sp.Poly.from_dict({(e,):c for e,c in co.items()},x,domain=sp.ZZ)
        assert zero_cyclotomic(co,p,3)==poly.rem(phi).is_zero
        counts['sympy_remainder_crosschecks']+=1

# Exact scalar cost and gap controls at N=1331.
N=1331;D=132;E=143;baseline=Fraction(D,N);gap=Fraction(1,484)
assert Fraction(3,44)+Fraction(44,N)==Fraction(49,484)==baseline+gap
assert Fraction(E,N)>baseline+gap
assert Fraction(16,N)>Fraction(49,484)**2
best=None;best_shapes=[]
for a in range(3,45):
    for b in range(a,min(N,3*N//a)+1):
        density=Fraction(3,a)+Fraction(3,b)
        assert density>=baseline+gap
        if best is None or density<best:best=density;best_shapes=[(a,b)]
        elif density==best:best_shapes.append((a,b))
        counts['rank3_scalar_shapes']+=1
assert best==Fraction(67,660) and best_shapes==[(44,90)]

# Full coset tiling: verify every entry exactly once, rank-one phase criterion,
# endpoint cost, tile area, and orientation-independent equality dimensions.
cover=bytearray(N*N);cost=0;tiles=0
for r in range(121):
    rows=range(r,N,121)
    for c in range(11):
        cols=range(c,N,11)
        assert len(rows)==11 and len(cols)==121
        assert ((rows[1]-rows[0])*(cols[1]-cols[0]))%N==0
        for row in rows:
            for col in cols:
                idx=row*N+col
                assert cover[idx]==0
                cover[idx]=1
        cost+=len(rows)+len(cols);tiles+=1
assert all(cover) and cost==175692 and tiles==N

# Independent integer divisor/sieve census using the retained old domains.
limit=10000
primes=[]
for n in range(2,limit+1):
    if all(n%p for p in primes if p*p<=n):primes.append(n)
residual=[];new1331=[]
for n in range(2,limit+1):
    ds=[d for d in range(1,int(n**.5)+1) if n%d==0]
    dn=min(d+n//d for d in ds)
    dominant=any(n%p==0 and n//p<p for p in primes if p<=n)
    old=dominant or dn*dn<12*n
    if not old:residual.append(n)
assert residual[0]==1331 and residual[1]==1859
assert [n for n in residual if n<=1858]==[1331]
assert 1859==11*13**2 and 156**2>12*1859 and 156**2<16*1859

results={
 'status':'PASS','arithmetic':'exact integer cyclotomic divisibility in characteristic zero',
 'counts':dict(counts),'lifted_cases_by_prime':sample_by_prime,
 'minimum_translation_symmetric_difference':minimum_symdiff,
 'negative_controls':negative_controls,
 'target':{'N':N,'cost':cost,'tiles':tiles,'entries_covered':len(cover),'published_gap':str(gap),
           'best_relaxed_integer_rank3_density':str(best),'best_relaxed_integer_shapes':best_shapes,
           'best_relaxed_integer_gap':str(best-baseline)},
 'old_residuals_through_10000':residual,'first_new_residual':1859,
 'seconds':round(time.time()-START,3)
}
(HERE/'RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
