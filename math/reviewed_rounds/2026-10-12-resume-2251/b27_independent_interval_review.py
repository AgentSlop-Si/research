"""Independent b27 interval replay. Author programs are not imported/executed."""
from fractions import Fraction
import json,math,hashlib,pathlib
HERE=pathlib.Path(__file__).resolve().parent
BITS=1024;U=1<<BITS
def up(n,d):return -((-n)//d)
def Q(n,d=1):
 assert d>0
 return n*U//d,up(n*U,d)
def plus(a,b):return a[0]+b[0],a[1]+b[1]
def minus(a):return -a[1],-a[0]
def times(a,b):
 t=(a[0]*b[0],a[0]*b[1],a[1]*b[0],a[1]*b[1])
 return min(t)//U,up(max(t),U)
def square(a):
 l,h=a
 if l<=0<=h:return 0,up(max(l*l,h*h),U)
 return min(l*l,h*h)//U,up(max(l*l,h*h),U)
def reciprocal(a):
 assert a[0]>0
 return U*U//a[1],up(U*U,a[0])
Z=(0,0);I=(U,U);C1=(I,Z);C0=(Z,Z)
def cadd(a,b):return plus(a[0],b[0]),plus(a[1],b[1])
def cneg(a):return minus(a[0]),minus(a[1])
def csub(a,b):return cadd(a,cneg(b))
def cmul(a,b):return plus(times(a[0],b[0]),minus(times(a[1],b[1]))),plus(times(a[0],b[1]),times(a[1],b[0]))
def cnorm(a):return plus(square(a[0]),square(a[1]))
def cinv(a):
 den=reciprocal(cnorm(a))
 return times(a[0],den),minus(times(a[1],den))
def cscale(a,n):return times(a[0],Q(n)),times(a[1],Q(n))
def frac_interval(l,h):
 return l.numerator*U//l.denominator,up(h.numerator*U,h.denominator)
def atan(n):
 v=sum((Fraction((-1)**j,(2*j+1)*n**(2*j+1)) for j in range(320)),Fraction())
 e=Fraction(1,641*n**641)
 return v,v+e
al,ah=atan(5);bl,bh=atan(239)
PI=frac_interval(16*al-4*bh,16*ah-4*bl)
assert 3*U<PI[0]<PI[1]<4*U
def root(d,k):
 if 2*k>d:k-=d
 t=times(PI,Q(2*k,d));v=square(t)
 # Horner, coefficients rounded independently; Taylor remainders with |t|<4.
 co=Q((-1)**160,math.factorial(320));si=Q((-1)**160,math.factorial(321))
 for j in range(159,-1,-1):
  co=plus(times(co,v),Q((-1)**j,math.factorial(2*j)))
  si=plus(times(si,v),Q((-1)**j,math.factorial(2*j+1)))
 si=times(si,t)
 ec=up(4**321*U,math.factorial(321));es=up(4**322*U,math.factorial(322))
 return (co[0]-ec,co[1]+ec),(si[0]-es,si[1]+es)
def enclosed(small,wide,oldscale):
 return wide[0]*U<=small[0]*oldscale and small[1]*oldscale<=wide[1]*U
def check(c,oldscale):
 d,k=c['d'],c['k'];assert d%2==1 and d>27 and math.gcd(d,k)==1
 q=root(d,k);qp=[C1]
 for j in range(1,d):qp.append(cmul(qp[-1],q))
 def f(j):return csub(C1,qp[j%d])
 # Gaussian Pascal recurrence, original derivative, no coefficient divisions.
 cs=[C1]
 for n in range(1,28):
  cs=[cadd(cs[j] if j<n else C0,cmul(qp[n-j],cs[j-1]) if j else C0) for j in range(n+1)]
 g=C0
 for j in range(1,28):g=cadd(g,cscale(cs[j],j*(-1)**(j-1)))
 wn=wd=C1;guard={}
 for j in range(1,28):
  wn=cmul(wn,f(j));guard['Gaussian denominator '+str(j)]=cnorm(f(j))
 for j in range(1,(d+27)//2+1):
  wd=cmul(wd,f(2*j));guard['W root '+str(j)]=cnorm(f(2*j))
 guard['W denominator']=cnorm(wd);guard['original derivative']=cnorm(g)
 tau=cscale(cmul(cmul(wn,cinv(wd)),cinv(g)),d)
 rho=cnorm(csub(tau,C1))
 E=C1;s=C1;Sm=C1
 for j in range(1,(d-1)//2+1):
  E=cmul(E,f(2*j))
  if j<=13:
   guard['prefix denominator '+str(j)]=cnorm(f(2*j))
   s=cmul(cmul(s,f(2*j-1)),cinv(f(2*j)));Sm=cadd(Sm,s)
 guard['E']=cnorm(E);guard['Sm']=cnorm(Sm)
 prefix=cscale(cmul(cinv(E),cinv(Sm)),d)
 # Original and prefix agree to enclosing intervals; exact identity supplied by theory.
 assert max(tau[0][0],prefix[0][0])<=min(tau[0][1],prefix[0][1])
 assert max(tau[1][0],prefix[1][0])<=min(tau[1][1],prefix[1][1])
 for name,value in [('tau_real',tau[0]),('tau_imag',tau[1]),('prefix_tau_real',prefix[0]),('prefix_tau_imag',prefix[1])]:
  assert enclosed(value,c[name],oldscale),(d,name)
 assert enclosed(rho,(c['rho_lower'],c['rho_upper']),oldscale),(d,'rho')
 assert set(guard)=={v['name'] for v in c['division_guards']}
 for g0 in c['division_guards']:
  v=guard[g0['name']];assert v[0]>0
  assert enclosed(v,(g0['squared_norm_lower'],g0['squared_norm_upper']),oldscale),(d,g0['name'])
 assert tau[1][0]>0 or tau[1][1]<0
 t=Fraction(9,4) if d==57 else Fraction(8,3)
 assert c['certified_threshold']==str(t)
 assert rho[0]*t.denominator>t.numerator*U
 assert c['rho_lower']*t.denominator>t.numerator*oldscale
 return {'d':d,'k':k,'guard_count':len(guard),'threshold':str(t),'rho_lower':rho[0],'rho_upper':rho[1],
         'coarse_lower_millionths':rho[0]*10**6//U,'coarse_upper_millionths':up(rho[1]*10**6,U)}
p=HERE/'b27_interval_certificates.json';data=json.loads(p.read_text())
assert data['scale']==1<<data['bits']
assert [c['d'] for c in data['certificates']]==list(range(57,210,2))
results=[check(c,data['scale']) for c in data['certificates']]
# Independent interval core self checks, zero divisor and invalid metadata negatives.
assert square((-U,U))==(0,U)
assert times((-U,U),(-2*U,3*U))==(-3*U,3*U)
negatives=0
for bad in [{'d':58},{'k':57},{'certified_threshold':'8/3'},{'rho_lower':U*10}]:
 c=dict(data['certificates'][0]);c.update(bad)
 try:check(c,data['scale'])
 except AssertionError:negatives+=1
 else:raise AssertionError('negative escaped')
try:reciprocal((0,U))
except AssertionError:negatives+=1
out={'status':'PASS independent original-normalization interval reconstruction','bits':BITS,'scale':U,
 'author_input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'pi_identity':'16 atan(1/5)-4 atan(1/239)',
 'orders':len(results),'guard_count':sum(r['guard_count'] for r in results),'negative_controls':negatives,'results':results}
(HERE/'b27_independent_interval_review.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='results'},indent=2))
