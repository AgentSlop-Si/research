"""Independent exact controls for the specified endpoint-anchor pivot.

Written for this review. Imports no candidate or historical research program.
All indexing is zero-based; permutation columns encode P e_j=e_rev(j).
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent
CAND = Path('/workspace/shared/scan_endpoint_20261019_0834/candidate')


def zeros(r, c=None):
    return [[0] * (r if c is None else c) for _ in range(r)]


def eye(n):
    a = zeros(n)
    for i in range(n):
        a[i][i] = 1
    return a


def tr(a):
    return [list(x) for x in zip(*a)]


def mul(a, b):
    out = zeros(len(a), len(b[0]))
    for i, row in enumerate(a):
        for k, x in enumerate(row):
            if x:
                for j, y in enumerate(b[k]):
                    if y:
                        out[i][j] += x * y
    return out


def scale(a, x):
    return [[x * y for y in row] for row in a]


def add(*matrices):
    return [[sum(a[i][j] for a in matrices) for j in range(len(matrices[0][0]))]
            for i in range(len(matrices[0]))]


def sub(a, rows, cols=None):
    cols = rows if cols is None else cols
    return [[a[i][j] for j in cols] for i in rows]


def block(a, b, c, d):
    return [x + y for x, y in zip(a, b)] + [x + y for x, y in zip(c, d)]


def bitrev(j, m):
    # String reversal is deliberately distinct from shift-loop constructions.
    return int(format(j, '0%db' % m)[::-1], 2)


def perm(n):
    m = n.bit_length() - 1
    assert 1 << m == n
    a = zeros(n)
    for j in range(n):
        a[bitrev(j, m)][j] = 1
    return a


def anchor(n, diag=3, endpoint=1):
    a = scale(eye(n), diag)
    a[0][0] += endpoint
    for i in range(n - 1):
        a[i][i+1] = a[i+1][i] = 1
    return a


def rank(a, p=None):
    a = [[F(x) for x in row] for row in a] if p is None else [[x % p for x in row] for row in a]
    r = 0
    for j in range(len(a[0])):
        s = next((s for s in range(r, len(a)) if a[s][j]), None)
        if s is None:
            continue
        a[r], a[s] = a[s], a[r]
        inv = 1 / a[r][j] if p is None else pow(a[r][j], -1, p)
        a[r] = [x * inv if p is None else x * inv % p for x in a[r]]
        for s in range(r + 1, len(a)):
            z = a[s][j]
            if z:
                a[s] = [x-z*y if p is None else (x-z*y) % p for x, y in zip(a[s], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def det(a):
    a = [[F(x) for x in row] for row in a]
    ans = F(1)
    for j in range(len(a)):
        s = next((s for s in range(j, len(a)) if a[s][j]), None)
        if s is None:
            return F(0)
        if s != j:
            a[s], a[j] = a[j], a[s]
            ans = -ans
        z = a[j][j]
        ans *= z
        for s in range(j + 1, len(a)):
            c = a[s][j] / z
            if c:
                for k in range(j+1, len(a)):
                    a[s][k] -= c*a[j][k]
        for s in range(j+1, len(a)):
            a[s][j] = 0
    return ans


def mod_fraction(x, p):
    x = F(x)
    return x.numerator * pow(x.denominator, -1, p) % p


def band_pairs(n):
    return [(i, j) for i in range(n) for j in range(n) if abs(i-j) <= 2]


def derivative(n, x):
    # Generic block differential, reconstructing blocks from original ordering.
    t = anchor(2*n)
    e, o = list(range(0, 2*n, 2)), list(range(1, 2*n, 2))
    b, c = sub(t, e, o), sub(t, o, e)
    xi, xb, xc, xd = sub(x, e), sub(x, e, o), sub(x, o, e), sub(x, o)
    return add(xi, scale(mul(xb, c), F(-1, 3)),
               scale(mul(b, xc), F(-1, 3)), scale(mul(mul(b, xd), c), F(1, 9)))


def dual_schur(n, x):
    # Independent scalar Gaussian elimination over Q[epsilon]/epsilon^2.
    def plus(a, b): return (a[0]+b[0], a[1]+b[1])
    def neg(a): return (-a[0], -a[1])
    def times(a, b): return (a[0]*b[0], a[0]*b[1]+a[1]*b[0])
    def inverse(a): return (1/a[0], -a[1]/a[0]**2)
    order = list(range(0, 2*n, 2)) + list(range(1, 2*n, 2))
    t = anchor(2*n)
    a = [[(F(t[i][j]), F(x[i][j])) for j in order] for i in order]
    active = list(range(2*n))
    for k in range(n, 2*n):
        others = [i for i in active if i != k]
        di = inverse(a[k][k])
        for i in others:
            for j in others:
                a[i][j] = plus(a[i][j], neg(times(times(a[i][k], di), a[k][j])))
        active.remove(k)
    return [[a[i][j][1] for j in range(n)] for i in range(n)]


def check_integrity():
    checked = []
    for name in ('MANIFEST.json', 'SOURCE_BINDINGS.json'):
        data = json.loads((CAND / name).read_text())
        for item in data:
            p = CAND / item['file'] if 'file' in item else Path(item['path'])
            b = p.read_bytes()
            assert len(b) == item['bytes']
            assert hashlib.sha256(b).hexdigest() == item['sha256']
            checked.append(str(p))
    assert hashlib.sha256((CAND / 'REPORT.md').read_bytes()).hexdigest() == '46968f362319f164f5eb01476d46899b34b9c1593f48a9cd412250f649c355ba'
    return {'verified_entries': len(checked), 'files': checked}


def check_local(n):
    e, o = list(range(0, 2*n, 2)), list(range(1, 2*n, 2))
    t = anchor(2*n)
    b = sub(t, e, o)
    s = add(sub(t, e), scale(mul(b, tr(b)), F(-1, 3)))
    expected = scale(anchor(n, 7, 4), F(1, 3))
    for i in range(n-1):
        expected[i][i+1] = expected[i+1][i] = F(-1, 3)
    assert s == expected
    assert [[mod_fraction(x, 5) for x in row] for row in s] == [[3*x % 5 for x in row] for row in anchor(n)]
    assert s != scale(anchor(n), 3), 'Must not substitute mod-5 identity over Q.'
    j = anchor(2*n, -2)
    sj = add(sub(j, e), scale(mul(sub(j, e, o), sub(j, o, e)), F(1, 2)))
    assert sj == scale(anchor(n, -2), F(1, 2))
    a = eye(n)
    for i in range(1, n): a[i][i-1] = -1
    assert anchor(n, -2) == scale(mul(a, tr(a)), -1)
    assert det(anchor(n, -2)) == (-1)**n
    result = {'n': n, 'exact_Q_schur': True, 'mod5_scale': 3, 'J_scale_Q': '1/2'}
    if n <= 8:
        pairs = band_pairs(n)
        columns = []
        for i, j in band_pairs(2*n):
            x = zeros(2*n); x[i][j] = 1
            y = derivative(n, x)
            assert all(y[a][b] == 0 for a in range(n) for b in range(n) if abs(a-b) > 2)
            if n == 4:
                assert y == dual_schur(n, x)
            columns.append([y[a][b] for a, b in pairs])
        jac = tr(columns)
        assert rank(jac) == 5*n-6
        assert rank([[mod_fraction(v, 5) for v in row] for row in jac], 5) == 5*n-6
        for i, j in pairs:
            y = zeros(n); y[i][j] = 1
            x = zeros(2*n)
            if j-i == 2: x[2*i+1][2*(i+1)+1] = 9
            if i-j == 2: x[2*(j+1)+1][2*j+1] = 9
            obtained = derivative(n, x)
            for a in range(n):
                for b in range(n):
                    diff = y[a][b]-obtained[a][b]
                    if diff:
                        assert abs(a-b) <= 1
                        x[2*a][2*b] += diff
            assert derivative(n, x) == y
        result.update(input_dimension=len(columns), output_rank=len(pairs), kernel_dimension=len(columns)-len(pairs), dual_scalar_check=(n == 4))
    return result


def check_pivot(q):
    h, n = 2**q, 2**(q+2)
    t, p = anchor(n), perm(n)
    tpt = mul(mul(t, p), t)
    odd = list(range(1, n, 2))
    o = sub(tpt, odd)
    ph, d = perm(h), eye(h)
    for i in range(1, h): d[i][i-1] = 1
    f = zeros(h); f[0][-1] = 1
    a = add(mul(mul(tr(d), ph), d), scale(add(f, tr(f)), 3))
    bb, cc, dd = scale(mul(ph, d), 3), scale(mul(tr(d), ph), 3), scale(ph, 9)
    assert o == block(a, bb, cc, dd)
    r = add(a, scale(mul(mul(bb, ph), cc), F(-1, 9)))
    l = zeros(h)
    for i in range(1, h): l[i][i-1] = 1
    u = mul(mul(ph, tr(l)), ph)
    comm = add(mul(u, l), scale(mul(l, u), -1))
    assert r == add(mul(ph, comm), scale(add(f, tr(f)), 3))
    m = [2**b-1 for b in range(q+1)]
    assert all(r[i][j] == 0 for i in range(h) for j in range(h) if i not in m or j not in m)
    rm = sub(r, m)
    reversed_rows = rm[::-1]
    k = zeros(q+1); k[0][0] = k[-1][-1] = 3
    for i in range(q): k[i+1][i], k[i][i+1] = 1, -1
    assert reversed_rows == k
    dk = det(k)
    assert dk == (6 if q % 2 == 0 else 10)
    assert rank(o) == h+q+1
    assert rank(o, 5) == h+q+1-(q % 2)
    nulls = 0
    for x in range(h):
        if x in m: continue
        w = zeros(2*h, 1); w[x][0] = 3
        v = mul(mul(ph, tr(d)), ph)
        for i in range(h): w[h+i][0] = -v[i][x]
        assert mul(o, w) == zeros(2*h, 1)
        nulls += 1
    if h >= 4:
        w = zeros(n, 1)
        w[5][0] += 3
        w[n//2+5][0] -= 1
        w[n-7][0] -= 1
        z = mul(tpt, w)
        assert all(z[i][0] == 0 for i in odd)
        assert any(z[i][0] != 0 for i in range(0, n, 2))
    # Test the dressed-boundary factor directly in parity coordinates.
    half = n//2
    order = list(range(0, n, 2)) + odd
    tp, pp = sub(t, order), sub(p, order)
    b = sub(tp, range(half), range(half, n))
    c = block(eye(half), scale(b, F(1, 3)), zeros(half), eye(half))
    dressed = mul(mul(tr(c), pp), c)
    g = sub(dressed, range(half, n))
    assert g == scale(o, F(1, 9))
    out = {'N': n, 'q': q, 'rank_Q': h+q+1, 'rank_F5': h+q+1-(q % 2), 'nullity_Q': h-q-1, 'residual_reversed_det': int(dk), 'independent_integer_null_vectors': nulls}
    if n == 8:
        assert det(g) == F(-10, 81)
        out['det_G_Q'] = str(det(g))
    return out


def check_h8():
    n, depth = 8, 3
    t, p = anchor(n), perm(n)
    a, c = mul(t, p), mul(p, t)
    aa, cc = [eye(n)], [eye(n)]
    for _ in range(depth-1):
        aa.append(mul(aa[-1], a)); cc.append(mul(cc[-1], c))
    cols = []
    for k in range(depth):
        for i, j in band_pairs(n):
            cols.append([aa[k][r][i]*cc[depth-1-k][j][s] for r in range(n) for s in range(n)])
    h = tr(cols)
    assert (len(h), len(h[0])) == (64, 102)
    rr = {str(p): rank(h, p) for p in (5, 12289)}
    assert rr == {'5': 64, '12289': 64}
    return {'N': n, 'depth': depth, 'shape': [64, 102], 'ranks': rr, 'scope': 'Only H_8; no larger threshold census.'}


if __name__ == '__main__':
    result = {'integrity': check_integrity(), 'local': [check_local(n) for n in (4, 8, 16)],
              'pivot': [check_pivot(q) for q in range(1, 7)], 'positive_control': check_h8(),
              'candidate_code_executed': False, 'historical_code_executed': False,
              'external_writes': False}
    out = json.dumps(result, indent=2) + '\n'
    (ROOT / 'REVIEWER_RESULTS.json').write_text(out)
    print(out, end='')
