"""Independent mathematical audit. Reads candidate JSON/text; imports no candidate code."""
from pathlib import Path
import hashlib,json,itertools,math
import sympy as s
ROOT=Path(__file__).resolve().parent.parent/'candidate'
OUT=Path(__file__).parent
results={}
manifest=json.loads((ROOT/'MANIFEST.json').read_text())
for e in manifest['canonical_files']:
 b=(ROOT/e['path']).read_bytes();assert len(b)==e['bytes'];assert hashlib.sha256(b).hexdigest()==e['sha256']
results['manifest_entries_verified']=len(manifest['canonical_files'])
assert hashlib.sha256((ROOT/'REPORT.md').read_bytes()).hexdigest()=='0b966bf02a815e93a5437040d78ee97620906bea70279d59a57100eff39cc3c5'
for e in json.loads((ROOT/'SOURCE_BINDINGS.json').read_text()):
 b=(ROOT/e['path']).read_bytes();assert len(b)==e['bytes'];assert hashlib.sha256(b).hexdigest()==e['sha256']
results['inherited_source_bindings_verified']=4
x=s.Symbol('x');v=s.symbols('v0:5')
def decode(poly):
 assert len({tuple(e) for e,n,d in poly})==len(poly)
 assert all(len(e)==5 and all(isinstance(k,int) and k>=0 for k in e) and isinstance(n,int) and isinstance(d,int) and d>0 for e,n,d in poly)
 return s.Poly(sum(s.Rational(n,d)*s.prod(w**k for w,k in zip(v,e)) for e,n,d in poly),*v,domain=s.QQ)
data=json.loads((ROOT/'PARITY_CERTIFICATES.json').read_text())
assert data['N']==16 and data['stride_order']==[1,3,7,5] and data['coefficient_domain']=='Q' and data['parity_sign']==1
records=data['patterns'];assert len(records)==14
patterns=[c for c in itertools.product(range(6),repeat=4) if sum(c)==5]
assert len(patterns)==56
orbits={max(tuple(c[k:]+c[:k]) for k in range(4)) for c in patterns}
assert orbits=={tuple(r['counts']) for r in records}
terms=0;den_primes=set();max_degree=0
for rec in records:
 count=rec['counts'];j=0;groups=[];names=[]
 for stride,c in zip([1,3,7,5],count):
  groups.append(1+sum(v[j+k-1]*x**(stride*k) for k in range(1,c+1)))
  names.extend(f'a{stride}_{k}' for k in range(1,c+1));j+=c
 assert j==5 and names==rec['variables']
 ordinary=s.Poly(s.prod(groups),x)
 cyclic=[sum(coef for (power,),coef in ordinary.terms() if power%16==i) for i in range(16)]
 fs=[s.Poly((-1)**i*cyclic[i]-cyclic[i+8],*v,domain=s.QQ) for i in range(8)]
 assert fs==[decode(f) for f in rec['inputs']]
 hs=[decode(h) for h in rec['multipliers']];assert len(hs)==8
 total=sum((f*h for f,h in zip(fs,hs)),s.Poly(0,*v,domain=s.QQ))
 assert total==s.Poly(1,*v,domain=s.QQ)==decode(rec['target'])
 mod_total=s.Poly(0,*v,modulus=17)
 for f,h in zip(fs,hs):
  def reduction(p):
   return s.Poly.from_dict({e:int(c.p)*pow(int(c.q),-1,17)%17 for e,c in p.terms()},v,modulus=17)
  mod_total+=reduction(f)*reduction(h)
  terms+=len(h.terms()) if not h.is_zero else 0
  if not h.is_zero and not f.is_zero:max_degree=max(max_degree,(f*h).total_degree())
  for _,c in h.terms():den_primes.update(s.factorint(c.q))
 assert mod_total==s.Poly(1,*v,modulus=17)
 # Independently verify that changing one nonzero multiplier coefficient breaks its identity.
 k=next(k for k,(f,h) in enumerate(zip(fs,hs)) if not f.is_zero and not h.is_zero)
 assert total+fs[k]!=s.Poly(1,*v,domain=s.QQ)
 assert fs[k]+1!=decode(rec['inputs'][k])
assert terms==182 and max_degree==13 and den_primes=={2,3,5,7}
results['parity']={'identities_Q':14,'identities_F17':14,'equations_rebuilt_from_ordinary_grouped_products':112,'five_factor_patterns':56,'multiplier_terms':terms,'largest_product_degree':max_degree,'denominator_primes':sorted(map(int,den_primes)),'independent_mutation_controls':28}
print('Parity identities, equation bindings, orbit coverage, hashes: PASS',flush=True)
# Integral cyclotomic calculations via symbolic polynomial remainders, not candidate routines.
a=s.Symbol('a')
def cyclic_a(expr,N):return s.rem(s.Poly(expr,a,domain=s.ZZ),s.Poly(a**N+1,a,domain=s.ZZ)).as_expr()
N=16
q=[cyclic_a(a**(t*t%(2*N)),N) for t in range(N)]
c=[cyclic_a(a**((-t*t)%(2*N)),N) for t in range(N)]
entries=0
for i in range(N):
 for j in range(N):
  z=cyclic_a(sum(c[(i-k)%N]*q[(k-j)%N] for k in range(N)),N)
  assert z==(N if i==j else 0);entries+=1
# Independently bind the displayed expanded Q16 and all shift/parity normalizations.
qdisplay=[1,a,a**4,a**9,-1,-a**9,a**4,-a,1,-a,a**4,-a**9,-1,a**9,a**4,a]
assert q==qdisplay
for r in range(16):
 for t in range(16):assert cyclic_a(q[(t-r)%16]-a**((r*r-2*r*t)%32)*q[t],16)==0
assert [(-1)**i*q[i] for i in range(16)]==[q[(i-8)%16] for i in range(16)]
assert cyclic_a(sum(c[(-k)%16]*(2 if k==1 else 1)*q[k] for k in range(16)),16)!=16
results['N16_integral_matrix_entries']=entries
results['shift_normalizations']=256
# Norm computed independently by even/odd parts: Q(x)Q(-x)=A(y)^2-y B(y)^2.
y=s.Symbol('y');norm_sizes=[]
for N in [4,8,16,32,64]:
 n=N//2;qq=[cyclic_a(a**(t*t%(2*N)),N) for t in range(N)]
 A=sum(qq[2*i]*y**i for i in range(n));B=sum(qq[2*i+1]*y**i for i in range(n))
 actual=s.rem(s.Poly(A*A-y*B*B,y),s.Poly(y**n-1,y))
 H=cyclic_a(sum((-1)**t*a**((2*t*t)%(2*N)) for t in range(N)),N)
 assert H!=0
 expected=s.Poly(H*sum((-1)**i*a**((2*i*i)%(2*N))*y**i for i in range(n)),y)
 diff=actual-expected
 assert all(cyclic_a(diff.nth(i),N)==0 for i in range(n))
 norm_sizes.append(N)
results['integral_norm_via_even_odd_decomposition']=norm_sizes
print('Integral inverse matrix, shifts, target coefficients, dyadic norms: PASS',flush=True)
# Norm pole guards verified by evaluation on every root, without convolution formula.
guards={};evaluations=0
for N,p in [(8,17),(16,97),(32,193)]:
 omega=pow(int(s.primitive_root(p)),(p-1)//N,p);roots=[pow(omega,k,p) for k in range(N)];count=0
 for stride in range(1,N):
  for alpha in range(p):
   vals=[(1-alpha*pow(root,stride,p))%p for root in roots]
   legal=all(vals)
   assert legal==(pow(alpha,N//math.gcd(N,stride),p)!=1)
   if not legal:continue
   for k in range(N//2):
    yy=roots[k]*roots[k]%p
    d=(1-alpha*alpha*pow(yy,stride,p))%p if stride%2 else (1-alpha*pow(yy,stride//2,p))%p
    assert d!=0
    assert vals[k]*vals[k+N//2]%p==(d if stride%2 else d*d%p)
    evaluations+=1
   count+=1
 guards[str(N)]=count
assert guards=={'8':77,'16':1285,'32':5301}
results['legal_norm_factor_cases']=guards;results['rootwise_norm_checks']=evaluations
# Finite-field construction and splitting certificate using SymPy's independent factorization.
z=s.Symbol('z')
R=s.Poly(sum(pow(6,t*(t+1)//2,17)*z**t for t in range(16)),z,modulus=17)
gs=[s.Poly(z-1,z,modulus=17),s.Poly(z**4+2*z**3-4*z**2+2*z+1,z,modulus=17),s.Poly(z**4-6*z**3+8*z**2-6*z+1,z,modulus=17),s.Poly(z**6-6*z**5+3*z**4+6*z**3+3*z**2-6*z+1,z,modulus=17)]
assert s.prod(gs)*(-1)==R
assert all(g.is_irreducible for g in gs)
assert R.factor_list()==(s.Integer(-1),[(g,1) for g in gs])
assert math.lcm(*[g.degree() for g in gs],2)==12
# Q16(a z) coefficient rescaling and primitive root in F17[t]/(t^2-3).
t=s.Symbol('t');mod=s.Poly(t*t-3,t,modulus=17)
def f17reduce(e):return s.rem(s.Poly(e,t,modulus=17),mod)
assert mod.is_irreducible
assert f17reduce(t**16)==s.Poly(-1,t,modulus=17)
assert f17reduce(t**32)==s.Poly(1,t,modulus=17)
assert f17reduce(t*(6*t))==s.Poly(1,t,modulus=17)
for k in range(16):assert f17reduce((6*t)**(k*k+k))==s.Poly(R.nth(k),t,modulus=17)
# Root guard independently expressed as gcd(R(z), (a*z)^16-1)=1; a^16=-1.
assert s.gcd(R,s.Poly(z**16+1,z,modulus=17)).degree()==0
results['finite_factor_degrees']=[g.degree() for g in gs]
results['finite_splitting_extension_degree']=12
results['finite_pole_gcd']=1
print('All rootwise norm checks and finite splitting certificate: PASS',flush=True)
# In-place recurrence on every basis vector and every legal alpha in F97; exact counters.
application_cases=0
p=97;N=16
for alpha in range(p):
 if pow(alpha,N,p)==1:continue
 alpha16=alpha;setupM=0
 for _ in range(4):alpha16=alpha16*alpha16%p;setupM+=1
 assert alpha16==pow(alpha,16,p) and setupM==4
 d=pow(1-alpha16,-1,p)
 for k in range(N):
  xx=[int(i==k) for i in range(N)];buf=xx[:];h=buf[0];M=A=0
  for i in range(1,N):h=(alpha*h+buf[i])%p;M+=1;A+=1
  buf[15]=d*h%p;M+=1
  for i in range(15):buf[i]=(buf[i]+alpha*buf[i-1])%p;M+=1;A+=1
  assert all((buf[i]-alpha*buf[i-1])%p==xx[i] for i in range(N))
  assert (M,A)==(31,30);application_cases+=1
assert (15*31+16,15*30)==(481,450)
assert (15*31+16+15*4,15*30+15,15)==(541,465,15)
results['recurrence_basis_cases']=application_cases
results['per_resolvent_cost']={'M':31,'A':30}
results['fifteen_stages_plus_scalar']={'M':481,'A':450}
results['setup_plus_one_vector_excluding_F_coeff']={'M':541,'A':465,'Inv':15}
results['all_checks_passed']=True
(OUT/'INDEPENDENT_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
