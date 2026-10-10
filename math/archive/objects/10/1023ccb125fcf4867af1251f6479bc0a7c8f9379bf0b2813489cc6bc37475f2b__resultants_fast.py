import sympy as S
from sympy.polys.rings import ring
from sympy.polys.domains import QQ
from sympy.polys.groebnertools import groebner
x=S.Symbol('x'); zz=S.CRootOf(x**4+1,3); K=QQ.algebraic_field(zz)
R,*v=ring('t0,t1,t2,t3,w',K);t=v[:4];w=v[4];Z=R.ground_new(K.unit);z=S.Symbol('z');pows=[Z**j for j in range(8)]
def show(f):
 out=0
 for e,c in f.items():
  cc=sum(S.Rational(int(a.numerator),int(a.denominator))*z**j for j,a in enumerate(reversed(c.to_list())))
  out+=cc*S.prod(S.Symbol(str(g))**ee for g,ee in zip(R.gens,e))
 return S.expand(out)
sig=[2,7,5,0,6,1,3,4]
M=[[pows[(r*(j-j%2))%8]+(-1)**j*t[j//2]*pows[(r*(j-j%2+1))%8] for j in range(8)]for r in range(8)]
B=[M[0][j]+w*M[7][j] for j in range(8)]
E=[]
for r in [1,2,3]:
 row=[]
 for j in [1,2,4,5,6]:
  if r in [j,(j+1)%8,sig[j]]:continue
  c=B[sig[j]]*M[(r-1)%8][j]-B[j]*M[(r-1)%8][sig[j]]
  b=B[sig[j]]*M[r][j]-B[j]*M[r][sig[j]]
  row.append((j,b,c))
 for ia in range(len(row)):
  for ib in range(ia+1,len(row)):
   j,b,c=row[ia];jj,bb,cc=row[ib];e=b*cc-bb*c
   guards=[]
   for g in [w]+B:
    while e and not e.rem(g):e=e.exquo(g);guards.append(show(g))
   e=e.monic();E.append(e)
   print('RESULTANT',r,j,jj,'GUARDFACTORS',guards,'terms',len(e),'EXPR',show(e),flush=True)
import json
export=[[[list(e),[[int(a.numerator),int(a.denominator)]for a in reversed(c.to_list())]] for e,c in f.items()] for f in E]
json.dump(export,open('adjacent_anchor_construction_0304/reduced_resultants.json','w'))
print('done',flush=True)
