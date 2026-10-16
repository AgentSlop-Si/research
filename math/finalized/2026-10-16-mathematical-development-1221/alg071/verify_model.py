"""Self-authored exhaustive finite controls for ALG071 model propositions.

This imports no owner-supplied code and does not test numerical Fourier code.
"""
from itertools import combinations, product
import json


def subsets(items):
    items = tuple(items)
    for mask in range(1 << len(items)):
        yield tuple(items[j] for j in range(len(items)) if mask >> j & 1)


def union_size(groups):
    return len(set().union(*(set(g) for g in groups))) if groups else 0


def savings(groups, core=1, allocation_per_cell=0):
    """Synchronous source-granular optimum: use any subset of resident groups."""
    return max((core + 1) * union_size(t) - sum(
        (1 + allocation_per_cell) * (core + len(g)) for g in t
    ) for t in subsets(groups))


def matching_number(edges):
    return max(len(t) for t in subsets(edges)
               if union_size(t) == 2 * len(t))


def main():
    a, b, c = (0, 1), (0, 2), (1, 3)
    witness = {"a": savings((a,)), "ab": savings((a, b)),
               "ac": savings((a, c)), "abc": savings((a, b, c))}
    assert witness == {"a": 1, "ab": 1, "ac": 1, "abc": 2}
    assert witness["ab"] + witness["ac"] < witness["a"] + witness["abc"]

    checked_graphs = 0
    all_edges = tuple(combinations(range(5), 2))
    for graph in subsets(all_edges):
        nu = matching_number(graph)
        for core in (1, 2, 3):
            assert savings(graph, core=core) == core * nu
            checked_graphs += 1

    triples = tuple(product(range(2), range(2, 4), range(4, 6)))
    checked_3dm = 0
    for family in subsets(triples):
        allowed = [t for t in subsets(family) if len(t) <= 2]
        value = max(5 * union_size(t) - 14 * len(t) for t in allowed)
        has_perfect = any(len(t) == 2 and union_size(t) == 6 for t in allowed)
        assert (value == 2) == has_perfect
        checked_3dm += 1

    return {
        "scope": "self-authored combinatorial model controls only; no supplied code executed",
        "non_submodularity_witness": witness,
        "homogeneous_pair_model_cases": checked_graphs,
        "tripartite_exact_cover_families": checked_3dm,
        "all_assertions_passed": True,
    }


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, sort_keys=True))
