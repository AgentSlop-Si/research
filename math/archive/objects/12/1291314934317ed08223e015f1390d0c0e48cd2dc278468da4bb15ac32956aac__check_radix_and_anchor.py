#!/usr/bin/env python3
"""Independent growing-radix and grid-anchor checks; no source imports."""
import json,math,random
from pathlib import Path
def field(n):
 p=n+1
 while any(p%d==0 for d in range(2,math.isqrt(p)+1)):p+=n
 proper=[d for d in range(1,n) if n%d==0]
 for w in range(2,p):
  if pow(w,n,p)==1 and all(pow(w,d,p)!=1 for d in proper):return p,w
 raise AssertionError
def run():
 rng=random.Random(202610092225);out={'radix_banks':0,'radix_output_entries':0,'expanded_data_entries':0,'grid_anchor_cases':[]}
 for M in [2,3,4,5,6,8,9,10,12,16,20,24]:
  p,w=field(M*M);eta=pow(w,M,p)
  B=[[rng.randrange(p) for j in range(M)] for h in range(M)]
  C=[[sum(B[h][j]*pow(w,(1-M*h)*t*j,p) for j in range(M))%p for t in range(M)] for h in range(M)]
  for b in [d for d in range(1,M+1) if M%d==0]:
   m=M//b;zeta=pow(eta,m,p);omega_small=pow(w,b*b,p);eta_small=pow(eta,b,p);nodes=[]
   for d in range(m):
    q=pow(w,1-M*d,p);qsmall=pow(q,b*b,p);nodes.append(qsmall)
    assert qsmall==omega_small*pow(eta_small,-b*d,p)%p
    assert pow(qsmall,m*m,p)==1 and all(pow(qsmall,a,p)!=1 for a in range(1,m*m) if m*m%a==0)
    Bhat=[[sum(B[d+c*m][j]*pow(zeta,-c*ell,p) for c in range(b))%p for ell in range(b)] for j in range(M)]
    for r in range(b):
     for a in range(m):
      t=r+b*a
      for ell in range(b):
       expected=sum(C[d+c*m][t]*pow(zeta,-c*ell,p) for c in range(b))%p
       routed=sum(pow(q,t*j,p)*Bhat[j][(ell+t*j)%b] for j in range(M))%p
       split=sum(pow(q,r*s,p)*pow(q,b*s*a,p)*sum(pow(qsmall,a*v,p)*pow(q,b*r*v,p)*Bhat[s+b*v][(ell+r*s)%b] for v in range(m)) for s in range(b))%p
       assert expected==routed==split;out['radix_output_entries']+=1
   assert len(set(nodes))==m//math.gcd(b,m)
   assert m*b*b*b*m==M*M*b
   out['expanded_data_entries']+=M*M*b;out['radix_banks']+=1
 for M in [2,4,8,16,32,64]:
  N=M*M;bits=N.bit_length()-1
  def rev(j):return int(format(j,'0%db'%bits)[::-1],2)
  def entry(i,j,a,b):
   it,iu=divmod(i,M);jt,ju=divmod(j,M)
   if jt>it or ju>iu:return 0
   dt,du=it-jt,iu-ju;return math.comb(dt+du,dt)*a**dt*b**du
  assert rev(0)==0 and rev(N-1)==N-1
  assert rev(N-2)==N//2-1 and rev(N-1-M)==N-1-M//2
  cols=[N-2,N-1-M,N-1]
  pairs=[(entry(N-1,j,2,3),entry(rev(N-1),rev(j),5,7)) for j in cols]
  r=M//2;assert pairs==[(3,5**r),(2,7**r),(1,1)]
  det=2*7**r-5**r-1;gap=2*7**r-3*5**r+5
  assert det>0 and gap>0
  for j in range(N):
   assert entry(0,j,2,3)==int(j==0) and entry(rev(0),rev(j),5,7)==int(j==0)
   assert entry(j,N-1,2,3)==int(j==N-1) and entry(rev(j),rev(N-1),5,7)==int(j==N-1)
  out['grid_anchor_cases'].append({'M':M,'N':N,'last_row_pairs':pairs,'homogeneous_determinant':det,'constant_modulus_triangle_gap':gap})
 return out
if __name__=='__main__':
 r=run();Path(__file__).with_name('RADIX_ANCHOR_RESULTS.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
