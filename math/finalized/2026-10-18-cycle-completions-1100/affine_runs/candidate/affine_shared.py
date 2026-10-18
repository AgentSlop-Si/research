#!/usr/bin/env python3
"""New source-preserving affine-run branch; imports the accepted jump route.

Arithmetic-data multiplications use the inherited explicit elementary backend.
The O(N) recognition guard precedes canonical conversions and graph allocation.
No input-size integer product or packed child product is evaluated here.
"""
from dataclasses import dataclass
import hashlib
from pathlib import Path
_ACCEPTED = Path(__file__).resolve().with_name('run_shared.py')
if hashlib.sha256(_ACCEPTED.read_bytes()).hexdigest() != '3d3b6e7f0f96013cc90349d76b30aec4afd72b9f0e2b6faed861bc7d74b2480b':
    raise RuntimeError('accepted portable jump dependency hash mismatch')
import run_shared as accepted
base = accepted.base


def affine_partition(blocks):
    """Greedy disjoint numeric affine runs. Every input block is inspected."""
    runs = []
    start = 0
    while start < len(blocks):
        end = min(start+2, len(blocks))
        if end > start+1:
            slope = blocks[start+1]-blocks[start]
            while end < len(blocks) and blocks[end]-blocks[end-1] == slope:
                end += 1
        runs.append((start, end-start))
        start = end
    return runs


def certify_runs(blocks, partition, plan, E):
    out = []
    for start, length in partition:
        first = base.canonical(blocks[start], plan, E)
        if length > 1:
            second = base.canonical(blocks[start+1], plan, E)
            slope = tuple(E.add(y, -x) for x, y in zip(first, second))
        else:
            slope = (0,)*plan.rank
        last = base.canonical(blocks[start+length-1], plan, E)
        predicted = tuple(E.add(x, E.mul(length-1, y)) for x, y in zip(first, slope))
        if predicted != last:
            return None
        out.append((start, length, first, slope, last))
    return out


def merge_vectors(records, rank, E):
    records.sort(key=lambda x: x[0])
    out = []
    i = 0
    while i < len(records):
        p = records[i][0]
        v = [0]*rank
        while i < len(records) and records[i][0] == p:
            v = [E.add(a, b) for a, b in zip(v, records[i][1])]
            i += 1
        if any(v):
            out.append((p, tuple(v)))
    return out


def run_events(runs, plan, E):
    records = []
    for start, length, u, v, last in runs:
        records.extend([
            (start, u),
            (start+1, tuple(E.add(b, -a) for a, b in zip(u, v))),
            (start+length, tuple(-E.add(a, b) for a, b in zip(last, v))),
            (start+length+1, last),
        ])
    return merge_vectors(records, plan.rank, E)


def make_graph(runs, lengths, plan, E):
    raw = []
    for side, rs in enumerate(runs):
        for position, difference in run_events(rs, plan, E):
            sign, vector = accepted.signed_normalize(difference)
            raw.append((vector, side, position, sign))
    raw.sort()
    leaves, sides = [], [[], []]
    for vector, side, position, sign in raw:
        if not leaves or leaves[-1] != vector:
            leaves.append(vector)
        sides[side].append((position, len(leaves)-1, sign))
    for terms in sides:
        terms.sort()
    pairs = []
    for i, u, sa in sides[0]:
        for j, v, sb in sides[1]:
            pairs.append((min(u, v), max(u, v), i+j, sa*sb))
    pairs.sort()
    products, events = [], []
    for u, v, position, sign in pairs:
        if not products or products[-1] != (u, v):
            products.append((u, v))
        events.append((position, len(products)-1, sign))
    events.sort()
    return {'version': 2, 'order': 2, 'rank': plan.rank, 'point': plan.point,
            'block_bits': plan.block_bits, 'nodes': plan.nodes,
            'lengths': lengths, 'runs': runs, 'leaves': leaves,
            'sides': sides, 'products': products, 'events': events}


def source_rows(runs, lengths, plan, E):
    result = []
    for x, row in zip(plan.nodes, plan.rows):
        maxima = []
        for rs in runs:
            maximum = 0
            for _, _, u, _, last in rs:
                maximum = max(maximum, abs(base.evaluate(u, row, E)),
                              abs(base.evaluate(last, row, E)))
            maxima.append(maximum)
        width, bound = base.slot_width(max(lengths), *maxima, E) if all(maxima) else (0, 0)
        result.append((x, *maxima, width, bound))
    return result


def evaluate_graph(graph, plan, E):
    leaves = [tuple(base.evaluate(v, row, E) for row in plan.rows) for v in graph['leaves']]
    products = [tuple(E.mul(a, b) for a, b in zip(leaves[u], leaves[v]))
                for u, v in graph['products']]
    targets = [base.interpolate(p, plan, E) for p in products]
    return {'leaf_rows': leaves, 'product_rows': products, 'targets': targets,
            'source_rows': source_rows(graph['runs'], graph['lengths'], plan, E)}


def check_certificate(blocks, graph, execution, plan, E):
    """O(N + (R+Q)r^4+Mr^2) independent-form dense binding and checker.

    Computes second differences from local source values, rather than the
    four-event interval formula used by the graph producer.
    """
    lengths = tuple(map(len, blocks))
    if len(graph['runs']) != 2 or len(graph['sides']) != 2:
        raise ValueError('side count')
    if (graph['version'], graph['order'], graph['rank'], graph['point'],
        graph['block_bits'], graph['nodes'], graph['lengths']) != (
            2, 2, plan.rank, plan.point, plan.block_bits, plan.nodes, lengths):
        raise ValueError('header')
    expected_vectors = []
    for bs, rs in zip(blocks, graph['runs']):
        next_start = 0
        local = []
        for start, length, u, slope, last in rs:
            if start != next_start or length < 1 or start+length > len(bs):
                raise ValueError('partition')
            if len(u) != plan.rank or len(slope) != plan.rank or len(last) != plan.rank:
                raise ValueError('vector dimensions')
            if u != base.canonical(bs[start], plan, E) or last != base.canonical(bs[start+length-1], plan, E):
                raise ValueError('endpoint canonicality')
            second = base.canonical(bs[start+1], plan, E) if length > 1 else u
            if slope != tuple(E.add(y, -x) for x, y in zip(u, second)):
                raise ValueError('slope')
            if last != tuple(E.add(x, E.mul(length-1, y)) for x, y in zip(u, slope)):
                raise ValueError('canonical affine endpoint')
            numeric_slope = E.add(bs[start+1], -bs[start]) if length > 1 else 0
            expected = bs[start]
            for pos in range(start, start+length):
                if bs[pos] != expected:
                    raise ValueError('dense affine binding')
                expected = E.add(expected, numeric_slope)
            # Restriction of delta^2 to this zero-extended interval. Only
            # the four boundary positions can be nonzero; collapse overlaps.
            positions = sorted(set((start, start+1, start+length, start+length+1)))
            for pos in positions:
                values = []
                for k in (pos, pos-1, pos-2):
                    if start <= k < start+length:
                        values.append(tuple(E.add(x, E.mul(k-start, y)) for x, y in zip(u, slope)))
                    else:
                        values.append((0,)*plan.rank)
                v = tuple(E.add(E.add(a, -E.add(b, b)), c) for a, b, c in zip(*values))
                local.append((pos, v))
            next_start = start+length
        if next_start != len(bs):
            raise ValueError('partition tail')
        expected_vectors.append(merge_vectors(local, plan.rank, E))
    leaves = graph['leaves']
    if leaves != sorted(leaves) or any(x == y for x, y in zip(leaves, leaves[1:])):
        raise ValueError('leaf uniqueness')
    used = []
    for want, terms in zip(expected_vectors, graph['sides']):
        if len(want) != len(terms):
            raise ValueError('term count')
        for (position, vector), (p, leaf, sg) in zip(want, terms):
            sign, normalized = accepted.signed_normalize(vector)
            if not 0 <= leaf < len(leaves) or (p, sg) != (position, sign) or leaves[leaf] != normalized:
                raise ValueError('second-difference binding')
            if any(abs(v) >= 2*plan.point for v in vector):
                raise ValueError('leaf width')
            used.append(leaf)
    used.sort()
    unique_used = [u for i, u in enumerate(used) if i == 0 or u != used[i-1]]
    if unique_used != list(range(len(leaves))):
        raise ValueError('unused/missing leaves')
    pairs = []
    for i, u, sa in graph['sides'][0]:
        for j, v, sb in graph['sides'][1]:
            pairs.append((min(u, v), max(u, v), i+j, 1 if sa == sb else -1))
    pairs.sort()
    products, events = [], []
    for u, v, position, sign in pairs:
        if not products or products[-1] != (u, v):
            products.append((u, v))
        events.append((position, len(products)-1, sign))
    if graph['products'] != products or graph['events'] != sorted(events):
        raise ValueError('pair events')
    direct_leaves = [tuple(base.evaluate(v, row, E) for row in plan.rows) for v in leaves]
    direct_products = [tuple(E.mul(a, b) for a, b in zip(direct_leaves[u], direct_leaves[v])) for u, v in products]
    decoded = []
    for vector in leaves:
        value = 0
        for c, w in zip(vector, plan.weights):
            value = E.add(value, E.mul(c, w))
        decoded.append(value)
    if execution['leaf_rows'] != direct_leaves or execution['product_rows'] != direct_products:
        raise ValueError('node rows')
    if execution['targets'] != [E.mul(decoded[u], decoded[v]) for u, v in products]:
        raise ValueError('target products')
    if execution['source_rows'] != source_rows(graph['runs'], lengths, plan, E):
        raise ValueError('source maxima/width')
    return True


def integrate_events(graph, targets, E):
    last_product = sum(graph['lengths'])-2
    last_event = last_product+4
    states = [0]*4
    coefficients = []
    at = 0
    peak = 0
    for position in range(last_event+1):
        value = 0
        while at < len(graph['events']) and graph['events'][at][0] == position:
            _, product, sign = graph['events'][at]
            value = E.add(value, targets[product] if sign > 0 else -targets[product])
            at += 1
        for j in range(4):
            states[j] = E.add(states[j], value)
            value = states[j]
            peak = max(peak, base.bits(value))
        if position <= last_product:
            if value < 0:
                raise ArithmeticError('negative ordinary coefficient')
            coefficients.append(value)
        elif value:
            raise ArithmeticError('nonzero convolution tail')
    if at != len(graph['events']) or any(states):
        raise ArithmeticError('nonzero fourth-difference tail')
    return coefficients, peak


@dataclass
class AffineResult:
    value: int
    graph: dict
    execution: dict
    statistics: dict


def multiply_affine(a, b, *, budget_factor=None, verify=True, base_bits=1024):
    """Return None for a rejected input. The default multiplier sets a budget."""
    if type(a) is not int or type(b) is not int:
        raise TypeError('integers required')
    E = base.Elementary()
    negative = (a < 0) != (b < 0)
    a, b = abs(a), abs(b)
    N = max(a.bit_length(), b.bit_length())
    if not a or not b or N <= base_bits:
        value = E.mul(a, b) if a and b else 0
        if negative:
            value = -value
        return AffineResult(value, {}, {}, {'branch': 'elementary', 'root_bits': N, **E.summary()})
    r = N.bit_length()-1
    plan = base.native_plan(r, E)
    blocks = (base.split_blocks(a, plan.block_bits, E), base.split_blocks(b, plan.block_bits, E))
    parts = tuple(affine_partition(bs) for bs in blocks)
    ra, rb = map(len, parts)
    # Metadata only. Complete bit cost is included in the proof.
    if budget_factor is not None and ra*rb*r**4 > budget_factor*N:
        return None
    runs = tuple(certify_runs(bs, part, plan, E) for bs, part in zip(blocks, parts))
    if any(rs is None for rs in runs):
        return None
    graph = make_graph(runs, tuple(map(len, blocks)), plan, E)
    execution = evaluate_graph(graph, plan, E)
    if verify:
        check_certificate(blocks, graph, execution, plan, E)
    coefficients, peak = integrate_events(graph, execution['targets'], E)
    value = base.assemble(coefficients, plan.block_bits, len(coefficients)-1, E)
    if negative:
        value = -value
    E.tick('sign_and_root_conversion', max(1, N+abs(value).bit_length()))
    return AffineResult(value, graph, execution, {'branch': 'affine_shared',
        'root_bits': N, 'rank': r, 'block_bits': plan.block_bits,
        'lengths': graph['lengths'], 'run_counts': (ra, rb),
        'difference_counts': tuple(map(len, graph['sides'])),
        'pair_events': len(graph['events']), 'shared_products': len(graph['products']),
        'largest_prefix_bits': peak, 'verified': verify, **E.summary()})


def multiply(a, b, *, affine_budget=64, jump_budget=64, verify=True):
    result = multiply_affine(a, b, budget_factor=affine_budget, verify=verify)
    if result is not None:
        return result.value
    return accepted.multiply(a, b, budget_factor=jump_budget, verify=verify)
