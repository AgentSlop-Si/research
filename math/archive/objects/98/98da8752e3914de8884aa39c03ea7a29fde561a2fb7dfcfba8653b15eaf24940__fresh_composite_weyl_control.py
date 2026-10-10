"""Fresh independent integer falsification control; no source code imported."""
import json,math,time
from pathlib import Path
start=time.time(); cases=0; minimum=[]; errors=[]
for N in range(3,26,2):
 m=(N+1)//2; h2=pow(2,-1,N); best=N
 for u in range(N):
  for v in range(N):
   A=(u*u+v*v)%N
   for r in range(N):
    for s in range(N):
     D=(u*s-v*r)%N
     if math.gcd(D,N)!=1: continue
     B=(r*r+s*s)%N; delta=((D-u*r-v*s)*h2)%N
     ga=math.gcd(N,A); gb=math.gcd(N,B); gd=math.gcd(N,delta)
     bound=max(N//gd,min(m,N//ga),min(m,N//gb))
     cases+=1; best=min(best,bound)
     if math.gcd(ga,gd)!=1 or math.gcd(gb,gd)!=1 or bound*bound<N or (delta==0 and bound<m):
      errors.append([N,u,v,r,s,ga,gb,gd,bound])
 minimum.append(dict(N=N,minimum_bound=best))
result=dict(kind="fresh integer exhaustive controls, not proof",cases=cases,all_passed=not errors,errors=errors,minimum_by_N=minimum,seconds=time.time()-start)
Path(__file__).with_name("fresh_composite_weyl_results.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
