"""Exact Gaussian-rational audit of energy-pruned DIF, for N = 1, 2, 4.

This is a finite implementation audit, not an all-N proof or a speed benchmark.
All input values, twiddles, squared norms, threshold comparisons, oracle values,
and error checks are exact.  The transform has the usual negative Fourier sign
and returns unnormalized coefficients.  No floating-point arithmetic is used.

Run: python exact_small_audit.py
Results: results/exact_small_audit.json, relative to this file.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
import json
from pathlib import Path


@dataclass(frozen=True)
class GaussianRational:
    re: Fraction
    im: Fraction

    def __add__(self, other: GaussianRational) -> GaussianRational:
        return G(self.re + other.re, self.im + other.im)

    def __sub__(self, other: GaussianRational) -> GaussianRational:
        return G(self.re - other.re, self.im - other.im)

    def __mul__(self, other: GaussianRational) -> GaussianRational:
        return G(self.re * other.re - self.im * other.im,
                 self.re * other.im + self.im * other.re)

    def squared_norm(self) -> Fraction:
        return self.re * self.re + self.im * self.im

    def power(self, exponent: int) -> GaussianRational:
        if exponent < 0:
            raise ValueError("Only nonnegative powers are used")
        answer = ONE
        for _ in range(exponent):
            answer = answer * self
        return answer

    def encode(self) -> list[str]:
        return [str(self.re), str(self.im)]


def G(re=0, im=0) -> GaussianRational:
    return GaussianRational(Fraction(re), Fraction(im))


ZERO, ONE, MINUS_ONE, I, MINUS_I = G(), G(1), G(-1), G(0, 1), G(0, -1)
ROOTS = {1: ONE, 2: MINUS_ONE, 4: MINUS_I}
ALPHABET = (ZERO, ONE, MINUS_ONE, I, MINUS_I)
EPSILONS = tuple(Fraction(a, 4) for a in range(5))


def norm_squared(values: tuple | list) -> Fraction:
    return sum((z.squared_norm() for z in values), Fraction(0))


def direct_dft(values: tuple | list) -> list[GaussianRational]:
    """Independent quadratic oracle, exact over Q(i)."""
    n = len(values)
    q = ROOTS[n]
    return [sum((z * q.power((j * k) % n)
                 for j, z in enumerate(values)), ZERO)
            for k in range(n)]


def energy_pruned_dif(values: tuple | list, epsilon: Fraction):
    """Return exact raw DFT hard-thresholding, trace, and logical work counts.

    A length-m node v owns raw Fourier outputs at offset modulo stride. Its
    unitary-output subtree energy is (m/N) * sum |v_j|^2. Prune on <=, including
    at leaves. This yields raw error <= sqrt(N) * epsilon * ||values||_2.
    """
    n = len(values)
    if n not in ROOTS:
        raise ValueError("This audit supports only N = 1, 2, 4")
    if not isinstance(epsilon, Fraction) or epsilon < 0:
        raise ValueError("epsilon must be a nonnegative Fraction")
    root_energy = norm_squared(values)
    threshold = epsilon * epsilon * root_energy
    out = [ZERO] * n
    counts = Counter(output_zero_writes=n, input_norm_values=n)
    trace = []
    stack = [(tuple(values), 0, 1, 0)]
    while stack:
        v, offset, stride, depth = stack.pop()
        m = len(v)
        energy = Fraction(m, n) * norm_squared(v)
        prune = energy <= threshold
        event = dict(length=m, offset=offset, stride=stride, depth=depth,
                     energy=energy, threshold=threshold, pruned=prune,
                     tie=(energy == threshold))
        trace.append(event)
        counts["visited_nodes"] += 1
        counts["node_norm_values"] += m
        counts["threshold_comparisons"] += 1
        if prune:
            counts["pruned_nodes"] += 1
            counts["pruned_outputs"] += m
            continue
        counts[f"active_depth_{depth}"] += 1
        if m == 1:
            out[offset] = v[0]
            counts["computed_outputs"] += 1
            continue
        h = m // 2
        q = ROOTS[m]
        left = tuple(v[j] + v[j + h] for j in range(h))
        right = tuple((v[j] - v[j + h]) * q.power(j) for j in range(h))
        left_energy = Fraction(h, n) * norm_squared(left)
        right_energy = Fraction(h, n) * norm_squared(right)
        if left_energy + right_energy != energy:
            raise AssertionError("Exact child energy partition failed")
        counts["split_nodes"] += 1
        counts["split_value_volume"] += m
        counts["butterflies"] += h
        stack.append((right, offset + stride, 2 * stride, depth + 1))
        stack.append((left, offset, 2 * stride, depth + 1))
    return out, trace, counts


def audit_case(values, epsilon, summary, tie_examples):
    n = len(values)
    exact = direct_dft(values)
    out, trace, counts = energy_pruned_dif(values, epsilon)
    root_energy = norm_squared(values)
    threshold_raw_squared = n * epsilon * epsilon * root_energy
    wanted = [z if z.squared_norm() > threshold_raw_squared else ZERO
              for z in exact]
    assert out == wanted, ("hard threshold mismatch", values, epsilon)
    assert norm_squared(exact) == n * root_energy, "oracle Parseval failure"
    assert max(((a-b).squared_norm() for a, b in zip(out, exact)),
               default=Fraction(0)) <= threshold_raw_squared
    assert len(out) == n
    assert counts["pruned_outputs"] + counts["computed_outputs"] == n
    if epsilon == 0:
        assert out == exact
    if epsilon >= 1:
        assert out == [ZERO] * n
    for event in trace:
        indices = range(event["offset"], n, event["stride"])
        oracle_energy = sum((exact[k].squared_norm() for k in indices),
                            Fraction(0)) / n
        assert oracle_energy == event["energy"], "subtree energy mismatch"
        if event["pruned"]:
            for k in indices:
                assert exact[k].squared_norm() <= threshold_raw_squared
                assert out[k] == ZERO
        if event["tie"] and event["energy"] > 0:
            category = ("root" if event["depth"] == 0 else
                        "leaf" if event["length"] == 1 else "internal")
            summary["positive_tie_nodes_" + category] += 1
            if category not in tie_examples:
                tie_examples[category] = dict(
                    n=n, input=[z.encode() for z in values], epsilon=str(epsilon),
                    node={k: str(v) if isinstance(v, Fraction) else v
                          for k, v in event.items()},
                    oracle=[z.encode() for z in exact],
                    output=[z.encode() for z in out])
    depth_count = Counter(e["depth"] for e in trace if not e["pruned"])
    for depth, active in depth_count.items():
        assert active <= 2 ** depth
        if root_energy > 0 and epsilon > 0:
            assert active * epsilon * epsilon < 1
    split_volume = counts["split_value_volume"]
    log_n = n.bit_length() - 1
    if epsilon == 0:
        volume_bound = Fraction(n * log_n)
    else:
        volume_bound = sum((Fraction(n, 2 ** d) *
                            min(Fraction(2 ** d), 1 / (epsilon * epsilon))
                            for d in range(log_n)), Fraction(0))
    assert split_volume <= volume_bound
    summary["cases"] += 1
    summary["output_coordinates_checked"] += n
    summary["subtree_energy_identities_checked"] += len(trace)
    summary["child_energy_partitions_checked"] += counts["split_nodes"]
    summary["hard_threshold_cases"] += 1
    summary["max_error_bound_cases"] += 1
    summary["split_volume_bound_cases"] += 1
    summary["zero_epsilon_cases"] += int(epsilon == 0)
    summary["root_discard_cases"] += int(epsilon >= 1)


def run_audit():
    per_n = {}
    totals = Counter()
    tie_examples = {}
    for n in ROOTS:
        summary = Counter()
        for values in product(ALPHABET, repeat=n):
            for epsilon in EPSILONS:
                audit_case(values, epsilon, summary, tie_examples)
        per_n[str(n)] = dict(summary)
        totals.update(summary)

    # A non-leaf positive-energy tie at epsilon = 1/2 is deliberately included.
    # Its length-2 even child has energy 2, while root energy is 8.
    internal_tie_input = (G(2), G(1, 1), ZERO, G(-1, -1))
    focused_inputs = [
        (ONE,),
        (ONE, ZERO),
        (ONE, ZERO, ZERO, ZERO),
        (ONE, ONE, ONE, ONE),
        internal_tie_input,
        tuple(z * G(Fraction(2, 7), Fraction(3, 11))
              for z in internal_tie_input),
        (G(Fraction(1, 3), Fraction(2, 5)), G(Fraction(-2, 7)),
         G(0, Fraction(3, 13)), G(Fraction(4, 17), Fraction(-5, 19))),
    ]
    boundary_epsilons = (Fraction(0), Fraction(1, 4),
                         Fraction(1, 2) - Fraction(1, 1024),
                         Fraction(1, 2),
                         Fraction(1, 2) + Fraction(1, 1024),
                         Fraction(3, 4), Fraction(1), Fraction(3, 2))
    focused = Counter()
    for values in focused_inputs:
        for epsilon in boundary_epsilons:
            audit_case(values, epsilon, focused, tie_examples)
    totals.update(focused)
    assert set(tie_examples) == {"root", "internal", "leaf"}
    return dict(
        status="PASS",
        scope="Finite exact implementation audit; not an all-N proof or timing result",
        arithmetic="fractions.Fraction pairs for Q(i); no floating point",
        convention="raw negative-sign DFT; root q=-i at N=4",
        alphabet=[z.encode() for z in ALPHABET],
        exhaustive_epsilons=[str(e) for e in EPSILONS],
        boundary_epsilons=[str(e) for e in boundary_epsilons],
        guarantee="max_k |output_k - (F_N x)_k|^2 <= N epsilon^2 ||x||_2^2",
        exact_hard_threshold="output_k = (F_N x)_k iff its squared magnitude exceeds N epsilon^2 ||x||_2^2; otherwise zero",
        exhaustive_by_n=per_n,
        focused_boundary_cases=dict(focused),
        totals=dict(totals),
        positive_threshold_tie_examples=tie_examples,
    )


if __name__ == "__main__":
    result = run_audit()
    destination = Path(__file__).resolve().parent / "results" / "exact_small_audit.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(dict(status=result["status"], totals=result["totals"],
                          results=str(destination)), indent=2))
