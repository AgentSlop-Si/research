#!/usr/bin/env python3
"""Independent, standard-library-only check of inert F020 certificate data.

No producer program is imported, evaluated, or executed. Coefficients are
reconstructed in Z[q] before reduction, using the Gaussian Pascal recurrence
C(n,k)=C(n-1,k-1)+q**k C(n-1,k). All arrays are ascending.
"""
import hashlib
import json
from math import comb, isqrt
from pathlib import Path

BASE = Path(__file__).resolve().parent
SOURCE = BASE / "sources/modular_certificates.json"


def trim(a):
    a = list(a)
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a or [0]


def add(a, b):
    c = [0] * max(len(a), len(b))
    for i, x in enumerate(a):
        c[i] += x
    for i, x in enumerate(b):
        c[i] += x
    return trim(c)


def neg(a):
    return [-x for x in a]


def mul(a, b):
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i+j] += x*y
    return trim(c)


def eval_poly(a, x, modulus=None):
    v = 0
    for c in reversed(a):
        v = v*x+c
        if modulus is not None:
            v %= modulus
    return v


def mod_coeff(a, ell):
    return trim([x % ell for x in a])


def rem_monic(a, b):
    assert b[-1] == 1
    a = trim(a)
    while len(a) >= len(b) and a != [0]:
        c, offset = a[-1], len(a)-len(b)
        for j, y in enumerate(b):
            a[offset+j] -= c*y
        a = trim(a)
    return a


def mod_remainder(a, b, ell):
    a, b = mod_coeff(a, ell), mod_coeff(b, ell)
    assert b != [0]
    inv = pow(b[-1], -1, ell)
    while a != [0] and len(a) >= len(b):
        c, offset = a[-1]*inv % ell, len(a)-len(b)
        for j, y in enumerate(b):
            a[offset+j] = (a[offset+j]-c*y) % ell
        a = trim(a)
    return a


def mod_gcd(a, b, ell):
    a, b = mod_coeff(a, ell), mod_coeff(b, ell)
    while b != [0]:
        a, b = b, mod_remainder(a, b, ell)
    inv = pow(a[-1], -1, ell)
    return [(x*inv) % ell for x in a]


def deriv(a):
    return trim([i*a[i] for i in range(1, len(a))])


def is_prime(n):
    return n >= 2 and all(n % k for k in range(2, isqrt(n)+1))


def gaussian_rows(nmax):
    rows = [[[1]]]
    for n in range(1, nmax+1):
        prev = rows[-1]
        row = []
        for k in range(n+1):
            left = prev[k-1] if 0 < k <= n else [0]
            right = [0]*k + prev[k] if k < n else [0]
            row.append(add(left, right))
        assert row[0] == [1] == row[-1]
        assert row == row[::-1]
        assert all(all(type(c) is int and c >= 0 for c in a) for a in row)
        assert all(eval_poly(a, 1) == comb(n, k) for k, a in enumerate(row))
        rows.append(row)
    return rows


def divide_zplus1(H):
    """H has coefficient polynomials in Z[q]; monic division adds no fractions."""
    U = [H[0]]
    for h in H[1:-1]:
        U.append(add(h, neg(U[-1])))
    assert add(H[-1], neg(U[-1])) == [0], "nonzero z=-1 remainder"
    assert U[-1] == [1]
    return U


def check_bezout(A, f, B, g, ell):
    assert all(type(x) is int for a in [A, f, B, g] for x in a)
    return mod_coeff(add(mul(A, f), mul(B, g)), ell) == [1]


def main():
    payload = SOURCE.read_bytes()
    data = json.loads(payload)
    assert data["coefficient_order"] == "ascending"
    records = data["records"]
    expected = {(9, b) for b in range(3, 9)} | {(25, b) for b in range(5, 25)}
    assert len(records) == len(expected) == 26
    assert {(r["d"], r["b"]) for r in records} == expected
    assert len({(r["d"], r["b"]) for r in records}) == len(records)
    rows = gaussian_rows(24)
    ring_checks = []
    phi = {}
    for p in [3, 5]:
        d = p*p
        f = [int(i % p == 0) for i in range(d-p+1)]
        assert f[-1] == 1
        shifted = [sum(f[j]*comb(j, i) for j in range(i, len(f))) for i in range(len(f))]
        assert shifted[-1] == 1
        assert all(c % p == 0 for c in shifted[:-1])
        assert shifted[0] % p == 0 and shifted[0] % (p*p) != 0
        assert rem_monic([-1]+[0]*(d-1)+[1], f) == [0]
        phi[d] = f
        ring_checks.append({"d": d, "p": p, "Phi_ascending": f,
                            "Phi_xplus1_ascending": shifted,
                            "Eisenstein_at_p": True,
                            "divides_x_to_d_minus1": True})
    results, exact_data = [], []
    for r in records:
        d, b, ell, w = r["d"], r["b"], r["prime"], r["omega_image"]
        assert is_prime(ell) and ell > max(d, b)
        order = next(i for i in range(1, d+1) if pow(w, i, ell) == 1)
        assert order == d == r["root_order"]
        assert eval_poly(phi[d], w, ell) == 0
        Hq = rows[b]
        Uq = divide_zplus1(Hq) if b % 2 else Hq
        H = [eval_poly(c, w, ell) for c in Hq]
        U = [eval_poly(c, w, ell) for c in Uq]
        assert H == r["H_ascending"]
        assert U == r["U_ascending"]
        assert len(H) == b+1 and H[0] == H[-1] == 1
        assert len(U) == b+1-(b % 2) and U[-1] == 1
        F = [1]+[0]*(d-1)+[1]
        Hp = mod_coeff(deriv(H), ell)
        assert len(Hp) == b and Hp[-1] == b % ell != 0
        A, B = r["H_Hprime_bezout"]
        C, D = r["U_F_bezout"]
        assert check_bezout(A, H, B, Hp, ell)
        assert check_bezout(C, U, D, F, ell)
        assert mod_gcd(H, Hp, ell) == [1]
        assert mod_gcd(U, deriv(U), ell) == [1]
        assert mod_gcd(U, F, ell) == [1]
        assert mod_gcd(H, F, ell) == ([1, 1] if b % 2 else [1])
        assert eval_poly(U, -1, ell) != 0
        reduced_H = [rem_monic(c, phi[d]) for c in Hq]
        reduced_U = [rem_monic(c, phi[d]) for c in Uq]
        assert [eval_poly(c, w, ell) for c in reduced_H] == H
        assert [eval_poly(c, w, ell) for c in reduced_U] == U
        attempts = []
        for attempt in r["attempts"]:
            l, a = attempt["prime"], attempt["root"]
            assert is_prime(l) and eval_poly(phi[d], a, l) == 0
            assert next(i for i in range(1, d+1) if pow(a, i, l) == 1) == d
            h = [eval_poly(c, a, l) for c in Hq]
            u = [eval_poly(c, a, l) for c in Uq]
            gh = mod_gcd(h, deriv(h), l)
            gu = mod_gcd(u, F, l)
            assert len(gh)-1 == attempt["derivative_gcd_degree"]
            assert len(gu)-1 == attempt["node_gcd_degree"]
            attempts.append({"prime": l, "omega_image": a,
                             "H_Hprime_gcd_ascending": gh,
                             "U_F_gcd_ascending": gu,
                             "common_F_roots": [(-pow(a, j, l)) % l for j in range(d)
                                                if eval_poly(u, -pow(a, j, l), l) == 0]})
        results.append({"d": d, "b": b, "prime": ell, "omega_image": w,
                        "exact_root_order": order, "H_degree": b,
                        "U_degree": len(U)-1, "derivative_leading_coefficient": b,
                        "coefficient_reconstruction": True,
                        "H_Hprime_Bezout_identity": True, "U_F_Bezout_identity": True,
                        "independent_modular_gcds": True,
                        "U_at_minus1_mod_prime": eval_poly(U, -1, ell),
                        "attempts": attempts})
        exact_data.append({"d": d, "b": b,
                           "H_Zomega_coefficients_ascending": reduced_H,
                           "U_Zomega_coefficients_ascending": reduced_U})
    output = {"decision": "PASS", "records_checked": len(results),
              "Bezout_identities_checked": 2*len(results),
              "producer_programs_executed": False,
              "source_sha256": hashlib.sha256(payload).hexdigest(),
              "scope": "Characteristic-zero residual guards for d=9,b=3..8 and d=25,b=5..24 only",
              "cyclotomic_integrality_and_irreducibility": ring_checks,
              "records": results}
    (BASE/"verification_results.json").write_text(json.dumps(output, indent=2)+"\n")
    (BASE/"independent_exact_coefficients.json").write_text(json.dumps(exact_data, indent=2)+"\n")
    print(json.dumps({k: v for k, v in output.items() if k != "records"}, indent=2))
    for r in results:
        print(f"PASS d={r['d']} b={r['b']} ell={r['prime']}: coefficient identity and both Bezout certificates")
    print("BAD-REDUCTION CONTROL:")
    print(json.dumps(next(r for r in results if (r['d'], r['b']) == (25, 9))["attempts"], indent=2))


if __name__ == "__main__":
    main()
