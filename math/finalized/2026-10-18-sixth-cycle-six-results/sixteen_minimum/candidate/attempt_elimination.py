"""Fresh exact characteristic-zero Groebner attempt, independently resource-bounded.
No historical research program is read or executed. Uses installed SymPy only.
"""
import json, pathlib, resource, sys, time
ROOT=pathlib.Path(__file__).resolve().parent
# Hard bounds apply only to this child process. They do not alter another worker.
resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
resource.setrlimit(resource.RLIMIT_CPU,(180,185))
import sympy as sp
from build_residual import encode_system
n=tuple(map(int,sys.argv[1].split(','))) if len(sys.argv)>1 else (2,2,2,2,2,1,2,1)
start=time.monotonic()
spec=encode_system(n)
x=sp.symbols('x')
K=sp.QQ.alg_field_from_poly(sp.Poly(x**16+1,x),alias='a')
a=K.unit
names=spec['variables']
variables=sp.symbols(' '.join(names))
uindex=len(variables)-1
zero=(0,)*len(variables)
cs=[]
for terms in spec['cyclic_coefficients']:
    cs.append({tuple(e)+(0,):K.convert(v) for e,v in terms})
f=[]
for i in range(1,16):
    row=dict(cs[i]); q=a**(i*i%32)
    for e,v in cs[0].items():
        row[e]=row.get(e,K.zero)-q*v
        if not row[e]:del row[e]
    f.append(sp.Poly.from_dict(row,variables,domain=K))
row={tuple(list(e[:-1])+[1]):v for e,v in cs[0].items()}
row[zero]=row.get(zero,K.zero)-K.one
f.append(sp.Poly.from_dict(row,variables,domain=K))
meta={'counts':n,'field':'Q[a]/(a^16+1)','variables':len(variables),'equations':len(f),
      'input_terms':sum(len(p.terms()) for p in f),'maximum_total_degree':max(p.total_degree() for p in f),
      'order':'grevlex','method':'f5b','cpu_limit_seconds':180,'address_space_limit_bytes':2*1024**3,
      'sympy_version':sp.__version__,'status':'RUNNING','setup_seconds':time.monotonic()-start}
(ROOT/'ELIMINATION_STATUS.json').write_text(json.dumps(meta,indent=2)+'\n')
print(json.dumps(meta),flush=True)
try:
    gb=sp.groebner(f,*variables,domain=K,order='grevlex',method='f5b')
    meta.update({'status':'UNIT_IDEAL' if list(gb.polys)==[sp.Poly(1,*variables,domain=K)] else 'NONUNIT_GROEBNER_BASIS',
      'basis_length':len(gb.polys),'elapsed_seconds':time.monotonic()-start,
      'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss})
    (ROOT/'ELIMINATION_BASIS.txt').write_text(str(gb)+'\n')
except MemoryError:
    meta.update({'status':'RESOURCE_LIMIT_MEMORY','elapsed_seconds':time.monotonic()-start,
      'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss})
(ROOT/'ELIMINATION_STATUS.json').write_text(json.dumps(meta,indent=2)+'\n')
print(json.dumps(meta),flush=True)
