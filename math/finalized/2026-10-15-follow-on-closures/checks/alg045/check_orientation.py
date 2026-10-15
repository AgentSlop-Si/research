import json
from pathlib import Path

def matmul(A,B,p):
 return [[sum(a*b for a,b in zip(row,col))%p for col in zip(*B)]for row in A]
def transpose(A):return [list(r)for r in zip(*A)]
def inv(A,p):
 n=len(A);R=[r[:]+[int(i==j)for j in range(n)]for i,r in enumerate(A)]
 for k in range(n):
  i=next(i for i in range(k,n)if R[i][k]);R[i],R[k]=R[k],R[i];c=pow(R[k][k],-1,p);R[k]=[v*c%p for v in R[k]]
  for i in range(n):
   if i!=k:
    c=R[i][k];R[i]=[(v-c*w)%p for v,w in zip(R[i],R[k])]
 return [r[n:]for r in R]
def support(A):return [sum(v!=0 for v in r)for r in A]
def gen(a,m,b,p,w):
 n=a*m*b;P=[[0]*n for _ in range(n)];Q=[[0]*n for _ in range(n)]
 for r0 in range(a):
  for t2 in range(b):
   for t1 in range(m):
    for t0 in range(a):
     k=t2+b*t1+b*m*t0;h=(r0*b+t2)*m+t1
     P[k][h]=pow(w,r0*k,p)
   for r1 in range(m):
    h=(r0*b+t2)*m+r1
    for r2 in range(b):Q[h][r0+a*r1+a*m*r2]=pow(w,a*r1*t2+a*m*r2*t2,p)
 return P,Q
results=[]
for a,m,b,p,w in [(2,2,2,17,2),(4,2,2,17,3),(2,4,2,17,3),(4,4,4,193,11),(2,3,2,13,2)]:
 n=a*m*b
 if pow(w,n,p)!=1 or any(pow(w,k,p)==1 for k in range(1,n)):continue
 P,Q=gen(a,m,b,p,w);S=[[int(i==(j+1)%n)for j in range(n)]for i in range(n)];D=[[pow(w,j,p)*int(i==j)for j in range(n)]for i in range(n)]
 case={'a':a,'m':m,'b':b,'N':n,'p':p,'omega':w,'actions':{}}
 for name,H in [('P',P),('P_transpose',transpose(P)),('Q',Q)]:
  Hi=inv(H,p)
  for nameA,A in [('shift',S),('clock',D)]:
   T=matmul(matmul(H,A,p),Hi,p);ss=support(T);case['actions'][name+'_'+nameA]={'monomial':all(v==1 for v in ss),'max_row_support':max(ss)}
   if name=='P' and max(ss)>1:case['actions'][name+'_'+nameA]['first_bad_row']={'row':next(i for i,v in enumerate(ss)if v>1),'values':next(r for r in T if sum(v!=0 for v in r)>1)}
 results.append(case)
Path(__file__).with_name('ORIENTATION_CHECKS.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results,indent=2))
