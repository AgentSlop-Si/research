"""Fresh ALG-063 bounded reference, 2026-10-17. No historical-code imports.

Exact prime-field reference. p is a trusted prime, already selected and paid for.
Inputs are canonical residues. The root is verified in O(N) field operations.
Field counters count inversion as one primitive, not its integer bit work.
"""


class Field:
    def __init__(self, p):
        self.p = p
        self.counts = {"add_sub": 0, "mul": 0, "eq": 0, "inv": 0}

    def add(self, a, b):
        self.counts["add_sub"] += 1
        return (a + b) % self.p

    def sub(self, a, b):
        self.counts["add_sub"] += 1
        return (a - b) % self.p

    def mul(self, a, b):
        self.counts["mul"] += 1
        return a * b % self.p

    def eq(self, a, b):
        self.counts["eq"] += 1
        return a == b

    def inv(self, a):
        assert a != 0
        self.counts["inv"] += 1
        return pow(a, -1, self.p)


def raw_twisted_dft(x, r, p, omega):
    """Return exact DFT or certified outside-family rejection.

    Accepted family: nnz(x)<=2r OR exists z with nnz(x-z*shift(x))<=r.
    Success is O(N(r+1)) field/index operations, at most one inversion;
    rejection is O(N). No supplied permutation or z is used.
    """
    n = len(x)
    if n < 1 or type(r) is not int or not 0 <= r <= n:
        raise ValueError("nonempty vector and integer 0<=r<=N required")
    if type(p) is not int or p < 2:
        raise ValueError("p must be a prevalidated prime")
    if type(omega) is not int or not 0 <= omega < p:
        raise ValueError("canonical root required")
    if any(type(v) is not int or not 0 <= v < p for v in x):
        raise ValueError("canonical field residues required")
    f = Field(p)
    powers = [1]
    v = 1
    for k in range(1, n + 1):
        v = f.mul(v, omega)
        if k < n:
            if f.eq(v, 1):
                raise ValueError("root has order smaller than N")
            powers.append(v)
        elif not f.eq(v, 1):
            raise ValueError("root is not an Nth root")
    nonzero = [(j, v) for j, v in enumerate(x) if not f.eq(v, 0)]
    m = len(nonzero)
    certificate = {"N": n, "r": r, "m": m}

    def spectral_progressions(terms):
        out = [0] * n
        for j, coefficient in terms:
            v = coefficient
            step = powers[j]
            for k in range(n):
                out[k] = f.add(out[k], v)
                v = f.mul(v, step)
        return out

    if m <= 2 * r:
        out = spectral_progressions(nonzero)
        certificate.update({"branch": "sparse_input", "accepted": True})
        return {"output": out, "certificate": certificate, "counts": f.counts}

    # Equality of ratios uses only cross products; all denominators are nonzero.
    balance, a, b = 0, 0, 1
    for j in range(n):
        u, v = x[j], x[(j - 1) % n]
        if f.eq(v, 0):
            continue
        if balance == 0:
            a, b, balance = u, v, 1
        elif f.eq(f.mul(u, b), f.mul(a, v)):
            balance += 1
        else:
            balance -= 1

    terms = []
    for j in range(n):
        d = f.sub(f.mul(b, x[j]), f.mul(a, x[(j - 1) % n]))
        if not f.eq(d, 0):
            terms.append((j, d))
    certificate.update({"a": a, "b": b, "vote_balance": balance,
                        "residual_support": [j for j, _ in terms],
                        "residual_nnz": len(terms)})
    if len(terms) > r:
        certificate.update({"branch": "outside_family", "accepted": False})
        return {"output": None, "certificate": certificate, "counts": f.counts}

    numerator = spectral_progressions(terms)
    denominators = [f.sub(b, f.mul(a, w)) for w in powers]
    regular, resonant = [], []
    for k, den in enumerate(denominators):
        (resonant if f.eq(den, 0) else regular).append(k)
    assert len(resonant) <= 1
    prefix = [1]
    for k in regular:
        prefix.append(f.mul(prefix[-1], denominators[k]))
    out = [0] * n
    if regular:
        inverse = f.inv(prefix[-1])
        for i in range(len(regular) - 1, -1, -1):
            k = regular[i]
            den_inverse = f.mul(inverse, prefix[i])
            out[k] = f.mul(numerator[k], den_inverse)
            inverse = f.mul(inverse, denominators[k])
    for k in resonant:
        v, total = 1, 0
        for value in x:
            total = f.add(total, f.mul(value, v))
            v = f.mul(v, powers[k])
        out[k] = total
    certificate.update({"branch": "twisted_residual", "accepted": True,
                        "resonant_bins": resonant})
    return {"output": out, "certificate": certificate, "counts": f.counts}
