#!/usr/bin/env python3
"""Own exact Q(w) arithmetic. No source code imported. w^2+w+1=0."""
from fractions import Fraction as Q
from pathlib import Path
import json,sys,cmath
class E:
 def __init__(self,a=0,b=0):
  if isinstance(a,E): self.a,self.b=a.a,a.b
  else:self.a,self.b=Q(a),Q(b)
 def __add__(self,y):
  y=E(y);return E(self.a+y.a,self.b+y.b)
 __radd__=__add__
 def __neg__(self):return E(-self.a,-self.b)
 def __sub__(self,y):return self+-E(y)
 def __rsub__(self,y):return E(y)+-self
 def __mul__(self,y):
  y=E(y);return E(self.a*y.a-self.b*y.b,self.a*y.b+self.b*y.a-self.b*y.b)
 __rmul__=__mul__
 def inverse(self):
  n=self.a*self.a-self.a*self.b+self.b*self.b
  assert n;return E((self.a-self.b)/n,-self.b/n)
 def __truediv__(self,y):return self*E(y).inverse()
 def __pow__(self,n):
  if n<0:return self.inverse()**(-n)
  out=E(1);a=self
  while n:
   if n&1:out=out*a
   a=a*a;n//=2
  return out
 def __eq__(self,y):y=E(y);return self.a==y.a and self.b==y.b
 def encode(self):return [str(self.a),str(self.b)]
def mm(a,b):return [[sum((x*y for x,y in zip(row,col)),E()) for col in zip(*b)] for row in a]
def eye(n):return [[E(i==j) for j in range(n)] for i in range(n)]
def inverse(a):
 n=len(a);z=[row[:]+eye(n)[i] for i,row in enumerate(a)]
 for j in range(n):
  k=next(k for k in range(j,n) if z[k][j]!=0);z[j],z[k]=z[k],z[j];c=z[j][j].inverse();z[j]=[x*c for x in z[j]]
  for k in range(n):
   if k!=j:
    c=z[k][j];z[k]=[x-c*y for x,y in zip(z[k],z[j])]
 return [row[n:] for row in z]

import itertools as it, random,math
def I(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def add(a,b,p):return [[(x+y)%p for x,y in zip(r,s)] for r,s in zip(a,b)]
def mul(a,b,p):return [[sum(x*y for x,y in zip(r,c))%p for c in zip(*b)] for r in a]
def inv(a,p):
 n=len(a);z=[[x%p for x in a[i]]+I(n)[i] for i in range(n)]
 for j in range(n):
  k=next(k for k in range(j,n) if z[k][j]);z[j],z[k]=z[k],z[j];v=pow(z[j][j],-1,p);z[j]=[x*v%p for x in z[j]]
  for k in range(n):
   if k!=j:
    v=z[k][j];z[k]=[(x-v*y)%p for x,y in zip(z[k],z[j])]
 return [r[n:] for r in z]
def rank(a,p):
 z=[row[:] for row in a];r=0
 for j in range(len(z[0])):
  ks=[i for i in range(r,len(z)) if z[i][j]%p]
  if not ks:continue
  k=ks[0];z[r],z[k]=z[k],z[r];v=pow(z[r][j],-1,p);z[r]=[x*v%p for x in z[r]]
  for k in range(len(z)):
   if k!=r:
    v=z[k][j];z[k]=[(x-v*y)%p for x,y in zip(z[k],z[r])]
  r+=1
  if r==len(z):break
 return r
def sub(a,rows,cols):return [[a[i][j] for j in cols] for i in rows]
def cycles(pi):
 rem=set(range(len(pi)));out=[]
 while rem:
  start=min(rem);v=start;c=[]
  while v in rem:c.append(v);rem.remove(v);v=pi[v]
  assert v==start;out.append(c)
 return out
def green(pi,w,p):
 n=len(pi);H=I(n)
 for i,j in enumerate(pi):H[i][j]=(H[i][j]-w[i])%p
 return H,inv(H,p)
def valid(pi,w,p):return all(math.prod(w[i] for i in c)%p!=1 for c in cycles(pi))
def coeff(B,pi,tau,i,k,j,p):
 ti=tau.index(j);A,C=B[i][j],B[i][ti];BB,D=B[pi[i]][j],B[pi[i]][ti];EE,G=B[k][j],B[k][ti];FF,H=B[pi[k]][j],B[pi[k]][ti]
 return [(A*G-C*EE)%p,(BB*G-D*EE)%p,(A*H-C*FF)%p,(BB*H-D*FF)%p]
def local_rows(B,pi,tau,p):
 n=len(pi);rows={}
 for i,k in it.combinations(range(n),2):
  bad={i,k,pi[i],pi[k],tau[i],tau[k]};rows[(i,k)]=[(j,coeff(B,pi,tau,i,k,j,p)) for j in range(n) if j not in bad]
 return rows
def det2(a,p):return (a[0][0]*a[1][1]-a[0][1]*a[1][0])%p
def hom(c,p):return [[c[2],c[3]],[-c[0]%p,-c[1]%p]]
def target(n,p,w):
 h=(n+1)//2;F=[[pow(w,i*j,p) for j in range(n)] for i in range(n)];A=[[pow(w,h*i*i,p) if i==j else 0 for j in range(n)] for i in range(n)];return F,A,inv(add(inv(F,p),A,p),p)
def main():
 # N3 closure over Q(w), distinct from the prior two-Green representation seal.
 w=E(0,1);F=[[w**(i*j) for j in range(3)] for i in range(3)];A=[[w**(2*i*i) if i==j else E() for j in range(3)] for i in range(3)];Fi=inverse(F);B=inverse([[Fi[i][j]+A[i][j] for j in range(3)] for i in range(3)]);M=mm(F,A);K=mm(B,A);M2=mm(M,M);K2=mm(K,K)
 for i in range(3):
  for j in range(3):
   assert M2[i][j]-(2+w)*M[i][j]+(3+3*w)*E(i==j)==0
   assert (6+4*w)*K2[i][j]-(8+7*w)*K[i][j]+(3+3*w)*E(i==j)==0
   assert (-2-3*w)*B[i][j]+(6+4*w)*mm(mm(B,A),B)[i][j]==F[i][j]
 assert (6+4*w)-(8+7*w)+(3+3*w)==1 and K[0][1]!=0
 # N3 supplied finite coefficients, exact guarded inverse and online scan.
 p=241;F3,A3,B3=target(3,p,15);P=[1,2,0];Pi=[2,0,1];D=[15,1,1];t=207;kappa=2;Gs=[green(pi,[t]*3,p)[1] for pi in [P,Pi]];Bconstructed=[[kappa*D[i]*(Gs[0][i][j]+Gs[1][i][j])*D[j]%p for j in range(3)] for i in range(3)];assert Bconstructed==B3 and (1-pow(t,3,p))%p==22
 K3=mul(B3,A3,p);assert add(add([[66*x%p for x in r] for r in mul(K3,K3,p)],[[128*x%p for x in r] for r in K3],p),[[48*x%p for x in r] for r in I(3)],p)==[[0]*3 for _ in range(3)];assert add([[194*x%p for x in r] for r in B3],[[66*x%p for x in r] for r in mul(mul(B3,A3,p),B3,p)],p)==F3
 # Explicit recurrence scan, independently authored without inverse matrices.
 def scan(v,t,pi):
  out=[]
  for i in range(3):
   j=i;s=0;weight=1
   for _ in range(3):s=(s+weight*v[j])%p;weight=weight*t%p;j=pi[j]
   out.append(s*pow(1-pow(t,3,p),-1,p)%p)
  return out
 def applyB(v):
  vv=[D[i]*v[i]%p for i in range(3)];y=scan(vv,t,P);z=scan(vv,t,Pi);return [kappa*D[i]*(y[i]+z[i])%p for i in range(3)]
 for j in range(3):
  v=[int(i==j) for i in range(3)];y=applyB(v);z=applyB([A3[i][i]*y[i]%p for i in range(3)]);assert [(194*y[i]+66*z[i])%p for i in range(3)]==[F3[i][j] for i in range(3)]
 # N5 target gate construction: do not copy reported coefficient rows.
 pi=[2,3,4,0,1];tau=[3,2,4,1,0];F5,A5,B5=target(5,p,91);assert pow(91,5,p)==1 and all(pow(91,i,p)!=1 for i in range(1,5));assert [pi[tau[i]] for i in range(5)]!=[tau[pi[i]] for i in range(5)]
 G5=sum(pow(91,3*i*i,p) for i in range(5))%p;c5=5*G5%p;assert (G5,c5,(1+c5)%p)==(103,33,34)
 rows=local_rows(B5,pi,tau,p);hs={};local=[]
 for pair,rr in rows.items():
  assert len(rr)<=1
  if rr:
   j,c=rr[0];assert any(c);H=hom(c,p);guard=det2(H,p);assert guard;hs[pair]=H
   # Projective witness u_i=e0, u_k=H e0; no component division.
   ui=[1,0];uk=[H[0][0],H[1][0]];assert any(uk);z=[ui[0]*uk[0],ui[1]*uk[0],ui[0]*uk[1],ui[1]*uk[1]];assert sum(x*y for x,y in zip(c,z))%p==0
   local.append(dict(pair=list(pair),column=j,coefficients=c,homography_guard=guard))
 assert len(hs)==7
 C1=mul(mul(inv(hs[(0,2)],p),hs[(1,2)],p),hs[(0,1)],p);C3=mul(mul(inv(mul(hs[(2,4)],hs[(0,2)],p),p),hs[(3,4)],p),hs[(0,3)],p);comm=add(mul(C1,C3,p),[[-x%p for x in r] for r in mul(C3,C1,p)],p);assert C1==[[75,4],[33,140]] and C3==[[106,125],[20,52]] and det2(comm,p)==162
 cuts=[]
 for s in range(5):
  A={(s+j)%5 for j in range(2)};C=[j for j in range(5) if j not in A];cross=[sum(plan[i] not in A for i in A) for plan in [pi,tau]];br=rank(sub(B5,sorted(A),C),p);assert cross[0]==2 and sum(cross)>=br==2;cuts.append(dict(start=s,crossings=cross,target_rank=br))
 # Genuine same-order sums including boundary masks and zero edge weights.
 rng=random.Random(3510);controls=[]
 for trial in range(24):
  branches=[];Q=[];nonzero_endpoints=trial%3!=0
  for bi,perm in enumerate([pi,tau]):
   weights=[rng.randrange(2,p) for _ in range(5)]
   if trial%2==0:weights[(trial+bi)%5]=0
   while not valid(perm,weights,p):weights[0]=(weights[0]+1)%p
   H,G=green(perm,weights,p);left=[rng.randrange(1,p) for _ in range(5)];right=[rng.randrange(1,p) for _ in range(5)]
   if not nonzero_endpoints:left[bi]=0;right[(bi+2)%5]=0
   branch=[[left[i]*G[i][j]*right[j]%p for j in range(5)] for i in range(5)];branches.append(branch)
   Q.append(inv(branch,p) if nonzero_endpoints else None)
  T=add(branches[0],branches[1],p);rr=local_rows(T,pi,tau,p);guards=[det2(hom(c,p),p) for v in rr.values() for j,c in v]
  if nonzero_endpoints:
   assert mul(mul(Q[0],T,p),Q[1],p)==add(*Q,p)
   for (i,k),v in rr.items():
    for j,c in v:
     ai,bi=Q[0][i][i],Q[0][i][pi[i]];ak,bk=Q[0][k][k],Q[0][k][pi[k]];z=[ai*ak,bi*ak,ai*bk,bi*bk];assert sum(x*y for x,y in zip(c,z))%p==0
  if all(guards):
   hh={pair:hom(v[0][1],p) for pair,v in rr.items() if v};c1=mul(mul(inv(hh[(0,2)],p),hh[(1,2)],p),hh[(0,1)],p);c3=mul(mul(inv(mul(hh[(2,4)],hh[(0,2)],p),p),hh[(3,4)],p),hh[(0,3)],p);cm=add(mul(c1,c3,p),[[-x%p for x in r] for r in mul(c3,c1,p)],p);assert det2(cm,p)==0
  controls.append(dict(trial=trial,singular_endpoints=not nonzero_endpoints,zero_edges=trial%2==0,zero_homography_guards=guards.count(0)))
 out=dict(status='PASS',N3_complex_quadratic_closure=True,N3_exact_minimal_degree=2,N3_complex_four_scan_identity=True,N3_finite_denominator=22,N3_basis_outputs_checked=3,N5_Gauss_scalar=G5,N5_feedback_guard=(1+c5)%p,N5_coefficients=local,N5_halfcuts=cuts,N5_return_maps=[C1,C3],N5_commutator=comm,N5_commutator_determinant=det2(comm,p),genuine_green_controls=controls,source_code_executed=False)
 path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('INDEPENDENT_RESULTS.json');path.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
