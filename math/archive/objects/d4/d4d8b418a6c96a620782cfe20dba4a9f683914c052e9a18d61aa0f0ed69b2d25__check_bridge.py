#!/usr/bin/env python3
"""Fresh checks; no user-supplied program is run or imported."""
import json, math, random, platform
from pathlib import Path
import mpmath as mp
P=998244353; ROOT=3
OUT=Path(__file__).resolve().parent
rng=random.Random(1847)
def inv(x): return pow(int(x)%P,P-2,P)
def det(a):
 a=[list(map(lambda x:int(x)%P,row)) for row in a]; n=len(a); d=1
 for c in range(n):
  r=next((r for r in range(c,n) if a[r][c]),None)
  if r is None:return 0
  if r!=c:a[r],a[c]=a[c],a[r];d=-d
  v=a[c][c];d=d*v%P;iv=inv(v)
  for r in range(c+1,n):
   f=a[r][c]*iv%P
   for j in range(c+1,n):a[r][j]=(a[r][j]-f*a[c][j])%P
 return d%P
def rank(a):
 a=[list(map(lambda x:int(x)%P,row)) for row in a]; m=len(a); n=len(a[0]); r=0
 for c in range(n):
  s=next((s for s in range(r,m) if a[s][c]),None)
  if s is None:continue
  a[r],a[s]=a[s],a[r];iv=inv(a[r][c])
  for j in range(c,n):a[r][j]=a[r][j]*iv%P
  for s in range(m):
   if s==r:continue
   f=a[s][c]
   for j in range(c,n):a[s][j]=(a[s][j]-f*a[r][j])%P
  r+=1
  if r==m:break
 return r

def polyval(c,x):
 y=0
 for v in reversed(c):y=(y*x+v)%P
 return y

def grid(N):
 Q=1<<(N-1).bit_length();j=[(2*Q*k+N)//(2*N) for k in range(N)]
 return Q,j,[(Q*k-N*j[k])*inv(N)%P for k in range(N)]
results={'scope':'Fresh independent exact finite-field and high-precision controls; no uploaded code executed','python':platform.python_version(),'prime':P}
# A identity plus arbitrary disjoint Cauchy minors.
ac=[]
for K in [2,4,8,16,32,64]:
 z=pow(ROOT,(P-1)//K,P);aa=[pow(z,i,P) for i in range(K)]
 A=[[sum(b*pow(z,((i-j)*b)%K,P) for b in range(K))*inv(K)%P for j in range(K)]for i in range(K)]
 for i in range(K):
  for j in range(K):assert A[i][j]==((K-1)*inv(2)%P if i==j else aa[j]*inv(aa[i]-aa[j])%P)
 minors=0
 for t in range(1,min(8,K//2)+1):
  for _ in range(3):
   ij=rng.sample(range(K),2*t);assert det([[A[i][j]for j in ij[t:]]for i in ij[:t]])!=0;minors+=1
 ac.append({'K':K,'entries':K*K,'nonzero_disjoint_minors':minors})
results['A_and_Cauchy']=ac
# Cyclic scan commutator determinant, selected principal minor.
cc=[]
for N in [3,5,7,9,13,17,23,31,47,61]:
 Q,j,w=grid(N)
 # Sort selected output rows into arbitrary odd-a cycle order.
 for a in [1,3,5]:
  order=sorted(range(N),key=lambda k:(j[k]*pow(a,-1,Q))%Q);v=[w[k]for k in order]
  C=[[(v[i]-v[k])*(inv(2) if i<=k else -inv(2))%P for k in range(N)]for i in range(N)]
  theoretical=inv(4)*(-1)**N
  for i in range(N):theoretical=theoretical*(v[i]-v[(i+1)%N])%P
  d=det(C);assert d==theoretical and d!=0
 cc.append({'N':N,'Q':Q,'odd_orders_tested':3,'selected_rank':N})
results['selected_commutators']=cc
# Structured forcing block decomposition, root phases, and complete prefix reconstruction.
bc=[]
for N,M,R,B in [(13,4,3,2),(29,4,4,2),(61,8,5,2),(61,8,5,4),(113,8,7,4)]:
 Q,j,w=grid(N);K=Q//M;z=pow(ROOT,(P-1)//Q,P)
 for a,beta in [(1,0),(3,2),(5,7)]:
  # Monomial coefficient bank; one arbitrary length-K vector per order.
  F=[[rng.randrange(P) for _ in range(R)]for _ in range(K)]
  boundary=[pow(z,(M*((a*u)%Q+beta)+a*M*(M-1)//2)%Q,P)for u in range(K)]
  pol=[[ (F[(a*u)%K][r]-boundary[u]*F[(a*u+a*M)%K][r])%P for r in range(R)]for u in range(K)]
  gamma=[pow(z,(a*t*(t-1)//2+beta*t)%Q,P)for t in range(Q)]
  v=[[gamma[u]*c%P for c in pol[u]]for u in range(K)]
  rho=pow(z,a*K%Q,P)
  eta=[pow(z,(a*(ell*K)*(ell*K-1)//2+beta*ell*K)%Q,P)for ell in range(M)]
  for ell in range(M):
   for u in range(K):assert gamma[ell*K+u]==gamma[u]*eta[ell]*pow(rho,ell*u,P)%P
  # Full reference vector of polynomial prefix coefficients, used only as test oracle.
  coeff=[[gamma[t]*x%P for x in pol[t%K]]for t in range(Q)]
  total=[sum(row[r] for row in coeff)%P for r in range(R)]
  pref=[0]*R;ref={}; nodes={}
  for k in range(N):nodes[j[k]*pow(a,-1,Q)%Q]=(k,w[k])
  for t in range(Q):
   if t in nodes:
    k,x=nodes[t];ref[k]=polyval([(total[r]*inv(2)-pref[r])%P for r in range(R)],x)
   pref=[(pref[r]+coeff[t][r])%P for r in range(R)]
  # Two-pass blocked algorithm. Each block sum is an M-point DFT in ell for each r.
  def block(q,ell):
   return [eta[ell]*sum(pow(rho,ell*u,P)*v[u][r]for u in range(q,q+B))%P for r in range(R)]
  totals=[[0]*R for _ in range(M)]
  for q in range(0,K,B):
   for ell in range(M):
    d=block(q,ell);totals[ell]=[(totals[ell][r]+d[r])%P for r in range(R)]
  start=[];p=[0]*R
  for ell in range(M):start.append(p[:]);p=[(p[r]+totals[ell][r])%P for r in range(R)]
  curs=[s[:]for s in start];got={}
  for q in range(0,K,B):
   for ell in range(M):
    coarse=[(total[r]*inv(2)-curs[ell][r])%P for r in range(R)]
    for u in range(q,q+B):
     t=ell*K+u
     if t not in nodes:continue
     k,x=nodes[t]
     local=eta[ell]*sum(pow(rho,ell*s,P)*polyval(v[s],x)for s in range(q,u))%P
     got[k]=(polyval(coarse,x)-local)%P
    d=block(q,ell);curs[ell]=[(curs[ell][r]+d[r])%P for r in range(R)]
  assert got==ref
  # All Q offset extensions, arithmetic grids over ell at each fixed u.
  for u in range(K):
   ds=[]
   for ell in range(M):
    t=u+ell*K; jj=a*t%Q; kk=(2*N*jj+Q)//(2*Q); ds.append(Q*kk-N*jj)
   ds.sort();assert all(ds[i+1]-ds[i]==K for i in range(M-1))
  bc.append({'N':N,'Q':Q,'K':K,'M':M,'R':R,'B':B,'a':a,'beta':beta,'outputs_exactly_equal':N})
results['blocked_prefix_controls']=bc
# Numerical operator identity and generating-function collapse, fresh mpmath matrices.
mp.mp.dps=70
nc=[]
for K in [4,8,12]:
 U=mp.matrix([[mp.exp(-2j*mp.pi*k*b/K)/mp.sqrt(K)for b in range(K)]for k in range(K)])
 G=mp.matrix([mp.mpc(rng.randrange(-9,10),rng.randrange(-9,10))/11 for _ in range(K)])
 H=U*mp.diag([0]+[mp.mpf(1)/b for b in range(1,K)])*U.conjugate().transpose()
 Ys=[U*mp.matrix([mp.besselj(r,mp.pi*b/K)*G[b]for b in range(K)])for r in range(7)]
 err=mp.mpf(0)
 for r in range(1,6):
  y=2*r*K/mp.pi*H*Ys[r]-Ys[r-1]
  if r==1:y+=mp.matrix([G[0]/mp.sqrt(K)]*K)
  err=max(err,max(abs(y[k]-Ys[r+1][k])for k in range(K)))
 ge=mp.mpf(0)
 for w in [mp.mpf('-0.9'),mp.mpf('0.13'),mp.mpf('0.8')]:
  ys=[U*mp.matrix([mp.besselj(r,mp.pi*b/K)*G[b]for b in range(K)])for r in range(64)]
  merged=ys[0]+sum((2*(-1j)**r*mp.chebyt(r,w)*ys[r]for r in range(1,64)),mp.matrix(K,1))
  exact=U*mp.matrix([mp.exp(-1j*mp.pi*w*b/K)*G[b]for b in range(K)])
  ge=max(ge,max(abs(merged[k]-exact[k])for k in range(K)))
 assert err<mp.mpf('1e-60') and ge<mp.mpf('1e-65')
 nc.append({'K':K,'cycle_error':str(err),'generating_function_64_order_error':str(ge),'dps':70})
results['numerical_oracle_controls']=nc
# A rigorous amplification inequality, with independent high-precision finite controls.
amp=[]
for K in [4,16,128,1024]:
 for R in [6,12,24]:
  z=mp.pi/K;e0=mp.mpf(0);e1=mp.mpf(1)
  for r in range(1,R):e0,e1=e1,2*r/z*e1-e0
  lo=mp.factorial(R-1)/z**(R-1);hi=mp.factorial(R-1)*(2/z)**(R-1)
  assert lo<=e1<=hi
  amp.append({'K':K,'R':R,'observed_log2_amplification':str(mp.log(e1,2)),'proved_lower_log2':str(mp.log(lo,2))})
results['forward_seed_error_amplification']=amp
results['all_checks_passed']=True
(OUT/'CHECK_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
