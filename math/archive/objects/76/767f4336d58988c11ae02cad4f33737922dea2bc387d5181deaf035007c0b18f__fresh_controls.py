"""New independently authored controls. Imports no supplied research program."""
import itertools, json, random, time
from pathlib import Path
import sympy as S
rng=random.Random(202610100958)
OUT=Path(__file__).parent

def add(a,b,p):
 n=max(len(a),len(b));return [((a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0))%p for i in range(n)]
def mul(a,b,p):
 if not a or not b:return []
 n=max(len(a),len(b))
 if n<=4:
  c=[0]*(len(a)+len(b)-1)
  for i,x in enumerate(a):
   for j,y in enumerate(b):c[i+j]=(c[i+j]+x*y)%p
  return c
 k=(n+1)//2;a0,a1=a[:k],a[k:];b0,b1=b[:k],b[k:]
 c0=mul(a0,b0,p);c2=mul(a1,b1,p);c1=mul(add(a0,a1,p),add(b0,b1,p),p)
 for i,x in enumerate(c0):c1[i]=(c1[i]-x)%p
 for i,x in enumerate(c2):c1[i]=(c1[i]-x)%p
 c=[0]*(len(a)+len(b)-1)
 for h,v in [(0,c0),(k,c1),(2*k,c2)]:
  for i,x in enumerate(v):
   if h+i<len(c):c[h+i]=(c[h+i]+x)%p
 return c

def blocked_values(coeff,omega,N,p):
 b=len(coeff);s=b-1;pw=[pow(omega,j,p) for j in range(N)]
 kernel=[pw[(-(d*(d-1)//2))%N] for d in range(-s,b)]
 ans=[]
 for K in range(0,N,b):
  v=[coeff[j]*pw[(K*j+j*(j+1)//2)%N]%p for j in range(b)]
  cv=mul(v,kernel,p)
  ans.extend(pw[(a*(a-1)//2)%N]*cv[a+s]%p for a in range(min(b,N-K)))
 return ans

def recurrence_values(y,coeff,p):
 b=len(coeff);s=b-1;cv=[0]*(len(y)+s)
 for k in range(0,len(y),b):
  z=mul(y[k:k+b],coeff[::-1],p)
  for j,v in enumerate(z):cv[k+j]=(cv[k+j]+v)%p
 return cv[s:len(y)]

def rank(M,p):
 a=[row[:] for row in M];r=0
 for j in range(len(a[0]) if a else 0):
  k=next((k for k in range(r,len(a)) if a[k][j]%p),None)
  if k is None:continue
  a[r],a[k]=a[k],a[r];v=pow(a[r][j],-1,p);a[r]=[z*v%p for z in a[r]]
  for i in range(r+1,len(a)):
   v=a[i][j];a[i]=[(x-v*y)%p for x,y in zip(a[i],a[r])]
  r+=1
  if r==len(a):break
 return r

def solve(M,b,p):
 a=[row[:]+[v] for row,v in zip(M,b)];n=len(a)
 for j in range(n):
  k=next((k for k in range(j,n) if a[k][j]%p),None)
  if k is None:return None
  a[j],a[k]=a[k],a[j];v=pow(a[j][j],-1,p);a[j]=[z*v%p for z in a[j]]
  for i in range(n):
   if i!=j:
    v=a[i][j];a[i]=[(x-v*y)%p for x,y in zip(a[i],a[j])]
 return [row[-1] for row in a]

def model_check(y,r,omega,p):
 N=len(y);s=rank([[y[i+j] for j in range(r)] for i in range(r)],p)
 if s==0:return [] if not any(y) else None
 co=solve([[y[i+j] for j in range(s)] for i in range(s)],[-y[i+s]%p for i in range(s)],p)
 if co is None:return None
 co=co+[1]
 roots=[j for j,v in enumerate(blocked_values(co,omega,N,p)) if v==0]
 if len(roots)!=s or any(recurrence_values(y,co,p)):return None
 weights=solve([[pow(omega,i*j,p) for j in roots] for i in range(s)],y[:s],p)
 assert all(sum(c*pow(omega,b*j,p) for b,c in zip(roots,weights))%p==y[j] for j in range(N))
 return list(zip(roots,weights))

def eliminant(x,r,c,p):
 # Direct alternating expansion used only as an independent low-r control.
 D=r*(r+1)*(r+2)//6;v=[0]*(D+1)
 for perm in itertools.permutations(range(r+1)):
  inv=sum(perm[i]>perm[j] for i in range(r+1) for j in range(i+1,r+1));a=(-1)**inv;e=0
  for i,j in enumerate(perm):
   d=i-j;e+=d*(d-1)//2;a=a*x[c+d]%p
  v[e]=(v[e]+a)%p
 return v

def recognize(x,r,omega,p):
 N=len(x)
 if not any(x):return (0,[])
 c=next((c for c in range(r,N-r) if x[c]),None)
 if c is None:return None
 el=eliminant(x,r,c,p);L=N//S.gcd(2,N)
 for a in range(int(L)):
  t=pow(omega,(-2*a)%N,p);v=0
  for z in el[::-1]:v=(v*t+z)%p
  if v:continue
  y=[z*pow(omega,(-a*j*j)%N,p)%p for j,z in enumerate(x)]
  ans=model_check(y,r,omega,p)
  if ans is not None:return a,ans
 return None

start=time.time();result={'method':'new independent scripts; no supplied program executed'}
# C03: fixed homogeneous Sylvester construction, including degree drops.
a,w=S.symbols('a w');checks=[]
for m in [1,2,3]:
 for case in range(3):
  A=S.Matrix([[rng.randrange(-2,3) for j in range(m)] for i in range(m)])
  B=S.Matrix([[rng.randrange(-2,3) for j in range(m)] for i in range(m)])
  if case==2:A[m-1,:]=S.zeros(1,m)
  D=S.diag(*[w**i for i in range(m)])
  f=S.Poly((A-a*D*A*D).det(),a);g=S.Poly((B-a*w*D*B*D).det(),a)
  fc=[f.nth(i) for i in range(m,-1,-1)];gc=[g.nth(i) for i in range(m,-1,-1)]
  rows=[]
  for co in [fc,gc]:
   for i in range(m):rows.append([0]*i+co+[0]*(m-1-i))
  R=S.Poly(S.Matrix(rows).det(method='domain-ge'),w)
  T=m*m*(2*m-1);v=m*(m-1)*(4*m+1)//6;b=m*(m-1)*(2*m-1)//6
  assert all(R.nth(j)==(-1)**(m*m)*R.nth(T-j) for j in range(T+1))
  U,rem=S.div(R,S.Poly(w**v*(w-1)**(m*m),w));assert rem.is_zero
  assert all(U.nth(j)==U.nth(2*b-j) for j in range(2*b+1))
  checks.append({'m':m,'case':case,'resultant_zero':R.is_zero,'passed':True})
result['C03']=checks
# Even bank, exact mod-p diagnostic. Does not substitute for characteristic-zero proof.
z=S.symbols('z');ev=[]
for N in list(range(4,42,2))+[48,64,96]:
 h=N//2;p=int(S.nextprime(4*h))
 while (p-1)%N:p=int(S.nextprime(p))
 q=pow(int(S.primitive_root(p)),(p-1)//N,p)
 moments=[pow(q,j*(j-1)//2,p) for j in range(2*h+2)]
 pol=[]
 for n in [h-1,h]:
  rr=S.Poly(1,z, modulus=p)
  for k in range(n):rr*=S.Poly(z-pow(q,k,p),z,modulus=p)
  pol.append(S.Poly.from_list([(int(rr.nth(j))*moments[n]*pow(moments[j],-1,p))%p for j in range(n,-1,-1)],z,modulus=p))
 G,Ph=pol;F=Ph*S.Poly(z,z,modulus=p)
 assert S.gcd(F,G).degree()==0
 W=F.diff()*G-F*G.diff();assert W.degree()==2*h-1 and int(W.LC())%p==2
 picked=None
 for t in range(1,4*h+1):
  B=F+t*G
  if S.gcd(B,B.diff()).degree()==0 and S.gcd(B,S.Poly(z**N+1,z,modulus=p)).degree()==0:picked=t;break
 assert picked is not None
 assert all(sum(int(B.nth(j))*moments[s+j] for j in range(h+2))%p==0 for s in range(h-1))
 assert rank([[moments[i+j] for j in range(h)] for i in range(h)],p)==h
 ev.append({'N':N,'p':p,'root':q,'t':picked,'passed':True})
result['even_prony']=ev
# Blocked primitives, arbitrary vectors and awkward block tails.
prim=0
for N,p in [(3,7),(4,5),(6,7),(9,19),(12,13),(16,17),(20,41),(30,31),(64,193)]:
 omega=pow(int(S.primitive_root(p)),(p-1)//N,p)
 for degree in range(1,min(18,N)):
  for rep in range(3):
   co=[rng.randrange(p) for _ in range(degree+1)];y=[rng.randrange(p) for _ in range(N)]
   vals=blocked_values(co,omega,N,p)
   assert vals==[sum(v*pow(omega,j*k,p) for j,v in enumerate(co))%p for k in range(N)]
   rec=recurrence_values(y,co,p)
   assert rec==[sum(co[j]*y[k+j] for j in range(len(co)))%p for k in range(N-degree)]
   prim+=1
result['blocked_primitive_cases']=prim
ex=[]
for N,p in [(3,7),(4,5)]:
 omega=pow(int(S.primitive_root(p)),(p-1)//N,p);family={(0,)*N}
 for a in range(N):
  for b in range(N):
   for c in range(1,p):family.add(tuple(c*pow(omega,(a*j*j+b*j)%N,p)%p for j in range(N)))
 count=0
 for x in itertools.product(range(p),repeat=N):
  got=recognize(x,1,omega,p)
  assert (got is not None)==(x in family)
  count+=1
 ex.append({'N':N,'p':p,'vectors':count,'family_size':len(family),'passed':True})
result['exhaustive_recognition']=ex
structured=0;arbitrary=0
for N,p,r in [(6,7,2),(9,19,3),(12,13,4),(16,17,4),(20,41,4),(30,31,4)]:
 omega=pow(int(S.primitive_root(p)),(p-1)//N,p)
 for rep in range(20):
  a=rng.randrange(N);s=rng.randrange(1,r+1);bs=rng.sample(range(N),s);cs=[rng.randrange(1,p) for _ in bs]
  x=[sum(c*pow(omega,(a*j*j+b*j)%N,p) for b,c in zip(bs,cs))%p for j in range(N)]
  got=recognize(x,r,omega,p);assert got is not None;structured+=1
  xx=[rng.randrange(p) for _ in range(N)]
  blocked=model_check(xx,r,omega,p)
  # Soundness independently checked by reconstruction inside model_check.
  arbitrary+=1
result['structured_recognition_cases']=structured;result['arbitrary_candidate_cases']=arbitrary
result['elapsed_seconds']=round(time.time()-start,3);result['all_passed']=True
(OUT/'fresh_controls_results.json').write_text(json.dumps(result,indent=2))
print(json.dumps({k:(len(v) if isinstance(v,list) else v) for k,v in result.items()},indent=2))
