import unittest
import numpy as np

from sparse_surrogate import (
    flatness_tau2, sufficient_sample_count, sparsify_input,
    approximate_dft_all, theorem_failure_bound, universal_sample_count,
)

class SparseSurrogateTests(unittest.TestCase):
    def test_flatness_extremes(self):
        n=64
        x=np.ones(n,dtype=np.complex128)
        self.assertAlmostEqual(flatness_tau2(x),1.0,places=12)
        y=np.zeros(n,dtype=np.complex128); y[7]=3-4j
        self.assertAlmostEqual(flatness_tau2(y),1/n,places=12)

    def test_unbiased_mean_empirical(self):
        rng=np.random.default_rng(12)
        n=32
        x=rng.normal(size=n)+1j*rng.normal(size=n)
        acc=np.zeros(n,dtype=np.complex128)
        trials=4000
        for t in range(trials):
            s,_=sparsify_input(x,.5,.1,rng=rng,samples=8)
            for j,v in s.items(): acc[j]+=v
        acc/=trials
        self.assertLess(np.linalg.norm(acc-x)/np.linalg.norm(x),0.08)

    def test_spike_is_exact(self):
        n=256
        x=np.zeros(n,dtype=np.complex128); x[13]=2+3j
        out,plan=approximate_dft_all(x,.25,.05,rng=np.random.default_rng(1),return_plan=True)
        ref=np.fft.fft(x,norm='ortho')
        self.assertLess(np.max(np.abs(out-ref)),1e-10)
        self.assertEqual(plan.support_size,1)

    def test_explicit_bound_matches_sample_count(self):
        rng=np.random.default_rng(3)
        n=128
        x=rng.normal(size=n)+1j*rng.normal(size=n)
        eps=.4; delta=.05
        k=sufficient_sample_count(x,eps,delta)
        b=theorem_failure_bound(n,eps,flatness_tau2(x),k)
        self.assertLessEqual(b,delta*(1+1e-12))

    def test_all_bins_typical_trial(self):
        rng=np.random.default_rng(9)
        n=1024
        x=rng.normal(size=n)+1j*rng.normal(size=n)
        eps=.35; delta=.05
        out,plan=approximate_dft_all(x,eps,delta,rng=rng,return_plan=True)
        ref=np.fft.fft(x,norm='ortho')
        err=np.max(np.abs(out-ref))/np.linalg.norm(x)
        self.assertLessEqual(err,eps)
        self.assertLessEqual(plan.support_size,plan.actual_draws)

    def test_l1_ceiling_guarantee_typical(self):
        rng=np.random.default_rng(23); n=1024
        x=rng.normal(size=n)+1j*rng.normal(size=n)
        eps=.30; delta=.05
        out,plan=approximate_dft_all(x,eps,delta,rng=rng,scale="l1_ceiling",return_plan=True,exact_sparse_bypass=False)
        ref=np.fft.fft(x,norm="ortho")
        err=np.max(np.abs(out-ref))
        self.assertLessEqual(err,eps*np.linalg.norm(x,1)/np.sqrt(n))
        self.assertEqual(plan.requested_samples,universal_sample_count(n,eps,delta))

    def test_exact_sparse_bypass(self):
        n=2048; x=np.zeros(n,dtype=np.complex128); x[[2,31]]=[1+2j,-3j]
        out,plan=approximate_dft_all(x,.2,.05,rng=np.random.default_rng(5),return_plan=True)
        self.assertEqual(plan.method,"exact-sparse-bypass")
        self.assertLess(np.max(np.abs(out-np.fft.fft(x,norm="ortho"))),1e-10)

if __name__=='__main__': unittest.main()
