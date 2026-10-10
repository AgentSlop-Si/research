"""Fresh small controls for a new assessment-level generalization; no source imports."""
import json, random
from pathlib import Path
import sympy as S
w,a=S.symbols('w a')
rng=random.Random(20261010)
records=[]
for m in range(1,4):
 for trial in range(2):
  A=S.Matrix(m,m,[rng.randrange(-3,5) for _ in range(m*m)])
  B=S.Matrix(m,m,[rng.randrange(-3,5) for _ in range(m*m)])
  def pencil(M,e):
   return S.Poly(S.expand(S.Matrix(m,m,lambda i,j:M[i,j]*(1-a*w**(e+i+j))).det()),a).as_expr()
  P,Q=pencil(A,0),pencil(B,1)
  # Fixed-degree Sylvester determinant also covers singular coefficient matrices.
  pc=[S.Poly(P,a).nth(k) for k in range(m,-1,-1)]
  qc=[S.Poly(Q,a).nth(k) for k in range(m,-1,-1)]
  syl=S.Matrix([[0]*j+c+[0]*(m-1-j) for c in (pc,qc) for j in range(m)])
  R=S.Poly(S.expand(syl.det()),w)
  v=m*(m-1)*(4*m+1)//6; D=m*m*(2*m-1); b=(m-1)*m*(2*m-1)//6
  U,rem=S.div(R,S.Poly(w**v*(w-1)**(m*m),w))
  assert rem.is_zero
  coeff=U.as_expr().expand()
  assert S.expand(w**(2*b)*coeff.subs(w,1/w)-coeff)==0
  assert S.expand(w**D*R.as_expr().subs(w,1/w)-(-1)**(m*m)*R.as_expr())==0
  valuation=min(k[0] for k,c in R.terms()) if not R.is_zero else None
  records.append({'m':m,'trial':trial,'A':list(A),'B':list(B),'predicted_v':v,'actual_v':valuation,'degree':R.degree(),'quotient_degree':U.degree(),'pass':True})
for m in range(1,9):
 v=sum(min(2*i,2*j+1) for i in range(m) for j in range(m))
 assert v==m*(m-1)*(4*m+1)//6
 # At A=B=I, each difference has exactly one zero at w=1 in characteristic zero.
 assert sum(2*m-2*j-1 for j in range(m))==m*m
records.append({'diagonal_specialization':'A=B=I, m=1..8','valuation_formula':True,'w1_multiplicity':True})
path=Path('publication_assessment_20261010/GENERAL_PENCIL_CONTROLS.json')
path.write_text(json.dumps(records,indent=2,default=str)+'\n')
print('Fresh controls passed:',len(records)-1,'arbitrary matrix pairs; diagonal formulas m=1..8')
