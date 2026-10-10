import copy
import itertools
import math
import unittest
from unittest.mock import patch

import numpy as np
from scipy import fft
from projected_circuit import ProjectedCircuit
from modular_bridge import replay, primitive_root, dft, circular, integer_product


class CircuitTests(unittest.TestCase):
    def test_real_and_complex_registration(self):
        rng = np.random.default_rng(88)
        for n in (1, 2, 17, 32, 63):
            bins = sorted(set([0, n//2, n-1]))
            for complex_input in (False, True):
                x = rng.normal(size=n)
                if complex_input:
                    x = x+1j*rng.normal(size=n)
                e = ProjectedCircuit(n, bins)
                np.testing.assert_allclose(e.query(e.register(x)), fft.fft(x)[bins], atol=2e-12)

    def test_pruned_registration(self):
        rng = np.random.default_rng(17)
        x = rng.normal(size=128)+1j*rng.normal(size=128)
        e = ProjectedCircuit(128, [1, 2, 63, 127], registration='pruned', radix=16)
        node = e.register(x)
        np.testing.assert_allclose(e.query(node), fft.fft(x)[e.bins], atol=2e-11)
        self.assertGreater(e.memory_report()['registration_plan_bytes'], 0)
        e.release_registration_plan()
        self.assertEqual(e.memory_report()['registration_plan_bytes'], 0)

    def test_mixed_circuit_against_dense(self):
        rng = np.random.default_rng(812)
        for n in (15, 32, 97):
            ks = sorted(set([0, 3, n//2, n-1]))
            e = ProjectedCircuit(n, ks)
            a, b, c = rng.normal(size=(3, n))/n
            an, bn, cn = map(e.register, (a, b, c))
            r = e.relation([(an, 2-1j, 4), (bn, -.5, -2)], [(3, .25j), (3, -.1j)])
            rtime = (2-1j)*np.roll(a, 4)-.5*np.roll(b, -2)
            rtime[3] += .15j
            node = e.add(e.convolve(r, cn), e.shift(bn, 7))
            actual = e.query(node, ks+ks[:1])
            expected = (fft.fft(rtime)*fft.fft(c)+fft.fft(np.roll(b, 7)))[ks+ks[:1]]
            np.testing.assert_allclose(actual, expected, atol=1e-12)

    def test_persistence_random_branching_and_zeros(self):
        rng = np.random.default_rng(411)
        n, m = 32, 13
        x = rng.normal(size=(m, n))*.005
        x[:, 0] += 1
        x[1] = np.ones(n)  # many zero Fourier values: no inverse allowed
        e = ProjectedCircuit(n, range(n), cache_bytes=30000)
        base = e.product(map(e.register, x))
        records = [(base, x.copy())]
        for _ in range(40):
            source, xx = records[int(rng.integers(len(records)))]
            xx = xx.copy()
            at, pos = int(rng.integers(m)), int(rng.integers(n))
            delta = float(rng.normal()*.01)
            newer = source.edit(at, pos, delta)
            xx[at, pos] += delta
            expected = np.prod(fft.fft(xx, axis=1), axis=0)
            np.testing.assert_allclose(newer.frequencies(), expected, rtol=3e-12, atol=3e-12)
            records.append((newer, xx))
        np.testing.assert_allclose(base.frequencies(), np.prod(fft.fft(x, axis=1), axis=0), atol=1e-12)

    def test_many_edits_rebuild_only_union_of_paths(self):
        m, n = 64, 64
        e = ProjectedCircuit(n, [0, 3, 7])
        nodes = [e.register_projection([1+i*.001]*3) for i in range(m)]
        old = e.product(nodes)
        old.frequencies()
        for p in (1, 2, 4, 16, 64):
            keys = list(range(0, m, m//p))
            changes = {i: e.scale(nodes[i], 1.01) for i in keys}
            updated = old.replace_many(changes)
            before = e.stats['new_nodes']
            out = updated.frequencies()
            # p leaves plus sum min(2^d,p) internal ancestors.
            bound = p+sum(min(2**d, p) for d in range(int(math.log2(m))))
            self.assertLessEqual(e.stats['last_evaluated_nodes'], bound)
            np.testing.assert_allclose(out, old.frequencies()*1.01**p, rtol=1e-12)
            self.assertEqual(before, e.stats['new_nodes'])

    def test_cache_disabled_bounded_and_return_isolation(self):
        for budget in (0, 64, 128, 20000):
            e = ProjectedCircuit(16, [0, 1, 2, 3], cache_bytes=budget)
            a = e.register(np.arange(16)/16)
            shared = e.add(a, e.impulse(3, .1))
            roots = [e.convolve(shared, shared), e.add(shared, a)]
            first = e.query_many(roots)
            second = e.query_many(roots)
            for x, y in zip(first, second):
                np.testing.assert_allclose(x, y)
            first[0][:] = 0
            np.testing.assert_allclose(e.query(roots[0]), second[0])
            self.assertLessEqual(e.memory_report()['cache_bytes'], budget)

    def test_fused_roots_avoid_shared_work_with_no_cache(self):
        e = ProjectedCircuit(8, [0, 1], cache_bytes=0)
        a = e.register_projection([2, 3])
        shared = e.add(a, e.impulse(1))
        roots = [e.scale(shared, 2), e.convolve(shared, shared)]
        fused = e.query_many(roots)
        work = e.stats['last_evaluated_nodes']
        separate_work = 0
        for root, expected in zip(roots, fused):
            np.testing.assert_allclose(e.query(root), expected)
            separate_work += e.stats['last_evaluated_nodes']
        self.assertLess(work, separate_work)

    def test_deep_dag_is_iterative(self):
        e = ProjectedCircuit(8, [0, 1])
        node = e.register_projection([1, 1])
        for _ in range(2500):
            node = e.scale(node, 1.00001)
        np.testing.assert_allclose(e.query(node), [1.00001**2500]*2)
        self.assertEqual(len(e.export([node])['nodes']), 2501)

    def test_metadata_adapter_keeps_multiple_bases(self):
        from baseline_phase7.cost_aware_fft import RelationFFT
        upstream = RelationFFT()
        a = upstream.register(np.arange(32)/32)
        b = upstream.register(np.sin(np.arange(32)))
        composite = a.shift(3)
        composite.terms.update(b.terms)
        composite.edit(7, .125)
        expected = fft.fft(composite.signal())
        e = ProjectedCircuit(32, [0, 3, 17, 31])
        with patch.object(type(composite), 'signal', side_effect=AssertionError('must not materialize')):
            node, other = e.from_phase5([composite, a])
        np.testing.assert_allclose(e.query(node), expected[e.bins], atol=1e-11)
        self.assertEqual(e.memory_report()['basis_count'], 2)
        self.assertEqual(e.memory_report()['basis_projection_bytes'], 128)

    def test_no_dense_input_retention(self):
        import weakref, gc
        x = np.arange(64, dtype=float)
        ref = weakref.ref(x)
        e = ProjectedCircuit(64, [0, 1])
        node = e.register(x)
        del x
        gc.collect()
        self.assertIsNone(ref())
        self.assertEqual(e.memory_report()['basis_projection_bytes'], 32)

    def test_invalid_inputs(self):
        for bins in ([1.5], [True], [-1], [8], [1, 1], []):
            with self.assertRaises((ValueError, TypeError)):
                ProjectedCircuit(8, bins)
        e = ProjectedCircuit(8, [0, 1])
        a = e.register_projection([1, 2])
        with self.assertRaises(ValueError): e.scale(a, float('inf'))
        with self.assertRaises(ValueError): e.query(a, [2])
        with self.assertRaises(ValueError): e.add(a, ProjectedCircuit(8, [0, 1]).impulse())
        with self.assertRaises(TypeError): e.product([a]).replace_many({.5: a})
        with self.assertRaises(ValueError): e.register(np.ones(7))
        with self.assertRaises(FloatingPointError): e.query(e.scale(e.scale(a, 1e300), 1e300))


class ExactTests(unittest.TestCase):
    def test_export_replays_over_four_fields(self):
        rng = np.random.default_rng(717)
        n = 8
        for p in (17, 97, 193, 257):
            w = primitive_root(p, n)
            for trial in range(50):
                a, b, c = rng.integers(-3, 4, size=(3, n)).tolist()
                e = ProjectedCircuit(n, range(n))
                an, bn, cn = [e.register_projection(np.zeros(n)) for _ in range(3)]
                relation = e.relation([(an, 2, 3), (bn, -1, 0)], [(4, 3)])
                product = e.product([relation, cn, an])
                branch = product.edit(1, 2, -2)
                out = e.add(branch.root, e.shift(bn, -3))
                ar = [2*a[(j-3) % n]-b[j]+(3 if j == 4 else 0) for j in range(n)]
                cc = c[:]; cc[2] -= 2
                time = circular(circular(ar, cc), a)
                time = [v+b[(j+3) % n] for j, v in enumerate(time)]
                schedule = e.export([out])
                got = replay(schedule, {0: a, 1: b, 2: c}, p, w)[0]
                self.assertEqual(got, dft(time, range(n), w, p))
                if trial == 0:
                    bad = copy.deepcopy(schedule)
                    for row in bad['nodes']:
                        if row['op'] == 'scale': row['data'][0] += 1; break
                    self.assertNotEqual(replay(bad, {0: a, 1: b, 2: c}, p, w)[0], got)

    def test_exact_integer_bridge(self):
        import random
        r = random.Random(112)
        for bits in (0, 1, 8, 24, 64, 100):
            for _ in range(12):
                a, b = r.getrandbits(bits), -r.getrandbits(bits)
                got, cert = integer_product(a, b)
                self.assertEqual(got, a*b)
                self.assertGreater(cert['crt_modulus'], cert['coefficient_bound'])
        self.assertEqual(integer_product(-987654321, -123456789)[0], 987654321*123456789)

    def test_noninteger_modular_scale_rejected(self):
        e = ProjectedCircuit(8, [0, 1])
        for c in (.5, 1j):
            with self.assertRaises(ValueError):
                replay(e.export([e.impulse(0, c)]), {}, 17)


if __name__ == '__main__':
    unittest.main()
