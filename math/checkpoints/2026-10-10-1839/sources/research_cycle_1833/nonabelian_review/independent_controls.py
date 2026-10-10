#!/usr/bin/env python3
"""Independent audit controls. Never imports or executes the submitted programs.

Groups are generated as permutations or matrices. Stabilizers are recovered by
enumerating unions of cycles of each left-regular permutation, independently of
the submitted subset-image algorithm. Small cases additionally exhaust *all*
labeled permutations and use literal set translations for every prefix.
"""
from array import array
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import permutations
from math import factorial, gcd
from pathlib import Path
import ast
import hashlib
import json
import re
import time

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent.parent


def generated(identity, generators, multiply):
    elements = [identity]
    index = {identity: 0}
    for x in elements:
        for g in generators:
            y = multiply(x, g)
            if y not in index:
                index[y] = len(elements)
                elements.append(y)
    table = [[index[multiply(x, y)] for y in elements] for x in elements]
    return elements, table


def permutation_group(degree, generators):
    return generated(tuple(range(degree)), generators,
                     lambda a, b: tuple(a[b[j]] for j in range(degree)))


def dihedral(vertices):
    return permutation_group(vertices, [tuple((x + 1) % vertices for x in range(vertices)),
                                        tuple(-x % vertices for x in range(vertices))])


def quaternion_matrices():
    # Two matrices over F_3 square to -I and anticommute.
    def multiply(a, b):
        return ((a[0]*b[0]+a[1]*b[2]) % 3, (a[0]*b[1]+a[1]*b[3]) % 3,
                (a[2]*b[0]+a[3]*b[2]) % 3, (a[2]*b[1]+a[3]*b[3]) % 3)
    return generated((1, 0, 0, 1), [(0, 1, 2, 0), (1, 1, 1, 2)], multiply)


def group_checks(table):
    n = len(table)
    assert all(table[0][x] == x == table[x][0] for x in range(n))
    assert all(set(row) == set(range(n)) for row in table)
    assert all({table[x][y] for x in range(n)} == set(range(n)) for y in range(n))
    assert all(table[table[x][y]][z] == table[x][table[y][z]]
               for x in range(n) for y in range(n) for z in range(n))
    return [next(y for y in range(n) if table[x][y] == table[y][x] == 0)
            for x in range(n)]


def cycle_union_stabilizers(table):
    n = len(table)
    stabs = array('I', [0]) * (1 << n)
    cycle_profiles = []
    for g in range(n):
        remaining = set(range(n))
        cycles = []
        while remaining:
            x = min(remaining)
            cycle = 0
            while x in remaining:
                remaining.remove(x)
                cycle |= 1 << x
                x = table[g][x]
            cycles.append(cycle)
        masks = [0]
        for cycle in cycles:
            masks += [mask | cycle for mask in masks]
        for mask in masks:
            stabs[mask] |= 1 << g
        cycle_profiles.append([c.bit_count() for c in cycles])
    for mask in range(1, 1 << n):
        assert gcd(mask.bit_count(), n) % stabs[mask].bit_count() == 0
        assert stabs[mask] == stabs[((1 << n) - 1) ^ mask]
    return stabs, cycle_profiles


def literal_stabilizer(table, members):
    return frozenset(g for g, row in enumerate(table) if {row[x] for x in members} == members)


def exact_dp(table, stabs):
    n = len(table)
    # Compress out the mandatory identity bit. Every state denotes {e} union S.
    size = 1 << (n - 1)
    scores = array('h', [0]) * size
    counts = [0] * size
    final_bit = array('I', [0]) * size
    counts[0] = 1
    for state in range(1, size):
        bits = state
        best = -1
        ways = 0
        while bits:
            bit = bits & -bits
            bits -= bit
            prev = state ^ bit
            val = scores[prev]
            if val > best:
                best, ways, final_bit[state] = val, counts[prev], bit
            elif val == best:
                ways += counts[prev]
        scores[state] = best + stabs[(state << 1) | 1].bit_count() - 1
        counts[state] = ways
    state = size - 1
    order = []
    while state:
        bit = final_bit[state]
        order.append(bit.bit_length())
        state ^= bit
    order.append(0)
    order.reverse()
    prefix = set()
    literal = []
    for x in order:
        prefix.add(x)
        literal.append(sorted(literal_stabilizer(table, prefix)))
    assert sum(len(h) - 1 for h in literal) == scores[-1]
    return {'maximum': scores[-1], 'labeled_optimal_orders': n * counts[-1],
            'identity_first_states': size, 'witness_indices': order,
            'witness_stabilizers': literal}


def subgroup_lattice(table):
    n = len(table)
    # Independently test every identity-containing subset for closure.
    subgroups = []
    for mask in range(1, 1 << n, 2):
        if n % mask.bit_count():
            continue
        s = frozenset(x for x in range(n) if mask & (1 << x))
        if all(table[x][y] in s for x in s for y in s):
            subgroups.append(s)
    return sorted(subgroups, key=lambda s: (len(s), tuple(sorted(s))))


def maximal_subgroups(h, subs):
    proper = [k for k in subs if k < h]
    return [k for k in proper if not any(k < j for j in proper)]


def subgroup_controls(table, inverse, subs):
    n = len(table)
    permutable = all({table[x][y] for x in h for y in k} ==
                     {table[y][x] for x in h for y in k} for h in subs for k in subs)
    normals = [h for h in subs if all({table[table[g][x]][inverse[g]] for x in h} == h
                                    for g in range(n))]
    @lru_cache(None)
    def count(h):
        if len(h) == 1:
            return 1
        return sum(factorial(len(h)//len(k)) * count(k)**(len(h)//len(k))
                   for k in maximal_subgroups(h, subs))
    maxs = maximal_subgroups(frozenset(range(n)), subs)
    return {'subgroup_count': len(subs), 'pairwise_permutable': permutable,
            'normal_subgroup_count': len(normals),
            'all_subgroups_normal': len(normals) == len(subs),
            'maximal_subgroups': [sorted(k) for k in maxs],
            'maximal_indices': [n // len(k) for k in maxs],
            'maximal_subgroups_all_normal': all(k in normals for k in maxs),
            'formal_recursive_count': count(frozenset(range(n)))}


def hierarchy_tops(order, h, table, inverse, subs):
    if len(order) == 1:
        return [frozenset({0})]
    valid = []
    for k in maximal_subgroups(h, subs):
        size = len(k)
        ok = True
        for j in range(0, len(order), size):
            block = order[j:j+size]
            representative = block[0]
            if set(block) != {table[x][representative] for x in k}:
                ok = False
                break
            local = tuple(table[x][inverse[representative]] for x in block)
            if not hierarchy_tops(local, k, table, inverse, subs):
                ok = False
                break
        if ok:
            valid.append(k)
    return valid


def generated_subgroup(table, elements):
    result = set(elements) | {0}
    while True:
        enlarged = result | {table[x][y] for x in result for y in result}
        if enlarged == result:
            return frozenset(result)
        result = enlarged


def exhaustive_all_orders(name, table, inverse, subs, predicted_maximum):
    n = len(table)
    h = frozenset(range(n))
    hist = Counter()
    hierarchical = nonhierarchical_optimal = 0
    uniqueness_failures = saturation_disagreements = generated_top_disagreements = 0
    types = Counter()
    for order in permutations(range(n)):
        prefix = set()
        stabilizers = []
        for x in order:
            prefix.add(x)
            stabilizers.append(literal_stabilizer(table, prefix))
        score = sum(len(s) - 1 for s in stabilizers)
        hist[score] += 1
        tops = hierarchy_tops(order, h, table, inverse, subs)
        hierarchical += bool(tops)
        optimal = score == predicted_maximum
        if optimal and not tops:
            nonhierarchical_optimal += 1
        assert not tops or optimal
        if name in ('D8', 'Q8'):
            saturated = all(len(s) == gcd(j, n) for j, s in enumerate(stabilizers, 1))
            saturation_disagreements += saturated != optimal
            assert bool(tops) == optimal
            if optimal:
                uniqueness_failures += len(tops) != 1
                accumulated = generated_subgroup(table, set().union(*stabilizers[:-1]))
                generated_top_disagreements += accumulated != tops[0]
        if name == 'S3' and optimal:
            types[str(len(stabilizers[2]))] += 1
    assert sum(hist.values()) == factorial(n)
    assert max(hist) == predicted_maximum
    assert not uniqueness_failures and not saturation_disagreements and not generated_top_disagreements
    return {'all_labeled_orders_checked': factorial(n),
            'score_histogram': dict(sorted(hist.items())),
            'hierarchical_orders': hierarchical,
            'nonhierarchical_optimal_orders': nonhierarchical_optimal,
            'p_group_saturation_disagreements': saturation_disagreements,
            'p_group_top_uniqueness_failures': uniqueness_failures,
            'p_group_generated_top_disagreements': generated_top_disagreements,
            'S3_optimal_types_by_H3_order': dict(types)}


def convention_checks(table, inverse, stabs):
    n = len(table)
    checks = 0
    for mask in range(1 << n):
        subset = {x for x in range(n) if mask & (1 << x)}
        stab = literal_stabilizer(table, subset)
        assert sum(1 << x for x in stab) == stabs[mask]
        for y in range(n):
            right = {table[x][y] for x in subset}
            left = {table[y][x] for x in subset}
            assert literal_stabilizer(table, right) == stab
            assert literal_stabilizer(table, left) == {
                table[table[y][g]][inverse[y]] for g in stab}
            checks += 1
    return checks


def abelian_value(n):
    d = n
    w = Fraction(0)
    for p in range(2, n + 1):
        while d % p == 0:
            d //= p
            w += Fraction(p - 1, p)
    assert d == 1 and (n * w).denominator == 1
    return int(n * w)


def explicit_s3(elements, table, inverse, subs):
    a = elements.index((1, 0, 2))
    b = elements.index((0, 2, 1))
    order = [0, a, b, table[b][a], table[a][b], table[table[a][b]][a]]
    prefix = set()
    stabilizers = []
    accumulated = frozenset({0})
    containments = []
    for x in order:
        prefix.add(x)
        h = literal_stabilizer(table, prefix)
        stabilizers.append(sorted(h))
        accumulated = generated_subgroup(table, accumulated | h)
        containments.append(accumulated <= prefix)
    assert [len(h) for h in stabilizers] == [1, 2, 1, 2, 1, 6]
    assert containments == [True, True, True, False, False, True]
    assert not hierarchy_tops(tuple(order), frozenset(range(6)), table, inverse, subs)
    return {'symbols': ['e', 'a', 'b', 'ba', 'ab', 'aba'], 'indices': order,
            'stabilizers': stabilizers, 'accumulated_containment': containments,
            'score': sum(len(h) - 1 for h in stabilizers), 'hierarchical': False}


def check_submitted_witness(name, elements, table, saved):
    def decode(label):
        if name in ('S3', 'A4'):
            value = ast.literal_eval(label)
        elif name == 'Q8':
            # Quaternion i and j are the independently chosen matrix generators.
            units = {'1': (1, 0, 0, 1), 'i': (0, 1, 2, 0), 'j': (1, 1, 1, 2)}
            i, j = elements.index(units['i']), elements.index(units['j'])
            units['k'] = elements[table[i][j]]
            value = units[label.lstrip('-')]
            if label.startswith('-'):
                value = tuple(-x % 3 for x in value)
        else:
            a, b = map(int, re.fullmatch(r'r(\d+)s(\d+)', label).groups())
            degree = len(elements[0])
            action = 5 if name == 'M16' else degree - 1
            value = tuple((a + pow(action, b, degree) * x) % degree for x in range(degree))
        return elements.index(value)
    order = [decode(label) for label in saved['witness']]
    assert set(order) == set(range(len(table))) and order[0] == 0
    prefix = set()
    accumulated = frozenset({0})
    first_failure = None
    for j, x in enumerate(order, 1):
        prefix.add(x)
        actual = literal_stabilizer(table, prefix)
        assert actual == {decode(label) for label in saved['stabilizers'][j-1]}
        assert len(actual) == saved['stabilizer_orders'][j-1]
        accumulated = generated_subgroup(table, accumulated | actual)
        if first_failure is None and not accumulated <= prefix:
            first_failure = j
    assert first_failure == saved['accumulated_containment_first_failure']
    assert sum(h-1 for h in saved['stabilizer_orders']) == saved['maximum']
    return {'all_saved_stabilizers_recomputed': True,
            'accumulated_containment_first_failure': first_failure}


def main():
    start = time.monotonic()
    cases = [('S3', permutation_group(3, [(1, 0, 2), (0, 2, 1)])),
             ('D8', dihedral(4)), ('Q8', quaternion_matrices()), ('D10', dihedral(5)),
             ('A4', permutation_group(4, [(1, 2, 0, 3), (1, 0, 3, 2)])),
             ('D12', dihedral(6)), ('D14', dihedral(7)), ('D16', dihedral(8)),
             ('M16', permutation_group(8, [tuple((x + 1) % 8 for x in range(8)),
                                          tuple(5 * x % 8 for x in range(8))])),
             ('D18', dihedral(9))]
    # Static submitted JSON is comparison data, never executed or imported.
    submitted = json.loads((ROOT/'research_cycle_1826/nonabelian_prefix/fresh_exact_results.json').read_text())
    source_dir = ROOT/'research_cycle_1826/nonabelian_prefix'
    assert [json.loads(s) for s in (source_dir/'control_stdout.jsonl').read_text().splitlines()] == submitted
    submitted_structure = json.loads((source_dir/'structure_results.json').read_text())
    assert json.loads((source_dir/'structure_stdout.json').read_text()) == submitted_structure
    expected_structure = {r['group']: r for r in submitted_structure}
    expected = {r['group']: r for r in submitted}
    results = []
    for name, (elements, table) in cases:
        inverse = group_checks(table)
        stabs, cycles = cycle_union_stabilizers(table)
        r = {'group': name, 'order': len(table), 'element_encoding': elements,
             'multiplication_table': table, 'left_translation_cycle_lengths': cycles}
        r.update(exact_dp(table, stabs))
        r['abelian_value'] = abelian_value(len(table))
        assert r['maximum'] == r['abelian_value'] == expected[name]['maximum']
        assert r['labeled_optimal_orders'] == expected[name]['labeled_optimal_orders']
        r['submitted_witness_verification'] = check_submitted_witness(name, elements, table, expected[name])
        subs = subgroup_lattice(table)
        r['subgroup_controls'] = subgroup_controls(table, inverse, subs)
        if name in ('D8', 'Q8', 'D16', 'M16'):
            assert r['subgroup_controls']['formal_recursive_count'] == r['labeled_optimal_orders']
            assert r['subgroup_controls']['maximal_subgroups_all_normal']
            assert all(q == 2 for q in r['subgroup_controls']['maximal_indices'])
            assert all(len(h) == gcd(j, len(table))
                       for j, h in enumerate(r['witness_stabilizers'], 1))
        if name in ('S3', 'D8', 'Q8'):
            r['convention_subset_translation_checks'] = convention_checks(table, inverse, stabs)
            r['exhaustive'] = exhaustive_all_orders(name, table, inverse, subs, r['maximum'])
            assert r['exhaustive']['score_histogram'][r['maximum']] == r['labeled_optimal_orders']
            assert {str(k): v for k, v in r['exhaustive']['score_histogram'].items()} == expected_structure[name]['direct_permutation_check']['score_histogram']
        if name in expected_structure:
            frozen = expected_structure[name]
            for key in ('subgroup_count', 'pairwise_permutable', 'all_subgroups_normal'):
                assert r['subgroup_controls'][key] == frozen[key]
            assert r['subgroup_controls']['formal_recursive_count'] == frozen['formal_abelian_count_recurrence']
        if name == 'S3':
            r['explicit_boundary_witness'] = explicit_s3(elements, table, inverse, subs)
            assert r['subgroup_controls']['formal_recursive_count'] == 216
            assert r['exhaustive']['hierarchical_orders'] == 216
            assert r['exhaustive']['nonhierarchical_optimal_orders'] == 144
            assert r['exhaustive']['S3_optimal_types_by_H3_order'] == {'1': 288, '3': 72}
        if name == 'M16':
            assert len(subs) == 11
            assert r['subgroup_controls']['pairwise_permutable']
            assert not r['subgroup_controls']['all_subgroups_normal']
            shift = elements.index(tuple((x + 1) % 8 for x in range(8)))
            dilation = elements.index(tuple(5 * x % 8 for x in range(8)))
            conjugate = table[table[shift][dilation]][inverse[shift]]
            r4 = table[table[shift][shift]][table[shift][shift]]
            assert conjugate == table[r4][dilation] and conjugate not in (0, dilation)
            r['nonnormal_subgroup_witness'] = {'s': dilation, 'r_s_r_inverse': conjugate,
                                             'r4_s': table[r4][dilation]}
        results.append(r)
        print(json.dumps({'group': name, 'maximum': r['maximum'],
                          'count': r['labeled_optimal_orders'],
                          'states': r['identity_first_states'], 'status': 'PASS'}), flush=True)
    # A written-at-start fingerprint detects accidental predecessor changes.
    snapshot = json.loads((OUT/'INPUT_SNAPSHOT.json').read_text())
    for path, original in snapshot['files'].items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == original['sha256'], path
    output = {'status': 'PASS', 'method': 'fresh cycle-union stabilizers, compressed exact DP, full labeled permutation controls',
              'groups': results, 'identity_first_dp_states': sum(r['identity_first_states'] for r in results),
              'all_labeled_permutations_checked': sum(r.get('exhaustive', {}).get('all_labeled_orders_checked', 0) for r in results),
              'all_input_hashes_unchanged': True, 'elapsed_seconds': time.monotonic() - start}
    assert output['identity_first_dp_states'] == 209696
    assert output['all_labeled_permutations_checked'] == 81360
    (OUT/'independent_results.json').write_text(json.dumps(output, indent=2)+'\n')
    print(json.dumps({k: v for k, v in output.items() if k != 'groups'}), flush=True)


if __name__ == '__main__':
    main()
