#!/usr/bin/env python3
"""Independent direct-Gauss-sum controls. No supplied program is read or imported."""
import json
from math import isqrt
from pathlib import Path


def prime(p):
    return p >= 2 and all(p % d for d in range(2, isqrt(p) + 1))


def factors(n):
    return [d for d in range(2, n + 1) if n % d == 0 and prime(d)]


def rank(a, p):
    a = [row[:] for row in a]
    row = 0
    for col in range(len(a[0])):
        pivot = next((r for r in range(row, len(a)) if a[r][col] % p), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        inv = pow(a[row][col], -1, p)
        a[row] = [v * inv % p for v in a[row]]
        for r in range(row + 1, len(a)):
            v = a[r][col]
            if v:
                a[r] = [(a[r][c] - v * a[row][c]) % p for c in range(len(a[0]))]
        row += 1
        if row == len(a):
            break
    return row


def check(n, p, w, alpha, beta):
    delta = (1 - pow(alpha, n, p) - pow(beta, n, p)) % p
    assert delta and alpha and beta
    assert pow(w, n, p) == 1 and all(pow(w, n // q, p) != 1 for q in factors(n))
    phi = [1]
    for s in range(1, n):
        phi.append(phi[-1] * (1 - pow(w, s, p)) % p)
    assert all(phi)
    gauss = [sum(pow(w, (-t*t-r*t) % n, p) for t in range(n)) % p for r in range(n)]
    inv_n = pow(n, -1, p)
    # Compute W by independently dividing direct coefficient C by sector scalar g.
    weights = [[0] * n for _ in range(n)]
    for a in range(n):
        for b in range(n - a):
            sector = (pow(alpha, a, p) * pow(beta, b, p) * phi[a+b]
                      * pow(delta * phi[a] * phi[b] % p, -1, p)) % p
            weights[a][b] = gauss[a+b] * inv_n * pow(sector, -1, p) % p
    kappa = (n // 2) % 2
    assert [r for r, value in enumerate(gauss) if value] == list(range(kappa, n, 2))
    assert sum(gauss) % p == n % p
    for r in range(n):
        assert gauss[(r+2) % n] == pow(w, (r+1) % n, p) * gauss[r] % p
    expected = n if n % 4 == 2 else n - 1
    actual = rank(weights, p)
    assert actual == expected, (n, p, w, alpha, beta, actual, expected)
    last = expected - 1
    assert all(weights[a][last-a] for a in range(expected))
    assert all(weights[a][b] == 0 for a in range(n) for b in range(n) if a+b > last)
    if n % 4 == 0:
        assert not any(weights[-1]) and not any(row[-1] for row in weights)
    # A changed truncation is not covered by the theorem.
    narrower = [[weights[a][b] if a+b < n-1 else 0 for b in range(n)] for a in range(n)]
    narrow_expected = n - 2 if n % 4 == 2 else n - 1
    assert rank(narrower, p) == narrow_expected
    return {"N": n, "p": p, "w": w, "alpha": alpha, "beta": beta,
            "rank": actual, "rank_with_a_plus_b_less_than_N_minus_1": narrow_expected,
            **({"W": weights} if n <= 4 else {})}


# A genuinely non-prime field boundary: F_9 = F_3[j]/(j^2+1), N=4, w=j.
class F9:
    def __init__(self, a=0, b=0):
        if isinstance(a, F9):
            self.a, self.b = a.a, a.b
        else:
            self.a, self.b = a % 3, b % 3
    def __add__(self, other):
        other = F9(other)
        return F9(self.a + other.a, self.b + other.b)
    __radd__ = __add__
    def __neg__(self): return F9(-self.a, -self.b)
    def __sub__(self, other): return self + (-F9(other))
    def __rsub__(self, other): return F9(other) + (-self)
    def __mul__(self, other):
        other = F9(other)
        return F9(self.a*other.a-self.b*other.b, self.a*other.b+self.b*other.a)
    __rmul__ = __mul__
    def __pow__(self, exp):
        if exp < 0:
            assert self
            exp %= 8
        result, base = F9(1), self
        while exp:
            if exp & 1: result = result * base
            base, exp = base * base, exp // 2
        return result
    def __truediv__(self, other): return self * F9(other) ** -1
    def __bool__(self): return bool(self.a or self.b)
    def __eq__(self, other):
        other = F9(other)
        return self.a == other.a and self.b == other.b
    def pair(self): return [self.a, self.b]


def extension_boundary():
    n, w, delta = 4, F9(0, 1), F9(-1)
    phi = [F9(1)]
    for s in range(1, n): phi.append(phi[-1] * (1-w**s))
    gauss = [sum((w**((-t*t-r*t) % n) for t in range(n)), F9()) for r in range(n)]
    a = [[F9() for _ in range(n)] for _ in range(n)]
    for r in range(n):
        for c in range(n-r):
            g = phi[r+c] / (delta * phi[r] * phi[c])
            a[r][c] = gauss[r+c] / (F9(n)*g)
    original = [[x.pair() for x in row] for row in a]
    row = 0
    for col in range(n):
        pivot = next((r for r in range(row, n) if a[r][col]), None)
        if pivot is None: continue
        a[row], a[pivot] = a[pivot], a[row]
        inv = a[row][col] ** -1
        a[row] = [x * inv for x in a[row]]
        for r in range(row + 1, n):
            v = a[r][col]
            a[r] = [a[r][c] - v*a[row][c] for c in range(n)]
        row += 1
    assert row == 3
    return {"field": "F_3[j]/(j^2+1)", "N": 4, "w": [0,1], "alpha": [1,0],
            "beta": [1,0], "rank": row, "W_pairs": original}


def main():
    cases = []
    for n in range(2, 65, 2):
        ps = []
        k = 1
        while len(ps) < 3:
            p = k*n + 1
            if prime(p): ps.append(p)
            k += 1
        for p in ps:
            w = next(x for x in range(2, p) if pow(x, n, p) == 1
                     and all(pow(x, n//q, p) != 1 for q in factors(n)))
            roots = sorted({w, pow(w, -1, p)})
            choices = [(1,1)]
            extra = next(((a,b) for a in range(2, min(p, 9)) for b in range(2, min(p, 9))
                          if (1-pow(a,n,p)-pow(b,n,p)) % p), None)
            if extra: choices.append(extra)
            for root in roots:
                for alpha, beta in choices:
                    cases.append(check(n, p, root, alpha, beta))
    result = {"verdict": "PASS", "supplied_source_read_or_imported": False,
              "prime_field_cases": len(cases), "even_lengths": list(range(2,65,2)),
              "entry_count": sum(c["N"]**2 for c in cases),
              "extension_field_boundary": extension_boundary(), "cases": cases}
    output = Path(__file__).with_name("EVEN_CHART_RANK_CONTROLS.json")
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({key: value for key, value in result.items() if key != "cases"}, indent=2))


if __name__ == "__main__": main()
