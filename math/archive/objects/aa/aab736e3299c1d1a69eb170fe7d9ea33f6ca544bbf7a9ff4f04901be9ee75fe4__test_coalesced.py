import gc
import unittest
import weakref
import numpy as np

from coalesced_projected import CoalescedProjectedFourier, modular_phase
from vendor.projected_fourier import ProjectedFourierState


class CoalescedTests(unittest.TestCase):
    def check_fft(self, state, basis, **kwargs):
        dense = state.coefficients @ basis
        for j, value in state.sparse.items():
            dense[j] += value
        expected = np.fft.fft(dense)[state.bins]
        np.testing.assert_allclose(state.query(), expected, rtol=3e-11, atol=3e-10, **kwargs)

    def test_all_bins_random_mixed_updates(self):
        rng = np.random.default_rng(281)
        n, r = 64, 5
        basis = rng.normal(size=(r, n)) + 1j*rng.normal(size=(r, n))
        bins = rng.permutation(n)
        state = CoalescedProjectedFourier(n, bins, np.fft.fft(basis, axis=1)[:, bins])
        for t in range(2000):
            if t % 3:
                state.add_point(int(rng.integers(n)), complex(*rng.normal(size=2)))
            else:
                state.add_coefficient(int(rng.integers(r)), complex(*rng.normal(size=2)))
            if t % 37 == 0:
                self.check_fft(state, basis)
        self.check_fft(state, basis)

    def test_repeated_keys_cost_depends_on_distinct_changes(self):
        n = 128
        basis = np.arange(n, dtype=float)[None, :].astype(complex)
        bins = np.array([0, 1, 7, 127])
        state = CoalescedProjectedFourier(n, bins, np.fft.fft(basis)[:, bins])
        for _ in range(20000):
            state.add_coefficient(0, 0.125)
            state.add_point(3, 0.25j)
        self.assertEqual(len(state.pending), 2)
        self.check_fft(state, basis)
        self.assertEqual(state.last_stats.pending_keys, 2)
        self.assertEqual(state.last_stats.strategy, "coalesced")
        self.assertEqual(len(state.pending), 0)

    def test_exact_cancellation_removes_entries_during_updates(self):
        state = CoalescedProjectedFourier(16, [0, 3], np.ones((1, 2), complex))
        for _ in range(10000):
            state.add_coefficient(0, 0.125)
            state.add_point(2, -0.5j)
            state.add_coefficient(0, -0.125)
            state.add_point(2, 0.5j)
        self.assertEqual(state.pending, {})
        self.assertEqual(state.sparse, {})
        np.testing.assert_array_equal(state.query(), np.zeros(2))
        self.assertEqual(state.last_stats.strategy, "cached")

    def test_long_history_not_retained_or_scanned(self):
        state = CoalescedProjectedFourier(8, [0], np.ones((1, 1), complex))
        for _ in range(20000):
            state.add_coefficient(0, 0.125)
            state.query()
            self.assertFalse(state.pending)
        self.assertFalse(hasattr(state, "events"))
        self.assertEqual(state.last_stats.pending_keys, 1)
        np.testing.assert_array_equal(state.query(), [2500])

    def test_rebuild_reclaims_many_deleted_points(self):
        n = 4096
        state = CoalescedProjectedFourier(n, [0, 1, n-1], np.empty((0, 3)), sparse_residual=((j, 1) for j in range(n)))
        for j in range(n):
            state.add_point(j, -1)
        self.assertEqual(len(state.pending), n)
        self.assertEqual(len(state.sparse), 0)
        np.testing.assert_array_equal(state.query(), np.zeros(3))
        self.assertEqual(state.last_stats.strategy, "rebuild")
        self.assertEqual(state.last_stats.reclaimed_keys, n)
        self.assertFalse(state.pending)

    def test_cancellation_shrinks_pending_tombstones_before_query(self):
        import sys
        state = CoalescedProjectedFourier(8192, [0], np.empty((0, 1)))
        for j in range(8192):
            state.add_point(j, 1)
        large_bytes = sys.getsizeof(state.pending)
        for j in range(8191):
            state.add_point(j, -1)
        self.assertEqual(len(state.pending), 1)
        self.assertLessEqual(state._pending_high_water, 4)
        self.assertLess(sys.getsizeof(state.pending), large_bytes/16)
        state.add_point(8191, -1)
        self.assertEqual(state._pending_high_water, 0)
        self.assertEqual(sys.getsizeof(state.pending), sys.getsizeof({}))
        np.testing.assert_array_equal(state.query(), [0])

    def test_duplicate_bins_zero_rank_and_one_bin(self):
        for bins in ([5], [7, 0, 7, 2, 2], list(range(8))):
            state = CoalescedProjectedFourier(8, bins, np.empty((0, len(bins))), sparse_residual=[(1, 2), (1, -1)])
            state.add_point(7, 3-2j)
            self.check_fft(state, np.empty((0, 8), complex))
            state.add_point(1, -1)
            self.check_fft(state, np.empty((0, 8), complex))

    def test_projection_owns_memory_and_does_not_pin_full_fft(self):
        full = np.ones((1, 8192), complex)
        projection = full[:, :4]
        self.assertTrue(projection.flags.c_contiguous)
        owner = weakref.ref(full)
        state = CoalescedProjectedFourier(8192, [0, 1, 2, 3], projection)
        self.assertTrue(state.projection.flags.owndata)
        self.assertFalse(np.shares_memory(state.projection, full))
        del projection, full
        gc.collect()
        self.assertIsNone(owner())

    def test_input_and_output_buffers_are_independent(self):
        bins = np.array([0, 1])
        p = np.ones((1, 2), complex)
        c = np.ones(1, complex)
        state = CoalescedProjectedFourier(4, bins, p, c)
        bins[:] = 3
        p[:] = 99
        c[:] = 99
        answer = state.query()
        answer[:] = 0
        np.testing.assert_array_equal(state.query(), [1, 1])
        np.testing.assert_array_equal(state.bins, [0, 1])

    def test_snapshot_discards_sub_ulp_no_op(self):
        p = np.ones((2, 1), complex)
        c = np.array([1e16, -1e16], complex)
        state = CoalescedProjectedFourier(1, [0], p, c)
        original = ProjectedFourierState(1, [0], p, c)
        state.add_coefficient(0, 1)
        original.add_coefficient(0, 1)
        np.testing.assert_array_equal(state.query(), [0])
        np.testing.assert_array_equal(original.query(), [1])
        self.assertFalse(state.pending)

    def test_disclosed_cancellation_limit_and_explicit_rebase(self):
        # This is a LIMITATION regression, not a claim of numerical agreement:
        # (1 - 1e16) rounds to -1e16, losing the final unit on cached replay.
        state = CoalescedProjectedFourier(1, [0], np.ones((1, 1)), [1e16])
        state.add_coefficient(0, -1e16)
        state.add_coefficient(0, 1)
        self.assertEqual(state.coefficients[0], 1)
        np.testing.assert_array_equal(state.query(), [0])
        np.testing.assert_array_equal(state.rebase(), [1])

    def test_modular_phase_high_indices_matches_fft(self):
        n = 1 << 20
        bins = np.array([0, 1, n-1, n-2, n//2, n-1])
        x = np.zeros(n, complex)
        x[n-1] = 1
        state = CoalescedProjectedFourier(n, bins, np.empty((0, len(bins))))
        state.add_point(n-1, 1)
        np.testing.assert_allclose(state.query(), np.fft.fft(x)[bins], atol=2e-15, rtol=2e-15)

    def test_modular_phase_overflow_guard(self):
        n = (1 << 62) - 57
        j = n-1
        bins = np.array([n-1, n-2, 0, 1], dtype=np.int64)
        expected = np.exp(-2j*np.pi*np.array([1, 2, 0, n-1], dtype=float)/n)
        np.testing.assert_array_equal(modular_phase(n, bins, j), expected)
        state = CoalescedProjectedFourier(n, bins, np.empty((0, len(bins))), prepared_positions=[j])
        state.add_point(j, 1)
        np.testing.assert_array_equal(state.query(), expected)

    def test_prepared_and_unprepared_phases_match(self):
        n = 257
        bins = np.array([0, 1, 100, 256, 1])
        a = CoalescedProjectedFourier(n, bins, np.empty((0, len(bins))))
        b = CoalescedProjectedFourier(n, bins, np.empty((0, len(bins))), prepared_positions=[0, 1, 256, 256])
        for j in (0, 1, 256):
            a.add_point(j, 0.3-0.7j)
            b.add_point(j, 0.3-0.7j)
        np.testing.assert_array_equal(a.query(), b.query())

    def test_rebase_matches_fresh_relation(self):
        rng = np.random.default_rng(69)
        basis = rng.normal(size=(4, 32)) + 1j*rng.normal(size=(4, 32))
        bins = [1, 2, 29, 31]
        state = CoalescedProjectedFourier(32, bins, np.fft.fft(basis)[:, bins])
        for i in range(1000):
            state.add_coefficient(i % 4, complex(*rng.normal(size=2)))
            state.query()
        state.add_point(31, 0.375j)
        got = state.rebase()
        self.assertEqual(state.last_stats.strategy, "explicit_rebase")
        np.testing.assert_array_equal(got, state._rebuild_value())
        self.check_fft(state, basis)

    def test_invalid_shape_bounds_and_zero_edits(self):
        for n, bins, p in [(0, [0], np.empty((0, 1))), (4, [], np.empty((0, 0))), (4, [4], np.empty((0, 1))), (4, [0], np.empty((2, 2)))]:
            with self.assertRaises(ValueError):
                CoalescedProjectedFourier(n, bins, p)
        state = CoalescedProjectedFourier(4, [0], np.ones((1, 1)))
        with self.assertRaises(ValueError):
            state.add_point(4, 1)
        with self.assertRaises(ValueError):
            state.add_coefficient(-1, 1)
        state.add_point(0, 0)
        state.add_coefficient(0, 0)
        self.assertEqual(state.pending, {})


if __name__ == "__main__":
    unittest.main()
