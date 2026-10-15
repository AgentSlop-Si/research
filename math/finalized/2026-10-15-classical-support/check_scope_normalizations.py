"""Fresh bounded normalization controls for two already accepted support records.
These are not a replay of REVIEW-01/06 or a proof of broader applications.
"""
import json, math
from pathlib import Path
import sympy as s
x,q,tau,t=s.symbols('x q tau t')
checks=[]
trace_total=0
for d in (2,3,4,5,6,8,9,10,12):
    f=s.Poly(s.cyclotomic_poly(d,x),x);m=f.degree()
    Q=s.div(x**d-1,f.as_expr(),x)[0]
    rem=lambda a:s.rem(s.expand(a),f.as_expr(),x)
    for j in range(m):
        S=sum(f.nth(k)*x**(k-1-j) for k in range(j+1,m+1))
        delta=rem(x*Q*S)
        for i in range(m):
            h=rem(delta*x**i)
            tr=rem(sum(h.subs(x,x**a) for a in range(1,d) if math.gcd(a,d)==1))
            assert tr==(d if i==j else 0),(d,i,j,tr)
            trace_total+=1
checks.append({'name':'integral_trace_extraction','d':[2,3,4,5,6,8,9,10,12],'identities':trace_total,'pass':True})
for A in range(1,9):
    J=s.hermite_prob(A+1,x)+A*(1-tau)*s.hermite_prob(A-1,x)
    if A%2:
        m=(A+1)//2;c=s.Rational(2*m-1,2*m)*(tau-1);alpha=-s.Rational(1,2)
        P=(-1)**m*s.factorial(m)*(s.assoc_laguerre(m,alpha,t)+c*s.assoc_laguerre(m-1,alpha,t))
        pull=2**m*P.subs(t,x*x/2)
        disc=(-1)**m*2**(2*m*m+m)*P.subs(t,0)*s.discriminant(P,t)**2
    else:
        m=A//2;c=tau-1;alpha=s.Rational(1,2)
        P=(-1)**m*s.factorial(m)*(s.assoc_laguerre(m,alpha,t)+c*s.assoc_laguerre(m-1,alpha,t))
        pull=x*2**m*P.subs(t,x*x/2)
        disc=(-1)**m*2**(2*m*m+3*m)*P.subs(t,0)**3*s.discriminant(P,t)**2
    assert s.expand(J-pull)==0
    assert s.expand(s.discriminant(J,x)-disc)==0
checks.append({'name':'hermite_laguerre_parity_and_discriminant','A':[1,2,3,4,5,6,7,8],'pass':True})
for A in range(0,7):
    U=s.hermite_prob(A,x);V=s.expand(s.I**(-A)*U.subs(x,s.I*x))
    K=s.expand(x*U*V-s.diff(U,x)*V+U*s.diff(V,x))
    ds=list(range(1,A+1))+[2*A+1]
    D=math.prod(ds[j]-ds[i] for j in range(len(ds)) for i in range(j))
    W=s.wronskian([s.hermite_prob(k,x) for k in ds],x)/D
    assert s.expand(K-W)==0
checks.append({'name':'normalized_hook_identity','A':list(range(7)),'pass':True})
for p in [3,5,7,11,13,17,19,23,29,31,37,41,43]:
    A=(p-1)//2;U=s.hermite_prob(A,x);V=s.expand(s.I**(-A)*U.subs(x,s.I*x))
    assert s.Poly(x*U*V-s.diff(U,x)*V+U*s.diff(V,x)-x**p,x,modulus=p).is_zero
checks.append({'name':'prime_hook_congruence','primes_through':43,'pass':True})
T0=s.Integer(1);T1=x-1
for n in range(1,8):
    T=T1
    D=s.Poly(s.discriminant(T,x),q)
    E,r=s.div(D,s.Poly((q-1)**(n*(n-1)//2),q))
    assert r.is_zero and E.eval(1)==math.prod(j**j for j in range(1,n+1))
    assert s.discriminant(s.hermite_prob(n,x),x)==math.prod(j**j for j in range(1,n+1))
    T0,T1=T1,s.expand((x-1)*T1-(q**n-1)*x*T0)
checks.append({'name':'signed_rs_discriminant_q1','degrees':list(range(1,8)),'pass':True})
out={'scope':'Bounded fresh normalization controls. General results are supported by the symbolic proof/source review, not inferred from finite tests. No M17 full determinant replay, no Gaussian primitivity claim, no all-composite extension.','all_passed':True,'checks':checks}
Path(__file__).with_name('FRESH_NORMALIZATION_CONTROLS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
