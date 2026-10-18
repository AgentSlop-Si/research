#!/usr/bin/env python3
"""Fresh exact controls for the prime-cube rank-three separation proof.
No previous author/reviewer checker is imported. Exact determinants are evaluated
in Q[X]/Phi_(p^3)(X) by signed permutation sums and exact integer reductions.
"""
from itertools import combinations, permutations, product
from fractions import Fraction
from collections import Counter
from pathlib import Path
import hashlib, json, random, time

ROOT=Path(__file__).resolve().parent
START=time.time()
PERMS={}
for k in (2,3,4):
    PERMS[k]=[(perm,(-1)**sum(perm[i]>perm[j] for i in range(k) for j in range(i+1,k))) for perm in permutations(range(k))]

def determinant(p,R,C):
    N=p**3; q=p*p
    coeff=Counter()
    for perm,sign in PERMS[len(R)]:
        coeff[sum(R[i]*C[perm[i]] for i in range(len(R)))%N]+=sign
    bases={e%q for e,c in coeff.items() if c}
    rem={}
    for b in bases:
        last=coeff.get(b+(p-1)*q,0)
        for j in range(p-1):
            c=coeff.get(b+j*q,0)-last
            if c: rem[b+j*q]=c
    return rem

def nonzero(p,R,C):
    # Fast exact vanishing check for a signed polynomial modulo Phi_(p^3).
    N=p**3; q=p*p; coeff={}
    for perm,sign in PERMS[len(R)]:
        e=sum(R[i]*C[perm[i]] for i in range(len(R)))%N
        coeff[e]=coeff.get(e,0)+sign
    for e,c in coeff.items():
        if c:
            b=e%q
            if any(coeff.get(b+j*q,0)!=c for j in range(p)):
                return True
    return False

def check(p,R,C):
    assert len(set(x%(p*p) for x in R))==4
    assert len(set(x%(p*p) for x in C))==4
    assert nonzero(p,R,C), (p,R,C)

res={'status':'running','method':'Exact integer permutation sums modulo Phi_(p^3); no numerical ranks and no finite-field substitute.', 'independence':'Fresh checker; no accepted checker imports.'}

# Exhaust all canonical lower-two-digit B-B, B-C, C-C parameters at p=5.
p=5; pairs=list(combinations(range(p),2)); triples=list(combinations(range(p),3))
B=[tuple(p*x for x in u)+(t,) for u in triples for t in range(1,p)]
C=[tuple(p*x for x in v)+tuple(t+p*x for x in w) for v in pairs for w in pairs for t in range(1,p)]
counts={}
for label,left,right in [('B-B',B,B),('B-C',B,C),('C-C',C,C)]:
    count=0
    for R in left:
        for S in right:
            check(p,R,S); count+=1
    counts[label]=count
res['exhaustive_canonical_p5_minors']=counts
print('Exhaustive canonical p=5 exact minors:',counts,flush=True)

# Arbitrary high digits, translations and all ten unordered pattern pairings.
rng=random.Random(202610181338)
def build(p,typ):
    N=p**3
    if typ=='U':
        a=rng.sample(range(p),4); v=[x+p*rng.randrange(p*p) for x in a]
    elif typ=='A':
        a=rng.randrange(p); b=rng.sample(range(p),4)
        v=[a+p*x+p*p*rng.randrange(p) for x in b]
    elif typ=='B':
        a,t=rng.sample(range(p),2); b=rng.sample(range(p),3)
        v=[a+p*x+p*p*rng.randrange(p) for x in b]+[t+p*rng.randrange(p*p)]
    else:
        a,t=rng.sample(range(p),2); b=rng.sample(range(p),2); c=rng.sample(range(p),2)
        v=[a+p*x+p*p*rng.randrange(p) for x in b]+[t+p*x+p*p*rng.randrange(p) for x in c]
    shift=rng.randrange(N)
    return [(x+shift)%N for x in v]
patcounts={}
for p in (5,7,11,13,17):
    n=0
    for i,T in enumerate('UABC'):
        for S in 'UABC'[i:]:
            for _ in range(1000):
                check(p,build(p,T),build(p,S)); n+=1
    patcounts[str(p)]=n
res['arbitrary_high_digit_pattern_minors']=patcounts
print('Arbitrary high-digit exact minors:',patcounts,flush=True)

# Verify the mixed-case finite group lemma exhaustively, rather than sampling.
trans={}
for p in (5,7,11,13,17,19):
    n=0
    for xx in combinations(range(p),3):
        X=set(xx)
        for d in range(1,p):
            Y={(x+d)%p for x in X}
            assert X!=Y and X.symmetric_difference(Y)
            n+=1
    trans[str(p)]=n
res['translation_obstruction_exhaustive']=trans

# Exact integer occupancy patterns of five selected representatives.
patterns=[]
def parts(n,lo=1):
    if n==0:yield ()
    for k in range(lo,n+1):
        for tail in parts(n-k,k):yield (k,)+tail
for z in parts(5):
    if len(z)>=4:typ='U'
    elif max(z)>=4:typ='A'
    elif max(z)>=3:typ='B'
    else:assert sum(v==2 for v in z)>=2;typ='C'
    patterns.append({'occupancy':list(z),'selected_type':typ})
res['five_point_selection_patterns']=patterns

# Independently cross-check the permutation reduction with SymPy exact
# polynomial remainder for representative high-digit and translated examples.
import sympy as sp
X=sp.Symbol('X'); independent=0
for p in (5,11):
    phi=sp.Poly(sp.cyclotomic_poly(p**3,X),X,domain=sp.ZZ)
    for T in 'UABC':
        for S in 'UABC':
            R=build(p,T); Cc=build(p,S); coeff=Counter()
            for perm,sign in PERMS[4]:
                coeff[sum(R[i]*Cc[perm[i]] for i in range(4))%(p**3)]+=sign
            poly=sp.Poly.from_dict({(e,):c for e,c in coeff.items() if c},X,domain=sp.ZZ)
            rr=poly.rem(phi)
            expected=determinant(p,R,Cc)
            assert {(e[0]):int(c) for e,c in rr.terms()}==expected
            assert not rr.is_zero
            independent+=1
res['sympy_independent_polynomial_remainders']=independent

# Target scalar consequences; no claim that scalar feasible shapes exist.
N=1331; D=132; gap=Fraction(1,484); target=Fraction(D,N)
assert Fraction(3,44)+Fraction(44,N)==target+gap==Fraction(49,484)
assert 44*44<3*N
shapes=0; least=None; minimizers=[]
for a in range(3,45):
    for b in range(a,min(N,(3*N)//a)+1):
        rho=Fraction(3,a)+Fraction(3,b)
        assert rho>=target+gap
        shapes+=1
        if least is None or rho<least:least=rho;minimizers=[[a,b]]
        elif rho==least:minimizers.append([a,b])
assert Fraction(143,N)>target+gap
assert Fraction(16,N)>(target+gap)**2
assert 63*63<=3*N and Fraction(6,63)<target and 63>44
res['target_scalar_checks']={'N':N,'D':D,'optimum':N*D,'rank_three_side_bound':44,'rank_three_shapes':shapes,'analytic_density_floor':str(target+gap),'higher_rank_area_gap':str(gap),'integer_scalar_minimum_density':str(least),'integer_scalar_minimizers':minimizers,'former_63_square_excluded':True}

# Explicit N-tile coset partition and entrywise once-only coverage.
coverage=bytearray(N*N); tiles=0; cost=0
for u in range(121):
    R=[u+121*k for k in range(11)]
    for v in range(11):
        Cc=[v+11*k for k in range(121)]
        assert all(((r-R[0])*(c-Cc[0]))%N==0 for r in R for c in Cc)
        for r in R:
            off=r*N
            for c in Cc:
                idx=off+c; assert coverage[idx]==0;coverage[idx]=1
        tiles+=1;cost+=len(R)+len(Cc)
assert all(coverage) and tiles==N and cost==175692
res['target_partition']={'tiles':tiles,'coverage_entries':len(coverage),'minimum_coverage':min(coverage),'maximum_coverage':max(coverage),'cost':cost,'tile_shape':[11,121],'rank_certificate':'All exact multiplicative plaquettes divisible by N.'}

# Actual Fourier rank-three negative control: four projective classes each side.
p=11; R=[0,p*p,2*p*p,1]; Cc=R[:]; small=[0,p*p,1]
assert not nonzero(p,R,Cc) and nonzero(p,small,small)
assert all(any(((r-s)*(c-Cc[0]))%(p**3) for c in Cc) for r,s in combinations(R,2))
assert all(any(((c-d)*(r-R[0]))%(p**3) for r in R) for c,d in combinations(Cc,2))
refinements=[(R[:3],Cc[:3]),(R[:3],Cc[3:]),(R[3:],Cc)]
seen=set()
for rr,cc in refinements:
    assert all(((r-rr[0])*(c-cc[0]))%(p**3)==0 for r in rr for c in cc)
    for rc in product(rr,cc): assert rc not in seen;seen.add(rc)
assert seen==set(product(R,Cc))
refcost=sum(len(r)+len(c) for r,c in refinements)
assert refcost==15<24
res['four_class_rank_three_negative_control']={'N':p**3,'rows':R,'columns':Cc,'rank':3,'projective_row_classes':4,'projective_column_classes':4,'nonzero_3_minor_remainder':determinant(p,small,small),'original_cost':24,'rank_one_refinement_cost':refcost,'refinement_tiles':3}

# Independent census of accepted domains plus precisely this new target.
def divisors(n):return [d for d in range(1,n+1) if n%d==0]
def primes(n):
    out=[]; d=2
    while d*d<=n:
        if n%d==0:
            out.append(d)
            while n%d==0:n//=d
        d+=1
    if n>1:out.append(n)
    return out
old=[];new=[]
for n in range(2,10001):
    DD=min(d+n//d for d in divisors(n))
    accepted=DD*DD<12*n or any(p>n//p for p in primes(n))
    if not accepted:old.append(n)
    if not accepted and n!=1331:new.append(n)
assert old[0]==1331 and new[0]==1859 and len(old)==25 and len(new)==24
NN=1859; DD=min(d+NN//d for d in divisors(NN))
assert DD==156 and 12*NN<DD*DD<16*NN
res['domain_census_through_10000']={'previous_residuals':old,'newly_settled':[1331],'remaining_residuals':new,'all_lengths_through':1858,'next_N':1859,'next_D':156,'next_first_problematic_rank':3}
res['status']='passed';res['elapsed_seconds']=round(time.time()-START,3);res['sympy_version']=sp.__version__
(ROOT/'RESULTS.json').write_text(json.dumps(res,indent=2)+'\n')
print('Target optimum:',N*D,'; exact area penalty:',gap,flush=True)
print('Scalar shapes:',shapes,'; minimum scalar density:',least,'at',minimizers,flush=True)
print('Explicit tiles:',tiles,'; entries covered exactly once:',len(coverage),flush=True)
print('Next residual:',new[0],'; remaining through 10000:',len(new),flush=True)
print('All exact controls passed in',res['elapsed_seconds'],'seconds.',flush=True)
