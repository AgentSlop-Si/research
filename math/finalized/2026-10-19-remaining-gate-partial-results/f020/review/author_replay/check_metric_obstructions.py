"""Fresh symbolic transcription checks; no root-order census or prior-code imports."""
from pathlib import Path
import json
import sympy as S

OUT = Path(__file__).resolve().parent
checks = []

def check(name, expression):
    value = S.simplify(S.expand(expression))
    assert value == 0, (name, value)
    checks.append({"name": name, "exact_difference": str(value), "passed": True})

q, X, c, s = S.symbols("q X c s", nonzero=True)
P = [S.Integer(1), X]
for k in range(1, 4):
    P.append(S.expand(X * P[-1] - (1 - q**k) * P[-2]))
A = 3 - q - q**2 - q**3
B = (1 - q) * (1 - q**3)
check("actual P4 formula", P[4] - (X**4 - A*X**2 + B))
check("A deflation", A - (1-q)*(q**2+2*q+3))
check("B deflation", B - (1-q)**2*(q**2+q+1))
R = (q**2+q+1)/(q**2+2*q+3)**2
check("spectral ratio cancellation", S.cancel(B/A**2 - R))
check("unit-circle numerator factor", q**2+q+1 - q*(q+1+q**-1))
check("unit-circle denominator factor", q**2+2*q+3 - 2*q*(1+(q+q**-1)+(q**-1-q)/2))

# Re(c+i s)=c and Im(c+i s)=s, with c^2+s^2=1.
a = 1+2*c
Dreal = c*(a*a-s*s)+2*a*s*s
Dimag = s*(a*a-s*s)-2*a*c*s
check("imaginary denominator identity on unit circle", S.rem(Dimag-s*c*(c+2), s*s+c*c-1, s))
check("denominator squared modulus on unit circle", S.rem(Dreal**2+Dimag**2-(a*a+s*s)**2, s*s+c*c-1, s))

# Generic residual reversal defect, with Q=q^b and t=q^k.
Q, t = S.symbols("Q t", nonzero=True)
check("reversal conjugation defect", (1-Q/t) - ((1-Q)+Q*(1-1/t)))

# Symbolic finite geometric sum identity underlying the uniform trace proof.
n = S.symbols("n", integer=True, positive=True)
check("geometric sum rational numerator", (1-q)*(q*(1-q**n)/(1-q)) - (q-q**(n+1)))

# Normality equations for a generic four-vertex zero-diagonal tridiagonal path.
sr = S.symbols("s1:4")
tr = S.symbols("t1:4")
sb = S.symbols("S1:4")
tb = S.symbols("T1:4")
T = S.zeros(4)
Tstar = S.zeros(4)
for k in range(3):
    T[k,k+1], T[k+1,k] = sr[k], tr[k]
    Tstar[k,k+1], Tstar[k+1,k] = tb[k], sb[k]
C = T*Tstar-Tstar*T
check("normality first diagonal", C[0,0] - (sr[0]*sb[0]-tr[0]*tb[0]))
for k in range(1, 3):
    check(f"normality telescoping diagonal {k+1}", C[k,k]-(tr[k-1]*tb[k-1]+sr[k]*sb[k]-sr[k-1]*sb[k-1]-tr[k]*tb[k]))
for k in range(2):
    check(f"normality distance-two equation {k+1}", C[k,k+2]-(sr[k]*tb[k+1]-tb[k]*sr[k+1]))

# Independent symbolic matrix construction of the actual P4 characteristic polynomial.
J = S.zeros(4)
for k in range(1, 4):
    J[k-1,k] = 1
    J[k,k-1] = 1-q**k
characteristic = J.charpoly()
check("actual Jacobi characteristic polynomial", characteristic.as_expr().subs(characteristic.gen, X) - P[4])
check("actual Jacobi trace squared", S.trace(J**2)-2*A)
check("actual Jacobi fourth invariant", S.trace(J**4)-(2*A*A-4*B))

# The compression defect is checked as a generic scalar-block identity.
m, aa, aaa, nn, nnb, cc, ccb = S.symbols("m a A n N C B")
check("compressed metric equation bookkeeping", (m*aa+nn*cc-aaa*m-ccb*nnb) - ((m*aa-aaa*m)-(ccb*nnb-nn*cc)))

payload = {
    "kind": "fresh symbolic transcription controls, not a root-order census",
    "all_passed": True,
    "assertion_count": len(checks),
    "checks": checks,
    "imports_prior_research_code": False,
    "claims_numeric_root_certification": False,
}
(OUT/"CHECKS.json").write_text(json.dumps(payload, indent=2)+"\n")
print(f"PASS: {len(checks)} exact symbolic transcription assertions")
