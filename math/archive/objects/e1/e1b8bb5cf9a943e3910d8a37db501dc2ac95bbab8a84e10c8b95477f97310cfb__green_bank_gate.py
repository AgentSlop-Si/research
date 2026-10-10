from __future__ import annotations

"""Exact certificates for sums of independently ordered cyclic Green resolvents.

The main structural fact is elementary:
for t total orders on the same finite set there are two equally sized disjoint
subsets separated in every order, of size at least floor(N/2**t).
On such a rectangle every diagonally gauged cyclic Green kernel has rank one.

The finite-field routines below are only reproducibility certificates for the
complex theorem.  They do not replace Chebotarev's complex Fourier-minor theorem.
"""

from dataclasses import dataclass, asdict
from itertools import permutations
import json
import math
import random
from pathlib import Path
from typing import Iterable, Sequence


# ---------- elementary finite-field helpers ----------

def is_prime_64(n: int) -> bool:
    if n < 2:
        return False
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for p in small:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        s += 1
        d //= 2
    # Deterministic Miller--Rabin bases for unsigned 64-bit integers.
    for a in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        if a % n == 0:
            continue
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True


def factor_distinct(n: int) -> list[int]:
    out: list[int] = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        out.append(n)
    return out


def primitive_root_mod_prime(p: int) -> int:
    if not is_prime_64(p):
        raise ValueError("modulus must be prime")
    factors = factor_distinct(p - 1)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in factors):
            return g
    raise RuntimeError("primitive root not found")


def primitive_nth_root(p: int, n: int) -> int:
    if (p - 1) % n:
        raise ValueError("n must divide p-1")
    g = primitive_root_mod_prime(p)
    w = pow(g, (p - 1) // n, p)
    if pow(w, n, p) != 1:
        raise AssertionError("root order failure")
    for q in factor_distinct(n):
        if pow(w, n // q, p) == 1:
            raise AssertionError("root is not primitive")
    return w


def inv_mod(x: int, p: int) -> int:
    x %= p
    if x == 0:
        raise ZeroDivisionError
    return pow(x, p - 2, p)


def rank_mod(matrix: Sequence[Sequence[int]], p: int) -> int:
    if not matrix:
        return 0
    a = [[int(x) % p for x in row] for row in matrix]
    m, n = len(a), len(a[0])
    r = 0
    for c in range(n):
        pivot = next((i for i in range(r, m) if a[i][c] % p), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        z = inv_mod(a[r][c], p)
        a[r] = [(z * x) % p for x in a[r]]
        for i in range(m):
            if i != r and a[i][c]:
                z = a[i][c]
                a[i] = [(a[i][j] - z * a[r][j]) % p for j in range(n)]
        r += 1
        if r == m:
            break
    return r


def det_mod(matrix: Sequence[Sequence[int]], p: int) -> int:
    n = len(matrix)
    if any(len(row) != n for row in matrix):
        raise ValueError("square matrix required")
    a = [[int(x) % p for x in row] for row in matrix]
    det = 1
    for c in range(n):
        pivot = next((i for i in range(c, n) if a[i][c]), None)
        if pivot is None:
            return 0
        if pivot != c:
            a[c], a[pivot] = a[pivot], a[c]
            det = (-det) % p
        pv = a[c][c]
        det = det * pv % p
        z = inv_mod(pv, p)
        for i in range(c + 1, n):
            if a[i][c]:
                f = a[i][c] * z % p
                for j in range(c, n):
                    a[i][j] = (a[i][j] - f * a[c][j]) % p
    return det


# ---------- permutations and simultaneous separation ----------

def permutation_cycles(perm: Sequence[int]) -> list[list[int]]:
    n = len(perm)
    if sorted(perm) != list(range(n)):
        raise ValueError("not a permutation")
    seen = [False] * n
    cycles: list[list[int]] = []
    for start in range(n):
        if seen[start]:
            continue
        cyc: list[int] = []
        x = start
        while not seen[x]:
            seen[x] = True
            cyc.append(x)
            x = perm[x]
        cycles.append(cyc)
    return cycles


def cycle_metadata(perm: Sequence[int]) -> tuple[list[int], list[int], list[int]]:
    """Return cycle id, position in cycle, and cycle length for every vertex."""
    cycles = permutation_cycles(perm)
    cid = [0] * len(perm)
    pos = [0] * len(perm)
    clen = [0] * len(perm)
    for r, cyc in enumerate(cycles):
        for k, x in enumerate(cyc):
            cid[x] = r
            pos[x] = k
            clen[x] = len(cyc)
    return cid, pos, clen


def random_n_cycle(n: int, rng: random.Random) -> list[int]:
    order = list(range(n))
    rng.shuffle(order)
    p = [0] * n
    for i, x in enumerate(order):
        p[x] = order[(i + 1) % n]
    return p


def random_permutation_with_cycles(n: int, c: int, rng: random.Random) -> list[int]:
    if not (1 <= c <= n):
        raise ValueError("bad cycle count")
    order = list(range(n))
    rng.shuffle(order)
    # Positive lengths summing to n.
    cuts = sorted(rng.sample(range(1, n), c - 1)) if c > 1 else []
    bounds = [0] + cuts + [n]
    p = [0] * n
    for a, b in zip(bounds, bounds[1:]):
        cyc = order[a:b]
        for i, x in enumerate(cyc):
            p[x] = cyc[(i + 1) % len(cyc)]
    return p


def simultaneous_separated_sets(
    orders: Sequence[Sequence[int]],
    universe: Sequence[int] | None = None,
) -> tuple[list[int], list[int], list[int]]:
    """Find equal sets A,B separated in every total order.

    ``orders[r][x]`` is the position of element x in order r.
    The returned orientation is +1 if A precedes B and -1 otherwise.
    Guaranteed size: floor(|universe|/2**len(orders)).
    """
    if not orders:
        raise ValueError("at least one order required")
    n = len(orders[0])
    if any(len(o) != n for o in orders):
        raise ValueError("order sizes differ")
    U = list(range(n)) if universe is None else list(universe)
    if len(set(U)) != len(U):
        raise ValueError("universe repeats elements")

    # First order: lower and upper halves.
    sorted_u = sorted(U, key=lambda x: orders[0][x])
    m = len(sorted_u) // 2
    A = sorted_u[:m]
    B = sorted_u[-m:] if m else []
    orient = [1]

    for o in orders[1:]:
        m = len(A)
        merged = sorted(A + B, key=lambda x: o[x])
        prefix = set(merged[:m])
        A_low = [x for x in A if x in prefix]
        B_high = [x for x in B if x not in prefix]
        B_low = [x for x in B if x in prefix]
        A_high = [x for x in A if x not in prefix]
        if len(A_low) != len(B_high) or len(B_low) != len(A_high):
            raise AssertionError("balance identity failed")
        if len(A_low) >= len(B_low):
            A, B = A_low, B_high
            orient.append(1)
        else:
            # Swap the old sides.  This flips all previous orientations.
            A, B = B_low, A_high
            orient = [-s for s in orient]
            orient.append(1)

    for o, s in zip(orders, orient):
        if A and B:
            if s == 1:
                assert max(o[x] for x in A) < min(o[y] for y in B)
            else:
                assert min(o[x] for x in A) > max(o[y] for y in B)
    return A, B, orient


def common_cycle_cell(perms: Sequence[Sequence[int]]) -> tuple[list[int], list[list[int]], int]:
    """Largest cell in which every permutation has a fixed cycle label."""
    if not perms:
        raise ValueError("permutations required")
    n = len(perms[0])
    metadata = [cycle_metadata(p) for p in perms]
    cells: dict[tuple[int, ...], list[int]] = {}
    for x in range(n):
        key = tuple(meta[0][x] for meta in metadata)
        cells.setdefault(key, []).append(x)
    cell = max(cells.values(), key=lambda z: (len(z), [-x for x in z]))
    orders = [meta[1] for meta in metadata]
    cycle_product = math.prod(len(permutation_cycles(p)) for p in perms)
    return cell, orders, cycle_product


# ---------- Green and Fourier rectangles ----------

def green_entry(
    perm: Sequence[int], alpha: int, left: Sequence[int], right: Sequence[int],
    i: int, j: int, mod: int,
) -> int:
    cid, pos, clen = cycle_metadata(perm)
    if cid[i] != cid[j]:
        return 0
    L = clen[i]
    den = (1 - pow(alpha, L, mod)) % mod
    if den == 0:
        raise ValueError("singular Green cycle")
    dist = (pos[i] - pos[j]) % L
    return left[i] * pow(alpha, dist, mod) % mod * right[j] % mod * inv_mod(den, mod) % mod


def green_rectangle(
    perm: Sequence[int], alpha: int, left: Sequence[int], right: Sequence[int],
    rows: Sequence[int], cols: Sequence[int], mod: int,
) -> list[list[int]]:
    return [[green_entry(perm, alpha, left, right, i, j, mod) for j in cols] for i in rows]


def fourier_rectangle(rows: Sequence[int], cols: Sequence[int], root: int, mod: int) -> list[list[int]]:
    return [[pow(root, (i * j) % (mod - 1), mod) for j in cols] for i in rows]


@dataclass
class CertificateRow:
    t: int
    n: int
    field_modulus: int
    separated_size: int
    threshold: int
    sum_rank: int
    fourier_rank: int
    fourier_det: int
    term_ranks: list[int]
    orientations: list[int]


def find_field_for_n(n: int) -> int:
    k = 1
    while True:
        p = k * n + 1
        if is_prime_64(p):
            return p
        k += 1


def certify_hamiltonian_case(t: int, n: int, seed: int = 1800) -> CertificateRow:
    if not is_prime_64(n):
        raise ValueError("complex theorem uses prime transform length")
    rng = random.Random(seed + 1009 * t + n)
    perms = [random_n_cycle(n, rng) for _ in range(t)]
    orders = [cycle_metadata(p)[1] for p in perms]
    A, B, orientations = simultaneous_separated_sets(orders)
    s = len(A)
    if s <= t:
        raise ValueError("case does not cross the rank gate")

    q = find_field_for_n(n)
    w = primitive_nth_root(q, n)
    total = [[0] * s for _ in range(s)]
    term_ranks: list[int] = []
    for r, perm in enumerate(perms):
        while True:
            alpha = rng.randrange(0, q)
            if pow(alpha, n, q) != 1:
                break
        left = [rng.randrange(1, q) for _ in range(n)]
        right = [rng.randrange(1, q) for _ in range(n)]
        G = green_rectangle(perm, alpha, left, right, A, B, q)
        rr = rank_mod(G, q)
        term_ranks.append(rr)
        if rr > 1:
            raise AssertionError("separated Green rectangle exceeded rank one")
        for i in range(s):
            for j in range(s):
                total[i][j] = (total[i][j] + G[i][j]) % q
    sum_rank = rank_mod(total, q)
    F = fourier_rectangle(A, B, w, q)
    fourier_rank = rank_mod(F, q)
    determinant = det_mod(F, q)
    if sum_rank > t:
        raise AssertionError("sum rank exceeds number of terms")
    if fourier_rank != s or determinant == 0:
        raise AssertionError("chosen finite-field Fourier certificate vanished")
    return CertificateRow(
        t=t,
        n=n,
        field_modulus=q,
        separated_size=s,
        threshold=(2 ** t) * (t + 1),
        sum_rank=sum_rank,
        fourier_rank=fourier_rank,
        fourier_det=determinant,
        term_ranks=term_ranks,
        orientations=orientations,
    )


def certify_bounded_cycle_case(t: int, n: int, cycles_each: int, seed: int = 2818) -> dict:
    rng = random.Random(seed + n + 31 * t + 101 * cycles_each)
    perms = [random_permutation_with_cycles(n, cycles_each, rng) for _ in range(t)]
    cell, orders, product_bound = common_cycle_cell(perms)
    A, B, orientation = simultaneous_separated_sets(orders, cell)
    return {
        "t": t,
        "n": n,
        "cycles_each": cycles_each,
        "cycle_product_bound": product_bound,
        "largest_common_cycle_cell": len(cell),
        "separated_size": len(A),
        "guaranteed_floor": n // (product_bound * (2 ** t)),
        "orientations": orientation,
    }


def exhaustive_two_order_check(n: int) -> dict:
    """Fix the first order and exhaust every second order."""
    first = list(range(n))
    minimum = n
    count = 0
    histogram: dict[int, int] = {}
    for p in permutations(range(n)):
        pos = [0] * n
        for i, x in enumerate(p):
            pos[x] = i
        A, B, _ = simultaneous_separated_sets([first, pos])
        s = len(A)
        minimum = min(minimum, s)
        histogram[s] = histogram.get(s, 0) + 1
        count += 1
    return {
        "n": n,
        "permutations_checked": count,
        "minimum_separated_size": minimum,
        "guaranteed_floor": n // 4,
        "histogram": {str(k): v for k, v in sorted(histogram.items())},
    }


def generate_results() -> dict:
    test_ns = {2: 13, 3: 37, 4: 83, 5: 193, 6: 449, 7: 1031, 8: 2309}
    certs = [asdict(certify_hamiltonian_case(t, n)) for t, n in test_ns.items()]
    bounded = [
        certify_bounded_cycle_case(2, 109, 3),
        certify_bounded_cycle_case(3, 257, 2),
        certify_bounded_cycle_case(4, 1297, 2),
    ]
    exhaustive = exhaustive_two_order_check(8)
    boundary = []
    rng = random.Random(18018)
    for t, n in [(3, 31), (4, 79), (5, 191)]:
        perms = [random_n_cycle(n, rng) for _ in range(t)]
        orders = [cycle_metadata(p)[1] for p in perms]
        A, B, _ = simultaneous_separated_sets(orders)
        boundary.append({
            "t": t,
            "n": n,
            "separated_size": len(A),
            "gate_conclusive": len(A) > t,
        })
    return {
        "theorem": {
            "hamiltonian_gate": "floor(N/2^t) <= t is necessary",
            "equivalent_threshold": "N < 2^t (t+1)",
            "bounded_cycle_gate": "floor(N/(2^t product(c_r))) <= t is necessary",
            "term_lower_bound": "t >= log2(N)-log2(t+1); hence t=Omega(log N)",
        },
        "exact_hamiltonian_certificates": certs,
        "bounded_cycle_certificates": bounded,
        "exhaustive_two_order": exhaustive,
        "subthreshold_random_instances": boundary,
    }


if __name__ == "__main__":
    out = generate_results()
    target = Path(__file__).with_name("results.json")
    target.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps(out, indent=2, sort_keys=True))
