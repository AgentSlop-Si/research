"""Independent finite Taylor controls, using only this audit's fresh arithmetic."""
import sympy as S
import json,time,math
from pathlib import Path
from audit_compute import add,scale,mul,ev,discriminant,resultant,coeffs
OUT=Path(__file__).resolve().parent
x=S.Symbol('x')

def run(s,A,indices):
    start=time.monotonic();b=(s-1)//2;n=A*s+b;k=A//2;p=2*A+1;d=s*p
    if s==1:K=S.QQ;w=K.one;phi=S.Poly(x-1,x)
    else:
        phi=S.Poly(S.cyclotomic_poly(s,x),x);K=S.QQ.alg_field_from_poly(phi,alias='w');w=K.unit
    one=K.one;zero=K.zero
    def trunc(v):return (v+[zero]*(k+1))[:k+1]
    def plus(a,b):return [u+v for u,v in zip(a,b)]
    def times(a,b):return trunc(mul(a,b))
    def qp(e):return [w**e*K.convert(S.binomial(S.Rational(e,s),j)) for j in range(k+1)]
    ones=trunc([one]);zeros=[zero]*(k+1)
    G=[one]
    for m in range(1,b+1):G=[(G[j-1] if j else zero)+(w**j*G[j] if j<len(G) else zero) for j in range(m+1)]
    kap=(-s)**k*math.prod(range(1,A,2))
    samples=[]
    for j in indices:
        z=[-v for v in qp(j)];opz=plus(ones,z);old=ones;cur=opz
        if n==0:cur=ones
        for m in range(2,n+1):
            qm1=qp(m-1);qm1[0]-=one
            new=plus(times(opz,cur),times(times(qm1,z),old))
            old,cur=cur,new
        expected=kap*ev(G,-w**j)
        assert all(v==zero for v in cur[:k])
        assert cur[k]==expected
        assert expected!=zero
        samples.append({'j':j,'all_lower_coefficients_zero':True,'exact_leading_coefficient_matches':True})
    R=one
    for j in range(s):R*=ev(G,-w**j)
    Delta=discriminant(G,one)
    BB=Delta*R
    def qpoly(a):
        if s==1:return S.Poly(S.Rational(a.numerator,a.denominator),x)
        cs=list(reversed(a.to_list()))
        return S.Poly(sum(S.Rational(c.numerator,c.denominator)*x**i for i,c in enumerate(cs)),x)
    bad=S.gcd(S.Poly(phi,x,modulus=p),S.Poly(qpoly(BB),x,modulus=p))
    assert bad.degree()<phi.degree()
    result={'s':s,'A':A,'p':p,'n':n,'order_in_t':k,'kappa':kap,'tested_j':samples,'lower_bad_factor_degree':bad.degree(),'lower_cyclotomic_degree':phi.degree(),'elapsed_seconds':time.monotonic()-start}
    print(json.dumps({a:result[a] for a in ['s','A','p','n','order_in_t','kappa','lower_bad_factor_degree','elapsed_seconds']}),flush=True)
    return result
if __name__=='__main__':
    # These are local Taylor tests at lower cyclotomic orders, not new full content computations.
    cases=[(1,2,[0,1,4]),(1,6,[0,1,12]),(1,8,[0,1,16]),(5,6,list(range(5))+[5,64]),(9,2,list(range(9))+[9,44]),(13,2,list(range(13))+[13,64])]
    rr=[run(*v) for v in cases]
    (OUT/'SERIES_CONTROLS.json').write_text(json.dumps(rr,indent=2)+'\n')
