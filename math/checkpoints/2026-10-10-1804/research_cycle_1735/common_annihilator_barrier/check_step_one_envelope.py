"""Fresh exact controls for the frozen step-one bank guard proof.
Finite-field identities and integer inequalities only; no finite-field lift is claimed.
"""
from sympy import isprime,primitive_root
from pathlib import Path
import random,json

def peval(c,z,p):
 v=0
 for x in reversed(c):v=(v*z+x)%p
 return v

def pmul(a,b,p):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]=(c[i+j]+x*y)%p
 return c

def transform(P,R,q,rho,qh,lam,p):
 V=[0]*(len(P)+1)
 for j,x in enumerate(P):
  V[j]=(V[j]-lam*x)%p
  V[j+1]=(V[j+1]+qh*pow(rho,j,p)*x)%p
 U=[(pow(q,j,p)-lam)*x%p for j,x in enumerate(R)]
 return V,U

out=[]
for n in [27,35,37,47,127]:
 d=(n+13)//10;m=n-d;r=3*(d-1)
 p=n+1
 while not isprime(p):p+=n
 q=pow(int(primitive_root(p)),(p-1)//n,p)
 h=pow(4,-1,n);e=pow(2,-1,n);rho=pow(q,e,p);qh=pow(q,h,p)
 assert rho*rho%p==q
 D=[1]
 for j in range(2,d):D=pmul(D,[1,-pow(q,j,p)%p],p)
 rng=random.Random(n);P=[rng.randrange(p) for _ in range(3*d-6)];R=[rng.randrange(p) for _ in range(d-1)]
 def values(P,R):
  return [(pow(q,h*k*k%n,p)*peval(P,pow(rho,k,p),p)+peval(R,pow(q,k,p),p))%p for k in range(n)]
 B=values(P,R);x=3
 lambdas=[x*pow(q,j,p)%p for j in range(d-1) for repeat in range(2)]+[pow(q,j,p) for j in range(d-1)]
 target=[k*pow(x,k-1,p)*peval(D,pow(q,k,p),p)%p if k else 0 for k in range(n+r)]
 for lam in lambdas:
  B=[(B[(k+1)%n]-lam*B[k])%p for k in range(n)]
  P,R=transform(P,R,q,rho,qh,lam,p)
  assert B==values(P,R)
  target=[(target[k+1]-lam*target[k])%p for k in range(len(target)-1)]
 assert all(v==0 for v in R)
 assert all(v==0 for v in target)
 assert len(P)-1<=6*d-10<n
 assert n-4*d+4>=6*d-9
 out.append({'N':n,'d':d,'m':m,'banks':2*m+2,'p':p,'q_residue':q,'rho_residue':rho,'operator_degree':r,'max_final_polynomial_degree':6*d-10,'derivative_zero_block_length':n-4*d+4,'operator_identity_all_entries':True,'ordinary_component_killed':True,'derivative_target_annihilated':True})
for n in range(27,100000,2):
 d=(n+13)//10;m=n-d
 assert d>=4 and n>=10*d-13
 assert m>=(n-1)//2 and m>=3*(d-1)
 assert m+1>=3*(d-1)
 assert n-5*d+12>=(n+1)//2
 assert n-4*d+4>=6*d-9 and 6*d-10<n
 assert n-2*d>=4*d-7 and 4*d-8<n
 assert m>d-2
p=Path(__file__).parent
(p/'STEP_ONE_ENVELOPE_CONTROL.json').write_text(json.dumps({'status':'PASS','scope':'Exact operator identities and bounded integer sanity checks; the Markdown source supplies the all-order proof','all_odd_integer_checks':[27,99999],'cases':out},indent=2)+'\n')
print(json.dumps(out,indent=2))
