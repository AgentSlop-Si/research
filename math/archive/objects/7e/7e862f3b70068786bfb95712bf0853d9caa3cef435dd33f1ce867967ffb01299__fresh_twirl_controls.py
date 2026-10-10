"""Independent exact magnetic-twirl controls; supplied source is never loaded."""
from pathlib import Path
import json,math
OUT=Path(__file__).resolve().parent

def ident(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def invmat(A,p):
 n=len(A);B=[[(v%p) for v in row]+ident(n)[i] for i,row in enumerate(A)];det=1
 for j in range(n):
  piv=next((i for i in range(j,n) if B[i][j]),None)
  if piv is None:return None,0
  if piv!=j:B[piv],B[j]=B[j],B[piv];det=-det
  v=B[j][j];det=det*v%p;iv=pow(v,-1,p);B[j]=[x*iv%p for x in B[j]]
  for i in range(n):
   if i!=j:
    z=B[i][j]
    if z:B[i]=[(x-z*y)%p for x,y in zip(B[i],B[j])]
 return [r[n:] for r in B],det%p

def rank(A,p):
 A=[r[:] for r in A];i=0
 for j in range(len(A[0])):
  row=next((k for k in range(i,len(A)) if A[k][j]%p),None)
  if row is None:continue
  A[row],A[i]=A[i],A[row];iv=pow(A[i][j]%p,-1,p);A[i]=[x*iv%p for x in A[i]]
  for k in range(i+1,len(A)):
   z=A[k][j]%p
   if z:A[k]=[(x-z*y)%p for x,y in zip(A[k],A[i])]
  i+=1
  if i==len(A):break
 return i

def product(A,B,p):
 return [[sum(a*B[k][j] for k,a in enumerate(row))%p for j in range(len(B[0]))] for row in A]
def equal(A,B):return A==B

def root(n,p):
 if n==1:return 1
 for w in range(2,p):
  if pow(w,n,p)==1 and all(pow(w,d,p)!=1 for d in range(1,n) if n%d==0):return w
 raise ValueError('root')

def qbinomial(n,k,q,p):
 row=[1]
 for d in range(1,n+1):
  row=[((row[r] if r<len(row) else 0)+(pow(q,d-r,p)*row[r-1] if r else 0))%p for r in range(d+1)]
 return row[k]

# Independent fresh evaluator: direct seed plus rolling window, then each cycle.
def window(x,a,L,p):
 n=len(x);seed=0;c=1
 for r in range(L):seed=(seed+c*x[(-r)%n])%p;c=c*a%p
 y=[seed]
 for i in range(1,n):y.append((a*y[-1]+x[i]-c*x[(i-L)%n])%p)
 return y

def solve_strided(z,d,c,K,p):
 n=len(z);M=n//K
 if d==0:
  if c==0:raise ValueError('singular')
  return [-z[(i+K)%n]*pow(c,-1,p)%p for i in range(n)]
 r=c*pow(d,-1,p)%p;den=(1-pow(r,M,p))%p
 if not den:raise ValueError('singular')
 y=[0]*n
 for residue in range(K):
  indices=list(range(residue,n,K));v=0
  for i in indices:v=(r*v+z[i]*pow(d,-1,p))%p
  v=v*pow(den,-1,p)%p
  for i in indices:v=(r*v+z[i]*pow(d,-1,p))%p;y[i]=v
 return y

def sector_executor(x,a,b,K,q,ell,p):
 n=len(x);z=[pow(q,i*ell,p)*v%p for i,v in enumerate(x)]
 # Fresh product expansion of prod_(i=1)^ell (1-q^i t).
 coeff=[1];den=1
 for i in range(1,ell+1):
  t=pow(q,i,p);new=[0]*(len(coeff)+1)
  for j,v in enumerate(coeff):new[j]=(new[j]+v)%p;new[j+1]=(new[j+1]-t*v)%p
  coeff=new;den=den*(1-t)%p
 factor=pow(b,ell,p)*pow(den,-1,p)%p;rhs=[0]*n
 for h,v in enumerate(coeff):
  win=window(z,a*pow(q,h,p)%p,K-ell,p)
  rhs=[(x+factor*v*y)%p for x,y in zip(rhs,win)]
 return solve_strided(rhs,(1-pow(b,K,p))%p,pow(a,K,p),K,p)

records=[];fullentries=0;weightedentries=0;singular=0;legalzero=0;noncommuting=0;rankcases=0
# Both parities and all edge cases, including N1, K1, K=N, alpha0,beta0,d0.
for n,K,p in [(1,1,17),(2,1,17),(2,2,17),(3,1,97),(3,3,97),(4,2,97),(4,4,97),(6,2,97),(6,3,97),(8,2,97),(8,4,97),(8,8,97),(12,3,97),(12,4,97),(15,5,241),(16,4,97),(20,5,241),(24,6,97)]:
 w=root(n,p);q=pow(w,n//K,p);S=[[int(i==(j+1)%n) for j in range(n)] for i in range(n)]
 params=[(0,0),(0,1),(1,0),(1,1),(2,1),(0,2),(2,3),(w,2)]
 for a,b in params:
  guard=(pow((1-pow(b,K,p))%p,n//K,p)-pow(a,n,p))%p
  inverses=[];Qs=[]
  for j in range(K):
   Q=[[(int(i==t)*(1-b*pow(q,i+j,p))-a*int(i==(t+1)%n))%p for t in range(n)] for i in range(n)]
   G,det=invmat(Q,p);assert det==guard;assert (G is not None)==bool(guard);inverses.append(G);Qs.append(Q)
  if not guard:singular+=1;continue
  if (1-pow(b,K,p))%p==0:legalzero+=1
  if K>1 and a%p and b%p:
   assert product(Qs[0],Qs[1],p)!=product(Qs[1],Qs[0],p);noncommuting+=1
  ik=pow(K,-1,p)
  R0=[[sum(G[i][t] for G in inverses)*ik%p for t in range(n)] for i in range(n)]
  expectedrank=n if pow(a,n,p)!=1 else n-K+1
  assert rank(R0,p)==expectedrank;rankcases+=1
  assert product(R0,S,p)==product(S,R0,p)
  for ell in range(K):
   R=[[sum(pow(q,-j*ell,p)*inverses[j][i][t] for j in range(K))*ik%p for t in range(n)] for i in range(n)]
   # Independent closed Gaussian-binomial matrix before D inverse.
   P=[[sum(pow(a,r,p)*qbinomial(r+ell,ell,q,p)*int(i==(t+r)%n) for r in range(K-ell))*pow(b,ell,p)*pow(q,t*ell,p)%p for t in range(n)] for i in range(n)]
   D=[[(int(i==t)*(1-pow(b,K,p))-pow(a,K,p)*int(i==(t+K)%n))%p for t in range(n)] for i in range(n)]
   DI,detD=invmat(D,p);assert detD==pow(guard,K,p)
   assert product(DI,P,p)==R
   assert product(R,S,p)==[[pow(q,ell,p)*x%p for x in row] for row in product(S,R,p)]
   for t in range(n):
    x=[int(i==t) for i in range(n)];y=sector_executor(x,a,b,K,q,ell,p)
    assert y==[R[i][t] for i in range(n)]
    if ell==0:fullentries+=n
    else:weightedentries+=n
  records.append({'N':n,'K':K,'prime':p,'omega':w,'alpha':a,'beta':b,'guard':guard,'all_sectors_checked':K,'rank_R0':expectedrank})
# Exact Fourier commutator ranks; all divisors at these lengths.
comm=[]
for n,p in [(1,17),(2,17),(3,97),(4,97),(6,97),(8,97),(12,97),(15,241),(16,97),(20,241),(24,97)]:
 w=root(n,p);F=[[pow(w,(-i*j)%n,p) for j in range(n)] for i in range(n)]
 for K in range(1,n+1):
  if n%K:continue
  C=[[(F[i][(j+K)%n]-F[(i-K)%n][j])%p for j in range(n)] for i in range(n)]
  r=rank(C,p);pred=n-K if (n-K)%2==0 else n;assert r==pred
  comm.append({'N':n,'K':K,'rank':r})
# Weyl coefficients at odd prime N, compared by their explicit trace sums.
weyl=[]
for n,p in [(3,7),(5,11),(7,29),(11,23),(13,53)]:
 w=root(n,p);G=sum(pow(w,-t*t%n,p) for t in range(n))%p
 assert G and G*G%p==pow(-1,(n-1)//2,p)*n%p
 for a in range(n):
  for b in range(n):
   c=sum(pow(w,(-t*t-(a+b)*t)%n,p) for t in range(n))*pow(n,-1,p)%p
   expected=G*pow(n,-1,p)*pow(w,(a+b)**2*pow(4,-1,n)%n,p)%p
   assert c==expected and c
 weyl.append({'N':n,'prime':p,'nonzero_coefficients':n*n})
r={'policy':'Only this freshly authored control program executed; no supplied research modules loaded.','legal_cases':len(records),'singular_parameter_cases_rejected':singular,'legal_zero_d_cases':legalzero,'generic_noncommuting_cases':noncommuting,'unweighted_basis_entries':fullentries,'weighted_basis_entries':weightedentries,'rank_R0_cases':rankcases,'commutator_rank_cases':len(comm),'weyl_coefficients':sum(x['nonzero_coefficients'] for x in weyl),'cases':records,'commutator_cases':comm,'weyl_cases':weyl}
(OUT/'fresh_twirl_results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if not k.endswith('cases') or isinstance(v,int)},indent=2))
