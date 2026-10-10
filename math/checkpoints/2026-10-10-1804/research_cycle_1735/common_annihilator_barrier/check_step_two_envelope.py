"""Fresh exact finite-field control of the uniform proof's operator identities.
This tests algebraic identities only, not the complex coherence inequality.
"""
from sympy import isprime,primitive_root
import json,random
from pathlib import Path

def poly_eval(c,z,p):
 v=0
 for a in c[::-1]:v=(v*z+a)%p
 return v

def poly_mul(a,b,p):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]=(c[i+j]+x*y)%p
 return c

def transform(c,q,p,lam,pref,raise_degree):
 out=[0]*(len(c)+raise_degree)
 for j,x in enumerate(c):
  out[j]=(out[j]-lam*x)%p
  out[j+raise_degree]=(out[j+raise_degree]+pref*pow(q,2*j,p)*x)%p
 return out

results=[]
for n,d in [(35,4),(1025,4),(1297,4)]:
 p=n+1
 while not isprime(p):p+=n
 q=pow(int(primitive_root(p)),(p-1)//n,p)
 h=pow(4,-1,n);e=pow(2,-1,n);rho=pow(q,e,p)
 D=[1]
 for j in range(2,d):D=poly_mul(D,[1,-pow(q,j,p)%p],p)
 rng=random.Random(n);E=[rng.randrange(p) for _ in range(d-2+(d-1)//2)];O=[rng.randrange(p) for _ in range(d-2+(d-2)//2)];R=[rng.randrange(p) for _ in range(d-1)]
 def values(E,O,R):
  return [(pow(q,h*k*k%n,p)*(poly_eval(E,pow(q,k,p),p)+pow(rho,k,p)*poly_eval(O,pow(q,k,p),p))+poly_eval(R,pow(q,k,p),p))%p for k in range(n)]
 B=values(E,O,R);x=3
 for j in range(d-1):
  lam=x*x*pow(q,2*j,p)%p
  for _ in range(2):
   B=[(B[(k+2)%n]-lam*B[k])%p for k in range(n)]
   E=transform(E,q,p,lam,q,1)
   O=transform(O,q,p,lam,q*q%p,1)
   R=transform(R,q,p,lam,1,0)
   assert B==values(E,O,R)
 target=[k*pow(x,k-1,p)*poly_eval(D,pow(q,k,p),p)%p if k else 0 for k in range(n+4*(d-1))]
 for j in range(d-1):
  lam=x*x*pow(q,2*j,p)%p
  for _ in range(2):target=[(target[k+2]-lam*target[k])%p for k in range(len(target)-2)]
 assert all(v==0 for v in target)
 results.append({'N':n,'d':d,'p':p,'q_residue':q,'x':x,'operator_factors':2*(d-1),'all_envelope_transform_entries_pass':True,'all_derivative_target_annihilation_entries_pass':True})
pth=Path(__file__).parent/'STEP_TWO_ENVELOPE_CONTROL.json'
pth.write_text(json.dumps({'status':'PASS','scope':'Exact algebraic operator identities only; not a coherence or rank certificate','cases':results},indent=2)+'\n')
print(json.dumps(results,indent=2))
