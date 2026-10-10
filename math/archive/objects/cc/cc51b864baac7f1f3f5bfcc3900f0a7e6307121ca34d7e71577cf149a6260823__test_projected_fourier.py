import unittest
import numpy as np
from projected_fourier import ProjectedFourierState

class TestProjectedFourier(unittest.TestCase):
    def test_matches_full_fft_without_storing_full_spectra(self):
        rng=np.random.default_rng(404)
        n,r,q=256,7,19
        bt=rng.standard_normal((r,n))+1j*rng.standard_normal((r,n))
        coeff=rng.standard_normal(r)+1j*rng.standard_normal(r)
        bins=np.sort(rng.choice(n,q,replace=False))
        projection=np.fft.fft(bt,axis=1)[:,bins]
        state=ProjectedFourierState(n,bins,projection,coeff,prepared_positions=[3,91,200],event_capacity=64)
        x=coeff@bt
        for t in range(80):
            if t%3:
                i=t%r; d=complex(.01*(t+1),-.003*t)
                state.add_coefficient(i,d); x += d*bt[i]
            else:
                j=[3,91,200][(t//3)%3]; d=complex(.02*t,.001*t)
                state.add_point(j,d); x[j]+=d
            if t%5==0:
                self.assertTrue(np.allclose(state.query(),np.fft.fft(x)[bins],rtol=2e-11,atol=2e-9))
                state.compact()
        self.assertTrue(np.allclose(state.query(),np.fft.fft(x)[bins],rtol=2e-11,atol=2e-9))

    def test_bounded_history_forces_exact_rebuild(self):
        n,r,q=64,3,8
        rng=np.random.default_rng(1)
        proj=rng.standard_normal((r,q))+1j*rng.standard_normal((r,q))
        c=np.ones(r,dtype=complex)
        st=ProjectedFourierState(n,np.arange(q),proj,c,event_capacity=2)
        for _ in range(10): st.add_coefficient(0,.1)
        got=st.query()
        self.assertEqual(st.last_stats.strategy,'rebuild')
        self.assertTrue(np.allclose(got,st.coefficients@proj))

if __name__=='__main__':unittest.main()
