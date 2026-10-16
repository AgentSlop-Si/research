import importlib.util,sys,random,json,hashlib
from pathlib import Path
source=Path(sys.argv[1] if len(sys.argv)>1 else 'alg007_fallback_contract_0817/publication_safe/alg007_bounded_adapter.py')
assert hashlib.sha256(source.read_bytes()).hexdigest()=='b41f85a2492d6d47749aff4f57188fa5872dd0c77c027b6a93ccefeaee216bd8'
spec=importlib.util.spec_from_file_location('new_adapter',source); mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
p=mod.P;rng=random.Random(20261016);calls=0;coords=0;routes={}
for n in (4,8,16,32,64):
 for m in (2,4,8):
  if n%m or n//m<m:continue
  w=pow(31,(p-1)//n,p)
  for a in (1,n-1):
   for beta in (0,1,n-1):
    cases=[[0]*n,[1]*n,[rng.randrange(p) for _ in range(n)]]
    # One independently synthesized block mode: inverse of the twist.
    cases.append([pow(w,-(a*t*(t-1)//2+(a*m*(j//m)+beta)*t),p) for j in range(n) for t in [j%m]])
    for x in cases:
     expected=tuple(sum(v*pow(w,-j*k,p) for j,v in enumerate(x))%p for k in range(n))
     for cap in (0,1,m):
      for budget in (0,1,23,1000,10000000):
       got=mod.transform(x,m,cap,a=a,beta=beta,attempt_budget=budget)
       assert got['values']==expected,(n,m,a,beta,cap,budget)
       ledger=got['ledger'];assert ledger['attempt_spent']<=budget
       assert ledger['attempt_spent']==sum(sum(c.values()) for phase,c in ledger['phases'].items() if phase in ('recognition','decode'))
       assert ledger['total_units']==sum(ledger['total'].values())
       assert ledger['total']['output_coordinate']==n
       routes[got['route']]=routes.get(got['route'],0)+1;calls+=1;coords+=n
# nontrivial supplied primitive roots, including inverse root
for n in (8,16,32):
 w=pow(31,(p-1)//n,p)
 x=list(range(n))
 for exponent in (3,n-1):
  root=pow(w,exponent,p)
  expected=tuple(sum(v*pow(root,-j*k,p) for j,v in enumerate(x))%p for k in range(n))
  for budget in (0,10000000):
   got=mod.transform(x,2,2,root=root,attempt_budget=budget)
   assert got['values']==expected;routes[got['route']]=routes.get(got['route'],0)+1;calls+=1;coords+=n
assert sum(routes.values())==calls
result={'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'calls':calls,'coordinates':coords,'routes':routes,'scope':'Independent direct-DFT and ledger invariants for new self-authored module only; no historical program run','pass':True}
Path(__file__).resolve().parent.joinpath('RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
