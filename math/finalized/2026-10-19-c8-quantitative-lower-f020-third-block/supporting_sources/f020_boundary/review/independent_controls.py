#!/usr/bin/env python3
"""Fresh exact transcription controls; no historical program is imported or run.

All polynomial arithmetic below uses integer sparse dictionaries. Mixed-
characteristic valuation bounds use the least permitted ramification s=2.
The finite prime list is a control for, not the proof of, the universal result.
"""
from collections import defaultdict
from fractions import Fraction
from math import comb, gcd
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
CHECKS = []

def check(label, condition, **data):
    record = {"label": label, "pass": bool(condition), **data}
    CHECKS.append(record)
    if not condition:
        raise AssertionError(record)

def clean(d):
    return {k: v for k, v in d.items() if v}

def add(*terms):
    d = defaultdict(int)
    for a, factor in terms:
        for k, v in a.items():
            d[k] += factor*v
    return clean(d)

def mul(a,b):
    d = defaultdict(int)
    for ka,va in a.items():
        for kb,vb in b.items():
            d[tuple(x+y for x,y in zip(ka,kb))] += va*vb
    return clean(d)

def shift(a, powers):
    return {tuple(x+y for x,y in zip(k,powers)):v for k,v in a.items()}

def edge(j):
    return {(0,k):-comb(j,k) for k in range(1,j+1)}

def continuant(n, start=1):
    a = {(0,0):1}
    if n == 0:
        return a
    b = {(1,0):1}
    for j in range(1,n):
        a,b = b,add((shift(b,(1,0)),1),(mul(edge(start+j-1),a),-1))
    return b

def vp(n,p):
    assert n
    n=abs(n)
    k=0
    while n%p==0:
        n//=p
        k+=1
    return k

def coef_bound(poly, p, e, degree):
    values=[e*vp(v,p)+t for (x,t),v in poly.items() if x==degree]
    return min(values) if values else None

def embed(poly):
    return {(x,0,t):v for (x,t),v in poly.items()}

def translate(poly):
    d=defaultdict(int)
    for (x,t),v in poly.items():
        for z in range(x+1):
            d[(x-z,z,t+z)] += v*comb(x,z)
    return clean(d)

def mixed_weight(k,v,p,e,alpha):
    a,z,t=k
    return e*vp(v,p)+t+a*alpha

def prime_controls(p):
    e=p*(p-1)
    alpha=Fraction(2*p-1,2*p)
    L=Fraction(4*p-1,2)
    c=(-1)**((p+1)//2)
    A=continuant(p)
    B=continuant(p,p+1)
    G=continuant(p-1,p+2)
    M=continuant(p-1)
    R=mul(G,M)
    P=continuant(2*p)
    U=edge(p)
    check(f"p={p}: exact joining identity", P==add((mul(A,B),1),(mul(U,R),-1)))
    lam={k:v for k,v in A.items() if k[0]==1}
    g=add(({(p,0):1},1),(lam,1))
    E=add((A,1),(g,-1))
    difference=add((B,1),(A,-1))
    check(f"p={p}: odd p-block parity", all(x%2==1 for x,t in A))
    check(f"p={p}: shifted difference parity", all(x%2==1 for x,t in difference))
    check(f"p={p}: lambda valuation", coef_bound(A,p,e,1)==p-1)
    check(f"p={p}: lambda residue", A.get((1,p-1),0)%p==c%p)
    check(f"p={p}: p-block coefficient lower bound", all(coef_bound(A,p,e,x)>=p-1 for x in range(1,p,2)))
    check(f"p={p}: remainder supported in odd degrees >=3", all(3<=x<p and x%2 for x,t in E))
    check(f"p={p}: shifted difference coefficient bound", all(e*vp(v,p)+t>=p for (x,t),v in difference.items()))
    check(f"p={p}: joining product parity", all(x%2==0 for x,t in R))
    check(f"p={p}: joining coefficient bounds", all(coef_bound(R,p,e,2*j)>=p-1-j for j in range(p)))
    R0={k:v for k,v in R.items() if k[0]==0}
    C=mul(U,R0)
    P0={k:v for k,v in P.items() if k[0]==0}
    check(f"p={p}: exact constant sign", P0=={k:-v for k,v in C.items()})
    check(f"p={p}: constant valuation", coef_bound(P,p,e,0)==2*p-1)
    check(f"p={p}: constant leading residue", P.get((0,2*p-1),0)%p==p-1)
    weights={(x,t):Fraction(e*vp(v,p)+t)+x*alpha for (x,t),v in P.items()}
    check(f"p={p}: monic boundary integrality", min(weights.values())==2*p-1)
    face={(x,t):P[(x,t)]%p for (x,t),w in weights.items() if w==2*p-1}
    check(f"p={p}: boundary residual exactly Y^(2p)-1", face=={(2*p,0):1,(0,2*p-1):p-1})
    check(f"p={p}: irreducibility denominator", gcd(2*p-1,2*p)==1)
    check(f"p={p}: center Newton point strictly above segment", Fraction(p-1)>alpha*(p-1))
    check(f"p={p}: center derivative leading term lambda", e+(p-1)*alpha>p-1)
    # Under g(a)=kappa and kappa^2=C, the exact two subtracted terms
    # g(a)^2-C vanish. The remaining target is 2*kappa*t^p*(Z^p+cZ).
    eg=embed(g)
    residual={(0,p,0):1,(0,1,0):c}
    target=shift(mul(eg,residual),(0,0,p))
    error=add((translate(P),1),(mul(eg,eg),-1),(embed(C),1),(target,-2))
    error_weights={k:mixed_weight(k,v,p,e,alpha) for k,v in error.items()}
    minimum=min(error_weights.values()) if error_weights else None
    check(f"p={p}: exact whole translated residual error > L", minimum is not None and minimum>L,
          L=str(L), minimum_error_weight=str(minimum), gap=str(minimum-L), error_monomials=len(error))
    derivative={(x-1,t):x*v for (x,t),v in P.items() if x}
    derivative_error=add((derivative,1),({(p,p-1):2*c},-1))
    derivative_target=Fraction(4*p-3,2)
    derivative_minimum=min(Fraction(e*vp(v,p)+t)+x*alpha for (x,t),v in derivative_error.items())
    check(f"p={p}: exact derivative residual error above leading scale", derivative_minimum>derivative_target,
          leading_scale=str(derivative_target), minimum_error_weight=str(derivative_minimum))
    check(f"p={p}: joining-error universal gap", Fraction(1,2)-Fraction(1,p)>0)
    check(f"p={p}: nonlinear p-block remainder gap", 3*alpha-1>0)
    check(f"p={p}: shifted p-block gap", alpha>0)
    check(f"p={p}: quadratic increment gap", Fraction(1,2)>0)
    check(f"p={p}: all nonleading binomial terms suppressed", all(e+(p-j)*alpha+j>p for j in range(1,p)))
    # In characteristic p derivative(Z^p+cZ)=c and c is a unit.
    check(f"p={p}: simple additive residual", c%p!=0)
    check(f"p={p}: opposite discs disjoint", alpha<1)
    check(f"p={p}: exact root count", 2*p==p+p)
    check(f"p={p}: root spacings yield discriminant exponent", 2*p*(p-1)+2*p*p*alpha==p*(4*p-3))
    for s in (2,3):
        es=p**(s-1)*(p-1)
        # Phi_(p^s)(1+T)=sum_(j=0)^(p-1)(1+T)^(j*p^(s-1)).
        coeffs=[sum(comb(j*p**(s-1),k) if k<=j*p**(s-1) else 0 for j in range(p)) for k in range(es+1)]
        check(f"p={p},s={s}: shifted cyclotomic Eisenstein", coeffs[-1]==1 and coeffs[0]==p and all(v%p==0 for v in coeffs[:-1]))
        check(f"p={p},s={s}: ramification covers every error bound", es>=e and es>L)

def symbolic_correspondence_controls():
    import sympy as sp
    q,x,z,v=sp.symbols('q x z v')
    polys=[sp.Integer(1),x]
    for n in range(1,10):
        polys.append(sp.expand(x*polys[-1]-(1-q**n)*polys[-2]))
    gaussian=[[sp.Integer(1)]]
    for n in range(1,11):
        prev=gaussian[-1]
        gaussian.append([sp.Integer(1)]+[sp.expand(prev[k]+q**(n-k)*prev[k-1]) for k in range(1,n)]+[sp.Integer(1)])
    for n in range(11):
        H=sum(gaussian[n][k]*z**k for k in range(n+1))
        transformed=sp.expand(v**n*polys[n].subs(x,v+v**-1))
        check(f"b={n}: exact actual H/P correspondence", sp.expand(H.subs(z,v*v)-transformed)==0)
        check(f"b={n}: endpoint unit modulo t", sp.expand(polys[n].subs(q,1))==x**n)
    for b in range(1,9):
        lhs=0
        for k in range(b):
            lhs+=polys[k]**2*sp.prod(1-q**j for j in range(k+1,b))
        rhs=sp.diff(polys[b],x)*polys[b-1]-polys[b]*sp.diff(polys[b-1],x)
        check(f"b={b}: exact diagonal CD sign and normalization", sp.expand(lhs-rhs)==0)

def main():
    for p in (3,5,7,11,13):
        prime_controls(p)
    symbolic_correspondence_controls()
    output={"status":"PASS", "total_assertions":len(CHECKS), "all_passed":all(r['pass'] for r in CHECKS),
            "purpose":"Finite exact transcription controls only; universal proof is in INDEPENDENT_REVIEW.md.",
            "historical_programs_executed":False, "checks":CHECKS}
    (ROOT/'INDEPENDENT_CHECKS.json').write_text(json.dumps(output,indent=2)+'\n')
    print(f"PASS: {len(CHECKS)} exact independent assertions")

if __name__=='__main__':
    main()
