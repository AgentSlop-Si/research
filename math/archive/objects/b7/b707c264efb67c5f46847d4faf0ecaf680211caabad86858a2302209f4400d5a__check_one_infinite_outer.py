"""Independent exact N4 projective-boundary audit, authored 2026-10-09.

Builds the cyclic resolvents by their finite geometric series and adjugates
by symbolic cofactors. It imports no existing project or uploaded program.
"""
from pathlib import Path
from itertools import combinations, permutations
import json
import sympy as s

OUT = Path(__file__).resolve().parent
x = s.Symbol('x')
D = s.QQ_I
N = 4
Z = s.zeros(N)
V = s.zeros(N)
order = (0, 2, 1, 3)
for j in range(N):
    Z[(j + 1) % N, j] = 1
    V[order[(j + 1) % N], order[j]] = 1

def green(T, p):
    q = s.Rational(1, p)
    return sum((q**k * T**k for k in range(N)), s.zeros(N)) / (1-q**N)

G = green(Z, 4)
J = green(V, 5)
H = G + x * J
A = s.Matrix(N, N, lambda i, j: s.expand((-1)**(i+j) * H.minor_submatrix(j,i).det()))
detH = s.factor(sum(H[0,k]*A[k,0] for k in range(N)))
assert all(s.expand(z) == 0 for z in H*A-detH*s.eye(N))
C = J.adjugate()
F = s.Matrix(N, N, lambda i,j: s.I**(i*j))

def poly(z):
    return s.Poly(z, x, domain=D)

def coefficient_rows(K):
    rows = []
    for i in range(1,N):
        for j in range(1,N):
            u, v = K[i,j]*K[0,0], K[i,0]*K[0,j]
            aa = (G[i,0]*G[0,j], G[i,0]*J[0,j]+J[i,0]*G[0,j], J[i,0]*J[0,j])
            bb = (G[i,j]*G[0,0], G[i,j]*J[0,0]+J[i,j]*G[0,0], J[i,j]*J[0,0])
            rows.append([u*aa[k]-v*bb[k] for k in range(3)])
    return rows

def det3(M):
    d = poly(0)
    for p in permutations(range(3)):
        sign = (-1)**sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))
        d += sign*M[0][p[0]]*M[1][p[1]]*M[2][p[2]]
    return d

def discard_guard(g, guard):
    # A repeated exact gcd removes only roots explicitly forbidden by the guard.
    removed = []
    while g.degree() > 0:
        common = g.gcd(guard)
        if common.degree() == 0:
            break
        removed.append(str(common.as_expr()))
        g = g.exquo(common)
    return g.monic(), removed

zero_values = sorted(set(-G[i,j]/J[i,j] for i in range(N) for j in range(N)))
results = []
for name, mat in [('finite_left_infinite_right', A*F*C), ('infinite_left_finite_right', C*F*A)]:
    K = {(i,j):poly(mat[i,j]) for i in range(N) for j in range(N)}
    rows = coefficient_rows(K)
    guard = poly(detH)*K[0,0]
    g = poly(0)
    used = []
    for ids in combinations(range(9),3):
        d = det3([rows[k] for k in ids])
        if d.is_zero:
            continue
        g = g.gcd(d)
        cleared, removed = discard_guard(g, guard)
        used.append({'rows':ids, 'determinant_degree':d.degree(), 'cumulative_gcd_degree':g.degree()})
        if cleared.degree() == 0:
            break
    assert cleared.degree() == 0, (name, str(cleared.as_expr()))
    branches = []
    for b in zero_values:
        B = G+b*J
        zero = [(i,j) for i in range(N) for j in range(N) if B[i,j] == 0]
        required = [K[pos] for pos in zero]
        for i,k in combinations(range(N),2):
            for j,l in combinations(range(N),2):
                if all(B[r,c] != 0 for r,c in [(i,j),(i,l),(k,j),(k,l)]):
                    required.append(K[i,j]*K[k,l]*B[i,l]*B[k,j] - K[i,l]*K[k,j]*B[i,j]*B[k,l])
        zg = poly(0)
        for f in required:
            zg = zg.gcd(f)
            if zg.degree() == 0:
                break
        rem, rm = discard_guard(zg, poly(detH))
        assert rem.degree() == 0, (name, b, str(rem.as_expr()))
        branches.append({'middle_b':str(b), 'zero_positions':zero, 'necessary_polynomial_count':len(required), 'gcd':str(zg.as_expr()), 'singular_guard_factors_removed':rm})
    record = {'chart':name, 'rank_minor_sequence':used, 'rank_minor_gcd':str(g.as_expr()), 'guard':str(guard.as_expr()), 'guard_factors_removed':removed, 'regular_remainder':str(cleared.as_expr()), 'zero_middle_branches':branches, 'excluded':True}
    results.append(record)
    (OUT/'ONE_INFINITE_OUTER_RESULTS.json').write_text(json.dumps({'field':'Q(i)', 'determinant':str(detH), 'green_construction':'Exact geometric series', 'adjugate_identity_checked':True, 'uploaded_code_executed':False, 'charts':results},indent=2)+'\n')
    print(name, 'EXCLUDED over Q(i), rank witness count',len(used),'and zero branches',len(branches),flush=True)

print('Both one-infinite-outer charts are excluded for every projective middle coupling.',flush=True)
