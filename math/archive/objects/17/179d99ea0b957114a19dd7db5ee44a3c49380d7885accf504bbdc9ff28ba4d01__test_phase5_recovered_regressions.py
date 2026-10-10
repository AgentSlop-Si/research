import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
from scipy import fft

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import cost_aware_fft as m


class SpectrumOnlyTests(unittest.TestCase):
    def test_auto_preserves_reference_for_native_recommendation_shapes(self):
        for n, k in [(7, 1), (8, 1), (16384, 3), (65536, 4)]:
            with self.subTest(n=n, k=k):
                x = np.arange(n, dtype=float) / n
                changes = [(j, .25 * (j + 1)) for j in range(k)]
                edited = x.copy()
                for p, d in changes:
                    edited[p] += d
                got = m.sparse_from_known_changes(fft.rfft(x), n, changes, 'auto')
                np.testing.assert_allclose(got, fft.rfft(edited), rtol=3e-11, atol=1e-9)

    def test_original_dc_regression(self):
        got = m.sparse_from_known_changes(fft.rfft(np.arange(8.)), 8,
                                          [(1, 2.)], 'auto')
        self.assertEqual(got[0], 30)

    def test_no_forward_or_inverse_reconstruction(self):
        z = fft.rfft(np.arange(8.))
        with patch.object(m._fft, 'rfft', side_effect=AssertionError('hidden forward FFT')):
            with patch.object(m._fft, 'irfft', side_effect=AssertionError('hidden inverse FFT')):
                self.assertEqual(m.sparse_from_known_changes(z, 8, [(1, 2)], 'auto')[0], 30)
        with self.assertRaises(ValueError):
            m.sparse_from_known_changes(z, 8, [(1, 2)], 'native')

    def test_zero_and_cancelled_edits(self):
        z = fft.rfft(np.arange(8.))
        for changes in [[], [(1, 2), (1, -2)]]:
            np.testing.assert_array_equal(m.sparse_from_known_changes(z, 8, changes, 'auto'), z)


class BudgetTests(unittest.TestCase):
    def test_calibration_skips_overbudget_pruned(self):
        e = m.RelationFFT(max_temp_bytes=256)
        state = e.register(np.arange(16.)).edit(3, 1.)
        prof = e.calibrate(state, repeats=2)
        self.assertNotIn('pruned', prof.median_seconds)
        self.assertIn(prof.best_method, ('native', 'direct'))

    def test_calibration_skips_backend_allocation_failure(self):
        e = m.RelationFFT()
        state = e.register(np.arange(16.)).edit(3, 1.)
        with patch.object(e, '_pruned_spectrum', side_effect=MemoryError('backend workspace')):
            prof = e.calibrate(state, repeats=2)
        self.assertNotIn('pruned', prof.median_seconds)
        self.assertEqual(e.stats['calibration_pruned_memory_skips'], 1)

    def test_calibration_does_not_hide_nonmemory_errors(self):
        e = m.RelationFFT()
        state = e.register(np.arange(16.)).edit(3, 1.)
        with patch.object(e, '_pruned_spectrum', side_effect=ValueError('invalid transform')):
            with self.assertRaises(ValueError):
                e.calibrate(state, repeats=2)

    def test_admission_and_execution_share_estimate(self):
        e = m.RelationFFT()
        state = e.register(np.arange(16.)).edit(3, 1.)
        needed = e._pruned_required_bytes(state)
        e.max_temp_bytes = needed - 1
        with self.assertRaises(MemoryError):
            state.spectrum('pruned')
        prof = e.calibrate(state, repeats=2)
        self.assertNotIn('pruned', prof.median_seconds)
        e.max_temp_bytes = needed
        prof = e.calibrate(state, repeats=2)
        self.assertIn('pruned', prof.median_seconds)

    def test_old_incomplete_pruned_budget_is_rejected(self):
        n, k = 65536, 8
        e = m.RelationFFT(max_temp_bytes=16*n + 8*(n//k))
        s = e.register(np.zeros(n))
        for p in range(k):
            s.edit(p+1, p+.25)
        with self.assertRaises(MemoryError):
            s.spectrum('pruned')

    def test_phase_backing_storage_not_visible_slice_is_charged(self):
        n, count = 4096, 2049
        e = m.RelationFFT(max_phase_bytes=count*16)
        phase = e._phase_vector(n, 7, count)
        self.assertEqual(phase.nbytes, 32784)
        self.assertEqual(m._retained_array_bytes(phase), 49152)
        self.assertEqual(e.memory_report()['internal_phase_cache_bytes'], 0)
        self.assertEqual(len(e._phase), 0)

    def test_phase_lru_charges_real_bytes_on_insert_and_evict(self):
        e = m.RelationFFT(max_phase_bytes=49152)
        for p in [7, 9, 11, 7]:
            phase = e._phase_vector(4096, p, 2049)
            self.assertEqual(len(e._phase), 1)
            actual = sum(m._retained_array_bytes(a) for a in e._phase.values())
            self.assertEqual(actual, e.memory_report()['internal_phase_cache_bytes'])
            self.assertLessEqual(actual, e.max_phase_bytes)
            self.assertFalse(phase.flags.writeable)


class NormalStateTests(unittest.TestCase):
    def test_shift_combine_edits_queries_forks_and_subscriptions(self):
        self.max_abs_error = 0.
        for n in [1, 2, 3, 7, 8, 16, 31, 64, 128, 1024, 4096, 16384, 65536]:
            with self.subTest(n=n):
                rng = np.random.default_rng(532+n)
                e = m.RelationFFT()
                a, b = rng.normal(size=n), rng.normal(size=n)
                sa, sb = e.register(a), e.register(b)
                sx, ax = sa.fork(), a.copy()
                for _ in range(min(7, n)):
                    p, d = int(rng.integers(n)), float(rng.normal())
                    sx.edit(p, d)
                    ax[p] += d
                shift = int(rng.integers(n))
                sy = e.combine([sx.shift(shift), sb], [1.25, -.75])
                ref = fft.rfft(1.25*np.roll(ax, shift)-.75*b)
                methods = ['direct', 'native', 'auto'] + (['pruned'] if n & (n-1) == 0 else [])
                for method in methods:
                    got = sy.spectrum(method)
                    np.testing.assert_allclose(got, ref, rtol=3e-11, atol=1e-9)
                    self.max_abs_error = max(self.max_abs_error, float(np.max(np.abs(got-ref))))
                qs = sorted(set([0, n//2, min(3, n//2)]))
                np.testing.assert_allclose(sy.bins(qs), ref[qs], rtol=3e-11, atol=1e-9)
                for q in qs:
                    np.testing.assert_allclose(sy.bin(q), ref[q], rtol=3e-11, atol=1e-9)
                cached = sy.spectrum(cache_output=True)
                cached[:] = 0
                np.testing.assert_allclose(sy.spectrum(), ref, rtol=3e-11, atol=1e-9)
                sibling = sy.fork()
                sy.edit(0, .125)
                np.testing.assert_allclose(sy.spectrum(), ref+.125, rtol=3e-11, atol=1e-9)
                np.testing.assert_allclose(sibling.spectrum(), ref, rtol=3e-11, atol=1e-9)
                tracked, xt = m.subscribe(sx, qs), ax.copy()
                for _ in range(30):
                    p, d = int(rng.integers(n)), float(rng.normal())
                    tracked.edit(p, d)
                    xt[p] += d
                    np.testing.assert_allclose(tracked.values(), fft.rfft(xt)[qs], rtol=3e-11, atol=1e-9)
                tracked.state.edit(0, 1)
                with self.assertRaises(RuntimeError):
                    tracked.values()
        print('\nNormal-state maximum absolute error:', self.max_abs_error)


if __name__ == '__main__':
    unittest.main()
