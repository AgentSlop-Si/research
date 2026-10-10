#!/usr/bin/env python3
"""Independent exact checker. Standard library only; no predecessor source execution."""
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path
import json,hashlib,time
ROOT=Path(__file__).resolve().parent
class C:
 def __init__(self,x=0):
  if isinstance(x,C):self.a=x.a
  elif isinstance(x,(int,Q)):self.a=(Q(x),Q(0),Q(0),Q(0))
  else:self.a=tuple(Q(v) for v in x)+(Q(0),)*(4-len(x))
 def __add__(self,o):
  if not isinstance(o,(int,Q,C)):return NotImplemented
  o=C(o);return C(tuple(a+b for a,b in zip(self.a,o.a)))
 __radd__=__add__
 def __neg__(self):return C(tuple(-a for a in self.a))
 def __sub__(self,o):return self+-C(o) if isinstance(o,(int,Q,C)) else NotImplemented
 def __rsub__(self,o):return C(o)+-self
 def __mul__(self,o):
  if not isinstance(o,(int,Q,C)):return NotImplemented
  o=C(o);v=[Q(0)]*7
  for i,a in enumerate(self.a):
   for j,b in enumerate(o.a):v[i+j]+=a*b
  for k in range(6,3,-1):v[k-4]-=v[k]
  return C(v[:4])
 __rmul__=__mul__
 def __truediv__(self,o):return self*C(inv(C(o).a))
 def __pow__(self,n):
  if n<0:return C(inv(self.a))**(-n)
  a=C(1);b=self
  while n:
   if n&1:a=a*b
   b=b*b;n//=2
  return a
 def __bool__(self):return any(self.a)
 def __eq__(self,o):return isinstance(o,(C,int,Q)) and self.a==C(o).a
 def __repr__(self):return str(self.a)
@lru_cache(maxsize=None)
def inv(a):
 c=C(a);assert c
 cols=[(c*C(tuple([0]*j+[1]))).a for j in range(4)]
 mat=[[cols[j][i] for j in range(4)]+[Q(i==0)] for i in range(4)]
 for i in range(4):
  k=next(j for j in range(i,4) if mat[j][i]);mat[i],mat[k]=mat[k],mat[i]
  d=mat[i][i];mat[i]=[v/d for v in mat[i]]
  for j in range(4):
   if j!=i:
    d=mat[j][i];mat[j]=[x-d*y for x,y in zip(mat[j],mat[i])]
 ans=tuple(mat[i][-1] for i in range(4));assert c*C(ans)==1;return ans
class P:
 def __init__(self,o=0):
  if isinstance(o,P):self.d=o.d.copy()
  elif isinstance(o,dict):self.d={int(k):C(v) for k,v in o.items() if C(v)}
  else:self.d={0:C(o)} if C(o) else {}
 def __add__(self,o):
  if not isinstance(o,(int,Q,C,P)):return NotImplemented
  out=self.d.copy()
  for k,v in P(o).d.items():out[k]=out.get(k,C(0))+v
  return P(out)
 __radd__=__add__
 def __neg__(self):return P({k:-v for k,v in self.d.items()})
 def __sub__(self,o):return self+-P(o) if isinstance(o,(int,Q,C,P)) else NotImplemented
 def __rsub__(self,o):return P(o)+-self
 def __mul__(self,o):
  if not isinstance(o,(int,Q,C,P)):return NotImplemented
  out={}
  for i,a in self.d.items():
   for j,b in P(o).d.items():out[i+j]=out.get(i+j,C(0))+a*b
  return P(out)
 __rmul__=__mul__
 def __bool__(self):return bool(self.d)
 def __eq__(self,o):return isinstance(o,(int,Q,C,P)) and self.d==P(o).d
 def degree(self):return max(self.d,default=-1)
 def lc(self):return self.d[self.degree()]
 def monic(self):return self*C(1)/self.lc() if self else self
 def __truediv__(self,o):return self*C(inv(C(o).a))
 def divmod(self,o):
  o=P(o);assert o;r=P(self);q=P()
  while r and r.degree()>=o.degree():
   a=P({r.degree()-o.degree():r.lc()/o.lc()});q=q+a;r=r-a*o
  return q,r
 def gcd(self,o):
  a,b=self,P(o)
  while b:a,b=b,a.divmod(b)[1]
  return a.monic()
 def exquo(self,o):
  q,r=self.divmod(o);assert not r;return q
class R:
 def __init__(self,n=0,d=1):
  if isinstance(n,R):self.n,self.d=n.n,n.d;return
  n,d=P(n),P(d);assert d
  if not n:self.n,self.d=P(0),P(1);return
  g=n.gcd(d);n=n.exquo(g);d=d.exquo(g);lc=d.lc();self.n=n/lc;self.d=d/lc
 def __add__(self,o):
  o=R(o);return R(self.n*o.d+o.n*self.d,self.d*o.d)
 __radd__=__add__
 def __neg__(self):return R(-self.n,self.d)
 def __sub__(self,o):return self+-R(o)
 def __rsub__(self,o):return R(o)+-self
 def __mul__(self,o):
  o=R(o);return R(self.n*o.n,self.d*o.d)
 __rmul__=__mul__
 def __truediv__(self,o):
  o=R(o);return R(self.n*o.d,self.d*o.n)
 def __rtruediv__(self,o):return R(o)/self
 def __bool__(self):return bool(self.n)
 def __eq__(self,o):
  o=R(o);return self.n*o.d==o.n*self.d
Z=C([0,1]);X=R(P({1:1}));SIG=(2,7,5,0,6,1,3,4)
checks=0
def require(ok,label):
 global checks
 assert ok,label;checks+=1

def dec(x):return P({m[0]:C(c) for m,c in x})
def rat(x):return R(dec(x['numer']),dec(x['denom']))
def require_fraction(cert,key,value):require(rat(cert[key])==value,key)
def numerator(cert,key):return dec(cert[key]['numer'])
def supported(p,guards,label):
 p=P(p)
 for g in guards:
  while p.degree()>0:
   h=p.gcd(g)
   if h.degree()==0:break
   p=p.exquo(h)
 require(p.degree()==0,'denominator support '+label)
def fractions_supported(cert,keys,guards):
 for key in keys:supported(dec(cert[key]['denom']),guards,key)
def bez(cert,key,left=None,right=None,expected=P(1)):
 b=cert[key];a=dec(b['left']);c=dec(b['right'])
 if left is not None:require(a==left,key+' left source')
 if right is not None:require(c==right,key+' right source')
 require(dec(b['s'])*a+dec(b['t'])*c==expected,key+' exact Bezout')
 if 'gcd' in b:require(dec(b['gcd'])==expected,key+' gcd label')
def matrix(t):return [[R(Z**((2*(j//2)*r)%8))+(-1)**j*t[j//2]*R(Z**(((2*(j//2)+1)*r)%8)) for j in range(8)] for r in range(8)]
def B(M,w):return [M[0][j]+w*M[7][j] for j in range(8)]
def bc(M,w,r,j):
 b=B(M,w);return b[SIG[j]]*M[r][j]-b[j]*M[r][SIG[j]],b[SIG[j]]*M[r-1][j]-b[j]*M[r-1][SIG[j]]
def res(M,w,r,j,k):
 a,b=bc(M,w,r,j);c,d=bc(M,w,r,k);return a*d-c*b
# Exact polynomial quotient R_jk/B_k for a support chain j -> k -> l.
def chain(M,w,r,j,k,l):
 b=B(M,w);det=lambda a,c:M[r][a]*M[r-1][c]-M[r][c]*M[r-1][a]
 return b[l]*det(j,k)-b[k]*det(j,l)+b[j]*det(k,l)
def L46(M,w,r):return chain(M,w,r,4,6,3)
def edge(M,w,r,j,column):
 b,c=bc(M,w,r,j);return b*M[r-1][column]-c*M[r][column]
def nm(j):return 1+X*R(Z**((-2*j)%8))
def dm(j):return 1+X*R(Z**((-(2*j+1))%8))
def load(name):return json.loads((ROOT/name).read_text())
def monic_match(cert,key,frac):require(dec(cert[key])==frac.n.monic(),key+' monic numerator')

def check_wzero():
 c=load('WZERO_CERTIFICATE.json');d=X;w=R(0)
 m=matrix([R(0),R(0),R(0),d]);D6=bc(m,w,1,6)[0];D4=bc(m,w,1,4)[0]
 A6=bc(matrix([R(0),R(1),R(0),d]),w,1,6)[0]-D6
 A4=bc(matrix([R(0),R(0),R(1),d]),w,1,4)[0]-D4
 for k,v in [('A6',A6),('D6',D6),('A4',A4),('D4',D4)]:require_fraction(c,k,v)
 fractions_supported(c,['A6','D6','A4','D4'],[])
 bez(c,'A6_D6_bezout',numerator(c,'A6'),numerator(c,'D6'))
 bez(c,'A4_D4_bezout',numerator(c,'A4'),numerator(c,'D4'))
 b=-D6/A6;cc=-D4/A4;require_fraction(c,'t1',b);require_fraction(c,'t2',cc)
 guards=[numerator(c,'A6'),numerator(c,'A4')]
 q=bc(matrix([R(0),b,cc,d]),w,1,2)[0];require_fraction(c,'q_fraction',q);monic_match(c,'Q',q)
 p0=res(matrix([R(0),b,cc,d]),w,2,4,5);a0=res(matrix([R(1),b,cc,d]),w,2,4,5)-p0
 require_fraction(c,'P0',p0);require_fraction(c,'A0',a0)
 require(res(matrix([R(2),b,cc,d]),w,2,4,5)==p0+2*a0,'wzero affine t0 check')
 fractions_supported(c,['t1','t2','q_fraction','P0','A0'],guards)
 bez(c,'Q_A0_bezout',dec(c['Q']),numerator(c,'A0'))
 a=-p0/a0;require_fraction(c,'t0',a);guards.append(numerator(c,'A0'))
 h=res(matrix([a,b,cc,d]),w,3,1,4);require_fraction(c,'h_fraction',h);monic_match(c,'H',h)
 fractions_supported(c,['t0','h_fraction'],guards)
 bez(c,'Q_H_bezout',dec(c['Q']),dec(c['H']))
 return {'theorem':'u0=0 excluded','checks':checks,'degrees':[dec(c['Q']).degree(),dec(c['H']).degree()]}

def check_b15(is_b1):
 c=load('B1_CERTIFICATE.json' if is_b1 else 'B5_CERTIFICATE.json');w=X
 a=nm(0)/dm(0) if is_b1 else R(0);b=-nm(1)/dm(1);cc=nm(2)/dm(2)
 def mat(d):return matrix([a,b,cc,d])
 def f(d):return L46(mat(d),w,1)/w
 D=f(R(0));A=f(R(1))-D
 require_fraction(c,'D',D);require_fraction(c,'A',A);require(f(R(2))==D+2*A,'B15 affine t3')
 base=[X.n]+[h.n for j in ([0,1,2] if is_b1 else [1,2]) for h in [nm(j),dm(j)]]
 fractions_supported(c,['A','D'],base);bez(c,'A_D_bezout',numerator(c,'A'),numerator(c,'D'))
 d=-D/A;require_fraction(c,'t3',d);guards=base+[numerator(c,'A')];m=mat(d)
 for j in ([1,2,5] if is_b1 else [2,5]):require(B(m,w)[j]==0,'B15 zero pivot '+str(j))
 q=L46(m,w,2);require_fraction(c,'q_fraction',q);monic_match(c,'Q',q)
 for r in [1,2]:require(res(m,w,r,4,6)==B(m,w)[6]*L46(m,w,r),'R46 chain quotient '+str(r))
 h=res(m,w,3,1,4) if is_b1 else edge(m,w,2,4,5)
 if not is_b1:require(c['edge_minor']==[2,4],'B5 edge source')
 require_fraction(c,'h_fraction',h);monic_match(c,'H',h)
 fractions_supported(c,['t3','q_fraction','h_fraction'],guards)
 bez(c,'Q_H_bezout',dec(c['Q']),dec(c['H']))
 return {'theorem':'B1=0 excluded' if is_b1 else 'B5=0, B1!=0 excluded','checks':checks,'degrees':[dec(c['Q']).degree(),dec(c['H']).degree()]}

def check_b6_b3():
 c=load('B6_B3_CERTIFICATE.json');w=X;b=nm(1)/dm(1);cc=-nm(2)/dm(2);d=-nm(3)/dm(3)
 def mat(a):return matrix([a,b,cc,d])
 def f(a):return -chain(mat(a),w,3,5,1,7)
 D=f(R(0));A=f(R(1))-D
 require_fraction(c,'D',D);require_fraction(c,'A',A);require(f(R(2))==D+2*A,'B6B3 affine t0')
 base=[X.n]+[h.n for j in [1,2,3] for h in [nm(j),dm(j)]]
 fractions_supported(c,['A','D'],base);bez(c,'A_D_bezout',numerator(c,'A'),numerator(c,'D'))
 a=-D/A;require_fraction(c,'t0',a);guards=base+[numerator(c,'A')];m=mat(a)
 for j in [3,4,6]:require(B(m,w)[j]==0,'B6B3 zero pivot '+str(j))
 require(res(m,w,3,1,5)==-B(m,w)[1]*chain(m,w,3,5,1,7),'R315 quotient')
 q=chain(m,w,4,2,5,1);h=chain(m,w,7,2,5,1)
 for r in [4,7]:require(res(m,w,r,2,5)==B(m,w)[5]*chain(m,w,r,2,5,1),'R25 quotient '+str(r))
 require_fraction(c,'q_fraction',q);require_fraction(c,'h_fraction',h);monic_match(c,'Q',q);monic_match(c,'H',h)
 fractions_supported(c,['t0','q_fraction','h_fraction'],guards);bez(c,'Q_H_bezout',dec(c['Q']),dec(c['H']))
 return {'theorem':'B6=B3=0 excluded','checks':checks,'degrees':[dec(c['Q']).degree(),dec(c['H']).degree()]}

def check_b6_zeroedge():
 c=load('B6_ZEROEDGE_CERTIFICATE.json');w=X;cc=-nm(2)/dm(2);d=-nm(3)/dm(3)
 def mat(a,b):return matrix([a,b,cc,d])
 D1=edge(mat(R(0),R(0)),w,1,2,6);A1=edge(mat(R(0),R(1)),w,1,2,6)-D1
 require_fraction(c,'D1',D1);require_fraction(c,'A1',A1)
 require(edge(mat(R(0),R(2)),w,1,2,6)==D1+2*A1,'B6zeroedge affine t1')
 base=[X.n]+[h.n for j in [2,3] for h in [nm(j),dm(j)]]
 fractions_supported(c,['A1','D1'],base);bez(c,'A1_D1_bezout',numerator(c,'A1'),numerator(c,'D1'),X.n)
 b=-D1/A1;require_fraction(c,'t1',b);guards=base+[numerator(c,'A1')]
 D0=edge(mat(R(0),b),w,2,5,6);A0=edge(mat(R(1),b),w,2,5,6)-D0
 require_fraction(c,'D0',D0);require_fraction(c,'A0',A0)
 require(edge(mat(R(2),b),w,2,5,6)==D0+2*A0,'B6zeroedge affine t0')
 fractions_supported(c,['t1','A0','D0'],guards);bez(c,'A0_D0_bezout',numerator(c,'A0'),numerator(c,'D0'))
 a=-D0/A0;require_fraction(c,'t0',a);guards.append(numerator(c,'A0'));fractions_supported(c,['t0'],guards);m=mat(a,b)
 for j in [4,6]:require(B(m,w)[j]==0,'B6zeroedge zero pivot '+str(j))
 require([e['name'] for e in c['equations']]==['E41','E42'],'B6zeroedge final sources')
 pol=[]
 for entry,r,j in zip(c['equations'],[4,4],[1,2]):
  h=edge(m,w,r,j,6);require(rat(entry['fraction'])==h,entry['name']+' source')
  supported(dec(entry['fraction']['denom']),guards,entry['name']);pol.append(dec(entry['fraction']['numer']))
 bez(c,'final_bezout',*pol)
 return {'theorem':'B6=0, v6=0 excluded','checks':checks,'degrees':[p.degree() for p in pol]}

# Manufactured exact non-Fourier controls, independent of the elimination builders.
def dense_controls():
 n=8
 def ident():return [[Q(i==j) for j in range(n)] for i in range(n)]
 def mul(A,B):return [[sum(A[i][k]*B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
 def inverse(A):
  m=[r.copy()+e for r,e in zip(A,ident())]
  for k in range(n):
   p=next(i for i in range(k,n) if m[i][k]);m[k],m[p]=m[p],m[k]
   d=m[k][k];m[k]=[v/d for v in m[k]]
   for i in range(n):
    if i!=k:
     d=m[i][k];m[i]=[a-d*b for a,b in zip(m[i],m[k])]
  return [r[n:] for r in m]
 records=[]
 for mode in ['u0_zero','v5_v6_zero','all_edges_zero']:
  u=[Q(i+1,17) for i in range(n)];v=[Q(i+2,19) for i in range(n)]
  if mode=='u0_zero':u[0]=Q(0)
  elif mode=='v5_v6_zero':v[5]=v[6]=Q(0)
  else:u=[Q(0)]*n;v=[Q(0)]*n
  U=ident();V=ident();x=[Q(i+2,i+3) for i in range(n)];y=[Q(2*i+1,i+5) for i in range(n)]
  for j in range(n):U[(j+1)%n][j]+=u[(j+1)%n];V[SIG[j]][j]+=v[j]
  UI=inverse(U);VI=inverse(V)
  require(mul(U,UI)==ident() and mul(V,VI)==ident(),'manufactured invertibility '+mode)
  M=[[UI[i][j]*x[j]+y[i]*VI[i][j] for j in range(n)] for i in range(n)]
  A=mul(U,M);L=mul(A,V);expected=[[U[i][j]*y[j]+x[i]*V[i][j] for j in range(n)] for i in range(n)]
  require(L==expected,'manufactured complete matrix identity '+mode)
  def minors(mat):
   BB=[mat[0][j]+u[0]*mat[7][j] for j in range(n)];found=[]
   for j in [1,2,4,5,6]:
    for r in range(1,n):
     if r not in {j,(j+1)%n,SIG[j]}:
      b=BB[SIG[j]]*mat[r][j]-BB[j]*mat[r][SIG[j]]
      c=BB[SIG[j]]*mat[r-1][j]-BB[j]*mat[r-1][SIG[j]]
      found.append(b+u[r]*c)
   return found
  require(not any(minors(M)),'manufactured necessary minors '+mode)
  for r,j,col in [(2,4,5),(1,2,6),(2,5,6),(4,1,6),(4,2,6)]:
   if v[col]==0:
    BB=[M[0][j]+u[0]*M[7][j] for j in range(n)]
    b=BB[SIG[j]]*M[r][j]-BB[j]*M[r][SIG[j]]
    c=BB[SIG[j]]*M[r-1][j]-BB[j]*M[r-1][SIG[j]]
    require(b*M[r-1][col]-c*M[r][col]==0,'manufactured zeroedge eliminant '+mode)
  if mode!='all_edges_zero':
   found=False
   for rr in range(n):
    for jj in range(n):
     bad=[r.copy() for r in M];bad[rr][jj]+=Q(1,97)
     if any(minors(bad)):
      found=True;break
    if found:break
   require(found,'manufactured perturbation rejected '+mode)
  records.append({'kind':mode,'legal_nonfourier_control':True,'complete_identity':True,'minor_checks':True})
 return records

# Independent arithmetic and negative controls.
def controls():
 require(Z**4==-1,'cyclotomic defining relation');require(Z**8==1,'eighth root')
 for c in [C([1,2,3,4]),C([Q(1,3),0,Q(-2,5),7]),Z]:require(c*C(inv(c.a))==1,'field inverse control')
 p=P({0:C([1,1]),2:C([0,1,0,1]),3:1});q=P({0:2,1:1})
 require((p*q).exquo(q)==p,'polynomial division control');require(R(p*q,q)==R(p),'fraction cancellation control')
 c=load('WZERO_CERTIFICATE.json');b=c['Q_H_bezout'];a=dec(b['left']);h=dec(b['right']);S=dec(b['s']);T=dec(b['t'])
 require((S+1)*a+T*h!=1,'perturbed Bezout negative control')
 # Source index legality for all ordinary minors and resultants used.
 for r,j in [(1,2),(1,4),(1,6),(2,4),(2,5),(2,6),(3,1),(3,4),(3,5),(4,1),(4,2),(4,5),(7,2),(7,5)]:
  require(r not in {j,(j+1)%8,SIG[j]},'off-support source index')
  require(0 not in {j,(j+1)%8,SIG[j]},'row-zero source pivot')
 for r,col in [(2,5),(1,6),(2,6),(4,6)]:require(r not in {col,(col+1)%8,SIG[col]},'zeroedge source index')
 return 'PASS'
if __name__=='__main__':
 start=time.time();out={'independent_arithmetic':'standard-library rational arithmetic, abstract quartic field','controls':controls(),'manufactured_controls':dense_controls(),'results':[]}
 for f in [check_wzero,lambda:check_b15(True),lambda:check_b15(False),check_b6_b3,check_b6_zeroedge]:
  r=f();out['results'].append(r);print('PASS',r,flush=True)
 out.update({'checks':checks,'elapsed_seconds':time.time()-start,'verdict':'PASS'})
 import argparse
 parser=argparse.ArgumentParser();parser.add_argument('--output');args=parser.parse_args()
 if args.output:Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out),flush=True)
