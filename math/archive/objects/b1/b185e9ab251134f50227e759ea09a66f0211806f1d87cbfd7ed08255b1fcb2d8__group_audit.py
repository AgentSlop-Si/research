from __future__ import annotations

from collections import Counter, deque
from dataclasses import asdict, dataclass
from random import Random

from tensor_weil import (
    coefficient_field,
    identity,
    is_symplectic,
    linear_symplectic,
    lower_chirp_symplectic,
    mat_mul,
    partial_weyl_symplectic,
    random_word,
    support_counts,
    symplectic_identity,
    upper_right_rank,
)


def _key(a: list[list[int]]) -> tuple[int, ...]:
    return tuple(x for row in a for x in row)


def _matrix(k: tuple[int, ...], n: int) -> list[list[int]]:
    d = 2 * n
    return [list(k[i * d:(i + 1) * d]) for i in range(d)]


def sp4_3_generators() -> list[list[list[int]]]:
    p, n = 3, 2
    c1 = [[1, 0], [0, 0]]
    c2 = [[0, 0], [0, 1]]
    c12 = [[0, 1], [1, 0]]
    swap = [[0, 1], [1, 0]]
    shear = [[1, 1], [0, 1]]
    scale = [[2, 0], [0, 1]]
    return [
        lower_chirp_symplectic(c1, p),
        lower_chirp_symplectic(c2, p),
        lower_chirp_symplectic(c12, p),
        linear_symplectic(swap, p),
        linear_symplectic(shear, p),
        linear_symplectic(scale, p),
        partial_weyl_symplectic(n, [0], p),
    ]


def exhaustive_sp4_3_rank_distribution() -> dict[int, int]:
    p, n = 3, 2
    gens = sp4_3_generators()
    start = _key(symplectic_identity(n))
    seen = {start}
    queue = deque([start])
    counts: Counter[int] = Counter()
    while queue:
        k = queue.popleft()
        s = _matrix(k, n)
        assert is_symplectic(s, p)
        counts[upper_right_rank(s, p)] += 1
        for g in gens:
            nk = _key(mat_mul(g, s, p))
            if nk not in seen:
                seen.add(nk)
                queue.append(nk)
    if len(seen) != 51840:
        raise AssertionError(f"generated {len(seen)} elements, expected 51840")
    return dict(sorted(counts.items()))


@dataclass
class SupportAudit:
    p: int
    n: int
    trials: int
    checked_dense_cross_ratios: int
    max_word_length: int


def random_support_audit(p: int, n: int, trials: int = 120, seed: int = 2401) -> SupportAudit:
    q = p ** n
    ell, zeta = coefficient_field(q)
    omega = pow(zeta, q // p, ell)
    rng = Random(seed + 100 * p + n)
    dense_cross = 0
    for _ in range(trials):
        length = rng.randrange(1, 13)
        s, u, _stage_ranks = random_word(p, n, ell, omega, length, rng)
        r = upper_right_rank(s, p)
        rows, cols = support_counts(u, ell)
        want = p ** r
        if set(rows) != {want} or set(cols) != {want}:
            raise AssertionError((p, n, length, r, set(rows), set(cols)))
        if r == n:
            dense_cross += 1
    return SupportAudit(p, n, trials, dense_cross, 12)


def run_audit() -> dict:
    dist = exhaustive_sp4_3_rank_distribution()
    support = [
        asdict(random_support_audit(3, 2)),
        asdict(random_support_audit(3, 3, trials=80)),
        asdict(random_support_audit(5, 2, trials=80)),
    ]
    return {
        "sp4_3_size": sum(dist.values()),
        "sp4_3_rank_B_distribution": {str(k): v for k, v in dist.items()},
        "support_audits": support,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_audit(), indent=2, sort_keys=True))
