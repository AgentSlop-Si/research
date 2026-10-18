#!/usr/bin/env python3
"""Fresh review controls; no author/prior checker imports or execution.
Characteristic-zero determinant tests use ordinary cyclotomic polynomial remainders.
These controls supplement a separately inspected universal proof.
"""
from pathlib import Path
from itertools import permutations, combinations
from fractions import Fraction
from collections import Counter
import random, hashlib, json, time
import sympy as sp

HERE=Path(__file__).resolve().parent
CAND=Path(__file__).resolve().parent.parent/'candidate'
START=time.perf_counter()
RNG=random.Random(0x202610181514)
X=sp.Symbol('x')
COUNTS=Counter()
PERMS={k:[(s,(-1)**sum(s[i]>s[j] for i in range(k) for j in range(i+1,k))) for s in permutations(range(k))] for k in range(1,6)}


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def check_inputs():
    result={}
    for name,data in json.loads((CAND/'MANIFEST.json').read_text())['files'].items():
        p=CAND/name
        assert sha(p)==data['sha256'] and p.stat().st_size==data['bytes'],p
        result[str(p)]=sha(p)
    for data in json.loads((CAND/'SOURCES.json').read_text())['accepted_local_dependencies']:
        assert sha(CAND/data['path'])==data['sha256'],data['path']
        result[data['path']]=sha(CAND/data['path'])
    return result


class ExactCyclotomic:
    """Represent powers modulo the irreducible characteristic-zero Phi_n."""
    def __init__(self,n):
        self.n=n
        poly=sp.Poly(sp.cyclotomic_poly(n,X),X,domain=sp.ZZ)
        self.poly=poly
        self.degree=poly.degree()
        self.low={int(m[0]):int(v) for m,v in poly.terms() if m[0]!=self.degree}
        self.powers=[]
        for e in range(n):
            v={e:1}
            while v and max(v)>=self.degree:
                h=max(v);a=v.pop(h);shift=h-self.degree
                for j,c in self.low.items():
                    z=j+shift;v[z]=v.get(z,0)-a*c
                    if not v[z]:v.pop(z)
            self.powers.append(v)
    def det_terms(self,R,C):
        assert len(R)==len(C)
        terms=Counter()
        for perm,sgn in PERMS[len(R)]:
            terms[sum(R[i]*C[perm[i]] for i in range(len(R)))%self.n]+=sgn
        return {e:v for e,v in terms.items() if v}
    def reduce(self,terms):
        answer=Counter()
        for e,v in terms.items():
            for j,c in self.powers[e%self.n].items():answer[j]+=v*c
        return {j:v for j,v in answer.items() if v}
    def nz(self,R,C):
        COUNTS['exact_determinants']+=1
        return bool(self.reduce(self.det_terms(R,C)))

CACHE={}
def ctx(n):
    if n not in CACHE:CACHE[n]=ExactCyclotomic(n)
    return CACHE[n]

def greedy_rows(n,R,C,stop=None):
    if stop is None:stop=len(C)
    chosen=[];Q=ctx(n)
    for r in R:
        trial=chosen+[r]
        for cols in combinations(C,len(trial)):
            if Q.nz(trial,cols):
                chosen=trial;break
        if len(chosen)==stop:return chosen
    return chosen

OUT={'status':'running','method':'Exact integer determinant sums reduced modulo ordinary characteristic-zero cyclotomic polynomials; fresh independent script.'}
OUT['input_hashes_before']=check_inputs()
print('Frozen packet and six pinned dependencies verified.',flush=True)

# Prime-square universal minors, with independent exponent choices and k=5 included.
nums={}
for q in (5,7,11,13,17,19):
    n=0
    for k in range(2,6):
        for _ in range(100):
            R=RNG.sample(range(q*q),k)
            C=[a+q*RNG.randrange(q) for a in RNG.sample(range(q),k)]
            assert ctx(q*q).nz(R,C),(q,R,C)
            n+=1
    nums[str(q)]=n
OUT['prime_square_universal_minors']=nums
print('Prime-square controls:',sum(nums.values()),flush=True)

# Short-support at exact threshold +1; arbitrary and clustered row sets.
pairs=[(5,7),(7,11),(11,13),(11,17),(13,17),(17,19)]
nums={}
for p,q in pairs:
    n=p*q;count=0
    for k in (2,3,4):
        m=(k-1)*q+1
        for iteration in range(100):
            T=RNG.sample(range(n),k)
            if iteration%3==0:
                # q-sized fibers modulo p concentrate maximally.
                order=RNG.sample(range(p),p)
                A=[u+p*v for u in order for v in RNG.sample(range(q),q)][:m]
            elif iteration%3==1:
                order=RNG.sample(range(q),q)
                A=[u+q*v for u in order for v in RNG.sample(range(p),p)][:m]
            else:A=RNG.sample(range(n),m)
            assert len(greedy_rows(n,A,T))==k,(p,q,A,T)
            count+=1
    nums[f'{p}x{q}']=count
OUT['semiprime_short_support_rank_controls']=nums
print('Short-support controls:',sum(nums.values()),flush=True)

# The short-support zero-count envelope independently maximizes every possible
# distribution of k support terms among q-frequency groups, at k<=p.
def compositions(total,parts):
    if parts==1:
        yield (total,);return
    for first in range(1,total-parts+2):
        for tail in compositions(total-first,parts-1):yield (first,)+tail
count=0
for p,q in pairs[:5]:
    for k in range(1,p+1):
        for t in range(1,k+1):
            for ks in compositions(k,t):
                z0=min(v-1 for v in ks)
                assert z0*q+(p-z0)*(t-1)<=(k-1)*q
                count+=1
OUT['short_support_integer_zero_envelopes']=count

# Two residue classes, one >2q. Extract exact four-minors from independently
# selected row/column sets and rich fibers.
nums={}
for p,q in pairs:
    n=p*q*q;count=0
    for _ in range(80):
        y0,y1=RNG.sample(range(q),2)
        A0=RNG.sample(range(p*q),2*q+1)
        A1=RNG.sample(range(p*q),RNG.randint(1,q))
        T=RNG.sample(range(p*q),3)
        C=[]
        for v in T:C += [v+p*q*w for w in RNG.sample(range(q),2)]
        # First get three independent representatives within the large block.
        B0=greedy_rows(p*q,A0,T)
        assert len(B0)==3
        R=[y0+q*a for a in B0]+[y1+q*A1[0]]
        assert any(ctx(n).nz(R,D) for D in combinations(C,4)),(p,q,R,C)
        count+=1
    nums[f'{p}x{q}^2']=count
OUT['two_residue_four_minor_controls']=nums
print('Two-residue controls:',sum(nums.values()),flush=True)

# Sharp projective description in genuine s=3 examples with d=q and d=pq.
genuine=[]
for p,q in pairs:
    n=p*q*q
    for d in (q,p*q):
        step=n//d
        reps=RNG.sample(range(q),3)
        R=[u+step*k for u in reps for k in range(d)]
        C=[d*j for j in range(n//d)]
        assert len(set(R))==len(R) and max(R)<n
        c0=C[0]
        gcd=sp.igcd(*([n]+[c-c0 for c in C]))
        assert gcd==d
        # K of order d has step n/d, so projective classes are mod n/d.
        assert len({r%(n//d) for r in R})==3
        assert ctx(n).nz(reps,C[:3])
        for _ in range(80):assert not ctx(n).nz(RNG.sample(R,4),RNG.sample(C,4))
        genuine.append({'p':p,'q':q,'d':d,'a':len(R),'b':len(C),'rank':3,'zero_four_minors':80})
OUT['genuine_three_projective_class_examples']=genuine
print('Genuine s=3 rank-three examples:',len(genuine),flush=True)

# Author-selected certificates are data, not executable code; re-evaluate each
# using an unrelated exact polynomial representation.
certs=json.loads((CAND/'TARGET_MINOR_CERTIFICATES.json').read_text())
branches=Counter();shapes=set();occupancy=Counter()
for z in certs:
    R=z['row_minor'];C=z['column_minor'];a,b=z['shape'];s,t=z['residue_occupancies']
    assert len(R)==len(C)==len(set(R))==len(set(C))==4
    assert all(0<=v<1859 for v in R+C)
    assert len({r%13 for r in R})<=s and len({c%13 for c in C})<=t
    assert ctx(1859).nz(R,C),z
    assert a<=s*143 and b<=t*143
    shapes.add((a,b));occupancy[a,b]+=1;branches[z['proof_branch']]+=1
assert len(certs)==1504 and len(shapes)==94 and set(occupancy.values())=={16}
OUT['independently_checked_retained_four_minor_certificates']={'count':len(certs),'shapes':len(shapes),'branches':dict(branches)}
print('Retained four-minor certificates:',len(certs),flush=True)

# Full scalar search, not Fourier existence claims.
N=1859;D=156;B=66;floor=Fraction(49,572);best=None;bestshape=None;admissible=0;bad=[]
for a in range(3,N+1):
    for b in range(a,min(N,3*N//a)+1):
        f=Fraction(3*(a+b),a*b)
        if f<=Fraction(D,N):bad.append((a,b))
        if a<=52 or b<=B:
            admissible+=1
            assert f>=floor,(a,b,f)
            if best is None or f<best:best,bestshape=f,(a,b)
assert len(bad)==94 and set(bad)==shapes and not any(a<=52 or b<=66 for a,b in bad)
assert best==Fraction(477,5564) and bestshape==(52,107)
OUT['target_scalar_audit']={'admissible_shapes':admissible,'minimum':str(best),'minimizing_shape':bestshape,'excluded_former_bad_shapes':len(bad)}

# Divisor, equality and all rank-case constants over a much larger prime range.
qs=list(sp.primerange(13,5001));num=0
for q in qs:
    n=11*q*q;ds=sp.divisors(n)
    vals={int(d):int(d+n//d) for d in ds}
    assert min(vals.values())==12*q
    assert {d for d,v in vals.items() if v==12*q}=={q,11*q}
    assert min(2*d+n//d for d in ds if d<n)==13*q
    bb=max(66,31+2*q,3*q)
    assert 49*bb<=264*q
    assert Fraction(3,4*q)+Fraction(4*q,n)==Fraction(49,44*q)
    assert Fraction(49,44*q)-Fraction(12,11*q)==Fraction(1,44*q)
    assert Fraction(13,11*q)>Fraction(49,44*q)
    assert 16*44*44>11*49*49
    num+=1
OUT['family_density_divisor_equality_controls']={'prime_count':num,'max_q':qs[-1]}
print('Scalar/family controls:',admissible,num,flush=True)

# Explicit once-only target partition, checking the rank-one difference identity
# throughout each tile with integer arithmetic.
q=13;n=11*q*q;seen=bytearray(n*n);cost=0;tiles=0
for u in range(11*q):
    R=[u+11*q*k for k in range(q)]
    for v in range(q):
        C=[v+q*j for j in range(11*q)]
        assert all(((r-R[0])*(c-C[0]))%n==0 for r in R for c in C)
        for r in R:
            offset=r*n
            for c in C:
                ix=offset+c;assert not seen[ix];seen[ix]=1
        cost+=len(R)+len(C);tiles+=1
assert all(seen) and cost==290004 and tiles==1859
OUT['target_full_partition']={'tiles':tiles,'entries':sum(seen),'cost':cost,'side_sizes':[q,11*q]}

# Fresh divisor sieve census of the precise retained union.
M=10000;divs=[[] for _ in range(M+1)]
for d in range(1,M+1):
    for n in range(d,M+1,d):divs[n].append(d)
primes={n for n in range(2,M+1) if len(divs[n])==2}
old=[];remaining=[];new=[]
for n in range(2,M+1):
    dn=min(d+n//d for d in divs[n])
    lp=max(d for d in divs[n] if d in primes)
    covered=dn*dn<12*n or lp*lp>n or n==1331
    if not covered:
        old.append(n)
        q=sp.integer_nthroot(n//11,2)[0] if n%11==0 else 0
        family=q>11 and q in primes and n==11*q*q
        if family:new.append(n)
        else:remaining.append(n)
assert new==[1859,3179,3971,5819,9251] and remaining[0]==2197
assert old==json.loads((CAND/'RESULTS.json').read_text())['domain_census_through_10000']['previous_residuals']
assert remaining==json.loads((CAND/'RESULTS.json').read_text())['domain_census_through_10000']['remaining_residuals']
n=2197;d=min(x+n//x for x in divs[n]);a,b=52,126
assert d==182 and 12*n<d*d<16*n and a*b<=3*n
assert Fraction(3*(a+b),a*b)==Fraction(89,1092)<Fraction(d,n)
assert Fraction(3,52)+Fraction(52,n)==Fraction(55,676)<Fraction(56,676)==Fraction(d,n)
OUT['domain_census']={'through':M,'previous_residuals':old,'newly_settled':new,'remaining_residuals':remaining,'all_lengths_through':2196,'next_rank_gate':3,'next_scalar_shape':[52,126]}
print('Full partition and next gate verified.',flush=True)

# Independently ask SymPy polynomial remainder to cross-check determinant
# representations, including both nonzero and genuinely zero examples.
count=0
for n in (25,49,35,77,143,245,847,1859):
    Q=ctx(n)
    for k in (2,3,4):
        for _ in range(5):
            R=RNG.sample(range(n),k);C=RNG.sample(range(n),k)
            ts=Q.det_terms(R,C)
            poly=sp.Poly.from_dict({(e,):v for e,v in ts.items()},X,domain=sp.ZZ)
            actual={int(m[0]):int(c) for m,c in poly.rem(Q.poly).terms() if c}
            assert actual==Q.reduce(ts)
            count+=1
for p,q in pairs[:4]:
    n=p*q*q;Q=ctx(n);R=[0,p*q,1,1+p*q];C=RNG.sample(range(0,n,q),4)
    ts=Q.det_terms(R,C)
    assert not sp.Poly.from_dict({(e,):v for e,v in ts.items()},X,domain=sp.ZZ).rem(Q.poly)
    assert not Q.reduce(ts)
    count+=1
OUT['sympy_direct_remainder_crosschecks']=count
OUT['input_hashes_after']=check_inputs()
assert OUT['input_hashes_before']==OUT['input_hashes_after']
OUT['status']='all_passed';OUT['counts']=dict(COUNTS);OUT['elapsed_seconds']=round(time.perf_counter()-START,3)
(HERE/'RESULTS.json').write_text(json.dumps(OUT,indent=2)+'\n')
print('ALL PASSED',OUT['counts'],'seconds',OUT['elapsed_seconds'],flush=True)
