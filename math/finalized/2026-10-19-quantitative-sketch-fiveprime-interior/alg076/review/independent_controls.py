#!/usr/bin/env python3
"""Independent exact controls; no candidate code is imported or executed."""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import hashlib, json

OUT = Path(__file__).resolve().parent

def decimal_interval(q, places=40):
    scale=10**places
    n=q.numerator*scale//q.denominator
    def fmt(z):
        return f'{z//scale}.{z%scale:0{places}d}'
    return {'lower':fmt(n), 'upper':fmt(n+1), 'denominator_power_10':places}

# e=sum_{j=0}^40 1/j! + tail. After the first omitted term 1/41!,
# every successive term ratio is <=1/42. All operations below are rational.
e_lo = sum((F(1,factorial(j)) for j in range(41)),F(0))
e_hi = e_lo + F(1,factorial(41))/(1-F(1,42))
assert e_lo > F(2718,1000) and e_hi < F(2719,1000)
N,k,d,eps2,s=1024,496,528,F(1,4),1280
lam,mu=F(13,20),F(1,5)
assert N-k==d and lam*eps2*s==208 and mu*s==256
assert 1+lam==F(33,20) and 1/(1-mu)==F(5,4)
chernoff_lo=e_lo**208 * F(20,33)**528 + F(5,4)**1024/e_hi**256
chernoff_hi=e_hi**208 * F(20,33)**528 + F(5,4)**1024/e_lo**256
threshold=F(12,10**13)
assert chernoff_hi < threshold

# A separate direct Gamma/Poisson calculation at the same split.
# G_d(x)=exp(-x)*sum_{j=d}^infty x^j/j! for integer d.
# Bound the positive Poisson tail through j=640, then a geometric tail.
x=320
poisson_partial=sum((F(x**j,factorial(j)) for j in range(d,641)),F(0))
poisson_tail_bound=F(x**641,factorial(641))/(1-F(x,642))
gamma_lower_lo=poisson_partial/e_hi**x
gamma_lower_hi=(poisson_partial+poisson_tail_bound)/e_lo**x
energy_poly=sum((F(s**j,factorial(j)) for j in range(N)),F(0))
energy_tail_lo=energy_poly/e_hi**s
energy_tail_hi=energy_poly/e_lo**s
union_lo=gamma_lower_lo+energy_tail_lo
union_hi=gamma_lower_hi+energy_tail_hi
assert union_hi < chernoff_lo < threshold
assert gamma_lower_hi < e_lo**208*F(20,33)**528
assert energy_tail_hi < F(5,4)**1024/e_hi**256

# Polynomial identities G_d-G_{d+1}=exp(-t)t^d/d! and
# G_d'=exp(-t)t^(d-1)/(d-1)! reduce to coefficient arithmetic.
for q in range(1,65):
    p=[F(1,factorial(j)) for j in range(q)]
    derivative=[(j+1)*p[j+1] for j in range(q-1)]+[F(0)]
    difference=[p[j]-derivative[j] for j in range(q)]
    assert difference==[F(0)]*(q-1)+[F(1,factorial(q-1))]
    pnext=p+[F(1,factorial(q))]
    assert [pnext[j]-(p[j] if j<q else 0) for j in range(q+1)]==[F(0)]*q+[F(1,factorial(q))]

# Realification of the genuinely complex rank-one L=[1,i]:
# Re(Lx)=a-d, Im(Lx)=b+c for x=(a+ib,c+id).
A=[[F(1),F(0),F(0),F(-1)], [F(0),F(1),F(1),F(0)]]
def tr(M):return [list(row) for row in zip(*M)]
def mm(A,B):return [[sum((a*b for a,b in zip(row,col)),F(0)) for col in tr(B)] for row in A]
def scale(M,c):return [[c*x for x in row] for row in M]
def ident(n):return [[F(i==j) for j in range(n)] for i in range(n)]
assert mm(A,tr(A))==scale(ident(2),2)
P=scale(mm(tr(A),A),F(1,2)); I=ident(4)
Q=[[I[i][j]-P[i][j] for j in range(4)] for i in range(4)]
assert P==tr(P) and mm(P,P)==P
assert mm(A,Q)==[[F(0)]*4 for _ in range(2)]
assert mm(P,Q)==[[F(0)]*4 for _ in range(4)]
assert sum(Q[i][i] for i in range(4))/2==1 # E||QX||^2=N_complex-r_complex.

# Relative threshold is not independent of X; the absolute-optimal estimate
# need not be relative-optimal. N=1, rank 0, epsilon=1/2, fixed h=3/4.
# At X=1 the nonzero estimate succeeds strictly and h=0 fails strictly.
# Continuity gives a nonempty open Gaussian-positive success neighborhood.
assert (F(1)-F(3,4))**2 < F(1,4)*F(1)**2
assert F(1)**2 > F(1,4)*F(1)**2

# Exact finite-domain exception: one scalar distinguishes every binary 4-vector.
encoded={sum(((bits>>j)&1)*2**j for j in range(4)) for bits in range(16)}
assert len(encoded)==16

# Stipulated radix-2 butterfly occurrence identity and its lower bound.
# Test every dyadic factorization through N=2^14 and several R values.
c=F(1,4); costs=0
for n in range(15):
    nN=2**n
    for logK in range(n+1):
        logM=n-logK; K=2**logK; M=2**logM
        for R in {max(1,(M+3)//4),M,2*M}:
            B=F(R*K*logK+nN*logM,2)
            rhs=F(nN,2)*(F(R,M)*logK+logM)
            assert B==rhs
            if F(R,M)>=c:assert B>=c*F(nN*n,2)
            costs+=1

result={
 'status':'PASS',
 'arithmetic':'Python standard-library exact fractions only; decimal intervals are outward rounded for display',
 'e_taylor_degree':40,
 'chernoff_bound_enclosure':{'lower':decimal_interval(chernoff_lo)['lower'],'upper':decimal_interval(chernoff_hi)['upper']},
 'required_strict_upper_bound':'0.0000000000012',
 'direct_gamma_union_enclosure':{'lower':decimal_interval(union_lo)['lower'],'upper':decimal_interval(union_hi)['upper']},
 'gamma_polynomial_degrees_checked':64,
 'complex_realification_projector_and_normalization':'PASS',
 'relative_optimality_countercontrol':'PASS',
 'finite_domain_injection_countercontrol':'PASS',
 'dyadic_butterfly_instances_checked':costs,
 'scope':'Finite arithmetic and model-boundary controls support, but do not replace, the independent all-N proof review.'
}
(OUT/'INDEPENDENT_CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
