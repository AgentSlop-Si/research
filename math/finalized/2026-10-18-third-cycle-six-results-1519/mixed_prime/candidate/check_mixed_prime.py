#!/usr/bin/env python3
"""Fresh exact controls, independent of all earlier author/reviewer checkers.
Integer determinant sums are reduced in characteristic-zero cyclotomic fields.
For mixed pq^m use the tensor basis of Q(zeta_p) and Q(zeta_(q^m)).
Finite samples are supplementary controls, never the universal proof.
"""
from itertools import combinations, permutations, product
from collections import Counter
from fractions import Fraction
from pathlib import Path
import hashlib, json, random, time

ROOT=Path(__file__).resolve().parent
START=time.time()
RNG=random.Random(202610181501)
PERMS={k:[(v,(-1)**sum(v[i]>v[j] for i in range(k) for j in range(i+1,k))) for v in permutations(range(k))] for k in range(1,5)}
COUNTS=Counter()

def terms(N,R,C):
    assert len(R)==len(C)<=4
    out=Counter()
    for v,sgn in PERMS[len(R)]:
        out[sum(r*C[v[i]] for i,r in enumerate(R))%N]+=sgn
    return {k:v for k,v in out.items() if v}

class Cyclo:
    def __init__(self,p,q,m=1):
        assert p!=q
        self.p,self.q,self.m=p,q,m
        self.n=p*q**m
        self.base=q**(m-1)
        aa=pow(q**m,-1,p);bb=pow(p,-1,q**m)
        self.crt=[(e*aa%p,e*bb%(q**m)) for e in range(self.n)]
    def nonzero_terms(self,D):
        # Each b gives a p-by-q integer coefficient matrix. Reducing both
        # 1+alpha+...+alpha^(p-1) and 1+beta^base+...+beta^((q-1)base)
        # is exactly its double-centering against the last row/column.
        mats={}
        for e,c in D.items():
            u,v=self.crt[e];b=v%self.base;j=v//self.base
            mats.setdefault(b,Counter())[u,j]+=c
        for M in mats.values():
            last=M[self.p-1,self.q-1]
            for u in range(self.p-1):
                for j in range(self.q-1):
                    if M[u,j]-M[self.p-1,j]-M[u,self.q-1]+last:
                        return True
        return False
    def nz(self,R,C):
        COUNTS['mixed_exact_determinants']+=1
        return self.nonzero_terms(terms(self.n,R,C))

def primepower_nz(q,m,R,C):
    N=q**m;base=N//q;D=terms(N,R,C)
    COUNTS['prime_power_exact_determinants']+=1
    for b in {e%base for e in D}:
        v=D.get(b+(q-1)*base,0)
        if any(D.get(b+j*base,0)!=v for j in range(q-1)):
            return True
    return False

def rank_basis(ctx,R,C,k=None):
    """Greedy exact row-basis certificate; returns independent selected rows.
    Only used with at most four columns, so determinant sizes never exceed 4.
    """
    if k is None:k=len(C)
    basis=[]
    for r in R:
        S=basis+[r]
        if any(ctx.nz(S,D) for D in combinations(C,len(S))):
            basis=S
            if len(basis)==k:return basis
    return basis

res={'status':'running','method':'Exact characteristic-zero cyclotomic determinant reduction. No numerical rank or finite-field substitution.','proof':'REPORT.md contains the universal proof; finite samples supplement it.'}

# Universal square-order minor: rows arbitrary distinct, columns distinct mod q.
univ={}
for q in (5,7,11,13,17,19):
    n=0
    for k in (2,3,4):
        for _ in range(400):
            R=RNG.sample(range(q*q),k)
            C=[v+q*RNG.randrange(q) for v in RNG.sample(range(q),k)]
            assert primepower_nz(q,2,R,C),(q,R,C)
            n+=1
    univ[str(q)]=n
res['prime_square_universal_minors']=univ
print('Prime-square universal exact minors',univ,flush=True)

# Exhaust every k-column set at pq=35 against a fixed near-extremal row set
# of size (k-1)q+1: all rows from k-1 full p-residue fibers and one new row.
ctx=Cyclo(5,7)
exhaust={}
for k in (2,3,4):
    A=[r for r in range(35) if r%5<k-1]+[k-1]
    assert len(A)==(k-1)*7+1
    n=0
    for C in combinations(range(35),k):
        B=rank_basis(ctx,A,C)
        assert len(B)==k,(A,C,B)
        n+=1
    exhaust[str(k)]={'column_sets':n,'row_count':len(A)}
res['exhaustive_semiprime_boundary_column_sets_N35']=exhaust
print('Exhaustive F35 boundary column sets',exhaust,flush=True)

# All combinatorial zero-count envelopes used in the short-support proof.
envelopes=0
def compositions(n,t):
    if t==1:
        yield (n,);return
    for v in range(1,n-t+2):
        for tail in compositions(n-v,t-1):yield (v,)+tail
for p,q in ((5,7),(5,11),(7,11),(11,13),(11,17),(13,17),(17,19),(19,23)):
    for k in range(1,min(p,8)+1):
        for t in range(1,k+1):
            for kv in compositions(k,t):
                for z0 in range(min(kv)):
                    bound=z0*q+(p-z0)*(t-1)
                    assert bound<=(k-1)*q
                    envelopes+=1
res['exhaustive_short_support_zero_count_envelopes']=envelopes

# Independent exact arbitrary and boundary semiprime full-column-rank controls.
semis={}
for p,q in ((5,7),(7,11),(11,13),(11,17),(13,17),(17,19)):
    cc=Cyclo(p,q);count=0
    for k in (3,4):
        for i in range(300):
            if i%2:
                A=RNG.sample(range(p*q),(k-1)*q+1)
            else:
                xs=RNG.sample(range(p),k)
                A=[r for r in range(p*q) if r%p in xs[:-1]]
                A += [xs[-1]+p*RNG.randrange(q)]
                RNG.shuffle(A)
            C=RNG.sample(range(p*q),k)
            assert len(rank_basis(cc,A,C))==k,(p,q,A,C)
            count+=1
    semis[f'{p}x{q}']=count
res['arbitrary_semiprime_short_support_rank_controls']=semis
print('Semiprime rank controls',semis,flush=True)

# Extract real four-by-four minors in the two-residue direct-sum case.
# The large row class has exactly 2q+1 rows; the other contains one row.
# Three rich fibers, each with two columns, supply the separated subspaces.
direct={}
for p,q in ((5,7),(7,11),(11,13),(11,17),(13,17),(17,19)):
    low=Cyclo(p,q);high=Cyclo(p,q,2);count=0
    for i in range(300):
        y0,y1=RNG.sample(range(q),2)
        if i%2:
            A=RNG.sample(range(p*q),2*q+1)
        else:
            x=RNG.sample(range(p),3)
            A=[a for a in range(p*q) if a%p in x[:2]]+[x[2]+p*RNG.randrange(q)]
            RNG.shuffle(A)
        T=RNG.sample(range(p*q),3)
        AA=rank_basis(low,A,T)
        assert len(AA)==3
        RR=[y0+q*a for a in AA]+[y1+q*RNG.randrange(p*q)]
        CC=[v+p*q*w for v in T for w in RNG.sample(range(q),2)]
        witness=next((D for D in combinations(CC,4) if high.nz(RR,D)),None)
        assert witness is not None,(p,q,RR,CC)
        count+=1
    direct[f'{p}x{q}²']=count
res['two_residue_direct_sum_exact_four_minors']=direct
print('Two-residue separated four-minors',direct,flush=True)

# Exact three-residue invertibility and projective-rank-three positive controls.
# R is a union of three order-q cosets, C the full order-pq annihilator.
rankthree={}
for p,q in ((5,7),(7,11),(11,13),(11,17),(13,17),(17,19)):
    cc=Cyclo(p,q,2);N=p*q*q
    labels=RNG.sample(range(q),3)
    R=[s+p*q*j for s in labels for j in range(q)]
    C=[q*j for j in range(p*q)]
    # Projective row-class count is exactly 3 (classes modulo pq).
    assert len({r%(p*q) for r in R})==3
    # All rows in a coset agree on C; nonzero 3-minor certifies exact rank.
    assert cc.nz(labels,[0,p*q,2*p*q])
    zero=0
    for _ in range(400):
        RR=RNG.sample(R,4);CC=RNG.sample(C,4)
        assert not cc.nz(RR,CC),(p,q,RR,CC)
        zero+=1
    rankthree[f'{p}x{q}²']={'shape':[len(R),len(C)],'rank':3,'zero_four_minors':zero}
res['genuine_rank_three_coset_controls']=rankthree

# Counterexample to the direct mixed-prime occupancy analogue, exact all-ones.
neg=[]
for p,q in ((5,7),(7,11),(11,13),(11,17),(13,17)):
    N=p*q*q;R=[q*q*j for j in range(p)];C=[p*j for j in range(q*q)]
    assert all(r*c%N==0 for r in R for c in C)
    assert len({r%(p*q) for r in R})==p
    assert len({c%(p*q) for c in C})==q
    neg.append({'p':p,'q':q,'shape':[p,q*q],'rank':1,'occupancies_mod_pq':[p,q]})
res['mixed_occupancy_negative_controls']=neg

# Exact target density audit, both dichotomy branches and all bad scalar shapes.
N=1859;D=156;floor=Fraction(49,572);delta=Fraction(1,572)
assert floor-Fraction(D,N)==delta
cnt=0;minimum=None;bad=[];dichotomy_excluded=[]
for a in range(3,int((3*N)**.5)+1):
    for b in range(a,min(N,3*N//a)+1):
        density=Fraction(3*(a+b),a*b)
        admissible=a<=52 or b<=66
        if admissible:
            assert density>=floor
            cnt+=1
            if minimum is None or density<minimum[0]:minimum=(density,a,b)
        if density<=Fraction(D,N):
            bad.append([a,b]);assert not admissible
            dichotomy_excluded.append([a,b])
assert len(bad)==94
res['target_rank_three_scalar_audit']={'admissible_shapes':cnt,'minimum_density':str(minimum[0]),'minimum_shape':list(minimum[1:]),'formerly_bad_shapes':len(bad),'formerly_bad_shapes_all_excluded':True,'bad_shapes':bad}

# Actual four-minor witnesses at every one of the 94 formerly obstructive
# target scalar shapes, under every pair of 1,2,3,4 low-q residue occupancies.
def residue_sample(n,q,occ,size):
    labels=RNG.sample(range(q),occ)
    forced=[v+q*RNG.randrange(n//q) for v in labels]
    pool=[r for r in range(n) if r%q in labels and r not in forced]
    ans=forced+RNG.sample(pool,size-occ)
    RNG.shuffle(ans)
    return ans

def buckets(S,mod):
    out={}
    for x in S:out.setdefault(x%mod,[]).append(x)
    return out

def four_witness(p,q,R,C):
    N=p*q*q;high=Cyclo(p,q,2);low=Cyclo(p,q)
    rr=buckets(R,q);cc=buckets(C,q)
    if len(cc)>=4:
        row=next(v[:4] for v in buckets(R,p).values() if len(v)>=4)
        col=[v[0] for v in list(cc.values())[:4]]
        branch='four-column-residues'
    elif len(rr)>=4:
        col=next(v[:4] for v in buckets(C,p).values() if len(v)>=4)
        row=[v[0] for v in list(rr.values())[:4]]
        branch='four-row-residues'
    elif len(rr)==1:
        y=next(iter(rr));AA=[(r-y)//q for r in R]
        fibers=buckets(C,p*q)
        col=[v[0] for v in list(fibers.values())[:4]]
        basis=rank_basis(low,AA,[c%(p*q) for c in col])
        assert len(basis)==4
        row=[y+q*a for a in basis];branch='one-row-residue'
    elif len(rr)==2:
        y=max(rr,key=lambda k:len(rr[k]));other=next(k for k in rr if k!=y)
        AA=[(r-y)//q for r in rr[y]]
        rich=[(v,items[:2]) for v,items in buckets(C,p*q).items() if len(items)>=2][:3]
        assert len(rich)==3 and len(AA)>2*q
        basis=rank_basis(low,AA,[v for v,_ in rich]);assert len(basis)==3
        row=[y+q*a for a in basis]+[rr[other][0]]
        col=next(list(D) for D in combinations([x for _,items in rich for x in items],4) if high.nz(row,D))
        branch='two-row-residues'
    else:
        assert len(rr)==3
        baseC=next(v[:3] for v in buckets(C,p*q).values() if len(v)>=3)
        baseR=[v[0] for v in rr.values()]
        assert high.nz(baseR,baseC)
        result=next(((baseR+[r],baseC+[c]) for r in R if r not in baseR for c in C if c not in baseC and high.nz(baseR+[r],baseC+[c])),None)
        assert result is not None
        row,col=result;branch='three-row-residues'
    assert high.nz(row,col)
    assert set(row)<=set(R) and set(col)<=set(C)
    return row,col,branch

witnesses=[];branches=Counter()
for a,b in bad:
    for s,t in product(range(1,5),repeat=2):
        R=residue_sample(1859,13,s,a);C=residue_sample(1859,13,t,b)
        row,col,branch=four_witness(11,13,R,C)
        branches[branch]+=1
        witnesses.append({'shape':[a,b],'residue_occupancies':[s,t],'row_minor':row,'column_minor':col,'proof_branch':branch})
(ROOT/'TARGET_MINOR_CERTIFICATES.json').write_text(json.dumps(witnesses,indent=2)+'\n')
res['target_obstructive_shape_four_minor_witnesses']={'shapes':len(bad),'occupancy_pairs_per_shape':16,'total_certificates':len(witnesses),'branches':dict(branches),'certificate_file':'TARGET_MINOR_CERTIFICATES.json'}
print('Target shape actual four-minor certificates',res['target_obstructive_shape_four_minor_witnesses'],flush=True)

def prime(n):
    return n>=2 and all(n%d for d in range(2,int(n**.5)+1))
def divisors(n):
    return [d for d in range(1,n+1) if n%d==0]
family=[]
for q in [n for n in range(13,1000) if prime(n)]:
    N=11*q*q;ds=divisors(N) if q<40 else [1,11,q,11*q,q*q,N]
    B=max(66,31+2*q,3*q)
    assert 49*B<=264*q
    assert min(d+N//d for d in ds)==12*q
    assert min(2*d+N//d for d in ds if d<N)==13*q
    assert Fraction(3,4*q)+Fraction(4*q,N)==Fraction(49,44*q)
    assert Fraction(13,11*q)>Fraction(49,44*q)
    family.append(q)
assert 16*1936>11*2401
res['family_exact_divisor_density_controls']={'primes_q_through_1000':len(family),'first_q':family[0],'last_q':family[-1]}

# Full target partition, explicit exact coverage and rank-one plaquette phases.
p=11;q=13;N=p*q*q;D=12*q
rows=[[u+p*q*j for j in range(q)] for u in range(p*q)]
cols=[[v+q*j for j in range(p*q)] for v in range(q)]
coverage=bytearray(N*N);tiles=0;cost=0
for R in rows:
    for C in cols:
        assert len(R)==q and len(C)==p*q
        assert all(((r-R[0])*(c-C[0]))%N==0 for r in R for c in C)
        for r in R:
            for c in C:
                pos=r*N+c
                assert coverage[pos]==0
                coverage[pos]=1
        tiles+=1;cost+=len(R)+len(C)
assert all(coverage) and tiles==N and cost==290004
res['target_full_coset_tiling']={'N':N,'tiles':tiles,'entries_covered_once':len(coverage),'cost':cost,'side_sizes':[q,p*q]}
print('Full target coset tiling',res['target_full_coset_tiling'],flush=True)

# Fresh accepted-domain census; no prior checker or previous result imported.
old=[];new=[];added=[]
for n in range(2,10001):
    ds=divisors(n);d=min(x+n//x for x in ds)
    balanced=d*d<12*n
    dominant=any(prime(x) and x>n//x for x in ds)
    prior=balanced or dominant or n==1331
    r=int((n//11)**.5) if n%11==0 else 0
    added_family=(11*r*r==n and r>11 and prime(r))
    if not prior:old.append(n)
    if not prior and added_family:added.append(n)
    if not(prior or added_family):new.append(n)
assert old[0]==1859 and new[0]==2197
assert added==[1859,3179,3971,5819,9251]
assert Fraction(3,52)+Fraction(52,2197)==Fraction(55,676)<Fraction(182,2197)
assert 52*126<=3*2197 and Fraction(3*(52+126),52*126)<Fraction(182,2197)
res['domain_census_through_10000']={'previous_residuals':old,'newly_settled':added,'remaining_residuals':new,'all_lengths_through':2196,'next_N':2197,'next_D':182,'next_problematic_rank':3,'next_scalar_obstruction':{'a':52,'b':126,'rank_relaxation':3,'area':6552,'density':'89/1092'}}

# Independent SymPy polynomial-remainder verification of the evaluator.
import sympy as sp
X=sp.symbols('X');cross=0
for p,q,m in ((5,7,1),(5,7,2),(7,11,1),(11,13,1),(11,13,2),(13,17,1)):
    cc=Cyclo(p,q,m);phi=sp.Poly(sp.cyclotomic_poly(cc.n,X),X,domain=sp.ZZ)
    for k in (2,3,4):
        for j in range(2):
            R=RNG.sample(range(cc.n),k);C=RNG.sample(range(cc.n),k)
            if j and k==4:
                # A deliberately singular choice with four rows in a subgroup
                # and columns in its annihilator whenever the sizes permit it.
                R=[cc.n//p*i for i in range(k)];C=[p*i for i in range(k)]
            dd=terms(cc.n,R,C)
            pol=sp.Poly.from_dict({(e,):v for e,v in dd.items()},X,domain=sp.ZZ)
            symbolic=not pol.rem(phi).is_zero
            assert symbolic==cc.nonzero_terms(dd),(p,q,m,R,C)
            cross+=1
res['sympy_independent_remainder_crosschecks']=cross
res['determinant_evaluation_counts']=dict(COUNTS)
res['status']='all_passed';res['elapsed_seconds']=round(time.time()-START,3)
(ROOT/'RESULTS.json').write_text(json.dumps(res,indent=2)+'\n')
print('ALL PASSED',json.dumps({'elapsed_seconds':res['elapsed_seconds'],'determinants':dict(COUNTS),'new_residual':2197,'newly_settled':added}),flush=True)
