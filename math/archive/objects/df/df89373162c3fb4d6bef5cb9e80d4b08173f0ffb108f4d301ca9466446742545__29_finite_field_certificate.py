#!/usr/bin/env python3
"""Exact modular arithmetic audit for the phase-frame/polyphase FFT identities.

No NumPy, floating point, or FFT library; small fields and lengths only.
Proof at all lengths is independent of these finite tests.
"""
from __future__ import annotations
import json,random,pathlib,hashlib
ROOT=pathlib.Path(__file__).resolve().parent

def isprime(n):
    if n<2:return False
    d=2
    while d*d<=n:
        if n%d==0:return False
        d+=1 if d==2 else 2
    return True

def prime_factors(n):
    a=[]; p=2
    while p*p<=n:
        if n%p==0:
            a.append(p)
            while n%p==0:n//=p
        p+=1 if p==2 else 2
    if n>1:a.append(n)
    return a

def root_of_order(q):
    c=1
    while True:
        p=c*q+1
        if isprime(p):break
        c+=1
    primes=prime_factors(p-1)
    g=next(g for g in range(2,p) if all(pow(g,(p-1)//d,p)!=1 for d in primes))
    w=pow(g,(p-1)//q,p)
    assert pow(w,q,p)==1 and all(pow(w,q//d,p)!=1 for d in prime_factors(q))
    return p,w

def one(q,m,seed=20261010):
    assert q%m==0 and q//m>=m
    k=q//m
    p,w=root_of_order(q)
    rng=random.Random(seed+q)
    x=[rng.randrange(p) for _ in range(q)]
    w_m=pow(w,k,p)
    w_k=pow(w,m,p)
    inv_m=pow(m,-1,p)
    # s[b,t] is any nonzero chirp; exact frame requires no analytic phase formula.
    s=[[pow(w,(t*(t-1)//2+(m*b+2)*t)%q,p) for t in range(m)] for b in range(k)]
    d=[[sum(s[b][t]*x[b*m+t]*pow(w_m,(-r*t)%m,p) for t in range(m))%p
        for r in range(m)] for b in range(k)]
    xx=[]
    for b in range(k):
        for t in range(m):
            value=(inv_m*pow(s[b][t],-1,p)*sum(
                d[b][r]*pow(w_m,(r*t)%m,p) for r in range(m)))%p
            xx.append(value)
    assert xx==x
    # Verify exact phase projection sum, independent of Fourier identity.
    pp=[0]*q
    for r in range(m):
        for b in range(k):
            for t in range(m):
                pp[b*m+t]=(pp[b*m+t]+pow(s[b][t],-1,p)*
                    pow(w_m,(r*t)%m,p)*d[b][r])%p
    assert [(v*inv_m)%p for v in pp]==x
    # Mixed-radix transform directly from *recovered* summaries.
    v=[[sum(xx[b*m+t]*pow(w_k,(ell*b)%k,p) for b in range(k))%p
        for t in range(m)] for ell in range(k)]
    y=[0]*q
    for ell in range(k):
        for j in range(m):
            y[ell+j*k]=sum(v[ell][t]*pow(w,(ell*t)%q,p)*
                    pow(w_m,(j*t)%m,p) for t in range(m))%p
    direct=[sum(x[n]*pow(w,(out*n)%q,p) for n in range(q))%p
            for out in range(q)]
    assert y==direct,(q,m,p)
    raw=json.dumps({'q':q,'m':m,'p':p,'w':w,'x':x,'y':y}).encode()
    return {'Q':q,'M':m,'K':k,'field_prime':p,'primitive_Q_root':w,
            'exact_frame_residual':'0 mod p','exact_joint_DFT_residual':'0 mod p',
            'sha256_test_vector':hashlib.sha256(raw).hexdigest()}

def main():
    out=[one(q,m) for q,m in [(15,3),(16,4),(25,5),(32,4),(35,5),(55,5),(77,7),(121,11),(143,11),(221,13)]]
    (ROOT/'finite_field_certificate.json').write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
