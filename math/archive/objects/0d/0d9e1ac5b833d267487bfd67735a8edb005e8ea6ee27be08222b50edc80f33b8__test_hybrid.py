import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import unittest
import numpy as np
from hybrid_sparse import sparse_dft, sparse_plan, normalize_changes, update_spectrum, low_rank_plus_sparse
from adaptive_fft import AdaptiveFFT

class TestHybrid(unittest.TestCase):
    def test_all_small_binary_sparsities(self):
        rng=np.random.default_rng(188)
        for n in [1,2,4,8,16,32,64,128,512]:
            for k in sorted(set([0,1,2,3,4,7,16,n//2,n])):
                if k>n: continue
                indices=rng.choice(n,size=k,replace=False)
                vals=rng.normal(size=k)+1j*rng.normal(size=k)
                edits=list(zip(indices.tolist(),vals.tolist()))
                y,plan=sparse_dft(n,edits,return_plan=True)
                x=np.zeros(n,dtype=np.complex128)
                x[indices]=vals
                self.assertTrue(np.allclose(y,np.fft.fft(x),rtol=2e-11,atol=2e-10), f'{n=} {k=} maxdiff={np.max(np.abs(y-np.fft.fft(x)))}')
                self.assertEqual(plan.n,n)
                self.assertLessEqual(plan.sparse_phase_terms,n)
                self.assertGreaterEqual(plan.b,max(k,1))
                if k:
                    self.assertLess(plan.b,2*k)

    def test_duplicates_cancel(self):
        d=normalize_changes(16,[(3,2),(3,-2),(8,1),(8,3)])
        self.assertEqual(d,{8:4+0j})
        y=sparse_dft(16,[(3,2),(3,-2),(8,1),(8,3)])
        x=np.zeros(16);x[8]=4
        self.assertTrue(np.allclose(y,np.fft.fft(x)))

    def test_reject_bad_inputs(self):
        for arg in [3,0,-1]:
            with self.assertRaises(ValueError): sparse_dft(arg,[(0,1)])
        with self.assertRaises(ValueError): sparse_dft(8,[(8,1)])
        with self.assertRaises(ValueError): sparse_dft(8,[(-1,1)])
        with self.assertRaises(ValueError): sparse_dft(8,[(0,float('nan'))])

    def test_known_full_edit(self):
        rng=np.random.default_rng(77)
        for n in [8,16,64,256,1024]:
            base=rng.normal(size=n)
            old=np.fft.fft(base)
            indices=rng.choice(n,size=min(n,7),replace=False)
            vals=rng.normal(size=len(indices))
            modified=base.copy()
            modified[indices]+=vals
            output,plan=update_spectrum(old,list(zip(indices.tolist(),vals.tolist())))
            self.assertTrue(np.allclose(output,np.fft.fft(modified),atol=2e-10))
            self.assertEqual(plan.k,len(indices))

    def test_low_rank_sparse(self):
        rng=np.random.default_rng(33)
        for n in [8,64,256]:
            basis=rng.normal(size=(2,n))
            coeff=np.array([2.5,-0.75])
            edits=[(0,0.4),(n//2,-0.65),(n-1,1.2)]
            y,plan=low_rank_plus_sparse(np.fft.fft(basis,axis=1),coeff,edits)
            x=coeff@basis
            for pos,val in edits:x[pos]+=val
            self.assertTrue(np.allclose(y,np.fft.fft(x),atol=2e-10))
            self.assertEqual(plan.k,3)

    def test_pluggable_small_transform(self):
        def brute(a):
            m=len(a)
            omega=np.exp(-2j*np.pi/m)
            return np.array([sum(a[j]*omega**(j*k) for j in range(m)) for k in range(m)])
        for n in [4,8,16,64]:
            y=sparse_dft(n,[(0,1),(n//2,3)],small_transform_1d=brute)
            x=np.zeros(n);x[0]=1;x[n//2]=3
            self.assertTrue(np.allclose(y,np.fft.fft(x),atol=1e-10))

    def test_existing_engine_compatibility(self):
        rng=np.random.default_rng(123)
        eng=AdaptiveFFT(mode='plain')
        for n in [32,256]:
            base=rng.normal(size=n)
            prior=eng.fft(base)
            edits=[(4,2),(7,-1)]
            y,_=update_spectrum(prior,edits)
            b=base.copy();b[4]+=2;b[7]-=1
            self.assertTrue(np.allclose(y,np.fft.fft(b)))

if __name__=='__main__': unittest.main()
