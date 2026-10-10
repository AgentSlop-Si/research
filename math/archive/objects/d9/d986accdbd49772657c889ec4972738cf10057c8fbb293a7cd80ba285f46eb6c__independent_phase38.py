#!/usr/bin/env python3
"""Reviewer reconstruction of all Phase38 inputs and polynomial gates; source code inert."""
from pathlib import Path
import random,json,subprocess,sys,tempfile
R=random.Random(3800)
def mm(A,B,p):return [[sum(x*y for x,y in zip(r,c))%p for c in zip(*B)] for r in A]
def inv(A,p):
 n=len(A);X=[r[:]+[int(i==j) for j in range(n)] for i,r in enumerate(A)]
 for j in range(n):
  k=next(k for k in range(j,n) if X[k][j]);X[k],X[j]=X[j],X[k];s=pow(X[j][j],-1,p);X[j]=[x*s%p for x in X[j]];r=X[j]
  for k in range(n):
   if k!=j:
    s=X[k][j]
    if s:X[k]=[(x-s*y)%p for x,y in zip(X[k],r)]
 return [r[n:] for r in X]
def orders(n):
 rng=random.Random(37037+n);out=[]
 while len(out)<6:
  v=list(range(1,n));rng.shuffle(v);v=[0]+v
  if v not in out:out.append(v)
 return out
def kernels(n,p):
 root=pow(3 if p==998244353 else 31,(p-1)//n,p);ii=pow(root,n//4,p)
 alpha=[(a+b*ii)*pow(d,-1,p)%p for a,b,d in [(1,1,4),(2,1,7),(1,2,8),(1,-1,5),(2,1,9),(1,1,6)]];Gs=[]
 for order,a in zip(orders(n),alpha):
  pos={x:k for k,x in enumerate(order)};guard=(1-pow(a,n,p))%p;assert guard;powers=[pow(a,k,p)*pow(guard,-1,p)%p for k in range(n)]
  Gs.append([[powers[(pos[i]-pos[j])%n] for j in range(n)] for i in range(n)])
 wa=(1+ii)*pow(3,-1,p)%p;wc=(1-ii)*pow(4,-1,p)%p
 A=[[(Gs[0][i][j]+wa*Gs[1][i][j])%p for j in range(n)] for i in range(n)]
 C=[[(Gs[4][i][j]+wc*Gs[5][i][j])%p for j in range(n)] for i in range(n)]
 F=[[pow(root,i*j,p) for j in range(n)] for i in range(n)]
 return A,C,F,Gs[2],Gs[3]
def mulpoly(a,b,p):return [sum(a[i]*b[k-i] for i in range(len(a)) if 0<=k-i<len(b))%p for k in range(len(a)+len(b)-1)]
def gate(T,A,B,indices,p):
 r,s,c,d,e=indices;out=[]
 for j,h in [(1,d),(2,e)]:
  a=mulpoly([A[s][c],B[s][c]],[A[r][h],B[r][h]],p);b=mulpoly([A[s][h],B[s][h]],[A[r][c],B[r][c]],p)
  out.append([(T[1][j]*T[0][0]*x-T[1][0]*T[0][j]*y)%p for x,y in zip(a,b)])
 return out
def resultant(a,b,p):return ((a[2]*b[0]-a[0]*b[2])**2-(a[2]*b[1]-a[1]*b[2])*(a[1]*b[0]-a[0]*b[1]))%p
def det(A,p):
 A=[r[:] for r in A];v=1
 for j in range(len(A)):
  k=next((k for k in range(j,len(A)) if A[k][j]),None)
  if k is None:return 0
  if k!=j:A[k],A[j]=A[j],A[k];v=-v
  pivot=A[j][j];v=v*pivot%p;s=pow(pivot,-1,p)
  for k in range(j+1,len(A)):
   a=A[k][j]*s%p;A[k]=[(x-a*y)%p for x,y in zip(A[k],A[j])]
 return v%p
def calibrated(T,M,p):
 n=len(T);assert all(T[0]) and all(M[0]);assert all(T[i][0] and M[i][0] for i in range(n))
 v=[t*pow(m,-1,p)%p for t,m in zip(T[0],M[0])];u=[T[i][0]*pow(M[i][0]*v[0]%p,-1,p)%p for i in range(n)]
 out=[[u[i]*M[i][j]*v[j]%p for j in range(n)] for i in range(n)]
 assert out[0]==T[0] and all(out[i][0]==T[i][0] for i in range(n))
 return sum(out[i][j]!=T[i][j] for i in range(1,n) for j in range(1,n))
def main():
 source=Path(__file__).parent/'source';output=Path(__file__).parent;tmp=tempfile.TemporaryDirectory();binary=Path(tmp.name)/'exhaustive_own';subprocess.run(['g++','-O3','-std=c++17',str(output/'exhaustive_own.cpp'),'-o',str(binary)],check=True);source_results=json.loads((source/'phase38_audit.json').read_text());cases=[]
 for p in [998244353,2013265921]:
  for n in [4,8,16,32,64,128,256]:
   A,C,F,G,H=kernels(n,p);Ai=inv(A,p);Ci=inv(C,p);T=mm(mm(Ai,F,p),Ci,p)
   expected=list(map(int,(source/f'phase38_instance_N{n}_p{p}.txt').read_text().split()));got=[n,p]+[v for M in [T,G,H] for r in M for v in r];assert expected==got
   f,g=gate(T,G,H,[0,1,0,1,2],p);res=resultant(f,g,p);assert res
   record=next(x for x in source_results['field_results'] if x['N']==n and x['prime']==p)
   assert record['first_eq']==f and record['second_eq']==g and record['quadratic_resultant']==res
   u,v=record['bezout_u'],record['bezout_v'];a=mulpoly(u,f,p);b=mulpoly(v,g,p);assert [(x+y)%p for x,y in zip(a,b)]==[1,0,0,0]
   mismatch=calibrated(T,[[(G[i][j]+7*H[i][j])%p for j in range(n)] for i in range(n)],p);assert mismatch==(n-1)**2
   dat={'N':n,'prime':p,'fixed_order_resultant':res,'anchor_calibration_matches':2*n-1,'interior_mismatches':mismatch,'instance_entries_rebuilt':3*n*n,'outer_inverses_rebuilt':True}
   if n<=64:
    run=subprocess.run([str(binary)],input=' '.join(map(str,got)),text=True,capture_output=True,check=True);ex=json.loads(run.stdout);assert ex['checked']==n*n*(n-1)**2*(n-2);expectedzeros=1 if n==64 and p==2013265921 else 0;assert ex['zeros']==expectedzeros
    if expectedzeros:assert ex['exceptions']==[[53,55,19,26,5]]
    dat['exhaustive']=ex
   else:
    zeros=0
    for j in range(200000):
     rr=R.sample(range(n),2);cc=R.sample(range(n),3);ff,gg=gate(T,G,H,rr+cc,p);zeros+=resultant(ff,gg,p)==0
    assert zeros==0;dat['own_independent_sample_count']=200000;dat['own_sample_zeros']=zeros
   if n==64:
    ff,gg=gate(T,G,H,[53,55,19,26,5],p);collision=resultant(ff,gg,p);assert collision==(470304279 if p==998244353 else 0);dat['exception_mapping_resultant']=collision
   cases.append(dat);print('PASS',n,p,flush=True)
 # Formula vs direct Sylvester determinant, including low-degree degenerations.
 for p in [101,998244353]:
  for j in range(150):
   a=[R.randrange(p) for _ in range(3)];b=[R.randrange(p) for _ in range(3)]
   if j<50:a[2]=0
   if j<20:b[2]=0
   S=[[a[2],a[1],a[0],0],[0,a[2],a[1],a[0]],[b[2],b[1],b[0],0],[0,b[2],b[1],b[0]]]
   assert resultant(a,b,p)==det(S,p)
 # Planted arbitrary masked/permuted pencil at a common root; mask recovery exact.
 planted=0
 for n in [4,8,16]:
  p=998244353
  for trial in range(10):
   a=[[R.randrange(1,p) for j in range(n)] for i in range(n)];b=[[R.randrange(1,p) for j in range(n)] for i in range(n)];star=R.randrange(p);rp=R.sample(range(n),n);cp=R.sample(range(n),n);u=[R.randrange(1,p) for i in range(n)];v=[R.randrange(1,p) for i in range(n)];M=[[(a[rp[i]][cp[j]]+star*b[rp[i]][cp[j]])%p for j in range(n)] for i in range(n)];T=[[u[i]*M[i][j]*v[j]%p for j in range(n)] for i in range(n)]
   f,g=gate(T,a,b,[rp[0],rp[1],cp[0],cp[1],cp[2]],p);assert sum(f[j]*pow(star,j,p) for j in range(3))%p==0 and sum(g[j]*pow(star,j,p) for j in range(3))%p==0 and resultant(f,g,p)==0;assert calibrated(T,M,p)==0;planted+=1
 result={'status':'PASS','cases':cases,'Sylvester_controls':300,'planted_mask_permutation_controls':planted,'source_programs_executed':False}
 (output/'INDEPENDENT_RESULTS.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
if __name__=='__main__':main()
