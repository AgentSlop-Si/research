"""Fresh exact reviewer controls for the augmented-content argument."""
import sympy as S, json, math, pathlib
q,z,y,t=S.symbols('q z y t');out=pathlib.Path('research_cycle_0958/review/supplement_v1')
records=[]
for s in [3,7,11]:
 b=(s-1)//2; phi=S.cyclotomic_poly(s,q)
 def red(f): return S.rem(S.expand(f),phi,q)
 def conj(f): return red(f.subs(q,q**(s-1)))
 hp=S.Integer(1); h=z+1
 for n in range(2,b+1): hp,h=h,S.expand((1+z)*h+(q**(n-1)-1)*z*hp)
 u,rem=S.div(h,z+1,z); assert rem==0
 g=red(u.subs(z,-1));v=S.Integer(1)
 for j in range(1,(s-3)//4+1):v=red(v*(1-q**(2*j)))
 for j in range(b):v=red(v*(1-q**(2*j+1)))
 disc=S.Integer(1) if b==1 else S.discriminant(u,z)
 gam=red(disc*S.resultant(z**s+1,u,z));delta=red(2*g-v)
 pair=red(gam*conj(gam));aug=red(pair*delta)
 c=math.gcd(*(int(x) for x in S.Poly(aug,q).all_coeffs()))
 assert red(g*conj(v)+conj(g)*v-v*conj(v))==0
 rec={'s':s,'augmented_coefficients_descending':list(map(int,S.Poly(aug,q).all_coeffs())),'content':c,'gamma':str(gam),'delta':str(delta),'inverse_identity':True}
 if s==7:
  rec['p13_pair_gcd']=str(S.Poly(S.gcd(S.Poly(phi,q, modulus=13),S.Poly(pair,q,modulus=13)),q).as_expr())
  rec['p13_delta_gcd']=str(S.Poly(S.gcd(S.Poly(phi,q, modulus=13),S.Poly(delta,q,modulus=13)),q).as_expr())
 records.append(rec)
 assert c=={3:1,7:49,11:161051}[s]
pair=[]
for p in [3,5,7,11,13,17,19,29]:
 A=(p-1)//2; hs=[S.Integer(1),y]
 for n in range(2,A+1):hs.append(S.expand(y*hs[-1]-(n-1)*hs[-2]))
 H=hs[A];V=S.expand(sum(co*y**deg*(-1)**((A-deg)//2) for (deg,),co in S.Poly(H,y).terms()))
 W=S.Poly(S.diff(H,y)*V-H*S.diff(V,y)-y*H*V+y**p,y,modulus=p)
 assert W.is_zero
 J=S.Poly(y*H-2*S.diff(H,y),y,modulus=p); gg=S.gcd(J,J.diff()).monic()
 assert gg.as_expr()==(y**2 if p%4==1 else 1)
 pair.append({'p':p,'A':A,'wronskian_exact':True,'tau2_gcd_with_derivative':str(gg.as_expr())})
(out/'reviewer_composite_results.json').write_text(json.dumps({'contents':records,'pairing_controls':pair},indent=2)+'\n')
print(json.dumps({'contents':[r['content'] for r in records],'pairing_controls':len(pair),'pass':True}))
