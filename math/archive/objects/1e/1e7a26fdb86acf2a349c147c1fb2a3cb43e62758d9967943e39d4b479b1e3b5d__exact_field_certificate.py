#!/usr/bin/env python3
"""Exact finite-field certificate for the unequal-block Green identity.

Uses the NTT prime 998244353.  Tested N must satisfy 2N | (p-1), so the
parity-twist root exists.  All operations are exact modulo p.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
import random

P = 998244353
GENERATOR = 3


@dataclass(frozen=True)
class State:
    a: int
    beta: int


def balanced_partition(n: int, blocks: int):
    q, r = divmod(n, blocks)
    lengths = [q + 1] * r + [q] * (blocks - r)
    starts = [0]
    for ell in lengths[:-1]:
        starts.append(starts[-1] + ell)
    ends = [s + ell for s, ell in zip(starts, lengths)]
    return starts, lengths, ends


def root_of_order(order: int) -> int:
    if (P - 1) % order:
        raise ValueError(f"order {order} does not divide P-1")
    return pow(GENERATOR, (P - 1) // order, P)


def tri(t: int) -> int:
    return t * (t - 1) // 2


def poly_mul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] = (out[i + j] + x * y) % P
    return out


def recurrence_setup(nodes):
    q = [1]
    for lam in nodes:
        q = poly_mul(q, [1, -lam % P])
    b = len(nodes)
    inv = [0] * b
    inv[0] = pow(q[0], P - 2, P)
    for n in range(1, b):
        total = 0
        for j in range(1, min(n, b) + 1):
            total = (total + q[j] * inv[n - j]) % P
        inv[n] = (-total * inv[0]) % P
    return q, inv


def exp_sequence(nodes, weights, length):
    b = len(nodes)
    seq = [sum(weights[j] * pow(nodes[j], k, P) for j in range(b)) % P
           for k in range(min(b, length))]
    if length <= b:
        return seq
    q, inv = recurrence_setup(nodes)
    cursor = b
    while cursor < length:
        take = min(b, length - cursor)
        past = seq[cursor - b: cursor]
        conv = poly_mul(past, q)
        rhs = [(-conv[b + t]) % P for t in range(take)]
        block = poly_mul(rhs, inv)[:take]
        seq.extend(block)
        cursor += take
    return seq


def run_case(n: int, blocks: int, seed: int) -> dict:
    if (P - 1) % (2 * n):
        raise ValueError("2N must divide P-1")
    rng = random.Random(seed)
    units = [a for a in range(1, n) if math.gcd(a, n) == 1]
    state = State(rng.choice(units), rng.randrange(n))
    zeta = root_of_order(n)
    eta = root_of_order(2 * n)
    starts, lengths, ends = balanced_partition(n, blocks)
    x = [rng.randrange(P) for _ in range(n)]

    summaries = []
    phases = []
    for s, ell in zip(starts, lengths):
        ph = []
        total = 0
        for t in range(ell):
            val = pow(zeta, (state.a * tri(t) + (state.a * s + state.beta) * t) % n, P)
            if n & 1:
                val = val * pow(eta, t, P) % P
            ph.append(val)
            total = (total + val * x[s + t]) % P
        phases.append(ph)
        summaries.append(total)

    y = [0] * n
    for b, (s, ell) in enumerate(zip(starts, lengths)):
        for t in range(ell):
            y[s + t] = pow(phases[b][t], P - 2, P) * summaries[b] % P
    direct = [sum(y[j] * pow(zeta, (-k * j) % n, P) for j in range(n)) % P
              for k in range(n)]

    nodes = [pow(zeta, (-s) % n, P) for s in starts]
    end_weights = [0] * blocks
    h = n & 1
    for b, (s, ell) in enumerate(zip(starts, lengths)):
        coeff = pow(zeta, (-state.a * tri(ell) - state.a * s * ell - state.beta * ell) % n, P)
        if h:
            coeff = coeff * pow(eta, (-ell) % (2 * n), P) % P
        end_weights[(b + 1) % blocks] = coeff * summaries[b] % P
    dseq = exp_sequence(nodes, summaries, n)
    eseq = exp_sequence(nodes, end_weights, n)
    forcing = [(dseq[k] - eseq[k]) % P for k in range(n)]

    indices = [(state.a * j) % n for j in range(n)]
    gauge = []
    for j in range(n):
        val = pow(zeta, (state.a * tri(j) + state.beta * j) % n, P)
        if h:
            val = val * pow(eta, j, P) % P
        gauge.append(val)
    terms = [forcing[indices[j]] * pow(gauge[j], P - 2, P) % P for j in range(n)]
    inv2 = pow(2, P - 2, P)
    seed_value = sum(terms) % P * inv2 % P
    prefix = 0
    decoded = [0] * n
    for j in range(n):
        decoded[indices[j]] = gauge[j] * (seed_value - prefix) % P
        prefix = (prefix + terms[j]) % P

    if decoded != direct:
        raise AssertionError((n, blocks, state))
    return {"n": n, "blocks": blocks, "a": state.a, "beta": state.beta, "passed": True}


def run_suite():
    cases = []
    for n in [7, 14, 17, 28, 34, 56, 68, 112, 119, 136]:
        if (P - 1) % (2 * n):
            continue
        for blocks in [3, 4, 5, 7]:
            if blocks <= n and 2 * (((n + blocks - 1) // blocks) - 1) < n:
                cases.append(run_case(n, blocks, 1000 + 17 * n + blocks))
    return cases


if __name__ == "__main__":
    rows = run_suite()
    print(f"exact finite-field cases: {len(rows)}")
    for row in rows:
        print(row)
