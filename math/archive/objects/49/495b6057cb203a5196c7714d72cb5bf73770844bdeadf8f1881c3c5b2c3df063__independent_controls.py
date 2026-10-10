"""Fresh exact controls for the ramified cluster lemma and its bounded corollaries.
No predecessor code is imported or executed. SymPy is used only as an installed
exact polynomial arithmetic library. Predecessor certificates are read as data.
"""
from pathlib import Path
from functools import lru_cache
from math import comb, factorial, prod, gcd, isqrt
import json
import sympy as s
q,z,x=s.symbols('q z x')
OUT=Path(__file__).resolve().parent
@lru_cache(None)
def H(n):
    # Gaussian q-Pascal, independent of the three-term recurrence in the proof.
    row=[s.Integer(1)]
    for j in range(1,n+1):
        row=[s.expand((row[k] if k<j else 0)+(q**(j-k)*row[k-1] if k else 0)) for k in range(j+1)]
    return sum(c*z**k for k,c in enumerate(row))
def mod(expr,d):return s.rem(s.Poly(s.expand(expr),q),s.Poly(s.cyclotomic_poly(d,q),q)).as_expr()
def modx(expr,d):return sum(mod(c,d)*x**k[0] for k,c in s.Poly(s.expand(expr),x).terms())
def eps_coefficient(n,d,k,L):
    # q -> q*(1+epsilon^2)^(1/d), z -> -q^k+epsilon*x.
    out=0
    for (r,j),c in s.Poly(H(n),q,z).terms():
        for h in range(min(j,L)+1):
            if (L-h)%2==0:
                t=(L-h)//2
                out+=c*q**r*s.binomial(s.Rational(r,d),t)*comb(j,h)*(-q**k)**(j-h)*x**h
    return modx(out,d)
results={'recurrence_checks':[], 'q_lucas_checks':[], 'local_cluster_checks':[], 'leading_discriminant_checks':[], 'overlap_controls':[], 'fixed_base_contents':[], 'bad_reduction_controls':[], 'isolated_existing_certificates':[]}
for n in range(2,13):
    assert s.expand(H(n)-(1+z)*H(n-1)-(q**(n-1)-1)*z*H(n-2))==0
    results['recurrence_checks'].append(n)
for d,A,b in [(3,2,0),(3,2,1),(5,2,2),(5,1,2),(7,1,2),(9,1,4)]:
    n=d*A+b
    assert all(mod(c,d)==0 for c in s.Poly(H(n)-(1+z**d)**A*H(b),z).all_coeffs())
    results['q_lucas_checks'].append({'d':d,'A':A,'b':b,'n':n})
for d,A,b in [(1,4,0),(3,2,0),(5,2,2),(5,1,2),(7,1,2)]:
    n=d*A+b
    for k in range(d):
        for L in range(A):assert eps_coefficient(n,d,k,L)==0
        lead=eps_coefficient(n,d,k,A)
        ga=mod(H(b).subs(z,-q**k),d)
        expected=ga*sum(s.Rational((-1)**j*factorial(A)*d**(A-j),2**j*factorial(j)*factorial(A-2*j))*q**((-k*(A-2*j))%d)*x**(A-2*j) for j in range(A//2+1))
        assert modx(lead-expected,d)==0,(d,A,b,k,lead,expected)
    results['local_cluster_checks'].append({'d':d,'A':A,'b':b,'n':n,'all_d_clusters_checked':d})
for d,A,b in [(1,4,0),(3,2,0),(5,1,2),(5,2,2)]:
    n=d*A+b; K=d*A*(A-1)//2; phi=s.Poly(s.cyclotomic_poly(d,q),q)
    D=s.Poly(s.discriminant(H(n),z),q)
    E=s.exquo(D,phi**K)
    assert not s.rem(E,phi).is_zero
    Q=s.exquo(s.Poly(q**d-1,q),phi).as_expr()
    DB=s.discriminant(H(b),z) if b>=2 else 1
    R=s.resultant(z**d+1,H(b),z)
    P=prod(j**j for j in range(1,A+1))
    C=(-1)**(A*(d-1)//2)*d**(d*A*(A+1)//2)*P**d*DB*R**(2*A)
    assert mod(E.as_expr()-Q**K*C,d)==0
    results['leading_discriminant_checks'].append({'d':d,'A':A,'b':b,'n':n,'exact_Phi_d_order':K,'leading_formula_verified':True})
for d,A,b in [(3,2,1),(3,3,1)]:
    n=d*A+b; D=s.Poly(s.discriminant(H(n),z),q); phi=s.Poly(s.cyclotomic_poly(d,q),q); K=0
    while s.rem(D,phi).is_zero:D=s.exquo(D,phi);K+=1
    assert mod(s.resultant(z**d+1,H(b),z),d)==0
    results['overlap_controls'].append({'d':d,'A':A,'b':b,'n':n,'actual_order':K,'inapplicable_separated_order':d*A*(A-1)//2})
for d,wanted in [(5,5),(9,3**8),(13,13**4)]:
    b=(d-1)//2
    D=mod(s.discriminant(H(b),z),d); R=mod(s.resultant(z**d+1,H(b),z),d); B=s.Poly(mod(D*R,d),q)
    content=int(s.polys.polytools.primitive(B.as_expr(),q)[0]); assert content==wanted
    primitive=s.Poly(B.as_expr()/content,q)
    assert gcd(*[abs(int(c)) for c in primitive.all_coeffs()])==1
    results['fixed_base_contents'].append({'d':d,'b':b,'discriminant_remainder':str(D),'cluster_resultant_remainder':str(R),'product_remainder':str(B.as_expr()),'content':content,'primitive_part':str(primitive.as_expr())})
for d,p in [(5,61),(13,5)]:
    b=(d-1)//2; phi=s.Poly(s.cyclotomic_poly(d,q),q,modulus=p)
    DG=s.Poly(s.discriminant(H(b),z),q,modulus=p); RG=s.Poly(s.resultant(z**d+1,H(b),z),q,modulus=p)
    dc=s.gcd(phi,DG); rc=s.gcd(phi,RG)
    assert dc.degree()+rc.degree()>0
    assert s.gcd(phi,DG*RG).degree()<phi.degree()
    if (d,p)==(13,5):
        factors=[f for f,e in s.factor_list(phi)[1]]
        assert len(factors)==3 and all(f.degree()==4 for f in factors)
        for f in factors:
            assert s.rem(s.Poly(q**(p**4)-q,q,modulus=p),f).is_zero
            assert s.gcd(s.Poly(q**(p**2)-q,q,modulus=p),f).degree()==0
    results['bad_reduction_controls'].append({'d':d,'p':p,'gcd_discriminant_with_Phi':str(dc.as_expr()),'gcd_cluster_resultant_with_Phi':str(rc.as_expr()),'a_good_factor_still_exists':True})
# Verify ONLY the two already accepted isolated cases needed to include p=d
# in the d=5 and d=13 target families. No finite-range census is performed.
def trim(a):
    while len(a)>1 and a[-1]==0:a.pop()
    return a
def pmul(a,b,p):
    c=[0]*(len(a)+len(b)-1)
    for i,u in enumerate(a):
        for j,v in enumerate(b):c[i+j]=(c[i+j]+u*v)%p
    return trim(c)
def padd(a,b,p):return trim([((a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0))%p for i in range(max(len(a),len(b)))])
source=Path('diagonal_chirp_classification_0246/MODULAR_CERTIFICATES.json')
certs=json.loads(source.read_text())
selected=[c for c in certs if c['N'] in [25,169]]
(OUT/'EXCEPTION_CERTIFICATES.json').write_text(json.dumps(selected,indent=2)+'\n')
for N in [25,169]:
    c=next(c for c in certs if c['N']==N); p=c['prime_p']; v=c['primitive_q']; m=(N-1)//2
    assert p>1 and all(p%t for t in range(2,isqrt(p)+1))
    prime_divisors=[t for t in range(2,N+1) if N%t==0 and all(t%u for u in range(2,isqrt(t)+1))]
    assert pow(v,N,p)==1 and all(pow(v,N//t,p)!=1 for t in prime_divisors)
    row=[1]
    for j in range(1,m+1):row=[((row[k] if k<j else 0)+(pow(v,j-k,p)*row[k-1] if k else 0))%p for k in range(j+1)]
    T=[((-1)**(m-k)*u)%p for k,u in enumerate(row)]; assert T==c['T']
    DT=[k*T[k]%p for k in range(1,len(T))]
    assert padd(pmul(c['squarefree_bezout_u'],T,p),pmul(c['squarefree_bezout_v'],DT,p),p)==[1]
    results['isolated_existing_certificates'].append({'N':N,'prime_p':p,'primitive_q':v,'certificate_identity_verified':True,'source':str(source)})
(OUT/'CONTROL_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps({k:len(v) for k,v in results.items()},indent=2))
print('All exact controls passed.')
