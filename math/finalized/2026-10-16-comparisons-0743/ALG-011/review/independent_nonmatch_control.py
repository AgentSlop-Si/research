"""New finite algebra check; imports no historical or author implementation."""
import itertools
import json
from pathlib import Path

p, n, q, lam = 5, 4, 2, 1
x = [1, 3, 1, 0]
e = [[0 for _ in range(n)] for _ in range(n)]
for i in range(n):
    e[i][i] = -pow(q, i, p) % p
    if i + 1 < n:
        e[i][i + 1] = -pow(q, i, p) * (pow(q, i + 1, p) - 1) % p
ex = [sum(a * b for a, b in zip(row, x)) % p for row in e]
residual = [(a - lam * b) % p for a, b in zip(ex, x)]
y = [sum(x[j] * pow(q, i * j, p) for j in range(n)) % p for i in range(n)]
jy = [((pow(q, -i - 1, p) - 1) * y[(i + 1) % n] - pow(q, -i - 1, p) * y[(i + 2) % n]) % p for i in range(n)]
solutions = {}
for length in range(n + 1):
    cs = []
    for c in itertools.product(range(p), repeat=length):
        if all((x[j] + sum(c[i - 1] * x[j - i] for i in range(1, length + 1))) % p == 0 for j in range(length, n)):
            cs.append(list(c))
    solutions[str(length)] = cs
    if cs:
        minimal_length = length
        break
t = next(t for t in range(n) if (-pow(q, t, p)) % p == lam)
coordinate_sum = sum(pow(q, -i * t, p) * y[i] for i in range(n)) % p
assert ex == x and residual == [0] * n
assert y == [0, 1, 4, 4] and jy == y
assert minimal_length == 2 and solutions['2'] == [[4, 2]]
assert t == 2 and coordinate_sum == (n * x[t]) % p == 4
result = {
    'scope': 'Finite control for nonidentification of sparse E-shift defect cap and constant-coefficient LFSR length; not implementation replay or a new proof acceptance.',
    'field': 5, 'N': n, 'q': q, 'lambda': lam, 'defect_cap': 0,
    'x': x, 'E': e, 'Ex': ex, 'residual': residual, 'Fx': y,
    'JFx': jy, 'minimal_LFSR_length': minimal_length,
    'minimal_connection_coefficients': solutions['2'],
    'actual_source_eigenindex': t, 'inverse_coordinate_sum': coordinate_sum,
    'all_assertions_passed': True,
}
Path(__file__).with_name('INDEPENDENT_NONMATCH_CONTROL.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
