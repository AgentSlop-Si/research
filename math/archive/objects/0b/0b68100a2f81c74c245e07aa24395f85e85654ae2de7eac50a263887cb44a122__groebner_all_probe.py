import sympy as S,json,time,sys
from sympy.polys.rings import ring
from sympy.polys.domains import QQ,GF
from sympy.polys.groebnertools import groebner
p=int(sys.argv[1]) if len(sys.argv)>1 else 17
if p:
 K=GF(p);Z=K(2 if p==17 else 3)
else:
 z=S.Symbol('z');root=S.CRootOf(z**4+1,3);K=QQ.algebraic_field(root);Z=K.unit
R,*vs=ring('t0,t1,t2,t3,w',K,order='grevlex')
E=[]
for f in json.load(open('adjacent_anchor_construction_0304/all_row_resultants.json')):
 d={}
 for ex,cs in f:
  d[tuple(ex)]=sum(K(num)/K(den)*Z**j for j,(num,den) in enumerate(cs))
 E.append(R.from_dict(d))
print('start',p,len(E),time.time(),flush=True)
G=groebner(E,R,method='buchberger');print('done',len(G),time.time(),flush=True)
for f in G: print(f,flush=True)
t0,t1,t2,t3,w=vs;t=[t0,t1,t2,t3]
B=[]
for j in range(8):
 a=j-j%2;B.append(1+w*Z**((-a)%8)+(-1)**j*t[j//2]*(1+w*Z**((-(a+1))%8)))
for label,g in [('w',w),('tprod',t0*t1*t2*t3),('pivots',S.prod(B[1:])),('all',w*t0*t1*t2*t3*S.prod(B[1:]))]:
 r=g
 for k in range(1,4):
  r=r.rem(G);print('GUARD_REMAINDER',label,k,len(r),flush=True)
  if not r:break
  r*=g
