#!/usr/bin/env python3
"""Independent outer fixed-point reconstruction, with exact integer operations.
No source-package executable is imported or run. NumPy/mpmath are references.
"""
from fractions import Fraction as F
from math import factorial, isqrt
from pathlib import Path
import json
import numpy as np
import mpmath as mp
mp.mp.dps=100


def trunc_ratio(a,b):
    return (abs(a)//b)*(1 if a>=0 else -1)


def bit_ceiling(numerator,denominator=1):
    q=max(0,numerator.bit_length()-denominator.bit_length())
    return q if denominator*(1<<q)>=numerator else q+1


def pi_bounds(bits):
    # Exact alternating-series enclosures, summed to a prespecified degree.
    count=bits+20
    bounds=[]
    for denominator in [5,239]:
        s=sum((F((-1)**k,(2*k+1)*denominator**(2*k+1)) for k in range(count)),F(0))
        d=F((-1)**count,(2*count+1)*denominator**(2*count+1))
        bounds.append((min(s,s+d),max(s,s+d)))
    (a,b),(c,d)=bounds
    return 16*a-4*d,16*b-4*c


def angle_round(num,den,q):
    assert 8*abs(num)<=den
    degree=4
    while factorial(degree+1)<1<<(q+12):degree+=1
    guard=bit_ceiling(4096*(degree+1)**2)+1
    work=q+guard; scale=1<<work
    lower,upper=pi_bounds(work+12)
    ipi=(lower.numerator*scale)//lower.denominator
    angle=trunc_ratio(-2*num*ipi,den)
    assert abs(angle)<=scale
    ar,ai=scale,0;sr,si=ar,ai
    for k in range(1,degree+1):
        oldar=ar
        ar=trunc_ratio(-ai*angle,scale*k)
        ai=trunc_ratio(oldar*angle,scale*k)
        sr+=ar;si+=ai
    real=trunc_ratio(sr,1<<guard);imag=trunc_ratio(si,1<<guard)
    argerror=2*abs(F(num,den))*(upper-F(ipi,scale))+F(1,scale)
    cert=argerror+F(1,factorial(degree+1))+F(3*degree*(degree+1),scale)+F(2,1<<q)
    assert cert<=F(3,1<<q)
    actual=mp.e**(-2j*mp.pi*num/den)
    measured=abs(mp.mpc(real,imag)/(1<<q)-actual)
    assert measured<=mp.mpf(cert.numerator)/cert.denominator
    return (real+1j*imag)/(1<<q),float(measured),str(cert)

records=[]; phases=[];coeffchecks=0
for n in [2,3,5,7,8,9,16,17,31,32,33]:
    length=1<<(2*n-1).bit_length();c=(n-1)//2
    h=[(2*k*length+n)//(2*n) for k in range(n)]
    b=[k*length-n*h[k] for k in range(n)]
    base=np.exp(-2j*np.pi*np.outer(h,np.arange(n))/length)/np.sqrt(length)
    exact=np.exp(-2j*np.pi*np.outer(np.arange(n),np.arange(n))/n)/np.sqrt(n)
    for epsilon in [F(1,16),F(1,64),F(1,10**6)]:
        r=2
        while factorial(r)*epsilon<16:r+=1
        q=bit_ceiling(512*r*r*epsilon.denominator,epsilon.numerator);s=1<<q
        lower,upper=pi_bounds(q+20);ilam=lower.numerator*s//(4*lower.denominator)
        ci=s;coeff=[]
        for k in range(r):
            exactc=(mp.pi/4)**k/factorial(k)
            cm=mp.mpf(ci)/s
            assert 0<=cm<=exactc+mp.mpf('1e-90')
            assert abs(cm-exactc)<=3*k*mp.mpf(1)/s+mp.mpf('1e-90')
            coeffchecks+=1;coeff.append(((-1j)**k)*ci/s)
            ci=ci*ilam//(s*(k+1))
        im=[s]*n;om=[s]*n;total=np.zeros((n,n),complex)
        for k in range(r):
            total+=coeff[k]*(np.asarray(om,dtype=float)/s)[:,None]*base*(np.asarray(im,dtype=float)/s)[None,:]
            im=[trunc_ratio(a*4*(j-c),length) for j,a in enumerate(im)]
            om=[trunc_ratio(a*2*b[j],n) for j,a in enumerate(om)]
        phi=[]
        for k,bk in enumerate(b):
            value,error,cert=angle_round(c*bk,n*length,q)
            phi.append(value);phases.append({'N':n,'q':q,'k':k,'measured_error':error,'certificate':cert})
        ialpha=isqrt((length*s*s)//n)
        rounded=(ialpha/s)*np.asarray(phi)[:,None]*total
        err=float(np.linalg.norm(rounded-exact,2));bound=F(4,factorial(r))+F(64*r*r,s)
        assert err<float(bound)+3e-13
        records.append({'N':n,'epsilon':str(epsilon),'R':r,'q':q,'operator_error':err,'bound':str(bound),'ratio':err/float(bound)})
result={'status':'PASS','scope':'Outer wrapper independently reconstructed; exact transforms replace the dyadic backend. This is not execution of the supplied reference or eager asymptotic tables.',
        'rounded_operator_cases':len(records),'phase_cases':len(phases),'coefficient_cases':coeffchecks,
        'maximum_outer_operator_bound_ratio':max(x['ratio'] for x in records),'records':records,'phases':phases,
        'versions':{'numpy':np.__version__,'mpmath':mp.__version__}}
Path(__file__).with_name('FRESH_OUTER_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['records','phases']},indent=2))
