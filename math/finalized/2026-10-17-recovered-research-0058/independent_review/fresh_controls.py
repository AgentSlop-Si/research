"""Independent controls written for the recovered pair and radix review.

No author or historical program is imported. Integer arithmetic is an exact
oracle; explicit volumes, rather than runtime, test the stated scan ledger.
"""
from itertools import combinations
from pathlib import Path
import json
import random


def pair_controls():
    rng = random.Random(202610170058)
    n = 5
    edges = list(combinations(range(n), 2))
    size = 1 << len(edges)
    count = budget_count = 0
    for trial in range(40):
        solo = [rng.randrange(0, 13) for _ in range(n)]
        costs = [max(solo[u], solo[v]) + rng.randrange(0, 10)
                 for u, v in edges]
        memory = [rng.randrange(0, 8) for _ in edges]
        covered = [0] * size
        charged = [0] * size
        used_memory = [0] * size
        matching = [True] * size
        savings = [0] * size
        best_matching = [0] * size
        for s in range(1, size):
            bit = s & -s
            i = bit.bit_length() - 1
            t = s ^ bit
            u, v = edges[i]
            mask = (1 << u) | (1 << v)
            covered[s] = covered[t] | mask
            charged[s] = charged[t] + costs[i]
            used_memory[s] = used_memory[t] + memory[i]
            matching[s] = matching[t] and not (covered[t] & mask)
            savings[s] = sum(solo[j] for j in range(n)
                             if covered[s] >> j & 1) - charged[s]
            best_matching[s] = savings[s] if matching[s] else 0
        best_any = savings.copy()
        # Downward subset maxima: every resident graph gets its exact optimum.
        for i in range(len(edges)):
            bit = 1 << i
            for s in range(size):
                if s & bit:
                    best_any[s] = max(best_any[s], best_any[s ^ bit])
                    best_matching[s] = max(best_matching[s], best_matching[s ^ bit])
        assert best_any == best_matching
        count += size
        # A nonnegative additive budget is downward closed in edge coordinates.
        for budget in range(sum(memory) + 1):
            a = max(savings[s] for s in range(size)
                    if used_memory[s] <= budget)
            b = max(savings[s] for s in range(size)
                    if matching[s] and used_memory[s] <= budget)
            assert a == b
            budget_count += 1
    # The domination hypothesis really matters.
    relaxed_star_saving = 3 * 2 - 2 * 1
    relaxed_matching_saving = 2 * 2 - 1
    assert relaxed_star_saving > relaxed_matching_saving
    # An extra memory constraint cannot be silently discarded.
    weighted_edges = [(0, 1, 5, 2), (2, 3, 4, 1)]
    unconstrained = sum(e[2] for e in weighted_edges)
    budget_one = max(e[2] for e in weighted_edges if e[3] <= 1)
    assert (unconstrained, budget_one) == (9, 4)
    return {"all_graphs_and_cost_ledgers": count,
            "downward_closed_additive_budget_cases": budget_count,
            "domination_omission_counterexample": [relaxed_star_saving,
                                                    relaxed_matching_saving],
            "budget_omission_counterexample": [unconstrained, budget_one]}


def cascade(value, m, stages):
    B = 1 << m
    p = B - 1
    bit_length = max(1, value.bit_length())
    chunks = (bit_length + m - 1) // m
    states = [0] * stages
    quotient = 0
    for index in reversed(range(chunks)):
        a = (value >> (index * m)) & (B - 1)
        for stage in range(stages):
            r = states[stage]
            total = r + a
            correction = int(total >= p)
            a = r + correction
            states[stage] = total - correction * p
        quotient = quotient * B + a
    residual = sum(r * p**j for j, r in enumerate(states))
    assert divmod(value, p**stages) == (quotient, residual)
    volume = stages * chunks * m
    return quotient, residual, volume


def conversion_controls():
    rng = random.Random(20261017)
    cases = 0
    rows = []
    for m in range(2, 8):
        for d in range(1, 6):
            Q = ((1 << m) - 1)**d
            for L in (2, 3, 4, 7, 8, 16, 32):
                limit = Q**L
                for value in (0, 1, Q-1, limit-1, rng.randrange(limit)):
                    stats = []
                    def split(x, ell):
                        if ell == 1:
                            assert 0 <= x < Q
                            return [x]
                        k = ell // 2
                        high, low, volume = cascade(x, m, d*k)
                        stats.append((ell, x.bit_length(), d*k, volume))
                        return split(low, k) + split(high, ell-k)
                    digits = split(value, L)
                    assert len(digits) == L
                    assert all(0 <= z < Q for z in digits)
                    assert sum(z * Q**i for i, z in enumerate(digits)) == value
                    def reconstruct(ds):
                        if len(ds) == 1:
                            return ds[0]
                        k = len(ds)//2
                        return reconstruct(ds[:k]) + Q**k * reconstruct(ds[k:])
                    assert reconstruct(digits) == value
                    cases += 1
                    if value == limit-1:
                        N = value.bit_length()
                        rows.append({"m":m,"d":d,"L":L,"N":N,
                                     "root_stages":stats[0][2],
                                     "root_volume":stats[0][3],
                                     "total_volume":sum(s[3] for s in stats),
                                     "root_ratio_N2_over_m":stats[0][3]*m/(N*N),
                                     "total_ratio_N2_over_m":sum(s[3] for s in stats)*m/(N*N)})
    return {"exact_balanced_conversion_and_reconstruction_cases":cases,
            "maximal_capacity_cost_cases":len(rows),
            "root_ratio_range":[min(r["root_ratio_N2_over_m"] for r in rows),
                                max(r["root_ratio_N2_over_m"] for r in rows)],
            "total_ratio_range":[min(r["total_ratio_N2_over_m"] for r in rows),
                                 max(r["total_ratio_N2_over_m"] for r in rows)],
            "rows":rows}


if __name__ == "__main__":
    result = {"status":"PASS", "pair":pair_controls(),
              "balanced_conversion":conversion_controls(),
              "execution_scope":"Only this fresh independent file was executed; Python arithmetic is an exactness oracle, not a bit-complexity timing benchmark."}
    path = Path(__file__).with_name("FRESH_RESULTS.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status":result["status"], "pair":result["pair"],
                      "balanced_conversion":{k:v for k,v in result["balanced_conversion"].items() if k != "rows"}}, indent=2))
