"""Independent review controls for ALG-070. Python standard library only.

The online comparison is self-authored using common-denominator integer credits.
The exact offline oracle is a global shortest path on (request index, cache
bitmask): a primitive action loads one page, discards one page, or serves the
next request. It includes paid speculation and time-indexed availability.
Candidate code is imported only for cross-checking, not to define either oracle.
"""
from collections import Counter
from fractions import Fraction as Q
from heapq import heappop, heappush
from itertools import product
from math import lcm
from pathlib import Path
import hashlib
import importlib.util
import json
import random
import sys
import time

HERE = Path(__file__).resolve().parent
COUNTS = Counter()
EXAMPLES = {}


def import_file(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


policy_module = import_file('reviewed_policy', HERE / 'candidate/weighted_cache.py')
oracle_module = import_file('reviewed_oracle', HERE / 'candidate/offline_oracle.py')


def integer_policy(sequence, k, prices):
    denominator = lcm(*(x.denominator for x in prices))
    costs = [int(x * denominator) for x in prices]
    residents = []
    credits = []
    paid = 0
    candidate = policy_module.WeightedCache(k, dict(enumerate(prices)))
    for v in sequence:
        if v is None:
            continue
        miss = v not in residents
        if not miss:
            credits[residents.index(v)] = costs[v]
        else:
            if len(residents) == k:
                amount = min(credits)
                credits = [x - amount for x in credits]
                zeros = [h for h, c in zip(residents, credits) if c == 0]
                slot = residents.index(min(zeros))
                residents.pop(slot)
                credits.pop(slot)
            residents.append(v)
            credits.append(costs[v])
            paid += costs[v]
        assert candidate.request(v) == miss
        assert candidate.total == Q(paid, denominator)
        assert candidate.credit == {h: Q(c, denominator) for h, c in zip(residents, credits)}
        assert all(0 <= c <= costs[h] for h, c in zip(residents, credits))
        COUNTS['integer_policy_step_matches'] += 1
    return Q(paid, denominator)


def primitive_offline(sequence, k, prices, available=None):
    """Dijkstra on all chronological primitive actions; no subset-jump formula."""
    full = (1 << len(prices)) - 1
    availability = [full] * len(sequence) if available is None else available
    start = (0, 0)
    best = {start: Q(0)}
    heap = [(Q(0), 0, 0)]
    while heap:
        value, t, cache = heappop(heap)
        if best.get((t, cache)) != value:
            continue
        if t == len(sequence):
            return value
        neighbors = []
        request = sequence[t]
        if request is None or cache & (1 << request):
            neighbors.append((t + 1, cache, Q(0)))
        for v, price in enumerate(prices):
            bit = 1 << v
            if cache & bit:
                neighbors.append((t, cache ^ bit, Q(0)))
            elif availability[t] & bit and cache.bit_count() < k:
                neighbors.append((t, cache | bit, price))
        for nt, nc, charge in neighbors:
            target = (nt, nc)
            nv = value + charge
            if target not in best or nv < best[target]:
                best[target] = nv
                heappush(heap, (nv, nt, nc))
    raise ValueError('infeasible request or availability')


def verify_manifest():
    root = HERE / 'candidate'
    manifest = json.loads((root / 'MANIFEST.json').read_text())
    for record in manifest['files']:
        body = (root / record['path']).read_bytes()
        assert len(body) == record['bytes'], record['path']
        assert hashlib.sha256(body).hexdigest() == record['sha256'], record['path']
        blob = b'blob ' + str(len(body)).encode() + b'\0' + body
        assert hashlib.sha1(blob).hexdigest() == record['git_blob_sha1'], record['path']
        COUNTS['manifest_files_verified'] += 1
    binding = json.loads((root / 'SOURCE_BINDING.json').read_text())
    for entry in [binding['accepted_uniform_report']['binding'],
                  binding['prior_report']['binding'], binding['task_plan']]:
        body = (root / entry['path']).read_bytes()
        assert hashlib.sha256(body).hexdigest() == entry['sha256']
        assert hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest() == entry['git_blob_sha1']
        COUNTS['controlling_source_bindings_verified'] += 1
    original = (HERE / 'dependencies/ACCEPTED_UNIFORM_REPORT.md')
    assert original.read_bytes() == (root / 'source/ACCEPTED_UNIFORM_REPORT.md').read_bytes()
    COUNTS['designated_local_source_matches'] += 1
    replay = json.loads((HERE / 'replay/VALIDATION.json').read_text())
    retained = json.loads((root / 'VALIDATION.json').read_text())
    for key in ('result', 'failures', 'counts', 'examples', 'source_sha256', 'scope'):
        assert replay[key] == retained[key], key
    COUNTS['candidate_replay_semantic_matches'] += 1


def exhaustive_checks():
    worst = (Q(0), None)
    vectors = [(Q(1, 3), Q(11, 7), Q(13, 2)), (Q(100), Q(1), Q(1)),
               (Q(1), Q(1), Q(1)), (Q(17, 19), Q(101, 103), Q(5, 2))]
    for prices in vectors:
        for k in (1, 2, 3):
            candidate_oracle = oracle_module.OfflineOracle(k, dict(enumerate(prices)))
            for n in range(6):
                for sequence in product(range(3), repeat=n):
                    paid = integer_policy(sequence, k, prices)
                    optimum = primitive_offline(sequence, k, prices)
                    assert optimum == candidate_oracle.solve(sequence)
                    assert paid <= k * optimum
                    COUNTS['independent_global_oracle_sequences'] += 1
                    if optimum and paid / optimum > worst[0]:
                        worst = (paid / optimum, [k, list(map(str, prices)), sequence])
    EXAMPLES['largest_exhaustive_ratio'] = [str(worst[0]), worst[1]]


def random_release_and_zero_checks():
    rng = random.Random(202610181929)
    for trial in range(180):
        m = rng.randrange(2, 6)
        k = rng.randrange(1, m + 1)
        prices = tuple(Q(rng.randrange(1, 150), rng.randrange(1, 43)) for _ in range(m))
        sequence = []
        availability = []
        for t in range(20):
            released = min(m, 1 + t // 3)
            availability.append((1 << released) - 1)
            sequence.append(None if t % 7 == 0 else rng.randrange(released))
        paid = integer_policy(sequence, k, prices)
        optimum = primitive_offline(sequence, k, prices, availability)
        assert paid <= k * optimum
        active = [v for v in sequence if v is not None]
        active_sets = [{v for v in range(m) if mask & (1 << v)}
                       for mask, request in zip(availability, sequence) if request is not None]
        candidate = oracle_module.OfflineOracle(k, dict(enumerate(prices)))
        assert optimum == candidate.solve(active, active_sets)
        COUNTS['release_and_zero_output_traces'] += 1
    # A legal prefetched page must be paid once even if it predates first service.
    prices = (Q(2, 5), Q(7, 3))
    assert primitive_offline([0, 1], 2, prices) == sum(prices)
    assert primitive_offline([None, 0, None, 1], 2, prices) == sum(prices)
    COUNTS['paid_prefetch_explicit_checks'] += 2


def potential_checks():
    prices = (Q(2, 5), Q(7, 3), Q(19, 11), Q(101, 2))
    for k in (1, 2, 3):
        masks = [m for m in range(1 << len(prices)) if m.bit_count() <= k]
        for amask in masks:
            av = [v for v in range(len(prices)) if amask & (1 << v)]
            for factors in product((Q(0), Q(1, 5), Q(1, 2), Q(1)), repeat=len(av)):
                credit = {v: prices[v] * f for v, f in zip(av, factors)}
                for omask in masks:
                    ov = [v for v in range(len(prices)) if omask & (1 << v)]
                    def potential(cs, os):
                        return (k - 1) * sum(cs.values(), Q(0)) + k * sum((prices[v] - cs.get(v, 0) for v in os), Q(0))
                    start = potential(credit, ov)
                    assert start >= 0
                    for request in ov:
                        candidate = policy_module.WeightedCache(k, dict(enumerate(prices)))
                        candidate.credit = credit.copy()
                        candidate.request(request)
                        assert candidate.total + potential(candidate.credit, ov) <= start
                        COUNTS['independent_potential_service_states'] += 1
                    for v in ov:
                        assert potential(credit, [w for w in ov if w != v]) <= start
                        COUNTS['independent_potential_evictions'] += 1
                    if len(ov) < k:
                        for v in range(len(prices)):
                            if v not in ov:
                                assert potential(credit, ov + [v]) - start <= k * prices[v]
                                COUNTS['independent_potential_loads'] += 1


def convolution_and_sharpness_checks():
    def conv(a, b):
        n = len(a)
        return tuple(sum((a[j] * b[(i - j) % n] for j in range(n)), Q(0)) for i in range(n))
    def coefficient_product(operands):
        n = len(operands[0])
        out = [Q(0)] * n
        for indexes in product(range(n), repeat=len(operands)):
            term = Q(1)
            for a, j in zip(operands, indexes):
                term *= a[j]
            out[sum(indexes) % n] += term
        return tuple(out)
    sys.path.insert(0, str(HERE / 'candidate'))
    candidate_test = import_file('candidate_convolution_helpers', HERE / 'candidate/validate.py')
    for n in (1, 2, 4, 7):
        a = tuple(Q(n + 1 if i == 0 else 1) for i in range(n))
        b = (Q(1),) + (Q(0),) * (n - 1)
        kernels = [tuple(Q((v + 2) * (i + 3), v + 1) for i in range(n)) for v in range(5)]
        views = [conv(conv(a, b), h) for h in kernels]
        assert len(set(views)) == len(kernels)
        for h, actual in zip(kernels, views):
            assert actual == tuple(n * x + sum(h) for x in h)
            COUNTS['invertible_convolution_realizations'] += 1
        for depth in (1, 2, 3):
            front = candidate_test.FrontEnd(n)
            ra, rb = front.register(a), front.register(b)
            rhs = [front.register(h) for h in kernels[:depth]]
            handle = front.recipe(ra, rb, rhs)
            result, count = candidate_test.build(front, handle)
            assert result == coefficient_product([a, b] + kernels[:depth])
            charge = (depth + 1) * (8 * n * n + n + 1) + 2 * n + 3
            assert sum(count.values()) == charge
            assert candidate_test.tariff(n, front.recipes[handle]) == charge
            COUNTS['fresh_convolution_recipe_controls'] += 1
    # New adversarial traces with a deliberately different zero-credit tie rule.
    for k in range(1, 10):
        cache = []
        sequence = []
        for t in range(150):
            v = max(set(range(k + 1)) - set(cache))
            sequence.append(v)
            if len(cache) == k:
                cache.pop(0)
            cache.append(v)
        phases = []
        labels = set()
        for v in sequence:
            if v not in labels and len(labels) == k:
                phases.append(labels)
                labels = set()
            labels.add(v)
        phases.append(labels)
        cache = set()
        paid = 0
        cursor = 0
        for phase in phases:
            target = set(phase)
            target.update(v for v in sorted(cache) if len(target) < k)
            target.update(v for v in range(k + 1) if len(target) < k)
            assert len(target) == k
            if cache:
                assert len(target - cache) <= 1
            paid += len(target - cache)
            cache = target
        assert paid <= k + (len(sequence) - 1) // k
        COUNTS['independent_sharpness_phase_schedules'] += 1


def main():
    start = time.monotonic()
    for check in (verify_manifest, exhaustive_checks, random_release_and_zero_checks,
                  potential_checks, convolution_and_sharpness_checks):
        before = time.monotonic()
        check()
        print(f'{check.__name__}: PASS ({time.monotonic() - before:.3f}s)', flush=True)
    result = {'result': 'PASS', 'counts': dict(COUNTS), 'examples': EXAMPLES,
              'elapsed_seconds': round(time.monotonic() - start, 3),
              'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'candidate_report_sha256': hashlib.sha256((HERE / 'candidate/REPORT.md').read_bytes()).hexdigest(),
              'scope': 'Finite controls support the independently reviewed proof; they are not proof of unbounded claims.'}
    (HERE / 'REVIEW_VALIDATION.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    main()
