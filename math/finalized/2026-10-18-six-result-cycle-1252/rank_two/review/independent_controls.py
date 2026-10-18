"""Independent acceptance controls. No candidate or predecessor program is imported.
Exact characteristic-zero ranks use a chosen root of the cyclotomic polynomial;
all density and census checks are integer/rational, with no floating rank.
"""
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import product
from pathlib import Path
import hashlib, json, math, random, time
import sympy as S
from sympy.polys.matrices import DomainMatrix

HERE=Path(__file__).resolve().parent
SOURCE=Path(__file__).resolve().parent.parent/'candidate'
EXPECTED='7aacb964f32e3061d1f1c0d7d1d554e281a3d5d219b53dc11948c7bc83971cdf'
start=time.monotonic()
OUT={'status':'PASS', 'sympy_version':S.__version__, 'independence':'New review code; no author or previous review checker imported or executed.'}

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def verify_inputs():
    assert sha(SOURCE/'REPORT.md')==EXPECTED
    m=json.loads((SOURCE/'MANIFEST.json').read_text())
    for f in m['files']:
        p=SOURCE/f['path']; assert len(p.read_bytes())==f['bytes'] and sha(p)==f['sha256']
    s=json.loads((SOURCE/'SOURCES.json').read_text())
    for f in s['accepted_local_dependencies'].values():
        p=SOURCE/f['path']; assert len(p.read_bytes())==f['bytes'] and sha(p)==f['sha256']
    return {'candidate_report_sha256':EXPECTED,'candidate_manifest_sha256':sha(SOURCE/'MANIFEST.json'),'candidate_file_count':len(m['files']), 'accepted_dependencies':s['accepted_local_dependencies']}
OUT['verified_inputs']=verify_inputs()

def divs(n):return [d for d in range(1,n+1) if n%d==0]
def constants(n):
    ds=divs(n);D=min(d+n//d for d in ds);E=min(2*d+n//d for d in ds[:-1]);return ds,D,E

class ExactFourier:
    def __init__(self,n):
        x=S.Symbol('x'); self.n=n
        root=S.CRootOf(S.cyclotomic_poly(n,x),0)
        self.K=S.QQ.algebraic_field(root)
        z=self.K.from_sympy(root)
        self.w=[self.K.one]
        for j in range(1,n):self.w.append(self.w[-1]*z)
        assert self.w[-1]*z==self.K.one
        assert all(self.w[e]!=self.K.one for e in range(1,n))
    def matrix(self,R,C):return [[self.w[(-r*c)%self.n] for c in C] for r in R]
    def rank(self,A):return int(DomainMatrix(A,(len(A),len(A[0])),self.K).rank())

def classes(A):
    a,b=len(A),len(A[0]); rows={}; cols={}
    for i in range(a):rows.setdefault(tuple(A[i][j]/A[i][0] for j in range(b)),[]).append(i)
    for j in range(b):cols.setdefault(tuple(A[i][j]/A[0][j] for i in range(a)),[]).append(j)
    return list(rows.values()),list(cols.values())

def split_check(A,rankfun):
    a,b=len(A),len(A[0]);rowclasses,colclasses=classes(A)
    assert min(len(rowclasses),len(colclasses))==2
    if len(rowclasses)==2:
        pieces=[[[A[i][j] for j in range(b)] for i in part] for part in rowclasses]
        assert all(rankfun(P)==1 for P in pieces)
        new_cost=sum(len(P)+len(P[0]) for P in pieces)
        assert new_cost==a+2*b and 2*(a+b)-new_cost==a
        assert sorted(i for p in rowclasses for i in p)==list(range(a))
    if len(colclasses)==2:
        pieces=[[[A[i][j] for j in part] for i in range(a)] for part in colclasses]
        assert all(rankfun(P)==1 for P in pieces)
        new_cost=sum(len(P)+len(P[0]) for P in pieces)
        assert new_cost==2*a+b and 2*(a+b)-new_cost==b
        assert sorted(j for p in colclasses for j in p)==list(range(b))
    return len(rowclasses),len(colclasses)

def exact_coset(s,n,order):
    step=n//order
    return set(s)=={(s[0]+step*j)%n for j in range(order)}

def rank_two_shape_equality(R,C,n,E,rc,cc):
    # Derive the actual subgroup from selected differences, not a guessed shape.
    for A,B,count in [(R,C,rc),(C,R,cc)]:
        if count!=2:continue
        d=math.gcd(n,*(v-B[0] for v in B))
        representatives={v%(n//d) for v in A}
        assert len(representatives)==2 and len(A)<=2*d and len(B)<=n//d
        if n*2*(len(A)+len(B))==E*len(A)*len(B):
            assert len(A)==2*d and len(B)==n//d and 2*d+n//d==E
            assert set(A)=={(r+j*(n//d))%n for r in representatives for j in range(d)}
            assert exact_coset(B,n,n//d)

EX={}; saved_rectangles={}
for n in range(2,8):
    F=ExactFourier(n);ds,D,E=constants(n)
    subsets=[[j for j in range(n) if mask>>j&1] for mask in range(1,1<<n)]
    stat=Counter();hist=Counter(); minimum=None;records=[]
    for R in subsets:
        for C in subsets:
            A=F.matrix(R,C);r=F.rank(A);a,b=len(R),len(C)
            hist[r]+=1;stat['rectangles']+=1
            assert a*b<=n*r
            gap=n*r*(a+b)-D*a*b
            assert gap>=0 and (r==1 or gap>0)
            if gap==0:
                g=math.gcd(n,*(v-R[0] for v in R));d=n//g
                assert r==1 and a*b==n and a+b==D
                assert exact_coset(R,n,d) and exact_coset(C,n,n//d)
                stat['optimal_density_rectangles']+=1
            if r==2:
                rc,cc=split_check(A,F.rank)
                stat['rank_two_rectangles']+=1
                stat['rank_two_both_classes' if rc==cc==2 else 'rank_two_rows' if rc==2 else 'rank_two_columns']+=1
                assert n*2*(a+b)>=E*a*b>D*a*b
                density=Fraction(2*(a+b),a*b)
                minimum=density if minimum is None else min(minimum,density)
                rank_two_shape_equality(R,C,n,E,rc,cc)
                if n*2*(a+b)==E*a*b:stat['rank_two_density_equalities']+=1
            if n<=4:
                mask=sum(1<<(i*n+j) for i in R for j in C)
                records.append((mask,r*(a+b),r))
    assert minimum==Fraction(E,n)
    EX[n]={**dict(stat),'rank_histogram':dict(hist),'minimum_rank_two_density':str(minimum)}
    if n<=4:saved_rectangles[n]=records
    print('Fourier exhaustive',n,EX[n],flush=True)
OUT['exhaustive_fourier']=EX

# Fresh exact optimization over all disjoint rectangle tilings for the smallest lengths.
# A first-uncovered-cell recurrence counts each set partition once.
small_optima={}
for n,records in saved_rectangles.items():
    full=(1<<(n*n))-1
    bycell=[[rec for rec in records if rec[0]>>j&1] for j in range(n*n)]
    @lru_cache(None)
    def solve(mask):
        if mask==full:return (0,1,0)
        missing=(~mask)&full; first=(missing&-missing).bit_length()-1
        best=10**9;count=0;bad=0
        for m,c,r in bycell[first]:
            if mask&m:continue
            tail,ways,tailbad=solve(mask|m);total=c+tail
            if total<best:best=total;count=ways;bad=(ways if r>=2 else tailbad)
            elif total==best:count+=ways;bad+=(ways if r>=2 else tailbad)
        return best,count,bad
    best,count,bad=solve(0);_,D,_=constants(n)
    assert best==n*D and bad==0
    small_optima[n]={'minimum_cost':best,'optimal_tilings':count,'higher_rank_optimal_tilings':bad,'states':solve.cache_info().currsize}
    print('Exact tiling optimum',n,small_optima[n],flush=True)
OUT['exhaustive_small_tiling_optima']=small_optima

# Arbitrary unit-modulus phases in Q(i), not all roots of unity.
K=S.QQ_I
phases=[K.one,K(-1),K(0,1),K(S.Rational(3,5),S.Rational(4,5)),K(S.Rational(5,13),S.Rational(12,13))]
assert all(z*K.from_sympy(S.conjugate(K.to_sympy(z)))==K.one for z in phases)
def gaussian_rank(A):return int(DomainMatrix(A,(len(A),len(A[0])),K).rank())
generic=Counter()
for inner in product(phases,repeat=4):
    A=[[K.one]*3,[K.one,inner[0],inner[1]],[K.one,inner[2],inner[3]]]
    r=gaussian_rank(A);generic['matrices']+=1;generic['rank_'+str(r)]+=1
    if r==2:split_check(A,gaussian_rank)
# Rectangular families with arbitrarily many distinct projective classes on one side.
for q in range(2,len(phases)+1):
    for repeat in range(1,5):
        A=[[K.one]*repeat+[z]*3 for z in phases[:q]]
        for B in (A,[list(row) for row in zip(*A)]):
            assert gaussian_rank(B)==2;split_check(B,gaussian_rank);generic['structured_rank_two']+=1
OUT['non_root_unit_modulus_controls']=dict(generic)
print('General unit-modulus controls',dict(generic),flush=True)

# Deterministic additional exact Fourier rectangles, with normalization-independent ranks.
rng=random.Random(202610181248)
extra=Counter()
for n in [8,9,10,12,15,16,18,20,24,25,27,35,49]:
    F=ExactFourier(n);ds,D,E=constants(n)
    candidates=[]
    for _ in range(8):
        a=rng.randint(2,min(7,n));b=rng.randint(2,min(7,n))
        candidates.append((sorted(rng.sample(range(n),a)),sorted(rng.sample(range(n),b))))
    for d in ds[:-1]:
        R=[j*(n//d) for j in range(d)]+[1+j*(n//d) for j in range(d)]
        C=[j*d for j in range(n//d)]
        candidates.append((R,C))
    for R,C in candidates:
        A=F.matrix(R,C);r=F.rank(A);a,b=len(R),len(C);extra['rectangles']+=1
        assert a*b<=n*r
        if r==2:
            rc,cc=split_check(A,F.rank);rank_two_shape_equality(R,C,n,E,rc,cc)
            assert n*2*(a+b)>=E*a*b;extra['rank_two']+=1
        if D*D<12*n:assert n*r*(a+b)>=D*a*b and (r==1 or n*r*(a+b)>D*a*b)
OUT['additional_exact_fourier']=dict(extra)
print('Additional exact Fourier',dict(extra),flush=True)

# Direct integer verification of scalar relaxations, independent of actual existence.
scalar=Counter()
for n in range(2,501):
    ds,D,E=constants(n);assert E>D
    for d in ds[:-1]:
        for a in range(2,2*d+1):
            for b in range(2,n//d+1):
                assert 2*n*(a+b)>=E*a*b>D*a*b
                if 2*n*(a+b)==E*a*b:assert (a,b)==(2*d,n//d) and 2*d+n//d==E
                scalar['rank_two_envelope_shapes']+=1
    if D*D<12*n:
        scalar['eligible_lengths']+=1
        for a in range(3,n+1):
            for b in range(a,n+1):
                r=max(3,(a*b+n-1)//n)
                if r<=a:
                    assert n*r*(a+b)>D*a*b
                    # Squared strict inequality also checks the irrational branch without floats.
                    assert n*r*r*(a+b)*(a+b)>=12*(a*b)**2
                    scalar['higher_rank_shapes']+=1
OUT['scalar_relaxation_controls']=dict(scalar)
print('Integer scalar controls',dict(scalar),flush=True)

# Large target certificates use exponent equality and a primitive-root nonzero minor.
# Coverage is checked again AFTER merging to prove globally sharp penalty constructions.
targets={}
for n,d,square in [(343,7,26),(847,11,41)]:
    ds,D,E=constants(n);h=n//d
    rowparts=[[r+h*t for t in range(d)] for r in range(h)]
    colparts=[[c+d*t for t in range(h)] for c in range(d)]
    tiles=[(R,C,1) for R in rowparts for C in colparts]
    assert len(tiles)==n
    merged=(rowparts[0]+rowparts[1],colparts[0],2)
    modified=[t for t in tiles if not(t[1]==colparts[0] and (t[0]==rowparts[0] or t[0]==rowparts[1]))]+[merged]
    results=[]
    for family in [tiles,modified]:
        cover=[0]*(n*n);cost=0;area2=0
        for R,C,r in family:
            for x in R:
                for y in C:cover[x*n+y]+=1
            cost+=r*(len(R)+len(C))
            if r==1:assert all((x-R[0])*(y-C[0])%n==0 for x in R for y in C)
            else:
                exps=[[(-x*y)%n for y in C] for x in R]
                assert len(set(tuple(row) for row in exps))==2
                assert exps[0][0]==0 and exps[0][1]==0 and exps[d][0]==0 and exps[d][1]%n!=0
                area2+=len(R)*len(C)
        assert set(cover)=={1}
        assert n*(cost-n*D)==(E-D)*area2
        results.append({'tiles':len(family),'cost':cost,'covered_entries':len(cover),'higher_rank_area':area2})
    assert results[0]['cost']==n*D and results[1]['cost']==n*D+2*d
    assert E-D==d and D*D<E*E<12*n
    assert square*square<=2*n and n*4*square<D*square*square
    assert not any(square<=2*e and square<=n//e for e in ds[:-1])
    targets[n]={'D':D,'E2':E,'optimum':n*D,'penalty':str(Fraction(E-D,n)),'constructions':results,'impossible_rank_two_square':square}
    print('Target exact coverage',n,targets[n],flush=True)
OUT['large_target_controls']=targets

# Deliberate exact counterexamples outside the asserted hypotheses/generalizations.
A=S.Matrix([[1,-1,S.I,-S.I],[-S.I,1,-1,S.I],[S.I,-S.I,1,-1],[-1,S.I,-S.I,1]])
assert A.rank()==3 and A[:3,:3].det()==2-2*S.I
B=[[K.from_sympy(A[i,j]) for j in range(4)] for i in range(4)]
assert tuple(map(len,classes(B)))==(4,4)
F=ExactFourier(11);R=[0,1,3];C=[0,2,7];assert F.rank(F.matrix(R,C))==3
G=S.GF(23);B=[[G(pow(2,(-r*c)%11,23)) for c in C] for r in R]
assert DomainMatrix(B,(3,3),G).rank()==2 and tuple(map(len,classes(B)))==(3,3)
OUT['negative_controls']={'rank_three_unit_modulus':{'rank':3,'projective_classes':[4,4],'minor':'2-2i'},'finite_field':{'N':11,'modulus':23,'root':2,'field_rank':2,'complex_rank':3,'projective_classes':[3,3]}}
print('Negative controls passed',flush=True)

# Sieve-derived census: a distinct implementation of factor/divisor enumeration.
limit=10000;primes=[];isprime=[True]*(limit+1);isprime[0]=isprime[1]=False
for p in range(2,limit+1):
    if isprime[p]:
        primes.append(p)
        for k in range(p*p,limit+1,p):isprime[k]=False
all_divs=[[] for _ in range(limit+1)]
for d in range(1,limit+1):
    for k in range(d,limit+1,d):all_divs[k].append(d)
new=[];residual=[];old_residual=[]
for n in range(2,limit+1):
    ds=all_divs[n];D=min(d+n//d for d in ds)
    dominant=any(isprime[p] and p*p>n for p in ds)
    old=D*D<8*n or dominant
    current=D*D<12*n or dominant
    if current and not old:new.append(n)
    if not current:residual.append(n)
    if not old:old_residual.append(n)
assert [n for n in new if n<=1000]==[343,847]
assert not [n for n in residual if n<=1000]
assert len(new)==44 and len(residual)==25 and residual[0]==1331
OUT['domain_census']={'limit':limit,'new_lengths':new,'residual_lengths':residual,'new_count':len(new),'residual_count':len(residual),'old_residual_through_1000':[n for n in old_residual if n<=1000]}
ds,D,E=constants(1331)
assert D==132 and E==143 and 12*1331<D*D<16*1331
assert 63*63<=3*1331 and 1331*3*(63+63)<D*63*63
OUT['next_boundary']={'N':1331,'D':D,'E2':E,'upper_bound':1331*D,'lower_bound':'1331 sqrt(15972)','remaining_tile_rank':3,'relaxed_scalar_obstruction':[63,63,3],'actual_rank_three_rectangle_claimed':False}
assert verify_inputs()==OUT['verified_inputs']
OUT['elapsed_seconds']=round(time.monotonic()-start,3)
(HERE/'RESULTS.json').write_text(json.dumps(OUT,indent=2)+'\n')
print('Census',OUT['domain_census'],flush=True)
print('ALL INDEPENDENT CONTROLS PASSED',OUT['elapsed_seconds'],flush=True)
