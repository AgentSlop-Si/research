"""Fresh independent exact controls; no predecessor implementation imports."""
import sympy as s,json,math,hashlib,time
from pathlib import Path
OUT=Path(__file__).parent;q,z,x,y=s.symbols('q z x y')
protected_dirs=['ramified_chirp_squarefreeness_0341','ramified_chirp_independent_audit_0352','diagonal_chirp_classification_0246']
protected=[p for name in protected_dirs for p in (OUT.parent/name).rglob('*') if p.is_file()]
def hashes():return {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
before=hashes();(OUT/'PRESERVATION_BEFORE.json').write_text(json.dumps(before,indent=2))
cache={}
def H(n):
 if n not in cache:
  row=[s.Integer(1)]
  for a in range(1,n+1):row=[s.Integer(1)]+[s.expand(row[k]+q**(a-k)*row[k-1]) for k in range(1,a)]+[s.Integer(1)]
  cache[n]=s.expand(sum(c*z**k for k,c in enumerate(row)))
 return cache[n]
def red(f,d):return s.rem(f,s.cyclotomic_poly(d,q),q)
def disc_reciprocal(h,n):
 extra=s.Integer(1)
 if n%2:
  h,rem=s.div(h,z+1,z);assert rem==0
  extra=s.expand(h.subs(z,-1)**2);n-=1
 r=n//2;p=s.Poly(h,z);basis=[s.Integer(2),y]
 for k in range(2,r+1):basis.append(s.expand(y*basis[-1]-basis[-2]))
 c=p.nth(r)+sum(p.nth(r+j)*basis[j] for j in range(1,r+1))
 return s.expand(extra*c.subs(y,2)*c.subs(y,-2)*s.discriminant(c,y)**2)
def data(d,b):
 ph=s.cyclotomic_poly(d,q);u=s.div(H(b),z+1,z)[0];g=red(u.subs(z,-1),d)
 m=(b+d)//2
 num=den=s.Integer(1)
 for k in range(1,b+1):num=red(num*(1-q**k),d)
 for k in range(1,m+1):den=red(den*(1-q**((2*k)%d)),d)
 w=red(num*s.invert(den,ph,q),d);tau=red(d*w*s.invert(g,ph,q),d)
 delta=red(s.discriminant(u,z),d) if b>1 else s.Integer(1)
 R=red(s.resultant(z**d+1,u,z),d)
 return g,w,tau,delta,R
results={'local_models':[],'ordinary_discriminants':[],'inversion_identities':[],'hermite_wronskians':[],'exception_certificates':[]}
for n in range(2,13):assert s.expand(H(n)-(1+z)*H(n-1)-(q**(n-1)-1)*z*H(n-2))==0
results['q_pascal_recurrence_through_n']=12
for d,A,b in [(3,1,1),(3,2,1),(3,3,1),(3,4,1),(7,1,3),(7,2,3),(11,1,5)]:
 n=d*A+b;g,w,tau,delta,R=data(d,b);t0=s.Integer(1);t1=-x
 ts=[t0,t1]
 for a in range(2,A+1):ts.append(s.expand(-x*ts[-1]-s.Rational(a-1,d)*ts[-2]))
 predicted=red((-1)**A*d**A*(g*x*ts[A]+A*w*ts[A-1]),d)
 terms=s.Poly(H(n),q,z).terms()
 for e in range(A+2):
  actual=0
  for ell in range(e+1):
   if (e-ell)%2:continue
   j=(e-ell)//2
   for (r,k),c in terms:
    if k>=ell:actual+=c*q**(r%d)*s.binomial(s.Rational(r,d),j)*s.binomial(k,ell)*(-1)**(k-ell)*x**ell
  actual=red(actual,d)
  assert s.expand(actual-(predicted if e==A+1 else 0))==0,(d,A,b,e)
 results['local_models'].append({'d':d,'A':A,'b':b,'n':n,'leading':str(predicted)})
 print('local model',d,A,b,'pass',flush=True)
Ds={}
for d,A,b in [(3,1,1),(3,2,1),(3,3,1),(7,1,3)]:
 n=d*A+b;L=d*A*(A-1)//2+A;ph=s.cyclotomic_poly(d,q)
 if n not in Ds:Ds[n]=disc_reciprocal(H(n),n)
 D=Ds[n];E,rem=s.div(D,ph**L,q);assert rem==0
 g,w,tau,delta,R=data(d,b)
 J=x*s.hermite_prob(A,x)-A*tau*s.hermite_prob(A-1,x)
 S=red(s.discriminant(J,x),d);P=math.prod(j**j for j in range(1,A+1))
 C=red((-1)**(A*(d-1)//2)*d**(d*A*(A+1)//2+A)*P**(d-1)*S*delta*R**(2*A)*g**2,d)
 Q=s.div(q**d-1,ph,q)[0]
 observed=red(E,d);expected=red(Q**L*C,d)
 assert observed==expected and observed!=0,(d,A,b)
 results['ordinary_discriminants'].append({'d':d,'A':A,'b':b,'n':n,'order':L,'C':str(C),'normalized_quotient_at_root':str(observed)})
 print('discriminant',d,A,b,'pass',flush=True)
for n in range(2,8):assert s.expand(disc_reciprocal(H(n),n)-s.discriminant(H(n),z))==0
results['direct_discriminant_crosscheck_through_n']=7
for d in [3,7,11,15,19]:
 b=(d-1)//2;g,w,tau,_,_=data(d,b);v=red(d*w,d)
 gi=red(g.subs(q,q**(d-1)),d);vi=red(v.subs(q,q**(d-1)),d)
 assert red(g*vi+gi*v-v*vi,d)==0
 results['inversion_identities'].append({'d':d,'g':str(g),'v':str(v)})
for p in [3,7,11,19,23,31]:
 A=(p-1)//2;U=s.hermite_prob(A,x)
 V=sum(abs(c)*x**mon[0] for mon,c in s.Poly(U,x).terms())
 W=s.expand(s.diff(U,x)*V-U*s.diff(V,x)-x*U*V+x**p)
 assert s.Poly(W,x,modulus=p).is_zero
 results['hermite_wronskians'].append({'p':p,'A':A})
# Only specified existing exceptional orders, read inert JSON; no supplied code is run.
source=OUT.parent/'diagonal_chirp_classification_0246/MODULAR_CERTIFICATES.json'
certs=[c for c in json.loads(source.read_text()) if c['N'] in [9,45,49,121,361]]
assert sorted(c['N'] for c in certs)==[9,45,49,121,361]
def primality(p):return p>=2 and all(p%d for d in range(2,math.isqrt(p)+1))
def trim(a):
 while len(a)>1 and a[-1]==0:a.pop()
 return a
def mul(a,b,p):
 c=[0]*(len(a)+len(b)-1)
 for i,ai in enumerate(a):
  for j,bj in enumerate(b):c[i+j]=(c[i+j]+ai*bj)%p
 return trim(c)
def add(a,b,p):return trim([( (a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0))%p for i in range(max(len(a),len(b)))])
def evaluate(a,x,p):
 r=0
 for c in reversed(a):r=(r*x+c)%p
 return r
for c in certs:
 N,p,root=c['N'],c['prime_p'],c['primitive_q'];n=(N-1)//2
 assert primality(p) and pow(root,N,p)==1
 assert all(pow(root,N//ell,p)!=1 for ell in s.factorint(N))
 row=[1]
 for a in range(1,n+1):row=[1]+[(row[k]+pow(root,a-k,p)*row[k-1])%p for k in range(1,a)]+[1]
 T=[(-1)**(n+k)*v%p for k,v in enumerate(row)];assert T==c['T']
 deriv=[k*T[k]%p for k in range(1,len(T))]
 bezout=add(mul(c['squarefree_bezout_u'],T,p),mul(c['squarefree_bezout_v'],deriv,p),p)
 assert bezout==[1]
 assert all(evaluate(T,pow(root,k,p),p)!=0 for k in range(N))
 results['exception_certificates'].append({'N':N,'n':n,'prime':p,'root':root,'bezout_identity':True,'all_cycle_nodes_clear':True})
 print('exception',N,'pass',flush=True)
(OUT/'EXCEPTION_CERTIFICATES.json').write_text(json.dumps(certs,indent=2))
(OUT/'CONTROL_RESULTS.json').write_text(json.dumps(results,indent=2))
after=hashes();assert before==after
(OUT/'PRESERVATION.json').write_text(json.dumps({'protected_file_count':len(before),'before':before,'after':after,'unchanged':True},indent=2))
print('All exact controls passed',flush=True)
