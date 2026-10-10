import unittest
import numpy as np

from relation_view import DynamicFourierState


class TestRelationView(unittest.TestCase):
    def setUp(self):
        self.rng = np.random.default_rng(9217)

    def test_dynamic_coefficients_and_points(self):
        n, r = 128, 5
        basis_time = self.rng.standard_normal((r,n)) + 1j*self.rng.standard_normal((r,n))
        basis_spec = np.fft.fft(basis_time, axis=1)
        coeff = self.rng.standard_normal(r) + 1j*self.rng.standard_normal(r)
        state = DynamicFourierState(basis_spec, coeff)
        bins = [0,3,17,64,127]
        view = state.view(bins, prepared_positions=[7,55])

        time = coeff @ basis_time
        for _ in range(30):
            if self.rng.random() < .55:
                i = int(self.rng.integers(r))
                d = complex(self.rng.standard_normal(), self.rng.standard_normal())
                state.add_coefficient(i,d)
                coeff[i] += d
                time += d*basis_time[i]
            else:
                j = int(self.rng.choice([7,55]))
                d = complex(self.rng.standard_normal(), self.rng.standard_normal())
                state.add_point(j,d)
                time[j] += d
            if self.rng.random() < .4:
                got = view.query()
                expected = np.fft.fft(time)[bins]
                self.assertTrue(np.allclose(got,expected,rtol=2e-11,atol=2e-9))
        got=view.query()
        self.assertTrue(np.allclose(got,np.fft.fft(time)[bins],rtol=2e-11,atol=2e-9))

    def test_repeated_updates_coalesce(self):
        n=64
        basis_time=np.eye(3,n,dtype=np.complex128)
        state=DynamicFourierState(np.fft.fft(basis_time,axis=1),[1,2,3])
        view=state.view([1,5,9])
        for _ in range(10):
            state.add_coefficient(1, .25)
            state.add_point(4, 1)
        state.add_point(4,-10)
        got=view.query(strategy='replay')
        # Point edits cancel. Coefficient 1 gained 2.5.
        coeff=np.array([1,4.5,3],dtype=np.complex128)
        expected=(coeff@basis_time)
        self.assertTrue(np.allclose(got,np.fft.fft(expected)[[1,5,9]]))
        self.assertEqual(view.last_stats.coalesced_coefficients,1)
        self.assertEqual(view.last_stats.coalesced_points,0)

    def test_auto_rebuild_long_backlog(self):
        n,r=128,4
        basis_time=self.rng.standard_normal((r,n))
        state=DynamicFourierState(np.fft.fft(basis_time,axis=1),np.ones(r))
        view=state.view(np.arange(16))
        for _ in range(100):
            state.add_coefficient(0,1e-3)
        got=view.query(strategy='auto')
        self.assertEqual(view.last_stats.strategy,'rebuild')
        expected=state.coefficients@state.basis_spectra[:,np.arange(16)]
        self.assertTrue(np.allclose(got,expected))

    def test_event_log_compaction_and_stale_view(self):
        n=32
        basis=np.fft.fft(np.eye(2,n),axis=1)
        state=DynamicFourierState(basis,[1,1])
        a=state.view([1,2,3],pin_event_log=True)
        b=state.view([4,5],pin_event_log=True)
        state.add_point(7,2)
        a.query()
        self.assertEqual(state.compact_event_log(),0)  # b has not consumed it
        b.query()
        self.assertEqual(state.compact_event_log(),1)
        state.add_coefficient(0,3)
        # Explicitly rebuild one view, then compact after both have advanced.
        a.query()
        b.query()
        self.assertEqual(state.compact_event_log(),1)

    def test_dense_matches_relation(self):
        n,r=64,6
        bt=self.rng.standard_normal((r,n))+1j*self.rng.standard_normal((r,n))
        bs=np.fft.fft(bt,axis=1)
        c=self.rng.standard_normal(r)+1j*self.rng.standard_normal(r)
        state=DynamicFourierState(bs,c,[(3,2+1j),(17,-.5j)])
        x=c@bt
        x[3]+=2+1j; x[17]+=-.5j
        self.assertTrue(np.allclose(state.dense(),np.fft.fft(x),rtol=2e-11,atol=2e-9))


if __name__ == '__main__':
    unittest.main()
