from pathlib import Path
import re,json,ast,math
import sympy as S
ROOT=Path(__file__).resolve().parent
NOTE=ROOT.parents[1]/'discriminant_note';q,y=S.symbols('q y')
text=(NOTE/'manuscript.md').read_text();rows=[];unreduced=[]
for base in [3,7,11,15,19]:
 seg=text.split('### Base '+str(base)+'\n')[1].split('\n### Base ')[0].split('\n## Appendix B')[0]
 data=json.loads((NOTE/'certificates'/f'EXACT_CONTENT_S{base}.json').read_text())
 vectors=[ast.literal_eval(a) for a in re.findall(r'\[[0-9, \-]+\]',seg)]
 r=(base-3)//4;P=vectors[:r+1];delta,aug,bez=vectors[r+1:]
 content=math.gcd(*data['augmented'])
 assert P==data['P'] and delta==data['delta'] and aug==[x//content for x in data['augmented']]
 assert sum(x*y for x,y in zip(aug,bez))==1
 rows.append({'base':base,'all_displayed_appendix_vectors_match':True,'normalized_bezout_identity':True})
 def poly(v):return S.Poly(sum(c*q**j for j,c in enumerate(v)),q)
 phi=S.Poly(S.cyclotomic_poly(base,q),q);gamma=poly(data['Gamma']);delta=poly(data['delta'])
 gi=S.Poly(gamma.as_expr().subs(q,q**(base-1)),q).rem(phi)
 full=gamma*gi*delta
 if base in [11,15,19]:
  got=int(full.content());expected={11:11**4,15:3**12*5**8,19:19**10}[base];assert got==expected
  unreduced.append({'s':base,'unreduced_product_content':got,'after_cyclotomic_reduction_content':int(full.rem(phi).content())})
 if base==7:
  phip=S.Poly(phi.as_expr(),q,modulus=13);pairp=S.Poly(poly(data['Gamma_pair']).as_expr(),q,modulus=13);dp=S.Poly(delta.as_expr(),q,modulus=13)
  assert phip.gcd(pairp)==S.Poly(1,q,modulus=13)
  assert phip.gcd(dp)==S.Poly(q*q+6*q+1,q,modulus=13)
  assert delta.resultant(phi)==1183
  H=S.Poly(S.hermite_prob(6,y),y,modulus=13);J=S.Poly(y,y,modulus=13)*H-H.diff().mul_ground(2)
  assert J==S.Poly(y**7+12*y**5+9*y**3,y,modulus=13)
  boundary={'s':7,'p':13,'Gamma_pair_gcd':1,'delta_gcd':'q^2+6q+1','delta_norm':1183,'J':'y^7+12y^5+9y^3','triple_zero_verified':True}
(ROOT/'independent_certificate_text_results.json').write_text(json.dumps({'appendix':rows,'unreduced_controls':unreduced,'exception_control':boundary},indent=2)+'\n')
print('PASS: appendix vectors, Bezout identities, unreduced-content controls, and actual s=7 p=13 exception.')
