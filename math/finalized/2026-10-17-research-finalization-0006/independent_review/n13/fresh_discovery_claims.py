"""Independent checks of optional discovery/factorization claims, 17 Oct 2026."""
import json
from pathlib import Path
p,q,n=53,16,13

def mul(a,b):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]=(c[i+j]+x*y)%p
 return c

def prod(fs):
 a=[1]
 for b in fs:a=mul(a,b)
 return a

def solve(A,b):
 a=[r[:]+[v] for r,v in zip(A,b)];k=0
 for c in range(len(A[0])):
  t=next(i for i in range(k,len(A)) if a[i][c]);a[t],a[k]=a[k],a[t];z=pow(a[k][c],-1,p);a[k]=[z*v%p for v in a[k]]
  for i in range(len(A)):
   if i!=k:
    z=a[i][c];a[i]=[(v-z*w)%p for v,w in zip(a[i],a[k])]
  k+=1
 return [r[-1] for r in a]

def G(e,d,a,b):
 r=e*a%n;l=d*b%n;w=pow(q,e*d%n,p)
 if r+l>=n:return 0
 z=1
 for i in range(1,l+1):z=z*(1-pow(w,r+i,p))*pow((1-pow(w,i,p))%p,-1,p)%p
 return z

def f(a,b):return pow(q,10*(a+b)**2%n,p)
def v(b,a,y):return (f(a,b)-pow(y,13-a-b,p)*G(-1,1,a,b)*pow(G(-1,1,13-b,b),-1,p))*pow(G(1,1,a,b),-1,p)%p

def H(y,lam):
 rows=[(1,a) for a in range(1,5)]+[(2,2),(2,3)]
 A=[[v(b,a+j,y) for j in range(6)] for b,a in rows]
 rhs=[(-v(b,a+7,y)-lam*v(b,a+6,y))%p for b,a in rows]
 return solve(A,rhs)+[lam,1]

def elim(y,z):
 def EF(lam,s):
  h=H(y,lam);e=t=0
  for j,c in enumerate(h):
   a=s+j;den=pow(G(1,1,a,3),-1,p)
   U=(f(a,3)-pow(y,10-a,p)*G(-1,1,a,3)*pow(G(-1,1,10,3),-1,p))*den%p
   V=pow(z,a,p)*G(1,-1,a,3)*den%p
   e=(e+c*U)%p;t=(t+c*V)%p
  return e,t
 e10,f10=EF(0,1);e11,f11=EF(1,1);e20,f20=EF(0,2);e21,f21=EF(1,2)
 a=mul([e10,(e11-e10)%p],[f20,(f21-f20)%p]);b=mul([e20,(e21-e20)%p],[f10,(f11-f10)%p])
 return [(x-y)%p for x,y in zip(a,b)]
assert prod([[-6%p,1],[49,7,1],[12,21,1],[20,29,1]])==[36,25,12,17,34,9,51,1]
assert prod([[14,1],[-18%p,1],[-14%p,1],[29,14,1],[8,29,1]])==[17,25,35,42,4,3,25,1]
assert prod([[8,1],[-21%p,1],[-19%p,1],[-1%p,1],[11,25,40,1]])==[27,23,20,38,8,35,7,1]
checks=[]
for y,z,lam,want in [(14,43,51,[40,10,48]),(43,14,25,[36,30,4]),(3,3,7,[3,49,7])]:
 coeff=elim(y,z);assert coeff==want and sum(c*pow(lam,i,p) for i,c in enumerate(coeff))%p==0
 checks.append({'y':y,'z':z,'lambda':lam,'elimination_coefficients':coeff,'H':H(y,lam)})
out={'verdict':'PASS','three_base_factorizations_verified':True,'discovery_polynomials':checks,'scope':'Discovery identities only; actual existence is certified by the separate full literal checks.'}
Path(__file__).with_name('DISCOVERY_CLAIMS_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
