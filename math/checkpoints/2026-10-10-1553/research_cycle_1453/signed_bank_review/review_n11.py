#!/usr/bin/env python3
"""Independent exact audit. Reads inert JSON only; no author program import/execution.
Arithmetic library: SymPy's algebraic-number domain. Every problem formula is
reconstructed from the permitted bank definition and the displayed construction.
"""
from pathlib import Path
import hashlib,json,time
from sympy import Symbol, cyclotomic_poly
from sympy.polys.domains import QQ

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
SRC=OUT/'sources'
t0=time.time()
x=Symbol('x'); qsym=Symbol('q')
K=QQ.algebraic_field((cyclotomic_poly(11,x),qsym))
Z,O,q=K.zero,K.one,K.unit
qp=[q**i for i in range(11)]
def cv(a): return K.convert(QQ(str(a)))
def parse(v): return sum((cv(c)*qp[i] for i,c in enumerate(v)),Z)
def serial(v):
 a=list(reversed(v.to_list())); return [str(c) for c in a]+['0']*(10-len(a))
def md(a,p=23):
 return sum((int(c.numerator)*pow(int(c.denominator),-1,p)*pow(2,i,p) for i,c in enumerate(reversed(a.to_list()))))%p
W=json.loads((SRC/'N11_EXACT_WITNESS.json').read_text())
MC=json.loads((SRC/'N11_MODULAR_CERTIFICATE.json').read_text())
# Rebuild Gaussian coefficients with Pascal recurrence (no division formula).
G={}
for s in (1,-1):
 for n in range(11):
  for l in range(n+1):
   G[s,n,l]=O if l in (0,n) else G[s,n-1,l-1]+qp[(s*l)%11]*G[s,n-1,l]
def gaussian(e,d,a,b):
 r=e*a%11; l=d*b%11
 return G[e*d,r+l,l] if r+l<=10 else Z
def f(a,b): return qp[(3*(a+b)**2)%11]
H=f(1,1)/gaussian(1,1,1,1)
T=f(9,2)/gaussian(-1,1,9,2)
m=[(f(a,1)-H*gaussian(-1,1,a,1))/(H*gaussian(1,1,a,1)) for a in range(1,10)]
n=[(f(a,2)-T*gaussian(-1,1,a,2))/gaussian(1,1,a,2) for a in range(2,9)]
assert [serial(v) for v in m]==W['moment_one']
assert [serial(v) for v in n]==W['moment_two']
assert serial(H)==W['H'] and serial(T)==W['T']
A=[m[s:s+4] for s in range(3)]+[n[:4]]
rhs=[-m[6],-m[7],-m[8],-n[6]]
assert [[serial(v) for v in row] for row in A]==W['coefficient_matrix']
assert [serial(v) for v in rhs]==W['coefficient_rhs']
def solve(A,b):
 a=[row[:]+[v] for row,v in zip(A,b)]; N=len(a)
 for i in range(N):
  h=next(j for j in range(i,N) if a[j][i]); a[i],a[h]=a[h],a[i]
  inv=O/a[i][i]; a[i]=[v*inv for v in a[i]]
  for j in range(N):
   if i!=j and a[j][i]:
    z=a[j][i]; a[j]=[u-z*v for u,v in zip(a[j],a[i])]
 return [row[-1] for row in a]
g=solve(A,rhs)+[Z,Z,O]
assert [serial(v) for v in g]==W['g_ascending']
assert g[0]
# Independent polynomial remainder arithmetic in t over K.
def trim(a):
 a=a[:]
 while len(a)>1 and not a[-1]: a.pop()
 return a
def padd(a,b): return trim([(a[i] if i<len(a) else Z)+(b[i] if i<len(b) else Z) for i in range(max(len(a),len(b)))])
def pscale(a,c): return trim([z*c for z in a])
def pmul(a,b):
 c=[Z]*(len(a)+len(b)-1)
 for i,u in enumerate(a):
  for j,v in enumerate(b):
   if u and v: c[i+j]+=u*v
 return trim(c)
def prem(a,div=g):
 a=trim(a)
 while len(a)>=len(div):
  s=len(a)-len(div); c=a[-1]/div[-1]
  for j,z in enumerate(div): a[s+j]-=c*z
  a=trim(a)
 return a
powers=[]
for r in range(17):
 a=prem([Z]*r+[O]); powers.append(a+[Z]*(6-len(a)))
def evalmoment(v,r): return sum((u*k for u,k in zip(powers[r],v)),Z)
# The row matrices use shared nodes, independent moments in each sector.
M={}
for b in range(11):
 M[b]=[]
 for a in range(11):
  M[b].append([gaussian(1,1,a,b)*u for u in powers[a]]+[gaussian(-1,1,a,b),gaussian(1,-1,a,b)]+[gaussian(-1,-1,a,b)*u for u in powers[-a%11]])
rows={int(b):[parse(v) for v in z] for b,z in W['row_vectors'].items()}
checks={b:[sum((u*v for u,v in zip(row,rows[b])),Z)==f(a,b) for a,row in enumerate(M[b])] for b in range(11)}
assert all(all(v) for v in checks.values())
# Independently rebuild the displayed row recipes and chosen square solves.
built={}
k0=-H*(m[5]+sum((g[k]*m[k-1] for k in range(1,6)),Z))/g[0]
built[1]=[k0]+[H*m[k-1] for k in range(1,6)]+[H,f(0,1)-k0-H]+[Z]*6
l1=-(n[5]+sum((g[k]*n[k-1] for k in range(1,6)),Z))/g[0]
l0=-(n[4]+g[1]*l1+sum((g[k]*n[k-2] for k in range(2,6)),Z))/g[0]
p=(f(1,2)-gaussian(1,1,1,2)*l1)/gaussian(1,-1,1,2)
q1=(f(10,2)-T*gaussian(-1,1,10,2))/gaussian(-1,-1,10,2)
q0=f(0,2)-l0-T-p
built[2]=[l0,l1]+n[:4]+[T,p,q0,q1]+[Z]*4
for b in [0,3,4,5]:
 cols=MC['full_row_minors'][str(b)]['columns']
 sol=solve([[row[j] for j in cols] for row in M[b]],[f(a,b) for a in range(11)])
 built[b]=[Z]*14
 for j,v in zip(cols,sol):built[b][j]=v
for b in range(1,6):
 z=built[b];built[11-b]=z[8:]+[z[7],z[6]]+z[:6]
assert built==rows
print('All eleven displayed row recipes match the literal witness.',flush=True)
# Direct exact Fourier trace extraction, independent of Gaussian factors.
C=sum((qp[(-j*j)%11] for j in range(11)),Z)/cv(11)
assert C and serial(C)==W['C']
trace_checks=[]
for a in range(11):
 for b in range(11):
  extracted=sum((qp[(-b*t-(t+a)*t)%11] for t in range(11)),Z)/cv(11)
  trace_checks.append(extracted==C*f(a,b))
assert all(trace_checks)
print('Exact sextic, all 121 row equations, and 121 target trace coefficients passed.',flush=True)
# Modular linear algebra written here, including exact determinant and rank.
def detmod(A):
 a=[[z%23 for z in row] for row in A]; ans=1
 for i in range(len(a)):
  h=next((j for j in range(i,len(a)) if a[j][i]),None)
  if h is None:return 0
  if h!=i:a[i],a[h]=a[h],a[i];ans=-ans
  d=a[i][i];ans=ans*d%23
  for j in range(i+1,len(a)):
   s=a[j][i]*pow(d,-1,23)%23
   a[j]=[(u-s*v)%23 for u,v in zip(a[j],a[i])]
 return ans%23
def rankmod(A):
 a=[[z%23 for z in row] for row in A]; i=0
 for c in range(len(a[0])):
  h=next((j for j in range(i,len(a)) if a[j][c]),None)
  if h is None:continue
  a[i],a[h]=a[h],a[i];d=pow(a[i][c],-1,23);a[i]=[z*d%23 for z in a[i]]
  for j in range(i+1,len(a)):
   s=a[j][c];a[j]=[(u-s*v)%23 for u,v in zip(a[j],a[i])]
  i+=1
  if i==len(a):break
 return i
Ag=[[md(z) for z in row] for row in A]
mg=[md(z) for z in g]
assert detmod(Ag)==1 and mg==[12,21,2,4,0,0,1]
# Sylvester determinant of g,g' rebuilt with shifts in descending order.
gd=[mg[i]*i%23 for i in range(1,7)]
syl=[]
for k in range(5):syl.append([0]*k+mg[::-1]+[0]*(4-k))
for k in range(6):syl.append([0]*k+gd[::-1]+[0]*(5-k))
res=detmod(syl); assert res==6
assert pow(2,11,23)==1 and all(pow(2,i,23)!=1 for i in range(1,11))
modmat={b:[[md(v) for v in row] for row in A] for b,A in M.items()}
modranks=[rankmod(modmat[b]) for b in range(11)]
augranks=[rankmod([r+[md(f(a,b))] for a,r in enumerate(modmat[b])]) for b in range(11)]
assert modranks==augranks==[11,8,10,11,11,11,11,11,11,10,8]
minors={}
for b,record in MC['full_row_minors'].items():
 cols=record['columns'];d=detmod([[r[i] for i in cols] for r in modmat[int(b)]])
 assert d and d==record['determinant'];minors[b]={'columns':cols,'determinant':d}
assert modmat=={int(b):A for b,A in MC['matrices'].items()}
# Good reduction is defined on a local ring: every literal coefficient is integral there.
assert all(int(c.denominator)%23 for z in g for c in z.to_list())
# Restricted depressed-quintic obstruction, not a universal twelve-bank claim.
A5=[m[r:r+4] for r in range(4)]
d5=solve(A5,[-m[r+5] for r in range(4)])
fail5=[n[r+5]+sum((d5[k]*n[r+k] for k in range(4)),Z) for r in range(2)]
assert detmod([[md(v) for v in row] for row in A5])==20
assert [md(v) for v in d5]+[0,1]==[10,1,4,8,0,1]
assert [md(v) for v in fail5]==[21,17]
assert [serial(v) for v in d5+[Z,O]]==W['restricted_quintic_ascending']
assert [serial(v) for v in fail5]==W['restricted_quintic_row_two_residuals']
result={'status':'all_passed','independence':'Fresh reviewer code; author mathematics and inert JSON only. No author program read, imported, executed, or compiled.', 'N':11,'banks_upper_bound':14,'orientation_counts':[6,1,1,6], 'all_eleven_recipes_match_witness':True,'restricted_depressed_quintic':{'determinant_mod23':20,'polynomial_ascending_mod23':[10,1,4,8,0,1],'incompatibilities_mod23':[21,17],'not_a_universal_lower_bound':True},'all_121_exact_row_checks':checks,'all_121_direct_fourier_trace_checks':all(trace_checks),'exact_g_ascending':[serial(v) for v in g], 'mod23_coefficient_determinant':1,'mod23_g':mg,'mod23_sylvester_resultant':res,'mod23_full_row_minors':minors,'mod23_row_ranks':modranks,'mod23_augmented_ranks':augranks,'elapsed_seconds':time.time()-t0}
(OUT/'EXACT_REVIEW_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print('Good-reduction coefficient system, resultant, all matrices, ranks and selected minors passed.',flush=True)
# Save all original source hashes read; mathematical draft added by report finalization.
hashes={str(p.relative_to(OUT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(SRC.rglob('*')) if p.is_file()}
(OUT/'REVIEWED_SOURCE_HASHES.json').write_text(json.dumps(hashes,indent=2)+'\n')
print('Seconds:',time.time()-t0,flush=True)
