#!/usr/bin/env python3
"""Own reconstruction of finite parameter data; no source code execution."""
from pathlib import Path
import itertools,json,math,random,sys
P=65537
RNG=random.Random(109057)
def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def mm(a,b):return [[sum(x*y for x,y in zip(r,c))%P for c in zip(*b)] for r in a]
def det(a):
 a=[r[:] for r in a];out=1
 for j in range(len(a)):
  k=next((k for k in range(j,len(a)) if a[k][j]%P),None)
  if k is None:return 0
  if k!=j:a[k],a[j]=a[j],a[k];out=-out
  v=a[j][j];out=out*v%P;iv=pow(v,-1,P)
  for i in range(j+1,len(a)):
   c=a[i][j]*iv%P
   for k in range(j,len(a)):a[i][k]=(a[i][k]-c*a[j][k])%P
 return out%P

def inv(a):
 n=len(a);z=[r[:]+eye(n)[i] for i,r in enumerate(a)]
 for j in range(n):
  k=next(k for k in range(j,n) if z[k][j]);z[j],z[k]=z[k],z[j];c=pow(z[j][j],-1,P);z[j]=[x*c%P for x in z[j]]
  for k in range(n):
   if k!=j:
    c=z[k][j]
    if c:z[k]=[(x-c*y)%P for x,y in zip(z[k],z[j])]
 return [r[n:] for r in z]
def rank(a):
 if not a or not a[0]:return 0
 a=[r[:] for r in a];k=0
 for j in range(len(a[0])):
  q=next((q for q in range(k,len(a)) if a[q][j]),None)
  if q is None:continue
  a[k],a[q]=a[q],a[k];c=pow(a[k][j],-1,P);a[k]=[x*c%P for x in a[k]]
  for q in range(k+1,len(a)):
   c=a[q][j]
   if c:a[q]=[(x-c*y)%P for x,y in zip(a[q],a[k])]
  k+=1
  if k==len(a):break
 return k

def rect(a,R,C):return [[a[i][j] for j in C] for i in R]
def diagonal_product(A,d,B):return mm([[x*d[j]%P for j,x in enumerate(row)] for row in A],B)
def pencil(A,B,w,j):
 n=len(A);return [[A[i][k]*(B[k][(j+1)%n]-pow(w,i,P)*B[k][j])%P for k in range(n)] for i in range(n)]
def branch(par):
 pi=par['sigma'];weights=par['weights'];n=len(pi);assert sorted(pi)==list(range(n));seen=[];x=0
 while x not in seen:seen.append(x);x=pi[x]
 assert x==0 and len(seen)==n;rho=math.prod(weights)%P;assert rho!=1 and all(weights)
 # Direct unique cyclic path numerator, independently compared to matrix inversion.
 G=[[0]*n for i in range(n)];den=pow((1-rho)%P,-1,P)
 for i in range(n):
  j=i;v=den
  for _ in range(n):G[i][j]=v;v=v*weights[j]%P;j=pi[j]
 K=eye(n)
 for i,j in enumerate(pi):K[i][j]=(K[i][j]-weights[i])%P
 assert G==inv(K)
 l,r,ld,rd=[par[k] for k in ['row_perm','col_perm','row_scale','col_scale']];assert sorted(l)==sorted(r)==list(range(n)) and all(ld) and all(rd)
 return [[ld[i]*G[l[i]][r[j]]*rd[j]%P for j in range(n)] for i in range(n)]
def main():
 root=Path(__file__).resolve().parent;source=json.loads((root/'source/RESULTS.json').read_text());cert=json.loads((root/'source/CERTIFICATE.json').read_text());rec=source['four_green_witness'];n=8;w=4096;assert pow(w,n,P)==1 and pow(w,n//2,P)==P-1;stages=[]
 for pars in rec['green_parameters']:
  a,b=map(branch,pars);stages.append([[(x+y)%P for x,y in zip(r,s)] for r,s in zip(a,b)])
 A,B=stages;assert A==rec['A'] and B==rec['B'] and det(A) and det(B);M=diagonal_product(A,rec['d'],B);K=pencil(A,B,w,0);assert K==cert['pencil_matrix'];kd=det(K);assert kd==cert['two_column_pencil_det_GF65537']==55687
 # Independent Leibniz determinant, no elimination reuse.
 ld=0
 for perm in itertools.permutations(range(n)):
  inversions=sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n));v=1
  for i,j in enumerate(perm):v=v*K[i][j]%P
  ld=(ld+(-1 if inversions%2 else 1)*v)%P
 assert ld==kd
 counts=[]
 for k in range(1,n+1):
  sets=list(itertools.combinations(range(n),k));count=0
  for rr in sets:
   for cc in sets:assert det(rect(M,rr,cc));count+=1
  counts.append(count)
 assert sum(counts)==12869
 cosets=0
 for dr in [1,2,4,8]:
  for dc in [1,2,4,8]:
   for a in range(dr):
    for b in range(dc):
     rr=list(range(a,n,dr));cc=list(range(b,n,dc));expected=n//math.gcd(n,dr*dc);assert rank(rect(M,rr,cc))>=expected;assert rank([[pow(w,i*j,P) for j in cc] for i in rr])==expected;cosets+=1
 assert cosets==225
 # Capacity dominance is not equality of actual rank profiles.
 rr=[0,4];cc=[0,2];assert rank(rect(M,rr,cc))==2 and rank([[pow(w,i*j,P) for j in cc] for i in rr])==1
 # Exhaustive interface minima for selected rectangles; compare actual product.
 interface=[]
 for k in range(1,9):
  rr=RNG.sample(range(n),k);cc=RNG.sample(range(n),9-k);cost=[]
  for mask in range(1<<n):
   S=[i for i in range(n) if mask>>i&1];Sc=[i for i in range(n) if not(mask>>i&1)];cost.append(rank(rect(A,rr,Sc))+rank(rect(B,S,cc)))
  r=rank(rect(M,rr,cc));assert min(cost)==r;interface.append({'rows':rr,'columns':cc,'minimum':min(cost),'actual_rank':r})
 # Constructed hidden gauges satisfy every column, full intertwining and normalization.
 positive=[]
 for n in [4,8,16]:
  w=pow(3,(P-1)//n,P);F=[[pow(w,i*j,P) for j in range(n)] for i in range(n)]
  while True:
   A=[[RNG.randrange(P) for j in range(n)] for i in range(n)]
   if det(A):break
  d=[RNG.randrange(1,P) for i in range(n)];c=[RNG.randrange(1,P) for i in range(n)];target=[[c[i]*F[i][j]%P for j in range(n)] for i in range(n)];B=mm(inv(A),target);B=[[x*pow(d[i],-1,P)%P for x in r] for i,r in enumerate(B)];assert diagonal_product(A,d,B)==target
  for j in range(n):assert all(sum(x*y for x,y in zip(row,d))%P==0 for row in pencil(A,B,w,j))
  X=[[B[i][(j+1)%n] for j in range(n)] for i in range(n)];X=mm(X,inv(B));Y=mm(inv(A),[[pow(w,i,P)*x%P for x in row] for i,row in enumerate(A)]);assert all(d[i]*X[i][j]%P==Y[i][j]*d[j]%P for i in range(n) for j in range(n));positive.append(n)
 # det K0=0 is insufficient: preserve first two Fourier columns, alter a later entry.
 n=8;w=4096;A=eye(n);B=[[pow(w,i*j,P) for j in range(n)] for i in range(n)];B[0][2]=(B[0][2]+1)%P;assert det(B);K0=pencil(A,B,w,0);K1=pencil(A,B,w,1);assert rank(K0)==0 and K1[0][0]==1 and all(K1[0][j]==0 for j in range(1,n))
 out={'status':'PASS','source_code_executed':False,'reconstructed_Green_branches':4,'pencil_determinant_elimination':kd,'pencil_determinant_Leibniz':ld,'nonzero_square_minors_by_size':counts,'full_spark_minors':sum(counts),'Fourier_coset_capacity_profiles':cosets,'exact_rank_equality_countercontrol':{'rows':rr if False else [0,4],'columns':[0,2],'candidate_rank':2,'Fourier_rank':1},'matroid_minimax_controls':interface,'hidden_gauge_positive_sizes':positive,'K0_singular_insufficient_control':{'K0_rank':0,'K1_forces_d0_zero':True}}
 path=Path(sys.argv[1]) if len(sys.argv)>1 else root/'INDEPENDENT_RESULTS.json';path.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
