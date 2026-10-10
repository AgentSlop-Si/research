#!/usr/bin/env python3
"""Fresh reviewer implementation; no uploaded modules or data are imported."""
import random,json,math
from pathlib import Path
from collections import Counter
rng=random.Random(3818);counts=Counter();profiles=[]
class Field:
 def __init__(self,p,N):
  self.p=p;self.N=N;self.w=pow(3,(p-1)//N,p);assert pow(self.w,N,p)==1 and pow(self.w,N//2,p)!=1
  self.roots=[1]
  for j in range(1,N):self.roots.append(self.roots[-1]*self.w%p)
 def fft(self,x,inverse=False):
  n=len(x);a=list(x);j=0;p=self.p
  for i in range(1,n):
   bit=n//2
   while j&bit:j^=bit;bit//=2
   j^=bit
   if i<j:a[i],a[j]=a[j],a[i]
  m=2
  while m<=n:
   for start in range(0,n,m):
    for k in range(m//2):
     t=a[start+k+m//2]*self.roots[((-1 if inverse else 1)*self.N//m*k)%self.N]%p
     u=a[start+k];a[start+k]=(u+t)%p;a[start+k+m//2]=(u-t)%p
   m*=2
  return a
 def pruned(self,n,items,inverse=False):
  stat=Counter();items={j:v%self.p for j,v in items.items() if v%self.p};s=len(items)
  def rec(L,rows):
   stat['allocated']+=L
   if not rows:return [0]*L
   if L==1:return [rows[0][1]]
   even=[];odd=[]
   for j,v in rows:(odd if j&1 else even).append((j//2,v));stat['partition']+=1
   a=rec(L//2,even);b=rec(L//2,odd);out=[0]*L
   for k in range(L//2):
    t=b[k]*self.roots[((-1 if inverse else 1)*self.N//L*k)%self.N]%self.p
    out[k]=(a[k]+t)%self.p;out[k+L//2]=(a[k]-t)%self.p;stat['field']+=3
   return out
  ans=rec(n,list(items.items()));scale=n*(1+math.ceil(math.log2(s+1)))
  assert stat['field']<=6*scale and stat['allocated']<=6*scale and stat['partition']<=4*scale
  counts['pruned_calls']+=1;return ans

def bm(seq,p):
 C=[1];B=[1];L=0;m=1;b=1
 for n,s in enumerate(seq):
  d=(s+sum(C[j]*seq[n-j] for j in range(1,len(C))))%p
  if not d:m+=1;continue
  T=C[:];coef=d*pow(b,-1,p)%p;C += [0]*max(0,len(B)+m-len(C))
  for j,x in enumerate(B):C[j+m]=(C[j+m]-coef*x)%p
  if 2*L<=n:L=n+1-L;B=T;b=d;m=1
  else:m+=1
 return L,C+[0]*max(0,L+1-len(C))
def horner(a,x,p):
 v=0
 for c in reversed(a):v=(v*x+c)%p
 return v
def recover(y,b,f):
 M=len(y);p=f.p;L,C=bm(y[:2*b],p)
 if L>b:return None
 if L==0:return {} if not any(y) else None
 if not C[L]:return None
 vals=f.pruned(M,{i:v for i,v in enumerate(C)});H=[i for i,v in enumerate(vals) if not v]
 if len(H)!=L:return None
 A=[sum(C[j]*y[u-j] for j in range(u+1))%p for u in range(L)]
 der=[(j*C[j])%p for j in range(1,L+1)];amps={}
 for h in H:
  zh=f.roots[h*f.N//M];lam=f.roots[(-h*f.N//M)%f.N];den=horner(der,zh,p)
  if not den:return None
  amp=-lam*horner(A,zh,p)*pow(den,-1,p)%p
  if not amp:return None
  amps[h]=amp
 if f.pruned(M,amps,True)!=y:return None
 return amps
def synth(modes,Q,M,f):
 byh=[{} for h in range(M)]
 for t,amps in enumerate(modes):
  for h,a in amps.items():byh[h][t]=a*f.roots[h*t%f.N]%f.p
 out=[0]*f.N
 for h,entries in enumerate(byh):
  for v,x in enumerate(f.pruned(Q,entries)):out[h+M*v]=M*x%f.p
 return out
def run(x,f,b=None,K0=None):
 N=f.N;Q=1<<((N.bit_length()-1)//2);M=N//Q;modes=[];total=0;heavy=0
 B=b if K0 is None else min(M//2,max(1,(K0+Q-1)//Q)*(M.bit_length()-1))
 for t in range(Q):
  y=x[t::Q];a=recover(y,B,f)
  if a is None:
   if K0 is None:return None,{'heavy':0,'discovered':total}
   heavy+=1;vals=f.fft(y);a={h:v*pow(M,-1,f.p)%f.p for h,v in enumerate(vals) if v};assert len(a)>B
  modes.append(a);total+=len(a)
  if K0 is not None and total>K0:
   assert heavy<=K0//(B+1)+1
   return None,{'heavy':heavy,'discovered':total,'B':B}
 if K0 is not None:assert heavy<=K0//(B+1)
 return synth(modes,Q,M,f),{'heavy':heavy,'discovered':total,'B':B}
def from_modes(modes,Q,M,f):
 x=[0]*f.N
 for t,a in enumerate(modes):
  for u in range(M):x[t+Q*u]=sum(v*f.roots[(-h*u*f.N//M)%f.N] for h,v in a.items())%f.p
 return x
def support(x,f):
 Q=1<<((f.N.bit_length()-1)//2)
 return [sum(v!=0 for v in f.fft(x[t::Q])) for t in range(Q)]
def check(x,f,b=None,K0=None):
 out,meta=run(x,f,b,K0);r=support(x,f);expected=max(r)<=b if K0 is None else sum(r)<=K0
 assert (out is not None)==expected
 if out is not None:assert out==f.fft(x);counts['accepted']+=1;counts['output_entries']+=f.N
 else:counts['rejected']+=1
 counts['recognition_cases']+=1;counts['heavy_fallbacks']+=meta['heavy'];return out,meta
for p in [65537,998244353]:
 for N in [4,8,16,32,64,128]:
  f=Field(p,N)
  for trial in range(10):
   n=1<<rng.randrange(0,N.bit_length());s=rng.randrange(n+1);a={j:rng.randrange(1,p) for j in rng.sample(range(n),s)};x=[a.get(j,0) for j in range(n)]
   for inv in [False,True]:
    y=f.pruned(n,a,inv);assert y==f.fft(x,inv)
    direct=[sum(x[j]*f.roots[((-1 if inv else 1)*j*k*f.N//n)%f.N] for j in range(n))%p for k in range(n)]
    assert y==direct;counts['pruning_direct_cases']+=1
for p in [65537,998244353]:
 for N in [4,8,16,32,64]:
  f=Field(p,N);Q=1<<((N.bit_length()-1)//2);M=N//Q
  for j in range(N):
   x=[int(i==j) for i in range(N)];check(x,f,b=max(1,M//4));check(x,f,K0=M);check(x,f,K0=M-1)
  for b in sorted(set([1,M//4 or 1,M//2])):
   for trial in range(6):
    modes=[{h:rng.randrange(1,p) for h in rng.sample(range(M),rng.randrange(b+1))} for t in range(Q)]
    x=from_modes(modes,Q,M,f);out,_=check(x,f,b=b);assert out is not None;k=sum(map(len,modes));check(x,f,K0=k)
    if k:check(x,f,K0=k-1)
    if 2*b<M:x[-1]=(x[-1]+1)%p;check(x,f,b=b);counts['late_corruption']+=1
  check([0]*N,f,K0=0);check([rng.randrange(p) for _ in range(N)],f,b=M//2);check([rng.randrange(p) for _ in range(N)],f,K0=Q)
def rank(A,p):
 A=[r[:] for r in A];j=0
 for c in range(len(A[0])):
  k=next((k for k in range(j,len(A)) if A[k][c]),None)
  if k is None:continue
  A[j],A[k]=A[k],A[j];z=pow(A[j][c],-1,p);A[j]=[v*z%p for v in A[j]]
  for k in range(j+1,len(A)):
   z=A[k][c];A[k]=[(a-z*b)%p for a,b in zip(A[k],A[j])]
  j+=1
 return j
for N in [256,512,1024,2048,4096,16384]:
 f=Field(65537,N);Q=1<<((N.bit_length()-1)//2);M=N//Q
 for b in sorted(set([2,min(M//2,N.bit_length()),M//2])):
  modes=[{h:rng.randrange(1,f.p) for h in rng.sample(range(M),b)} for t in range(Q)];x=from_modes(modes,Q,M,f);check(x,f,b=b);check(x,f,K0=Q*b)
 modes=[{h:rng.randrange(1,f.p) for h in (range(M) if t==0 else [t%M,(t+1)%M])} for t in range(Q)]
 x=from_modes(modes,Q,M,f);K=sum(map(len,modes));_,meta=check(x,f,K0=K);check(x,f,K0=K-1);check(x,f,K0=0);profiles.append({'N':N,'K0':K,**meta})
 if Q==M:
  b=min(7,M-1);modes=[{(t+j)%M:(2*b if j==0 else 1) for j in range(b)} for t in range(Q)];x=from_modes(modes,Q,M,f);y,_=check(x,f,b=b)
  if all(x) and all(y):assert rank([x[t::Q] for t in range(Q)],f.p)==M;counts['dense_full_rank_controls']+=1
f=Field(65537,16)
for diagonal in [4,5]:
 modes=[{t:diagonal,(t+1)%4:1} for t in range(4)];x=from_modes(modes,4,4,f);y,_=check(x,f,b=2);assert all(y)==(diagonal==5)
def cyclic_solve(x,diag,beta,p):
 inv=[pow(v,-1,p) for v in diag];a=[-beta*v%p for v in inv];b=[xj*v%p for xj,v in zip(x,inv)];aa=1;bb=0
 for aj,bj in zip(a,b):aa=aj*aa%p;bb=(aj*bb+bj)%p
 assert (1-aa)%p
 prev=bb*pow(1-aa,-1,p)%p;out=[]
 for aj,bj in zip(a,b):prev=(aj*prev+bj)%p;out.append(prev)
 return out
for N in [8,16,32,64,128,256,512]:
 f=Field(65537,N);Q=1<<((N.bit_length()-1)//2);M=N//Q;modes=[{h:rng.randrange(1,f.p) for h in rng.sample(range(M),2)} for t in range(Q)]
 residual=from_modes(modes,Q,M,f);pd=[(7+2*f.roots[-j%N])%f.p for j in range(N)];ld=[(7+f.roots[j])%f.p for j in range(N)]
 try:x=cyclic_solve(residual,pd,1,f.p)
 except (ValueError,AssertionError):counts['guard_rejection']+=1;continue
 assert [(pd[j]*x[j]+x[j-1])%f.p for j in range(N)]==residual
 out,_=check(residual,f,b=2);y=cyclic_solve(out,ld,2,f.p);assert y==f.fft(x);counts['green_cases']+=1;counts['green_output_entries']+=N
Path('INDEPENDENT_RESULTS.json').write_text(json.dumps({'status':'PASS','counts':dict(counts),'aggregate_profiles':profiles,'execution':'reviewer-authored only','source_performance_counts_reproduced':False},indent=2,sort_keys=True)+'\n')
print(json.dumps(dict(counts),sort_keys=True))
