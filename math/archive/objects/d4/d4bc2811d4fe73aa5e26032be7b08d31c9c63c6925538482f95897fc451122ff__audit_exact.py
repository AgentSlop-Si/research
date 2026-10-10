#!/usr/bin/env python3
"""Fresh independent exact controls; does not import or execute submitted code."""
import sympy as s, json, math, time
from pathlib import Path
q,z,y,t,u=s.symbols('q z y t u')
OUT=Path(__file__).parent
start=time.time()
def H(n):
    # Gaussian row from q-Pascal, separately from Rogers-Szego's three-term recurrence.
    row=[s.Integer(1)]
    for k in range(1,n+1):
        old=row
        row=[s.Integer(1)]+[s.expand(old[j]+q**(k-j)*old[j-1]) for j in range(1,k)]+[s.Integer(1)]
    return sum(c*z**i for i,c in enumerate(row))
def disc(f,x):return s.Integer(1) if s.degree(f,x)<=1 else s.discriminant(f,x)
def arr(f):return [int(c) for c in reversed(s.Poly(f,q).all_coeffs())]
def canon(f,d):return s.rem(f,s.cyclotomic_poly(d,q),q)
def product_mod(seq,d):
    v=s.Integer(1)
    for a in seq:v=canon(v*a,d)
    return v

fixed=[]
for d in (3,7,11,15,19):
    b=(d-1)//2;h=H(b); U,rr=s.div(h,z+1,z);assert rr==0
    delta=canon(disc(U,z),d)
    # Direct product over all d roots of z^d+1, without a resultant implementation.
    R=product_mod((canon(U.subs(z,-q**j),d) for j in range(d)),d)
    gamma=canon(delta*R,d)
    paired=canon(gamma*canon(gamma.subs(q,q**(d-1)),d),d)
    g=canon(U.subs(z,-1),d)
    m=(b+d)//2
    num=product_mod((1-q**j for j in range(1,b+1)),d)
    den=product_mod((1-q**(2*j) for j in range(1,m+1)),d)
    assert s.gcd(den,s.cyclotomic_poly(d,q))==1
    v=canon(d*num*s.invert(den,s.cyclotomic_poly(d,q),q),d)
    inv=lambda f:canon(f.subs(q,q**(d-1)),d)
    identity=canon(g*inv(v)+inv(g)*v-v*inv(v),d)
    assert identity==0
    record=dict(d=d,b=b,degree_U=int(s.degree(U,z)),disc_U=arr(delta),res_F_U=arr(R),gamma=arr(gamma),paired_guard=arr(paired),paired_content=int(s.Poly(paired,q).content()),g=arr(g),v=arr(v),reciprocal_identity_zero=True)
    fixed.append(record)
    print('fixed',d,record['paired_content'],'seconds',time.time()-start,flush=True)
(OUT/'FIXED_BASE_INDEPENDENT.json').write_text(json.dumps(fixed,indent=2)+'\n')

# Direct H_n substitution into truncated epsilon series. All coefficients are
# rational polynomials modulo Phi_d; no radicals or floating point occur.
def local_series(n,d,alpha_index,M):
    values={}
    for (qj,zk),coef in s.Poly(H(n),q,z).terms():
        for eh in range(M//2+1):
            qcoef=coef*s.binomial(s.Rational(qj,d),eh)
            for l in range(min(zk,M-2*eh)+1):
                ep=2*eh+l
                c=qcoef*s.binomial(zk,l)*(-1)**(zk-l)*q**((qj+alpha_index*(zk-l))%d)
                values[ep,l]=values.get((ep,l),0)+c
    return {key:canon(value,d) for key,value in values.items()}
local=[]
for d,A,b in [(3,1,1),(3,2,1),(3,3,1),(3,4,1),(7,1,3),(7,2,3)]:
    n=A*d+b;g=canon(s.diff(H(b),z).subs(z,-1),d)
    numerator=product_mod((1-q**j for j in range(1,b+1)),d)
    denominator=product_mod((1-q**(2*j) for j in range(1,(b+d)//2+1)),d)
    v=canon(d*numerator*s.invert(denominator,s.cyclotomic_poly(d,q),q),d)
    vals=local_series(n,d,0,A+1)
    expected={}
    for j in range(A//2+1):
        l=A+1-2*j
        expected[l]=expected.get(l,0)+g*(-1)**j*s.factorial(A)*d**(A-j)/(2**j*s.factorial(j)*s.factorial(A-2*j))
    for j in range((A-1)//2+1):
        l=A-1-2*j
        expected[l]=expected.get(l,0)-v*(-1)**j*s.factorial(A)*d**(A-1-j)/(2**j*s.factorial(j)*s.factorial(A-1-2*j))
    for ep in range(A+2):
        for l in range(A+2):
            assert canon(vals.get((ep,l),0)-(expected.get(l,0) if ep==A+1 else 0),d)==0,(d,A,b,ep,l)
    checked=1
    for ai in range(1,d):
        vals=local_series(n,d,ai,A)
        ga=canon(H(b).subs(z,-q**ai),d)
        expected={}
        for j in range(A//2+1):
            l=A-2*j
            ap=(-1)**l*q**((-ai*l)%d)
            expected[l]=(-1)**(A+j)*s.factorial(A)*d**(A-j)*ga*ap/(2**j*s.factorial(j)*s.factorial(A-2*j))
        for ep in range(A+1):
            for l in range(A+1):
                assert canon(vals.get((ep,l),0)-(expected.get(l,0) if ep==A else 0),d)==0,(d,A,b,ai,ep,l)
        checked+=1
    local.append(dict(d=d,A=A,b=b,n=n,clusters=checked,all_lower_and_leading_coefficients_match=True))
    print('local',d,A,b,'seconds',time.time()-start,flush=True)
(OUT/'LOCAL_SERIES_INDEPENDENT.json').write_text(json.dumps(local,indent=2)+'\n')

# Ordinary discriminants via an independently derived reciprocal-quadratic product.
def ordinary_disc(n):
    hn=H(n)
    C=s.div(hn,z+1,z)[0] if n%2 else hn
    r=s.degree(C,z)//2
    S0=s.Integer(2);S1=u;terms=[S0,S1]
    for j in range(2,r+1):terms.append(s.expand(u*terms[-1]-terms[-2]))
    cp=s.Poly(C,z)
    P=cp.nth(r)+sum(cp.nth(r+j)*terms[j] for j in range(1,r+1))
    out=s.expand(P.subs(u,2)*P.subs(u,-2)*disc(P,u)**2)
    if n%2:out=s.expand(out*C.subs(z,-1)**2)
    if n<=7:assert s.expand(out-s.discriminant(hn,z))==0
    return out
full=[]
cache={}
for d,A,b in [(3,1,1),(3,2,1),(3,3,1),(7,1,3)]:
    n=d*A+b
    D=cache.setdefault(n,ordinary_disc(n))
    ph=s.cyclotomic_poly(d,q);K=d*A*(A-1)//2+A
    E=D
    for j in range(K):
        E,rem=s.div(E,ph,q);assert rem==0,(d,A,b,j)
    Ered=canon(E,d);assert Ered!=0
    h=H(b);U=s.div(h,z+1,z)[0];g=canon(U.subs(z,-1),d)
    delta=canon(disc(U,z),d)
    R=product_mod((canon(U.subs(z,-q**j),d) for j in range(d)),d)
    num=product_mod((1-q**j for j in range(1,b+1)),d)
    den=product_mod((1-q**(2*j) for j in range(1,(b+d)//2+1)),d)
    v=canon(d*num*s.invert(den,ph,q),d)
    tau=canon(v*s.invert(g,ph,q),d)
    J=y*s.hermite_prob(A,y)-A*t*s.hermite_prob(A-1,y)
    dj=canon(s.discriminant(J,y).subs(t,tau),d)
    PA=math.prod(j**j for j in range(1,A+1))
    constant=canon((-1)**(A*(d-1)//2)*d**(d*A*(A+1)//2+A)*PA**(d-1)*dj*delta*R**(2*A)*g**2,d)
    Q=s.div(q**d-1,ph,q)[0]
    predicted=canon(Q**K*constant,d)
    assert canon(Ered-predicted,d)==0,(d,A,b)
    full.append(dict(d=d,A=A,b=b,n=n,exact_cyclotomic_order=K,E_remainder=arr(Ered),leading_constant=arr(constant),complete_coefficient_matches=True))
    print('disc',d,A,b,'seconds',time.time()-start,flush=True)
(OUT/'ORDINARY_DISCRIMINANT_INDEPENDENT.json').write_text(json.dumps(full,indent=2)+'\n')
print('PASS',time.time()-start,flush=True)
