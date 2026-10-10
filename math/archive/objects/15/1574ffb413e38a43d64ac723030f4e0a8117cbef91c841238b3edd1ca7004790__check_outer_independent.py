"""Reviewer-authored reconstruction. Reads only inert JSON layout."""
from pathlib import Path
from fractions import Fraction as Q
import json, math, hashlib
import sys
sys.set_int_max_str_digits(200000)
import numpy as np
HERE=Path(__file__).parent
layout=json.loads((HERE/'outer_source/AFFINE_LAYOUT.json').read_text())
N=256
ps=[]
for cols in layout['affine_shuffle_columns']:
 a=[]
 for i in range(N):
  z=0
  for j,c in enumerate(cols):
   if (i>>j)&1:z^=c
  a.append(z)
 assert sorted(a)==list(range(N));ps.append(np.array(a,dtype=np.int64))
p1,p2,p3=ps;ip3=np.argsort(p3)
def rd(a,p):
 a=np.array(a,dtype=np.int64).copy()%p;r=0;det=1
 for c in range(a.shape[1]):
  cand=np.flatnonzero(a[r:,c])
  if not len(cand):continue
  t=r+int(cand[0])
  if t!=r:a[[r,t]]=a[[t,r]];det=-det
  v=int(a[r,c]);det=det*v%p
  a[r,c:]=a[r,c:]*pow(v,-1,p)%p
  a[r+1:,c:]=(a[r+1:,c:]-a[r+1:,c,None]*a[r,None,c:])%p
  r+=1
  if r==a.shape[0]:break
 return r,det%p if r==a.shape[0]==a.shape[1] else None
cuts=[]
for m in range(1,N):
 g=np.array([(i&m).bit_count()%2==0 for i in range(N)])
 a=int(np.sum(g[1:]!=g[:-1])); h=g[p2];b=int(np.sum(h[1:]!=h[:-1]))
 if a+b>=128:continue
 R=np.flatnonzero(~h);C=np.flatnonzero(g);rows=ip3[R];cols=p1[C]
 record=dict(mask=m,dg=a,dgp2=b,budget=a+b,rows=rows.tolist(),cols=cols.tolist(),ranks=[],determinants=[])
 for p,w in [(12289,8340),(65537,282)]:
  assert pow(w,256,p)==1 and pow(w,128,p)==p-1
  roots=np.array([pow(w,i,p) for i in range(N)],dtype=np.int64)
  rank,det=rd(roots[(rows[:,None]*cols[None,:])%N],p)
  assert rank==128 and det;record['ranks'].append(rank);record['determinants'].append(det)
 cuts.append(record)
assert len(cuts)==32
assert [(x['mask'],x['budget']) for x in sorted(cuts,key=lambda x:x['budget'])[:7]]==[(64,16),(168,47),(156,49),(128,52),(232,53),(220,59),(40,61)]
c=next(x for x in cuts if x['mask']==64)
def differences(vals):
 out=[0]*256
 for x in vals:
  for y in vals:out[(x-y)%256]+=1
 assert sum(out)==128**2
 return out
A=differences(c['rows']);B=differences(c['cols']);raw=[0]*256
for d in range(256):
 for e in range(256):raw[(d*e)%256]+=A[d]*B[e]
a=[raw[k]-raw[k+128] for k in range(128)]
assert a[64]==0 and all(a[128-k]==-a[k] for k in range(1,64))
# Arctangent alternating-series enclosure. Adjacent partial sums bracket exact value.
def atan_bounds(inv,terms=32):
 s=sum((Q((-1)**k,(2*k+1)*inv**(2*k+1)) for k in range(terms)),Q(0))
 t=s+Q((-1)**terms,(2*terms+1)*inv**(2*terms+1))
 return min(s,t),max(s,t)
l5,u5=atan_bounds(5);l239,u239=atan_bounds(239)
pi_lo=16*l5-4*u239;pi_hi=16*u5-4*l239
assert Q(314159,100000)<pi_lo<pi_hi<Q(314160,100000)
def cos_bounds(k):
 lo=pi_lo*k/128;hi=pi_hi*k/128;mid=(lo+hi)/2
 # Taylor polynomial through degree 48; degree-49 Lagrange remainder <= x^49/49!.
 s=sum(((-1)**j*mid**(2*j)/math.factorial(2*j) for j in range(25)),Q(0))
 error=abs(mid)**49/math.factorial(49)+(hi-lo)/2
 return s-error,s+error
lo=hi=Q(a[0])
for k in range(1,64):
 l,u=cos_bounds(k);v=2*a[k]
 lo+=v*(l if v>=0 else u);hi+=v*(u if v>=0 else l)
lo/=65536;hi/=65536
assert lo>Q(1264,25)
# Small readable enclosing rationals, verified by exact cross multiplication.
short_lo=Q(5056723058433,10**11);short_hi=Q(5056723058434,10**11)
assert short_lo<lo<hi<short_hi
root=np.exp(2j*np.pi/256)
K=root**(np.array(c['rows'])[:,None]*np.array(c['cols'])[None,:])/16
sv=np.linalg.svd(K,compute_uv=False);numeric_moment=float(np.sum(sv**4))
assert abs(numeric_moment-float(lo))<1e-9
out=dict(status='PASS',source_programs_executed=False,cuts=cuts,cut_count=32,modular_full_rank_certificates=64,moment_coefficients=a,row_difference_counts=A,col_difference_counts=B,pi_bounds=[str(pi_lo),str(pi_hi)],rational_moment_bounds=[str(lo),str(hi)],short_rational_moment_bounds=[str(short_lo),str(short_hi)],moment_threshold=str(Q(1264,25)),lambda17_threshold=str(Q(18,25)),numeric_moment_diagnostic=numeric_moment,numeric_sigma17_diagnostic=float(sv[16]),spectral_threshold='3 sqrt(2)/5',epsilon_threshold='sqrt(1+3 sqrt(2)/5)-1',unused_toffoli_variant=True)
(HERE/'OUTER_INDEPENDENT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS 32 cuts, 64 exact ranks; moment in',str(short_lo),str(short_hi),'sigma17 diagnostic',sv[16])
