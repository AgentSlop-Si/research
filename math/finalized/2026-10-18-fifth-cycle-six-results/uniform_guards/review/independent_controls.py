"""Independent F020 proof-transcription controls, authored by the reviewer.
The author checker is replayed separately and is never imported here.
"""
from pathlib import Path
import hashlib, json, sys
import sympy as s
q,z,x,v,t=s.symbols('q z x v t')
root=Path(__file__).resolve().parent
checks=[]
def check(name,test,**detail):
    assert bool(test), name
    checks.append(dict(name=name,passed=True,**detail))
def zero(expr): return s.cancel(s.expand(expr))==0
# Independent construction: three-term Rogers-Szego recurrence, not Pascal rows.
H=[s.Integer(1),1+z]
for n in range(1,8): H.append(s.expand((1+z)*H[-1]-z*(1-q**n)*H[-2]))
for b,h in enumerate(H):
    direct=sum(s.cancel(s.prod(1-q**j for j in range(b-k+1,b+1))/s.prod(1-q**j for j in range(1,k+1)))*z**k for k in range(b+1))
    check(f'product_definition_b{b}',zero(h-direct))
    check(f'q_difference_b{b}',zero(h.subs(z,q*z)-(1-z)*h-q**b*z*h.subs(z,z/q)))
    check(f'reciprocity_b{b}',zero(z**b*h.subs(z,1/z)-h))
    check(f'half_lattice_start_b{b}',zero(h.subs({q:v**2,z:v},simultaneous=True)-s.prod(1+v**a for a in range(1,b+1))))
    if b%2==0:
        E=s.prod(1-q**(2*a-1) for a in range(1,b//2+1))
        check(f'even_starts_b{b}',zero(h.subs(z,-1)-E) and zero(h.subs(z,-q)-E))
    else:
        r=(b-1)//2
        E=s.prod(1-q**(2*a-1) for a in range(1,r+1))
        g=E*sum(s.prod((1-q**(2*a))/(1-q**(2*a-1)) for a in range(j+1,r+1)) for j in range(r+1))
        check(f'odd_start_b{b}',zero(h.subs(z,-1)) and zero(h.subs(z,-q)-E*(1-q**b)))
        check(f'forced_root_sector_formula_b{b}',zero(s.diff(h,z).subs(z,-1)-g))
# Symbolic rotation exponents for arbitrary real j and integer b.
j,B=s.symbols('j B')
a=lambda J:B*J/2+J**2/4
check('rotation_forward_exponent',zero(a(j)-a(j+1)+j/2+(2*B+1)/4))
check('rotation_backward_exponent',zero(B+j+a(j-1)-a(j+1)))
check('rotated_reciprocity_exponent',zero(-a(-j)-B*j+a(j)))
# Exact generic Jacobi normalizations; c values are independent formal symbols.
c=s.symbols('c0:6',positive=True)
T=[s.Integer(1),x/2]
for n in range(1,5):T.append(s.expand(x*c[n]*T[-1]-T[-2]))
M=[T[0]]+[s.cancel(T[n]/(s.prod(c[k] for k in range(1,n))/2)) for n in range(1,6)]
check('even_first_monic_step',zero(M[2]-x*M[1]+2/c[1]*M[0]))
for n in range(2,5):check(f'even_monic_step_{n}',zero(M[n+1]-x*M[n]+M[n-1]/(c[n]*c[n-1])))
S=[s.Integer(1),c[1]*x]
for n in range(2,5):S.append(s.expand(x*c[n]*S[-1]-S[-2]))
N=[s.cancel(S[n]/s.prod(c[k] for k in range(1,n+1))) for n in range(5)]
for n in range(2,5):check(f'odd_monic_step_{n}',zero(N[n]-x*N[n-1]+N[n-2]/(c[n]*c[n-1])))
for parity in (1,-1):
    A=[s.Integer(1),c[0]*x-parity]
    for n in range(1,4):A.append(s.expand(c[n]*x*A[-1]-A[-2]))
    N=[s.cancel(A[n]/s.prod(c[k] for k in range(n))) for n in range(5)]
    check(f'half_first_monic_step_{parity}',zero(N[1]-x+parity/c[0]))
    for n in range(1,4):check(f'half_monic_step_{parity}_{n}',zero(N[n+1]-x*N[n]+N[n-1]/(c[n]*c[n-1])))
# Newton face controls from the reconstructed actual coefficients, including face derivative.
for b in range(2,9):
    hp=s.Poly(H[b],z)
    check(f'gaussian_leading_degrees_b{b}',all(s.Poly(hp.nth(k),q).degree()==k*(b-k) and s.Poly(hp.nth(k),q).LC()==1 for k in range(b+1)))
    for J in range(1,b+1):
        vals=[k*(k-2*J+1) for k in range(b+1)];minimum=min(vals)
        face=sum(v**k for k,val in enumerate(vals) if val==minimum)
        check(f'newton_face_b{b}_j{J}',minimum==-J*(J-1) and zero(face-v**(J-1)*(1+v)) and s.diff(face,v).subs(v,-1)!=0)
    degree=2*sum((b-i)*(b+1-2*i) for i in range(1,b+1))
    check(f'discriminant_exponent_b{b}',degree==b*(b*b-1)//3)
for b in range(2,6):
    D=s.Poly(s.discriminant(H[b],z),q)
    V,rem=s.div(D,s.Poly((q-1)**(b*(b-1)//2),q))
    check(f'direct_discriminant_b{b}',D.LC()==1 and D.degree()==b*(b*b-1)//3 and rem.is_zero and V.LC()==1 and V.degree()==b*(b-1)*(2*b-1)//6)
D4=s.discriminant(H[4],z);V4=s.cancel(D4/(q-1)**6)
expected=(q+1)**2*(q*q+q+1)*(q**3+3*q*q+3*q+5)**2*(q**4+3*q**3+4*q*q+3*q+5)
check('exact_V4_factorization',zero(V4-expected))
mod=s.Poly(V4.subs(q,1+t),t,modulus=3)
check('exact_t3_b4_failure',mod.as_expr()==t**14-t**13-t**11-t**10+t**9+t**8 and min(m[0] for m,c in mod.terms())==8 and 8>=s.totient(9))
# Independent q-Hermite and CD constructions.
P=[s.Integer(1),x]
for n in range(1,8):P.append(s.expand(x*P[-1]-(1-q**n)*P[-2]))
for b in range(1,9):
    check(f'hermite_map_b{b}',zero(v**b*P[b].subs(x,v+1/v)-H[b].subs(z,v*v)))
    weighted=sum(P[k]**2*s.prod(1-q**a for a in range(k+1,b)) for k in range(b))
    check(f'CD_kernel_b{b}',zero(weighted-s.diff(P[b],x)*P[b-1]+P[b]*s.diff(P[b-1],x)))
# Bounded controls at already certified orders; both direct node values and gcds.
for d,b,e in [(3,0,1),(3,1,2),(3,2,1),(5,3,2),(5,4,1),(9,4,2),(9,5,5),(9,8,1)]:
    K=s.QQ.alg_field_from_poly(s.Poly(s.cyclotomic_poly(d,q),q),'omega')
    Q=K.unit**e;R=K.poly_ring(z);Z=R.gens[0]
    hs=[R.one,1+Z]
    for n in range(1,b):hs.append((1+Z)*hs[-1]-Z*(1-Q**n)*hs[-2])
    h=hs[b];u=h.exquo(Z+1) if b%2 else h
    check(f'field_order_d{d}_b{b}_embedding{e}',Q**d==K.one and all(Q**k!=K.one for k in range(1,d)))
    check(f'negative_node_values_d{d}_b{b}_embedding{e}',all(u.evaluate(0,-Q**k)!=K.zero for k in range(d)))
    check(f'positive_node_values_d{d}_b{b}_embedding{e}',all(h.evaluate(0,Q**k)!=K.zero for k in range(d)))
    check(f'node_gcd_d{d}_b{b}_embedding{e}',u.gcd(Z**d+1).degree()==0 and h.gcd(Z**d-1).degree()==0)
    if b%2: check(f'forced_simple_d{d}_b{b}_embedding{e}',h.diff(0).evaluate(0,-K.one)!=K.zero)
    if (d,b)==(9,4):check('t_failure_has_no_charzero_collision',h.gcd(h.diff(0)).degree()==0)
# Complex Jacobi counterexample: genuine nondegeneracy is insufficient for simplicity.
u=[s.Rational(3,5)-s.Rational(4,5)*s.I,s.Rational(4,5),s.Rational(3,5)+s.Rational(4,5)*s.I]
R=[s.Integer(1),x]
for a in u:R.append(s.expand(x*R[-1]-a*R[-2]))
check('complex_recurrence_counterexample',zero(R[-1]-(x*x-1)**2) and all(s.re(a)>0 for a in u))
# Independent source retrieval versus frozen source bytes and Git blob IDs.
base=root.parent/'f020_uniform_guards_20261018_1919'
source_checks=[]
for key in ('residual_boundary','accepted_composition'):
    fresh=json.loads((root/'sources'/f'{key}_fresh.json').read_text())
    raw=fresh['content'].encode();frozen=(base/'sources'/f'{key}.md').read_bytes()
    gitsha=hashlib.sha1(f'blob {len(raw)}\0'.encode()+raw).hexdigest()
    check(f'pinned_source_{key}',raw==frozen and gitsha==fresh['git_blob_sha1'])
    source_checks.append({'source_url':fresh['source_url'],'git_blob_sha1':gitsha,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'fresh_content_matches_frozen':True})
(root/'SOURCE_VERIFICATION.json').write_text(json.dumps(source_checks,indent=2)+'\n')
result={'status':'PASS','assertions':len(checks),'python':sys.version,'sympy':s.__version__,'scope':'Independent bounded transcription controls. Unlimited claims are proved in the report and reviewed separately. No order census extension.','checks':checks}
(root/'INDEPENDENT_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','assertions':len(checks)}))
