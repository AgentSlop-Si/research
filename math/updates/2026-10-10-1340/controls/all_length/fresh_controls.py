#!/usr/bin/env python3
"""Fresh reviewer controls. Does not read, import, or execute package programs.
These finite controls corroborate the proof; they are not an eager FFT executor.
"""
from fractions import Fraction as F
from math import factorial, gcd, isqrt
from pathlib import Path
import json
import numpy as np


def geometry(n):
    length = 2 ** (2*n-1).bit_length()
    center = (n-1)//2
    bins = [(2*k*length+n)//(2*n) for k in range(n)]
    residues = [k*length-n*h for k,h in enumerate(bins)]
    return length, center, bins, residues


def ceil_log2_rat(x):
    k=0
    while (1<<k)*x.denominator < x.numerator: k+=1
    return k


def toward_zero(x):
    return x.numerator//x.denominator if x>=0 else -((-x.numerator)//x.denominator)


def params(eps):
    r=2
    while factorial(r)*eps<16: r+=1
    q=ceil_log2_rat(F(512*r*r)/eps)
    bound=F(4,factorial(r))+12*eps/128+F(64*r*r,1<<q)
    assert bound<eps
    return r,q,bound


geo=[]
for n in range(1,2049):
    l,c,h,b=geometry(n)
    assert 2*n<=l<4*n and len(set(h))==n and 0<=min(h)<=max(h)<l
    assert all(2*abs(v)<=n for v in b)
    assert all(abs(F(4*(j-c),l))<=1 for j in range(n))
    assert len(set(b))==n//gcd(n,l)
    geo.append(n)

schedule=[]
for power in range(2,101):
    eps=F(1,1<<power);r,q,e=params(eps)
    schedule.append({'epsilon_exponent':power,'R':r,'q':q,'bound_over_epsilon':str(e/eps)})

# Exact mask recurrences on independently chosen grid masks, both signs.
maskchecks=0
for n in [2,3,5,7,8,9,15,16,17,31,32,33,61,64]:
    l,c,h,b=geometry(n)
    factors=[F(4*(j-c),l) for j in range(n)]+[F(2*z,n) for z in b]
    for q in [4,9,17]:
        for a in factors:
            approx=1
            for r in range(1,19):
                approx=F(toward_zero(approx*a*(1<<q)),1<<q)
                assert abs(approx)<=1 and abs(approx-a**r)<=F(r,1<<q)
                maskchecks+=1

oprows=[]; negatives=[]
for n in list(range(2,65))+[65,67,71,73,97,127]:
    l,c,h,b=geometry(n); jj=np.arange(n); kk=np.arange(n)
    u=4*(jj-c)/l; v=2*np.array(b)/n
    phi=np.exp(-2j*np.pi*c*np.array(b)/(n*l))
    base=np.exp(-2j*np.pi*np.outer(h,jj)/l)/np.sqrt(l)
    target=np.exp(-2j*np.pi*np.outer(kk,jj)/n)/np.sqrt(n)
    correction=np.exp(-2j*np.pi*np.outer(np.array(b)/n,jj-c)/l)
    analytic=np.sqrt(l/n)*phi[:,None]*base*correction
    identity_error=np.linalg.norm(analytic-target,2)
    assert identity_error<2e-12
    for r in [2,4,6,8]:
        series=np.zeros((n,n),complex)
        for t in range(r):
            series += ((-1j*np.pi/4)**t/factorial(t))*v[:,None]**t*base*u[None,:]**t
        trunc=np.sqrt(l/n)*phi[:,None]*series
        measured=float(np.linalg.norm(trunc-target,2)); bound=4/factorial(r)
        assert measured<=bound+2e-12
        oprows.append({'N':n,'R':r,'operator_error':measured,'tail_bound':bound,'ratio':measured/bound,'identity_error':float(identity_error)})
    if n in [3,7,17,31]:
        uncorrected=np.sqrt(l/n)*base
        phase_omitted=np.sqrt(l/n)*series
        neg={'N':n,'uncorrected_error':float(np.linalg.norm(uncorrected-target,2)),
             'omitted_endpoint_phase_error':float(np.linalg.norm(phase_omitted-target,2))}
        assert neg['uncorrected_error']>0.1 and neg['omitted_endpoint_phase_error']>0.1
        negatives.append(neg)


def isprime(p):
    if p<2:return False
    return all(p%d for d in range(2,isqrt(p)+1))


def prime_factors(n):
    fac=[];d=2
    while d*d<=n:
        if n%d==0:
            fac.append(d)
            while n%d==0:n//=d
        d+=1
    if n>1:fac.append(n)
    return fac


def modrank(a,p):
    a=[list(row) for row in a];row=0
    for col in range(len(a[0])):
        k=next((k for k in range(row,len(a)) if a[k][col]%p),None)
        if k is None:continue
        a[row],a[k]=a[k],a[row]
        inv=pow(a[row][col],-1,p);a[row]=[(x*inv)%p for x in a[row]]
        for k in range(row+1,len(a)):
            factor=a[k][col]
            if factor:a[k]=[(x-factor*y)%p for x,y in zip(a[k],a[row])]
        row+=1
        if row==len(a):break
    return row

ranks=[]
for n in range(2,65):
    l,c,h,b=geometry(n);order=n*l;p=order+1
    while not isprime(p):p+=order
    factors=prime_factors(order);z=1
    for a in range(2,p):
        z=pow(a,(p-1)//order,p)
        if pow(z,order,p)==1 and all(pow(z,order//d,p)!=1 for d in factors):break
    assert z!=1
    mat=[[pow(z,(-bk*(j-c))%order,p) for j in range(n)] for bk in b]
    rank=modrank(mat,p);expected=n//gcd(n,l)
    assert rank==expected
    ranks.append({'N':n,'L':l,'field_prime':p,'root':z,'root_order':order,'rank':rank,'predicted_rank':expected})

# Adversarial deterministic backend-error injection, independent of source code.
# Every call returns U_L v + delta ||v|| e with one fixed worst-output direction.
adversarial=[]
rng=np.random.default_rng(20261010)
for n in [3,7,16,17,31]:
    l,c,h,b=geometry(n);u=np.array([4*(j-c)/l for j in range(n)])
    v=2*np.array(b)/n;phi=np.exp(-2j*np.pi*c*np.array(b)/(n*l))
    target=np.exp(-2j*np.pi*np.outer(np.arange(n),np.arange(n))/n)/np.sqrt(n)
    padded=np.exp(-2j*np.pi*np.outer(np.arange(l),np.arange(n))/l)/np.sqrt(l)
    for eps in [F(1,64),F(1,1024)]:
        r,q,cert=params(eps);delta=float(eps/128)
        for kind in ['dense','impulse','alternating','dynamic']:
            x=rng.integers(-9,10,n)+1j*rng.integers(-9,10,n)
            if kind=='impulse':x=np.eye(1,n,n//2).reshape(-1).astype(complex)
            if kind=='alternating':x=(-1.0)**np.arange(n)
            if kind=='dynamic':x=x*np.power(2.0,-np.arange(n))
            out=np.zeros(n,complex)
            direction=np.zeros(l,complex);direction[h[0]]=1
            for t in range(r):
                weighted=u**t*x
                z=padded@weighted+delta*np.linalg.norm(weighted)*direction
                out+=((-1j*np.pi/4)**t/factorial(t))*v**t*z[h]
            out*=np.sqrt(l/n)*phi
            error=float(np.linalg.norm(out-target@x)/np.linalg.norm(x))
            checked_bound=4/factorial(r)+6*delta
            assert error<=checked_bound+2e-12
            adversarial.append({'N':n,'epsilon':str(eps),'input':kind,'relative_error':error,'analytic_bound':checked_bound})

result={'status':'PASS','scope':'Fresh independent finite controls, not production/runtime certification; supplied programs unexecuted.',
        'geometry_lengths':len(geo),'schedule_count':len(schedule),'mask_checks':maskchecks,
        'operator_comparisons':len(oprows),'maximum_operator_bound_ratio':max(x['ratio'] for x in oprows),
        'max_identity_error':max(x['identity_error'] for x in oprows),
        'rank_cases':len(ranks),'adversarial_backend_cases':len(adversarial),
        'negative_controls':negatives,'schedules':schedule,'operators':oprows,'ranks':ranks,'adversarial':adversarial,
        'versions':{'numpy':np.__version__}}
path=Path(__file__).with_name('FRESH_CONTROLS.json');path.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['schedules','operators','ranks','adversarial']},indent=2))
