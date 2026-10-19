"""Fresh exact integer identities for b=3p+1; no imported checker code."""
from pathlib import Path
import json
import sympy as S
x,q,v=S.symbols('x q v')

def path(lo,hi):
    A,B=S.Poly(1,x,q),S.Poly(x,x,q)
    if hi<lo:return A
    for j in range(lo,hi):A,B=B,S.Poly(x,x,q)*B-S.Poly(1-q**j,x,q)*A
    return B

results=[]
for p in [3,5,7]:
    n=3*p+1
    P=[S.Poly(1,x,q),S.Poly(x,x,q)]
    for j in range(1,n):P.append(S.Poly(x,x,q)*P[-1]-S.Poly(1-q**j,x,q)*P[-2])
    A,B,T=path(1,p),path(p+1,2*p),path(2*p+1,3*p-1)
    Aleft,Bright,Bleft,Ttail,M=path(1,p-1),path(p+2,2*p),path(p+1,2*p-1),path(2*p+2,3*p-1),path(p+2,2*p-1)
    up,u2p=S.Poly(1-q**p,x,q),S.Poly(1-q**(2*p),x,q)
    rebuilt=A*B*T-up*Aleft*Bright*T-u2p*A*Bleft*Ttail+up*u2p*Aleft*M*Ttail
    assert rebuilt==P[n-2]
    assert P[-1]==S.Poly(x,x,q)*P[-2]-S.Poly(1-q**(3*p),x,q)*P[-3]
    # Build Gaussian coefficients using Pascal recursion, independently of P.
    gaussian=[S.Poly(1,q)]
    for j in range(1,n+1):
        gaussian=[(gaussian[k] if k<j else S.Poly(0,q))+(S.Poly(q**(j-k),q)*gaussian[k-1] if k else S.Poly(0,q)) for k in range(j+1)]
    H=S.Poly(sum(a.as_expr()*v**(2*k) for k,a in enumerate(gaussian)),v,q)
    transformed=S.Poly(S.expand(v**n*P[-1].as_expr().subs(x,v+1/v)),v,q)
    assert transformed==H and gaussian[0]==S.Poly(1,q)
    # Polynomial CD telescope in denominator-cleared form.
    W=S.Poly(1,q)
    kernel=S.Poly(1,x,q)
    for j in range(1,n):
        uj=S.Poly(1-q**j,x,q)
        kernel=uj*kernel+P[j]*P[j]
    wronskian=P[-1].diff(x)*P[-2]-P[-1]*P[-2].diff(x)
    assert kernel==wronskian
    results.append({'p':p,'n':n,'tail_identity':True,'successor_recurrence':True,'Gaussian_H_normalization':True,'Gaussian_H_constant_one':True,'ordinary_square_CD_identity':True,'status':'PASS'})
    print('PASS',p,n,flush=True)
Path(__file__).with_name('EXACT_CHECKS.json').write_text(json.dumps({'status':'PASS','controls':results,'sympy_version':S.__version__},indent=2)+'\n')
