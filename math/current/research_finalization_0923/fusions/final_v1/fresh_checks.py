"""Fresh independently authored checks. No supplied source code is read/imported."""
import json, random, cmath, math
from fractions import Fraction as F
from pathlib import Path
R=random.Random(104)
p=257

def rank(A):
 A=[list(r) for r in A];i=0
 for j in range(len(A[0]) if A else 0):
  z=next((k for k in range(i,len(A)) if A[k][j]%p),None)
  if z is None:continue
  A[i],A[z]=A[z],A[i];s=pow(A[i][j],-1,p);A[i]=[(a*s)%p for a in A[i]]
  for k in range(len(A)):
   if k!=i:
    s=A[k][j];A[k]=[(a-s*b)%p for a,b in zip(A[k],A[i])]
  i+=1
  if i==len(A):break
 return i

def solve(A,b):
 n=len(b);A=[list(row)+[v] for row,v in zip(A,b)]
 for i in range(n):
  z=next((k for k in range(i,n) if A[k][i]%p),None)
  if z is None:return None
  A[i],A[z]=A[z],A[i];s=pow(A[i][i],-1,p);A[i]=[(v*s)%p for v in A[i]]
  for k in range(n):
   if k!=i:
    s=A[k][i];A[k]=[(a-s*b)%p for a,b in zip(A[k],A[i])]
 return [row[-1] for row in A]

def recognize(c,q,t):
 N=len(c);r=rank([[c[i+j] for j in range(t)] for i in range(t)])
 if r==0:return [] if all(v==0 for v in c) else None
 H=[[c[i+j] for j in range(r)] for i in range(r)]
 a=solve(H,[-c[i+r] for i in range(r)])
 if a is None:return None
 nodes=[]
 for u in range(N):
  z=pow(q,u,p);v=1
  for v0 in reversed(a):v=(v*z+v0)%p
  if v==0:nodes.append((u,z))
 if len(nodes)!=r:return None
 g=solve([[pow(z,i,p) for u,z in nodes] for i in range(r)],c[:r])
 if g is None or any(v==0 for v in g):return None
 if any(sum(g0*pow(z,j,p) for (u,z),g0 in zip(nodes,g))%p!=c[j] for j in range(N)):return None
 return [(u,g0) for (u,z),g0 in zip(nodes,g)]

modal_cases=0;outputs_checked=0
for N in [4,8,16,32]:
 q=pow(3,256//N,p);assert pow(q,N,p)==1 and pow(q,N//2,p)!=1
 for t in range(1,min(4,N//2)+1):
  for z in range(36):
   rr=R.randrange(t+1);us=R.sample(range(N),rr);gs=[R.randrange(1,p) for _ in us]
   c=[sum(g*pow(q,u*j,p) for u,g in zip(us,gs))%p for j in range(N)]
   if z%3==1:c[R.randrange(N)]=(c[R.randrange(N)]+1)%p
   elif z%3==2:c=[R.randrange(p) for _ in range(N)]
   ans=recognize(c,q,t)
   true=[(u,sum(c[j]*pow(q,(-u*j)%N,p) for j in range(N))*pow(N,-1,p)%p) for u in range(N)]
   true=[(u,g) for u,g in true if g]
   assert (ans is not None)==(len(true)<=t),(N,t,c,ans,true)
   modal_cases+=1
   if ans is not None:
    assert sorted(ans)==true
    a=[R.randrange(1,p) for _ in range(N)];b=[R.randrange(1,p) for _ in range(N)];x=[R.randrange(p) for _ in range(N)]
    y=[a[i]*sum(c[j]*pow(q,i*j,p)*sum(b[k]*x[k]*pow(q,j*k,p) for k in range(N)) for j in range(N))%p for i in range(N)]
    yy=[N*a[i]*sum(g*b[(-i-u)%N]*x[(-i-u)%N] for u,g in ans)%p for i in range(N)]
    assert y==yy
    outputs_checked+=N

# Rational local-energy quantization, no clipping, exact local error test.
H=[[F(1 if ((i&j).bit_count()%2)==0 else -1,2) for j in range(4)] for i in range(4)]
eta=F(1,8);h=F(1,8192);local_checks=0
for _ in range(300):
 v=[F(R.randrange(-1000,1001),2**R.randrange(0,20)) for j in range(4)]
 M=max(map(abs,v))
 if M==0:continue
 s=F(1)
 while s<M:s*=2
 while s>=2*M:s/=2
 u=[z/s for z in v]
 q=[F(round(z/h))*h for z in u]
 exact=[sum(H[i][j]*v[j] for j in range(4)) for i in range(4)]
 tab=[F(round(sum(H[i][j]*q[j] for j in range(4))/h))*h for i in range(4)]
 y=[s*z for z in tab]
 assert sum((a-b)**2 for a,b in zip(y,exact))<=eta**2*sum(z*z for z in v)
 local_checks+=1

# Weyl-covariant nonlinear counterexample, numerical controls only.
nonlinear=[]
for N in [2,3,4,8,16]:
 q=cmath.exp(2j*math.pi/N)
 def U(x):return [sum(q**(i*j)*x[j] for j in range(N))/math.sqrt(N) for i in range(N)]
 def A(x):
  n=sum(abs(a)**2 for a in x)
  if not n:return [0j]*N
  s=sum(abs(a)**4 for a in x)/(n*n);f=(1-s)/(1-1/N)
  return [cmath.exp(1j*math.pi*f)*a for a in U(x)]
 x=[complex(R.random(),R.random()) for _ in range(N)]
 shift=lambda x:[x[(j-1)%N] for j in range(N)]
 mod=lambda x:[q**j*x[j] for j in range(N)]
 y=A(x);a=A(shift(x));b=mod(y)
 c=A(mod(x));d=[y[(j+1)%N] for j in range(N)]
 cov=max(max(abs(aa-bb) for aa,bb in zip(a,b)),max(abs(aa-bb) for aa,bb in zip(c,d)))
 flat=[1+0j]*N;rel=math.sqrt(sum(abs(a-b)**2 for a,b in zip(A(flat),U(flat)))/N)
 assert cov<1e-10 and abs(rel-2)<1e-10
 nonlinear.append({'N':N,'covariance_residual':cov,'flat_relative_error':rel})

result={'supplied_programs_executed':False,'exact_modal_recognition_cases':modal_cases,'exact_orbit_output_coordinates_checked':outputs_checked,'exact_rational_local_quantization_cases':local_checks,'nonlinear_counterexample_numerical_controls':nonlinear,'limitations':['Finite controls support the proofs; they do not prove all-size statements.','Local quantization entries were computed for sampled keys, not a production eager table.','No timing or finite-word implementation benchmark.']}
Path(__file__).with_name('fresh_check_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
