import own_base as k
from pathlib import Path
from collections import defaultdict
import math,json
K=k.K;E=k.E;eta=k.Z;g=k.G
class P:
 def __init__(self,a=0):self.a=a.a.copy() if isinstance(a,P) else (a if isinstance(a,dict) else {(0,)*5:a} if a else {})
 def __add__(self,b):
  c=defaultdict(int,self.a)
  for e,v in P(b).a.items():c[e]+=v
  return P({e:v for e,v in c.items() if v})
 __radd__=__add__
 def __neg__(self):return P({e:-v for e,v in self.a.items()})
 def __sub__(self,b):return self+-P(b)
 def __rsub__(self,b):return P(b)+-self
 def __mul__(self,b):
  c=defaultdict(int)
  for e,v in self.a.items():
   for f,w in P(b).a.items():c[tuple(x+y for x,y in zip(e,f))]+=v*w
  return P({e:v for e,v in c.items() if v})
 __rmul__=__mul__
 def __pow__(self,n):
  z=P(1)
  for i in range(n):z=z*self
  return z
 def __eq__(self,b):return self.a==P(b).a
al,be,ga,ep,d=[P({tuple(int(i==j) for j in range(5)):1}) for i in range(5)]
L=be**2-ga*ep;M=-2*al*be+al*ga+al*ep+be*ga+be*ep-2*ga*ep;J=(be-ga)**2;s=al+be
assert (be-ga)*(be*d*d+(be-al)*d+be-ga)-(ep-be)*d*(ga*d+2*ga-al-be)==L*d*d+M*d+J
assert J*(ga*ga*L-ga*s*M+s*s*J)==ga*ga*J*L-ga*(2*ga-s)*M*L+(2*ga-s)**2*L*L
# Coefficient-wise q=1+241z congruences, with all nonconstant coefficients zero.
def prodmod(a,b):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]=(c[i+j]+x*y)%241
 return c
qq=[1,241];q3=prodmod(prodmod(qq,qq),qq);assert q3==[1,0,0,0]
Gmod=g.mod();etamod=eta.mod()
for i in range(5):
 for j in range(5):
  nom=[pow(etamod,i*j,241),0,0,0]
  for t,v in enumerate(qq):nom[t]=(nom[t]-v*Gmod*pow(etamod,-3*(i+j)**2,241))%241
  if i==j:
   for t,v in enumerate(q3):nom[t]=(nom[t]+5*v*Gmod*pow(etamod,-3*i*i,241))%241
  assert nom[1:]==[0,0,0]
expected_base=[20,102,234,89,163,163];expected_ext=[124,139,53,1,160,85];expected_end=[1,44,153,153,44,41,117,7,7,117,72,113,64,64,113];cases=[]
for q in [1,483,1447,1929,2411,242,965]:
 B=[[(eta**(i*j)-q*g*eta**(-3*(i+j)**2)+(5*q**3*g*eta**(-3*i*i) if i==j else 0))/(1+5*q**3*g) for j in range(5)] for i in range(5)]
 assert [[x.mod() for x in row] for row in B]==[[161,20,102,102,20],[20,182,62,26,92],[102,62,236,28,26],[102,26,28,236,62],[20,92,26,62,182]]
 assert (1+5*q**3*g)*(1-5*q**3*g)==1-125*q**6
 a,b,c,e,f,h=B[0][1],B[0][2],B[1][2],B[1][3],B[1][4],B[2][3];alpha,beta,gamma,eps=c/(a*b),e/(a*b),f/a**2,h/b**2
 lead=beta**2-gamma*eps;k.p1=(-2*alpha*beta+alpha*gamma+alpha*eps+beta*gamma+beta*eps-2*gamma*eps)/lead;k.p0=(beta-gamma)**2/lead;disc=k.p1**2-4*k.p0
 assert [x.mod() for x in [a,b,gamma,beta-gamma,lead,disc]]==expected_base and k.p1.mod()==30 and k.p0.mod()==124 and pow(disc.mod(),120,241)==240
 dd=E(0,1);den=E(gamma)*(dd+2)-alpha-beta;t=(E(gamma)*dd+E(alpha+beta)*dd**2)/den;kap=(t+dd**2)/gamma;x=(t-dd)/kap;rr=[x,(E(alpha)-x)/dd,(E(beta)-x)/dd,(E(gamma)-x)/dd];z=kap/(1+t)
 u=[E(1)]+[E(B[0][i])*rr[i-1] for i in range(1,5)];v=[z/t]+[E(B[0][i])-z*u[i] for i in range(1,5)];di=[E(B[i][i])-(1+t)*u[i]*v[i] for i in range(5)]
 assert t.norm()==1 and t.conj()==1/t
 assert [y.norm().mod() for y in [dd,den,kap,t,1+t,1-t]]==expected_ext and [y.norm().mod() for y in u+v+di]==expected_end
 Id=[[E(i==j) for j in range(5)] for i in range(5)];greens=[]
 for pole in [t,1/t]:
  W=[[E(0) for j in range(5)] for i in range(5)]
  for i in range(5):W[i][(i+1)%5]=E(1) if i<4 else pole
  G=[[(E(1) if i<=j else pole)/(1-pole) for j in range(5)] for i in range(5)];IW=[[Id[i][j]-W[i][j] for j in range(5)] for i in range(5)]
  assert k.isid(k.mm(IW,G)) and k.isid(k.mm(G,IW));greens.append(G)
 rec=[[(1-t)*u[i]*greens[0][i][j]*v[j]+(t-1)*v[i]*greens[1][i][j]*u[j]+(di[i] if i==j else 0) for j in range(5)] for i in range(5)]
 assert all(rec[i][j]==B[i][j] and rec[i][j].conj()==B[i][j] for i in range(5) for j in range(5))
 def scan(inp,pole):
  y0=sum(inp)/(1-pole);y=[y0]+[E(0)]*4;y[4]=inp[4]+pole*y0
  for i in range(3,0,-1):y[i]=inp[i]+y[i+1]
  assert y[0]-y[1]==inp[0]
  return y
 for inp in [[E(i==j) for i in range(5)] for j in range(5)]+[[E(i+1) for i in range(5)],[dd+E(eta**i) for i in range(5)]]:
  y0=scan([v[i]*inp[i] for i in range(5)],t);y1=scan([u[i]*inp[i] for i in range(5)],1/t);got=[(1-t)*u[i]*y0[i]+(t-1)*v[i]*y1[i]+di[i]*inp[i] for i in range(5)]
  assert got==[sum(E(B[i][j])*inp[j] for j in range(5)) for i in range(5)]
 cases.append({'q':q,'ambient_restriction_admitted':q%2==1 and q%5!=0,'both_root_entries':50,'inverse_entries':100,'scan_outputs':35,'guard_residues':expected_base+expected_ext+expected_end})
z=P({(0,0,0,0,1):1});c=al;assert (1-z)*((1+c)*z*z+(1-2*c)*z+1+c)==1-(z**3-c*(1-z)**3)
p=65521;primitive=next(g for g in range(2,p) if all(pow(g,(p-1)//r,p)!=1 for r in [2,3,5,7,13]))
def dft(x,omega):return [sum(x[j]*pow(omega,i*j,p) for j in range(len(x)))%p for i in range(len(x))]
blue=[]
for n,m in [(1,5),(2,5),(3,5),(4,9),(5,13),(7,15),(8,21),(9,21),(10,35),(12,35),(13,35),(15,35)]:
 assert m>=2*n-1 and (p-1)%(2*n)==(p-1)%m==0
 theta=pow(primitive,(p-1)//(2*n),p);w=theta*theta%p;wm=pow(primitive,(p-1)//m,p);inp=[(j*j+5*j+7)%p for j in range(n)];aa=[0]*m;bb=[0]*m
 for j in range(n):aa[j]=inp[j]*pow(theta,j*j,p)%p
 for j in range(-n+1,n):bb[j%m]=pow(theta,-j*j,p)
 aa=dft(aa,wm);bb=dft(bb,wm);cc=dft([a*b%p for a,b in zip(aa,bb)],wm);conv=[cc[-i%m]*pow(m,-1,p)%p for i in range(m)]
 assert [conv[i]*pow(theta,i*i,p)%p for i in range(n)]==dft(inp,w);blue.append([n,m])
pads=[]
for n in [1,2,3,4,100,10000,1000000,14532303,10**12,10**30]:
 target=2*n-1;qmin=math.isqrt((target-1)//5)+1;kk=max(0,(qmin-1+2409)//2410);q=2410*kk+1;m=5*q*q
 assert m>=target and (kk==0 or 5*(q-2410)**2<target) and m-target<=24100*(math.isqrt(target)+1)+5*2410**2;pads.append({'n':n,'q':q,'M':m})
# The full natural-order two-cycle-plus-diagonal ansatz has rank <=2,
# while actual chirp resolvents have full contiguous half-cut rank.
def rankmod(A):
 A=[r[:] for r in A];r=0
 for j in range(len(A[0])):
  a=next((a for a in range(r,len(A)) if A[a][j]),None)
  if a is None:continue
  A[a],A[r]=A[r],A[a];t=pow(A[r][j],-1,p);A[r]=[x*t%p for x in A[r]]
  for a in range(r+1,len(A)):
   t=A[a][j];A[a]=[(x-t*y)%p for x,y in zip(A[a],A[r])]
  r+=1
 return r
cuts=[]
for N in [5,7,9,13,15]:
 w=pow(primitive,(p-1)//N,p);h=pow(2,-1,N);gg=sum(pow(w,h*j*j,p) for j in range(N))%p;c=N*gg%p;assert (1+c)%p
 B=[[(pow(w,i*j,p)-gg*pow(w,-h*(i+j)**2,p)+(c*pow(w,-h*i*i,p) if i==j else 0))*pow(1+c,-1,p)%p for j in range(N)] for i in range(N)]
 r=N//2;assert rankmod([row[r:] for row in B[:r]])==r
 cuts.append({'N':N,'cut_rank':r,'two_cycle_plus_diagonal_rejected':r>2})
Path('EXTENSION_REVIEW_RESULTS.json').write_text(json.dumps({'status':'PASS','exact_q_cases':cases,'general_polynomial_identities':3,'formal_target_congruences':25,'base_guard_residues':expected_base,'extension_guard_residues':expected_ext,'endpoint_guard_residues':expected_end,'Bluestein_controls':blue,'minimal_padding_controls':pads,'full_natural_ansatz_controls':cuts,'source_code_executed':False},indent=2,sort_keys=True)+'\n');print('EXTENSION AND CONDITIONAL BRIDGE PASS')
