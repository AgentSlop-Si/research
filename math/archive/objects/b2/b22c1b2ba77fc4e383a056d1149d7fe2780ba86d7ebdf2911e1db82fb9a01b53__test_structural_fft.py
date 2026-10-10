"""Regression tests for input-independent FFT graph and tabulated WHT."""
import math
import random
import unittest
import numpy as np
from structural_fft import (
    FFTGraph, CompactSplitRadix, SharedLookupTable, fwht_mod, tabulated_fwht_mod,
    count_nontrivial_twiddles, asymptotic_block_length,
)


class GraphTests(unittest.TestCase):
    def test_fft_against_numpy_all_inputs_complex_random(self):
        rng = np.random.default_rng(20261009)
        for n in [1,2,4,8,16,32,64,128,256]:
            for method in ['radix2','split_radix']:
                graph = FFTGraph(n,method)
                for _ in range(3):
                    a = rng.normal(size=n) + 1j*rng.normal(size=n)
                    actual = np.array(graph.execute(a))
                    expected = np.fft.fft(a)
                    np.testing.assert_allclose(actual,expected,rtol=1e-12,atol=1e-10,
                                               err_msg=f'{method} n={n}')

    def test_compact_template_same_transform_without_expanded_graph(self):
        rng=np.random.default_rng(20261009)
        for n in [1,2,4,8,16,32,64,256,1024]:
            plan=CompactSplitRadix(n)
            full=FFTGraph(n,'split_radix')
            for _ in range(2):
                a=rng.standard_normal(n)+1j*rng.standard_normal(n)
                np.testing.assert_allclose(plan.execute(a), np.fft.fft(a),atol=1e-9)
                np.testing.assert_allclose(plan.execute(a), full.execute(a),atol=1e-9)
            self.assertLessEqual(plan.stats()['twiddle_complex_values'],2*n)

    def test_graph_for_all_zero_ones_impulse_and_reuse(self):
        for method in ('radix2', 'split_radix'):
            for n in (8,16,128):
                graph = FFTGraph(n,method)
                inputs = [np.zeros(n), np.ones(n),np.arange(n),np.eye(n)[n//3]]
                for a in inputs:
                    np.testing.assert_allclose(graph.execute(a), np.fft.fft(a), atol=1e-9)
                # identical precompiled graph is reused for all input arrays
                self.assertEqual(graph.stats()['n'],n)

    def test_complex_twiddle_recurrence_and_gains(self):
        for n in [1,2,4,8,16,32,64,128,256,512,1024,2048]:
            g2 = FFTGraph(n,'radix2')
            gs = FFTGraph(n,'split_radix')
            a=g2.stats()
            b=gs.stats()
            self.assertEqual(a['nontrivial_complex_multiplies'],count_nontrivial_twiddles(n,'radix2'))
            self.assertEqual(b['nontrivial_complex_multiplies'],count_nontrivial_twiddles(n,'split_radix'))
            self.assertEqual(a['complex_add_sub'],int(n*math.log2(n)))
            self.assertEqual(b['complex_add_sub'],int(n*math.log2(n)))
            if n>=16:
                self.assertLess(b['nontrivial_complex_multiplies'],a['nontrivial_complex_multiplies'])

    def test_n_must_be_power_of_two(self):
        with self.assertRaises(ValueError):
            FFTGraph(7)
        with self.assertRaises(ValueError):
            FFTGraph(0)

    def test_original_integer_multiplication(self):
        a=np.array([4,3,2,1,0,0,0,0], dtype=float)
        b=np.array([8,7,6,5,0,0,0,0], dtype=float)
        graph=FFTGraph(8,'split_radix')
        fa=np.array(graph.execute(a))
        fb=np.array(graph.execute(b))
        product=np.fft.ifft(fa*fb)
        np.testing.assert_allclose(product.real, [32,52,61,60,34,16,5,0],atol=1e-10)
        self.assertEqual(sum(int(round(v.real))*10**j for j,v in enumerate(product)),7006652)

    def test_packed_two_distinct_real_ffts(self):
        rng = np.random.default_rng(1009)
        for n in [4,8,32,128]:
            graph = FFTGraph(n, 'split_radix')
            for _ in range(4):
                a=rng.standard_normal(n)
                b=rng.standard_normal(n)
                fa,fb=graph.execute_two_real(a,b)
                np.testing.assert_allclose(fa,np.fft.fft(a),rtol=1e-12,atol=1e-10)
                np.testing.assert_allclose(fb,np.fft.fft(b),rtol=1e-12,atol=1e-10)

class WalshTests(unittest.TestCase):
    def test_tabulated_against_standard_for_random_inputs(self):
        rng = random.Random(20261009)
        for p in (3,5):
            cache = SharedLookupTable(p, max_entries=500_000)
            for n in [1,2,4,8,16,32,64,128,256,1024]:
                for block in [2,4,8]:
                    if p == 5 and block == 8:
                        continue  # 390625-entry table is not needed in tests
                    for _ in range(3):
                        a=[rng.randrange(p) for _ in range(n)]
                        expected=fwht_mod(a,p)
                        got, stats=tabulated_fwht_mod(a,p,block,cache)
                        self.assertEqual(got, expected, f'p={p}, n={n}, block={block}')
                        self.assertEqual(stats['online_field_reads'],stats['n']*stats['passes'])

    def test_linear_identity_every_field_element(self):
        p=3
        table=SharedLookupTable(p)
        t=table.ensure(4)
        self.assertEqual(len(t),p**4)
        for code in range(len(t)):
            x=[]
            c=code
            for _ in range(4):
                x.append(c%p)
                c//=p
            self.assertEqual(list(t[code]), fwht_mod(x,p))

    def test_multipass_and_inversion(self):
        p=5
        cache=SharedLookupTable(p)
        x=[(7*j*j+j+3)%p for j in range(512)]
        y, _=tabulated_fwht_mod(x,p,4,cache)
        z, _=tabulated_fwht_mod(y,p,4,cache)
        inv_n=pow(len(x),-1,p)
        self.assertEqual([(i*inv_n)%p for i in z],x)

    def test_table_is_independent_of_online_values(self):
        cache=SharedLookupTable(3)
        cache.ensure(8)
        before=cache.stats()['total_table_entries']
        for k in range(4):
            tabulated_fwht_mod([k%3]*256,3,8,cache)
        self.assertEqual(cache.stats()['total_table_entries'],before)

    def test_expected_sublinear_table_family(self):
        for L in (16, 32, 64, 128, 256, 1024):
            n=1<<L
            b=asymptotic_block_length(n,3,0.25)
            self.assertTrue(b & (b-1) == 0)
            self.assertLessEqual(b*math.log(3),0.251*L*math.log(2))
            self.assertGreaterEqual(b,2)

if __name__=='__main__':
    unittest.main(verbosity=2)
