#!/usr/bin/env python3
"""Fresh exact finite controls for the ALG-071 heterogeneous pair theorem.
Only Python standard library. No historical module is read, imported, or run.
"""
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import random
import time

HERE = Path(__file__).resolve().parent
COUNTS = {"exhaustive_abstract_instances": 0, "all_edge_sets_checked": 0,
          "individual_deletion_checks": 0, "complete_pruning_checks": 0,
          "unconstrained_matching_oracle_comparisons": 0,
          "bin_set_instances": 0, "weighted_bin_instances": 0,
          "budget_instances": 0, "atom_union_instances": 0,
          "constrained_matching_oracle_comparisons": 0,
          "intersection_identities_checked": 0}


def edge_set_data(s, edges, mask):
    deg = [0] * len(s)
    bill = 0
    for i, (u, v, c) in enumerate(edges):
        if mask >> i & 1:
            deg[u] += 1
            deg[v] += 1
            bill += c
    bill += sum(x for v, x in enumerate(s) if not deg[v])
    return bill, deg


def matching_oracle(s, edges):
    """Vertex recursion independent of the edge-set pruning algorithm."""
    incident = [[] for _ in s]
    for u, v, c in edges:
        incident[u].append((v, s[u] + s[v] - c))
        incident[v].append((u, s[u] + s[v] - c))

    @lru_cache(None)
    def value(remaining):
        if not remaining:
            return 0
        bit = remaining & -remaining
        u = bit.bit_length() - 1
        rest = remaining ^ bit
        ans = value(rest)
        for v, w in incident[u]:
            if rest >> v & 1:
                ans = max(ans, w + value(rest ^ (1 << v)))
        return ans
    return sum(s) - value((1 << len(s)) - 1)


def matching_masks(n, edges):
    """Enumerate matchings by vertex recursion, not all edge subsets."""
    incident = [[] for _ in range(n)]
    for i, (u, v, _) in enumerate(edges):
        incident[u].append((v, i))
        incident[v].append((u, i))

    def walk(remaining, chosen):
        if not remaining:
            yield chosen
            return
        bit = remaining & -remaining
        u = bit.bit_length() - 1
        rest = remaining ^ bit
        yield from walk(rest, chosen)
        for v, i in incident[u]:
            if rest >> v & 1:
                yield from walk(rest ^ (1 << v), chosen | (1 << i))
    return walk((1 << n) - 1, 0)


def verify(s, edges, feasible=lambda mask: True, constrained=False,
           all_deletions=False, every_pruning=False):
    assert all(c >= max(s[u], s[v]) for u, v, c in edges)
    values = []
    degrees = []
    optimum = None
    for mask in range(1 << len(edges)):
        cost, deg = edge_set_data(s, edges, mask)
        values.append(cost)
        degrees.append(deg)
        COUNTS["all_edge_sets_checked"] += 1
        if feasible(mask):
            optimum = cost if optimum is None else min(optimum, cost)
    for mask, deg in enumerate(degrees):
        if not feasible(mask):
            continue
        if all_deletions:
            for i, (u, v, _) in enumerate(edges):
                if mask >> i & 1 and (deg[u] >= 2 or deg[v] >= 2):
                    smaller = mask ^ (1 << i)
                    assert feasible(smaller), ("not downward closed", mask, smaller)
                    assert values[smaller] <= values[mask]
                    COUNTS["individual_deletion_checks"] += 1
        if every_pruning:
            current = mask
            while max(degrees[current], default=0) > 1:
                for i, (u, v, _) in enumerate(edges):
                    if current >> i & 1 and (degrees[current][u] >= 2 or degrees[current][v] >= 2):
                        smaller = current ^ (1 << i)
                        assert feasible(smaller)
                        assert values[smaller] <= values[current]
                        current = smaller
                        break
            assert values[current] <= values[mask]
            assert feasible(current)
            assert current & mask == current
            COUNTS["complete_pruning_checks"] += 1
    if constrained:
        oracle = min(values[m] for m in matching_masks(len(s), edges) if feasible(m))
        COUNTS["constrained_matching_oracle_comparisons"] += 1
    else:
        oracle = matching_oracle(s, edges)
        COUNTS["unconstrained_matching_oracle_comparisons"] += 1
    assert optimum == oracle, (s, edges, optimum, oracle)
    return optimum


def exhaustive_abstract():
    # Every labelled graph for n<=4; solo prices 0,1,2; each present edge
    # costs max(endpoint prices) or that value plus one.
    for n in range(1, 5):
        pairs = list(combinations(range(n), 2))
        for s in product(range(3), repeat=n):
            for shape in product((-1, 0, 1), repeat=len(pairs)):
                edges = [(u, v, max(s[u], s[v]) + d)
                         for (u, v), d in zip(pairs, shape) if d >= 0]
                verify(s, edges, all_deletions=True, every_pruning=True)
                COUNTS["exhaustive_abstract_instances"] += 1


def random_bin_instances(rng):
    for weighted, count in ((False, 600), (True, 200)):
        for _ in range(count):
            n = rng.randrange(1, 9)
            q = [rng.randrange(256) for _ in range(n)]
            bw = [rng.randrange(5) if weighted else 1 for _ in range(8)]
            measure = lambda mask: sum(bw[b] for b in range(8) if mask >> b & 1)
            lam = rng.randrange(5)
            s = [lam * measure(mask) for mask in q]
            pairs = list(combinations(range(n), 2))
            rng.shuffle(pairs)
            pairs = pairs[:rng.randrange(min(12, len(pairs)) + 1)]
            edges = []
            for u, v in pairs:
                h = rng.randrange(7)
                c = lam * measure(q[u] | q[v]) + h
                assert s[u] + s[v] - c == lam * measure(q[u] & q[v]) - h
                COUNTS["intersection_identities_checked"] += 1
                edges.append((u, v, c))
            opt = verify(s, edges, every_pruning=True)
            output = sum(mask.bit_count() for mask in q)
            assert opt + output == min(edge_set_data(s, edges, m)[0] + output
                                       for m in range(1 << len(edges)))
            COUNTS["weighted_bin_instances" if weighted else "bin_set_instances"] += 1


def memory_instances(rng):
    for atoms in (False, True):
        for _ in range(250):
            n = rng.randrange(2, 8)
            s = [rng.randrange(8) for _ in range(n)]
            pairs = list(combinations(range(n), 2))
            rng.shuffle(pairs)
            pairs = pairs[:rng.randrange(min(10, len(pairs)) + 1)]
            edges = [(u, v, max(s[u], s[v]) + rng.randrange(5)) for u, v in pairs]
            base = rng.randrange(15)
            if atoms:
                dependencies = [rng.randrange(256) for _ in edges]
                sizes = [rng.randrange(1, 6) for _ in range(8)]
                headers = [rng.randrange(3) for _ in edges]
                def memory(mask):
                    union = 0
                    cost = base
                    for i in range(len(edges)):
                        if mask >> i & 1:
                            union |= dependencies[i]
                            cost += headers[i]
                    return cost + sum(sizes[j] for j in range(8) if union >> j & 1)
                cap = base + rng.randrange(sum(sizes) + sum(headers) + 1)
            else:
                charges = [rng.randrange(1, 10) for _ in edges]
                def memory(mask):
                    return base + sum(c for i, c in enumerate(charges) if mask >> i & 1)
                cap = base + rng.randrange(sum(charges) + 1)
            feasible = lambda mask: memory(mask) <= cap
            verify(s, edges, feasible=feasible, constrained=True,
                   all_deletions=True, every_pruning=True)
            COUNTS["atom_union_instances" if atoms else "budget_instances"] += 1


def brute(s, edges, predicate=lambda m: True):
    return min(edge_set_data(s, edges, m)[0]
               for m in range(1 << len(edges)) if predicate(m))


def controls():
    s = [1, 1, 1]
    edges = [(0, 1, 0), (0, 2, 0)]
    assert brute(s, edges) == 0 and matching_oracle(s, edges) == 1
    dominance = {"all_sets_cost": 0, "best_matching_cost": 1}

    # Same-bin third consumer can be served by containment but is not an endpoint.
    endpoints_cost = matching_oracle([1, 1, 1], [(0, 1, 1)])
    containment_cost = min(3, 1)  # the only candidate covers all three consumers
    assert endpoints_cost == 2 and containment_cost == 1

    # Budgeted optimum with two disjoint pairs of saving 5 and 6.
    s = [5, 5, 6, 6]
    edges = [(0, 1, 5), (2, 3, 6)]
    feasible = lambda m: 6 * m.bit_count() <= 6
    budget_cost = verify(s, edges, feasible=feasible, constrained=True)
    assert sum(s) - matching_oracle(s, edges) == 11
    assert sum(s) - budget_cost == 6

    # Positive cold construction removes a seemingly profitable pair.
    assert matching_oracle([2, 2], [(0, 1, 5)]) == 4
    assert matching_oracle([2, 2], [(0, 1, 2)]) == 2

    # A non-downward-closed domain may contain no matching at all.
    edges = [(0, 1, 1), (1, 2, 1)]
    allowed = lambda m: m == 3
    assert brute([1, 1, 1], edges, allowed) == 2
    assert not any(allowed(m) for m in matching_masks(3, edges))

    # The old homogeneous non-submodularity witness remains unchanged.
    s = [2, 2, 2, 2]
    edges = [(0, 1, 3), (0, 2, 3), (1, 3, 3)]
    savings = {}
    for name, mask in (("A", 1), ("AB", 3), ("AC", 5), ("ABC", 7)):
        used = [e for i, e in enumerate(edges) if mask >> i & 1]
        savings[name] = sum(s) - verify(s, used)
    assert savings == {"A": 1, "AB": 1, "AC": 1, "ABC": 2}

    # Knapsack embedding in the abstract cost ledger.
    profits, sizes, cap = [3, 5, 8, 9], [2, 4, 5, 7], 10
    s = [p for p in profits for _ in range(2)]
    edges = [(2*i, 2*i+1, p) for i, p in enumerate(profits)]
    feasible = lambda m: sum(a for i, a in enumerate(sizes) if m >> i & 1) <= cap
    cost = verify(s, edges, feasible=feasible, constrained=True)
    knapsack = max(sum(p for i, p in enumerate(profits) if m >> i & 1)
                   for m in range(1 << len(profits)) if feasible(m))
    assert sum(s) - cost == knapsack == 13
    return {"dominance_removed": dominance,
            "undeclared_containment": {"endpoint_model_cost": endpoints_cost,
                                       "actual_containment_cost": containment_cost},
            "budget_erased": {"unconstrained_saving": 11, "feasible_saving": 6},
            "cold_activation_omitted": {"true_saving": 0, "false_saving": 2},
            "downward_closure_removed": {"feasible_matching_exists": False},
            "preserved_non_submodularity": savings,
            "abstract_knapsack_embedding_optimum": knapsack}


def main():
    started = time.monotonic()
    rng = random.Random(71001758)
    exhaustive_abstract()
    random_bin_instances(rng)
    memory_instances(rng)
    negative = controls()
    result = {"status": "PASS", "arithmetic": "exact Python integers",
              "fresh_code_only": True, "historical_programs_executed": False,
              "seed": 71001758, "counts": COUNTS, "controls": negative,
              "elapsed_seconds": round(time.monotonic() - started, 3),
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE / "FRESH_RESULTS.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
