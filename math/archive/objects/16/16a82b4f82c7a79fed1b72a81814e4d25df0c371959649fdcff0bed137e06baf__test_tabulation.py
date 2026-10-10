import unittest
import numpy as np
from lookup_fft import (QuantizedDFTTable, normalized_fft_quantized,
                        normal_dit_stages, direct_group_matrix)
from cost_model import model

class TabulationTests(unittest.TestCase):
    def test_exact_grouping_complex_random_all_positions(self):
        rng=np.random.default_rng(91)
        for L in range(2,9):
            N=2**L
            a=rng.uniform(-.7,.7,N)+1j*rng.uniform(-.7,.7,N)
            for s in range(L):
                for t in range(1,L-s+1):
                    x=normal_dit_stages(a,s,t)
                    y=direct_group_matrix(a,s,t)
                    self.assertTrue(np.allclose(x,y,rtol=0,atol=3e-12),(L,s,t,np.max(abs(x-y))))

    def test_full_table_matches_lazy_and_direct_table(self):
        rng=np.random.default_rng(2)
        for t,R in [(1,4),(2,1)]:
            K=2**t
            f=QuantizedDFTTable(K,R,"full")
            l=QuantizedDFTTable(K,R,"lazy")
            d=QuantizedDFTTable(K,R,"direct")
            for _ in range(90):
                grid=rng.integers(-R,R+1,(K,2))
                z=(grid[:,0]+1j*grid[:,1])/R
                a=f.apply(z);b=l.apply(z);c=d.apply(z)
                self.assertTrue(np.array_equal(a,b), (t,R,a,b))
                self.assertTrue(np.array_equal(a,c), (t,R,a,c))
            self.assertEqual(f.stats.misses,0)

    def test_table_grouped_normalized_fft(self):
        rng=np.random.default_rng(5)
        for L in [4,6,8,10]:
            N=1<<L
            for name in ["random","constant","impulse","alternating"]:
                if name=="random":
                    raw=rng.normal(size=N)+1j*rng.normal(size=N)
                    raw=raw/np.maximum(1,abs(raw))
                elif name=="constant":raw=np.ones(N,dtype=complex)
                elif name=="impulse":
                    raw=np.zeros(N,dtype=complex);raw[19%N]=1
                else:raw=np.array([1 if j%2==0 else -1 for j in range(N)],dtype=complex)
                for t in [1,2,3]:
                    R=256
                    out,stats,_=normalized_fft_quantized(raw,t,R,table_mode="lazy")
                    target=np.fft.fft(raw)/N
                    err=float(np.max(abs(out-target)))
                    conservative=(2*stats.group_count+1)/R
                    self.assertLessEqual(err,conservative+1e-12,(L,t,name,err,conservative))
                    self.assertEqual(stats.processed,sum(N//(2**min(t,L-s)) for s in range(0,L,t)))

    def test_one_table_across_many_fft_stage_groups(self):
        raw=np.array([.33*np.sin(j)+.16j*np.cos(j) for j in range(64)])
        out,stats,tables=normalized_fft_quantized(raw,2,1,table_mode="full",max_entries=7000)
        self.assertEqual(set(tables),{4})
        self.assertEqual(stats.group_count,3)
        self.assertEqual(stats.processed,3*64//4)
        self.assertLessEqual(float(np.max(abs(out-np.fft.fft(raw)/64))),1.75)

    def test_word_cost_model_growing_block(self):
        e=[model(L) for L in (128,256,1024,8192,65536)]
        self.assertTrue(e[-1].grouped_levels>e[0].grouped_levels)
        self.assertLessEqual(e[-1].log2_table_entries, e[-1].cap_fraction*e[-1].log2_N)
        self.assertTrue(e[-1].preprocessing_below_N)
        self.assertLess(e[-1].normalized_error_bound,.05)

if __name__=='__main__':unittest.main()
