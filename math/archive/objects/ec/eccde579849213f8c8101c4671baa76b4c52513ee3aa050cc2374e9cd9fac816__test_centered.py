"""Reproducible checks of v12 centered shared-state Fourier correction."""
import unittest
import math
import numpy as np
from numpy.testing import assert_allclose

import centered_lift as cm
import prototype as base
import unit_step_core as core


class CenteredTests(unittest.TestCase):
    def setUp(self):
        self.rng=np.random.default_rng(20261009)

    def randvec(self,n):
        return self.rng.normal(size=n)+1j*self.rng.normal(size=n)

    def test_minimax_center(self):
        for n in [1,2,3,8,37,93,511,513,1001]:
            q=base.next_power_of_two(n)
            c=cm.support_center(n,q)
            self.assertAlmostEqual(max(abs(c),abs((n-1)/q-c)),(n-1)/(2*q))
            # Includes asymmetric candidates, not merely the old c=0.
            for offset in [-0.2,-0.03,0.01,0.07,0.3]:
                cc=c+offset
                self.assertGreaterEqual(max(abs(cc),abs((n-1)/q-cc))+1e-13,
                                        (n-1)/(2*q))

    def test_exact_grid_two_step_carrier(self):
        for n in [1,2,3,8,17,37,93,127,255,511,1023,10001]:
            q=base.next_power_of_two(n)
            j,r,theta=base.exact_nearest_grid_map(n,q)
            self.assertTrue(np.all((np.diff(j)==1)|(np.diff(j)==2)))
            product=cm.shared_carrier(n,j)
            target=np.exp(-2j*np.pi*cm.support_center(n,q)*theta)
            self.assertLess(np.max(np.abs(product-target)),5e-12)
            self.assertTrue(np.all(np.abs(product)>0.99999999999))
            self.assertEqual(r[0],0)

    def test_rank_certificates(self):
        a=cm.certified_rank(511,1e-8,False)
        b=cm.certified_rank(511,1e-8,True)
        self.assertEqual((a,b),(15,11))
        for n in [37,93,127,255,511,1001,4095,10007]:
            for tau in [1e-4,1e-8,1e-12]:
                x=cm.certified_rank(n,tau,False)
                y=cm.certified_rank(n,tau,True)
                self.assertLessEqual(y,x)
                self.assertLessEqual(cm.certified_tail(y,np.pi*(n-1)/(2*base.next_power_of_two(n))),tau)

    def test_deterministic_exact_lift(self):
        # Direct N-FFT is a validation oracle, not part of the algorithm.
        for n in [8,17,37,93,127,255,511]:
            for x in [self.randvec(n),np.eye(1,n,0,dtype=np.complex128)[0],
                      np.exp(2j*np.pi*np.arange(n)*3/n)]:
                rank=13
                y=cm.centered_truncated_center(x,rank)
                f=np.fft.fft(x)/np.sqrt(n)
                q=base.next_power_of_two(n)
                e=cm.certified_tail(rank,np.pi*(n-1)/(2*q))*np.linalg.norm(x)
                self.assertLessEqual(np.max(np.abs(y-f)),e+1e-11*np.linalg.norm(x))

    def test_fused_center_error(self):
        for n in [37,93,127,255,511]:
            x=self.randvec(n)
            block=base.choose_dyadic_block(base.next_power_of_two(n))
            for H in [0,1,2,3]:
                f=cm.centered_fused_center(x,10,block,H)
                r=cm.centered_truncated_center(x,10)
                eb=base.addition_kernel_error_bound(n,10,block,H)*np.linalg.norm(x)
                self.assertLessEqual(np.max(np.abs(f-r)),eb+1e-11*np.linalg.norm(x))
                target=np.fft.fft(x)/np.sqrt(n)
                bound=cm.centered_deterministic_bound(n,10,block,H)*np.linalg.norm(x)
                self.assertLessEqual(np.max(np.abs(f-target)),bound+1e-11*np.linalg.norm(x))

    def test_baseline_center_zero_regression(self):
        for n in [37,93,255]:
            q=base.next_power_of_two(n)
            block=base.choose_dyadic_block(q)
            state=core.draw_state(q,self.rng)
            x=self.randvec(n)
            for H in [0,1,2]:
                ref=base.fused_addition_bessel_chirp_row(x,9,block,state,H)
                got=cm.centered_fused_row(x,9,block,state,H,center_override=0)
                assert_allclose(got,ref,rtol=0,atol=1e-12)

    def test_randomized_row_positive_variance(self):
        n=93; q=base.next_power_of_two(n)
        block=base.choose_dyadic_block(q)
        x=self.randvec(n)
        rank=8;H=1
        center=cm.centered_fused_center(x,rank,block,H)
        errors=[]
        for i in range(90):
            state=core.draw_state(q,self.rng)
            y=cm.centered_fused_row(x,rank,block,state,H)
            errors.append(y-center)
        noise=np.array(errors)
        empirical=np.mean(np.abs(noise)**2,axis=0)
        theorem=cm.centered_row_variance_bound(x,rank,block,H)
        self.assertLess(float(np.mean(empirical)),theorem)
        self.assertLess(float(np.max(empirical)),1.2*theorem) # finite sample
        self.assertLess(float(np.max(np.abs(np.mean(noise,axis=0)))),2.0) # sampling error

    def test_rank_independent_addition_bound_direct_kernels(self):
        # This checks the exact mathematical coefficient convolution, not the
        # transform's end-to-end floating-point implementation.
        from scipy.special import jv
        rng=np.random.default_rng(981)
        for n in [37,127,511]:
            q=base.next_power_of_two(n)
            block=base.choose_dyadic_block(q)
            center=cm.support_center(n,q)
            for rank in [3,7,13,21]:
                for H in [0,1,2]:
                    bnd=cm.addition_bound_rank_independent(n,block,H)
                    worst=0.0
                    for trial in range(8):
                        b=int(rng.integers(0,1+(n-1)//block))
                        t=int(rng.integers(0,min(block,n-b*block)))
                        theta=float(rng.uniform(-0.5,0.5))
                        zb=math.pi*(b*block/q-center)
                        delta=math.pi*t/q
                        coeff=2*theta
                        a=math.acos(coeff)
                        exact=0j;fused=0j
                        for r in range(rank):
                            mult=1 if r==0 else 2*(-1j)**r*math.cos(r*a)
                            exact+=mult*jv(r,zb+delta)
                            approx=sum(jv(r-h,zb)*jv(h,delta)
                                       for h in range(-H,H+1))
                            fused+=mult*approx
                        err=abs(exact-fused)
                        worst=max(worst,err)
                    self.assertLessEqual(worst,bnd+1e-11)

    def test_local_bound_independent_of_expansion_rank(self):
        for n in [127,511,4095]:
            block=base.choose_dyadic_block(base.next_power_of_two(n))
            for H in [0,1,2]:
                v=cm.addition_bound_rank_independent(n,block,H)
                self.assertGreaterEqual(v,0.0)
                self.assertLess(v,base.addition_kernel_error_bound(n,11,block,H))
                self.assertAlmostEqual(v,cm.addition_bound_rank_independent(n,block,H))
        self.assertLess(cm.bessel_l1_envelope(math.pi/2),4.25)

    def test_parameter_search_fully_charged_proxy(self):
        n=511;tol=1e-4
        old=cm.choose_parameters(n,tol,old_v11=True)
        new=cm.choose_parameters(n,tol)
        self.assertEqual((old['rank'],old['halfwidth']),(11,2))
        self.assertEqual((new['rank'],new['halfwidth']),(7,2))
        self.assertLess(new['work_proxy'],old['work_proxy'])
        self.assertLessEqual(new['deterministic_error_bound'],tol)

    def test_robust_end_to_end(self):
        n=127
        x=self.randvec(n)
        out=cm.centered_robust_fft(x,rank=8,rows=5,g=3.0,rng=self.rng,halfwidth=2)
        exact=np.fft.fft(x)/np.sqrt(n)
        radius=cm.robust_uniform_bound(x,8,3.0,2)
        self.assertLess(np.max(np.abs(out-exact)),radius)
        self.assertEqual(out.shape,(n,))
        self.assertTrue(np.isfinite(out).all())

    def test_zero_and_bounds_validation(self):
        n=93;q=base.next_power_of_two(n)
        block=base.choose_dyadic_block(q)
        z=np.zeros(n,dtype=np.complex128)
        state=core.draw_state(q,self.rng)
        self.assertTrue(np.all(cm.centered_fused_row(z,6,block,state,0)==0))
        self.assertEqual(cm.centered_row_variance_bound(z,6,block,0),0)
        for fn,arg in [(cm.certified_tail,(-1,1.0)),(cm.certified_rank,(100,0)),
                       (cm.support_center,(0,))]:
            with self.assertRaises(ValueError): fn(*arg)

if __name__=='__main__':unittest.main(verbosity=2)
