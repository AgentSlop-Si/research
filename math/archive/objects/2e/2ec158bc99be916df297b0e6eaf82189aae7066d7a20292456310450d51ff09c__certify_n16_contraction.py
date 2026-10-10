#!/usr/bin/env python3
"""Exact Gaussian-integer Banach certificate for all N16 Fourier entries.

The numerical file proposes a dyadic center and affine chart only. Acceptance
uses integer arithmetic, rational inequalities, and an elementary root enclosure.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
from pathlib import Path
from fractions import Fraction as F
from math import lcm, isqrt
import json, sys, time
import numpy as np
import scipy.linalg as la
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'seed_compatibility_gate'))
from check_n16_outer_gate import cycles
N,J=16,8

def cmul(a,b):
    ar,ai=a; br,bi=b
    return ar@br-ai@bi, ar@bi+ai@br

def cadd(*pairs):
    return sum((a for a,b in pairs)),sum((b for a,b in pairs))

def quantize(a,p=60):
    return tuple(np.asarray([int(round(float(v)*(1<<p))) for v in part.ravel()],dtype=object).reshape(a.shape)
                 for part in (a.real,a.imag))

def matrix_bound(pair,den):
    return F(max(int(sum(abs(r)+abs(i) for r,i in zip(rr,ii))) for rr,ii in zip(*pair)),den)

def show(x):
    return {'numerator':str(x.numerator),'denominator':str(x.denominator),'decimal':float(x)}

def proposed_chart():
    data=np.load(HERE/'NUMERICAL_CANDIDATE.npz')
    jac=data['jacobian']; transform=data['transforms']; physical=data['physical']
    right=la.lstsq(jac,np.eye(256,dtype=complex),lapack_driver='gelsy')[0].reshape(3,N,J,256)
    v=np.empty_like(right)
    for l in range(3):
        for i in range(N):
            v[l,i]=la.solve_triangular(transform[i],right[l,i])/(1 if l==2 else 4)
    center=quantize(physical); directions=quantize(v)
    chart={'dyadic_exponent':60,'center_real':center[0].tolist(),'center_imag':center[1].tolist(),
           'directions_real':directions[0].tolist(),'directions_imag':directions[1].tolist(),
           'parameter_order':'layer,row,term; direction coordinate is flattened Fourier row,column',
           'exact_target':'F16[i,j]=z^(i*j), z=(sqrt(2+sqrt(2))+i*sqrt(2-sqrt(2)))/2'}
    (HERE/'DYADIC_AFFINE_CHART.json').write_text(json.dumps(chart,separators=(',',':'))+'\n')

def certify():
    started=time.monotonic()
    chart=json.loads((HERE/'DYADIC_AFFINE_CHART.json').read_text())
    p=chart['dyadic_exponent']; scale=1<<p
    center=tuple(np.asarray(chart['center_'+part],dtype=object) for part in ('real','imag'))
    v=tuple(np.asarray(chart['directions_'+part],dtype=object) for part in ('real','imag'))
    assert center[0].shape==(3,N,J) and v[0].shape==(3,N,J,256)
    poles=[(j+2)**N-1 for j in range(J)]
    assert all(d>0 for d in poles)
    common=lcm(*poles); den=scale*common
    gs=np.zeros((J,N,N),dtype=object)
    for j,perm in enumerate(cycles(N)):
        d=j+2
        for col in range(N):
            row=col
            for power in range(N):
                gs[j,row,col]=d**(N-power)*(common//poles[j]); row=perm[row]
    b=(np.eye(N,dtype=object),np.zeros((N,N),dtype=object))
    for off in (0,4):
        for i in range(4):
            for j in range(4):
                val=[(1,0),(0,1),(-1,0),(0,-1)][i*j%4]
                b[0][off+i,off+j],b[1][off+i,off+j]=val
    h=[]; dh=[]
    for l in range(3):
        hpair=tuple(np.empty((N,N),dtype=object) for _ in range(2))
        dpair=tuple(np.empty((N,N,256),dtype=object) for _ in range(2))
        for part in range(2):
            for i in range(N):
                hpair[part][i]=center[part][l,i]@gs[:,i,:]
                dpair[part][i]=gs[:,i,:].T@v[part][l,i]
        h.append(hpair); dh.append(dpair)
    bh1=cmul(b,h[0]); prefix=cmul(h[1],bh1); left=cmul(cmul(h[2],h[1]),b)
    product=cmul(h[2],prefix); den3=den**3
    # All entries in the exact chart Jacobian share den^3.
    jr=np.empty((256,256),dtype=object); ji=np.empty_like(jr)
    for t in range(256):
        d0=tuple(q[:,:,t] for q in dh[0]); d1=tuple(q[:,:,t] for q in dh[1]); d2=tuple(q[:,:,t] for q in dh[2])
        deriv=cadd(cmul(d2,prefix),cmul(cmul(h[2],d1),bh1),cmul(left,d0))
        jr[:,t]=deriv[0].ravel(); ji[:,t]=deriv[1].ravel()
    for t in range(256): jr[t,t]-=den3
    ecenter=matrix_bound((jr,ji),den3)
    # A rational lower approximation to z. Each positive component differs
    # from its true value by < 2/Z. Its modulus is <= 1, so for 0<=e<16
    # the complex l1 error of its e-th power is < 120/Z.
    Z=1<<160
    slo=isqrt(2*Z*Z); shi=slo+1
    cr=isqrt((2*Z+slo)*Z); ci=isqrt((2*Z-shi)*Z); rootden=2*Z
    powers=[(1,0,1)]
    for e in range(1,16):
        ar,ai,ad=powers[-1]
        powers.append((ar*cr-ai*ci,ar*ci+ai*cr,ad*rootden))
    residual=F(0)
    for i in range(N):
        for j in range(N):
            tr,ti,td=powers[i*j%16]
            rr=int(product[0][i,j])*td-tr*den3
            ri=int(product[1][i,j])*td-ti*den3
            residual=max(residual,F(abs(rr)+abs(ri),den3*td))
    residual+=F(120,Z)
    hs=[matrix_bound(pair,den) for pair in h]
    ls=[]
    for pair in dh:
        ls.append(F(max(int(sum(abs(pair[0][i,k,t])+abs(pair[1][i,k,t]) for k in range(N) for t in range(256))) for i in range(N)),den))
    # Matrix infinity bounds imply output-entry bounds. Derivative variation
    # at ||y||_infinity <= rho is at most C2*rho + C3*rho^2.
    c2=8*(ls[2]*ls[1]*hs[0]+ls[2]*hs[1]*ls[0]+hs[2]*ls[1]*ls[0])
    c3=12*ls[2]*ls[1]*ls[0]
    rho=F(1,10**9)
    q=ecenter+c2*rho+c3*rho*rho
    inward=residual+q*rho
    # Lower bound |a0| by max(|Re a0|,|Im a0|), and variation using l1.
    physical_margin=None; max_direction=F(0)
    for l in range(3):
        for i in range(N):
            for j in range(J):
                base=F(max(abs(int(center[0][l,i,j])),abs(int(center[1][l,i,j]))),scale)
                sensitivity=F(int(sum(abs(v[0][l,i,j,t])+abs(v[1][l,i,j,t]) for t in range(256))),scale)
                margin=base-rho*sensitivity
                physical_margin=margin if physical_margin is None else min(physical_margin,margin)
                max_direction=max(max_direction,sensitivity)
    accepted=q<1 and inward<rho and physical_margin>0
    result={'status':'PASS_EXACT_LOCAL_EXISTENCE' if accepted else 'FAILED_CERTIFICATE',
            'all_arithmetic_after_chart_load':'Gaussian integers and rational fractions',
            'polydisk_radius':show(rho),'residual_upper_bound':show(residual),
            'center_derivative_defect_bound':show(ecenter),'layer_matrix_bounds':[show(x) for x in hs],
            'layer_direction_bounds':[show(x) for x in ls], 'quadratic_derivative_constant':show(c2),
            'cubic_derivative_constant':show(c3),'contraction_factor_bound':show(q),
            'image_radius_upper_bound':show(inward),'physical_nonzero_margin':show(physical_margin),
            'max_physical_direction_row_norm':show(max_direction),'fixed_pole_denominators':poles,
            'Fourier_equations_checked':256,'physical_endpoint_guards':384,
            'chart_complex_dimensions':256,'original_endpoint_parameters':384,
            'elapsed_seconds':time.monotonic()-started,
            'scope':'Existence of an algebraic N16 solution isolated in the supplied exact affine chart; no size lift or speedup.'}
    (HERE/'EXACT_CONTRACTION_CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k in ('status','elapsed_seconds') or isinstance(v,dict) and 'decimal' in v},indent=2),flush=True)
    assert accepted

if __name__=='__main__':
    if '--propose' in sys.argv: proposed_chart()
    certify()
