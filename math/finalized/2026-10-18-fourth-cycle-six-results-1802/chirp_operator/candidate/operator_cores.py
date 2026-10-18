#!/usr/bin/env python3
"""Exact finite-field reference: paid interleaved chirp-convolution MPO.

The prime and a primitive 2**n-th root are supplied, not discovered.
No predecessor implementation is imported. Counters count ideal field and
scalar-slot operations, not Python instructions or bit complexity.
"""


def order(n):
    out = []
    lo, hi = 0, n - 1
    while lo <= hi:
        out.append(lo)
        lo += 1
        if lo <= hi:
            out.append(hi)
            hi -= 1
    return out


def profile(n):
    return [1] + [2 ** (min((k + 1) // 2, n - k) + 1) - 1
                  for k in range(1, n)] + [1]


def prepare(n, omega, prime):
    if not isinstance(n, int) or n < 1:
        raise ValueError('n must be positive')
    N = 1 << n
    bill = {'multiplications': 0, 'root_guard_multiplications': 0}

    def mul(a, b):
        bill['multiplications'] += 1
        return a * b % prime

    def power(a, e):
        z = 1
        while e:
            if e & 1:
                z = mul(z, a)
            a = mul(a, a)
            e >>= 1
        return z

    if power(omega, N) != 1 or power(omega, N // 2) == 1:
        raise ValueError('root is not primitive')
    bill['root_guard_multiplications'] = bill['multiplications']
    inv = power(omega, N - 1)
    neg, pos, gp = [inv], [omega], [inv]
    for p in range(n - 1):
        neg.append(mul(neg[-1], neg[-1]))
        pos.append(mul(pos[-1], pos[-1]))
    for p in range(n - 1):
        gp.append(mul(mul(gp[-1], gp[-1]), neg[2 * p] if 2 * p < n else 1))
    gm = [mul(gp[p], pos[p]) for p in range(n)]
    pi = order(n)
    bridge = next(k for k in range(1, n + 1) if (k + 1) // 2 >= n - k)
    ranks = profile(n)
    cores = []
    table_slots = 0
    for k, p in enumerate(pi, 1):
        core = []
        before_radius = (ranks[k - 1] - 1) // 2
        after_radius = (ranks[k] - 1) // 2
        if k < bridge:
            # Signed powers of omega^(-2^p), prepared by two progressions.
            phases = {0: 1}
            zn = zp = 1
            for a in range(1, before_radius + 1):
                zn, zp = mul(zn, neg[p]), mul(zp, pos[p])
                phases[a], phases[-a] = zn, zp
            for a in range(-before_radius, before_radius + 1):
                for l in (0, 1):
                    for x in (0, 1):
                        delta = l - x
                        val = 1 if delta == 0 else mul(
                            gp[p] if delta == 1 else gm[p], phases[delta * a])
                        nxt = a + delta * (1 << p) if k % 2 else a
                        core.append((a, l, x, nxt, val))
        elif k == bridge:
            j = k // 2  # Low bits processed before this stage.
            A = 1 << j
            M = 1 << (n - k)
            L = 2 * M
            # T[a,c] = g(2^j c) omega^(-a 2^j c), signed a,c.
            # No individual coefficient exponentiation or root table is used.
            table = {}
            Gp = Gm = zn = zp = 1
            rp, rm = gp[j], gm[j]
            step = neg[2 * j] if 2 * j < n else 1
            for c in range(L):
                choices = [(0, 1, 1, 1)] if c == 0 else [
                    (c, Gp, zn, zp), (-c, Gm, zp, zn)]
                for signed_c, G, z, zi in choices:
                    table[0, signed_c] = G
                    plus = minus = G
                    for a in range(1, A):
                        plus, minus = mul(plus, z), mul(minus, zi)
                        table[a, signed_c] = plus
                        table[-a, signed_c] = minus
                Gp, Gm = mul(Gp, rp), mul(Gm, rm)
                rp, rm = mul(rp, step), mul(rm, step)
                zn, zp = mul(zn, neg[j]), mul(zp, pos[j])
            table_slots = len(table)
            j_after = (k + 1) // 2
            for a in range(-before_radius, before_radius + 1):
                for l in (0, 1):
                    for x in (0, 1):
                        for d in range(-after_radius, after_radius + 1):
                            c = ((l - x) << (p - j)) + (d << (j_after - j))
                            core.append((a, l, x, d, table[a, c]))
        else:
            M = 1 << (n - k)
            for d in range(-after_radius, after_radius + 1):
                for l in (0, 1):
                    for x in (0, 1):
                        old = (l - x) + 2 * d if k % 2 else (l - x) * M + d
                        core.append((old, l, x, d, 1))
        cores.append(core)
    bill.update(n=n, bridge=bridge, ranks=ranks,
                width=max(ranks), scalar_core_slots=sum(map(len, cores)),
                bridge_table_slots=table_slots, constant_slots=4 * n,
                nonzeros_by_stage=list(map(len, cores)))
    return cores, bill


def evaluate(cores, n, ell, source, prime):
    """Full sparse contraction, used only as a test, not an entry-speed claim."""
    states = {0: 1}
    for p, core in zip(order(n), cores):
        nxt = {}
        lb, sb = (ell >> p) & 1, (source >> p) & 1
        for a, l, s, b, w in core:
            if l == lb and s == sb and a in states:
                nxt[b] = (nxt.get(b, 0) + states[a] * w) % prime
        states = nxt
    return states.get(0, 0)


def apply_dense(cores, n, x, prime, selected=None, observe=None):
    """Literal left-to-right MPO/dense-vector contraction, with exact ledger.

    Physical input and output vectors use ordinary integer order. `selected`
    contains requested ordinary output indices; all frontiers are materialized.
    """
    N = 1 << n
    if len(x) != N:
        raise ValueError('input length mismatch')
    ranks = profile(n)
    permutation = [0]
    for p in order(n):
        permutation += [v + (1 << p) for v in permutation]
    current = [x[t] for t in permutation]
    bill = {'multiplications': 0, 'additions': 0,
            'zero_initializations': 0, 'stage_slots': [],
            'generic_feasible_stage_slots': [], 'nonzero_stage_slots': [],
            'peak_two_frontier_slots': N,
            'permutation_slots': N, 'permutation_build_writes': 2 * N - 1,
            'input_reads': N, 'input_route_writes': N}
    for k, core in enumerate(cores, 1):
        old_r, new_r = ranks[k - 1], ranks[k]
        old_radius, new_radius = (old_r - 1) // 2, (new_r - 1) // 2
        P, S = 1 << (k - 1), 1 << (n - k)
        out = [0] * (N * new_r)
        bill['zero_initializations'] += len(out)
        bill['peak_two_frontier_slots'] = max(
            bill['peak_two_frontier_slots'], len(current) + len(out))
        for a, lb, sb, b, w in core:
            ai, bi = a + old_radius, b + new_radius
            for lp in range(P):
                oldbase = lp * 2 * S * old_r + sb * old_r + ai
                newbase = (lp + lb * P) * S * new_r + bi
                for sr in range(S):
                    oi, ni = oldbase + 2 * sr * old_r, newbase + sr * new_r
                    out[ni] = (out[ni] + current[oi] * w) % prime
        updates = (N // 2) * len(core)
        bill['multiplications'] += updates
        bill['additions'] += updates
        bill['stage_slots'].append(len(out))
        bill['generic_feasible_stage_slots'].append(
            N * (1 << min((k + 1) // 2, n - k)))
        bill['nonzero_stage_slots'].append(sum(v != 0 for v in out))
        if observe is not None:
            observe(k, out)
        current = out
    ordinary = [0] * N
    for code, physical in enumerate(permutation):
        ordinary[physical] = current[code]
    chosen = list(range(N)) if selected is None else list(selected)
    result = [ordinary[ell] for ell in chosen]
    bill.update(output_route_writes=N, selected_output_writes=len(result),
                selected_output_indices=chosen)
    return result, bill
