import unittest, math
import numpy as np

from sparse_surrogate import (
    accuracy_tradeoff, make_head_tail_plan, plan_head_tail,
    sparsify_head_tail, approximate_dft_all_head_tail,
    sparse_surrogate_linf_lower_bound, flat_natural_scale_support_lower_bound,
    best_k_term_l2_tail,
)

class SparseSurrogateV2Tests(unittest.TestCase):
    def test_vanishing_accuracy_tradeoff(self):
        n=2**20; delta=n**-2
        eps=1/math.sqrt(math.log(n))
        p=accuracy_tradeoff(n,eps,delta)
        self.assertLess(p.samples,n)
        self.assertLess(p.depth_ratio,1.0)

    def test_head_tail_plan_beats_plain_on_compressible_input(self):
        n=4096
        x=(1.0/(np.arange(n)+1.0)**1.2).astype(np.complex128)
        eps=.20; delta=.05
        base=make_head_tail_plan(x,eps,delta,0)
        best=plan_head_tail(x,eps,delta,max_head=128)
        self.assertLess(best.support_upper_bound,base.support_upper_bound)
        self.assertGreaterEqual(best.head_size,1)

    def test_head_tail_guarantee_typical(self):
        n=4096
        rng=np.random.default_rng(123)
        phases=np.exp(2j*np.pi*rng.random(n))
        x=phases/(np.arange(n)+1.0)**1.1
        eps=.22; delta=.05
        plan=plan_head_tail(x,eps,delta,max_head=128)
        out,_=approximate_dft_all_head_tail(x,eps,delta,plan=plan,rng=np.random.default_rng(7),return_plan=True)
        ref=np.fft.fft(x,norm='ortho')
        target=eps*np.linalg.norm(x,1)/math.sqrt(n)
        self.assertLessEqual(np.max(np.abs(out-ref)),target)

    def test_best_k_term_tail_flat(self):
        n=128; x=np.ones(n,dtype=np.complex128)
        k=36
        self.assertAlmostEqual(best_k_term_l2_tail(x,k),math.sqrt(n-k),places=10)
        self.assertAlmostEqual(sparse_surrogate_linf_lower_bound(x,k),math.sqrt((n-k)/n),places=10)

    def test_natural_scale_requires_linear_support(self):
        n=10000
        self.assertEqual(flat_natural_scale_support_lower_bound(n,.5),7500)
        self.assertEqual(flat_natural_scale_support_lower_bound(n,0),n)

    def test_head_only_when_tail_deterministically_small(self):
        n=1024; x=np.zeros(n,dtype=np.complex128)
        x[0]=10
        x[1:]=1e-5
        p=make_head_tail_plan(x,.01,.05,1)
        self.assertEqual(p.requested_samples,0)
        self.assertEqual(p.method,'head-only')
        sparse,_=sparsify_head_tail(x,.01,.05,plan=p,rng=np.random.default_rng(1))
        self.assertEqual(set(sparse),{0})

if __name__=='__main__': unittest.main()
