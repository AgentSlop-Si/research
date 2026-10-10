"""Independent review: direct SymPy algebraic-field discriminants/resultants.
Never imports or executes a supplied research script. Inputs are JSON certificates only.
"""
from pathlib import Path
import hashlib,json,time
from math import gcd,prod
from functools import reduce
import sympy as S
ROOT=Path(__file__).resolve().parent
SRC=ROOT.parents[1]/'discriminant_note'/'certificates'
q,z,t=S.symbols('q z t')
rows=[]
for s in [3,7,11,15,19]:
 start=time.time(); phi=S.Poly(S.cyclotomic_poly(s,q),q)
 K=S.QQ.alg_field_from_poly(phi,alias='w');w=K.ext;wk=K.unit
 def elem(x):return K.from_sympy(x)
 def vec(a):
  a=elem(a) if not isinstance(a,K.dtype) else a
  out=list(reversed(a.to_list()))
  assert all(x.denominator==1 for x in out)
  return [int(x) for x in out]+[0]*(phi.degree()-len(out))
 def invol(a):
  a=elem(a) if not isinstance(a,K.dtype) else a
  out=K.zero; wi=wk**(s-1)
  for c in a.to_list():out=out*wi+K.convert(c)
  return out
 b=(s-1)//2;r=(s-3)//4
 h0=S.Poly(1,z,domain=K);h1=S.Poly(1+z,z,domain=K)
 for n in range(2,b+1):
  h0,h1=h1,S.Poly(1+z,z,domain=K)*h1+S.Poly.from_dict({(1,):wk**(n-1)-K.one},z,domain=K)*h0
 H=h1
 U,rem=H.div(S.Poly(z+1,z,domain=K));assert rem.is_zero
 g=U.rep.eval(-1);v=K.one
 for j in range(1,r+1):v*=K.one-wk**(2*j)
 for j in range(b):v*=K.one-wk**(2*j+1)
 delta=2*g-v
 du=U.rep.discriminant() if U.degree() else K.one
 res=S.Poly(z**s+1,z,domain=K).rep.resultant(U.rep)
 gamma=du*res;pair=gamma*invol(gamma);aug=pair*delta
 data=json.loads((SRC/f'EXACT_CONTENT_S{s}.json').read_text())
 own={'U':[vec(U.rep.nth(j)) for j in range(U.degree()+1)],'g':vec(g),'v':vec(v),'delta':vec(delta),'disc_U':vec(du),'res_F_U':vec(res),'Gamma':vec(gamma),'Gamma_pair':vec(pair),'augmented':vec(aug)}
 matches={name:value==data[name] for name,value in own.items()};assert all(matches.values()),(s,matches)
 # Independently reconstruct the reciprocal transform from U coefficients.
 P=S.Poly(0,t,domain=K);Sk0=S.Poly(2,t,domain=K);Sk1=S.Poly(t,t,domain=K)
 P+=S.Poly.from_dict({(0,):U.rep.nth(r)},t,domain=K)
 for j in range(1,r+1):
  if j==1:Sk=Sk1
  else:Sk0,Sk1=Sk1,S.Poly(t,t,domain=K)*Sk1-Sk0;Sk=Sk1
  P+=Sk.mul_ground(U.rep.nth(r+j))
 assert [vec(P.rep.nth(j)) for j in range(P.degree()+1)]==data['P']
 assert g*invol(v)+invol(g)*v==v*invol(v)
 content=reduce(gcd,vec(aug));expected={3:1,7:7**2,11:11**5,15:3**12*5**9,19:19**11}[s]
 assert content==expected
 reviewer=json.loads((SRC/f'INDEPENDENT_EXACT_S{s}.json').read_text())
 assert sum(a*b for a,b in zip(vec(aug),reviewer['augmented_gcd_bezout_coefficients']))==content
 row={'s':s,'direct_discriminant_resultant_matches':matches,'P_matches':True,'inverse_identity':True,'content':content,'bezout_verified':True,'elapsed_seconds':round(time.time()-start,3)}
 rows.append(row);print(json.dumps(row),flush=True)
(ROOT/'independent_discriminant_direct_results.json').write_text(json.dumps(rows,indent=2)+'\n')
