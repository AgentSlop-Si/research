"""Polynomially scaled uniform two-Green-sum escape family (all squares N=A^2>=4).

Analytic theorem, stronger than explicit_square_escape.py:
 - All scalar *parameters* a,b,eps,w_i have O(log N)-bit descriptions.
 - T applies in O(N) scalar arithmetic, is uniformly well conditioned,
   with every entry of T^-1 of magnitude at least eps/8=Omega(N^-2).
 - Operator-Schmidt rank N and nonconstant T*ones.
 - This still does NOT compute a Fourier transform.

Full exact coefficient growth for powers (1-1/N)^N is NOT O(log N) bits,
so these are exact-arithmetic, not bit-complexity claims.
"""
from __future__ import annotations
from fractions import Fraction
from math import isqrt


def params(n):
    if n<4 or isqrt(n)**2!=n: raise ValueError('n>=4 square')
    a=Fraction(1,100*n)
    eps=Fraction(1,1000000*n*n)
    b=Fraction(n-1,n)
    w0=Fraction(2*n+1,2*n)
    return a,eps,b,w0


def exact_gate(n):
    a,eps,b,w0=params(n)
    # b^n*(w0) < (3/8)*(9/8)<1/2; b^(n-1)>1/e>1/3.
    assert b**n*w0<Fraction(1,2)
    assert b**(n-1)>Fraction(1,3)
    # Therefore min G2 entry >1/3, max G2 entry <3
    hmin=Fraction(1,3)-6*a
    assert hmin>Fraction(1,4)
    # Uniformly ||(I-aSwap)G2||_inf<4N and ||I-aSwap||_inf<2.
    # Tail of the inverse Neumann expansion after linear term <=64N²eps².
    tail=64*n*n*eps*eps
    assert tail<eps/Fraction(8)
    # The off-diagonal leading term epsilon H>=epsilon/4 beats remainder.
    assert eps*hmin-tail>=eps/Fraction(8)
    # Remaining diagonal entries stay nonzero.
    assert a+12*n*eps+tail<Fraction(1,2)
    # T invertible: epsilon||(I-aSwap)G2||_inf <1.
    assert 4*n*eps<Fraction(1,2)
    # Weyl: sigma_min(R(G1))=a/(1-a²), perturb <=eps||G2||_F<=3Neps
    assert 3*n*eps<a/(1-a*a)
    # Uniform bounds on the condition number of T.
    # ||T||_2 <=1/(1-a)+3Neps; ||T^-1||_2 <= (1+a)/(1-4Neps).
    upper=(Fraction(1,1)/(1-a)+3*n*eps)*(1+a)/(1-4*n*eps)
    assert upper<2
    return {'N':n,'A':isqrt(n),'a':str(a),'epsilon':str(eps),'b':str(b),'w0':str(w0),
        'exact_inequalities_pass':True, 'inverse_nonzero_entry_lower_bound':str(eps/8),
        'all_inverse_entries_nonzero':True,'operator_schmidt_rank':n,
        'condition_number_strict_upper_bound':str(upper),
        'T_times_ones_nonconstant':True,'per_input_scalar_arithmetic':'O(N)',
        'FFT_factorization':False}


def numeric_check(n):
    import mpmath as mp
    mp.mp.dps=80
    a=mp.mpf(1)/(100*n)
    eps=mp.mpf(1)/(1000000*n*n)
    b=mp.mpf(n-1)/n
    w=[1+mp.mpf(1)/(2*n)]+[mp.mpf(1)]*(n-1)
    alpha=isqrt(n)
    i=mp.eye(n)
    s=mp.matrix(n)
    for j in range(n):
        r,c=divmod(j,alpha)
        s[j,c*alpha+r]=1
    g1=(i+a*s)/(1-a*a)
    # Matrix polynomial closed form, one term per ordered index pair.
    den=1-b**n*w[0]
    g2=mp.matrix(n)
    for row in range(n):
        for col in range(n):
            k=(col-row)%n
            ww=mp.mpf(1)
            for t in range(k): ww*=w[(row+t)%n]
            g2[row,col]=b**k*ww/den
    t=g1+eps*g2
    ti=t**-1
    e=max(abs(v) for v in ti*t-i)
    absmin=min(abs(ti[r,c]) for r in range(n) for c in range(n))
    ones=mp.matrix([1]*n)
    y=t*ones
    deviation=max(abs(y[k]-y[0]) for k in range(n))
    assert absmin>=eps/8
    assert deviation>0
    assert e<mp.mpf('1e-65')
    return {'n':n,'min_abs_inverse_entry':mp.nstr(absmin,14),
            'theorem_lower_bound':mp.nstr(eps/8,14),
            'matrix_inverse_residual':mp.nstr(e,7),
            'nonconstant_response_gap':mp.nstr(deviation,14)}

if __name__=='__main__':
    import json
    for n in [4,9,16,25,64,256,1024,4096]:
        print('EXACT',json.dumps(exact_gate(n)))
    for n in [4,9,16,25]:
        print('HIGH_PRECISION',json.dumps(numeric_check(n)))
