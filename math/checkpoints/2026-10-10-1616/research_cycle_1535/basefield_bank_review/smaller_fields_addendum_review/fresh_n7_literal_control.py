"""Independent controls for rational split-node all-order construction.
No author/source program imports, execution, compilation, or parsing.
"""
from pathlib import Path
import json
from sympy import nextprime, primitive_root
OUT=Path(__file__).resolve().parent

def poly_mul(a,b,p):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b): c[i+j]=(c[i+j]+x*y)%p
 return c

def solve(A,b,p):
 n=len(A); assert all(len(row)==n for row in A)
 M=[[x%p for x in row]+[v%p] for row,v in zip(A,b)]
 determinant=1
 for j in range(n):
  k=next((k for k in range(j,n) if M[k][j]),None)
  if k is None: raise ZeroDivisionError('singular')
  if k!=j:M[k],M[j]=M[j],M[k];determinant=-determinant
  pivot=M[j][j];determinant=determinant*pivot%p
  inv=pow(pivot,-1,p);M[j]=[v*inv%p for v in M[j]]
  for k in range(n):
   if k!=j:
    v=M[k][j];M[k]=[(a-v*b)%p for a,b in zip(M[k],M[j])]
 return [row[-1] for row in M],determinant%p

def inverse(A,p):
 n=len(A);M=[[v%p for v in A[i]]+[int(i==j) for j in range(n)] for i in range(n)]
 for j in range(n):
  k=next(k for k in range(j,n) if M[k][j]);M[k],M[j]=M[j],M[k]
  inv=pow(M[j][j],-1,p);M[j]=[v*inv%p for v in M[j]]
  for k in range(n):
   if k!=j:
    v=M[k][j];M[k]=[(a-v*b)%p for a,b in zip(M[k],M[j])]
 B=[r[n:] for r in M]
 assert all(sum(A[i][k]*B[k][j] for k in range(n))%p==int(i==j) for i in range(n) for j in range(n))
 assert all(sum(B[i][k]*A[k][j] for k in range(n))%p==int(i==j) for i in range(n) for j in range(n))
 return B

N=7;p=43;q=4;d=3;kap=2
nodes=[4,18,3];g=[42,9,18,1]
assert all(sum(c*pow(x,j,p) for j,c in enumerate(g))%p==0 for x in nodes)
def G(e,dd,a,b):
 r=e*a%N;ell=dd*b%N
 if r+ell>N-1:return 0
 z=pow(q,e*dd%N,p);out=1
 for j in range(1,ell+1):out=out*(1-pow(z,r+j,p))*pow(1-pow(z,j,p),-1,p)%p
 return out
pr=[[int(i==j) for j in range(d)] for i in range(d)]
for r in range(d,N):pr.append([-sum(g[k]*pr[r-d+k][j] for k in range(d))%p for j in range(d)])
def Mrow(b):
 return [[*(G(1,1,a,b)*v%p for v in pr[a]),G(-1,1,a,b),G(1,-1,a,b),*(G(-1,-1,a,b)*v%p for v in pr[-a%N])] for a in range(N)]
def f(a,b):return pow(q,kap*(a+b)**2%N,p)
selected={0:[0,1,2,3,5,6,7],2:[0,1,2,3,4,5,6],3:[0,1,2,3,4,6,7]}
Z={};minors={}
for b,I in selected.items():
 M=Mrow(b);v,det=solve([[r[j] for j in I] for r in M],[f(a,b) for a in range(N)],p)
 z=[0]*8
 for i,w in zip(I,v):z[i]=w
 Z[b]=z;minors[b]=det
assert minors=={0:27,2:19,3:3}
H=q*pow(1+q,-1,p)%p
s=[(f(a,1)*pow(H,-1,p)-G(-1,1,a,1))*pow(G(1,1,a,1),-1,p)%p for a in range(1,6)]
a,_=solve([[pow(x,r,p) for x in nodes] for r in range(1,4)],[H*s[r-1]%p for r in range(1,4)],p)
assert all(sum(a[i]*pow(nodes[i],r,p) for i in range(3))%p==H*s[r-1]%p for r in [4,5])
K=[sum(a[i]*pow(nodes[i],r,p) for i in range(3))%p for r in range(3)]
Z[1]=K+[H,(f(0,1)-H-K[0])%p,0,0,0]
for b in [1,2,3]:
 z=Z[b];Z[N-b]=z[5:8]+[z[4],z[3]]+z[:3]
assert all(sum(Mrow(b)[a][j]*Z[b][j] for j in range(8))%p==f(a,b) for b in range(N) for a in range(N))
banks=[(1,1,x) for x in nodes]+[(-1,1,1),(1,-1,1)]+[(-1,-1,x) for x in nodes]
h=[[0]*N for _ in banks]
V=[[pow(x,r,p) for x in nodes] for r in range(3)]
for b in range(N):
 plus,_=solve(V,Z[b][:3],p);minus,_=solve(V,Z[b][5:],p)
 for i,v in enumerate(plus):h[i][b]=v
 h[3][b]=Z[b][3];h[4][-b%N]=Z[b][4]
 for i,v in enumerate(minus):h[5+i][-b%N]=v
C=sum(pow(q,-t*t%N,p) for t in range(N))*pow(N,-1,p)%p
out=[[0]*N for _ in range(N)];weights=[];branches=0
for i,(e,dd,x) in enumerate(banks):
 delta=-pow(x,N,p)%p;row=[]
 for j in range(N):
  w=C*delta*sum(h[i][ell]*pow(q,-e*dd*j*ell%N,p) for ell in range(N))%p;row.append(w)
  A=[[int(a==b) for b in range(N)] for a in range(N)]
  for col in range(N):
   A[(col+e)%N][col]=(A[(col+e)%N][col]-x)%p
   A[col][col]=(A[col][col]-pow(q,(e*dd*j+dd*col)%N,p))%p
  inv=inverse(A,p);branches+=1
  for a in range(N):
   for b in range(N):out[a][b]=(out[a][b]+pow(N,-1,p)*w*inv[a][b])%p
 weights.append(row)
assert all(out[a][b]==pow(q,-a*b%N,p) for a in range(N) for b in range(N))
Aq=(22*22-4*11)%43
assert Aq==10 and (4*4+22*4+11)%43==29
A16=sum(v*pow(16,j,43) for j,v in enumerate([-31,-5,5,20,-1,-18]))*pow(29,-1,43)%43
B16=sum(v*pow(16,j,43) for j,v in enumerate([-9,-37,-21,3,10,6]))*pow(29,-1,43)%43
assert (A16*A16-4*B16)%43==12 and pow(12,21,43)==42
result={'status':'PASS','field':'F43','q':4,'actual_reduced_roots':nodes,'cubic_ascending':g,'quadratic_ascending':[11,22,1],'quadratic_discriminant':10,'quadratic_at_q':29,'selected_row_minor_residues':minors,'all_49_row_equations':True,'two_sided_inverse_branches':branches,'original_Fourier_entries':49,'raw_weights':weights,'separate_q16_discriminant':12,'separate_discriminant_Euler':42}
OUT=Path(__file__).resolve().parent
(OUT/'N7_INDEPENDENT_LITERAL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='raw_weights'},indent=2))
