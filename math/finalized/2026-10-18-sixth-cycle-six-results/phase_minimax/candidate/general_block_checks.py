#!/usr/bin/env python3
"""Fresh symbolic checks for the general periodic-block identities."""
import json
from pathlib import Path
import sympy as s
D=Path(__file__).resolve().parent
rt=s.sqrt(2);ii=s.I
roots=[1,(1-ii)/rt,-ii,(-1-ii)/rt,-1,(-1+ii)/rt,ii,(1+ii)/rt]
p=s.symbols('p0:4');q=s.symbols('q0:4')
F=s.Matrix(8,8,lambda j,k:roots[j*k%8]/s.sqrt(8))
V=s.diag(*(p*2))*F*s.diag(*(q*2))
U=s.zeros(8);W=s.zeros(8)
for c in range(2):
 for d in range(2):
  for u in range(2):
   n=4*c+2*d+u;r=c+2*u;k=d+2*u
   U[r,n]=1/rt;U[r+4,n]=(-1)**d/rt
   W[k,n]=1/rt;W[k+4,n]=(-1)**c/rt
expected=s.zeros(8)
for c in range(2):
 for d in range(2):
  for u in range(2):
   for v in range(2):
    expected[4*c+2*d+u,4*c+2*d+v]=p[c+2*u]*q[d+2*v]*roots[((c+2*u)*(d+2*v))%8]/rt
assert all(s.simplify(x)==0 for x in U.T*V*W-expected)
x,y=s.symbols('x y',nonzero=True)
H=s.Matrix([[1,1],[1,-1]])/rt
A=s.diag(1/x,x)*H*s.diag(1/y,y)
# x=e^(ir), y=e^(is), h=cos(2r)cos(2s).
h=(x**2+x**-2)*(y**2+y**-2)/4
assert s.simplify(s.trace(A.T*A)-2*h)==0
assert s.simplify((A.T*A).det()-1)==0
r=s.symbols('r'); tablesC=[1,r/2,0,-r/2,-1,-r/2,0,r/2];tablesS=[0,r/2,1,r/2,0,-r/2,-1,-r/2]
a,b,u,v=s.symbols('a b u v',real=True)
for j in range(8):
 m= s.expand((a+ii*b)*(u+ii*v)*(tablesC[j]-ii*tablesS[j]))
 assert s.simplify(s.im(m.subs(r,rt))-((a*v+b*u)*tablesC[j]-(a*u-b*v)*tablesS[j]).subs(r,rt))==0
out={'general_four_periodic_block_decomposition_all_64':True,'centered_block_trace':True,'centered_block_determinant':True,'negative_sign_semialgebraic_entry_formula_all_eight_roots':True,'scope':'Symbolic identities supporting the analytic sector proof; no unrestricted lower certificate.'}
(D/'GENERAL_BLOCK_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
