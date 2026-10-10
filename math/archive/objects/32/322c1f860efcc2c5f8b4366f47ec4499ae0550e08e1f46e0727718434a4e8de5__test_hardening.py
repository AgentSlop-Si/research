import collections
import unittest
import numpy as np
from arbitrary_output import ArbitraryBinsDFTPlan, AutoOutputPlan, ProductiveProjectionPlanner
from multi_view import SharedProjectedFourierStore, union_frequency_sets
from modular_phase import phase_row


class CountDeque(collections.deque):
    visited = 0
    def __iter__(self):
        for row in super().__iter__():
            self.visited += 1
            yield row
    def __reversed__(self):
        for row in super().__reversed__():
            self.visited += 1
            yield row


class TestHardening(unittest.TestCase):
    def test_phase_reduction_cancellation(self):
        n = 65536
        got = ArbitraryBinsDFTPlan(n, [n-1]).execute(np.ones(n))
        self.assertLess(abs(got[0]), 1e-8)

    def test_phase_reduction_above_int64_product(self):
        n = 10**12 + 39
        bins = np.array([0, 1, n//2, n-2, n-1], dtype=np.int64)
        j = n-3
        want = np.array([np.exp(-2j*np.pi*((j*int(k)) % n)/n) for k in bins])
        np.testing.assert_allclose(phase_row(n, j, bins), want, rtol=1e-14, atol=1e-14)
        for prepared in (None, [j]):
            st = SharedProjectedFourierStore(n, bins, np.empty((0, len(bins))),
                                            {'v': bins}, prepared_positions=prepared)
            st.add_point(j, 1)
            np.testing.assert_allclose(st.query('v'), want, rtol=1e-14, atol=1e-14)

    def test_different_or_mutated_calibration_sample(self):
        rng = np.random.default_rng(71)
        a = rng.normal(size=128)
        bins = [0, 17, 127]
        p = AutoOutputPlan(128, bins, sample=a, reps=1)
        b = rng.normal(size=128)
        np.testing.assert_allclose(p.project_stream_with_sample(b, [a])[0], np.fft.fft(b)[bins], atol=1e-9)
        a[:] += 4
        np.testing.assert_allclose(p.project_stream_with_sample(a, [])[0], np.fft.fft(a)[bins], atol=1e-9)

    def test_zero_productive_trials(self):
        p = ProductiveProjectionPlanner(128, [1], max_pruned_trials=0)
        p.project([np.ones(128), np.ones(128)], expected_count=2)
        self.assertEqual(len(p.stats.trials), 1)

    def test_recent_suffix_only(self):
        st = SharedProjectedFourierStore(8, [0], np.ones((2, 1)), {'v': [0]})
        for _ in range(10000): st.add_coefficient(0, 1)
        st.query('v')
        st.events = CountDeque(st.events)
        st.add_coefficient(0, 1)
        self.assertEqual(st.query('v')[0], 10001)
        self.assertLessEqual(st.events.visited, 2)

    def test_replay_preserves_chronological_order(self):
        # A reversed AXPY sequence gives 0 instead of 1 in this example.
        st = SharedProjectedFourierStore(8, [0], np.ones((4, 1)), {'v': [0]})
        for d in (1e16, -1e16, 1): st.add_coefficient(0, d)
        self.assertEqual(st.query('v')[0], 1)

    def test_fusion_accounts_for_lost_history(self):
        st = SharedProjectedFourierStore(8, [0], np.ones((10, 1)), {'a': [0], 'b': [0]}, event_capacity=0)
        st.add_coefficient(0, 1)
        result = st.query_many(['a', 'b'])
        self.assertEqual(result['a'][0], 1)
        self.assertEqual(st.views['a'].strategy, 'batch_rebuild')

    def test_fusion_omits_current_bins(self):
        st = SharedProjectedFourierStore(8, list(range(8)), np.ones((4,8)),
                                        {'a':[0], 'b':[0], 'current':list(range(8))}, event_capacity=0)
        st.add_coefficient(0, 1)
        st.query('current')
        result = st.query_many(['a', 'b', 'current'])
        self.assertEqual(st.views['a'].strategy, 'batch_rebuild')
        np.testing.assert_array_equal(result['current'], np.ones(8))

    def test_projection_owns_compact_storage(self):
        full = np.ones(65536, np.complex128)
        proj = full[:4][None, :]
        st = SharedProjectedFourierStore(65536, [0,1,2,3], proj, {'v':[0]}, [1])
        self.assertTrue(st.projection.flags.owndata)
        full[:] = 100
        st.add_coefficient(0, 1)
        self.assertEqual(st.query('v')[0], 2)

    def test_numeric_payload_counts_events(self):
        st = SharedProjectedFourierStore(8, [0], np.ones((1,1)), {'v':[0]})
        before = st.storage_bytes
        for _ in range(20): st.add_coefficient(0, 1)
        self.assertGreater(st.storage_bytes, before)


if __name__ == '__main__': unittest.main()
