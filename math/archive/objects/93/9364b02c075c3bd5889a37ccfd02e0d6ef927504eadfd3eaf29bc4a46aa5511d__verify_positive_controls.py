"""New standard-library dense exact controls, unrelated to Fourier solvability."""
from fractions import Fraction as F
import json,os
N=8;sig=[2,7,5,0,6,1,3,4];pivot=[3,0,0,1,0,0,0,1]
def eye():return [[F(i==j)for j in range(N)]for i in range(N)]
def mul(A,B):return [[sum(A[i][k]*B[k][j]for k in range(N))for j in range(N)]for i in range(N)]
def inv(A):
 T=[list(r)+e for r,e in zip(A,eye())]
 for j in range(N):
  p=next(i for i in range(j,N)if T[i][j]);T[j],T[p]=T[p],T[j];d=T[j][j];T[j]=[x/d for x in T[j]]
  for i in range(N):
   if i!=j:
    d=T[i][j];T[i]=[a-d*b for a,b in zip(T[i],T[j])]
 return [r[N:]for r in T]
def add(A,B):return [[A[i][j]+B[i][j]for j in range(N)]for i in range(N)]
report=[]
for q in range(1,5):
 u=[F(1,q+i+2)for i in range(N)];v=[F(1,2*q+3*i+3)for i in range(N)];x=[F(1,q+2*i+3)for i in range(N)];y=[F(1,q+3*i+5)for i in range(N)]
 U=eye();V=eye()
 for j in range(N):U[(j+1)%N][j]=u[(j+1)%N];V[sig[j]][j]=v[j]
 Q0=[[U[i][j]/x[i]for j in range(N)]for i in range(N)];Q1=[[V[i][j]/y[j]for j in range(N)]for i in range(N)];M=add(inv(Q0),inv(Q1));A=mul(U,M);L=mul(A,V)
 rhs=[[U[i][j]*y[j]+x[i]*V[i][j]for j in range(N)]for i in range(N)];assert L==rhs
 a=[A[pivot[j]][j]for j in range(N)];c=[A[pivot[j]][sig[j]]for j in range(N)];assert all(a)and all(c)
 h=[[c[j]*A[i][j]-a[j]*A[i][sig[j]]for j in range(N)]for i in range(N)]
 for j in range(N):
  assert -a[j]/c[j]==v[j]
  for i in range(N):
   if i not in [j,(j+1)%N,sig[j]]:assert h[i][j]==0
  assert h[(j+1)%N][j]/(c[j]*u[(j+1)%N])==y[j]
  i=sig[j];assert -h[i][j]/a[j]==x[i]
 for i in range(N):
  l=sig.index(i);n=(i+1)%N
  assert u[n]*a[l]*h[i][i]+c[i]*u[n]*h[i][l]-a[l]*h[n][i]==0
 bad=[r[:]for r in M];bad[0][0]+=1;assert mul(mul(U,bad),V)!=rhs
 report.append({'control':q,'status':'all guards, 40 equations, scale/direction reconstruction and dense matrix identity verified; perturbed matrix rejected'})
print('PASS: four exact all-edge paired-Green positive controls and four perturbed negative controls.')
json.dump({'not_fourier_candidates':True,'controls':report},open(os.path.join(os.path.dirname(__file__),'POSITIVE_CONTROLS.json'),'w'),indent=2)
