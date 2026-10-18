#!/usr/bin/env python3
"""Fresh independent controls; no earlier control file is imported or run.

Native arithmetic is used only here as an endpoint/identity oracle. Production
multiplications remain the pinned explicit elementary backend.
"""
import copy
import hashlib
import json
import math
from pathlib import Path
import random
import time
import run_shared as candidate

HERE = Path(__file__).resolve().parent
rng = random.Random(202610180007)
results = {'plans': [], 'complete_products': [], 'source_rows': [],
           'mutations': [], 'recognition': [], 'nonlinear_encoding': []}


def direct_binomial(x, j):
    numerator = 1
    for h in range(j):
        numerator *= x-h
    return numerator // math.factorial(j)


def independent_plan(r):
    ell = math.lcm(*range(1, r+1))
    d = ell//r
    congruences = []
    for p in range(2, r+1):
        if any(p % h == 0 for h in range(2, math.isqrt(p)+1)):
            continue
        q, u = 1, 1
        while d % (q*p) == 0:
            q *= p
        while ell % (u*p) == 0:
            u *= p
        if q > 1:
            congruences.append(((-pow(ell//u, -1, q)) % q, q))
    k = sum(residue*(d//q)*pow(d//q, -1, q) for residue, q in congruences) % d if d > 1 else 1
    P = 1+k*ell
    weights = tuple(math.comb(P+j-1, j) for j in range(r+1))
    s = (weights[-1]//d).bit_length()-1
    norms = lambda x: sum(abs(direct_binomial(x, h)) for h in range(r))
    start = min(range(r), key=lambda a: (max(norms(-a), norms(2*r-2-a)), a))
    return P, s, weights[:-1], tuple(range(-start, 2*r-1-start))


def direct_digits(value, weights):
    out = [0] * len(weights)
    for h in range(len(weights)-1, -1, -1):
        out[h], value = divmod(value, weights[h])
    assert value == 0
    return tuple(out)


def direct_row(blocks, weights, x):
    return [sum(((-1)**h)*digit*direct_binomial(x, h)
                for h, digit in enumerate(direct_digits(block, weights))) for block in blocks]


def from_blocks(blocks, s):
    return sum(value << (s*i) for i, value in enumerate(blocks))


def independent_blocks(value, s):
    value = abs(value)
    mask = (1 << s)-1
    answer = []
    while value:
        answer.append(value & mask)
        value >>= s
    return answer or [0]


def check_source_identities(a, b, result, max_rows=None):
    stats = result.statistics
    r, s = stats['rank'], stats['block_bits']
    P, independent_s, weights, nodes = independent_plan(r)
    assert s == independent_s
    ab, bb = independent_blocks(a, s), independent_blocks(b, s)
    graph, executed = result.graph, result.execution
    selected = list(range(len(nodes)))
    if max_rows is not None and max_rows < len(selected):
        selected = sorted({0, len(nodes)//2, len(nodes)-1})
    for xi in selected:
        x = nodes[xi]
        ar, br = direct_row(ab, weights, x), direct_row(bb, weights, x)
        am, bm = max(map(abs, ar)), max(map(abs, br))
        bound = max(len(ab), len(bb))*am*bm
        width = 8*((2*bound).bit_length()+7)//8 if bound else 0
        # Parentheses matter: exact source byte rounding.
        width = 8*(((2*bound).bit_length()+7)//8) if bound else 0
        assert executed['source_rows'][xi] == (x, am, bm, width, bound)
        for side, row in zip(graph['sides'], (ar, br)):
            expected = [row[0]] + [v-u for u, v in zip(row, row[1:])] + [-row[-1]]
            represented = [0] * (len(row)+1)
            for position, leaf, sign in side:
                represented[position] = sign*executed['leaf_rows'][leaf][xi]
            assert represented == expected
        if width:
            Q = 1 << width
            packed_a = sum(v << (width*i) for i, v in enumerate(ar))
            packed_b = sum(v << (width*j) for j, v in enumerate(br))
            numerator = sum(sign*executed['product_rows'][pid][xi] << (width*position)
                            for position, pid, sign in graph['events'])
            assert numerator == (1-Q)**2 * packed_a * packed_b
            quotient, remainder = divmod(numerator, (1-Q)**2)
            assert remainder == 0 and quotient == packed_a*packed_b
        else:
            assert not any(ar) or not any(br)
        results['source_rows'].append({'rank': r, 'node': x, 'width': width,
                                       'lengths': [len(ar), len(br)]})


def check_product(label, a, b, *, identities=False, budget=None, base_bits=1024):
    before = time.perf_counter()
    answer = candidate.multiply_runs(a, b, budget_factor=budget, base_bits=base_bits)
    assert answer is not None, label
    assert answer.value == a*b, label
    record = {'label': label, **answer.statistics,
              'elapsed_seconds': round(time.perf_counter()-before, 6)}
    results['complete_products'].append(record)
    if identities and answer.graph:
        check_source_identities(a, b, answer, max_rows=3)
    print('PASS', label, record.get('jump_counts'), record.get('occupied'),
          record.get('shared_products'), flush=True)
    return answer


for r in range(3, 25):
    plan = candidate.base.native_plan(r, candidate.base.Elementary())
    P, s, weights, nodes = independent_plan(r)
    assert (plan.point, plan.block_bits, plan.weights, plan.nodes) == (P, s, weights, nodes)
    results['plans'].append({'rank': r, 'point': P, 'block_bits': s})

# Complete signed elementary and low-threshold controls.
for a, b in [(0, 0), (0, -19), (-1, 1), (1, -1), (-7, -13), (2**80-1, -(2**73+1))]:
    check_product('elementary_sign_zero', a, b)
for i in range(12):
    a = rng.getrandbits(rng.randrange(180, 1200))
    b = rng.getrandbits(rng.randrange(50, 1100))
    if i % 2:
        a = -a
    if i % 3:
        b = -b
    check_product('arbitrary_small_%02d' % i, a, b, base_bits=64)

# Full dense support and a genuinely growing number of unrelated run values.
growing = []
for r in [12, 14, 16, 18, 20]:
    P, s, weights, nodes = independent_plan(r)
    rho = 1 << s
    length = (1 << r)//s+2
    run_count = max(2, (4*math.isqrt(1 << r))//(r*r))
    values_a = [rng.randrange(1, rho) for _ in range(run_count)]
    values_b = [rng.randrange(1, rho) for _ in range(run_count+1)]
    a_blocks = [values_a[min(run_count-1, i*run_count//length)] for i in range(length)]
    b_blocks = [values_b[min(run_count, i*(run_count+1)//length)] for i in range(length)]
    a, b = from_blocks(a_blocks, s), from_blocks(b_blocks, s)
    answer = check_product('growing_dense_runs_rank_%02d' % r, a, -b,
                           identities=True, budget=64)
    assert answer.statistics['rank'] == r
    assert min(answer.statistics['occupied']) > 4
    assert answer.statistics['pair_events']*r**4 <= 64*answer.statistics['root_bits']
    growing.append(answer.statistics)
results['growing_family'] = growing

# Dense constant blocks, all-ones carry boundaries, zeros, and unequal lengths.
r = 16
P, s, weights, nodes = independent_plan(r)
rho = 1 << s
length = (1 << r)//s+2
constant_a = from_blocks([rho-1]*length, s)
constant_b = from_blocks([rho//3]*(length-7), s)
constant_answer = check_product('dense_constant_full_carry', constant_a, constant_b,
                                identities=True, budget=64)
assert constant_answer.statistics['jump_counts'] == (2, 2)
assert constant_answer.statistics['shared_products'] == 1
mixed_a = [0]*(length//5) + [rho-1]*(length//5) + [0]*(length//5)
mixed_a += [P+7]*(length-len(mixed_a))
mixed_b = [P]*(length//4) + [3*P+1]*(length//4)
mixed_b += [rho-2]*(length-len(mixed_b))
answer = check_product('zero_gaps_leading_shift_and_cancellation',
                       -from_blocks(mixed_a, s), from_blocks(mixed_b, s),
                       identities=True, budget=64)
check_product('very_unbalanced_full_run', constant_a, -(rho-3), identities=True, budget=64)
check_product('both_negative_high_carries', -constant_a, -constant_a,
              identities=True, budget=64)

# Explicit regression: re-encoding integer jumps would change original rows.
first, second = P-1, P+1
v1, v2 = direct_digits(first, weights), direct_digits(second, weights)
difference = tuple(b-a for a, b in zip(v1, v2))
reencoded = direct_digits(second-first, weights)
assert difference != reencoded
assert sum(c*w for c, w in zip(difference, weights)) == second-first
results['nonlinear_encoding'].append({'rank': r, 'first': first, 'second': second,
                                     'difference_vector': difference,
                                     'reencoded_integer_jump': reencoded})

# Exact pre-conversion budget rejection and complete fallback, without a huge dense test.
rejected = candidate.multiply_runs(constant_a, constant_b, budget_factor=0)
assert rejected is None
results['recognition'].append({'case': 'zero_budget_rejects', 'passed': True})
fallback_a, fallback_b = (1 << 2048)+1, (1 << 2039)+3
assert candidate.multiply(fallback_a, fallback_b, budget_factor=0) == fallback_a*fallback_b
results['recognition'].append({'case': 'accepted_dispatcher_fallback', 'passed': True})

# Fresh certificate mutations. All must be rejected by the independent-form checker.
a_blocks = independent_blocks(constant_a, s)
b_blocks = independent_blocks(constant_b, s)
plan = candidate.base.native_plan(r, candidate.base.Elementary())
original_graph, original_execution = constant_answer.graph, constant_answer.execution

def rejection(name, change_graph=None, change_execution=None):
    graph, execution = copy.deepcopy(original_graph), copy.deepcopy(original_execution)
    if change_graph:
        change_graph(graph)
    if change_execution:
        change_execution(execution)
    failed = False
    try:
        candidate.check_certificate(a_blocks, b_blocks, plan, graph, execution, candidate.base.Elementary())
    except (ValueError, ArithmeticError, IndexError, AssertionError):
        failed = True
    assert failed, name
    results['mutations'].append({'case': name, 'rejected': True})

rejection('omit_terminal_transition', lambda g: g['sides'][0].pop())
rejection('omit_input_change', lambda g: g['changes'][0].pop())
rejection('bad_event_position', lambda g: g['events'].__setitem__(0, (1, *g['events'][0][1:])))
rejection('bad_event_sign', lambda g: g['events'].__setitem__(0, (*g['events'][0][:2], -g['events'][0][2])))
rejection('extra_product', lambda g: g['products'].append(g['products'][0]))
rejection('bad_target', change_execution=lambda e: e['targets'].__setitem__(0, e['targets'][0]+1))
rejection('bad_source_width', change_execution=lambda e: e['source_rows'].__setitem__(0, (*e['source_rows'][0][:3], e['source_rows'][0][3]+8, e['source_rows'][0][4])))
rejection('bad_leaf_row', change_execution=lambda e: e['leaf_rows'].__setitem__(0, (e['leaf_rows'][0][0]+1, *e['leaf_rows'][0][1:])))
rejection('bad_product_row', change_execution=lambda e: e['product_rows'].__setitem__(0, (e['product_rows'][0][0]+1, *e['product_rows'][0][1:])))

results['summary'] = {'complete_products': len(results['complete_products']),
                      'independent_plans': len(results['plans']),
                      'source_rows': len(results['source_rows']),
                      'mutation_rejections': len(results['mutations']),
                      'pass': True}
(HERE/'RESULTS.json').write_text(json.dumps(results, indent=2)+'\n')
print(json.dumps(results['summary'], indent=2), flush=True)
