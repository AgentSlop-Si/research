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

def run(N,p):
 assert (p-1)%N==0
 q=pow(int(primitive_root(p)),(p-1)//N,p);assert all(pow(q,j,p)!=1 for j in range(1,N))
 invN=pow(N,-1,p);kap=pow(4,-1,N);m=N-4;d=N-3
 cache={}
 def G(e,dd,a,b):
  r=e*a%N;l=dd*b%N
  if r+l>N-1:return 0
  z=pow(q,(e*dd)%N,p)
  key=(z,r+l,l)
  if key not in cache:
   # Independent Pascal recurrence for the Gaussian coefficient.
   rows=[[1]]
   for n in range(1,r+l+1):
    row=[1]*(n+1)
    for k in range(1,n):row[k]=(rows[-1][k-1]+pow(z,k,p)*rows[-1][k])%p
    rows.append(row)
   cache[key]=rows[-1][l]
  return cache[key]
 def f(a,b):return pow(q,kap*(a+b)**2%N,p)
 H=q*pow(1+q,-1,p)%p
 s=[(f(a,1)*pow(H,-1,p)-G(-1,1,a,1))*pow(G(1,1,a,1),-1,p)%p for a in range(1,N-1)]
 assert s[0]==1 and s[2]==q
 y=list(range(2,m+2));P=[1]
 for v in y:P=poly_mul(P,[-v%p,1],p)
 D=sum(P[k]*s[k] for k in range(m+1))%p
 U=sum(P[k]*s[k+1] for k in range(m+1))%p
 if D==0:return None
 x=U*pow(D,-1,p)%p
 if x==0 or x in y:return None
 nodes=y+[x]
 banks=[(1,1,v) for v in nodes]+[(-1,1,1),(1,-1,1)]+[(-1,-1,v) for v in nodes]
 count=len(banks);assert count==2*N-4
 # Selected axis columns: m fixed forward nodes, negative-epsilon singleton,
 # and first three fixed negative-negative nodes. Their matrix is literal.
 selected=list(range(m))+[d]+list(range(d+2,d+5))
 axis=[[pow(banks[i][2],banks[i][0]*a%N,p) for i in selected] for a in range(N)]
 try: axis_amp,axis_det=solve(axis,[f(a,0) for a in range(N)],p)
 except ZeroDivisionError:return None
 h=[[0]*N for _ in banks]
 for i,v in zip(selected,axis_amp):h[i][0]=v
 # First edge: d nodes, d+1 moments, with exactly one imposed recurrence.
 amps,vd=solve([[pow(v,r,p) for v in nodes] for r in range(d)],s[:d],p)
 assert sum(amps[i]*pow(nodes[i],d,p) for i in range(d))%p==s[d]
 for i,v in enumerate(nodes):h[i][1]=H*amps[i]*pow(v,-1,p)%p
 h[d][1]=H
 h[d+1][-1]=(f(0,1)-H-sum(h[i][1] for i in range(d)))%p
 # Positive interior rows: solely consecutive nonaxis forward moments, then
 # backward moments including zero for the remaining axis coefficient.
 for b in range(2,(N-1)//2+1):
  single=f(N-b,b)*pow(G(-1,1,N-b,b),-1,p)%p
  h[d][b]=single
  k=N-b-1
  residual=[(f(a,b)-single*G(-1,1,a,b))*pow(G(1,1,a,b),-1,p)%p for a in range(1,k+1)]
  plus,_=solve([[pow(v,a,p) for v in nodes[:k]] for a in range(1,k+1)],residual,p)
  for i,v in enumerate(plus):h[i][b]=v
  minus_mom=[(f(0,b)-single-sum(plus))%p]
  for r in range(1,b):
   a=N-r
   minus_mom.append((f(a,b)-single*G(-1,1,a,b))*pow(G(-1,-1,a,b),-1,p)%p)
  minus,_=solve([[pow(v,r,p) for v in nodes[:b]] for r in range(b)],minus_mom,p)
  for i,v in enumerate(minus):h[d+2+i][-b%N]=v
 # Reflection swaps all orientation roles and retains nodes and amplitudes.
 swap=list(range(d+2,2*d+2))+[d+1,d]+list(range(d))
 for b in range(1,(N-1)//2+1):
  for i,(e,dd,v) in enumerate(banks):
   j=swap[i];ee,ddd,vv=banks[j]
   assert (ee,ddd,vv)==(-e,-dd,v)
   h[j][ddd*(N-b)%N]=h[i][dd*b%N]
 # All normalized Weyl coefficients and guard nonvanishing.
 residuals=[]
 for a in range(N):
  for b in range(N):
   acc=sum(h[i][dd*b%N]*pow(v,e*a%N,p)*G(e,dd,a,b) for i,(e,dd,v) in enumerate(banks))%p
   if acc!=f(a,b):residuals.append([a,b,acc,f(a,b)])
 assert residuals==[]
 C=sum(pow(q,-t*t%N,p) for t in range(N))*invN%p;assert C
 out=[[0]*N for _ in range(N)];branches=0;nonzero_weights=0
 weights=[]
 for i,(e,dd,v) in enumerate(banks):
  delta=-pow(v,N,p)%p;assert delta
  row=[]
  for j in range(N):
   w=C*delta*sum(h[i][ell]*pow(q,(-e*dd*j*ell)%N,p) for ell in range(N))%p
   row.append(w);nonzero_weights+=bool(w)
   A=[[int(a==b) for b in range(N)] for a in range(N)]
   for col in range(N):
    A[(col+e)%N][col]=(A[(col+e)%N][col]-v)%p
    A[col][col]=(A[col][col]-pow(q,(e*dd*j+dd*col)%N,p))%p
   B=inverse(A,p);branches+=1
   for a in range(N):
    for b in range(N):out[a][b]=(out[a][b]+invN*w*B[a][b])%p
  weights.append(row)
 assert all(out[a][b]==pow(q,-a*b%N,p) for a in range(N) for b in range(N))
 return dict(N=N,p=p,q=q,m=m,d=d,fixed_nodes=y,last_node=x,D=D,U=U,axis_selected_columns=selected,axis_determinant=axis_det,vandermonde_determinant=vd,edge_moments=s,bank_count=count,raw_weights=weights,normalized_sector_amplitudes=h,inverse_branches_two_sided_verified=branches,nonzero_raw_weights=nonzero_weights,original_Fourier_entries_verified=N*N,status='PASS')

results=[]
for N in [7,9,11,13,15]:
 p=4*N
 while True:
  p=int(nextprime(p))
  if (p-1)%N:continue
  result=run(N,p)
  if result is not None:break
 results.append(result)
 print(json.dumps({k:result[k] for k in ['N','p','q','bank_count','inverse_branches_two_sided_verified','original_Fourier_entries_verified','status']}),flush=True)
(OUT/'INDEPENDENT_LITERAL_CONTROL_RESULTS.json').write_text(json.dumps({'status':'PASS','scope':'Finite-field controls complement a characteristic-zero proof; not a lifting argument.','results':results},indent=2)+'\n')
