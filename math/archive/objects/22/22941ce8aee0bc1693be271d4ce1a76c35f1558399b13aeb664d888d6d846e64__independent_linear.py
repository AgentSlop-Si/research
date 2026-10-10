"""Auditor-authored exact finite-field helpers. No constructor/source imports."""
def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def mm(a,b,p):return [[sum(x*y for x,y in zip(r,c))%p for c in zip(*b)] for r in a]
def mv(a,x,p):return [sum(u*v for u,v in zip(r,x))%p for r in a]
def add(a,b,p,t=1):return [[(x+t*y)%p for x,y in zip(r,s)] for r,s in zip(a,b)]
def scale(a,t,p):return [[v*t%p for v in r] for r in a]
def block(a,rr,cc):return [[a[i][j] for j in cc] for i in rr]
def inverse(a,p):
 n=len(a);z=[r[:]+e for r,e in zip(a,eye(n))]
 for j in range(n):
  u=next((i for i in range(j,n) if z[i][j]),None)
  if u is None:return None
  z[j],z[u]=z[u],z[j];iv=pow(z[j][j],-1,p);z[j]=[v*iv%p for v in z[j]]
  for i in range(n):
   if i!=j:
    t=z[i][j];z[i]=[(x-t*y)%p for x,y in zip(z[i],z[j])]
 return [r[n:] for r in z]
def det(a,p):
 z=[r[:] for r in a];answer=1
 for j in range(len(z)):
  u=next((i for i in range(j,len(z)) if z[i][j]),None)
  if u is None:return 0
  if u!=j:z[j],z[u]=z[u],z[j];answer=-answer
  v=z[j][j];answer=answer*v%p;iv=pow(v,-1,p)
  for i in range(j+1,len(z)):
   t=z[i][j]*iv%p;z[i]=[(x-t*y)%p for x,y in zip(z[i],z[j])]
 return answer%p
def rank(a,p):
 z=[r[:] for r in a];k=0
 for j in range(len(z[0]) if z else 0):
  u=next((i for i in range(k,len(z)) if z[i][j]),None)
  if u is None:continue
  z[k],z[u]=z[u],z[k];iv=pow(z[k][j],-1,p)
  for i in range(k+1,len(z)):
   t=z[i][j]*iv%p;z[i]=[(x-t*y)%p for x,y in zip(z[i],z[k])]
  k+=1
  if k==len(z):break
 return k
def root_table(n,p):
 w=pow(5 if p==97 else 3,(p-1)//n,p);assert pow(w,n,p)==1 and pow(w,n//2,p)!=1
 out=[1]*n
 for j in range(1,n):out[j]=out[j-1]*w%p
 return w,out
def qmatrix(N,W,p):
 q=[[0]*N for _ in range(N)]
 for j in range(N):q[2*j%N][j]=1;q[(2*j+1)%N][j]=W[j]
 return q
def dot(x,y,p):return sum(a*b for a,b in zip(x,y))%p
