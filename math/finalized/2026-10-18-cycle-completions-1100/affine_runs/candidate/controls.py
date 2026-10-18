#!/usr/bin/env python3
"""Fresh exact controls. Native products are test oracles, never production."""
from pathlib import Path
import copy
import hashlib
import itertools
import json
import math
import random
import affine_shared as prod
base = prod.base
RNG = random.Random(202610181043)
RESULTS = {'status': 'running', 'plans': [], 'certification_cases': 0,
           'graph_products': 0, 'source_identities': 0, 'convolutions': 0,
           'complete_products': [], 'corruption_rejections': [], 'obstructions': []}


def choose(x, j):
    value = 1
    for k in range(j):
        value = value*(x-k)//(k+1)
    return value


def canonical(a, plan):
    digits = [0]*plan.rank
    for j in reversed(range(plan.rank)):
        digits[j], a = divmod(a, choose(plan.point+j-1, j))
    assert a == 0
    return tuple(digits)


def polynomial(v, x):
    return sum((-1)**j*c*choose(x, j) for j, c in enumerate(v))


def difference(seq, order):
    result = list(seq)
    for _ in range(order):
        result = [result[0]]+[b-a for a, b in zip(result, result[1:])]+[-result[-1]]
    return result


def convolution(a, b):
    result = [0]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            result[i+j] += x*y
    return result


def integer(blocks, s):
    return sum(a << (i*s) for i, a in enumerate(blocks))


def check_graph(a, b, plan, packed=True):
    E = base.Elementary()
    parts = tuple(prod.affine_partition(bs) for bs in (a, b))
    runs = tuple(prod.certify_runs(bs, part, plan, E) for bs, part in zip((a, b), parts))
    if any(rs is None for rs in runs):
        return None
    graph = prod.make_graph(runs, (len(a), len(b)), plan, E)
    execution = prod.evaluate_graph(graph, plan, E)
    assert prod.check_certificate((a, b), graph, execution, plan, E)
    c, _ = prod.integrate_events(graph, execution['targets'], E)
    assert c == convolution(a, b)
    assert base.assemble(c, plan.block_bits, len(c)-1, E) == integer(a, plan.block_bits)*integer(b, plan.block_bits)
    RESULTS['convolutions'] += 1
    for side, bs in enumerate((a, b)):
        vectors = [canonical(v, plan) for v in bs]
        for h in range(plan.rank):
            expected = difference([v[h] for v in vectors], 2)
            actual = [0]*len(expected)
            for position, leaf, sign in graph['sides'][side]:
                actual[position] = sign*graph['leaves'][leaf][h]
            assert actual == expected
    for xi, x in enumerate(plan.nodes):
        ar = [polynomial(canonical(a0, plan), x) for a0 in a]
        br = [polynomial(canonical(b0, plan), x) for b0 in b]
        da, db = difference(ar, 2), difference(br, 2)
        e = [0]*(len(da)+len(db)-1)
        for position, product, sign in graph['events']:
            e[position] += sign*execution['product_rows'][product][xi]
        assert e == convolution(da, db)
        assert e == difference(convolution(ar, br), 4)
        am, bm = max(map(abs, ar)), max(map(abs, br))
        bound = max(len(a), len(b))*am*bm
        width = 8*(((2*bound).bit_length()+7)//8) if bound else 0
        assert execution['source_rows'][xi] == (x, am, bm, width, bound)
        if packed and bound:
            Q = 1 << width
            assert sum(v*Q**i for i, v in enumerate(da))*sum(v*Q**i for i, v in enumerate(db)) == (1-Q)**4*sum(v*Q**i for i, v in enumerate(ar))*sum(v*Q**i for i, v in enumerate(br))
        RESULTS['source_identities'] += 1
        RESULTS['convolutions'] += 2
    RESULTS['graph_products'] += 1
    return graph, execution


def run():
    plans = {}
    for r in range(2, 25):
        plan = base.native_plan(r, base.Elementary())
        H = math.lcm(*range(1, r+1))
        d = H//r
        assert plan.point > H
        assert plan.weights == tuple(choose(plan.point+j-1, j) for j in range(r))
        assert plan.rows == tuple(tuple((-1)**j*choose(x, j) for j in range(r)) for x in plan.nodes)
        assert plan.interpolation == tuple(choose(-plan.point-plan.nodes[0], j) for j in range(2*r-1))
        assert math.comb(r, r//2) <= H
        plans[r] = plan
        RESULTS['plans'].append({'rank': r, 'point_bits': plan.point.bit_length(), 'block_bits': plan.block_bits})
    # Endpoint certification exhaustively/randomly agrees with all interior
    # canonical vectors whenever it accepts. The test uses no production proof.
    for r in range(2, 11):
        p = plans[r]
        cap = 1 << p.block_bits
        for _ in range(150):
            length = RNG.randrange(1, 30)
            slope = RNG.randrange(-max(1, cap//(2*length)), max(2, cap//(2*length)))
            low = max(0, -(length-1)*slope)
            high = min(cap-1, cap-1-(length-1)*slope)
            if low > high:
                continue
            first = RNG.randint(low, high)
            bs = [first+i*slope for i in range(length)]
            rs = prod.certify_runs(bs, [(0, length)], p, base.Elementary())
            if rs is not None:
                _, _, u, v, _ = rs[0]
                assert all(canonical(a, p) == tuple(x+i*y for x, y in zip(u, v)) for i, a in enumerate(bs))
            RESULTS['certification_cases'] += 1
    for r in (2, 3, 4, 6, 8, 10):
        p = plans[r]
        cap = 1 << p.block_bits
        for _ in range(10):
            a = [RNG.randrange(cap) for i in range(RNG.randrange(1, 10))]
            b = [RNG.randrange(cap) for i in range(RNG.randrange(1, 10))]
            if not any(a): a[-1] = 1
            if not any(b): b[-1] = 1
            check_graph(a, b, p)
        for a, b in (([1]*8, [2]*9), (list(range(1, 10)), list(range(10, 0, -1))),
                     ([0, 0, 1, 2, 3, 3, 3, 1, 0, 0, 2], [2, 1, 0, 0, 0, 1])):
            if max(a+b) < cap:
                check_graph(a, b, p)
    # A numeric affine carry trap, and a dense-canonical-curvature family.
    for r in (6, 10, 16):
        p = plans[r]
        bs = [p.point-1+i for i in range(12)]
        assert prod.certify_runs(bs, [(0, len(bs))], p, base.Elementary()) is None
        stride = (p.point+1)//2
        bs = [stride*(i+1) for i in range(80)]
        assert max(bs) < 1 << p.block_bits
        low = [canonical(v, p)[0] for v in bs]
        support = sum(bool(v) for v in difference(low, 2))
        assert support >= len(bs)-2
        RESULTS['obstructions'].append({'rank': r, 'numeric_affine_runs': 1, 'blocks': len(bs), 'low_coordinate_delta2_support': support})
    # Quadratic first-three-plus-last sampling does not inherit the affine
    # endpoint lemma: an interior carry can escape all four samples.
    p = plans[10]
    q = (p.point+23)//24
    bs = [q*t*(10-t) for t in range(11)]
    assert max(bs) < 1 << p.block_bits
    assert all(canonical(bs[t],p) == (bs[t],)+(0,)*(p.rank-1) for t in (0,1,2,10))
    assert canonical(bs[5],p) != (bs[5],)+(0,)*(p.rank-1)
    RESULTS['quadratic_endpoint_obstruction'] = {'rank': 10, 'sample_positions': [0,1,2,10], 'failed_interior_position': 5}
    # Complete signed front end, including new-only accepted dense ramps.
    for r in (10, 12, 14, 16, 18, 20):
        p = plans[r]
        length = (2**r+p.block_bits-1)//p.block_bits+1
        assert length < p.point
        a = integer(list(range(1, length+1)), p.block_bits)
        b = integer(list(range(length, 0, -1)), p.block_bits)
        assert max(a.bit_length(), b.bit_length()).bit_length()-1 == r
        result = prod.multiply_affine(-a, b, budget_factor=64)
        assert result is not None and result.value == -a*b
        assert result.statistics['difference_counts'] == (3, 3)
        old = prod.accepted.multiply_runs(a, b, budget_factor=64)
        # The initial finite rank can fall below the old predicate; record it.
        record = result.statistics
        record['old_jump_budget_accepted'] = old is not None
        record['first_jump_counts'] = (length+1, length+1)
        RESULTS['complete_products'].append(record)
    # High canonical coordinate plus affine low coordinate: these cases pay
    # near-full block widths and ordinary output carry chains.
    for r in (10, 12, 14, 16, 20):
        p = plans[r]
        length = (2**r+p.block_bits-1)//p.block_bits+1
        top = ((2**p.block_bits-1)//p.weights[-1]-1)*p.weights[-1]
        assert top > 0 and top+length < 2**p.block_bits
        a = integer([top+i+1 for i in range(length)],p.block_bits)
        b = integer([top+length-i for i in range(length-2)],p.block_bits)
        result = prod.multiply_affine(a,-b,budget_factor=64)
        assert result is not None and result.value == -a*b
        assert result.statistics['rank'] == r
        assert result.statistics['largest_prefix_bits'] > p.block_bits
        record = result.statistics
        record['fixture'] = 'wide_affine_carry'
        RESULTS['complete_products'].append(record)
    for a, b in ((0, 7), (-7, 4), (1, -1), (2**1023-1, 2**1022+3),
                 (2**1100+123456789, -(2**1070+987654321))):
        assert prod.multiply(a, b) == a*b
        RESULTS['complete_products'].append({'branch': 'full_front_end', 'bits': max(abs(a).bit_length(), abs(b).bit_length())})
    # Exact budget guard fires before any canonical conversion.
    p = plans[12]
    length = (2**12+p.block_bits-1)//p.block_bits+1
    a = integer(list(range(1, length+1)), p.block_bits)
    old_cert = prod.certify_runs
    def forbidden(*args): raise AssertionError('conversion ran after budget rejection')
    prod.certify_runs = forbidden
    assert prod.multiply_affine(a, a, budget_factor=0) is None
    prod.certify_runs = old_cert
    assert prod.multiply(a, -a, affine_budget=0) == -a*a
    # A failed endpoint certificate also stops before graph construction.
    p = plans[10]
    length = (2**10+p.block_bits-1)//p.block_bits+1
    a = integer([p.point-1+i for i in range(length)],p.block_bits)
    old_graph = prod.make_graph
    prod.make_graph = forbidden
    assert prod.multiply_affine(a,a,budget_factor=64) is None
    prod.make_graph = old_graph
    assert prod.multiply(a,-a) == -a*a
    RESULTS['complete_products'].append({'branch': 'canonical_rejection_full_fallback', 'bits': a.bit_length()})
    # Corrupt one field at a time. Source arrays remain independently bound.
    p = plans[10]
    bs = ([1, 2, 3, 4, 5, 8, 10, 12], [4, 3, 2, 1, 7, 7, 7])
    fixture = check_graph(*bs, p)
    assert fixture is not None
    good_g, good_e = fixture
    mutations = [
        ('order', lambda g,e: g.update(order=1)),
        ('rank', lambda g,e: g.update(rank=g['rank']+1)),
        ('nodes', lambda g,e: g.update(nodes=tuple(x+1 for x in g['nodes']))),
        ('lengths', lambda g,e: g.update(lengths=(999, 999))),
        ('missing_side', lambda g,e: g['sides'].pop()),
        ('missing_run_side', lambda g,e: g.update(runs=(g['runs'][0],))),
        ('missing_run', lambda g,e: g['runs'][0].pop()),
        ('bad_endpoint', lambda g,e: g['runs'][0].__setitem__(0, (g['runs'][0][0][0], g['runs'][0][0][1], tuple(v+1 for v in g['runs'][0][0][2]), g['runs'][0][0][3], g['runs'][0][0][4]))),
        ('bad_slope', lambda g,e: g['runs'][0].__setitem__(0, (g['runs'][0][0][0], g['runs'][0][0][1], g['runs'][0][0][2], tuple(v+1 for v in g['runs'][0][0][3]), g['runs'][0][0][4]))),
        ('bad_run_start', lambda g,e: g['runs'][0].__setitem__(0, (1, *g['runs'][0][0][1:]))),
        ('missing_term', lambda g,e: g['sides'][0].pop()),
        ('term_sign', lambda g,e: g['sides'][0].__setitem__(0, (g['sides'][0][0][0],g['sides'][0][0][1],-g['sides'][0][0][2]))),
        ('missing_event', lambda g,e: g['events'].pop()),
        ('extra_event', lambda g,e: g['events'].append(g['events'][0])),
        ('event_position', lambda g,e: g['events'].__setitem__(0,(g['events'][0][0]+1,*g['events'][0][1:]))),
        ('leaf_vector', lambda g,e: g['leaves'].__setitem__(0,tuple(v+1 for v in g['leaves'][0]))),
        ('missing_product', lambda g,e: g['products'].pop()),
        ('target', lambda g,e: e['targets'].__setitem__(0,e['targets'][0]+1)),
        ('leaf_row', lambda g,e: e['leaf_rows'].__setitem__(0,tuple(v+1 for v in e['leaf_rows'][0]))),
        ('product_row', lambda g,e: e['product_rows'].__setitem__(0,tuple(v+1 for v in e['product_rows'][0]))),
        ('source_width', lambda g,e: e['source_rows'].__setitem__(0,tuple(v+8 if i==3 else v for i,v in enumerate(e['source_rows'][0])))),
    ]
    for name, mutate in mutations:
        g, e = copy.deepcopy(good_g), copy.deepcopy(good_e)
        mutate(g,e)
        try: prod.check_certificate(bs,g,e,p,base.Elementary())
        except (ValueError, IndexError, TypeError): RESULTS['corruption_rejections'].append(name)
        else: raise AssertionError('mutation accepted: '+name)
    corrupt_bs = (list(bs[0]), list(bs[1])); corrupt_bs[0][2] += 1
    try: prod.check_certificate(corrupt_bs,good_g,good_e,p,base.Elementary())
    except ValueError: RESULTS['corruption_rejections'].append('dense_interior_input')
    else: raise AssertionError('changed dense input accepted')
    RESULTS['status'] = 'pass'


if __name__ == '__main__':
    try:
        run()
    finally:
        Path(__file__).with_name('RESULTS.json').write_text(json.dumps(RESULTS, indent=2)+'\n')
    print(json.dumps({k: v if not isinstance(v,list) else len(v) for k,v in RESULTS.items()}, indent=2))
