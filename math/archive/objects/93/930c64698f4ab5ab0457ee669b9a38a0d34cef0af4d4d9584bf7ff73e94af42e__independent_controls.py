"""Fresh reviewer mathematics only. Never import/evaluate supplied source text."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json

def eye(n):return [[Q(i==j) for j in range(n)] for i in range(n)]
def plus(a,b):return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def scale(a,c):return [[c*x for x in r] for r in a]
def mul(a,b):return [[sum(x*y for x,y in zip(r,c)) for c in zip(*b)] for r in a]
def inv(a):
 n=len(a);v=[list(map(Q,r))+e for r,e in zip(a,eye(n))]
 for j in range(n):
  z=next(i for i in range(j,n) if v[i][j]);v[j],v[z]=v[z],v[j];q=v[j][j];v[j]=[t/q for t in v[j]]
  for i in range(n):
   if i!=j:
    q=v[i][j];v[i]=[x-q*y for x,y in zip(v[i],v[j])]
 return [r[n:] for r in v]
def norm(a):return max(sum(abs(x) for x in c) for c in zip(*a))
def conv(a,b):return [sum(a[j]*b[(k-j)%len(a)] for j in range(len(a))) for k in range(len(a))]
results=[]
for n in (1,2,3,4,8):
 I=eye(n);C=[[Q(0)]*n for _ in range(n)]
 for j in range(n):C[j][(j+1)%n]=Q(-1 if j==n-1 else 1)
 K=plus(I,inv(plus(I,scale(C,-1))));Ki=inv(K)
 assert norm(K)==Q(n+2,2) and norm(Ki)==Q(2**n,2**n+1)
 results.append({'control':'signed_resolvent_norms','n':n,'norm_K':str(norm(K)),'norm_inverse':str(norm(Ki)),'status':'pass'})
for n in (2,4,8):
 I=eye(n);T=[[Q(3 if i==j else -1 if abs(i-j)==1 else 0) for j in range(n)] for i in range(n)]
 S=plus(inv(T),inv(plus(T,I)));formula=plus(plus(scale(T,Q(1,2)),scale(I,Q(1,4))),scale(inv(plus(T,scale(I,Q(1,2)))),Q(-1,8)))
 assert formula==inv(S)
 results.append({'control':'path_green_inverse_identity','n':n,'status':'pass'})
p=97
for n,q in ((2,96),(4,22),(8,64),(16,8)):
 assert pow(q,n,p)==1 and pow(q,n//2,p)!=1
 x=[(j*j+7*j+11)%p for j in range(n)];X=[sum(x[j]*pow(q,j*k,p) for j in range(n))%p for k in range(n)]
 r=[x[-1]]+[((pow(q,j,p)-1)*x[j]+x[j-1])%p for j in range(1,n)]
 R=[sum(r[j]*pow(q,j*k,p) for j in range(n))%p for k in range(n)]
 assert all((X[(k+1)%n]-(1-pow(q,k,p))*X[k]-R[k])%p==0 for k in range(n))
 results.append({'control':'q_forcing_boundary_identity','n':n,'status':'pass'})
for raw in ([0,1,1,0],[0,-2,-1,2,3,0],[-3,-3,-2,0,1,3,3,0]):
 m=sorted(raw)[len(raw)//2];d=sum(abs(v-m) for v in raw)
 assert d==min(sum(abs(v-c) for v in raw) for c in range(min(raw)-2,max(raw)+3))
 results.append({'control':'cycle_flow_median_optimality','raw':raw,'distance':d,'status':'pass'})
for n in (3,7):
 a=[j-2 for j in range(n)];b=[j*j-3 for j in range(n)];c=[2*j-1 for j in range(n)];d=[j%3 for j in range(n)];I=[1]+[0]*(n-1)
 def F(a,b):return [sum(v) for v in zip(conv(conv(a,a),b),conv(a,b),conv(b,b),conv(c,d))]
 base=F(a,b);aa=conv(a,a);ab=conv(a,b)
 kernels={(0,1):[aa[j]+a[j]+2*b[j] for j in range(n)],(1,0):[2*ab[j]+b[j] for j in range(n)],(1,1):[2*a[j]+I[j] for j in range(n)],(2,0):b,(0,2):I,(2,1):I}
 for pa,pb,alpha,beta in product((0,n-1),(0,n-1),(-2,3),(-1,2)):
  newa=a.copy();newb=b.copy();newa[pa]+=alpha;newb[pb]+=beta
  predicted=[base[j]+sum(alpha**u*beta**v*ker[(j-u*pa-v*pb)%n] for (u,v),ker in kernels.items()) for j in range(n)]
  assert predicted==F(newa,newb)
 results.append({'control':'two_impulse_mixed_polynomial_identity','n':n,'cases':16,'status':'pass'})
# Explicit input-boundary counterexamples, distinct from intended-domain results.
columns=[2];encoded=[0,2];assert len(set(encoded))==2 and sorted(encoded)!=list(range(2))
results.append({'control':'affine_builder_missing_bit_range_guard','columns':columns,'output_by_formula':encoded,'status':'counterexample_confirmed','scope':'invalid descriptor admitted; intended valid GF2 layouts unaffected'})
n=4;raw_offset=-1;cpp_quotient=0;cpp_remainder=raw_offset-cpp_quotient*n;assert cpp_remainder==-1
results.append({'control':'shape_negative_sparse_remainder','n':4,'sparse_position':-1,'pa':0,'pb':0,'derived_cpp_index':cpp_remainder,'status':'counterexample_confirmed','scope':'raw ABI requires canonical nonnegative sparse offsets; no C++ executed'})
local=[Q(100),Q(100)];padded=local+[Q(1),Q(1)];assert max(local)/min(local)==1 and max(padded)/min(padded)==100
results.append({'control':'ambient_padding_condition','local_condition':1,'ambient_condition':100,'status':'counterexample_confirmed','scope':'condition-number padding assumption only'})
obj={'provenance':'Fresh independently authored reviewer arithmetic; no supplied source executed, imported, compiled or AST-parsed. These controls test formulas and scoped counterexamples, not uploaded test pass status.','control_records':len(results),'groups':len({r['control'] for r in results}),'results':results}
Path(__file__).with_name('INDEPENDENT_CONTROLS.json').write_text(json.dumps(obj,indent=2)+'\n');print(json.dumps({'records':len(results),'groups':obj['groups'],'all_checks_completed':True}))
