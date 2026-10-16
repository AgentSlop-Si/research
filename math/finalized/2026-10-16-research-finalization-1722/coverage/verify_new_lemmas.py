"""Fresh diagnostic controls for two bounded matrix lemmas; no source code imported.
The written proofs, not these finite checks, establish the universal claims.
"""
import json
from fractions import Fraction
from pathlib import Path
import numpy as np

def rank_mod(A,p):
 a=[list(map(lambda x:int(x)%p,row)) for row in A];m=len(a);n=len(a[0]);r=0
 for j in range(n):
  z=next((i for i in range(r,m) if a[i][j]),None)
  if z is None:continue
  a[r],a[z]=a[z],a[r];w=pow(a[r][j],-1,p);a[r]=[(v*w)%p for v in a[r]]
  for i in range(m):
   if i!=r and a[i][j]:
    w=a[i][j];a[i]=[(x-w*y)%p for x,y in zip(a[i],a[r])]
  r+=1
  if r==m:break
 return r

def mm(A,B,p):return [[sum(x*y for x,y in zip(a,b))%p for b in zip(*B)] for a in A]
def sub(A,B,g,p):return [[(x-g*y)%p for x,y in zip(a,b)] for a,b in zip(A,B)]

p=65537
assert pow(3,(p-1)//2,p)==p-1
fold=[]
for a,b in [(1,1),(2,1),(2,2),(4,2),(4,4),(8,4)]:
 N=a*b;w=pow(3,(p-1)//(4*N),p);z=pow(w,4,p)
 FL=[[pow(w,i*j,p) for j in range(4*N)] for i in range(4*N)]
 FS=[[pow(z,i*j,p) for j in range(N)] for i in range(N)]
 Q=[[0]*(4*N) for _ in range(N)]
 for X in range(2*a):
  for Y in range(2*b):Q[b*(X%a)+(Y%b)][2*b*X+Y]=1
 for r in range(min(2,N)+1):
  # Deterministic rank-r fold change, with r explicit independent columns.
  E=[[0]*(4*N) for _ in range(N)]
  for j in range(r):
   for i in range(N):E[i][j]=pow(i+1,j,p)
  er=rank_mod(E,p);assert er==r
  Qp=[[x+y for x,y in zip(q,e)] for q,e in zip(Q,E)]
  for g in [0,1,2,7]:
   D=sub(mm(Qp,FL,p),mm(FS,Qp,p),g,p)
   got=rank_mod(D,p);bound=max(0,N-(1 if g==0 else 2)*r)
   assert got>=bound
   fold.append({'a':a,'b':b,'N':N,'rank_delta':r,'gamma':g,'rank_defect':got,'lower_bound':bound})

# Disjoint normal spectra and invertible X do not force full-rank AX-XB.
A=[[1,0],[0,2]];B=[[3,0],[0,4]];X=[[3,2],[2,1]]
D=sub(mm(A,X,p),mm(X,B,p),1,p)
assert rank_mod(X,p)==2 and rank_mod(D,p)==1

rng=np.random.default_rng(20261016)
def build_target(M,cut,k):
 B=M[:cut,cut:];C=M[cut:,:cut]
 ub,sb,vb=np.linalg.svd(B,full_matrices=False)
 uc,sc,vc=np.linalg.svd(C,full_matrices=False)
 LB=np.zeros((cut,k),complex); RB=np.zeros((k,M.shape[0]-cut),complex)
 LC=np.zeros((M.shape[0]-cut,k),complex);RC=np.zeros((k,cut),complex)
 kb=min(k,len(sb));kc=min(k,len(sc))
 LB[:,:kb]=ub[:,:kb]*sb[:kb];RB[:kb,:]=vb[:kb,:]
 LC[:,:kc]=uc[:,:kc]*sc[:kc];RC[:kc,:]=vc[:kc,:]
 E=np.vstack([LB,LC])@np.hstack([RC,RB])
 T0=M-E;T0[:cut,cut:]=0;T0[cut:,:cut]=0
 R=M-(T0+E)
 op=max(sb[k] if k<len(sb) else 0,sc[k] if k<len(sc) else 0)
 frob=np.sqrt(sum(sb[k:]**2)+sum(sc[k:]**2))
 assert np.linalg.matrix_rank(E,tol=1e-8)<=k
 assert abs(np.linalg.norm(R,2)-op)<1e-8
 assert abs(np.linalg.norm(R,'fro')-frob)<1e-8
 return op,frob,sb,sc

generic=0
for n in range(2,10):
 for cut in range(1,n):
  M=rng.standard_normal((n,n))+1j*rng.standard_normal((n,n))
  for k in range(min(cut,n-cut)+2):build_target(M,cut,k);generic+=1

fourier=[]
for s in [2,4,6,8]:
 N=s*s;U=np.exp(2j*np.pi*np.outer(np.arange(N),np.arange(N))/N)/np.sqrt(N)
 for kind in ['x','y','xy']:
  def invol(j):
   x,y=divmod(j,s)
   return ((x+(s//2 if kind in ['x','xy'] else 0))%s)*s+(y+(s//2 if kind in ['y','xy'] else 0))%s
  plus=[];minus=[];seen=set()
  for j in range(N):
   if j in seen:continue
   jj=invol(j);seen.update([j,jj]);vp=np.zeros(N);vm=np.zeros(N)
   vp[j]=vp[jj]=1/np.sqrt(2);vm[j]=1/np.sqrt(2);vm[jj]=-1/np.sqrt(2)
   plus.append(vp);minus.append(vm)
  W=np.array(plus+minus).T;M=W.T@U@W;n=N//2;h=N//4
  expected=np.array(([1]*h+[0]*h) if kind=='x' else ([np.cos(np.pi/8)]*h+[np.sin(np.pi/8)]*h))
  for k in range(n+1):
   op,fr,sb,sc=build_target(M,n,k)
   assert np.max(np.abs(sb-expected))<1e-8 and np.max(np.abs(sc-expected))<1e-8
   expected_op=expected[k] if k<n else 0
   expected_fr=np.sqrt(2*np.sum(expected[k:]**2))
   assert abs(op-expected_op)<1e-8 and abs(fr-expected_fr)<1e-8
   fourier.append({'side':s,'N':N,'involution':kind,'k':k,'spectral_distance':float(op),'relative_frobenius':float(fr/np.sqrt(N))})

out={'scope':'Diagnostic controls only; universal results follow from written proofs. No uploaded or archived code executed.', 'fold_exact_field':p,'fold_cases':fold,'sylvester_counterexample':{'A':A,'B':B,'X':X,'D':[[int(v if v<p//2 else v-p) for v in row] for row in D],'rank_X':2,'rank_D':1},'generic_complex_completion_cases':generic,'fourier_numeric_cases':fourier,'count_fold':len(fold),'count_fourier':len(fourier),'status':'PASS'}
Path(__file__).with_name('CONTROL_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','count_fold','generic_complex_completion_cases','count_fourier']}))
