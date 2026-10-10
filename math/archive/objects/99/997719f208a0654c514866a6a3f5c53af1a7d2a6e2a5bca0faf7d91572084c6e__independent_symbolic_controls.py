"""Fresh controls. No archived or predecessor program is imported or executed."""
import hashlib,json,time
from pathlib import Path
import sympy as s
out=Path(__file__).parent
q,z,x=s.symbols('q z x');t=time.time()
# Generic discriminants via the polynomial recurrence, exact integer arithmetic.
a,b=s.S(1),z+1; rows=[]
for n in range(2,13):
    a,b=b,s.Poly((1+z)*b-(1-q**(n-1))*z*a,z).as_expr().expand()
    d=s.Poly(s.discriminant(b,z),q)
    fs=s.factor_list(d)[1]
    cyc=[]
    for f,e in fs:
        if f.is_cyclotomic:
            # The following bound comfortably contains every factor seen here.
            matches=[N for N in range(1,2*n+2) if f==s.Poly(s.cyclotomic_poly(N,q),q)]
            assert len(matches)==1
            cyc.append({'order':matches[0],'multiplicity':e})
    phi=s.Poly(s.cyclotomic_poly(2*n+1,q),q)
    assert s.gcd(d,phi).degree()==0
    rows.append({'degree_n':n,'cyclotomic_factors':cyc,'target_N':2*n+1,'target_cyclotomic_gcd_degree':0,'discriminant_factorization':str(s.factor(d.as_expr()))})
# Exact 4x4 counterexample to the proposed generic sector-to-simplicity inference.
rho=(1-s.I)/s.sqrt(2)
u=[rho*(15-8*s.I)/17,rho*s.Rational(4,17),rho*(15+8*s.I)/17]
p0,p1=s.S(1),x
for uj in u:p0,p1=p1,s.expand(x*p1-uj*p0)
assert s.simplify(p1-(x*x-rho)**2)==0
assert s.simplify(s.discriminant(p1,x))==0
# A separate exact failure of q-discriminant => ordinary discriminant.
h2=z*z-2*z+1 # H_2(z;-3)
dq=s.cancel((h2.subs(z,-3*z)-h2)/(-4*z))
assert s.discriminant(h2,z)==0
qres=s.resultant(h2,dq,z)
assert qres==16
res={'generic_discriminants':rows,'sector_counterexample':{'rho':str(rho),'squared_edges':[str(v) for v in u],'characteristic_polynomial':str((x*x-rho)**2),'discriminant':0},'q_discriminant_counterexample':{'q':-3,'H2':str(h2),'Dq_H2':str(dq),'ordinary_discriminant':0,'q_resultant':int(qres)},'elapsed_seconds':time.time()-t}
(out/'SYMBOLIC_CONTROLS.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps({'generic_degrees':list(range(2,13)),'sector_counterexample_verified':True,'q_discriminant_counterexample_verified':True,'elapsed_seconds':res['elapsed_seconds']}))
