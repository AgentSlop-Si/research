"""Fresh second-review controls. No imports from research directories."""
from pathlib import Path
import json
import sympy as s
q,x,w,z=s.symbols('q x w z')
# F4 is represented as F2[a]/(a^2+a+1). Reduce all expressions canonically.
a=s.symbols('a')
def f4(expr):
    p=s.Poly(s.expand(expr),a,x,modulus=2)
    return s.rem(p.as_expr(),a*a+a+1,a,domain=s.GF(2).poly_ring(x)).as_expr()
L=x*x+a*a; R=x*x+a
full=f4((x+1)*L*R+a*a*x*R+a*x*L)
assert f4(full-(x**5+x**4+x*x+x+1))==0
P=s.Poly(full,x,modulus=2)
assert s.gcd(P,P.diff()).degree()==0
assert f4(L-(x+a)**2)==f4(R-(x+a*a)**2)==0
f=s.Poly(q**5+q*q+1,q,modulus=2)
assert f.is_irreducible
rec=s.Poly(q**5+q**3+1,q,modulus=2)
assert rec.is_irreducible and f != rec
assert s.rem(s.Poly(q**31-1,q,modulus=2),f).is_zero
# All-order expressions are proved in text; these are only small transcription controls.
beta=lambda j:(1-q**(2*j))*(1-q**(2*j+1))
C=[s.Integer(1),w-2+q+q*q]
for k in range(1,4):
    C.append(s.expand((w-2+q**(2*k+1)+q**(2*k+2))*C[k]-beta(k)*C[k-1]))
checks=[]
for m in range(1,5):
    kernel=s.expand(sum(C[k]**2*s.prod(beta(j) for j in range(k+1,m)) for k in range(m)))
    wronskian=s.diff(C[m],w)*C[m-1]-C[m]*s.diff(C[m-1],w)
    assert s.expand(kernel-wronskian)==0
    row={'m':m,'kernel_identity':True}
    if m<=3:
        assert s.expand(s.resultant(C[m],kernel,w)-s.discriminant(C[m],w)*s.prod(beta(j)**j for j in range(1,m)))==0
        p=s.Poly(C[m].subs(w,x+2),x)
        pp=s.Poly(p.as_expr(),x,q,modulus=2).as_expr()
        A=sum(s.Poly(pp,x).coeff_monomial(x**j)*w**(j//2) for j in range(0,m+1,2))
        B=sum(s.Poly(pp,x).coeff_monomial(x**j)*w**((j-1)//2) for j in range(1,m+1,2))
        rs=s.resultant(A,B,w)
        assert s.Poly(s.discriminant(p.as_expr(),x)-rs**2,q,modulus=2).is_zero
        u=s.expand(z**m*p.as_expr().subs(x,z+1/z))
        du=s.discriminant(u,z)
        target=p.as_expr().subs(x,2)*p.as_expr().subs(x,-2)*s.discriminant(p.as_expr(),x)**2
        assert s.expand(du-target)==0
        assert s.Poly(du-p.as_expr().subs(x,0)**2*rs**4,q,modulus=2).is_zero
        row.update(resultant_identity=True,trace_discriminant_identity=True,mod2_discriminant_identity=True)
    checks.append(row)
vals=[]
for e in range(0,8):
    M=5**e
    def v5(k):
        n=0
        while k%5==0: k//=5;n+=1
        return n
    direct=sum((27*r//2)*5**v5(r) for r in range(1,(M-1)//2+1))
    num=(216*e+45)*25**e-16*e*M-45
    assert num%160==0 and direct==num//160
    vals.append({'e':e,'prefactor_valuation':direct})
result={'status':'PASS','historical_or_supplied_code_executed':False,
 'f020_F4_model_checked':True,'f020_order31_synthetic_factor_checked':True,
 'symbolic_small_controls':checks,'q29_valuation_formula_controls':vals,
 'scope':'Finite transcription controls only. General conclusions rely on the independently reviewed algebraic proofs.'}
Path(__file__).with_name('F020_Q29_SECOND_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','symbolic_cases':len(checks),'valuation_cases':len(vals)}))
