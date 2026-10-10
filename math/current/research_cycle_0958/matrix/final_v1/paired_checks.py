"""Fresh standard-library reconstruction of paired-layout and moment certificates.
No supplied executable program is read, imported, or executed by this script.
"""
import json, math, hashlib
from fractions import Fraction as Q
from pathlib import Path
O=Path(__file__).resolve().parent;R=O;N=256
D=O/'source_inputs'
cfg=json.loads((D/'AFFINE_LAYOUT.json').read_text())
def shuffle(cols):
 out=[]
 for i in range(N):
  s=0
  for b,c in enumerate(cols):
   if i&(1<<b):s^=c
  out.append(s)
 assert sorted(out)==list(range(N));return out
p1,p2,p3=[shuffle(v) for v in cfg['affine_shuffle_columns']];ip3=[p3.index(i) for i in range(N)]
gates=[]
for mask in range(1,N):
 g=[int((i&mask).bit_count()%2==0) for i in range(N)];gp=[g[p2[i]] for i in range(N)]
 b=sum(g[i]!=g[i-1] for i in range(1,N))+sum(gp[i]!=gp[i-1] for i in range(1,N))
 if b<N//2:gates.append((mask,{i for i in range(N) if not gp[i]},{i for i in range(N) if g[i]},b))
assert len(gates)==32
mask,rows,cols,b=next(x for x in gates if x[0]==64);assert b==16
allset=set(range(N));rc=allset-rows;cc=allset-cols
support={(i,j) for rs,cs in [(rows,cols),(rc,cc)] for i in rs for j in cs};assert len(support)==32768
overlaps=[]
for mask,rs,cs,b in gates:
 for rr,cc1 in [(rs,cs),(allset-rs,allset-cs)]:
  overlap=sum((i,j) in support for i in rr for j in cc1)
  if mask!=64:assert overlap==8192;overlaps.append(overlap);assert max(0,64-b)<=17
assert len(overlaps)==62
R0=sorted(ip3[i] for i in rows);C0=sorted(p1[j] for j in cols)
a=[0]*N;b=[0]*N
for i in R0:
 for j in R0:a[(i-j)%N]+=1
for i in C0:
 for j in C0:b[(i-j)%N]+=1
coef=[0]*128
for d in range(N):
 for e in range(N):
  k=d*e%N;coef[k%128]+=(1 if k<128 else -1)*a[d]*b[e]
old=O/'source_inputs/RATIONAL_MOMENT_CERTIFICATE.json'
assert coef==json.loads(old.read_text())['cyclotomic_reduction_coefficients']
assert coef[64]==0 and all(coef[128-k]==-coef[k] for k in range(1,64))
def atan_interval(q,terms):
 z=Q(1,q);s=sum(((-1)**k*z**(2*k+1)/Q(2*k+1) for k in range(terms)),Q(0));nextterm=(-1)**terms*z**(2*terms+1)/Q(2*terms+1)
 return min(s,s+nextterm),max(s,s+nextterm)
a0,a1=atan_interval(5,40);b0,b1=atan_interval(239,12)
pilo,pihi=16*a0-4*b1,16*a1-4*b0
scale=10**30
pilo=Q((pilo*scale).numerator//(pilo*scale).denominator,scale)
t=pihi*scale;pihi=Q(-((-t.numerator)//t.denominator),scale)
lo=hi=Q(coef[0]);terms=25
for k in range(1,64):
 xl,xh=pilo*k/128,pihi*k/128;x=(xl+xh)/2
 center=sum(((-1)**j*x**(2*j)/math.factorial(2*j) for j in range(terms)),Q(0))
 error=x**(2*terms)/math.factorial(2*terms)+(xh-xl)/2
 cl,ch=center-error,center+error;factor=2*coef[k]
 lo+=factor*(cl if factor>=0 else ch);hi+=factor*(ch if factor>=0 else cl)
lo/=N*N;hi/=N*N
assert lo>Q(1264,25)
def determinant(a,p):
 n=len(a);a=[r[:] for r in a];v=1
 for k in range(n):
  s=next((j for j in range(k,n) if a[j][k]%p),None)
  if s is None:return 0
  if s!=k:a[k],a[s]=a[s],a[k];v=-v
  v=v*a[k][k]%p;inv=pow(a[k][k],-1,p)
  for i in range(k+1,n):
   f=a[i][k]*inv%p
   for j in range(k,n):a[i][j]=(a[i][j]-f*a[k][j])%p
 return v%p
minors=[]
for p in [12289,65537]:
 w=next(pow(x,(p-1)//N,p) for x in range(2,p) if pow(pow(x,(p-1)//N,p),128,p)!=1)
 for name,rr,co in [('A',rows,cols),('D',rc,cc)]:
  rr=sorted(rr)[:17];co=sorted(co)[:17]
  primal=[[pow(w,ip3[i]*p1[j],p)*pow(16,-1,p)%p for j in co] for i in rr]
  dr=sorted(allset-set(cols if name=='A' else cc))[:17];dc=sorted(allset-set(rows if name=='A' else rc))[:17]
  dual=[[pow(w,(-p1[i]*ip3[j])%N,p)*pow(16,-1,p)%p for j in dc] for i in dr]
  dp,dd=determinant(primal,p),determinant(dual,p);assert dp and dd
  minors.append({'prime':p,'primitive_root':w,'block':name,'primal17':dp,'dual17':dd})
out={'status':'PASS','layout_semantics':'Three binary linear permutations from affine_shuffle_columns only; toffoli_gate_sequence_in_shuffle_2 is non-operative metadata in the inherited theorem/verifier. No nonlinear Toffoli-composed case claimed.','layout_sha256':hashlib.sha256((D/'AFFINE_LAYOUT.json').read_bytes()).hexdigest(),'gate_count':32,'paired_gate_count':64,'base_rank_cap':16,'other_overlap_counts':overlaps,'energy_relaxation_minimum':96,'moment_coefficients_match':True,'moment_lower':str(lo),'moment_upper':str(hi),'moment_display_only':[float(lo),float(hi)],'strict_moment_threshold':'1264/25','minors':minors,'exact_scope':'Paired analytic theorem and decisive saved-layout counts/moment reconstructed. Does not rerun every historical 128x128 modular rank or random synthetic generator test.'}
(O/'paired_check_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['moment_lower','moment_upper','other_overlap_counts']},indent=2))
