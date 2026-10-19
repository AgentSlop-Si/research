#!/usr/bin/env python3
"""Fresh N=3757 review controls; imports and executes no historical checker.

The universal theorem is audited in REVIEW.md. Finite determinant checks are
supplements and are explicitly not exhaustive selected Fourier rectangles.
"""
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, permutations
from math import gcd, isqrt
from pathlib import Path
import hashlib, json, random, time

HERE=Path(__file__).resolve().parent
N=3757
started=time.perf_counter()
counts=Counter()
PERMS={}

def perm_terms(k):
    if k not in PERMS:
        PERMS[k]=[(p, -1 if sum(p[i]>p[j] for i in range(k) for j in range(i+1,k))%2 else 1) for p in permutations(range(k))]
    return PERMS[k]

def cyclo_terms(exponent):
    # zeta_3757 = alpha_13^9 beta_289^89. These two primitive roots
    # give the tensor product basis Q(alpha_13,beta_289), degree 12*272.
    e=9*exponent%13
    f=89*exponent%289
    left=((e,1),) if e<12 else tuple((i,-1) for i in range(12))
    right=((f,1),) if f<272 else tuple((f-272+17*j,-1) for j in range(16))
    return ((i,j,si*sj) for i,si in left for j,sj in right)

def det_target(rows,cols):
    d=defaultdict(int)
    for p,sign in perm_terms(len(rows)):
        exponent=sum(rows[i]*cols[p[i]] for i in range(len(rows)))%N
        for i,j,s in cyclo_terms(exponent): d[(i,j)]+=sign*s
    counts['target_characteristic_zero_determinants']+=1
    return {k:v for k,v in d.items() if v}

def det_prime(rows,cols,p):
    d=[0]*p
    for perm,sign in perm_terms(len(rows)):
        d[sum(rows[i]*cols[perm[i]] for i in range(len(rows)))%p]+=sign
    # The only relation on 1,z,...,z^(p-1) is their sum.
    return any(x!=d[-1] for x in d[:-1])

# Independent finite case inventory: every prime17 minor of sizes<=3,
# modulo independent row/column translations. Translation only scales rows
# and columns, so normalized sets containing zero cover all possibilities.
prime_cases={}
for k in (1,2,3):
    sets=[(0,)+rest for rest in combinations(range(1,17),k-1)]
    total=0
    for rr in sets:
        for cc in sets:
            assert det_prime(rr,cc,17)
            total+=1
    prime_cases[str(k)]=total
counts['normalized_prime17_inversion_minors']=sum(prime_cases.values())

# All possible semiprime frequency differences. A rank-one block lies in
# one solution class for delta*k=constant mod221, of exactly gcd(delta,221)
# elements when nonempty. Three distinct frequencies only reduce the bound.
gcd_hist=Counter()
for delta in range(1,221):
    g=gcd(delta,221)
    kernel=[k for k in range(221) if k*delta%221==0]
    assert len(kernel)==g and g<=17
    gcd_hist[g]+=1
counts['nonzero_semiprime_differences']=220
triple_hist=Counter()
for x,y in combinations(range(1,221),2):
    g=gcd(221,gcd(x,y))
    assert g<=17
    triple_hist[g]+=1
counts['translated_three_frequency_sets']=sum(triple_hist.values())

# Every finite occupancy and abstract block-rank case used by the proof.
occupancy=[]
for t in (1,2,3):
    fibers=13*t
    record={'column_residue_count':t,'max_fibers':fibers,
            'two_rich_fibers_max_columns':2*17+(fibers-2),
            'no_triple_fiber_max_columns':2*fibers}
    assert record['two_rich_fibers_max_columns']<79
    assert record['no_triple_fiber_max_columns']<79
    occupancy.append(record)
rank_budgets=[]
for x in (1,2,3):
    for y in (1,2,3):
        if x+y<=3:
            assert min(x,y)==1
            rank_budgets.append([x,y])
assert rank_budgets==[[1,1],[1,2],[2,1]]
# If total rows>=52 and one block rank1, that block has <=17 rows.
# The other has >=35 and three columns, hence rank3 by short-support zeros.
assert 52-17==35>2*17

# Semiprime short-support zero inequality, including every distribution
# of k<=4 nonzero terms among frequency fibers and every permitted common
# zero count. No assumptions on nonzero complex coefficients are added.
def compositions(n,t):
    if t==1:
        yield (n,)
    else:
        for first in range(1,n-t+2):
            for rest in compositions(n-first,t-1): yield (first,)+rest
zero_cases=[]
for k in range(1,5):
    for t in range(1,k+1):
        for sizes in compositions(k,t):
            for common in range(min(sizes)):
                zeros=17*common+(13-common)*(t-1)
                assert zeros<=17*(k-1)
                zero_cases.append([k,t,list(sizes),common,zeros])
counts['short_support_integer_cases']=len(zero_cases)

# Projective equivalence audit over the complete divisor lattice.
divisors=[d for d in range(1,N+1) if N%d==0]
assert divisors==[1,13,17,221,289,3757]
projective=[]
for d in divisors:
    kernel=[i*(N//d) for i in range(d)]
    annihilator=[j*d for j in range(N//d)]
    assert len(kernel)==d and len(annihilator)==N//d
    assert all((x*y)%N==0 for x in kernel for y in annihilator)
    if 3*d>=52:
        assert d>17 and N//d<=17
    projective.append({'kernel_size':d,'column_coset_capacity':N//d})
counts['projective_divisor_cases']=len(projective)

# Complete old scalar dangerous set and its exact exclusion by the new
# dichotomy. This enumeration certifies shapes, not actual Fourier ranks.
dangerous=[]
equality=[]
for a in range(3,103):
    for b in range(a,3*N//a+1):
        if 3*N*(a+b)<=238*a*b:
            dangerous.append([a,b])
            assert a>51 and b>78
            if 3*N*(a+b)==238*a*b: equality.append([a,b])
assert len(dangerous)==750 and equality==[[68,156]]
counts['old_dangerous_scalar_shapes_excluded']=len(dangerous)
new_shapes=[]
for a in range(3,isqrt(3*N)+1):
    for b in range(a,3*N//a+1):
        if a<=51 or b<=78:
            den=Fraction(3*(a+b),a*b)
            assert den>=Fraction(272,N)>Fraction(238,N)
            new_shapes.append((den,a,b))
relax_min=min(new_shapes)
counts['new_dichotomy_stable_rank_shapes']=len(new_shapes)

# Target-only scalar cost and equality accounting.
assert min(d+N//d for d in divisors)==238
assert [d for d in divisors if d+N//d==238]==[17,221]
assert min(2*d+N//d for d in divisors if d<N)==255
assert Fraction(3,51)+Fraction(51,N)==Fraction(272,N)
assert Fraction(6,78)==Fraction(289,N)
assert 16*N>245**2 and N*238==894166
assert 272-238==34 and 255-238==17 and 245-238==7

# Exact new-pattern determinant controls. Separate families exercise the
# direct-sum rank-one extremum, the three-class projective separation,
# arbitrary translations, and multiplication by cyclic units.
rng=random.Random(37572026)
units=[i for i in range(1,N) if gcd(i,N)==1]
certificates=[]
base_patterns=[
    ('one_residue', [0,17,34,51], [0,1,2,3]),
    ('two_residues_rank_one_17', [0,1,18,35], [0,221,17,34]),
    ('two_residues_rank_one_13', [0,1,18,35], [0,221,13,26]),
    ('three_residues_projective_split', [0,17,1,2], [0,221,442,1]),
    ('four_row_residues', [0,1,2,3], [0,13,26,39]),
]
for name,rr,cc in base_patterns:
    for trial in range(80):
        u,v=rng.choice(units),rng.choice(units)
        ro,co=rng.randrange(N),rng.randrange(N)
        rows=[(u*r+ro)%N for r in rr]
        cols=[(v*c+co)%N for c in cc]
        assert len(set(rows))==len(set(cols))==4
        assert det_target(rows,cols)
        certificates.append({'family':name,'rows':rows,'columns':cols,'nonzero':True})

# Complete residue-factor controls for the new s=3 minor: the projective
# obstruction factor vanishes iff 221 divides the product of reduced row
# and column differences. This classifies all 48,400 nonzero pairs.
projective_factor_hist=Counter()
for u in range(1,221):
    for delta in range(1,221):
        zero=u*delta%221==0
        projective_factor_hist['zero' if zero else 'nonzero']+=1
        assert zero==(delta%(221//gcd(u,221))==0)
counts['projective_residue_factor_pairs']=sum(projective_factor_hist.values())
for u,delta in [(1,1),(13,17),(17,13),(13,1),(17,1),(220,220)]:
    rows=[0,17*u,1,2]
    cols=[0,221,442,delta]
    assert bool(det_target(rows,cols))==(u*delta%221!=0)
    certificates.append({'family':'projective_zero_boundary','rows':rows,'columns':cols,'nonzero':u*delta%221!=0})

# Sharp local extremizer and explicit strict-boundary counter-control.
# R is the union of K,1+K,2+K, K=<221>; C=<17>. Every entry equals
# that of its unique representative row in {0,1,2}, giving rank<=3.
extreme_rows=[h+221*k for h in range(3) for k in range(17)]
extreme_cols=[17*j for j in range(221)]
assert len(set(extreme_rows))==51 and len(set(extreme_cols))==221
for r in extreme_rows:
    for c in extreme_cols:
        assert (r*c-(r%221)*c)%N==0
assert det_target([0,1,2],[0,17,34])
assert not det_target([0,221,1,2],[0,17,34,51])
assert Fraction(3*(51+221),51*221)==Fraction(272,N)
assert 51*221==3*N and 221>78
counts['local_rank_three_extremizer_entry_identities']=51*221
# Omitting the distinct-frequency hypothesis destroys the rank-one size
# bound: the entire 221-row, one-column matrix is the all-ones vector.
assert all(k*0%221==0 for k in range(221)) and 221>17
counts['explicit_necessity_countercontrols']=2

# Genuine legal complex rank-three rectangle: F[R,C] with rows{0,221,442}
# and all3757 columns. Exactly three rows gives rank<=3, and a prime17
# 3-minor gives rank>=3. Four-row determinant controls below intentionally
# repeat rows, testing exact zeros without inventing a four-row submatrix.
assert det_target([0,221,442],[0,1,2])
assert not det_target([0,221,442,0],[0,1,2,3])
assert not det_target([0,1,2,3],[0,17,221,0])

# Independent ordinary-polynomial division using a separately constructed
# cyclotomic polynomial, versus the tensor-basis evaluator.
import sympy as sp
X=sp.Symbol('X')
phi=sp.Poly(sp.cyclotomic_poly(N,X),X)
phi_terms={degree[0]:int(coef) for degree,coef in phi.terms()}
assert phi.degree()==3264

def direct_remainder_nonzero(rows,cols):
    coef=defaultdict(int)
    for p,sgn in perm_terms(len(rows)):
        coef[sum(rows[i]*cols[p[i]] for i in range(len(rows)))%N]+=sgn
    for top in range(N-1,phi.degree()-1,-1):
        lead=coef.pop(top,0)
        if lead:
            shift=top-phi.degree()
            for degree,val in phi_terms.items():
                if degree!=phi.degree(): coef[degree+shift]-=lead*val
    return any(coef.values())
for item in certificates[::23]+certificates[-6:]:
    assert direct_remainder_nonzero(item['rows'],item['columns'])==item['nonzero']
    counts['independent_polynomial_division_crosschecks']+=1

# The 3757 tiles are represented exactly as independent coset partitions.
# Each point has the unique tile label (r mod221,c mod17). Full per-entry
# coverage replay is unnecessary; the two complete 1D partitions suffice.
row_buckets=[[i+221*k for k in range(17)] for i in range(221)]
col_buckets=[[j+17*k for k in range(221)] for j in range(17)]
assert sorted(x for bucket in row_buckets for x in bucket)==list(range(N))
assert sorted(x for bucket in col_buckets for x in bucket)==list(range(N))
assert all((221*x)*(17*y)%N==0 for x in range(17) for y in range(221))
assert len(row_buckets)*len(col_buckets)==N
assert N*(17+221)==894166
counts['target_one_dimensional_partition_entries']=2*N

sources={
    'sources/inherited_target_REPORT.md':'ef02706ac4265a67e5ff56f7f4d7bcfe41c987caf17e3cb0885f896d84bff1d5',
    'sources/mixed_prime_REPORT.md':'f986376ce3666499fcb7b53d9db16cf575c8f75862dd449cfc22e477dc279f66',
    'sources/rank_two_REPORT.md':'7aacb964f32e3061d1f1c0d7d1d554e281a3d5d219b53dc11948c7bc83971cdf',
}
for path,expected in sources.items():
    assert hashlib.sha256((HERE/path).read_bytes()).hexdigest()==expected

(HERE/'DANGEROUS_SHAPES.json').write_text(json.dumps(dangerous,indent=2)+'\n')
(HERE/'MINOR_CONTROLS.json').write_text(json.dumps(certificates,indent=2)+'\n')
result={
    'status':'PASS','scope':'N=3757 only; actual complex rank; disjoint no-sharing model',
    'proof_is_primary':True,'samples_do_not_exhaust_rectangles':True,
    'counts':dict(counts),'prime17_normalized_cases':prime_cases,
    'semiprime_difference_gcd_histogram':dict(gcd_hist),
    'semiprime_three_frequency_kernel_histogram':dict(triple_hist),
    'occupancy_cases':occupancy,'rank_budgets':rank_budgets,
    'short_support_cases':zero_cases,'projective_divisor_cases':projective,
    'projective_factor_histogram':dict(projective_factor_hist),
    'old_scalar_equality_shapes':equality,
    'new_scalar_relaxation_minimum':{'density':str(relax_min[0]),'shape':list(relax_min[1:])},
    'certified_rank_three_density':'272/3757',
    'target_baseline':'238/3757','target_cost':894166,
    'common_higher_rank_area_penalty':'7/3757',
    'source_sha256':sources,'elapsed_seconds':time.perf_counter()-started,
}
(HERE/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('short_support_cases','source_sha256')},indent=2))
