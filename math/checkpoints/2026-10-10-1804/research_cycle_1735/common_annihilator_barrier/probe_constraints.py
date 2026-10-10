import json, math
from sympy import nextprime, primitive_root

def data(n,p,q):
 h=pow(4,-1,n)
 def g(a,b,eps,delt):
  r=(eps*a)%n;l=(delt*b)%n
  if r+l>=n:return 0
  z=q if eps*delt==1 else pow(q,-1,p)
  u=1
  for j in range(1,l+1):u=u*(1-pow(z,r+j,p))*pow(1-pow(z,j,p),-1,p)%p
  return u
 def f(a,b):return pow(q,(h*(a+b)**2)%n,p)
 seq=[]
 for b in range(1,(n+1)//2):
  T=f(n-b,b)*pow(g(n-b,b,-1,1),-1,p)%p
  seq.append([(f(a,b)-T*g(a,b,-1,1))*pow(g(a,b,1,1),-1,p)%p for a in range(b,n-b)])
 return seq

def rref(a,p):
 a=[r[:] for r in a]
 if not a:return a,[]
 m=len(a);w=len(a[0]);i=0;piv=[]
 for j in range(w):
  k=next((k for k in range(i,m) if a[k][j]%p),None)
  if k is None:continue
  a[i],a[k]=a[k],a[i]
  a[i]=[x*pow(a[i][j],-1,p)%p for x in a[i]]
  for k in range(m):
   if k!=i and a[k][j]:
    c=a[k][j];a[k]=[(x-c*y)%p for x,y in zip(a[k],a[i])]
  piv.append(j);i+=1
  if i==m:break
 return a,piv

def probe(n):
 p=n+1
 while not __import__('sympy').isprime(p):p+=n
 q=pow(int(primitive_root(p)),(p-1)//n,p)
 seq=data(n,p,q);out=[]
 for m in range((n-1)//2,n-1):
  a=[s[r:r+m+1] for s in seq for r in range(len(s)-m)]
  _,piv=rref(a,p);rank=len(piv)
  _,piv2=rref([r[:-1] for r in a],p);rank2=len(piv2)
  out.append([m,len(a),rank,rank2])
  if rank==rank2:break
 return {'N':n,'p':p,'q':q,'constraints':out,'first_compatible':out[-1][0] if out[-1][2]==out[-1][3] else None}
if __name__=='__main__':
 results=[]
 for n in range(3,66,2):
  d=probe(n);results.append(d);print(d,flush=True)
 with open('research_cycle_1735/common_annihilator_barrier/PROBE_RESULTS.json','w') as f:json.dump(results,f,indent=2)
