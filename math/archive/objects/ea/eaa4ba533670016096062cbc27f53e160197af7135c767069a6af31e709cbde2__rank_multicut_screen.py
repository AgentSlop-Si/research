from functools import lru_cache
from itertools import permutations
from collections import Counter
import time

n=8;p=97
w=pow(5,(p-1)//n,p)
assert pow(w,n,p)==1 and pow(w,n//2,p)!=1
F=[[pow(w,i*j,p) for j in range(n)] for i in range(n)]
F2=[[pow(w,(i*3%n)*j,p) for j in range(n)] for i in range(n)]

@lru_cache(None)
def run_segments(mask):
 ans=[];k=0
 while k<n:
  if (mask>>k)&1:
   j=k
   while j+1<n and (mask>>(j+1))&1:j+=1
   ans.append((k,j));k=j+1
  else:k+=1
 return ans

def cut_cost(mask,up=1,down=1):
 comp=((1<<n)-1)^mask; res=0
 for a,b in run_segments(mask):
  if comp & ((1<<a)-1):res+=up
  if comp & (((1<<n)-1)^((1<<(b+1))-1)):res+=down
 return res

def rk(M,rows,cols):
 if not rows or not cols:return 0
 B=[[M[i][j] for j in cols] for i in rows]
 r=0
 for j in range(len(cols)):
  piv=next((k for k in range(r,len(rows)) if B[k][j]%p),None)
  if piv is None:continue
  B[r],B[piv]=B[piv],B[r]
  inv=pow(B[r][j],-1,p)
  for x in range(j,len(cols)):B[r][x]=B[r][x]*inv%p
  for k in range(r+1,len(rows)):
   x=B[k][j]
   if x:
    for l in range(j,len(cols)):B[k][l]=(B[k][l]-x*B[r][l])%p
  r+=1
  if r==len(rows):break
 return r

def precompute(M,allowedI,allowedH):
 full=(1<<n)-1
 pop=[i.bit_count() for i in range(1<<n)]
 costB={I:cut_cost(I) for I in allowedI}
 costC={H:cut_cost(H) for H in allowedH}
 vals={}
 for I in allowedI:
  R=[i for i in range(n) if not(I>>i)&1]
  for H in allowedH:
   # if |H|<|I| cannot include J size |I|
   if pop[H]<pop[I]:continue
   rank=rk(M,R,[j for j in range(n) if H>>j&1])
   gap=pop[I]-pop[H]+rank-costB[I]-costC[H]
   if gap<=0:continue
   # violations hold whenever J subset H
   sub=H
   while sub:
    if pop[sub]==pop[I]:
     k=(I,sub)
     if k not in vals or vals[k][0]<gap:vals[k]=(gap,H,rank)
    sub=(sub-1)&H
 return vals

full=(1<<n)-1
allnon=[i for i in range(1,full)]
I1=[i for i in allnon if len(run_segments(i))==1]
I2=[i for i in allnon if len(run_segments(i))<=2]
H1=[i for i in allnon if len(run_segments(i))==1]
H2=[i for i in allnon if len(run_segments(i))<=2]
start=time.time()
known=precompute(F,I1,H1)
print('known #',len(known), 'time',time.time()-start)
start=time.time()
v=precompute(F,I2,H2)
print('new constraints',len(v),'additional',len(set(v)-set(known)),'time',time.time()-start)
start=time.time()
out=Counter();examples=[]
for pi in permutations(range(n)):
 good1=True;good2=True
 for I in I2:
  J=sum(1<<pi[j] for j in range(n) if (I>>j)&1)
  if good1 and (I,J) in known:good1=False
  if good2 and (I,J) in v:good2=False
  if not good1 and not good2:break
 out[(good1,good2)]+=1
 if good1 and not good2 and len(examples)<5:
  for I in I2:
   J=sum(1<<pi[j] for j in range(n) if (I>>j)&1)
   if (I,J) in v and (I,J) not in known:
    examples.append((pi,I,J,v[(I,J)]));break
print('screening',out, 'examples',examples,'time',time.time()-start)
