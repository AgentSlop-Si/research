"""Independent review controls. Fresh code; no source/uploaded code imported.

Construct partial FFTs in closed form, not by the earlier butterfly program.
Construct the commutator linear map by applying it to matrix units.
"""
import hashlib
import json
from pathlib import Path


def identity(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def product(a, b, p):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) % p
             for j in range(len(b[0]))] for i in range(len(a))]


def rref(a, p):
    a = [row[:] for row in a]
    lead = 0
    pivots = []
    for col in range(len(a[0])):
        rows = [row for row in range(lead, len(a)) if a[row][col] % p]
        if not rows:
            continue
        a[lead], a[rows[0]] = a[rows[0]], a[lead]
        scale = pow(a[lead][col], -1, p)
        a[lead] = [x * scale % p for x in a[lead]]
        for row in range(len(a)):
            if row != lead:
                scale = a[row][col]
                a[row] = [(x - scale * y) % p
                          for x, y in zip(a[row], a[lead])]
        pivots.append(col)
        lead += 1
        if lead == len(a):
            break
    return a, pivots


def inverse(a, p):
    n = len(a)
    reduced, pivots = rref([row + unit for row, unit in zip(a, identity(n))], p)
    assert pivots[:n] == list(range(n))
    result = [row[n:] for row in reduced]
    assert product(a, result, p) == identity(n)
    return result


def hom_dimension(a, b, p):
    # A C = C B. Build every column of the map by actual matrix products.
    na, nb = len(a), len(b)
    columns = []
    for i in range(na):
        for j in range(nb):
            e = [[int(k == i and ell == j) for ell in range(nb)]
                 for k in range(na)]
            ae, eb = product(a, e, p), product(e, b, p)
            columns.append([(ae[k][ell] - eb[k][ell]) % p
                            for k in range(na) for ell in range(nb)])
    matrix = [list(row) for row in zip(*columns)]
    return na * nb - len(rref(matrix, p)[1])


def reverse_bits(j, count):
    return sum(((j >> k) & 1) << (count - k - 1) for k in range(count))


def closed_partial_transform(n, s, omega, p):
    # In each size-2^s block use F_(2^s) P_(2^s), then global P_n.
    m, bits = 1 << s, n.bit_length() - 1
    result = [[0] * n for _ in range(n)]
    for col in range(n):
        reversed_col = reverse_bits(col, bits)
        block, local_col = divmod(reversed_col, m)
        for local_row in range(m):
            exponent = (n // m) * local_row * reverse_bits(local_col, s)
            result[block * m + local_row][col] = pow(omega, exponent, p)
    return result


def monomial_cycles(a, p):
    n = len(a)
    assert all(sum(x != 0 for x in row) == 1 for row in a)
    assert all(sum(a[i][j] != 0 for i in range(n)) == 1 for j in range(n))
    target = [next(i for i in range(n) if a[i][j]) for j in range(n)]
    cycles = []
    remaining = set(range(n))
    while remaining:
        first, holonomy, indices = min(remaining), 1, []
        j = first
        while j in remaining:
            remaining.remove(j)
            indices.append(j)
            holonomy = holonomy * a[target[j]][j] % p
            j = target[j]
        assert j == first
        cycles.append((indices, holonomy))
    return cycles


def polynomial_multiply(a, b, p):
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i+j] = (c[i+j] + x*y) % p
    return c


def canonical_cycle(length, holonomy, p):
    a = [[0] * length for _ in range(length)]
    for j in range(length - 1):
        a[j+1][j] = 1
    a[0][length-1] = holonomy % p
    return a


def direct_sum(blocks):
    n = sum(len(a) for a in blocks)
    out, start = [[0] * n for _ in range(n)], 0
    for a in blocks:
        for i, row in enumerate(a):
            for j, x in enumerate(row):
                out[start+i][start+j] = x
        start += len(a)
    return out


def one_run(n, p):
    omega = next(x for x in range(2, p)
                 if pow(x, n, p) == 1 and pow(x, n//2, p) != 1)
    x = canonical_cycle(n, 1, p)
    records = []
    prior_m = prior_r = None
    for s in range(n.bit_length()):
        b, length = 1 << s, n // (1 << s)
        m = closed_partial_transform(n, s, omega, p)
        mi = inverse(m, p)
        r = product(product(m, x, p), mi, p)
        assert product(m, x, p) == product(r, m, p)
        if prior_m is not None:
            transition = product(m, inverse(prior_m, p), p)
            assert product(transition, prior_r, p) == product(r, transition, p)
        cycles = monomial_cycles(r, p)
        assert len(cycles) == b and all(len(c) == length for c, _ in cycles)
        holonomies = [h for _, h in cycles]
        assert len(set(holonomies)) == b
        cycle_polynomial_product = [1]
        for h in holonomies:
            cycle_polynomial_product = polynomial_multiply(
                cycle_polynomial_product, [(-h) % p] + [0] * (length-1) + [1], p)
        assert cycle_polynomial_product == [p-1] + [0] * (n-1) + [1]
        # Every pair's monic polynomials differ by a nonzero constant.
        gcd_certificates = []
        for i in range(b):
            for j in range(i+1, b):
                # alpha*(t^L-eta_i) + beta*(t^L-eta_j) = 1.
                alpha = pow((holonomies[j] - holonomies[i]) % p, -1, p)
                beta = -alpha % p
                assert (alpha + beta) % p == 0
                assert (-alpha * holonomies[i] - beta * holonomies[j]) % p == 1
                gcd_certificates.append([i, j, alpha, beta])
        blocks = [[[r[i][j] for j in indices] for i in indices] for indices, _ in cycles]
        hom_dims = [[hom_dimension(a, bb, p) for bb in blocks] for a in blocks]
        assert hom_dims == [[length if i == j else 0 for j in range(b)] for i in range(b)]
        centralizer_dim = hom_dimension(r, r, p)
        assert centralizer_dim == n
        repeated = direct_sum([canonical_cycle(length, 1, p) for _ in range(b)])
        repeated_dim = hom_dimension(repeated, repeated, p)
        assert repeated_dim == b*b*length
        repeated_cross = hom_dimension(canonical_cycle(length, 1, p), canonical_cycle(length, 1, p), p)
        assert repeated_cross == length
        # Independent dimension check: all I, R, ..., R^(N-1) are independent.
        powers, acc = [], identity(n)
        for _ in range(n):
            powers.append([v for row in acc for v in row])
            acc = product(acc, r, p)
        polynomial_span_rank = len(rref(powers, p)[1])
        assert polynomial_span_rank == n and acc == identity(n)
        records.append({"stage": s, "cycle_length": length,
                        "cycle_coordinates": [c for c, _ in cycles], "holonomies": holonomies,
                        "full_centralizer_dimension": centralizer_dim,
                        "polynomial_span_rank": polynomial_span_rank,
                        "pair_hom_dimensions": hom_dims,
                        "bezout_certificates_i_j_alpha_beta": gcd_certificates,
                        "identical_holonomy_positive_control_dimension": repeated_dim,
                        "identical_holonomy_pair_hom_dimension": repeated_cross})
        prior_m, prior_r = m, r
    dft = [[pow(omega, i*j, p) for j in range(n)] for i in range(n)]
    assert prior_m == dft
    assert prior_r == [[pow(omega, i, p) if i == j else 0 for j in range(n)] for i in range(n)]
    assert [sum(row) % p for row in [[row[0]] for row in prior_m]] == [1]*n
    # A changed operator does permit more commutants: R_final^N = I.
    changed_power_dimension = hom_dimension(identity(n), identity(n), p)
    assert changed_power_dimension == n*n
    # A genuine invariant restriction retains distinct eigenvalues.
    restriction = [row[:n//2] for row in prior_r[:n//2]]
    restriction_dimension = hom_dimension(restriction, restriction, p)
    assert restriction_dimension == n//2
    return {"N": n, "prime": p, "omega": omega, "stages": records,
            "full_similarity_and_local_transport": "PASS", "full_DFT_and_seed": "PASS",
            "changed_operator_R_to_N_centralizer_dimension": changed_power_dimension,
            "half_spectrum_invariant_restriction_centralizer_dimension": restriction_dimension}


if __name__ == "__main__":
    out = Path(__file__).resolve().parent
    data = {"status": "PASS", "construction": "Closed partial Fourier blocks, independent of prior butterfly program",
            "linear_algebra": "Exact finite-field matrix-unit commutator maps and polynomial-span ranks",
            "source_or_uploaded_code_executed": False,
            "runs": [one_run(4, 17), one_run(8, 17), one_run(8, 97)]}
    (out / "INDEPENDENT_CONTROLS.json").write_text(json.dumps(data, indent=2) + "\n")
    print(json.dumps({"status": data["status"], "runs": [{"N": r["N"], "p": r["prime"],
          "stage_dimensions": [s["full_centralizer_dimension"] for s in r["stages"]],
          "positive_control_dimensions": [s["identical_holonomy_positive_control_dimension"] for s in r["stages"]]}
          for r in data["runs"]]}, indent=2))
