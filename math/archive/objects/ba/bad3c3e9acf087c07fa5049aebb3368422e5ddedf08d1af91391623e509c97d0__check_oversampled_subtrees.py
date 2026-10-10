"""Finite-field identity checks for rational BM fusion, not timing claims."""
import random,json
from pathlib import Path
p=97

def root(n):
 return next(x for x in range(1,p) if pow(x,n,p)==1 and (n==1 or pow(x,n//2,p)!=1))
def trim(a):
 while len(a)>1 and a[-1]==0:a.pop()
 return a

def add(a,b):
 c=[0]*max(len(a),len(b))
 for i,x in enumerate(a):c[i]=(c[i]+x)%p
 for i,x in enumerate(b):c[i]=(c[i]+x)%p
 return trim(c)
def scale(a,x):return trim([v*x%p for v in a])
def mul(a,b):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]=(c[i+j]+x*y)%p
 return trim(c)
def mod(a,q):
 a=a[:]; inv=pow(q[-1],-1,p)
 while len(a)>=len(q):
  i=len(a)-len(q);c=a[-1]*inv%p
  for j,v in enumerate(q):a[i+j]=(a[i+j]-c*v)%p
  trim(a)
 return a

def modpow(a,n,q):
 z=[1]
 while n:
  if n&1:z=mod(mul(z,a),q)
  a=mod(mul(a,a),q);n//=2
 return z

def peval(a,t):
 z=0
 for x in reversed(a):z=(z*t+x)%p
 return z

def num(bs,ws):
 z=[0]
 for i,b in enumerate(bs):
  v=[b]
  for j,w in enumerate(ws):
   if i!=j:v=mul(v,[1,-w%p])
  z=add(z,v)
 return z

def recover(ys,lam,om):
 n=len(ys)
 return [sum(v*pow(om,(-j*r)%n,p) for j,v in enumerate(ys))*pow(n,-1,p)*pow(lam,-r,p)%p for r in range(n)]

def split(vals,lam,om):
 n=len(vals);h=n//2;e=[];o=[]
 for j in range(h):
  x=lam*pow(om,j,p)%p
  e.append((vals[j]+vals[j+h])*pow(2,-1,p)%p)
  o.append((vals[j]-vals[j+h])*pow(2*x,-1,p)%p)
 return e,o

rng=random.Random(20261009);counts=dict(cases=0,modular_corrections=0,parity_leaf_values=0,corrected_decoded_coefficients=0)
for L in [1,2,4,8]:
 for h in range(6):
  S=L*2**h
  if S>32:continue
  B=2**h;om=root(S)
  for _ in range(30):
   lam=rng.randrange(1,p);c=pow(lam,S,p)
   allowed=[w for w in range(1,p) if (1-c*pow(w,S,p))%p]
   k=rng.randint(1,min(L,len(allowed)));ws=rng.sample(allowed,k);bs=[rng.randrange(p) for w in ws]
   q=[1]
   for w in ws:q=mul(q,[1,-w%p])
   P=num(bs,ws);rs=modpow([(-x)%p for x in q[1:]],S,q)
   H=add(P,scale(mod(mul(P,rs),q),-c%p))
   bprime=[b*(1-c*pow(w,S,p))%p for b,w in zip(bs,ws)]
   assert H==num(bprime,ws);counts['modular_corrections']+=1
   grid=[lam*pow(om,j,p)%p for j in range(S)]
   raw=[peval(P,t)*pow(peval(q,t),-1,p)%p for t in grid]
   corr=[peval(H,t)*pow(peval(q,t),-1,p)%p for t in grid]
   states={0:(raw,corr)};ll=lam;oo=om
   for d in range(h):
    nxt={}
    for r,(a,b) in states.items():
     a0,a1=split(a,ll,oo);b0,b1=split(b,ll,oo)
     nxt[r]=(a0,b0);nxt[r+2**d]=(a1,b1)
    states=nxt;ll=ll*ll%p;oo=oo*oo%p
   answer=[None]*S
   for r,(rawleaf,correctleaf) in states.items():
    for j,v in enumerate(rawleaf):
     y=ll*pow(oo,j,p)%p
     target=sum(b*pow(w,r,p)*pow((1-pow(w,B,p)*y)%p,-1,p) for b,w in zip(bs,ws))%p
     assert v==target;counts['parity_leaf_values']+=1
    coeff=recover(correctleaf,ll,oo)
    for m,v in enumerate(coeff):answer[r+B*m]=v
   target=[sum(b*pow(w,m,p) for b,w in zip(bs,ws))%p for m in range(S)]
   assert answer==target
   counts['corrected_decoded_coefficients']+=S;counts['cases']+=1
res={'status':'passed','field_prime':p,'counts':counts,'limitation':'Direct polynomial arithmetic and quadratic DFT checks certify identities only, not fast running times.'}
Path(__file__).with_name('oversampled_subtree_checks.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
