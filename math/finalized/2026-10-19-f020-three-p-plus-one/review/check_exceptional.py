"""Independent exact characteristic-zero p=3 certificate for n=10."""
import sympy as S
from pathlib import Path
import json,time
q,x,y=S.symbols('q x y')
t0=time.time()
seq=[S.Poly(1,x,q),S.Poly(x,x,q)]
for n in range(1,10):seq.append(S.Poly(x*seq[-1].as_expr()-(1-q**n)*seq[-2].as_expr(),x,q))
P=S.Poly(seq[-1].as_expr(),x)
assert P.degree()==10 and all(m[0]%2==0 for m in P.monoms())
Q=S.Poly(sum(a*y**(m[0]//2) for m,a in P.terms()),y)
D=S.Poly(Q.nth(0),q)
assert S.expand(D.as_expr()-S.prod(q**j-1 for j in [1,3,5,7,9]))==0
print('Built Q5; computing discriminant',flush=True)
Delta=S.Poly(S.discriminant(Q.as_expr(),y),q)
assert Delta.degree()==140 and Delta.LC()!=0
print('Discriminant degree',Delta.degree(), 'seconds', time.time()-t0,flush=True)
checks=[]
for order in [27,81]:
    cycl=S.Poly(S.cyclotomic_poly(order,q),q)
    entries={}
    for name,poly in [('constant',D),('discriminant',Delta)]:
        rem=poly.rem(cycl)
        gcd=poly.gcd(cycl)
        modrem=S.Poly(poly.as_expr(),q,modulus=2).rem(S.Poly(cycl.as_expr(),q,modulus=2))
        assert not rem.is_zero and gcd.degree()==0 and not modrem.is_zero
        entries[name]={'degree':poly.degree(),'integer_remainder':list(reversed([int(a) for a in rem.all_coeffs()])),'gcd_degree':gcd.degree(),'mod2_remainder':str(modrem.as_expr())}
    checks.append({'order':order,'phi_degree':cycl.degree(),'checks':entries})
print('Computing direct degree-10 discriminant',flush=True)
full=S.Poly(S.discriminant(P.as_expr(),x),q)
# For even degree 2m, disc Q(X²)=(-1)^m 4^m Q(0) disc(Q)^2.
assert full == S.Poly(-1024*D.as_expr()*Delta.as_expr()**2,q)
print('Full discriminant identity PASS; seconds',time.time()-t0,flush=True)
result={'status':'PASS','Q5':str(Q.as_expr()),'constant_degree':D.degree(),'discriminant_degree':Delta.degree(),'discriminant_coefficients_ascending':list(reversed([int(a) for a in Delta.all_coeffs()])),'controls':checks,'degree_coverage':'For s>=5, deg Phi_(3^s)>=162>140, so neither D nor nonzero Delta can vanish at a primitive 3^s root. The only allowed remaining orders 27 and 81 are certified above.','full_discriminant_identity':'Disc_X P_10 = -1024 Q5(0) (Disc_Y Q5)^2','sympy_version':S.__version__,'elapsed_seconds':time.time()-t0}
Path(__file__).with_name('P3_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
