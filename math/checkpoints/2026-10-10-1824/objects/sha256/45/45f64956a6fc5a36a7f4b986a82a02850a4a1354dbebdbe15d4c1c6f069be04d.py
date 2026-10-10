"""Independent exact controls for the residual-root and classical Bezoutian examples."""
from pathlib import Path
import json
import sympy as s

x,y=s.symbols('x y')
N=15
h=x**9+x**6+x**3+2
g=s.expand((x-1)*h)
A=x**12+x**3-2
M=[]
for a in range(N):
    u=s.Poly(s.rem(x**a,g,x),x)
    v=s.Poly(s.rem(x**((-a)%N),g,x),x)
    M.append([u.nth(i) for i in range(10)]+[1]+[v.nth(i) for i in range(10)])
assert s.Matrix(M).rank()==14
assert s.gcd(g,s.diff(g,x))==1
assert s.rem(A,g,x)==0
assert s.expand(x**N*A.subs(x,1/x)+A.subs(x,0)*(1-x**N))==A
assert A.subs(x,1)==0
j={'N':N,'g':str(g),'h':str(h),'A':str(A),'g_squarefree':True,
   'h_reciprocal_coprime':s.gcd(h,s.expand(x**9*h.subs(x,1/x)))==1,
   'axis_rank_Q':14}
g0=x**3+x**2+x+2
H=2*x**3+x**2+x+1
P=s.Poly(s.cancel((g0*H.subs(x,y)-g0.subs(x,y)*H)/(x-y)),x,y)
B=s.Matrix([[P.coeff_monomial(x**i*y**j) for j in range(3)] for i in range(3)])
assert B.det()==20
out={'status':'PASS','simple_root_one_counterexample':j,
     'N5_reciprocal_bezout_matrix':[[int(z) for z in B.row(i)] for i in range(3)],
     'N5_reciprocal_bezout_determinant':int(B.det()),
     'N5_reciprocal_resultant':int(s.resultant(g0,H,x))}
path=Path(__file__).resolve().parent/'ADDITIONAL_EXACT_CONTROLS.json'
path.write_text(json.dumps(out,indent=2)+'\n')
print(path)
