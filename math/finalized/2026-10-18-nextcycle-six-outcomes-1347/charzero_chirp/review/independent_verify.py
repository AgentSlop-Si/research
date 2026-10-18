"""Independent review: no candidate executable is imported or run."""
from pathlib import Path
import hashlib, json, time
import sympy as s
SRC=Path(__file__).resolve().parent.parent/'candidate'
OUT=Path(__file__).resolve().parent
x,t,D,E=s.symbols('x t D E')
result={}
manifest=json.loads((SRC/'MANIFEST.json').read_text())
for f in manifest['canonical_files']:
 data=(SRC/f['path']).read_bytes()
 assert hashlib.sha256(data).hexdigest()==f['sha256']
 assert len(data)==f['bytes']
result['frozen_manifest_verified']=len(manifest['canonical_files'])
result['report_sha256']=hashlib.sha256((SRC/'REPORT.md').read_bytes()).hexdigest()
# Ring Z[t]/Phi16: t=a=zeta^{-1}; direct matrix multiplication, all 64 entries.
phi=t**8+1
def red0(v): return s.rem(s.expand(v),phi,t)
C=s.Matrix(8,8,lambda i,j:red0(t**(-((i-j)**2)%16)))
Q=s.Matrix(8,8,lambda i,j:red0(t**(((i-j)**2)%16)))
for i in range(8):
 for j in range(8):
  assert red0(sum(C[i,k]*Q[k,j] for k in range(8)))==(8 if i==j else 0)
result['characteristic_zero_matrix_entries']=64
# Independent SymPy sparse arithmetic for the exact finite-field ideal witnesses.
cs=json.loads((SRC/'CERTIFICATES.json').read_text())
def unpack(raw): return s.Poly(sum(c*D**m[0]*E**m[1] for m,c in raw),D,E,modulus=17)
for name in ['510','420','330','411','312']:
 c=cs[name]
 lhs=sum((unpack(f)*unpack(h) for f,h in zip(c['inputs'],c['multipliers'])),s.Poly(0,D,E,modulus=17))
 assert lhs==unpack(c['target'])
result['independent_ideal_identities']=['510','420','330','411','312']
# Bind rational expressions after deriving them from original coefficients by hand.
a,b=6,4
h=D/(D+a*E); A=a*h/E; B=-a*h/D; Cc=(b*h-E)/D; F=E*(s.Rational(b,a)+1/D)
eqs={'330':[A+Cc*E+F-a*h,Cc+D+B*F+a*h,A*D+Cc*F-h]}
R=1-E**2-D**2*E; A=D**3/R; Cc=-D-A*E; B=E-D**2-A*D*E
u=A*D;v=B;r=-B*D;tt=-A*E
ls=[(v-b*u,u-b*v),(r+tt,r-tt),(r-a*u,-tt-a*v)]
eqs['312']=[1+B*E-A*D]+[ls[i][0]*ls[j][1]-ls[i][1]*ls[j][0] for i,j in [(0,1),(0,2),(1,2)]]
eqs['510']=[a*D**2-D+a,b*D**4+a*D**3+D**2+a*D+b]
EE=b+a*D+a/D;h=D/(D+a*EE)
eqs['420']=[EE-D**2-h*(a*D+b),a/EE-a*EE-D*EE/h-a]
B=-2*D**2/(1+D**4);A=2*D**3/(1+D**4);H=D*(D**4-1)/(1+D**4);e=(b-B)/(1-b*B)
eqs['411']=[A+H+(A-H)*e,A-H*e-a*(1+B*e)]
for name,fs in eqs.items():
 for expression,packed in zip(fs,cs[name]['inputs']):
  numerator,denominator=s.cancel(expression).as_numer_denom()
  assert s.Poly(numerator,D,E,modulus=17)==unpack(packed)
  assert not s.Poly(denominator,D,E,modulus=17).is_zero
result['certificate_input_lists_rederived']=list(eqs)
# Direct algebraic-closure exclusion for all nine normalized length-five patterns
# having >=4 odd factors. Constant-normalized grouped polynomial coefficients
# are free; h*z=1 enforces target invertibility. No finite-point enumeration.
q=[pow(6,k*k,17) for k in range(8)]
patterns=[(n1,n2,n3,5-n1-n2-n3) for n1 in range(6) for n2 in range(6-n1) for n3 in range(6-n1-n2) if n1>=n3 and n1+n3>=4]
gbresults={}
for counts in patterns:
 p=1;vs=[]
 for stride,n in enumerate(counts,1):
  vv=s.symbols(f'c{stride}_1:{n+1}');vs.extend(vv)
  p*=1+sum(v*x**(stride*k) for k,v in enumerate(vv,1))
 p=s.Poly(s.rem(s.expand(p),x**8-1,x),x)
 h,z=s.symbols('h z'); fs=[p.nth(k)-h*q[k] for k in range(8)]+[h*z-1]
 st=time.monotonic();gb=s.groebner(fs,*vs,h,z,modulus=17,order='grevlex')
 assert list(gb)==[1],(counts,gb)
 gbresults[str(counts)]=round(time.monotonic()-st,4)
 print('Direct lower-five ideal:',counts,gbresults[str(counts)],flush=True)
result['direct_lower_five_unit_ideals']=gbresults
# Independently verify concrete F17^3 construction using polynomial remainders.
w=json.loads((SRC/'FINITE_WITNESS.json').read_text())
f=t**3+8*t**2+6*t+8
assert s.Poly(f,t,modulus=17).is_irreducible
f2=t**3+10*t**2+4*t+1
assert s.Poly(f2,t,modulus=17).is_irreducible
def red(v): return s.rem(s.Poly(v,t,modulus=17),s.Poly(f,t,modulus=17)).as_expr()
def cv(v): return sum(c*t**i for i,c in enumerate(v))
alphas=[cv(v) for v in w['alphas']]
poly=[s.Integer(1)]+[s.Integer(0)]*7
literal=[s.Integer(1)]+[s.Integer(0)]*7
for alpha in alphas:
 guard=red(1-alpha**8); assert guard!=0
 invguard=s.invert(s.Poly(guard,t,modulus=17),s.Poly(f,t,modulus=17)).as_expr()
 factor=[red(red(alpha**k)*invguard) for k in range(8)]
 literal=[red(sum(literal[j]*factor[(k-j)%8] for j in range(8))) for k in range(8)]
 poly=[red(poly[k]-alpha*poly[(k-1)%8]) for k in range(8)]
assert all(red(poly[k]-q[k])==0 for k in range(8))
for i in range(8):
 for j in range(8):
  assert red(8*literal[(i-j)%8]-pow(3,(i-j)**2,17))==0
result['finite_extension_field_irreducible']=True
result['finite_extension_pole_guards']=7
result['finite_extension_full_matrix_entries']=64
result['status']='PASS'
(OUT/'INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
