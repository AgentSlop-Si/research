"""New tests only. No historical module, test, helper, or archive is executed."""
import hashlib
import itertools
import json
from pathlib import Path
import random
import unittest

from alg007_bounded_adapter import P, GENERATOR, transform, ContractError


def root_for(q):
    return pow(GENERATOR, (P - 1) // q, P)


def direct_dft(raw, root):
    # Oracle is the definition, without any FFT kernel or adapter helper.
    q = len(raw)
    return tuple(sum(value * pow(root, (-index * frequency) % q, P)
                     for index, value in enumerate(raw)) % P
                 for frequency in range(q))


def exact_support(raw, m, a, beta, root):
    q, k = len(raw), len(raw) // m
    active = set()
    for block in range(k):
        for mode in range(m):
            coefficient = sum(raw[block * m + t] * pow(root,
                (a*t*(t-1)//2 + (a*m*block+beta)*t + k*mode*t) % q, P)
                for t in range(m)) % P
            if coefficient:
                active.add(mode)
    return active


def synthesize(q, m, coefficients, a=1, beta=0, root=None):
    # Test-only generation; every production call still reads raw coordinates.
    root = root or root_for(q)
    k, inverse_m = q // m, pow(m, P - 2, P)
    raw = []
    for block in range(k):
        for t in range(m):
            chirp = a*t*(t-1)//2 + (a*m*block+beta)*t
            raw.append(sum(value * pow(root, (-chirp-k*mode*t) % q, P)
                           for mode, value in coefficients[block].items()) * inverse_m % P)
    return raw


class AdapterTests(unittest.TestCase):
    cases = 0
    output_coordinates = 0
    routes = {}
    snapshots = []

    def checked(self, raw, m, cap, **kwargs):
        result = transform(raw, m, cap, **kwargs)
        self.assertEqual(result['values'], direct_dft(raw, result['model']['root']))
        self.assertEqual(len(result['values']), len(raw))
        ledger = result['ledger']
        rebuilt = {}
        for counts in ledger['phases'].values():
            for key, value in counts.items():
                rebuilt[key] = rebuilt.get(key, 0) + value
        self.assertEqual(rebuilt, ledger['total'])
        self.assertEqual(sum(rebuilt.values()), ledger['total_units'])
        attempt = sum(sum(ledger['phases'].get(phase, {}).values())
                      for phase in ('recognition', 'decode'))
        self.assertEqual(attempt, ledger['attempt_spent'])
        self.assertLessEqual(attempt, ledger['attempt_budget'])
        self.assertEqual(ledger['phases']['output']['output_coordinate'], len(raw))
        self.assertGreaterEqual(ledger['phases']['input']['data_read'], 2*len(raw))
        self.assertEqual(ledger['phases']['setup']['field_mul'], len(raw)-1)
        n = len(raw)
        exponents = [P-1, (P-1)//2, (P-1)//3, (P-1)//5,
                     n, n//2, P-2, P-2]
        if kwargs.get('root') is None:
            exponents.append((P-1)//n)
        h = sum(e.bit_count() + 2*e.bit_length() - 1 for e in exponents)
        cold = 15*n + 11 + h
        self.assertEqual(cold, sum(ledger['phases']['input'].values())
                         + sum(ledger['phases']['setup'].values()))
        if result['route'] == 'GREEN_ACCEPT':
            support = exact_support(raw, m, kwargs.get('a', 1), kwargs.get('beta', 0), result['model']['root'])
            self.assertEqual(set(result['support']), support)
            self.assertLessEqual(len(support), cap)
            self.assertEqual(result['progress']['completed_blocks'], len(raw)//m)
            self.assertEqual(ledger['phases']['recognition']['certificate_coordinate'], len(raw))
            self.assertLessEqual(result['progress']['full_discoveries'], len(support))
            self.assertEqual(ledger['phases']['decode'].get('green_seed_addition', 0), len(support)*len(raw))
            self.assertNotIn('fallback', ledger['phases'])
            self.assertEqual(ledger['total_units'], cold + attempt + 4*n + 3*len(support))
        else:
            self.assertIsNone(result['support'])
            n, l = len(raw), len(raw).bit_length()-1
            fallback = ledger['phases']['fallback']
            self.assertEqual(fallback['ntt_butterfly'], n*l//2)
            self.assertEqual(fallback['field_mul'], n*l//2)
            self.assertEqual(fallback['field_add'], n*l)
            self.assertEqual(fallback['ntt_finished'], 1)
            self.assertEqual(fallback['fallback_dispatch'], 1)
            kernel = 13*n*l//2 + 9*n + l + 1
            self.assertEqual(sum(fallback.values()), 1 + kernel)
            self.assertEqual(ledger['total_units'], cold + attempt + 1 + kernel + 4*n)
            if result['route'] == 'FALLBACK_CAP':
                self.assertGreater(result['progress']['observed_support_lower_bound'], cap)
                self.assertLessEqual(result['progress']['full_discoveries'], cap+1)
        type(self).cases += 1
        type(self).output_coordinates += len(raw)
        type(self).routes[result['route']] = type(self).routes.get(result['route'], 0) + 1
        return result

    def test_01_small_cartesian_raw_inputs(self):
        # Exhaustive over a declared finite alphabet, not over F_P^4.
        for raw in itertools.product((0, 1, P-1), repeat=4):
            for a in (1, 3):
                for beta in range(4):
                    for cap in range(3):
                        self.checked(raw, 2, cap, a=a, beta=beta)

    def test_02_sparse_dense_late_and_disjoint(self):
        rng = random.Random(7007)
        for q, m in ((8, 2), (16, 4), (32, 4), (64, 8), (128, 8), (256, 16)):
            k = q//m
            for a, beta in ((1, 0), (q-1, q-1), (3, q//2)):
                fixtures = [({},)*k,
                    tuple({0: rng.randrange(1, P)} for _ in range(k)),
                    tuple({b % m: b+1} for b in range(k)),
                    tuple({} if b < k-1 else {m-1: 123} for b in range(k)),
                    tuple({0: b+1} if b < k-1 else {0: b+1, m-1: 7} for b in range(k)),
                    tuple({j: rng.randrange(1, P) for j in range(m)} for _ in range(k))]
                for coefficients in fixtures:
                    raw = synthesize(q, m, coefficients, a, beta)
                    r = len(exact_support(raw, m, a, beta, root_for(q)))
                    for cap in sorted({0, max(0, r-1), r, m}):
                        result = self.checked(raw, m, cap, a=a, beta=beta,
                                              attempt_budget=10**8)
                        self.assertEqual(result['route'], 'GREEN_ACCEPT' if r <= cap else 'FALLBACK_CAP')
                raw = [rng.randrange(P) for _ in range(q)]
                for cap in (0, 1, m):
                    self.checked(raw, m, cap, a=a, beta=beta)

    def test_03_every_small_budget_prefix(self):
        q, m = 8, 2
        raw = synthesize(q, m, ({0: 3}, {0: 5}, {0: 7}, {0: 11}))
        full = self.checked(raw, m, 1, attempt_budget=10**6)
        required = full['ledger']['attempt_spent']
        for budget in range(required+2):
            result = self.checked(raw, m, 1, attempt_budget=budget)
            self.assertEqual(result['route'], 'GREEN_ACCEPT' if budget >= required else 'FALLBACK_BUDGET')
        self.snapshots.append({'name': 'small_budget_exhaustive', 'required_units': required,
                               'budgets_tested': required+2})

    def test_04_boundary_budgets_and_retained_work(self):
        q, m = 64, 8
        raw = synthesize(q, m, tuple({0: b+1, 7: b+2} for b in range(q//m)))
        full = self.checked(raw, m, 2, attempt_budget=10**7)
        rec = sum(full['ledger']['phases']['recognition'].values())
        total = full['ledger']['attempt_spent']
        budgets = [0, 1, m-1, m, 2*m-1, 2*m, rec-1, rec, rec+1,
                   rec+q, total//2, total-1, total, total+1]
        for budget in sorted(set(budgets)):
            result = self.checked(raw, m, 2, attempt_budget=budget)
            self.assertEqual(result['route'], 'GREEN_ACCEPT' if budget >= total else 'FALLBACK_BUDGET')
            if rec <= budget < total:
                self.assertEqual(result['ledger']['denied_reservation']['phase'], 'decode')
                self.assertEqual(result['progress']['completed_blocks'], q//m)
        # A second call cannot inherit roots/counters/certificates from the first.
        repeated = self.checked(raw, m, 2, attempt_budget=10**7)
        self.assertEqual(full, repeated)
        self.snapshots += [{'name': 'accepted_two_modes', 'result_without_values':
                            {k:v for k,v in full.items() if k != 'values'}},
                           {'name': 'late_decode_budget', 'result_without_values':
                            {k:v for k,v in self.checked(raw,m,2,attempt_budget=total-1).items() if k != 'values'}}]

    def test_05_supplied_root_and_orientation(self):
        q, m = 32, 4
        raw = list(range(q))
        primitive = root_for(q)
        for exponent in (1, 3, 7, 31):
            root = pow(primitive, exponent, P)
            self.checked(raw, m, 0, root=root)
            self.checked(raw, m, m, root=root, attempt_budget=10**7)

    def test_06_invalid_domain_is_not_fallback(self):
        bad = [([0]*3, 2, 0, {}), ([0]*12, 2, 0, {}), ([0]*16, 1, 0, {}),
               ([0]*16, 3, 0, {}), ([0]*16, 8, 0, {}), ([0]*16, 4, -1, {}),
               ([0]*16, 4, 5, {}), ([0]*16, 4, 1, {'a': 2}),
               ([0]*16, 4, 1, {'a': 17}), ([0]*16, 4, 1, {'beta': -1}),
               ([0]*16, 4, 1, {'root': 1}), ([0]*16, 4, 1, {'root': 0}),
               ([0]*16, 4, 1, {'root': P}), ([0]*16, 4, 1, {'root': root_for(8)}),
               ([False]+[0]*15, 4, 1, {}), ([-1]+[0]*15, 4, 1, {}),
               ([P]+[0]*15, 4, 1, {}), ([0.0]+[0]*15, 4, 1, {}),
               ([0]*16, True, 1, {}), ([0]*16, 4, True, {}),
               ([0]*16, 4, 1, {'attempt_budget': -1}),
               ([0]*16, 4, 1, {'attempt_budget': True})]
        for raw, m, cap, kwargs in bad:
            with self.assertRaises(ContractError) as caught:
                transform(raw, m, cap, **kwargs)
            self.assertNotIn('fallback', caught.exception.ledger.get('phases', {}))
        class ForbiddenList(list):
            def __len__(self):
                raise AssertionError('must not execute custom input methods')
        with self.assertRaises(ContractError):
            transform(ForbiddenList(), 2, 0)

    def test_07_fallback_ignores_partial_output(self):
        q, m = 16, 4
        late = synthesize(q,m,({0:1},{0:2},{0:3},{0:4,3:5}))
        result = self.checked(late,m,1,attempt_budget=10**6)
        self.assertEqual(result['route'],'FALLBACK_CAP')
        self.assertEqual(result['progress']['completed_blocks'],3)
        self.assertEqual(result['progress']['full_discoveries'],2)
        self.snapshots.append({'name':'late_cap_rejection','result_without_values':
                              {k:v for k,v in result.items() if k != 'values'}})


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(AdapterTests)
    outcome = unittest.TextTestRunner(verbosity=2).run(suite)
    report = {'status': 'PASS' if outcome.wasSuccessful() else 'FAIL',
              'test_methods': outcome.testsRun, 'failures': len(outcome.failures),
              'errors': len(outcome.errors), 'checked_transform_calls': AdapterTests.cases,
              'exact_output_coordinates': AdapterTests.output_coordinates,
              'routes': AdapterTests.routes, 'snapshots': AdapterTests.snapshots,
              'historical_program_execution': False,
              'oracle': 'independent direct finite-field DFT definition',
              'source_sha256': hashlib.sha256(Path(__file__).with_name('alg007_bounded_adapter.py').read_bytes()).hexdigest(),
              'test_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    Path(__file__).with_name('CHECK_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
    if not outcome.wasSuccessful():
        raise SystemExit(1)
