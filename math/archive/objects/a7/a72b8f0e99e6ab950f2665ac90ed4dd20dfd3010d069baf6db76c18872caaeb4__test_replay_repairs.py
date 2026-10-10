from collections import deque
import unittest
import numpy as np
from projected_fourier import ProjectedFourierState
from multi_view import SharedProjectedFourierStore


class Counted(deque):
    visits = 0
    def __iter__(self):
        for v in super().__iter__():
            self.visits += 1
            yield v
    def __reversed__(self):
        for v in super().__reversed__():
            self.visits += 1
            yield v


class Repairs(unittest.TestCase):
    def test_single_state_reads_only_unread_tail(self):
        s = ProjectedFourierState(32, [0, 3], np.ones((4, 2)))
        for _ in range(10000): s.add_coefficient(0, .125)
        s.query()
        s.events = Counted(s.events)
        s.add_coefficient(0, 1)
        np.testing.assert_allclose(s.query(), [1251, 1251])
        self.assertEqual(s.events.visits, 1)

    def test_many_consumer_tail_and_dormant_view(self):
        s = SharedProjectedFourierStore(32, [0, 3], np.ones((4, 2)),
                                        {'hot': [3], 'cold': [0, 3]}, promote_after=None)
        for _ in range(10000): s.add_coefficient(0, .125)
        s.query('hot')
        s.events = Counted(s.events)
        s.add_coefficient(0, 1)
        np.testing.assert_allclose(s.query('hot'), [1251])
        self.assertEqual(s.events.visits, 1)
        np.testing.assert_allclose(s.query('cold'), [1251, 1251])

    def test_chronological_replay(self):
        for shared in (False, True):
            proj = np.ones((4, 1))
            s = (SharedProjectedFourierStore(8, [0], proj, {'v': [0]}, coefficients=[1e16,0,0,0])
                 if shared else ProjectedFourierState(8, [0], proj, coefficients=[1e16,0,0,0]))
            s.add_coefficient(0, -1e16)
            s.add_coefficient(0, 1)
            got = s.query('v') if shared else s.query()
            np.testing.assert_array_equal(got, [1])

    def test_evicted_history_batch_cost_uses_rebuild(self):
        s = SharedProjectedFourierStore(32, [0, 3], np.ones((8, 2)),
                                        {'a': [0,3], 'b': [0,3]}, event_capacity=0)
        s.add_coefficient(0, 2)
        out = s.query_many(['a','b'])
        self.assertEqual(s.views['a'].strategy, 'batch_rebuild')
        for value in out.values(): np.testing.assert_allclose(value, [2, 2])

    def test_event_storage_is_charged_and_compacts(self):
        s = SharedProjectedFourierStore(8, [0], np.ones((1, 1)), {'v': [0]}, promote_after=None)
        initial = s.storage_bytes
        for _ in range(100): s.add_coefficient(0, 1)
        self.assertEqual(s.storage_bytes-initial, 3200)
        s.query('v'); s.compact()
        self.assertEqual(s.storage_bytes, initial)
        self.assertEqual(s.storage_report()['event_numeric_bytes'], 0)


if __name__ == '__main__': unittest.main()
