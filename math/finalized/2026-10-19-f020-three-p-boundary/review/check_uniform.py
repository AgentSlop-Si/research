from math import comb
from fractions import Fraction as F
from pathlib import Path
import json

# Sparse bivariate polynomials: (X exponent,T exponent) -> integer modulo p.
# T^(cut+1) is discarded, with cut always greater than every tested target.
def add(A,B,p,scale=1):
    C=A.copy()
    for m,a in B.items():
        C[m]=(C.get(m,0)+scale*a)%p
        if not C[m]:del C[m]
    return C

def mul(A,B,p,cut):
    C={}
    for (j,k),a in A.items():
        for (l,m),b in B.items():
            if k+m<=cut:C[(j+l,k+m)]=(C.get((j+l,k+m),0)+a*b)%p
    return {m:a for m,a in C.items() if a}

def edge(n,p,cut):return {(0,k):-comb(n,k)%p for k in range(1,min(n,cut)+1) if comb(n,k)%p}

def block(lo,hi,p,cut):
    # Vertices lo,...,hi inclusive, empty block is 1.
    if hi<lo:return {(0,0):1}
    A={(0,0):1};B={(1,0):1}
    for n in range(lo,hi):
        A,B=B,add({(j+1,k):a for (j,k),a in B.items()},mul(edge(n,p,cut),A,p,cut),p,-1)
    return B

def derivative(A,p):return {(j-1,k):j*a%p for (j,k),a in A.items() if j and j*a%p}
def minimum(A,w):return min((F(k)+j*w for (j,k) in A),default=None)
def high(A,w,L):
    mm=minimum(A,w)
    assert mm is None or mm>L,(mm,L)
    return str(mm)

def residual_check(P,expected,w,L,p):
    assert all(F(k)+j*w==L for j,k in expected)
    return high(add(P,expected,p,-1),w,L)

results=[]
for p in [5,7,11,13,17,19,23]:
    cut=3*p+1;e=p*(p-1);alpha=F(2*p-1,2*p);c=(-1)**((p+1)//2)
    assert e>3*p and cut>3*p
    A=block(1,p,p,cut);B=block(p+1,2*p,p,cut);C=block(2*p+1,3*p,p,cut)
    D=block(1,p-1,p,cut);E=block(p+2,2*p,p,cut)
    G=block(p+1,2*p-1,p,cut);J=block(2*p+2,3*p,p,cut);M=block(p+2,2*p-1,p,cut)
    R1=mul(D,E,p,cut);R2=mul(G,J,p,cut)
    prod=lambda *polys: __import__('functools').reduce(lambda u,v:mul(u,v,p,cut),polys,{(0,0):1})
    correction=prod(edge(p,p,cut),edge(2*p,p,cut),D,M,J)
    assembled=add(add(add(prod(A,B,C),prod(edge(p,p,cut),R1,C),p,-1),prod(edge(2*p,p,cut),A,R2),p,-1),correction,p)
    P=block(1,3*p,p,cut)
    assert assembled==P
    assert not any(j%2==0 for j,k in P)
    leading=residual_check(P,{(3*p,0):1,(p,2*p-1):-3%p},alpha,3*p*alpha,p)
    inner=residual_check(P,{(p,2*p-1):-3%p,(1,3*p-2):-3*c%p},F(1),F(3*p-1),p)
    dp=derivative(P,p)
    deriv=residual_check(dp,{(2*p,p-1):3*c%p,(0,3*p-2):-3*c%p},alpha,F(3*p-2),p)
    small_deriv=residual_check(dp,{(0,3*p-2):-3*c%p},F(1),F(3*p-2),p)
    lower={j:min(k for jj,k in P if jj==j) for j in sorted({j for j,k in P})}
    points=sorted(lower.items());hull=[]
    for point in points:
        while len(hull)>1 and F(point[1]-hull[-1][1],point[0]-hull[-1][0])<=F(hull[-1][1]-hull[-2][1],hull[-1][0]-hull[-2][0]):hull.pop()
        hull.append(point)
    assert hull==[(1,3*p-2),(p,2*p-1),(3*p,0)]
    assert (6*c)%p and (-3*c)%p
    results.append({'p':p,'minimal_ramification':e,'truncation_degree':cut,'polynomial_terms':len(P),'triple_block_identity':True,'parity_odd':True,'newton_vertices':hull,'alpha':str(alpha),'strict_error_minima':{'alpha':leading,'inner':inner,'alpha_derivative':deriv,'inner_derivative':small_deriv},'alpha_derivative_nonzero':6*c%p,'inner_derivative_nonzero':-3*c%p,'discriminant_valuation':3*p*(3*p-2),'status':'PASS'})
    print('PASS',p,'terms',len(P),'hull',hull,flush=True)
Path(__file__).with_name('UNIFORM_CHECKS.json').write_text(json.dumps({'results':results,'scope':'Finite exact controls support a separately written uniform proof; no extrapolation.','mixed_characteristic_justification':'All tested targets are less than 3p; p(p-1)>3p for p>=5. Any discarded coefficient divisible by p has valuation at least p(p-1), hence lies strictly above every target. T truncation also lies above every target, including after X differentiation.'},indent=2)+'\n')
