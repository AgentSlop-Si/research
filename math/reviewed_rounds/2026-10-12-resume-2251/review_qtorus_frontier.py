"""Independent review: support isolation and symbolic rank-one exponents.
Does not import or execute supplied archive code. No novelty assessment.
"""
import json
from pathlib import Path
orientations=[lambda a,c,m:(a%m,c%m),lambda a,c,m:(-c%m,(a+c)%m),lambda a,c,m:((a+c)%m,a%m)]
checks=0
for m in range(5,41):
 for a in range(m):
  for c in range(m):
   cases=[([(a,c),(a,c+1)],[(a+1,c+2),(a+1,c+3)],1), ([(a,c),(a+1,c-1)],[(a+3,c-2),(a+4,c-3)],0)]
   for rows,cols,selected in cases:
    for branch,f in enumerate(orientations):
     data=[]
     for x,y in rows:
      ra,rc=f(x,y,m)
      for z,w in cols:
       ca,cc=f(z,w,m);u=(ra-ca)%m;v=(rc-cc)%m
       if branch!=selected:assert u+v>=m
       else:
        assert u+v==m-1
        data.append((u,v,u,(-u*(u+1)//2+ca*v)%m))
     if branch==selected:
      for j,mod in [(0,None),(1,None),(2,2),(3,m)]:
       delta=data[0][j]+data[3][j]-data[1][j]-data[2][j]
       assert delta==0 if mod is None else delta%mod==0
    checks+=1
result={'status':'PASS','m_range':[5,40],'translated_minor_checks':checks,'scope':'Finite controls for the symbolic all-m>=5 support/phase proof; no imported code executed; no unrestricted Fourier bound or novelty claim'}
Path(__file__).resolve().with_name('qtorus_independent_review_controls.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result))
