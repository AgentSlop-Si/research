#!/usr/bin/env python3
"""Run-difference extension of the accepted native-matrix shared route.

The arithmetic/plan/stream primitives are imported from one hash-pinned reviewed
candidate, not from the historical original producer. This module is new.
All multiplication of arithmetic data uses that explicit elementary backend.
"""
from dataclasses import dataclass
import hashlib
import importlib.util
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parent / 'dependencies/shared_adaptive_completion_20261017_2130/shared_dispatcher.py'
BASE_SHA256 = 'a5c5e68fac2a43fa0847c15f2c09341c2da3f94013dc5a31ef6f797637fe4a06'
if hashlib.sha256(BASE.read_bytes()).hexdigest() != BASE_SHA256:
    raise RuntimeError('reviewed dependency hash mismatch')
_spec = importlib.util.spec_from_file_location('reviewed_shared_base', BASE)
base = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = base
_spec.loader.exec_module(base)


def run_transitions(blocks):
    """Exact change list, including the terminal transition to zero."""
    previous = 0
    changes = []
    for i, value in enumerate(blocks):
        if value != previous:
            changes.append((i, value))
            previous = value
    if previous:
        changes.append((len(blocks), 0))
    return changes


def signed_normalize(vector):
    first = next(v for v in vector if v)
    return (1, tuple(vector)) if first > 0 else (-1, tuple(-v for v in vector))


def make_graph(a_blocks, b_blocks, plan, E):
    """No supplied sparse/run oracle. Both complete block lists are scanned."""
    changes = [run_transitions(a_blocks), run_transitions(b_blocks)]
    raw = []
    zero = (0,) * plan.rank
    for side, records in enumerate(changes):
        previous = zero
        for position, value in records:
            current = base.canonical(value, plan, E) if value else zero
            difference = tuple(E.add(c, -p) for c, p in zip(current, previous))
            sign, vector = signed_normalize(difference)
            raw.append((vector, side, position, sign))
            previous = current
        if previous != zero:
            raise ArithmeticError('missing terminal transition')
    # Deterministic exact comparison sorting; no hashing or quadratic interning.
    raw.sort()
    leaves = []
    sides = [[], []]
    for vector, side, position, sign in raw:
        if not leaves or leaves[-1] != vector:
            leaves.append(vector)
        sides[side].append((position, len(leaves)-1, sign))
    for terms in sides:
        terms.sort()
    pairs = []
    for i, u, sign_a in sides[0]:
        for j, v, sign_b in sides[1]:
            lo, hi = (u, v) if u <= v else (v, u)
            pairs.append((lo, hi, i+j, 1 if sign_a == sign_b else -1))
    pairs.sort()
    products, events = [], []
    for u, v, position, sign in pairs:
        if not products or products[-1] != (u, v):
            products.append((u, v))
        events.append((position, len(products)-1, sign))
    events.sort()
    return {'version': 1, 'rank': plan.rank, 'point': plan.point,
            'block_bits': plan.block_bits, 'nodes': plan.nodes,
            'lengths': (len(a_blocks), len(b_blocks)), 'changes': changes,
            'leaves': leaves, 'sides': sides, 'products': products, 'events': events}


def source_rows(graph, leaf_rows, plan, E):
    """Actual maxima of the original native source rows, without dense rows."""
    result = []
    L = max(graph['lengths'])
    for xi, x in enumerate(plan.nodes):
        maxima = []
        for length, terms in zip(graph['lengths'], graph['sides']):
            running, largest = 0, 0
            for position, leaf, sign in terms:
                value = leaf_rows[leaf][xi]
                running = E.add(running, value if sign > 0 else -value)
                if position < length:
                    largest = max(largest, abs(running))
            if running:
                raise ArithmeticError('source difference polynomial has nonzero tail')
            maxima.append(largest)
        a_max, b_max = maxima
        if a_max and b_max:
            width, bound = base.slot_width(L, a_max, b_max, E)
        else:
            width, bound = 0, 0
        result.append((x, a_max, b_max, width, bound))
    return result


def evaluate_graph(graph, plan, E):
    leaf_rows = [tuple(base.evaluate(vector, row, E) for row in plan.rows)
                 for vector in graph['leaves']]
    node_rows = [tuple(E.mul(a, b) for a, b in zip(leaf_rows[u], leaf_rows[v]))
                 for u, v in graph['products']]
    targets = [base.interpolate(values, plan, E) for values in node_rows]
    return {'leaf_rows': leaf_rows, 'product_rows': node_rows, 'targets': targets,
            'source_rows': source_rows(graph, leaf_rows, plan, E)}


def check_certificate(a_blocks, b_blocks, plan, graph, execution, E):
    """Independent-form structural and target checks, including dense binding.

    This checker does not invoke make_graph or interpolation. Direct target
    products use only O(s)-bit operands and the explicit elementary multiplier.
    Their cost O(Q r^4) is included in the theorem.
    """
    if (graph['version'], graph['rank'], graph['point'], graph['block_bits'],
        tuple(graph['nodes']), tuple(graph['lengths'])) != (
            1, plan.rank, plan.point, plan.block_bits, plan.nodes,
            (len(a_blocks), len(b_blocks))):
        raise ValueError('header')
    leaves = graph['leaves']
    if not leaves or len(leaves) > sum(len(t) for t in graph['sides']):
        raise ValueError('leaf count')
    if list(leaves) != sorted(leaves) or any(a == b for a, b in zip(leaves, leaves[1:])):
        raise ValueError('leaf order/uniqueness')
    used = []
    zero = (0,) * plan.rank
    direct_run_rows = []
    for side, blocks in enumerate((a_blocks, b_blocks)):
        expected, changes, previous_value, previous_vector = [], [], 0, zero
        row_vectors = []
        # Separate full scan rather than invoking run_transitions.
        for position in range(len(blocks)+1):
            value = blocks[position] if position < len(blocks) else 0
            if value == previous_value:
                continue
            changes.append((position, value))
            vector = base.canonical(value, plan, E) if value else zero
            difference = tuple(E.add(c, -p) for c, p in zip(vector, previous_vector))
            sign, normalized = signed_normalize(difference)
            expected.append((position, normalized, sign))
            if position < len(blocks):
                row_vectors.append(vector)
            previous_value, previous_vector = value, vector
        if graph['changes'][side] != changes or len(graph['sides'][side]) != len(expected):
            raise ValueError('complete run binding')
        for (position, normalized, sign), actual in zip(expected, graph['sides'][side]):
            p, leaf, sg = actual
            if not (0 <= leaf < len(leaves)) or (p, sg) != (position, sign):
                raise ValueError('term binding')
            if leaves[leaf] != normalized:
                raise ValueError('canonical jump binding')
            used.append(leaf)
        direct_run_rows.append([tuple(base.evaluate(vector, row, E) for row in plan.rows)
                                for vector in row_vectors])
    used.sort()
    unique_used = [u for i, u in enumerate(used) if i == 0 or u != used[i-1]]
    if unique_used != list(range(len(leaves))):
        raise ValueError('unused/missing leaves')
    products = graph['products']
    if products != sorted(products) or any(a == b for a, b in zip(products, products[1:])):
        raise ValueError('product uniqueness')
    # Sorted merge assigns expected product identifiers without hash lookup.
    required = []
    for i, u, sa in graph['sides'][0]:
        for j, v, sb in graph['sides'][1]:
            u0, v0 = min(u, v), max(u, v)
            required.append((u0, v0, i+j, 1 if sa == sb else -1))
    required.sort()
    expected_products, expected_events = [], []
    for u, v, position, sign in required:
        if not expected_products or expected_products[-1] != (u, v):
            expected_products.append((u, v))
        expected_events.append((position, len(expected_products)-1, sign))
    if products != expected_products or graph['events'] != sorted(expected_events):
        raise ValueError('all term pair events')
    target_leaves = []
    for vector in leaves:
        if len(vector) != plan.rank or any(abs(c) >= plan.point for c in vector):
            raise ValueError('leaf bounds')
        target = 0
        for c, w in zip(vector, plan.weights):
            target = E.add(target, E.mul(c, w))
        target_leaves.append(target)
    if len(execution['targets']) != len(products):
        raise ValueError('target count')
    for (u, v), target in zip(products, execution['targets']):
        if E.mul(target_leaves[u], target_leaves[v]) != target:
            raise ValueError('interpolated target product')
    direct_leaves = [tuple(base.evaluate(vector, row, E) for row in plan.rows)
                     for vector in leaves]
    if direct_leaves != execution['leaf_rows']:
        raise ValueError('leaf evaluation')
    direct_products = [tuple(E.mul(a, b) for a, b in zip(direct_leaves[u], direct_leaves[v]))
                       for u, v in products]
    if direct_products != execution['product_rows']:
        raise ValueError('product evaluation')
    direct_sources = []
    for xi, x in enumerate(plan.nodes):
        maxima = [max((abs(row[xi]) for row in rows), default=0) for rows in direct_run_rows]
        if all(maxima):
            width, bound = base.slot_width(max(graph['lengths']), *maxima, E)
        else:
            width, bound = 0, 0
        direct_sources.append((x, *maxima, width, bound))
    if direct_sources != execution['source_rows']:
        raise ValueError('actual source maxima/width')
    return True


def integrate_events(graph, targets, E):
    last_delta = sum(graph['lengths'])
    last_product = last_delta-2
    events = graph['events']
    event_index, first, second, peak = 0, 0, 0, 0
    coefficients = []
    for position in range(last_delta+1):
        delta = 0
        while event_index < len(events) and events[event_index][0] == position:
            _, product, sign = events[event_index]
            value = targets[product]
            delta = E.add(delta, value if sign > 0 else -value)
            event_index += 1
        first = E.add(first, delta)
        second = E.add(second, first)
        peak = max(peak, base.bits(delta), base.bits(first), base.bits(second))
        if position <= last_product:
            if second < 0:
                raise ArithmeticError('negative ordinary convolution coefficient')
            coefficients.append(second)
        elif second:
            raise ArithmeticError('nonzero terminal convolution coefficient')
    if event_index != len(events) or first or second:
        raise ArithmeticError('nonzero second-difference tail')
    return coefficients, peak


@dataclass
class RunResult:
    value: int
    accepted: bool
    graph: dict
    execution: dict
    statistics: dict


def multiply_runs(a, b, *, budget_factor=None, verify=True, base_bits=1024):
    """Try the run branch; None means exact linear-budget rejection.

    An omitted budget permits all finite transition counts for experiments; the
    complete cost is then the parameterized bound, not automatically O(N).
    """
    if not isinstance(a, int) or not isinstance(b, int):
        raise TypeError('integers required')
    E = base.Elementary()
    sign_negative = (a < 0) != (b < 0)
    a, b = abs(a), abs(b)
    N = max(a.bit_length(), b.bit_length())
    if not a or not b or N <= base_bits:
        value = E.mul(a, b) if a and b else 0
        if sign_negative:
            value = -value
        return RunResult(value, True, {}, {}, {'branch': 'elementary', 'root_bits': N, **E.summary()})
    r = N.bit_length()-1
    # The inherited plan is built in its fresh ledger before root-size scans.
    plan = base.native_plan(r, E)
    a_blocks = base.split_blocks(a, plan.block_bits, E)
    b_blocks = base.split_blocks(b, plan.block_bits, E)
    ka, kb = len(run_transitions(a_blocks)), len(run_transitions(b_blocks))
    M = ka*kb  # Metadata only; the full metadata bit cost is charged in the proof.
    if budget_factor is not None and M*r**4 > budget_factor*N:
        return None
    graph = make_graph(a_blocks, b_blocks, plan, E)
    execution = evaluate_graph(graph, plan, E)
    if verify:
        check_certificate(a_blocks, b_blocks, plan, graph, execution, E)
    coefficients, peak = integrate_events(graph, execution['targets'], E)
    value = base.assemble(coefficients, plan.block_bits, len(coefficients)-1, E)
    if sign_negative:
        value = -value
    E.tick('sign_and_root_conversion', max(1, N+abs(value).bit_length()))
    stats = {'branch': 'run_shared', 'root_bits': N, 'rank': r,
             'block_bits': plan.block_bits, 'lengths': graph['lengths'],
             'occupied': (sum(bool(v) for v in a_blocks), sum(bool(v) for v in b_blocks)),
             'jump_counts': (ka, kb), 'pair_events': M,
             'shared_leaves': len(graph['leaves']), 'shared_products': len(graph['products']),
             'largest_prefix_bits': peak, 'verified': verify, **E.summary()}
    return RunResult(value, True, graph, execution, stats)


def multiply(a, b, *, budget_factor=64, verify=True):
    """Complete exact front end. Rejection preserves the accepted fallback."""
    result = multiply_runs(a, b, budget_factor=budget_factor, verify=verify)
    if result is not None:
        return result.value
    return base.Dispatcher().multiply(a, b)
