"""Fresh, independently written exact controls; no submitted code is imported."""
import json
from pathlib import Path
import sympy as S
x,y,z,t,c=S.symbols('x y z tau c')
checks=[]
for m in range(1,9):
    for s in [0,1]:
        A=2*m+s-1; al=S.Rational(2*s-1,2)
        Cm=(-1)**m*2**m*S.factorial(m)
        Cp=(-1)**(m-1)*2**(m-1)*S.factorial(m-1)
        R=S.Poly(S.hermite_prob(2*m+s,x)/x**s,x)
        R=S.expand(sum(co*y**(int(mono[0])//2) for mono,co in R.terms()))
        Rp=S.Poly(S.hermite_prob(2*m-2+s,x)/x**s,x)
        Rp=S.expand(sum(co*y**(int(mono[0])//2) for mono,co in Rp.terms()))
        L=S.assoc_laguerre(m,al,z); Lp=S.assoc_laguerre(m-1,al,z)
        W=S.expand(S.diff(R,y)*Rp-R*S.diff(Rp,y))
        D=S.expand(S.diff(L,z)*Lp-L*S.diff(Lp,z))
        cc=S.Rational(A,2*m)*(t-1)
        p=S.expand(R-A*(t-1)*Rp)
        J=x*S.hermite_prob(A,x)-A*t*S.hermite_prob(A-1,x)
        tests={
          'parity_laguerre':S.expand(R-Cm*L.subs(z,y/2))==0,
          'J_parity':S.expand(J-x**s*p.subs(y,x*x))==0,
          'J_quasi_laguerre':S.expand(p-Cm*(L+cc*Lp).subs(z,y/2))==0,
          'wronskian_scalar':S.expand(W-Cm*Cp*S.Rational(1,2)*D.subs(z,y/2))==0,
          'collision_location':S.factor(2*(m*cc*cc+(2*m+al)*cc+m+al)/cc-t*(A*t+1)/(t-1))==0,
          'W_squarefree':S.degree(S.gcd(W,S.diff(W,y)),y)==0,
        }
        if m<=5:
            dp=S.discriminant(p,y)
            dJ=S.discriminant(J,x)
            tests['disc_composition']=S.expand(dJ-(-1)**m*4**m*p.subs(y,0)**(2*s+1)*dp**2)==0
            dL=S.discriminant(L+c*Lp,z)
            tests['disc_scale']=S.expand(dp-2**(m*(m-1))*S.factorial(m)**(2*m-2)*dL.subs(c,cc))==0
            zc=(m*c*c+(2*m+al)*c+m+al)/c
            pref=S.prod(S.Integer(k)**(k-2*m+3) for k in range(1,m+1))*S.prod((k+al)**(k-1) for k in range(1,m))
            su=pref*(-c)**m*(L+c*Lp).subs(z,zc)/(m+al+c*m)
            tests['Sawa_Uchida_3_6']=S.cancel(dL-su)==0
        assert all(tests.values()),(m,s,tests)
        checks.append({'m':m,'s':s,'A':A,'alpha':str(al),'checks':tests})
M,T=S.symbols('m tau')
param=[]
for s in [0,1]:
    A=2*M+s-1; al=S.Rational(2*s-1,2); cc=A*(T-1)/(2*M)
    result=S.factor(2*(M*cc*cc+(2*M+al)*cc+M+al)/cc-T*(A*T+1)/(T-1))
    assert result==0
    param.append({'s':s,'symbolic_location_difference':str(result)})
out={'status':'PASS','date':'2026-10-17','fresh_code':True,'uploaded_code_executed':False,'families_checked':len(checks),'parametric_location_identities':param,'controls':checks}
Path(__file__).with_name('normalization_controls.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'PASS','families_checked':len(checks),'total_exact_checks':sum(len(a['checks']) for a in checks),'parametric_location_identities':param}))
