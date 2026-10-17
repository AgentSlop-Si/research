#!/usr/bin/env python3
"""Fresh exact arithmetic controls; no imported research code or author tests.

Exponents are computed in Z/q; coefficient arithmetic is performed separately.
This explicitly permits coefficient characteristic 2 for odd q.
"""
import hashlib
import json
from pathlib import Path


class PrimeField:
    def __init__(self, p):
        self.size = self.characteristic = p
        self.name = f"GF({p})"
    def add(self, a, b): return (a + b) % self.size
    def mul(self, a, b): return a * b % self.size
    def integer(self, n): return n % self.size
    def power(self, a, n): return pow(a, n, self.size)
    def inverse(self, a):
        assert a
        return pow(a, -1, self.size)


class BinaryField:
    def __init__(self, degree, modulus):
        self.size = 1 << degree
        self.characteristic = 2
        self.modulus = modulus
        self.name = f"GF(2^{degree}), polynomial {modulus:#b}"
        # Verify the quotient really is a field, without trusting the polynomial.
        for a in range(1, self.size):
            assert self.mul(a, self.power(a, self.size - 2)) == 1
    def add(self, a, b): return a ^ b
    def mul(self, a, b):
        result = 0
        while b:
            if b & 1:
                result ^= a
            b >>= 1
            a <<= 1
            if a & self.size:
                a ^= self.modulus
        return result
    def integer(self, n): return n & 1
    def power(self, a, n):
        result = 1
        while n:
            if n & 1:
                result = self.mul(result, a)
            a = self.mul(a, a)
            n >>= 1
        return result
    def inverse(self, a):
        assert a
        return self.power(a, self.size - 2)


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def run_case(q, field, accepted_domain=True):
    counts = {}
    def check(condition, category):
        counts[category] = counts.get(category, 0) + 1
        if not condition:
            raise AssertionError((q, field.name, category, counts[category]))
    mul, add = field.mul, field.add
    def total(values):
        answer = 0
        for value in values:
            answer = add(answer, value)
        return answer
    def exact_order(a, order):
        return field.power(a, order) == 1 and all(
            field.power(a, d) != 1 for d in range(1, order) if order % d == 0)
    roots = [a for a in range(1, field.size) if exact_order(a, q)]
    check(bool(roots), "root_exists")
    root = roots[0]
    powers = [field.power(root, exponent) for exponent in range(q)]
    zeta = lambda exponent: powers[exponent % q]
    iq = field.inverse(field.integer(q))
    ih = pow(2, -1, q)  # Only the exponent ring divides by 2.

    # K_b[d] is the actual operator entry U_b[x,y] with d=y-x.
    K = []
    for b in range(q):
        row = [mul(iq, total(zeta(-b * z * z * ih + d * z)
                             for z in range(q))) for d in range(q)]
        K.append(row)
        for x in range(q):
            for y in range(q):
                # Separately construct the three Fourier/chirp factors.
                product = total(mul(mul(mul(iq, zeta(-x * z)),
                                        zeta(-b * z * z * ih)), zeta(z * y))
                                for z in range(q))
                check(product == row[(y - x) % q], "fourier_conjugation_entries")
        if b == 0:
            for d in range(q):
                check(row[d] == int(d == 0), "zero_shear_entries")
            continue
        g = gcd(b, q)
        m = q // g
        u = b // g
        iu = pow(u, -1, m)
        i2 = pow(2, -1, m)
        eta = lambda exponent: zeta(g * exponent)
        G = total(eta(-u * z * z * i2) for z in range(m))
        Gminus = total(eta(u * z * z * i2) for z in range(m))
        check(mul(G, Gminus) == field.integer(m), "gauss_nonvanishing_product")
        check(G != 0, "gauss_nonzero")
        kappa = mul(field.inverse(field.integer(m)), G)
        for d in range(q):
            check((row[d] != 0) == (d % g == 0), "exact_support")
            expected = 0 if d % g else mul(kappa, eta((d // g) ** 2 * i2 * iu))
            check(row[d] == expected, "completed_square_entries")
        for x in range(q):
            check(sum(row[(y - x) % q] != 0 for y in range(q)) == m,
                  "row_support_count")
        ratio = mul(mul(row[0], row[0]), field.inverse(mul(row[g], row[-g])))
        check(ratio == eta(-iu), "signed_core_ratio")
        check(exact_order(ratio, m), "signed_core_exact_order")

    # Full entrywise sparse-matrix Weyl covariance, all b,a,c,x,y.
    # (U_b D(a,c))[x,y] = K_b[y+a-x] zeta^(c(y+a/2)).
    # (D(a+bc,c) U_b)[x,y] = zeta^(c(x-(a+bc)/2)) K_b[y-x+a+bc].
    for b in range(q):
        for a in range(q):
            for c in range(q):
                shifted_a = (a + b * c) % q
                left_phase = [zeta(c * (y + a * ih)) for y in range(q)]
                right_phase = [zeta(c * (x - shifted_a * ih)) for x in range(q)]
                for x in range(q):
                    for y in range(q):
                        lhs = mul(K[b][(y + a - x) % q], left_phase[y])
                        rhs = mul(right_phase[x], K[b][(y - x + shifted_a) % q])
                        check(lhs == rhs, "weyl_covariance_entries")

    # Exact additive law, including cancellation b+c=0 and identity factors.
    # Circulant products reduce every matrix entry to one of these d cases.
    for b in range(q):
        for c in range(q):
            for d in range(q):
                composed = total(mul(K[b][z], K[c][(d - z) % q]) for z in range(q))
                check(composed == K[(b + c) % q][d], "shear_law_circulant_entries")

    # Check F and C labels themselves, independently of U's label.
    for a in range(q):
        for c in range(q):
            for x in range(q):
                for y in range(q):
                    fd = mul(zeta(x * (y + a)), zeta(c * (y + a * ih)))
                    df = mul(zeta(a * (x + c * ih)), zeta((x + c) * y))
                    check(fd == df, "fourier_weyl_label_entries")
            for b in range(q):
                for x in range(q):
                    cd = zeta(b * x * x * ih + c * (x - a * ih))
                    dc = zeta((c + b * a) * (x - a * ih) + b * (x - a) ** 2 * ih)
                    check(cd == dc, "chirp_weyl_label_entries")

    # The old sign must be distinguished even though support/order agree.
    for b in range(1, q):
        check(K[b] != K[-b % q], "wrong_chirp_rejected")
        g = gcd(b, q)
        m = q // g
        u = b // g
        good = zeta(-g * pow(u, -1, m))
        wrong = zeta(g * pow(u, -1, m))
        check(good != wrong, "wrong_signed_ratio_rejected")
        check(exact_order(good, m) and exact_order(wrong, m),
              "order_only_control_cannot_distinguish")

    # Representative noncanonical integers must reduce to the same operator.
    for b in (-2 * q - 1, -q, -1, q, q + 1, 3 * q + 2):
        for d in range(q):
            direct = mul(iq, total(zeta(-b * z * z * ih + d * z) for z in range(q)))
            check(direct == K[b % q][d], "noncanonical_scalar_entries")
    return {"q": q, "coefficient_field": field.name,
            "coefficient_characteristic": field.characteristic,
            "root_integer_encoding": root, "counts": counts,
            "within_requested_prime_power_scope": accepted_domain,
            "status": "PASS"}


def main():
    cases = [(3, PrimeField(7)), (5, PrimeField(11)), (7, PrimeField(29)),
             (9, PrimeField(19)), (25, PrimeField(101)), (27, PrimeField(109)),
             (3, BinaryField(2, 0b111)), (7, BinaryField(3, 0b1011)),
             (9, BinaryField(6, 0b1000011))]
    results = []
    for q, field in cases:
        result = run_case(q, field)
        results.append(result)
        print(f"PASS q={q} in {field.name}: {sum(result['counts'].values()):,} checks", flush=True)
    # Diagnostic only: the gcd-based proof needs oddness, not prime powers.
    results.append(run_case(15, PrimeField(31), accepted_domain=False))
    payload = {"status": "PASS", "scope": "Fresh one-dimensional formula controls only",
               "historical_or_author_code_imported_or_executed": False,
               "cases": results,
               "total_checks": sum(sum(item["counts"].values()) for item in results),
               "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    path = Path(__file__).with_name("EXACT_FINITE_FIELD_RESULTS.json")
    path.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"TOTAL PASS: {payload['total_checks']:,} checks; {path.name}")


if __name__ == "__main__":
    main()
