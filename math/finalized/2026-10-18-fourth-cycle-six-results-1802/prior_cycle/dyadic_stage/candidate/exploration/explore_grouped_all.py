import sympy as s,itertools,time,json
N=16
for r in [5,6,7]:
 for ns in itertools.product(range(r+1),repeat=4):
  if sum(ns)!=r: continue
  # cyclic action 1,3,7,5 -> 1; instead use ordered (1,3,7,5)
  if ns!=max(ns[i:]+ns[:i] for i in range(4)):continue
  vs=[];cs=[s.Integer(0)]*N;cs[0]=s.Integer(1)
  for stride,n in zip([1,3,7,5],ns):
   cv=s.symbols('a'+str(stride)+':'+str(n+1)) if False else [s.Symbol(f'a{stride}_{j}') for j in range(1,n+1)]
   vs+=cv;cs=[s.expand(cs[i]+sum(cv[j-1]*cs[(i-stride*j)%N] for j in range(1,n+1))) for i in range(N)]
  eq=[s.expand((-1)**i*cs[i]-cs[(i-8)%N]) for i in range(8)]
  tt=time.time();g=s.groebner(eq,*vs,modulus=17)
  print(r,ns,'unit',list(g)==[1],'secs',round(time.time()-tt,4),'basis',list(g) if list(g)!=[1] else '',flush=True)
