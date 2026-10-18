"""Fresh bounded execution of the complete original ideal, never a numeric proxy."""
import resource,time,json,sys
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
resource.setrlimit(resource.RLIMIT_CPU,(180,185))
import sympy as s
start=time.time();o=json.load(open('ORIGINAL_IDEAL.json'))
names=[v for v in o['variables'] if v not in o['unobservable_variables']]+['z']
xs=s.symbols(' '.join(names));d=dict(zip(names,xs));z=d['z']
eq=[]
for e in o['equations']:
 f=0
 for t in e['terms']:
  a=sum(v*z**k for k,v in enumerate(t['coefficient']))
  for v in t['monomial']:a*=d[v]
  f+=a
 eq.append(f)
eq.append(z**4+1)
print(json.dumps(dict(event='start_exact_full_ideal',engine='SymPy '+s.__version__,ring='QQ[72 observable stage parameters,z]',equations=len(eq),variables=len(xs),memory_limit_bytes=1024**3,cpu_soft_limit_seconds=180,order='grevlex',method='f5b')),flush=True)
try:
 G=s.groebner(eq,*xs,order='grevlex',domain=s.QQ,method='f5b')
 print(json.dumps(dict(event='returned',elapsed_seconds=time.time()-start,basis_length=len(G.polys),unit_ideal=G.contains(1))),flush=True)
 open('EXACT_BASIS.txt','w').write(str(G))
except MemoryError:
 print(json.dumps(dict(event='memory_limit',elapsed_seconds=time.time()-start)),flush=True)
 sys.exit(42)
