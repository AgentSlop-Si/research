#!/usr/bin/env python3
"""Fresh exact controls for the sharp prime-cube rank-three side/density theorem.
No accepted author or reviewer checker is imported or executed. All Fourier
minors use integer signed permutation sums and exact reduction modulo Phi_(p^m).
Finite controls supplement the universal proof in REPORT.md.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations, product
from math import isqrt
from pathlib import Path
import hashlib, json, random, time

ROOT=Path(__file__).resolve().parent
START=time.time(); RNG=random.Random(202610181748)
COUNTS=Counter(); CERTS=[]
PERMS={k:[(s,(-1)**sum(s[i]>s[j] for i in range(k) for j in range(i+1,k))) for s in permutations(range(k))] for k in range(1,5)}

def det_terms(N,R,C):
    assert len(R)==len(C) and len(R)<=4
    D=Counter()
    for s,sign in PERMS[len(R)]:
        D[sum(r*C[s[i]] for i,r in enumerate(R))%N]+=sign
    return {e:v for e,v in D.items() if v}

def reduced(p,m,D):
    # Phi_(p^m)(X)=sum_(j=0)^(p-1) X^(j*p^(m-1)).
    # Reducing the coefficient of the last power in each residue fiber is exact.
    base=p**(m-1); out={}
    for b in {e%base for e in D}:
        last=D.get(b+(p-1)*base,0)
        for j in range(p-1):
            v=D.get(b+j*base,0)-last
            if v:out[b+j*base]=v
    return out

def nz(p,m,R,C):
    COUNTS[f'order_p{m}_determinants']+=1
    return bool(reduced(p,m,det_terms(p**m,R,C)))

def basis_rows(p,m,R,C):
    B=[]
    for r in R:
        T=B+[r]
        if any(nz(p,m,T,S) for S in combinations(C,len(T))):B=T
        if len(B)==len(C):return B
    return B

def find_four(p,R,C):
    for T in combinations(C,4):
        B=basis_rows(p,3,R,T)
        if len(B)==4:return B,list(T)
    raise AssertionError(('No independent four-minor',p,R,C))

def prime(n):return n>1 and all(n%d for d in range(2,isqrt(n)+1))
def divisors(n):
    small=[d for d in range(1,isqrt(n)+1) if n%d==0]
    return sorted(set(small+[n//d for d in small]))

def compositions(n,t):
    if t==1:yield (n,);return
    for i in range(1,n-t+2):
        for tail in compositions(n-i,t-1):yield (i,)+tail

res={'status':'running','method':'Exact characteristic-zero cyclotomic remainders, integer/rational inequalities, and explicit entry coverage. No numerical or finite-field rank substitute.','proof':'REPORT.md contains the universal proof. Samples do not enumerate all rectangles.'}

# Exhaust all column sets of size <=4 at F25 against one specified row set
# just beyond the sharp short-support zero threshold.
exhaust={}
for k in (1,2,3,4):
    A=[r for r in range(25) if r%5<k-1]+[k-1]
    count=0
    for C in combinations(range(25),k):
        assert len(basis_rows(5,2,A,C))==k
        count+=1
    exhaust[str(k)]={'column_sets':count,'row_count':len(A)}
res['exhaustive_F25_boundary_column_sets']=exhaust
print('F25 exhaustive boundary controls',exhaust,flush=True)

# Arbitrary high digits and different concentrated / random row patterns.
short={}
for p in (5,7,11,13,17,19):
    count=0
    for k in (2,3,4):
        for j in range(200):
            if j%2:
                A=RNG.sample(range(p*p),(k-1)*p+1)
            else:
                ys=RNG.sample(range(p),k)
                A=[y+p*z for y in ys[:-1] for z in range(p)]
                A += [ys[-1]+p*RNG.randrange(p)]
                RNG.shuffle(A)
            C=RNG.sample(range(p*p),k)
            assert len(basis_rows(p,2,A,C))==k
            count+=1
    short[str(p)]=count
res['prime_square_short_support_samples']=short

zero_envelopes=0
for p in (5,7,11,13,17,19):
    for k in range(1,min(8,p)+1):
        for t in range(1,k+1):
            for kv in compositions(k,t):
                for z0 in range(min(kv)):
                    assert z0*p+(p-z0)*(t-1)<=(k-1)*p
                    zero_envelopes+=1
res['short_support_zero_count_envelopes']=zero_envelopes

# Critical strengthened two-residue argument: both the 3+1 and 2+2 branches.
direct={}
for p in (5,7,11,13,17,19):
    cnt=Counter()
    for branch in ('3+1','2+2'):
        for j in range(200):
            y0,y1=RNG.sample(range(p),2)
            sizes=(2*p+1,p) if branch=='3+1' else (p+1,2*p)
            AA=[RNG.sample(range(p*p),v) for v in sizes]
            T=RNG.sample(range(p*p),3)
            R=[]
            for y,A,k in zip((y0,y1),AA,(3,1) if branch=='3+1' else (2,2)):
                B=basis_rows(p,2,A,T[:k]);assert len(B)==k
                R += [y+p*u for u in B]
            C=[v+p*p*w for v in T for w in RNG.sample(range(p),2)]
            B,S=find_four(p,R,C)
            if p==13:CERTS.append({'branch':branch,'p':p,'rows':B,'columns':S,'nonzero_remainder':reduced(p,3,det_terms(p**3,B,S))})
            cnt[branch]+=1
    direct[str(p)]=dict(cnt)
res['two_residue_direct_sum_samples']=direct
print('Two-residue direct sums',direct,flush=True)

# Exhaust every ordered four-fiber occupancy and every two-class size split
# in the theorem's critical range for the stated primes.
occupancy={};split={}
for p in (5,7,11,13,17,19):
    n=0
    for u in product(range(1,p+1),repeat=4):
        if sum(u)>3*p:
            assert sum(x>=2 for x in u)>=3
            assert max(u)>=3
            n+=1
    occupancy[str(p)]=n
    n=0
    for x in range(1,p*p+1):
        for y in range(1,p*p+1):
            if x+y>3*p:
                assert max(x,y)>2*p or min(x,y)>p
                n+=1
    split[str(p)]=n
    for d in (1,p,p*p,p**3):
        if 3*d>3*p:assert p**3//d<=p
res['four_fiber_occupancy_enumerations']=occupancy
res['two_class_size_split_enumerations']=split

# Genuine three-projective-class rank-three rectangles, on either divisor
# boundary. Structural rank <=3 and exact 3-minor; many exact vanishing 4-minors.
rigidity={}
for p in (5,7,11,13,17,19):
    zs=0
    for d in (p,p*p):
        N=p**3
        R=[u+(N//d)*j for u in (0,1,2) for j in range(d)]
        C=[d*j for j in range(N//d)]
        assert len(R)==3*d and len(C)==N//d
        assert nz(p,3,[0,1,2],[0,d,2*d])
        # Rows in each K-coset differ by annihilating increments.
        assert all(((N//d)*j*d)%N==0 for j in range(d))
        for _ in range(200):
            assert not nz(p,3,RNG.sample(R,4),RNG.sample(C,4))
            zs+=1
    rigidity[str(p)]=zs
res['three_class_rigidity_vanishing_four_minors']=rigidity

# Sharpness for all tested primes: R=pZ, C=three full fibers modulo p².
sharp=[]
for p in [v for v in range(5,1001) if prime(v)]:
    N=p**3
    assert Fraction(3,3*p)+Fraction(3,p*p)==Fraction(p+3,p*p)
    assert (3*p)*(p*p)==3*N
    assert 3*p<=p*p
    # Three column classes yield at most three directions; a universal minor
    # certifies actual rank three with the chosen representative columns.
    assert nz(p,2,[0,1,2],[0,1,2])
    sharp.append(p)
res['sharp_rank_three_density_family_checks']={'prime_count':len(sharp),'first_prime':sharp[0],'last_prime':sharp[-1],'density':'(p+3)/p^2','side_sizes':['3p','p^2']}

# The target scalar relaxation, plus every formerly obstructive shape.
p=13;N=p**3;D=p+p*p;base=Fraction(D,N);gap=Fraction(1,676)
assert N*D==399854
assert min(d+N//d for d in divisors(N))==D
assert min(2*d+N//d for d in divisors(N) if d<N)==195
assert Fraction(195,N)-base==Fraction(1,169)>gap
assert Fraction(16,169)-base==Fraction(2,169)>gap
assert Fraction(16,N)>(base+gap)**2
scalar=0;floor=None;mins=[];formerly=[]
for a in range(1,4*p+1):
    for b in range(a,min(N,3*N//a)+1):
        den=Fraction(3*(a+b),a*b)
        if a<=3*p:
            assert den>=Fraction(16,169)
            if floor is None or den<floor:floor=den;mins=[(a,b)]
            elif den==floor:mins.append((a,b))
            scalar+=1
        elif den<=base:formerly.append((a,b))
assert floor==Fraction(16,169) and mins==[(39,169)]
assert formerly and all(a>39 for a,b in formerly)
res['N2197_density_controls']={'N':N,'D':D,'optimal_cost':N*D,'rank_three_scalar_shapes':scalar,'rank_three_minimum':str(floor),'minimizing_shapes':mins,'rank_two_floor':str(Fraction(195,N)),'higher_rank_area_penalty':str(gap),'former_scalar_obstruction_count':len(formerly),'former_scalar_obstructions':formerly}

# Explicit full rank-one coset partition, checking every entry and phase.
coverage=bytearray(N*N);tiles=0;cost=0
for u in range(p*p):
    R=[u+p*p*j for j in range(p)]
    for v in range(p):
        C=[v+p*j for j in range(p*p)]
        for r in R:
            for c in C:
                assert ((r-R[0])*(c-C[0]))%N==0
                pos=r*N+c
                assert not coverage[pos]
                coverage[pos]=1
        tiles+=1;cost+=len(R)+len(C)
assert all(coverage) and tiles==N and cost==399854
res['target_coset_partition']={'N':N,'tiles':tiles,'entries_covered_once':len(coverage),'cost':cost,'unordered_side_sizes':[p,p*p]}
print('N2197 exact density and full tiling controls passed',flush=True)

# Recompute the accepted-domain union independently, then add exactly 2197.
old=[];new=[];added=[]
for n in range(2,10001):
    ds=divisors(n);dn=min(d+n//d for d in ds)
    balanced=dn*dn<12*n
    dominant=any(prime(d) and d>n//d for d in ds)
    q=isqrt(n//11) if n%11==0 else 0
    mixed=11*q*q==n and q>11 and prime(q)
    prior=balanced or dominant or n==1331 or mixed
    if not prior:old.append(n)
    if not prior and n==2197:added.append(n)
    if not prior and n!=2197:new.append(n)
assert old[0]==2197 and added==[2197] and new[0]==2873
n=new[0];dn=min(d+n//d for d in divisors(n))
assert n==13*13*17 and dn==186 and 12*n<dn*dn<16*n
res['domain_census_through_10000']={'previous_residuals':old,'newly_settled':added,'remaining_residuals':new,'all_lengths_through':2872,'next_N':n,'next_factorization':'13^2 * 17','next_D':dn,'next_problematic_rank':3}

# Separately implemented polynomial-division cross-checks, including zero cases.
import sympy as sp
X=sp.symbols('X');cross=0
for p in (5,7,11,13,17,19):
    for m in (1,2,3):
        phi=sp.Poly(sp.cyclotomic_poly(p**m,X),X,domain=sp.ZZ)
        for k in (2,3,4):
            for j in range(2):
                RR=RNG.sample(range(p**m),k);CC=RNG.sample(range(p**m),k)
                if j and m>1:
                    RR=[p**(m-1)*i for i in range(k)];CC=[p*i for i in range(k)]
                terms=det_terms(p**m,RR,CC)
                poly=sp.Poly.from_dict({(e,):v for e,v in terms.items()},X,domain=sp.ZZ)
                rem=poly.rem(phi)
                expected={e[0]:int(v) for e,v in rem.terms()} if not rem.is_zero else {}
                assert expected==reduced(p,m,terms)
                cross+=1
res['independent_sympy_remainder_crosschecks']=cross
res['determinant_evaluation_counts']=dict(COUNTS)
res['status']='all_passed';res['elapsed_seconds']=round(time.time()-START,3)
(ROOT/'TARGET_MINOR_CERTIFICATES.json').write_text(json.dumps(CERTS,indent=2)+'\n')
(ROOT/'RESULTS.json').write_text(json.dumps(res,indent=2)+'\n')
print('ALL PASSED',json.dumps({'elapsed_seconds':res['elapsed_seconds'],'counts':dict(COUNTS),'target_minor_certificates':len(CERTS),'next_residual':2873}),flush=True)
