"""Tiny exact-integer audit, independent of every uploaded implementation.

Run: python verify_fixed_pair_kernels.py
Only Python's standard library is used. These are circular convolutions;
the script proves no asymptotic novelty and measures no production speed.
"""
from __future__ import annotations

import json
import random


def circular(a, b):
    n = len(a)
    assert len(b) == n
    return [sum(a[i] * b[(j - i) % n] for i in range(n)) for j in range(n)]


def product(signals, n):
    out = [1] + [0] * (n - 1)
    for signal in signals:
        out = circular(out, signal)
    return out


def transform(x, gain, shift, edits):
    n = len(x)
    out = [gain * x[(j - shift) % n] for j in range(n)]
    for position, delta in edits.items():
        out[position % n] += delta
    return out


def sparse_convolve(edits, kernel):
    n = len(kernel)
    return [sum(delta * kernel[(j - position) % n]
                for position, delta in edits.items()) for j in range(n)]


def combine(kernel, gain, shift, edits, complement):
    """Fresh result, so a fork cannot mutate any parent kernel."""
    n = len(kernel)
    return [gain * kernel[(j - shift) % n] + value
            for j, value in enumerate(sparse_convolve(edits, complement))]


def initialize(a, b, rest):
    n = len(a)
    r = product(rest, n)
    u = circular(b, r)  # Excludes editable a.
    v = circular(a, r)  # Excludes editable b.
    y = circular(a, u)
    return r, u, v, y


def revise_pair(state, a_change, b_change):
    """Two sequential edits, using updated v in the second y update.

    Each change is (gain, circular shift, sparse additive residual).
    r never changes; u/v/y are independently allocated to preserve forks.
    """
    r, u, v, y = state
    ga, sa, da = a_change
    gb, sb, db = b_change
    y_after_a = combine(y, ga, sa, da, u)
    v_after_a = combine(v, ga, sa, da, r)
    y_after_b = combine(y_after_a, gb, sb, db, v_after_a)
    u_after_b = combine(u, gb, sb, db, r)
    return r, u_after_b, v_after_a, y_after_b


def explicit_cross_term(state, a_change, b_change):
    r, u, v, y = state
    ga, sa, da = a_change
    gb, sb, db = b_change
    n = len(r)
    cross = {}
    for pa, va in da.items():
        for pb, vb in db.items():
            p = (pa + pb) % n
            cross[p] = cross.get(p, 0) + va * vb
    first = combine(y, ga * gb, sa + sb, {}, r)
    second = sparse_convolve(da, transform(u, gb, sb, {}))
    third = sparse_convolve(db, transform(v, ga, sa, {}))
    fourth = sparse_convolve(cross, r)
    return [sum(parts) for parts in zip(first, second, third, fourth)]


def random_change(rng, n):
    edits = {}
    for _ in range(rng.randrange(5)):
        p = rng.randrange(n)
        edits[p] = edits.get(p, 0) + rng.randrange(-3, 4)
    edits = {p: delta for p, delta in edits.items() if delta}
    return rng.randrange(-2, 3), rng.randrange(-3 * n, 3 * n + 1), edits


def test():
    rng = random.Random(20261008)
    independent_cases = 0
    stream_steps = 0
    for n in range(1, 13):
        for trial in range(60):
            signals = [[rng.randrange(-3, 4) for _ in range(n)]
                       for _ in range(rng.randrange(2, 7))]
            if trial % 10 == 0:
                signals[0] = [0] * n
            a, b, *rest = signals
            state = initialize(a, b, rest)
            original = tuple(tuple(v) for v in state)
            ca, cb = random_change(rng, n), random_change(rng, n)
            updated = revise_pair(state, ca, cb)
            expected = initialize(transform(a, *ca), transform(b, *cb), rest)
            assert updated == expected, (n, trial, "fork")
            assert updated[-1] == explicit_cross_term(state, ca, cb)
            assert tuple(tuple(v) for v in state) == original, "parent mutated"
            assert updated[0] is state[0], "constant complement not shared"
            independent_cases += 1

            # Accumulating stream, plus a sibling branch at every step.
            for step in range(5):
                ca, cb = random_change(rng, n), random_change(rng, n)
                before = tuple(tuple(v) for v in state)
                sibling = revise_pair(state, (1, 0, {}), cb)
                sibling_expected = initialize(a, transform(b, *cb), rest)
                assert sibling == sibling_expected, (n, trial, step, "sibling")
                assert tuple(tuple(v) for v in state) == before
                state = revise_pair(state, ca, cb)
                a, b = transform(a, *ca), transform(b, *cb)
                assert state == initialize(a, b, rest), (n, trial, step, "stream")
                stream_steps += 1

    # Omission of the bilinear term has a visible, exact counterexample.
    state = initialize([1, 0, 0, 0], [1, 0, 0, 0], [])
    change = (1, 0, {1: 1})
    exact = revise_pair(state, change, change)[-1]
    without_cross_term = [1, 2, 0, 0]
    assert exact == [1, 2, 1, 0] and exact != without_cross_term

    return {
        "arithmetic": "unbounded Python integers, no FFT or floating point",
        "periods": list(range(1, 13)),
        "independent_fork_cases": independent_cases,
        "accumulating_stream_steps": stream_steps,
        "sibling_fork_checks": stream_steps,
        "includes": ["negative gains", "zero gains", "circular shifts",
                     "zero factors", "support collisions", "immutable parents",
                     "empty fixed complement", "explicit cross-term comparison"],
        "cross_term_counterexample": {
            "correct": exact, "omitting_cross_term": without_cross_term
        },
        "passed": True,
        "scope": "finite exact tests of derived identity; no production performance claim"
    }


if __name__ == "__main__":
    print(json.dumps(test(), indent=2))
