"""Independent-style exact checker: stdlib only, no certificate generator imports."""
import json,hashlib,itertools,copy
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).parent

def psum(a,b):
 out=dict(a)
 for k,v in b.items():
  out[k]=out.get(k,0)+v
  if not out[k]:out.pop(k)
 return out

def pprod(a,b):
 out={}
 for i,u in a.items():
  for j,v in b.items():
   k=tuple(x+y for x,y in zip(i,j));out[k]=out.get(k,0)+u*v
 return {k:v for k,v in out.items() if v}

def unpack(a):return {tuple(e):Fraction(n,d) for e,n,d in a}
def coefficients(counts):
 one={(0,)*5:Fraction(1)};res=[{} for _ in range(16)];res[0]=one;idx=0
 for stride,count in zip([1,3,7,5],counts):
  group={0:one}
  for k in range(1,count+1):
   ex=[0]*5;ex[idx]=1;idx+=1;group[k*stride]={tuple(ex):Fraction(1)}
  out=[{} for _ in range(16)]
  for i,r in enumerate(res):
   for j,t in group.items():out[(i+j)%16]=psum(out[(i+j)%16],pprod(r,t))
  res=out
 return res

def parity_inputs(counts):
 coeff=coefficients(counts)
 return [psum({e:(-1)**i*v for e,v in coeff[i].items()},{e:-v for e,v in coeff[i+8].items()}) for i in range(8)]
def check_certificate(rec):
 fs=[unpack(v) for v in rec['inputs']];hs=[unpack(v) for v in rec['multipliers']]
 if fs!=parity_inputs(rec['counts']):return False
 total={}
 for f,h in zip(fs,hs):total=psum(total,pprod(f,h))
 return total=={(0,)*5:Fraction(1)}

# Cyclotomic arithmetic: a^N=-1. Coefficients of powers are added directly.
def add_power(v,e,c=1):
 k,r=divmod(e,len(v));v[r]+=c*(-1 if k%2 else 1)
def cmul(u,v):
 w=[0]*len(u)
 for i,a in enumerate(u):
  if a:
   for j,b in enumerate(v):
    if b:add_power(w,i+j,a*b)
 return w

def check_inverse(N,mutate=False):
 # Literal row/column sum in Z[a]/(a^N+1), C_ij=a^(-(i-j)^2).
 for i in range(N):
  for j in range(N):
   r=[0]*N
   for k in range(N):
    coeff=2 if mutate and (k-j)%N==1 else 1
    add_power(r,-((i-k)%N)**2+((k-j)%N)**2,coeff)
   wanted=[0]*N;wanted[0]=N if i==j else 0
   if r!=wanted:return False
 return True

def check_norm(N):
 n=N//2;actual=[[0]*N for _ in range(N)]
 for i in range(N):
  for j in range(N):add_power(actual[(i+j)%N],i*i+j*j,(-1)**j)
 H=[0]*N
 for t in range(N):add_power(H,2*t*t,(-1)**t)
 assert any(H)
 expected=[[0]*N for _ in range(N)]
 for u in range(n):
  mon=[0]*N;add_power(mon,2*u*u,(-1)**u);expected[2*u]=cmul(H,mon)
 return actual==expected

def conv(a,b,p):
 n=len(a);return [sum(a[j]*b[(i-j)%n] for j in range(n))%p for i in range(n)]
def unit_parameter(alpha,stride,N,p):
 import math
 return pow(alpha,N//math.gcd(stride,N),p)!=1

def check_norm_factors(N,p):
 cases=0
 for stride in range(1,N):
  for alpha in range(p):
   if not unit_parameter(alpha,stride,N,p):continue
   b=[0]*N;b[0]=1;b[stride]=(-alpha)%p
   norm=conv(b,[((-1)**i*v)%p for i,v in enumerate(b)],p)
   n=N//2;desc=[0]*n;desc[0]=1
   if stride%2:
    desc[stride%n]=(desc[stride%n]-alpha*alpha)%p
    assert unit_parameter(alpha*alpha%p,stride%n,n,p)
   else:
    desc[stride//2]=(desc[stride//2]-alpha)%p
    assert unit_parameter(alpha,stride//2,n,p)
    desc=conv(desc,desc,p)
   assert norm==[desc[i//2] if i%2==0 else 0 for i in range(N)]
   cases+=1
 return cases

# Ordinary polynomial arithmetic over F17, independent of SymPy.
def trim(f):
 while len(f)>1 and f[-1]==0:f.pop()
 return f
def padd(a,b,p):return trim([( (a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0))%p for i in range(max(len(a),len(b)))])
def pmul(a,b,p):
 out=[0]*(len(a)+len(b)-1)
 for i,u in enumerate(a):
  for j,v in enumerate(b):out[i+j]=(out[i+j]+u*v)%p
 return trim(out)
def rem(a,b,p):
 a=a[:];bi=pow(b[-1],-1,p)
 while len(a)>=len(b) and a!=[0]:
  k=len(a)-len(b);c=a[-1]*bi%p
  for j,v in enumerate(b):a[k+j]=(a[k+j]-c*v)%p
  trim(a)
 return a
def pgcd(a,b,p):
 while b!=[0]:a,b=b,rem(a,b,p)
 return [v*pow(a[-1],-1,p)%p for v in a]
def ppow(a,n,f,p):
 out=[1]
 while n:
  if n&1:out=rem(pmul(out,a,p),f,p)
  a=rem(pmul(a,a,p),f,p);n//=2
 return out
def irreducible(f,p):
 n=len(f)-1;x=rem([0,1],f,p)
 if ppow(x,p**n,f,p)!=x:return False
 for q in [r for r in range(2,n+1) if n%r==0 and all(r%d for d in range(2,int(r**.5)+1))]:
  if pgcd(padd(ppow(x,p**(n//q),f,p),[0,-1],p),f,p)!=[1]:return False
 return True

def main():
 data=json.loads((ROOT/'PARITY_CERTIFICATES.json').read_text());assert len(data['patterns'])==14
 representatives={tuple(r['counts']) for r in data['patterns']};allpatterns=[v for v in itertools.product(range(6),repeat=4) if sum(v)==5]
 assert len(allpatterns)==56
 assert {max(v[i:]+v[:i] for i in range(4)) for v in allpatterns}==representatives
 assert all(check_certificate(r) for r in data['patterns'])
 denominators={d for r in data['patterns'] for poly in r['multipliers'] for _,_,d in poly}
 assert all(d%17 for d in denominators)
 # Exact prime-17 reduction of each rational identity.
 for r in data['patterns']:
  out={}
  for f,h in zip(r['inputs'],r['multipliers']):
   ff={tuple(m):n*pow(d,-1,17)%17 for m,n,d in f};hh={tuple(m):n*pow(d,-1,17)%17 for m,n,d in h}
   out=psum(out,pprod(ff,hh))
  out={m:c%17 for m,c in out.items() if c%17};assert out=={(0,)*5:1}
 bad=copy.deepcopy(data['patterns'][0]);bad['multipliers'][0][0][1]+=1;assert not check_certificate(bad)
 bad=copy.deepcopy(data['patterns'][0]);bad['inputs'][0][0][1]+=1;assert not check_certificate(bad)
 assert check_inverse(16) and not check_inverse(16,True)
 norms={str(N):check_norm(N) for N in [4,8,16,32,64]};assert all(norms.values())
 guards={str(N):check_norm_factors(N,p) for N,p in [(8,17),(16,97),(32,193)]}
 # A legal stride-eight parameter can have alpha^16=1: correct guard is alpha^2 !=1.
 alpha=8;assert pow(alpha,16,97)==1 and unit_parameter(alpha,8,16,97)
 # Constructive finite splitting bound for zeta^2=3 in char17.
 factors=[[16,1],[1,2,13,2,1],[1,11,8,11,1],[1,11,3,6,3,11,1]]
 prod=[16]
 for f in factors:prod=pmul(prod,f,17)
 target=[pow(6,t*(t+1)//2,17) for t in range(16)];assert prod==target
 assert all(irreducible(f,17) for f in factors)
 assert all(12%(len(f)-1)==0 for f in factors)
 # Direct formal quadratic-field guard for zeta=t, t^2=3.
 def km(u,v):return ((u[0]*v[0]+3*u[1]*v[1])%17,(u[0]*v[1]+u[1]*v[0])%17)
 def kp(u,n):
  out=(1,0)
  while n:
   if n&1:out=km(out,u)
   u=km(u,u);n//=2
  return out
 assert kp((0,1),16)==(16,0) and kp((0,1),32)==(1,0)
 assert km((0,1),(0,6))==(1,0)
 # Exact recurrence cost positive control on 97-rational legal factors.
 p=97;N=16;ops=[0,0];alpha=2;assert unit_parameter(alpha,1,N,p)
 x=list(range(N));H=x[0]
 for v in x[1:]:H=(alpha*H+v)%p;ops[0]+=1;ops[1]+=1
 y=[0]*N;y[-1]=H*pow((1-pow(alpha,N,p))%p,-1,p)%p;ops[0]+=1
 for i in range(N-1):y[i]=(x[i]+alpha*y[i-1])%p;ops[0]+=1;ops[1]+=1
 assert [(y[i]-alpha*y[i-1])%p for i in range(N)]==x and ops==[31,30]
 result={'all_exact_checks_passed':True,'parity_rational_certificates':14,'covered_five_odd_stride_patterns':56,'parity_certificate_terms':sum(len(poly) for r in data['patterns'] for poly in r['multipliers']),'parity_mod17_identities':14,'full_N16_inverse_entries':256,'dyadic_norm_sizes':norms,'legal_factor_norm_cases':guards,'finite_constructive_splitting_degree':12,'finite_factor_degrees':[len(f)-1 for f in factors],'negative_controls':['mutated multiplier rejected','mutated defining equation rejected','mutated chirp inverse rejected'],'resolvent_application_cost_N16':{'multiplications':ops[0],'additions':ops[1]},'scope':'N16 lower bound seven and upper bound fifteen, not an exact minimum; general dyadic norm transfer'}
 (ROOT/'CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
