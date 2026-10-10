import sympy as sp, json, itertools, time
from sympy import QQ
from pathlib import Path
OUT=Path(__file__).resolve().parent

def fld(N):
 t=sp.symbols('t'); K=QQ.alg_field_from_poly(sp.Poly(sp.cyclotomic_poly(N,t),t),alias='q');return K,K.unit

def solve(A,b,K):
 A=[list(r)+[v] for r,v in zip(A,b)]; m=len(A); n=len(A[0])-1;p=[];r=0
 for c in range(n):
  h=next((i for i in range(r,m) if A[i][c]),None)
  if h is None:continue
  A[h],A[r]=A[r],A[h];z=A[r][c]; A[r]=[v/z for v in A[r]]
  for i in range(m):
   if i!=r and A[i][c]:
    z=A[i][c];A[i]=[x-z*y for x,y in zip(A[i],A[r])]
  p.append(c);r+=1
  if r==m:break
 if any(not any(row[:n]) and row[n] for row in A):return None
 sol=[K.zero]*n
 for i,c in enumerate(p):sol[c]=A[i][n]
 return sol,p

def mult(f,g,K):
 a=[K.zero]*(len(f)+len(g)-1)
 for i,u in enumerate(f):
  for j,v in enumerate(g):a[i+j]+=u*v
 return a

def ev(f,x,K):
 v=K.zero
 for a in f[::-1]:v=v*x+a
 return v

def enc(a,N):
 return [str(v) for v in ([QQ.zero]*(N-1-len(a.to_list()))+a.to_list())[::-1]]

def setup(N):
 K,q=fld(N); one=K.one; zero=K.zero
 def G(a,b,e,d):
  r=e*a%N;l=d*b%N
  if r+l>=N:return zero
  z=q**(e*d%N);v=one
  for j in range(1,l+1):v*= (one-z**(r+j))/(one-z**j)
  return v
 f=lambda a,b:q**(pow(4,-1,N)*(a+b)**2%N)
 H=q/(one+q)
 s=[one]+[(f(a,1)/H-G(a,1,-1,1))/G(a,1,1,1) for a in range(2,N-1)]
 return K,q,G,f,H,s

if __name__=='__main__':
 results={}
 for N in (7,11):
  K,q,G,f,H,s=setup(N); d=N-3
  for exps in itertools.combinations(range(1,N),d-1):
   nodes=[q**e for e in exps]; p=[K.one]
   for x in nodes:p=mult(p,[-x,K.one],K)
   den=sum((p[k]*s[k] for k in range(d)),K.zero)
   if not den:continue
   x=sum((p[k]*s[k+1] for k in range(d)),K.zero)/den
   if not x or x in nodes:continue
   nodes.append(x)
   M=[[v**a for v in nodes]+[K.one]+[v**((-a)%N) for v in nodes] for a in range(N)]
   z=solve(M,[f(a,0) for a in range(N)],K)
   if z is None or len(z[1])!=N:continue
   r={'N':N,'degree':d,'fixed_exponents':list(exps),'last_node':enc(x,N),'denominator':enc(den,N),'axis_pivot_columns':z[1], 'axis_weights':[enc(v,N) for v in z[0]],'s':[enc(v,N) for v in s]}
   results[str(N)]=r; print('FOUND',N,exps,'last node',r['last_node'],'pivots',z[1],flush=True);break
 (OUT/'INTERMEDIATE_NODE_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
