"""End-to-end exact identities, covariance controls, adversarial common-seed trap."""
import unittest,math,sys
import numpy as np
from numpy.testing import assert_allclose
import mixedradix as v
import unit_step_core as core

class MixedRadix(unittest.TestCase):
    def setUp(self):
        self.rng=np.random.default_rng(20261010)

    def rv(self,n):
        return self.rng.normal(size=n)+1j*self.rng.normal(size=n)

    def test_split_and_block(self):
        for n,g,m in [(1,1,1),(3,1,3),(12,4,3),(24,8,3),(40,8,5),
                      (56,8,7),(96,32,3),(384,128,3),(512,512,1),
                      (768,256,3),(1001,1,1001),(1536,512,3)]:
            self.assertEqual((g,m),v.dyadic_odd_split(n))
            if g>1:core.validate_dimensions(g,v.sketch_block(g))

    def test_exact_cooley_tukey_all_lengths(self):
        for n in [1,2,3,4,6,7,8,12,18,20,24,32,40,56,64,93,96,127,
                  128,192,255,256,384,511,512,768,1001,1536]:
            for x in [self.rv(n),np.eye(1,n,0,dtype=np.complex128).reshape(n)]:
                ref=v.exact_mixedradix_reference(x)
                target=np.fft.fft(x)/math.sqrt(n)
                assert_allclose(ref,target,atol=4e-12*math.sqrt(n),rtol=0)

    def test_exact_on_block_one(self):
        for n in [1,3,6,12,20,24,40,56,93,127,1001]:
            x=self.rv(n)
            o=v.one_row_mixedradix(x,self.rng,block=1)
            assert_allclose(o,np.fft.fft(x)/math.sqrt(n),atol=1e-11,rtol=0)
            self.assertAlmostEqual(v.mixedradix_variance_bound(x,1),0.)

    def test_one_root_twiddle(self):
        for g,m in [(1,1),(4,3),(8,5),(128,3),(512,3),(8,127)]:
            table=v.twiddle_one_root(g,m)
            direct=np.exp(-2j*np.pi*np.arange(g)[:,None]*np.arange(m)[None,:]/(g*m))
            assert_allclose(table,direct,atol=3e-12,rtol=0)

    def test_exhaustive_unbiased_small(self):
        # Fix all other input columns to zero, vary single sketch's finite states.
        for g in [8,16]:
            m=3;N=g*m
            M=2 if g==8 else 4
            # Enumerate every state (uniform unit a, beta); exact ensemble mean.
            states=[core.ChirpState(a,beta) for a in range(1,g,2) for beta in range(g)]
            x=self.rv(N)
            xs=x.reshape(g,m)
            baseline=np.zeros((g,m),dtype=np.complex128)
            for s in range(m):
                baseline[:,s]=sum((core.one_row_estimate(xs[:,s],M,st)
                                   for st in states))/len(states)
            target=np.fft.fft(xs,axis=0)/math.sqrt(g)
            assert_allclose(baseline,target,atol=7e-14,rtol=0)
            ct=baseline*np.exp(-2j*np.pi*np.arange(g)[:,None]*np.arange(m)[None,:]/N)
            out=(np.fft.fft(ct,axis=1)/math.sqrt(m)).T.reshape(N)
            assert_allclose(out,np.fft.fft(x)/math.sqrt(N),atol=7e-14,rtol=0)

    def test_exact_covariance_projector_small(self):
        # Numerically reconstruct full E|error_k|^2 from all states, each g block.
        for g,M in [(8,2),(16,4)]:
            n=g*3
            cols=self.rv(n).reshape(g,3)
            states=[core.ChirpState(a,beta) for a in range(1,g,2) for beta in range(g)]
            for k1 in [0,1,g//2]:
                pred=v.mixedradix_variance_exact(cols.reshape(n),k1,M)
                sumvar=0.
                for s in range(3):
                    ref=np.fft.fft(cols[:,s])/math.sqrt(g)
                    vals=np.array([core.one_row_estimate(cols[:,s],M,st)[k1]-ref[k1]
                                   for st in states])
                    sumvar+=float(np.mean(np.abs(vals)**2))/3
                self.assertAlmostEqual(pred,sumvar,delta=1e-12)
                self.assertLessEqual(pred,v.mixedradix_variance_bound(cols.reshape(n),M)+1e-11)

    def test_empirical_mixedradix_variance(self):
        for g,m,M in [(16,3,2),(32,3,4),(32,5,4),(64,3,4)]:
            n=g*m
            x=self.rv(n)
            target=np.fft.fft(x)/math.sqrt(n)
            errors=[]
            for i in range(120):
                row=v.one_row_mixedradix(x,self.rng,block=M)
                errors.append(row-target)
            errors=np.array(errors)
            each=np.mean(np.abs(errors)**2,axis=0)
            self.assertLess(np.max(each),1.5*v.mixedradix_variance_bound(x,M))
            pred=np.array([v.mixedradix_variance_exact(x,k1,M) for k1 in range(g)])
            # Per k1, variance independent of k2; finite runs tested loosely.
            sample=np.mean(each.reshape(m,g),axis=0)
            self.assertLess(float(np.max(np.abs(sample-pred))),0.65*v.mixedradix_variance_bound(x,M))

    def test_full_projector_factorization_and_spectrum(self):
        # For every FIXED sketch-state tuple, row = F_N @ P with
        # P^*=P, P^2=M*P, rank(P)=N/M.
        for g,m,M in [(8,3,2),(16,3,4),(16,5,2)]:
            n=g*m
            states=[core.draw_state(g,self.rng) for _ in range(m)]
            def project(x):
                columns=np.asarray(x,dtype=np.complex128).reshape(g,m)
                y=np.empty_like(columns)
                for s in range(m):
                    y[:,s]=core.materialize_projected_signal(columns[:,s],M,states[s])
                return y.reshape(n)
            x=self.rv(n)
            row=v.one_row_mixedradix(x,self.rng,M,states=states)
            exact=np.fft.fft(project(x))/math.sqrt(n)
            assert_allclose(row,exact,atol=4e-12,rtol=0)
            P=np.column_stack([project(np.eye(n,dtype=np.complex128)[:,j])
                               for j in range(n)])
            assert_allclose(P,P.conj().T,atol=6e-14,rtol=0)
            assert_allclose(P@P,M*P,atol=8e-14,rtol=0)
            self.assertEqual(np.linalg.matrix_rank(P,tol=1e-9),n//M)
            self.assertLess(abs(np.linalg.norm(P-np.eye(n),2)-(M-1)),1e-12)
            self.assertAlmostEqual(np.linalg.norm(P-np.eye(n),'fro')**2,n*(M-1),places=11)

    def test_common_seed_is_dangerous(self):
        g=16;m=3;M=4
        x0=core.worst_case_signal(g,M,output=0)
        x=np.tile(x0[:,None],(1,m)).reshape(g*m)
        pred=v.mixedradix_variance_bound(x,M)
        self.assertAlmostEqual(pred,M/g,places=11)
        # For k1=k2=0, common seeds synchronize all errors coherently.
        states=[core.ChirpState(a,beta) for a in range(1,g,2) for beta in range(g)]
        target=np.fft.fft(x)/math.sqrt(g*m)
        errs=[]
        for st in states:
            row=v.one_row_mixedradix(x,self.rng,M,states=[st]*m)
            errs.append(row[0]-target[0])
        var=float(np.mean(np.abs(errs)**2))
        self.assertAlmostEqual(var,m*pred,delta=2e-12)
        self.assertGreater(var,2*pred)

    def test_work_proxy(self):
        for n in [1,2,8,96,192,384,768,1536,512,1001]:
            p=v.work_proxy(n)
            self.assertGreater(p['work_proxy'],0)
            self.assertEqual(p['g']*p['odd_part'],n)

    def test_streaming_robust_small(self):
        n=384
        x=self.rv(n)
        y=v.robust_mixedradix_fft(x,rows=13,gain=3.0,rng=self.rng)
        ref=np.fft.fft(x)/math.sqrt(n)
        self.assertLess(np.max(np.abs(y-ref)),v.robust_uniform_bound(x,None,3.0))
        self.assertTrue(np.all(np.isfinite(y)))

    def test_tight_beta_frame_exact_and_optimal_rank(self):
        for g,m,M in [(8,3,2),(16,3,4),(32,5,4),(64,3,4),(128,3,4)]:
            n=g*m
            x=self.rv(n)
            y=v.exact_beta_frame(x,self.rng,M)
            assert_allclose(y,np.fft.fft(x)/math.sqrt(n),atol=2e-11,rtol=0)
            # For any t, physical rank is N/M, so <M such rows cannot
            # span the full N-dimensional input space.
            self.assertLess((M-1)*(n//M),n)

    def test_reject_bad_inputs(self):
        for f,arg in [(v.dyadic_odd_split,(0,)),(v.sketch_block,(3,))]:
            with self.assertRaises(ValueError): f(*arg)
        x=np.zeros(24)
        with self.assertRaises(ValueError):v.one_row_mixedradix(x,self.rng,states=[core.ChirpState(1,0)])
        with self.assertRaises(ValueError):v.one_row_mixedradix(x,self.rng,block=5)

if __name__=='__main__':unittest.main(verbosity=2)
