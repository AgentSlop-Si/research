import json,random
from pathlib import Path
import independent_phase38 as m
R=random.Random(38077);out={'status':'PASS','scan_cases':0,'scan_entries':0,'separate_Weyl_failure_cases':0}
for p in [998244353,2013265921]:
 for n in [4,8,16,32,64,128,256]:
  vals=list(map(int,(Path('source')/f'phase38_instance_N{n}_p{p}.txt').read_text().split()))[2:]
  mats=[[[vals[k*n*n+i*n+j] for j in range(n)] for i in range(n)] for k in range(3)];T,G,H=mats
  A,C,F,gg,hh=m.kernels(n,p);assert G==gg and H==hh
  M=[[(G[i][j]+7*H[i][j])%p for j in range(n)] for i in range(n)];v=[T[0][j]*pow(M[0][j],-1,p)%p for j in range(n)];u=[T[i][0]*pow(M[i][0]*v[0]%p,-1,p)%p for i in range(n)]
  M=[[u[i]*M[i][j]*v[j]%p for j in range(n)] for i in range(n)];actual=m.mm(m.mm(A,M,p),C,p)
  root=pow(3 if p==998244353 else 31,(p-1)//n,p);roots=[pow(root,i,p) for i in range(n)]
  assert any((actual[i][(j+1)%n]-roots[i]*actual[i][j])%p for i in range(n) for j in range(n))
  assert any((roots[j]*actual[i][j]-actual[(i+1)%n][j])%p for i in range(n) for j in range(n));out['separate_Weyl_failure_cases']+=1
  ii=roots[n//4]
  for order,(a,b,d) in zip(m.orders(n),[(1,1,4),(2,1,7),(1,2,8),(1,-1,5),(2,1,9),(1,1,6)]):
   alpha=(a+b*ii)*pow(d,-1,p)%p;x=[R.randrange(p) for j in range(n)];z=0
   for j in order:z=(alpha*z+x[j])%p
   z=z*pow(1-pow(alpha,n,p),-1,p)%p;y=[0]*n
   for j in order:z=(alpha*z+x[j])%p;y[j]=z
   assert all((y[order[j]]-alpha*y[order[(j-1)%n]])%p==x[order[j]] for j in range(n));out['scan_cases']+=1;out['scan_entries']+=n
  if n==64 and p==2013265921:
   f,g=m.gate(T,G,H,[53,55,19,26,5],p);l=[(f[i]*g[2]-g[i]*f[2])%p for i in range(2)];assert l[1];r=-l[0]*pow(l[1],-1,p)%p
   assert sum(f[i]*pow(r,i,p) for i in range(3))%p==sum(g[i]*pow(r,i,p) for i in range(3))%p==0
   out['modular_collision']={'root':r,'gcd_degree':1,'mapping':[53,55,19,26,5]}
Path('ADDITIONAL_RESULTS.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(out)
