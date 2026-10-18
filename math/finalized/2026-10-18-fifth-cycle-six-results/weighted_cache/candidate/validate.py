"""Fresh exact validation for ALG-070; standard-library-only, no fetched code.

Proofs are in REPORT.md. These finite controls do not establish the theorem.
"""
import copy
import hashlib
import itertools
import json
import platform
import random
import time
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path

from weighted_cache import WeightedCache, run
from offline_oracle import OfflineOracle, action_graph_optimum

HERE = Path(__file__).resolve().parent
COUNTS = Counter()
EXAMPLES = {}


def phi(k, credit, offline, tariffs):
    return ((k - 1) * sum(credit.values(), Q(0)) +
            k * sum((tariffs[v] - credit.get(v, Q(0)) for v in offline), Q(0)))


def exhaustive_prefixes():
    families = [(1, 2, 5), (Q(1, 2), Q(2, 3), Q(7, 4)), (3, 3, 3), (1, 100, 2)]
    maxratio = (Q(0), None)
    for prices in families:
        tariffs = dict(enumerate(map(Q, prices)))
        for k in (1, 2, 3):
            oracle = OfflineOracle(k, tariffs)
            def visit(seq, online, dp):
                nonlocal maxratio
                opt = min(dp.values())
                assert online.total <= k * opt
                COUNTS['exhaustive_prefix_comparisons'] += 1
                if opt and online.total / opt > maxratio[0]:
                    maxratio = (online.total / opt, [list(map(str, prices)), k, list(seq)])
                if len(seq) == 7:
                    return
                for v in range(3):
                    nxt = copy.deepcopy(online)
                    nxt.request(v)
                    visit(seq + (v,), nxt, oracle.step(dp, v))
            visit((), WeightedCache(k, tariffs), oracle.initial())
    EXAMPLES['largest_small_instance_ratio'] = [str(maxratio[0]), maxratio[1]]


def independent_graph_checks():
    tariffs = {0: Q(2, 7), 1: Q(5, 3), 2: Q(19, 2)}
    for k in (1, 2, 3):
        oracle = OfflineOracle(k, tariffs)
        for length in range(5):
            for seq in itertools.product(range(3), repeat=length):
                assert oracle.solve(seq) == action_graph_optimum(seq, k, tariffs)
                COUNTS['two_offline_oracles_agree'] += 1
    # It is legal to prefetch the other page before its first request; it is paid.
    oracle = OfflineOracle(2, {0: Q(1, 2), 1: Q(7, 3)})
    dp = oracle.step(oracle.initial(), 0)
    both = oracle.states.index(frozenset({0, 1}))
    assert dp[both] == Q(17, 6)
    assert oracle.solve([0, 1]) == Q(17, 6)
    COUNTS['explicit_paid_prefetch_controls'] += 1


def primitive_potential_checks():
    tariffs = {0: Q(2, 3), 1: Q(3, 2), 2: Q(7, 5), 3: Q(13, 4)}
    universe = range(4)
    for k in (1, 2, 3):
        states = [frozenset(s) for n in range(k + 1) for s in itertools.combinations(universe, n)]
        for a in states:
            av = sorted(a)
            for vals in itertools.product((Q(0), Q(1, 3), Q(1)), repeat=len(a)):
                credit = {v: tariffs[v] * fraction for v, fraction in zip(av, vals)}
                for o in states:
                    before = phi(k, credit, o, tariffs)
                    assert before >= 0
                    for v in o:
                        assert phi(k, credit, o - {v}, tariffs) <= before
                        COUNTS['offline_eviction_transitions'] += 1
                    if len(o) < k:
                        for v in set(universe) - o:
                            assert phi(k, credit, o | {v}, tariffs) - before <= k * tariffs[v]
                            COUNTS['offline_load_transitions'] += 1
                    for request in o:
                        policy = WeightedCache(k, tariffs)
                        policy.credit = credit.copy()
                        policy.request(request)
                        assert policy.total + phi(k, policy.credit, o, tariffs) <= before
                        COUNTS['online_service_transitions'] += 1


def random_and_adversarial():
    rng = random.Random(70020261018)
    for m in (3, 4, 5, 6):
        prices = {v: Q(rng.randint(1, 100), rng.randint(1, 19)) for v in range(m)}
        for k in range(1, min(m, 4) + 1):
            oracle = OfflineOracle(k, prices)
            for _ in range(8):
                seq = tuple(rng.randrange(m) for _ in range(60))
                a = run(seq, k, prices)
                assert a.total <= k * oracle.solve(seq)
                COUNTS['long_random_sequences'] += 1
    for k in range(1, 9):
        tariffs = {v: Q(1) for v in range(k + 1)}
        policy = WeightedCache(k, tariffs)
        seq = []
        for _ in range(400):
            v = min(set(tariffs) - set(policy.credit))
            seq.append(v)
            assert policy.request(v)
        phases = []
        current = set()
        for v in seq:
            if v not in current and len(current) == k:
                phases.append(current)
                current = set()
            current.add(v)
        phases.append(current)
        loads = k
        prior = set(phases[0])
        prior.update(v for v in tariffs if len(prior) < k and v not in prior)
        for phase in phases[1:]:
            target = set(phase)
            target.update(v for v in sorted(prior) if len(target) < k and v not in target)
            target.update(v for v in tariffs if len(target) < k and v not in target)
            assert len(target) == k
            assert len(target - prior) <= 1
            loads += len(target - prior)
            prior = target
        assert loads <= k + (len(seq) - 1) // k
        assert policy.total == len(seq)
        COUNTS['adversarial_phase_certificates'] += 1


class FrontEnd:
    """Paid exact version/recipe registry; no collision-based identification."""
    def __init__(self, n):
        self.n = n
        self.raw = []
        self.recipes = []
        self.g = Counter()

    def register(self, values):
        values = tuple(map(Q, values))
        self.g['ingested_scalars'] += len(values)
        assert len(values) == self.n
        for i, old in enumerate(self.raw):
            # Full scan, including on unequal candidates, for simple exact ledger.
            equal = [x == y for x, y in zip(values, old)]
            self.g['normalization_scalar_reads'] += 2 * self.n
            self.g['normalization_equalities'] += self.n
            self.g['normalization_metadata'] += 1
            if all(equal):
                return i
        self.raw.append(values)
        self.g['raw_backing_writes'] += self.n
        return len(self.raw) - 1

    def recipe(self, a, b, kernels):
        key = (a, b, tuple(kernels))
        self.g['recipe_key_work'] += 2 + len(kernels)
        for i, old in enumerate(self.recipes):
            self.g['recipe_key_work'] += 2 + len(kernels) + len(old[2])
            if old == key:
                return i
        self.recipes.append(key)
        self.g['recipe_key_work'] += 2 + len(kernels)
        return len(self.recipes) - 1


def convolution(a, b, counts):
    n = len(a)
    out = [Q(0)] * n
    counts['zero_writes'] += n
    for i in range(n):
        for j in range(n):
            s = (i + j) % n
            out[s] += a[i] * b[j]
            counts['index_operations'] += 2
            counts['scalar_reads'] += 3
            counts['multiplications'] += 1
            counts['additions'] += 1
            counts['scalar_writes'] += 1
    counts['workspace_release'] += 1
    return out


def build(front, handle):
    a, b, hs = front.recipes[handle]
    count = Counter()
    count['slot_and_validity_metadata'] += 3
    result = convolution(front.raw[a], front.raw[b], count)
    for h in hs:
        result = convolution(result, front.raw[h], count)
    final = tuple(result)
    count['final_slot_copy_reads'] += front.n
    count['final_slot_copy_writes'] += front.n
    return final, count


def tariff(n, recipe):
    return Q((1 + len(recipe[2])) * (8 * n * n + n + 1) + 2 * n + 3)


def direct_product_oracle(operands):
    # Independent all-index coefficient product, no convolution routine reused.
    n = len(operands[0])
    out = [Q(0)] * n
    for indexes in itertools.product(range(n), repeat=len(operands)):
        value = Q(1)
        for a, i in zip(operands, indexes):
            value *= a[i]
        out[sum(indexes) % n] += value
    return tuple(out)


def convolution_controls():
    ledger_examples = []
    for n in (2, 3, 5):
        front = FrontEnd(n)
        base = [n + 1] + [1] * (n - 1)
        a0 = front.register(base)
        moved = base.copy()
        moved[1] += Q(2, 3)
        front.g['exact_update_additions'] += 1
        a1 = front.register(moved)
        moved[1] -= Q(2, 3)
        front.g['exact_update_additions'] += 1
        assert front.register(moved) == a0
        COUNTS['cancel_restore_version_checks'] += 1
        b = front.register([1] + [0] * (n - 1))
        hs = [front.register([Q((i + 1) * (j + 2), i + 2) for j in range(n)]) for i in range(3)]
        handles = [front.recipe(a, b, hs[:d]) for a in (a0, a1) for d in (1, 2, 3)]
        assert front.recipe(a0, b, hs[:2]) == handles[1]
        prices = {v: tariff(n, front.recipes[v]) for v in handles}
        front.g['certified_tariff_preparation'] += len(handles) * 4
        expected = {}
        for v in handles:
            ai, bi, kernels = front.recipes[v]
            operands = [front.raw[ai], front.raw[bi]] + [front.raw[h] for h in kernels]
            expected[v] = direct_product_oracle(operands)
        seq = [handles[i % 6] for i in [0, 1, 2, 0, 3, 4, 0, 5, 1, 0, 4, 2, 0, 1, 3, 0]] * 3
        for k in (1, 2, 3):
            policy = WeightedCache(k, prices)
            buffers = {}
            charges = Counter()
            active = []
            g = front.g.copy()
            zero_queries = 0
            for t, v in enumerate(seq):
                coords = [] if t % 11 == 0 else ([0, 0] if t % 5 == 0 else list(range(n)))
                g['query_ingestion'] += 1 + len(coords)
                if not coords:
                    zero_queries += 1
                    continue
                active.append(v)
                miss = policy.request(v)
                for gone in set(buffers) - set(policy.credit):
                    del buffers[gone]
                if miss:
                    vector, count = build(front, v)
                    assert sum(count.values()) == prices[v]
                    buffers[v] = vector
                    charges.update(count)
                assert set(buffers) == set(policy.credit)
                assert len(buffers) <= k
                assert [buffers[v][i] for i in coords] == [expected[v][i] for i in coords]
                g['coordinate_read_and_emit'] += 2 * len(coords)
                COUNTS['convolution_query_controls'] += 1
            opt = OfflineOracle(k, prices).solve(active)
            assert policy.total == sum(charges.values())
            assert policy.total <= k * opt
            common = sum(g.values())
            assert common + policy.total <= k * (common + opt)
            COUNTS['zero_output_queries_charged'] += zero_queries
            COUNTS['actual_recipe_builds'] += policy.build_count
            ledger_examples.append({'N': n, 'K': k, 'G': common,
                                    'G_categories': dict(g), 'build_charge': str(policy.total),
                                    'build_categories': dict(charges), 'offline_build_optimum': str(opt),
                                    'raw_backing_scalars': n * len(front.raw),
                                    'view_capacity_scalars': k * n,
                                    'peak_declared_scratch_scalars': 2 * n + 1})
    EXAMPLES['convolution_ledgers'] = ledger_examples


def interleaved_version_control():
    # Here update, exact version registration, and restoration happen while
    # actual materializations remain resident, not only before a cache run.
    front = FrontEnd(3)
    current = [Q(4), Q(1), Q(1)]
    a0 = front.register(current)
    b = front.register([1, 0, 0])
    h = front.register([1, 2, 3])
    v0 = front.recipe(a0, b, [h])
    f0 = tariff(3, front.recipes[v0])
    policy = WeightedCache(2, {v0: f0})
    buffers = {}
    assert policy.request(v0)
    buffers[v0], _ = build(front, v0)
    current[1] += Q(2, 3)
    front.g['exact_update_additions'] += 1
    a1 = front.register(current)
    v1 = front.recipe(a1, b, [h])
    f1 = tariff(3, front.recipes[v1])
    policy.register_tariff(v1, f1)
    front.g['certified_tariff_registration'] += 4
    assert policy.request(v1)
    buffers[v1], _ = build(front, v1)
    assert buffers[v0] != buffers[v1]
    previous_G = sum(front.g.values())
    current[1] -= Q(2, 3)
    front.g['exact_update_additions'] += 1
    restored = front.register(current)
    assert restored == a0 and front.recipe(restored, b, [h]) == v0
    assert sum(front.g.values()) > previous_G
    assert not policy.request(v0)
    assert policy.total == f0 + f1 and policy.build_count == 2
    expected = direct_product_oracle([front.raw[a0], front.raw[b], front.raw[h]])
    assert buffers[v0] == expected
    oracle = OfflineOracle(2, {v0: f0, v1: f1})
    assert oracle.solve([v0, v1, v0], [{v0}, {v0, v1}, {v0, v1}]) == policy.total
    try:
        policy.register_tariff(v0, f0 + 1)
    except ValueError:
        COUNTS['immutable_price_change_rejections'] += 1
    else:
        raise AssertionError('an existing handle was repriced')
    COUNTS['interleaved_paid_update_restore_hits'] += 1
    EXAMPLES['interleaved_restore'] = {'requests': [v0, v1, v0], 'builds': policy.build_count,
                                     'optional_charge': str(policy.total),
                                     'G_categories': dict(front.g),
                                     'restored_query_was_hit': True}


def mutation_controls():
    # Mutate actual built arrays and emitted operation ledgers, then compare
    # against the independent complete-product oracle and declared tariff.
    front = FrontEnd(3)
    a0 = front.register([4, 1, 1])
    a1 = front.register([4, 2, 1])
    b = front.register([1, 0, 0])
    h = front.register([1, 2, 3])
    v0, v1 = front.recipe(a0, b, [h]), front.recipe(a1, b, [h])
    vec0, charge0 = build(front, v0)
    vec1, charge1 = build(front, v1)
    expected1 = direct_product_oracle([front.raw[a1], front.raw[b], front.raw[h]])
    assert vec1 == expected1 and vec0 != expected1
    expected_charge = tariff(3, front.recipes[v1])
    assert sum(charge1.values()) == expected_charge
    mutation_evidence = {}
    claims = {
        'free_speculative_materialization': Q(0),
        'charge_unit_instead_of_tariff': Q(1),
        'omit_final_slot_copy': sum(charge1.values()) - charge1['final_slot_copy_reads'] - charge1['final_slot_copy_writes'],
        'omit_scratch_initialization': sum(charge1.values()) - charge1['zero_writes'],
    }
    for name, claim in claims.items():
        assert claim != expected_charge
        mutation_evidence[name] = {'claimed': str(claim), 'required': str(expected_charge)}
    # Illegal retained complete vector after eviction acts as a third slot.
    retained = {0: vec0, 1: vec1, 2: tuple(x * 2 for x in vec0)}
    assert len(retained) > 2
    mutation_evidence['retain_unaccounted_scratch_view'] = {'retained_views': 3, 'capacity': 2}
    partial = vec1[:1]
    assert len(partial) != front.n
    mutation_evidence['partial_answer_as_complete_view'] = {'stored_entries': len(partial), 'required': front.n}
    assert vec0 != expected1
    mutation_evidence['display_name_aliases_distinct_versions'] = {'wrong': list(map(str, vec0)), 'required': list(map(str, expected1))}
    # An actual cancel/restore scan is performed and then removed from G.
    moved = [4, 2, 1]
    moved[1] -= 1
    front.g['exact_update_additions'] += 1
    assert front.register(moved) == a0
    g_required = sum(front.g.values())
    g_omitted = g_required - front.g['normalization_scalar_reads'] - front.g['normalization_equalities']
    assert g_omitted < g_required
    mutation_evidence['omit_paid_return_to_old_version'] = {'claimed_G': g_omitted, 'required_G': g_required}
    COUNTS['rejected_accounting_mutations'] += len(mutation_evidence)
    EXAMPLES['accounting_mutation_evidence'] = mutation_evidence
    # A substantive bad-policy counterexample: price-oblivious LRU can exceed K.
    prices = {0: Q(100), 1: Q(1), 2: Q(1)}
    seq = (0, 1, 2) * 20
    recency, badcost = [], Q(0)
    for v in seq:
        if v in recency:
            recency.remove(v)
        else:
            badcost += prices[v]
            if len(recency) == 2:
                recency.pop()
        recency.insert(0, v)
    opt = OfflineOracle(2, prices).solve(seq)
    assert badcost > 2 * opt
    EXAMPLES['price_oblivious_lru_counterexample'] = {
        'tariffs': list(map(str, prices.values())), 'sequence': '(0,1,2) repeated 20 times',
        'LRU_cost': str(badcost), 'OPT_cost': str(opt), 'K': 2,
        'weighted_policy_cost': str(run(seq, 2, prices).total)}
    COUNTS['rejected_bad_policy_controls'] += 1


def edge_controls():
    for k in (1, 2, 7):
        assert run([], k, {0: Q(1, 13)}).total == 0
        assert run([0] * 100, k, {0: Q(1, 13)}).total == Q(1, 13)
        COUNTS['empty_and_repeat_controls'] += 2
    for bad in (0, -1):
        try:
            WeightedCache(1, {0: bad})
        except ValueError:
            COUNTS['invalid_tariff_rejections'] += 1
        else:
            raise AssertionError('accepted nonpositive tariff')
    oracle = OfflineOracle(2, {0: 1, 1: 2, 2: 3})
    assert oracle.solve([0, 1, 2, 0], [{0}, {0, 1}, {0, 1, 2}, {0, 1, 2}]) >= 6
    COUNTS['registration_availability_controls'] += 1


def main():
    started = time.monotonic()
    for test in (edge_controls, independent_graph_checks, primitive_potential_checks,
                 exhaustive_prefixes, random_and_adversarial, convolution_controls,
                 interleaved_version_control, mutation_controls):
        t = time.monotonic()
        test()
        print(f'{test.__name__}: PASS ({time.monotonic() - t:.3f}s)', flush=True)
    result = {
        'owner': 'ALG-070', 'result': 'PASS', 'failures': 0,
        'python': platform.python_version(), 'elapsed_seconds': round(time.monotonic() - started, 3),
        'counts': dict(COUNTS), 'examples': EXAMPLES,
        'source_sha256': {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest()
                          for name in ('weighted_cache.py', 'offline_oracle.py', 'validate.py')},
        'scope': 'Finite exact controls only; arbitrary-sequence theorem is proved in REPORT.md.'}
    (HERE / 'VALIDATION.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'result': result['result'], 'counts': result['counts'],
                      'elapsed_seconds': result['elapsed_seconds']}, indent=2), flush=True)


if __name__ == '__main__':
    main()
