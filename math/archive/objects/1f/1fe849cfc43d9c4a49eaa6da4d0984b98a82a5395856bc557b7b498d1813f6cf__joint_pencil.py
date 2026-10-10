"""Joint Hankel pencil compiler: share the overlap of adjacent Hankel windows.

At each trial w, form Y_k(alpha)=T_k(1-alpha*w**k) once for
k=0,...,2*s+1, then use windows k=0..2*s and 1..2*s+1 to
construct the two degree<=s+1 scalar determinant polynomials.

This changes only the arithmetic DAG; exact values match the original
independent-det_pencil_samples implementation for every input/w.
"""
from resultant_gate import det_mod, interp_newton


def shared_res_at(T,w,p,co,s=4):
    if len(T)<2*s+2 or s<1:
        raise ValueError('need 2s+2 reciprocal samples')
    m=s+1
    wpower=[1]
    for k in range(1,2*s+2):
        wpower.append(wpower[-1]*w%p)
        co.multiplies+=1
    vals0=[];vals1=[]
    for alpha in range(m+1):
        y=[(T[k]*(1-alpha*wpower[k]))%p for k in range(2*s+2)]
        co.multiplies+=2*(2*s+2)
        co.additions+=(2*s+2)
        H0=[[y[i+j] for j in range(m)] for i in range(m)]
        H1=[[y[i+j+1] for j in range(m)] for i in range(m)]
        vals0.append(det_mod(H0,p,co))
        vals1.append(det_mod(H1,p,co))
    p0=interp_newton(vals0,p,co)
    p1=interp_newton(vals1,p,co)
    # Match original Sylvester shape and polynomial orientation exactly.
    poly_a=list(reversed(p0+[0]*(m+1-len(p0))))
    poly_b=list(reversed(p1+[0]*(m+1-len(p1))))
    syl=[]
    for poly in (poly_a,poly_b):
        for t in range(m):
            syl.append([0]*t+poly+[0]*(m-1-t))
    return det_mod(syl,p,co)
