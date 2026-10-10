import json,random,math
import sympy as sp
from sympy.ntheory import primitive_root

def rank_mod(A,q):
 m=[[(int(x)%q) for x in row] for row in A]
 if not m:return 0
 nrow=len(m);ncol=len(m[0]);i=0
 for j in range(ncol):
  k=next((k for k in range(i,nrow) if m[k][j]%q),None)
  if k is None: continue
  m[i],m[k]=m[k],m[i];z=pow(m[i][j],-1,q)
  m[i]=[(t*z)%q for t in m[i]]
  for a in range(nrow):
   if a!=i and m[a][j]%q:
    t=m[a][j];m[a]=[(e-t*f)%q for e,f in zip(m[a],m[i])]
  i+=1
  if i==nrow: break
 return i

def phase37(N, seed):
 R=random.Random(seed)
 cycle=list(range(N));R.shuffle(cycle)
 position={v:i for i,v in enumerate(cycle)}
 c=1
 # root exponent curvature from cyclic Green
 def s(i,j):return int(position[i]<position[j])
 for _ in range(13):
  row=R.sample(range(N),N); col=R.sample(range(N),N)
  a=row[0];b=col[0]
  E=[[(c*(s(i,j)-s(i,b)-s(a,j)+s(a,b)))%N for j in col if j!=b] for i in row if i!=a]
  assert rank_mod(E,2)==N-1
  EF=[[((i-a)*(j-b))%N for j in col if j!=b] for i in row if i!=a]
  assert rank_mod(EF,2)==1
 return True

# symbolic generic s=1 test
w,a=sp.symbols('w a')
T=sp.symbols('T0:4')
P=[]
for e in (0,1):
 M=sp.Matrix([[T[e+i+j]*(1-a*w**(e+i+j)) for j in range(2)] for i in range(2)])
 P.append(sp.expand(M.det()))
R=sp.factor(sp.resultant(P[0],P[1],a))
Q=sp.cancel(R/(w**3*(w-1)**4))
assert sp.denom(Q)==1, 'unexpected symbolic denominator'
assert sp.expand(w**2*Q.subs(w,1/w)-Q)==0
assert sp.Poly(Q,w).degree()<=2

# odd prime p Weyl coefficient, quadratic chirp normalized rank test
prime_tests=[]
for p,q in ((5,31),(7,29),(11,23)):
 gen=int(primitive_root(q));omega=pow(gen,(q-1)//p,q)
 m=(p+1)//2
 # canonical F Weyl coefficient by independent literal trace formula
 F=[[pow(omega,i*j,q) for j in range(p)] for i in range(p)]
 invp=pow(p,-1,q)
 Gauss=(sum(pow(omega,t*t,q) for t in range(p))*invp)%q
 C=[]
 for A in range(p):
  row=[]
  for B in range(p):
   diag_trace=0
   for k in range(p):
    # (S^A T^B)^-1 F diagonal k,k
    diag_trace+=F[(k+A)%p][k]*pow(omega,(-B*k)%p,q)
   coefficient=(diag_trace*invp)%q
   predicted=Gauss*pow(omega,(-((A-B)*pow(2,-1,p))**2)%p,q)%q
   assert coefficient==predicted,(p,A,B,coefficient,predicted)
   row.append(coefficient)
  C.append(row)
 assert rank_mod(C,q)==p
 # rotated Weyl aligned class where delta=0, e.g U=S,V=ST (u=1,v=0,r=1,s=1)
 u,v,r,s=1,0,1,1
 D=(u*s-v*r)%p;h=(u*r+v*s)%p;delta=(D-h)*pow(2,-1,p)%p
 assert delta==0
 Aq=(u*u+v*v)%p
 chirp=[(Gauss*pow(omega,(-Aq*i*i*pow(4,-1,p))%p,q))%q for i in range(p)]
 H=[[chirp[i+j] for j in range(m)] for i in range(m)]
 assert rank_mod(H,q)==m
 prime_tests.append({'p':p,'coefficient_field_prime':q,'Weyl_rank':rank_mod(C,q),'Hankel_rank':rank_mod(H,q),'lower_bound':m})
checks={'phase37_mod2_curvature':{str(N):phase37(N,N*101) for N in (4,8,16,32)},'reciprocal_s1':{'verified_symbolically':True,'quotient':str(sp.factor(Q))},'phase13':prime_tests}
from pathlib import Path
Path('fft_review/INDEPENDENT_NOVELTY_MATH_CHECKS.json').write_text(json.dumps(checks,indent=2))
print(json.dumps(checks,indent=2))
