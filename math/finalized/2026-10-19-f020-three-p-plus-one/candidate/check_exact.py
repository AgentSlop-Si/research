#!/usr/bin/env python3
"""Fresh exact recurrence, p=3 certificate, H transfer and CD controls."""
import json,time
from math import comb
from pathlib import Path
import sympy as s
OUT=Path(__file__).resolve().parent
q,x,y=s.symbols('q x y')

def build(n):
    ps=[s.Poly(1,x),s.Poly(x,x)]
    for j in range(1,n):ps.append(s.Poly(x*ps[-1].as_expr()-(1-q**j)*ps[-2].as_expr(),x))
    return ps

def coeffs(poly,var=q):return list(reversed([int(v) for v in s.Poly(poly,var).all_coeffs()]))
def gaussian(n):
    row=[s.Poly(1,q)]
    for m in range(1,n+1):
        nxt=[]
        for k in range(m+1):
            a=row[k] if k<m else s.Poly(0,q)
            b=row[k-1].mul(s.Poly(q**(m-k),q)) if k else s.Poly(0,q)
            nxt.append(a+b)
        row=nxt
    return row

t=time.time(); ps=build(22); p10=ps[10]
print("Recurrence rebuilt",flush=True)
assert all(k[0]%2==0 for k,c in p10.terms())
Q=s.Poly(sum(c*y**(k[0]//2) for k,c in p10.terms()),y)
D=s.Poly(Q.nth(0),q)
assert D==s.Poly(-s.prod(1-q**j for j in [1,3,5,7,9]),q)
Delta=s.Poly(s.discriminant(Q.as_expr(),y),q)
assert Delta.degree()==140 and Delta.LC()==1
print('Q discriminant computed',flush=True)
# Different requested invariant: ordinary X-discriminant agrees with even lift.
full=s.Poly(s.discriminant(p10.as_expr(),x),q)
assert full==s.Poly(-1024*D.as_expr()*Delta.as_expr()**2,q)
print('Full discriminant verified',flush=True)
remdata=[]
for order,expected_exps in [
    (27,[17,16,15,13,8,5,3]),
    (81,[51,49,48,47,45,44,43,37,36,34,32,31,30,27,25,24,23,21,20,15,14,9,6,4,2,1])]:
    phi=s.Poly(s.cyclotomic_poly(order,q),q)
    rem=Delta.rem(phi)
    rem2=s.Poly(rem,q,modulus=2)
    expected=s.Poly(sum(q**j for j in expected_exps),q,modulus=2)
    assert rem2==expected and not rem2.is_zero
    assert s.gcd(Delta,phi).degree()==0
    remdata.append({'order':order,'phi_degree':phi.degree(),'integer_remainder_ascending':coeffs(rem),'mod2_nonzero_exponents':expected_exps,'rational_gcd_degree':0})
assert s.totient(243)>Delta.degree()
# Transcription controls for the original family and bilinear identity.
identity_cases=[]
for n in [10,16,22]:
    print('Checking exact identities',n,flush=True)
    P=ps[n]; prev=ps[n-1]; prior=ps[n-2]
    K=P.diff()*prev-P*prev.diff()
    Kprev=prev.diff()*prior-prev*prior.diff()
    assert K==prev**2+Kprev.mul_ground(1-q**(n-1))
    H=gaussian(n); rhs=[s.Poly(0,q) for _ in range(n+1)]
    for (j,),a in P.terms():
        a=s.Poly(a,q)
        for r in range(j+1):
            exponent=n+j-2*r
            assert exponent%2==0
            rhs[exponent//2]+=a.mul_ground(comb(j,r))
    assert rhs==H and H[0]==s.Poly(1,q)
    assert s.Poly(P.eval(2),q).eval(1)==2**n
    identity_cases.append({'degree':n,'ordinary_CD_telescope':True,'actual_Gaussian_transform':True,'H_constant':1,'P_at_q1_X2':2**n})
data={'status':'PASS','sympy_version':s.__version__,'elapsed_seconds':time.time()-t,
      'p3':{'degree':10,'allowed_s_min':3,'Q_coefficients_Y_ascending':[coeffs(Q.nth(j)) for j in range(6)],'D_ascending':coeffs(D),'Delta_ascending':coeffs(Delta),'Delta_degree':140,'Delta_leading_coefficient':1,'ordinary_X_discriminant_identity':'Disc_X P_10 = -1024 D (Disc_Y Q_5)^2','cyclotomic_remainders':remdata,'higher_s_min':5,'phi_243_degree':162},'exact_identity_cases':identity_cases}
(OUT/'EXACT_CHECKS.json').write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps({'status':'PASS','p3_Delta_degree':Delta.degree(),'exact_degrees':[10,16,22],'elapsed_seconds':data['elapsed_seconds']}))
