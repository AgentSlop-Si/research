import unittest
import numpy as np
from sampled_pruned_fft import sparse_fft, approximate_normalized_fft, sample_count

class SamplingTests(unittest.TestCase):
    def test_pruned_matches_dense_fft_for_random_sparse_vectors(self):
        rng=np.random.default_rng(79)
        for N in [1,2,16,64,256,1024]:
            for k in [0,1,2,4,8,16]:
                ids=rng.integers(0,N,size=k)
                vals=rng.uniform(-1,1,k)+1j*rng.uniform(-1,1,k)
                dense=np.zeros(N,complex)
                np.add.at(dense,ids,vals)
                result,stats=sparse_fft(N,ids,vals)
                self.assertTrue(np.allclose(result,np.fft.fft(dense),atol=3e-11,rtol=0), (N,k))
                self.assertEqual(len(result),N)

    def test_sparse_k_bound(self):
        N=4096
        for k in [1,2,4,16,64,128]:
            ids=np.arange(k)*(N//k)
            a,stats=sparse_fft(N,ids,np.ones(k))
            # Derivation: total slots at active recursion depth <= min(2^d,k) * N/(2^(d+1)).
            bound=N*(1+np.log2(k))/2
            self.assertLessEqual(stats.butterfly_slots,bound+N)

    def test_sampling_uniform_accuracy_for_fixed_inputs(self):
        rng=np.random.default_rng(53)
        for N in [1024,4096,16384]:
            signals=[]
            signals.append(np.ones(N,dtype=complex))
            signals.append(np.array([(-1)**i for i in range(N)],dtype=complex))
            signals.append(np.exp(2j*np.pi*7*np.arange(N)/N))
            z=rng.normal(size=N)+1j*rng.normal(size=N)
            signals.append(z/np.maximum(1,abs(z)))
            for i,x in enumerate(signals):
                epsilon=.4
                y,stats=approximate_normalized_fft(x,epsilon,0.01,seed=87)
                true=np.fft.fft(x)/N
                self.assertLessEqual(float(np.max(abs(y-true))),epsilon,(N,i))
                self.assertEqual(stats['samples'],sample_count(N,epsilon,.01))

    def test_sampling_not_exact(self):
        rng=np.random.default_rng(91)
        x=rng.uniform(-1,1,256).astype(complex)
        y,_=approximate_normalized_fft(x,.5,.02,seed=5)
        self.assertGreater(float(np.max(abs(y-np.fft.fft(x)/256))),1e-6)

if __name__=='__main__':unittest.main()
