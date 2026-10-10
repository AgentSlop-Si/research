#!/usr/bin/env python3
"""Fresh Phase37 reconstruction; reads certificates only as inert JSON data."""
import json,math,random,sys
from pathlib import Path
P=998244353;RNG=random.Random(370101)
def trim(a):
 a=[x%P for x in a]
 while len(a)>1 and a[-1]==0:a.pop()
 return a

def add(a,b):return trim([(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))])
def sub(a,b):return add(a,[-x for x in b])
def mul(a,b):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]=(c[i+j]+x*y)%P
 return trim(c)
def power(a,k):
 b=[1]
 while k:
  if k&1:b=mul(b,a)
  a=mul(a,a);k//=2
 return b

def div(a,b):
 a=trim(a);b=trim(b);assert b!=[0]
 while len(a)>=len(b) and a!=[0]:
  k=len(a)-len(b);c=a[-1]*pow(b[-1],-1,P)%P
  for j,x in enumerate(b):a[j+k]=(a[j+k]-c*x)%P
  a=trim(a)
 return a

def gcd(a,b):
 while b!=[0]:a,b=b,div(a,b)
 return trim([x*pow(a[-1],-1,P) for x in a])
def evaluate(a,z):
 x=0
 for c in reversed(a):x=(x*z+c)%P
 return x

def kernel(order,alpha):
 N=len(order);pos=[0]*N
 for i,j in enumerate(order):pos[j]=i
 guard=(1-pow(alpha,N,P))%P;assert guard
 powers=[pow(alpha,k,P)*pow(guard,-1,P)%P for k in range(N)]
 return [[powers[(pos[i]-pos[j])%N] for j in range(N)] for i in range(N)]
def mv(A,x):return [sum(a*b for a,b in zip(r,x))%P for r in A]
def mm(A,B):return [[sum(a*b for a,b in zip(r,c))%P for c in zip(*B)] for r in A]
def scan(order,alpha,x):
 last=0
 for i in order:last=(alpha*last+x[i])%P
 last=last*pow((1-pow(alpha,len(order),P))%P,-1,P)%P;out=[0]*len(x)
 for i in order:last=(alpha*last+x[i])%P;out[i]=last
 return out

def pencil(orders,I):
 N=len(orders);n=len(orders[0]);params=[(1,1,4),(2,1,7),(1,2,8),(1,-1,5),(2,1,9),(1,1,6)];aa=[(a+b*I)*pow(d,-1,P)%P for a,b,d in params];G=[kernel(o,a) for o,a in zip(orders,aa)];wa=(1+I)*pow(3,-1,P)%P;wc=(1-I)*pow(4,-1,P)%P;A=[[(G[0][i][j]+wa*G[1][i][j])%P for j in range(n)] for i in range(n)];C=[[(G[4][i][j]+wc*G[5][i][j])%P for j in range(n)] for i in range(n)];D1=[pow(I,3*j+1,P) for j in range(n)];D2=[pow(I,j*j+j+1,P) for j in range(n)];M0=[[0]*3 for _ in range(n)];M1=[[0]*3 for _ in range(n)]
 for col in range(3):
  v=[C[j][col]*D2[j]%P for j in range(n)]
  for mid,out in [(2,M0),(3,M1)]:
   y=mv(G[mid],v);y=[a*b%P for a,b in zip(D1,y)];y=mv(A,y)
   for j in range(n):out[j][col]=y[j]
 # Own one-pass recurrence for every branch, independently compared to dense kernels.
 for o,a,g in zip(orders,aa,G):
  x=[RNG.randrange(P) for i in range(n)];assert scan(o,a,x)==mv(g,x)
 return M0,M1,aa

def plaquette(M0,M1,n,j):
 e=lambda i,k:[M0[i][k],M1[i][k]]
 return sub(power(mul(e(0,0),e(1,j)),n),power(mul(e(0,j),e(1,0)),n))
def rank2(rows):
 basis={}
 for a in rows:
  while a:
   k=a.bit_length()-1
   if k in basis:a^=basis[k]
   else:basis[k]=a;break
 return len(basis)
def parity(A,a,b):
 n=len(A);rows=[]
 for i in range(n):
  if i==a:continue
  bits=0;k=0
  for j in range(n):
   if j==b:continue
   den=A[i][b]*A[a][j]%P;assert den
   r=A[i][j]*A[a][b]*pow(den,-1,P)%P;assert pow(r,n,P)==1;bit=pow(r,n//2,P);assert bit in [1,P-1]
   if bit==P-1:bits|=1<<k
   k+=1
  rows.append(bits)
 return rank2(rows)
def bareiss(a):
 a=[r[:] for r in a];n=len(a);old=1;sign=1
 for k in range(n-1):
  if a[k][k]==0:
   q=next((q for q in range(k+1,n) if a[q][k]),None)
   if q is None:return 0
   a[k],a[q]=a[q],a[k];sign=-sign
  pivot=a[k][k]
  for i in range(k+1,n):
   for j in range(k+1,n):
    num=a[i][j]*pivot-a[i][k]*a[k][j];assert num%old==0;a[i][j]=num//old
   a[i][k]=0
  old=pivot
 return sign*a[-1][-1]
def main():
 global P
 out={'status':'PASS','uploaded_or_constructor_code_executed':False};certs=[];cyclemap={};coeffs=0
 for f in sorted((Path(__file__).with_name('source')).glob('bezout_N*_p*.json')):
  d=json.loads(f.read_text());n=d['N'];P=d['prime'];assert all(P%a for a in range(2,math.isqrt(P)+1));gen=3 if P==998244353 else 31;I=pow(gen,(P-1)//4,P);assert I*I%P==P-1;orders=d['cycle_orders'];assert len(orders)==6 and len(set(map(tuple,orders)))==6
  for order in orders:assert sorted(order)==list(range(n)) and order[0]==0
  if n in cyclemap:assert cyclemap[n]==orders
  else:cyclemap[n]=orders
  M0,M1,alphas=pencil(orders,I);polys=[plaquette(M0,M1,n,j) for j in [1,2]];assert polys==d['polynomials_coefficients_mod_prime'];assert all(len(f)==2*n+1 and f[-1] for f in polys);assert [f[-1] for f in polys]==d['leading_coefficients_mod_prime'];assert gcd(*polys)==[1]
  u,v=d['bezout_coefficients_mod_prime'];assert add(mul(u,polys[0]),mul(v,polys[1]))==[1];coeffs+=sum(map(len,polys));certs.append({'N':n,'prime':P,'degree':2*n,'alpha_denominators_nonzero':True,'polynomial_gcd':1,'source_Bezout_identity':True})
 assert len(certs)==12;out['exact_pencil_certificates']=certs;out['independently_rebuilt_polynomial_coefficients']=coeffs;out['branch_scan_controls']=72
 # Check serialized cycles against an independently repeated public seeded algorithm.
 affinecounts={}
 for n,orders in cyclemap.items():
  rng=random.Random(37037+n);generated=[]
  while len(generated)<6:
   rest=list(range(1,n));rng.shuffle(rest);order=[0]+rest
   if order not in generated:generated.append(order)
  assert orders==generated;count=0
  for order in orders:
   pi=[0]*n
   for i,j in zip(order,order[1:]+order[:1]):pi[i]=j
   a=(pi[1]-pi[0])%n;b=pi[0];count+=all(pi[i]==(a*i+b)%n for i in range(n))
  assert count==(2 if n==4 else 0);affinecounts[n]=count
 out['affine_cycle_counts']=affinecounts
 # Every anchor at small sizes, exact integer determinant +/-1.
 determinants=0
 for n in [2,4,8,16]:
  for a in range(n):
   for b in range(n):
    E=[[int(i<j)-int(i<b)-int(a<j)+int(a<b) for j in range(n) if j!=b] for i in range(n) if i!=a];assert abs(bareiss(E))==1;determinants+=1
 out['integer_lattice_anchor_determinants']=determinants
 # Arbitrary endpoint gauges/permutations: root-membership and parity are exact.
 P=998244353;curvature=[]
 for n in [4,8,16,32,64,128]:
  alpha=pow(3,(P-1)//(n*n),P);assert pow(alpha,n*n,P)==1 and pow(alpha,n*n//2,P)!=1;order=RNG.sample(range(n),n);G=kernel(order,alpha);w=pow(alpha,n,P);F=[[pow(w,i*j,P) for j in range(n)] for i in range(n)];lp=RNG.sample(range(n),n);rp=RNG.sample(range(n),n);L=[RNG.randrange(1,P) for i in range(n)];RR=[RNG.randrange(1,P) for i in range(n)]
  dressed=lambda A:[[L[i]*A[lp[i]][rp[j]]*RR[j]%P for j in range(n)] for i in range(n)]
  GG=dressed(G);FF=dressed(F)
  for a,b in [(0,0)]+[(RNG.randrange(n),RNG.randrange(n)) for _ in range(4)]:assert parity(GG,a,b)==n-1 and parity(FF,a,b)==1
  curvature.append({'N':n,'anchors':5,'Green_rank':n-1,'Fourier_rank':1})
 out['parity_curvature_controls']=curvature
 # Planted Fourier members retain a common polynomial root.
 planted=0
 for n in [4,8,16]:
  w=pow(3,(P-1)//n,P);star=RNG.randrange(P);B=[[RNG.randrange(P) for j in range(3)] for i in range(n)];A=[[(pow(w,i*j,P)-star*B[i][j])%P for j in range(3)] for i in range(n)];f,g=[plaquette(A,B,n,j) for j in [1,2]];assert evaluate(f,star)==evaluate(g,star)==0 and len(gcd(f,g))>=2;planted+=1
 out['planted_Fourier_pencil_controls']=planted
 path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('INDEPENDENT_RESULTS.json');path.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
