#!/usr/bin/env python3
"""Fresh exact modular checker; standard library only; no historical imports."""
import json,hashlib,time
from pathlib import Path
from math import isqrt
P=1000000007
DEN=101

def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def mul(A,B):
 n=len(A); m=len(B[0]); k=len(B)
 return [[sum(A[i][t]*B[t][j] for t in range(k))%P for j in range(m)] for i in range(n)]
def inv(A):
 n=len(A);B=[r[:]+s for r,s in zip(A,eye(n))]
 for j in range(n):
  k=next((i for i in range(j,n) if B[i][j]),None)
  assert k is not None,'illegal modular denominator'
  B[j],B[k]=B[k],B[j]; t=pow(B[j][j],P-2,P); B[j]=[x*t%P for x in B[j]]
  for i in range(n):
   if i!=j and B[i][j]:
    t=B[i][j];B[i]=[(x-t*y)%P for x,y in zip(B[i],B[j])]
 return [r[n:] for r in B]
def rank(A):
 A=[r[:] for r in A];m=len(A);n=len(A[0]);r=0
 for j in range(n):
  k=next((i for i in range(r,m) if A[i][j]),None)
  if k is None:continue
  A[r],A[k]=A[k],A[r];t=pow(A[r][j],P-2,P)
  for i in range(r+1,m):
   if A[i][j]:
    c=A[i][j]*t%P
    for z in range(j+1,n):A[i][z]=(A[i][z]-c*A[r][z])%P
  r+=1
  if r==m:return r
 return r

def maps(s):
 out=[[] for _ in range(4)]
 for x in range(s):
  for y in range(s):
   nxt=[((x+2*y)%s,y),((x+2*y+1)%s,y),(x,(y+2*x)%s),(x,(y+2*x+1)%s)]
   for j,(u,v) in enumerate(nxt):out[j].append(s*u+v)
 return out

def case(s):
 n=s*s; ps=maps(s);Gs=[]; ms=[]
 for q in range(20):
  a=q+1;w=a*pow(DEN,P-2,P)%P;perm=ps[q%4];A=eye(n)
  for j,i in enumerate(perm):A[i][j]=(A[i][j]-w)%P
  G=inv(A);assert mul(A,G)==eye(n);Gs.append(G)
  seen=set();cycles=[]
  for j in range(n):
   if j not in seen:
    cyc=[];v=j
    while v not in seen:cyc.append(v);seen.add(v);v=perm[v]
    assert v==j;assert (pow(DEN,len(cyc),P)-pow(a,len(cyc),P))%P
    cycles.append(len(cyc))
  ms.append({'index':q,'map':q%4,'weight_numerator':a,'weight_denominator':DEN,'cycle_lengths':cycles})
 X=[[sum(G[i][j] for G in Gs[:10])%P for j in range(n)] for i in range(n)]
 Y=[[sum(G[i][j] for G in Gs[10:])%P for j in range(n)] for i in range(n)]
 T=mul(Y,X);counts={};fail=[];cap_min=20*n;stream=hashlib.sha256()
 for mask in range(1,(1<<n)-1):
  I=[i for i in range(n) if mask>>i&1];J=[i for i in range(n) if not(mask>>i&1)];k=min(len(I),len(J))
  r=rank([[T[i][j] for j in J] for i in I]);counts[str(k)]=counts.get(str(k),0)+1
  cap=sum(sum((mask>>i&1) and not(mask>>j&1) for j,i in enumerate(perm)) for perm in ps)*5
  cap_min=min(cap_min,cap-k);stream.update(f'{mask}:{r}:{cap}\n'.encode())
  if r!=k:fail.append({'mask':mask,'rank':r,'maximum':k})
 lamX=sum(pow(1-(q+1)*pow(DEN,P-2,P)%P,P-2,P) for q in range(10))%P
 lamY=sum(pow(1-(q+1)*pow(DEN,P-2,P)%P,P-2,P) for q in range(10,20))%P
 assert all(sum(row)%P==lamX*lamY%P for row in T)
 return {'s':s,'N':n,'field_prime':P,'branches':ms,'stages':[[0,10],[10,20]],'product_order':'YX','cuts_checked':(1<<n)-2,'cut_counts_by_min_side':counts,'failure_count':len(fail),'first_failures':fail[:10],'minimum_capacity_surplus':cap_min,'cut_stream_sha256':stream.hexdigest(),'matrix_mod_prime':T,'constant_vector_eigenvalue':lamX*lamY%P}

if __name__=='__main__':
 assert P>2 and all(P%d for d in range(2,isqrt(P)+1)), 'prime verification failed'
 assert rank([[0,0],[0,0]])==0 and rank([[1,2],[2,4]])==1 and rank([[0,1],[1,0]])==2
 st=time.time();out={'prime_verified_by_trial_division':True,'rank_controls_passed':True,'cases':[case(s) for s in (2,3,4)]};out['elapsed_seconds']=time.time()-st
 dest=Path(__file__).with_name('CHECK_RESULTS.json');dest.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({k:[{z:r[z] for z in ['N','cuts_checked','failure_count','first_failures','minimum_capacity_surplus','cut_stream_sha256']} for r in out[k]] for k in ['cases']},indent=2));print('seconds',out['elapsed_seconds'])
