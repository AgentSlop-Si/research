#!/usr/bin/env python3
"""Independent linear-work raw kernel preparation, no uploaded imports."""
import json,math
from pathlib import Path
def field(n):
 p=n+1
 while any(p%d==0 for d in range(2,math.isqrt(p)+1)):p+=n
 proper=[d for d in range(1,n) if n%d==0]
 for w in range(2,p):
  if pow(w,n,p)==1 and all(pow(w,d,p)!=1 for d in proper):return p,w
 raise AssertionError
def batch_inverse(v,p):
 prefix=[1]
 for x in v:
  assert x;prefix.append(prefix[-1]*x%p)
 z=pow(prefix[-1],-1,p);ans=[0]*len(v)
 for i in range(len(v)-1,-1,-1):ans[i]=z*prefix[i]%p;z=z*v[i]%p
 return ans
def root_table(w,n,p):
 a=[1]
 for _ in range(1,n):a.append(a[-1]*w%p)
 assert a[-1]*w%p==1
 return a
def solve_step(b,s,tab,deninv,p):
 m=len(b);n=m*m;d=math.gcd(s,m);L=m//d;a=tab[s%n];out=[0]*m
 for base in range(d):
  u=[(base+r*s)%m for r in range(L)]
  y0=(b[u[0]]+sum(tab[(s*(L-r))%n]*b[u[r]] for r in range(1,L)))%p*deninv%p
  out[u[0]]=y0
  for r in range(1,L):out[u[r]]=(a*out[u[r-1]]+b[u[r]])%p
 assert all((out[u]-a*out[(u-s)%m]-b[u])%p==0 for u in range(m))
 return out
def prepare(m,p,w):
 n=m*m;tab=root_table(w,n,p);eta=tab[m]
 den=[(1-tab[(s*(m//math.gcd(s,m)))%n])%p for s in range(1,m+1)]
 inv=batch_inverse(den,p)
 D=[[1]+[0]*(m-1)];P=[[1]+[0]*(m-1)]
 for s in range(1,m+1):
  prev=P[-1];rhs=[(tab[s-1]*prev[(u-(s-1))%m]-eta*prev[u])%p for u in range(m)]
  P.append(solve_step(rhs,s,tab,inv[s-1],p))
  if s<m:
   prev=D[-1];rhs=[tab[s-1]*prev[(u-(s-1))%m]%p for u in range(m)]
   D.append(solve_step(rhs,s,tab,inv[s-1],p))
 return P,D,den
def run():
 out={'cases':[],'spectral_table_values':0,'raw_product_coefficients':0,'inversions_per_complete_preparation':1,'scope':'Exact cyclic-solve preparation. No fast arbitrary-input multiplication claim.'}
 for m in list(range(2,21))+[24,32]:
  p,w=field(m*m);eta=pow(w,m,p);P,D,den=prepare(m,p,w)
  # Independently expand the product directly in the cyclic S ring.
  direct=[[1]+[0]*(m-1)]
  for j in range(m):
   nxt=[row[:] for row in direct]+[[0]*m]
   for s,row in enumerate(direct):
    for u,v in enumerate(row):nxt[s+1][(u+j)%m]=(nxt[s+1][(u+j)%m]+pow(w,j,p)*v)%p
   direct=nxt
  assert P==direct;out['raw_product_coefficients']+=m*(m+1)
  for h in range(m):
   q=pow(w,1-m*h,p);F=[1]
   for r in range(1,m+1):F.append(F[-1]*(1-pow(q,r,p))%p)
   for s in range(m):
    sampled=sum(D[s][u]*pow(eta,-h*u,p) for u in range(m))%p
    expected=pow(q,s*(s-1)//2,p)*pow(F[s],-1,p)%p
    assert sampled==expected;out['spectral_table_values']+=1
  out['cases'].append({'M':m,'N':m*m,'p':p,'omega':w,'denominators_nonzero':all(den),'cyclic_solves_P_and_D':2*m-1})
 return out
if __name__=='__main__':
 result=run();Path(__file__).with_name('RAW_PREPARATION_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
