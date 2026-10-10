import collections
import unittest
import numpy as np
from multi_view import SharedProjectedFourierStore
from view_optimizer import AdaptiveSpectralOrganizer


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


class TestOptimizerHardening(unittest.TestCase):
    def make(self, consumers=2, q=1, rank=4):
        views = {str(i): list(range(q)) for i in range(consumers)}
        st = SharedProjectedFourierStore(max(8,q), list(range(q)),
                np.ones((rank,q)), views, promote_after=None)
        org = AdaptiveSpectralOrganizer(st, min_history=2,
                replan_every=100000, replan_min_updates=100000)
        for history in org.history.values(): history.extend([0,1])
        org.replan()
        self.assertEqual(len(org.groups), 1)
        return st, org

    def test_group_replay_inspects_only_missing_suffix(self):
        st, org = self.make()
        for _ in range(10000): org.add_coefficient(0, 1)
        org.query('0')
        st.events = CountDeque(st.events)
        org.add_coefficient(0, 1)
        self.assertEqual(org.query('0')[0], 10001)
        self.assertLessEqual(st.events.visited, 2)
        self.assertEqual(next(iter(org.groups.values())).strategy, 'group_replay')

    def test_group_suffix_replay_preserves_chronological_order(self):
        st, org = self.make()
        for delta in (1e16, -1e16, 1): org.add_coefficient(0, delta)
        self.assertEqual(org.query('0')[0], 1)
        self.assertEqual(next(iter(org.groups.values())).strategy, 'group_replay')

    def test_group_cache_hit_publishes_only_requested_member(self):
        st, org = self.make(consumers=32, q=8)
        org.add_coefficient(0, 2)
        org.query('0')
        old = {name: view.cached for name, view in st.views.items()}
        got = org.query('0')
        replaced = [name for name in st.views if st.views[name].cached is not old[name]]
        self.assertEqual(replaced, ['0'])
        np.testing.assert_array_equal(got, np.full(8, 2))
        got[:] = 12345
        np.testing.assert_array_equal(org.query('0'), np.full(8, 2))
        np.testing.assert_array_equal(org.query('31'), np.full(8, 2))


if __name__ == '__main__': unittest.main()
