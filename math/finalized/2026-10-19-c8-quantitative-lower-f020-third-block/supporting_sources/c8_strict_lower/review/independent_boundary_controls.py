"""Exact boundary controls authored independently for this review."""
from pathlib import Path
import sympy as s,json
R=Path(__file__).resolve().parent;i=s.I
F=s.Matrix(4,4,lambda j,k:i**(-j*k)/2)
b=s.diag(1,-i,1,-i); phase=(1+i)/s.sqrt(2); a=phase*b
U=s.simplify(F*a*F*b)
assert s.simplify((U+U.conjugate().T)/2)==s.eye(4)/s.sqrt(2)
assert s.simplify((U-phase*s.eye(4))*(U-s.conjugate(phase)*s.eye(4)))==s.zeros(4)
assert a[0,0]==a[2,2] and a[1,1]==a[3,3]
assert b[0,0]==b[2,2] and b[1,1]==b[3,3]
# The boundary theta=pi/2 is deliberately excluded from endpoint rigidity.
V=s.diag(i,-i); T=s.Matrix([[0,1],[1,0]]); x=s.Matrix([1,1])
K=V*T*V.conjugate().T*T.conjugate().T
assert K==-s.eye(2) and K*x==-x
assert V*x!=i*x and V*x!=-i*x
out={'verdict':'PASS','assertions':6,'controls':['C4 equality is attained and its squared phases have half period 2','The theta=pi/2 extension of endpoint rigidity is false, so the strict angular hypothesis is essential'],'arithmetic':'exact symbolic Q(i,sqrt(2))'}
(R/'INDEPENDENT_BOUNDARY_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
