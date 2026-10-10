"""Fresh self-authored controls for proved disk/overlap lemma; no archived tests used."""
import json
from pathlib import Path
import sympy as S
from sympy.polys.domains import AlgebraicField
from sympy.polys.rings import ring
q=S.symbols('q');out=Path(__file__).resolve().parent
rows=[]
for d in [3,7,11,15,19]:
 K=AlgebraicField(S.QQ,(S.Poly(S.cyclotomic_poly(d,q),q),S.Symbol('w')));R,y=ring('y',K);w=K.unit
 b=(d-1)//2;H0,H1=R.one,1+y
 for n in range(2,b+1): H0,H1=H1,(1+y)*H1+(R(w**(n-1))-1)*y*H0
 U,rem=divmod(H1,1+y);assert not rem
 g=U.evaluate(y,-1); assert g
 W=K.one
 for j in range(1,b+1):W*=1-w**j
 for j in range(1,(b+d)//2+1): W/=1-w**(2*j)
 tau=d*W/g
 def conj(a):
  ans=K.zero
  for c in a.to_list(): ans=ans/w+c
  return ans
 assert K.one/tau+K.one/conj(tau)==K.one
 assert (tau-1)*(conj(tau)-1)==K.one
 polys=[R.one,y]
 for A in range(2,22):polys.append(y*polys[-1]-(A-1)*polys[-2])
 for A in range(1,21):
  J=y*polys[A]-R(tau)*polys[A].diff(y)
  disc=J.discriminant();assert disc
  # Exact Hermite ODE and local parameter expression.
  assert polys[A].diff(y).diff(y)-y*polys[A].diff(y)+A*polys[A]==0
  rows.append(dict(d=d,A=A,squarefree=True))
 print('d',d,'A1..20 exact squarefree and reciprocal identity',flush=True)
(out/'fresh_overlap_results.json').write_text(json.dumps(dict(method=__doc__,checks=len(rows),rows=rows),indent=2))
