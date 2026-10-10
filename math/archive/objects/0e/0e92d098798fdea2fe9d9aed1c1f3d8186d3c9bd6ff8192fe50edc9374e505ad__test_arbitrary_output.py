import unittest
import numpy as np
from arbitrary_output import ArbitraryBinsDFTPlan, FullFFTBinPlan, AutoOutputPlan, ProductiveProjectionPlanner, choose_radix

class TestArbitraryOutput(unittest.TestCase):
    def test_random_bins_match_fft(self):
        rng=np.random.default_rng(20261009)
        for n in (16,64,256,1024):
            x=rng.standard_normal(n)+1j*rng.standard_normal(n)
            for q in (1,3,8,15):
                if q>n: continue
                bins=rng.choice(n,q,replace=False)
                p=ArbitraryBinsDFTPlan(n,bins)
                got=p.execute(x); expected=np.fft.fft(x)[bins]
                self.assertTrue(np.allclose(got,expected,rtol=3e-11,atol=3e-9),(n,q,p.k,np.max(np.abs(got-expected))))
    def test_scattered_and_duplicate_residues(self):
        rng=np.random.default_rng(7); n=256
        bins=np.array([1,65,129,193,7,71,135,199])
        x=rng.standard_normal(n)+1j*rng.standard_normal(n)
        p=ArbitraryBinsDFTPlan(n,bins,radix=8)
        self.assertTrue(np.allclose(p.execute(x),np.fft.fft(x)[bins],rtol=2e-11,atol=2e-9))
    def test_stream_projection(self):
        rng=np.random.default_rng(11); n=128; bins=np.array([0,3,17,63,91])
        basis=rng.standard_normal((4,n))+1j*rng.standard_normal((4,n))
        p=ArbitraryBinsDFTPlan(n,bins)
        got=p.project_stream(iter(basis)); expected=np.fft.fft(basis,axis=1)[:,bins]
        self.assertTrue(np.allclose(got,expected,rtol=2e-11,atol=2e-9))
    def test_full_plan(self):
        rng=np.random.default_rng(3); n=64; bins=[2,5,33]
        x=rng.standard_normal(n)+1j*rng.standard_normal(n)
        self.assertTrue(np.allclose(FullFFTBinPlan(n,bins).execute(x),np.fft.fft(x)[bins]))
    def test_auto_without_sample(self):
        n=1024; bins=[1,100,777]
        p=AutoOutputPlan(n,bins)
        self.assertEqual(p.strategy,'arbitrary_pruned')
        self.assertTrue(n%choose_radix(n,len(bins))==0)
    def test_measured_auto_and_sample_reuse(self):
        rng=np.random.default_rng(99); n=4096; bins=np.sort(rng.choice(n,17,replace=False))
        basis=rng.standard_normal((3,n))+1j*rng.standard_normal((3,n))
        p=AutoOutputPlan(n,bins,sample=basis[0],reps=1,max_plan_bytes=8*1024*1024)
        got=p.project_stream_with_sample(basis[0],iter(basis[1:]))
        expected=np.fft.fft(basis,axis=1)[:,bins]
        self.assertTrue(np.allclose(got,expected,rtol=3e-11,atol=3e-9))
        self.assertGreaterEqual(p.calibration_ms,0)

    def test_productive_planner(self):
        rng=np.random.default_rng(123); n=2048; bins=np.sort(rng.choice(n,13,replace=False))
        basis=rng.standard_normal((7,n))+1j*rng.standard_normal((7,n))
        p=ProductiveProjectionPlanner(n,bins,max_plan_bytes=4*1024*1024,max_pruned_trials=2)
        got=p.project(iter(basis),expected_count=len(basis))
        expected=np.fft.fft(basis,axis=1)[:,bins]
        self.assertTrue(np.allclose(got,expected,rtol=3e-11,atol=3e-9))
        self.assertEqual(p.stats.basis_count,len(basis))
        self.assertGreaterEqual(len(p.stats.trials),1)

if __name__=='__main__': unittest.main()
