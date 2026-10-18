"""Independent, short, standard-library review of the unrestricted F8 packet.

No packet program is imported or executed. No elimination or numerical search.
"""
import ast
import hashlib
import itertools
import json
import re
from fractions import Fraction
from pathlib import Path

SOURCE = (Path(__file__).resolve().parent.parent / 'candidate')
HERE = Path(__file__).resolve().parent
N = 8
P = (7, 0, 6, 3, 4, 1, 2, 5)
PINV = tuple(P.index(j) for j in range(N))
ZERO = (0, 0, 0, 0)
ONE = (1, 0, 0, 0)


def kadd(a, b):
    return tuple(x + y for x, y in zip(a, b))


def kmul(a, b):
    out = [0] * 4
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            q, r = divmod(i + j, 4)
            out[r] += (-1) ** q * x * y
    return tuple(out)


def zp(k):
    q, r = divmod(k, 4)
    return tuple((-1) ** q if i == r else 0 for i in range(4))


def const(k):
    if isinstance(k, int):
        k = (k, 0, 0, 0)
    return {(): k} if any(k) else {}


def var(v):
    return {(v,): ONE}


def add(a, b):
    out = a.copy()
    for mon, coeff in b.items():
        out[mon] = kadd(out.get(mon, ZERO), coeff)
        if not any(out[mon]):
            del out[mon]
    return out


def neg(a):
    return {m: tuple(-x for x in k) for m, k in a.items()}


def mul(a, b):
    out = {}
    for x, u in a.items():
        for y, v in b.items():
            m = tuple(sorted(x + y))
            out[m] = kadd(out.get(m, ZERO), kmul(u, v))
            if not any(out[m]):
                del out[m]
    return out


def summation(items):
    out = {}
    for item in items:
        out = add(out, item)
    return out


def from_json(e):
    out = {}
    for term in e['terms']:
        assert len(term['coefficient']) == 4
        assert all(type(x) is int for x in term['coefficient'])
        mon = tuple(sorted(term['monomial']))
        out = add(out, {mon: tuple(term['coefficient'])})
    return out


def stage(s):
    return [[var(f'{s}_d{i}') if i == j else
             mul(var(f'{s}_l{i}'), var(f'{s}_m{j}')) if i > j else
             mul(var(f'{s}_u{i}'), var(f'{s}_v{j}'))
             for j in range(N)] for i in range(N)]


def minor(M, rows, cols):
    r, s = rows
    a, b = cols
    return add(mul(M[r][a], M[s][b]), neg(mul(M[r][b], M[s][a])))


def ladder_indices(n):
    return {(r, s, a, b) for r, s in itertools.combinations(range(n), 2)
            for a, b in itertools.combinations(range(n), 2)
            if s < a or b < r}


def parse_expression(text):
    def visit(node):
        if isinstance(node, ast.Constant):
            assert type(node.value) is int
            return const(node.value)
        if isinstance(node, ast.Name):
            return const(zp(1)) if node.id == 'z' else var(node.id)
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return neg(visit(node.operand))
        if isinstance(node, ast.BinOp):
            left = visit(node.left)
            if isinstance(node.op, ast.Pow):
                assert isinstance(node.right, ast.Constant)
                exponent = node.right.value
                assert type(exponent) is int and 0 <= exponent <= 4
                out = const(1)
                for _ in range(exponent):
                    out = mul(out, left)
                return out
            right = visit(node.right)
            if isinstance(node.op, ast.Add):
                return add(left, right)
            if isinstance(node.op, ast.Sub):
                return add(left, neg(right))
            if isinstance(node.op, ast.Mult):
                return mul(left, right)
        raise AssertionError(ast.dump(node))
    return visit(ast.parse(text.strip().replace('^', '**'), mode='eval').body)


manifest = json.loads((SOURCE / 'MANIFEST.json').read_text())
assert len(manifest['files']) == 42
paths = set()
for item in manifest['files']:
    assert item['path'] not in paths
    paths.add(item['path'])
    raw = (SOURCE / item['path']).read_bytes()
    assert len(raw) == item['bytes']
    assert hashlib.sha256(raw).hexdigest() == item['sha256']
actual = {str(p.relative_to(SOURCE)) for p in SOURCE.rglob('*') if p.is_file()}
assert actual == paths | {'MANIFEST.json'}
bindings = json.loads((SOURCE / 'SOURCE_BINDINGS.json').read_text())
for b in bindings:
    raw = (SOURCE / b['file']).read_bytes()
    gitsha = hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest()
    assert gitsha == b['local_git_blob']
    assert hashlib.sha256(raw).hexdigest() == b['sha256']
    if b['pinned_git_blob'] is not None:
        assert gitsha == b['pinned_git_blob']

original = json.loads((SOURCE / 'ORIGINAL_IDEAL.json').read_text())
relaxed = json.loads((SOURCE / 'RELAXED_QUADRICS.json').read_text())
allvars = [f'{s}_{g}{i}' for s in 'AB' for g in ('d', 'l', 'm', 'u', 'v') for i in range(N)]
unused = {f'{s}_{g}{i}' for s in 'AB' for g, i in (('l', 0), ('m', 7), ('u', 7), ('v', 0))}
assert original['variables'] == allvars
assert set(original['unobservable_variables']) == unused
assert original['field'] == relaxed['field'] == 'Q[z]/(z^4+1)'
assert original['permutation'] == list(P)
A, B = stage('A'), stage('B')
expected_original = [add(summation(mul(B[i][P[k]], A[k][j]) for k in range(N)),
                         neg(const(zp(i * j)))) for i in range(N) for j in range(N)]
assert len(original['equations']) == 64
for e, expected, (i, j) in zip(original['equations'], expected_original, itertools.product(range(N), repeat=2)):
    assert (e['row'], e['column']) == (i, j)
    assert from_json(e) == expected
used = {v for poly in expected_original for mon in poly for v in mon}
assert set(allvars) - used == unused and len(used) == 72
assert max(len(mon) for p in expected_original for mon in p) == 4

C = [[var(f'c{i}_{j}') for j in range(N)] for i in range(N)]
FB = [[summation(mul(const(zp(i*k)), C[k][PINV[j]]) for k in range(N))
       for j in range(N)] for i in range(N)]
assert relaxed['variables'] == [f'c{i}_{j}' for i in range(N) for j in range(N)] + ['t']
assert relaxed['invertibility_equation'] == 't*det(C)-1'
indices = ladder_indices(N)
assert len(indices) == 140
assert sum(b < r for r, s, a, b in indices) == 70
seen = {'C': set(), 'F*C*P^-1': set()}
expected_relaxed = []
for e in relaxed['equations']:
    typ = e['stage']
    rs = e['rows']
    cs = e['columns'] if typ == 'C' else e['columns_in_B']
    if typ != 'C':
        assert cs == [P[j] for j in e['columns_in_C']]
    key = tuple(rs) + tuple(sorted(cs))
    assert key in indices and key not in seen[typ]
    seen[typ].add(key)
    expected = minor(C if typ == 'C' else FB, rs, cs)
    assert from_json(e) == expected
    assert all(len(mon) == 2 for mon in expected)
    expected_relaxed.append(expected)
assert all(s == indices for s in seen.values())
assert len(expected_relaxed) == 280

for filename, ideal, ringvars, expected in [
    ('ORIGINAL_IDEAL.sing', 'I', [v for v in allvars if v not in unused], expected_original),
    ('RELAXED_IDEAL.sing', 'J', relaxed['variables'], expected_relaxed),
]:
    text = (SOURCE / filename).read_text()
    gotvars = re.search(r'ring R = \(0,z\),\(([^)]+)\),dp;', text).group(1).split(',')
    assert gotvars == ringvars
    assert 'minpoly = z^4+1;' in text
    equations = re.search(r'ideal ' + ideal + r' =\n(.*?);', text, re.S).group(1).split(',\n')
    if ideal == 'J':
        assert equations.pop().strip() == 't*det(C)-1'
        matrixvars = re.search(r'matrix C\[8\]\[8\] = ([^;]+);', text).group(1).split(',')
        assert matrixvars == ringvars[:-1]
    assert len(equations) == len(expected)
    for expression, poly in zip(equations, expected):
        assert parse_expression(expression) == poly

# Independent Vandermonde determinant, and both Fourier inverse products.
detF = ONE
for i, j in itertools.combinations(range(N), 2):
    detF = kmul(detF, kadd(zp(j), tuple(-x for x in zp(i))))
assert detF == (0, 0, 4096, 0)
for i, j in itertools.product(range(N), repeat=2):
    for direction in (-1, 1):
        total = ZERO
        for k in range(N):
            total = kadd(total, zp(direction * (i - j) * k))
        assert total == ((8, 0, 0, 0) if i == j else ZERO)
assert zp(4) == (-1, 0, 0, 0) and zp(8) == ONE
assert all(zp(k) != ONE for k in (1, 2, 4))
# The shifted polynomial is x^4+4x^3+6x^2+4x+2: Eisenstein at 2.
shifted_coefficients = [2, 4, 6, 4, 1]
assert all(c % 2 == 0 for c in shifted_coefficients[:-1])
assert shifted_coefficients[0] % 4 != 0


def lower_support(T):
    n = len(T)
    rows = {i for i in range(n) if any(T[i][j] for j in range(i))}
    cols = {j for j in range(n) if any(T[i][j] for i in range(j+1, n))}
    return rows, cols


def lower_lift(T):
    n = len(T)
    rows, cols = lower_support(T)
    l, m = [0]*n, [0]*n
    if rows:
        r, s = max(rows), min(cols)
        if not T[r][s]:
            return None
        for i in rows:
            l[i] = T[i][s]
        for j in cols:
            m[j] = Fraction(T[r][j], T[r][s])
    if all(T[i][j] == l[i]*m[j] for i in range(n) for j in range(i)):
        return l, m
    return None


def lower_minors_vanish(T):
    return all(T[r][a]*T[s][b] == T[r][b]*T[s][a]
               for r, s, a, b in ladder_indices(len(T)) if b < r)


# Check the support-aware lifting equivalence on every 4x4 ternary lower triangle.
ternary_cases = 0
positions = [(i, j) for i in range(4) for j in range(i)]
for values in itertools.product((-1, 0, 1), repeat=len(positions)):
    T = [[0]*4 for _ in range(4)]
    for (i, j), v in zip(positions, values):
        T[i][j] = v
    rows, cols = lower_support(T)
    support_ok = all(T[i][j] != 0 for i in rows for j in cols if i > j)
    assert (lower_lift(T) is not None) == (lower_minors_vanish(T) and support_ok)
    ternary_cases += 1

# Count actual distinct supports, rather than only qualifying row/column masks.
supports = set()
for rmask in range(128):
    for cmask in range(128):
        edges = tuple((i, j) for i in range(1, 8) for j in range(7)
                      if i > j and (rmask >> (i-1)) & 1 and (cmask >> j) & 1)
        supports.add(edges)
assert len(supports) == 7280

# Inverse-chart boundary, checked by both exact matrix products.
L = [[int(i >= j) for j in range(N)] for i in range(N)]
D = [[int(i == j) - int(i == j+1) for j in range(N)] for i in range(N)]
for X, Y in ((L, D), (D, L)):
    assert all(sum(X[i][k]*Y[k][j] for k in range(N)) == int(i == j)
               for i in range(N) for j in range(N))
assert lower_lift(L) is not None
assert lower_minors_vanish(D) and lower_minors_vanish([list(x) for x in zip(*D)])
assert lower_lift(D) is None
assert D[1][0] == D[2][1] == -1 and D[2][0] == 0

status = json.loads((SOURCE / 'ELIMINATION_STATUS.json').read_text())
assert status['exit_code'] == 152 and status['cpu_soft_limit_seconds'] == 180
assert status['cpu_hard_limit_seconds'] == 185
assert status['address_space_limit_bytes'] == 2**30
assert status['variables'] == 73 and status['equations'] == 65
assert status['coefficient_domain'] == 'QQ' and status['method'] == 'f5b'
assert not status['basis_returned'] and not status['unit_ideal_certificate_returned']
assert not (SOURCE / 'EXACT_BASIS.txt').exists()
events = [json.loads(line) for line in (SOURCE / 'EXACT_ELIMINATION.log').read_text().splitlines()]
assert len(events) == 1 and events[0]['event'] == 'start_exact_full_ideal'
assert events[0]['variables'] == 73 and events[0]['equations'] == 65
exit_log = (SOURCE / 'EXACT_ELIMINATION_EXIT.log').read_text()
assert 'exit code 152' in exit_log and 'CPU time limit exceeded' in exit_log
source = (SOURCE / 'exact_elimination_attempt.py').read_text()
ast.parse(source)  # Syntax only; never execute the elimination script.
assert 'resource.setrlimit(resource.RLIMIT_CPU,(180,185))' in source
assert 'resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))' in source
assert "eq.append(z**4+1)" in source
assert "s.groebner(eq,*xs,order='grevlex',domain=s.QQ,method='f5b')" in source

results = {
    'verdict': 'ACCEPT_SCOPED_REDUCTION_AND_RESOURCE_BLOCKER; TARGET_UNDECIDED',
    'manifest_members_verified': 42,
    'source_blob_bindings_recomputed': len(bindings),
    'source_pinned_blob_matches': 2,
    'original_symbolic_identities_checked': 64,
    'relaxed_symbolic_identities_checked': 280,
    'singular_polynomials_independently_parsed': 344,
    'original_observable_variables': 72,
    'inverse_relaxation_variables_including_t': 65,
    'inverse_relaxation_quadrics': 280,
    'original_max_degree': 4,
    'inverse_permutation': list(PINV),
    'fourier_determinant': list(detF),
    'fourier_inverse_entry_checks': 128,
    'ternary_lower_triangle_lifting_checks_n4': ternary_cases,
    'distinct_triangular_supports_n8': len(supports),
    'naive_four_triangle_support_count': len(supports)**4,
    'inverse_chart_counterexample_verified': True,
    'elimination_resource_log_consistent': True,
    'elimination_rerun': False,
    'external_writes': False,
    'source_packet_modified': False,
    'original_target_decided': False,
}
(HERE / 'CHECKS.json').write_text(json.dumps(results, indent=2) + '\n')
print(json.dumps(results, indent=2))
