import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import unittest
import numpy as np
from lazy_spectrum import LazySpectrum

class TestLazySpectrum(unittest.TestCase):
    def test_point_edits_and_partial_bins(self):
        rng=np.random.default_rng(1001)
        for n in [17,64,256,1024]:
            x=rng.standard_normal(n)+1j*rng.standard_normal(n)
            state=LazySpectrum.from_spectrum(np.fft.fft(x))
            edits=[]
            for _ in range(30):
                j=int(rng.integers(0,n)); d=complex(rng.normal(),rng.normal())
                x[j]+=d; edits.append((j,d)); state.add_edit(j,d)
            bins=rng.integers(0,n,size=min(25,n)).tolist()
            got=state.bins(bins)
            want=np.fft.fft(x)[bins]
            self.assertTrue(np.allclose(got,want,rtol=2e-11,atol=2e-10))

    def test_duplicate_edits_cancel(self):
        n=64
        x=np.arange(n,dtype=float)
        state=LazySpectrum.from_spectrum(np.fft.fft(x))
        state.add_edits([(7,2),(7,-2),(3,4)])
        self.assertEqual(state.pending_count,1)
        x[3]+=4
        got,_=state.materialize(method='direct')
        self.assertTrue(np.allclose(got,np.fft.fft(x)))

    def test_dense_direct_and_factorized(self):
        rng=np.random.default_rng(1002)
        for n in [64,256,1024]:
            base=rng.normal(size=n)+1j*rng.normal(size=n)
            idx=rng.choice(n,size=min(12,n),replace=False)
            vals=rng.normal(size=len(idx))+1j*rng.normal(size=len(idx))
            altered=base.copy(); altered[idx]+=vals
            for method in ['direct','factorized']:
                s=LazySpectrum.from_spectrum(np.fft.fft(base))
                s.add_edits(zip(idx.tolist(),vals.tolist()))
                got,plan=s.materialize(method=method)
                self.assertTrue(np.allclose(got,np.fft.fft(altered),rtol=2e-11,atol=3e-10))
                self.assertEqual(plan.pending_edits,len(idx))

    def test_commit(self):
        n=128
        rng=np.random.default_rng(1003)
        x=rng.normal(size=n)
        s=LazySpectrum.from_spectrum(np.fft.fft(x))
        s.add_edits([(1,2.0),(7,-1.5)])
        plan=s.compact(method='direct')
        self.assertEqual(plan.pending_edits,2)
        self.assertEqual(s.pending_count,0)
        self.assertEqual(s.dense_term_count,1)
        x[1]+=2;x[7]-=1.5
        self.assertTrue(np.allclose(s.bins([0,1,3,127]),np.fft.fft(x)[[0,1,3,127]]))

    def test_lazy_basis_plus_sparse(self):
        rng=np.random.default_rng(1004)
        n=256
        basis=rng.normal(size=(3,n))
        coeff=np.array([2.0,-0.5,0.25])
        edits=[(2,1.25),(17,-0.75),(250,0.5)]
        s=LazySpectrum.from_basis(np.fft.fft(basis,axis=1),coeff,edits=edits)
        x=coeff@basis
        for j,d in edits:x[j]+=d
        bins=[0,1,7,31,100,255]
        self.assertTrue(np.allclose(s.bins(bins),np.fft.fft(x)[bins],atol=2e-10))
        dense,_=s.materialize(method='direct')
        self.assertTrue(np.allclose(dense,np.fft.fft(x),atol=3e-10))


    def test_dense_native(self):
        rng=np.random.default_rng(1006)
        n=1024
        base=rng.normal(size=n)+1j*rng.normal(size=n)
        s=LazySpectrum.from_spectrum(np.fft.fft(base))
        edits=[(4,2+1j),(77,-.5j),(900,1.25)]
        for j,d in edits: base[j]+=d
        s.add_edits(edits)
        got,plan=s.materialize(method='native')
        self.assertEqual(plan.method,'native')
        self.assertTrue(np.allclose(got,np.fft.fft(base),rtol=2e-11,atol=3e-10))

    def test_validation(self):
        with self.assertRaises(ValueError): LazySpectrum(0)
        s=LazySpectrum.from_spectrum(np.ones(8))
        with self.assertRaises(ValueError): s.add_edit(8,1)
        with self.assertRaises(ValueError): s.bins([8])

if __name__=='__main__':unittest.main()

class TestPreparedBinView(unittest.TestCase):
    def test_prepared_support_queries(self):
        from lazy_spectrum import PreparedBinView
        rng=np.random.default_rng(1005)
        for n in [64,1024,4096]:
            x=rng.standard_normal(n)+1j*rng.standard_normal(n)
            support=rng.choice(n,size=min(12,n),replace=False).tolist()
            bins=rng.choice(n,size=min(17,n),replace=True).tolist()
            view=PreparedBinView(np.fft.fft(x),support,bins)
            for _ in range(40):
                j=int(rng.choice(support)); d=complex(rng.normal(),rng.normal())
                x[j]+=d; view.add_edit(j,d)
                self.assertTrue(np.allclose(view.values(),np.fft.fft(x)[bins],rtol=2e-11,atol=3e-10))
            self.assertLessEqual(view.phase_bytes,view.full_phase_cache_equivalent_bytes)

    def test_bad_support(self):
        from lazy_spectrum import PreparedBinView
        base=np.ones(16,dtype=complex)
        with self.assertRaises(ValueError): PreparedBinView(base,[1,1],[0])
        view=PreparedBinView(base,[1,2],[0,3])
        with self.assertRaises(ValueError): view.add_edit(3,1)

class TestBufferedSpectrum(unittest.TestCase):
    def test_threshold_flush(self):
        from lazy_spectrum import BufferedSpectrum
        rng=np.random.default_rng(1007);n=256
        x=rng.normal(size=n)+1j*rng.normal(size=n)
        s=BufferedSpectrum.from_spectrum(np.fft.fft(x),flush_threshold=4,flush_method='native')
        for j in [1,3,5,7,9,11,13,15,17]:
            d=complex(rng.normal(),rng.normal());x[j]+=d;s.add_edit(j,d)
        self.assertEqual(s.flush_count,2)
        self.assertEqual(s.pending_count,1)
        bins=[0,1,17,200,255]
        self.assertTrue(np.allclose(s.bins(bins),np.fft.fft(x)[bins],atol=3e-10))

    def test_threshold_planner(self):
        from lazy_spectrum import suggest_flush_threshold,threshold_cost_proxy
        b=suggest_flush_threshold(65536,64,16,backend='native')
        self.assertGreaterEqual(b,1);self.assertLessEqual(b,65536)
        self.assertLessEqual(threshold_cost_proxy(65536,64,16,b),threshold_cost_proxy(65536,64,16,1))
