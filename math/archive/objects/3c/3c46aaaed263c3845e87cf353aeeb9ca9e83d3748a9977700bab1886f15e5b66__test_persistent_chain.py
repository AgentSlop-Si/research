import unittest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
from scipy import fft
from persistent_chain import ChainEngine, Factor


def brute(factors):
    half=np.ones(factors[0].n//2+1,dtype=np.complex128)
    for factor in factors:
        half *= fft.rfft(factor.values())
    return fft.irfft(half,n=factors[0].n)


class TestPhase7(unittest.TestCase):
    def setUp(self):
        self.rng=np.random.default_rng(411)
        self.n=64
        self.engine=ChainEngine(max_bin_cache=512)
        self.seeds=[self.engine.seed(self.rng.normal(size=self.n)*0.1) for _ in range(5)]
        self.root=self.engine.chain(self.seeds)

    def test_base_chain(self):
        np.testing.assert_allclose(self.root.dense(),brute(self.seeds),rtol=1e-9,atol=1e-9)

    def test_frequency_queries(self):
        ks=[0,1,3,7,11,32,54,63]
        expected=fft.fft(self.root.dense())[ks]
        np.testing.assert_allclose(self.root.frequencies(ks),expected,atol=1e-9)

    def test_base_selected_output(self):
        qs=[2,17,31]
        np.testing.assert_allclose(self.root.time(qs),self.root.dense()[qs],atol=1e-9)

    def test_single_edit(self):
        other=self.root.edit(2,13,2.0)
        expect=brute([other.factor(i) for i in range(5)])
        np.testing.assert_allclose(other.dense('sparse'),expect,atol=1e-9)
        np.testing.assert_allclose(other.time([1,3,11]),expect[[1,3,11]],atol=1e-9)
        np.testing.assert_allclose(other.frequencies([1,23,63]),fft.fft(expect)[[1,23,63]],atol=1e-9)

    def test_repeated_edit_cancels(self):
        v=self.root.edit(2,4,3.0).edit(2,4,-3.0)
        self.assertTrue(v.factor(2).is_base())
        self.assertEqual(v.root.uid,self.root.root.uid)
        np.testing.assert_allclose(v.dense(),self.root.dense())

    def test_many_edits_same_factor(self):
        v=self.root
        for t,d in ((4,1.4),(7,-0.7),(30,0.8),(17,-0.4)):
            v=v.edit(1,t,d)
        expect=brute([v.factor(i) for i in range(5)])
        np.testing.assert_allclose(v.dense('sparse'),expect,atol=1e-9)
        np.testing.assert_allclose(v.time([0,1,6,29]),expect[[0,1,6,29]],atol=1e-9)

    def test_shift_only(self):
        v=self.root.shift(3,12)
        expected=np.roll(self.root.dense(),12)
        np.testing.assert_allclose(v.dense(),expected,atol=1e-9)
        np.testing.assert_allclose(v.time([1,10]),expected[[1,10]],atol=1e-9)

    def test_scale_only(self):
        v=self.root.scale(0,-2.75)
        np.testing.assert_allclose(v.dense(),-2.75*self.root.dense(),atol=1e-9)

    def test_shift_scale_edit_order(self):
        v=self.root.edit(0,3,1.0).shift(0,4).scale(0,2.0).edit(0,6,-1.4)
        expected=brute([v.factor(i) for i in range(5)])
        np.testing.assert_allclose(v.dense('sparse'),expected,atol=1e-9)
        np.testing.assert_allclose(v.time([1,13,63]),expected[[1,13,63]],atol=1e-9)

    def test_two_modified_factors(self):
        v=self.root.edit(0,3,1.25).edit(3,20,-0.75)
        expect=brute([v.factor(i) for i in range(5)])
        np.testing.assert_allclose(v.dense(),expect,atol=1e-9)
        np.testing.assert_allclose(v.frequencies([3,9,55]),fft.fft(expect)[[3,9,55]],atol=1e-9)
        with self.assertRaises(ValueError):
            v.dense('sparse')

    def test_all_factors_modified(self):
        v=self.root
        for j in range(5):
            v=v.edit(j,(j*5)%self.n,.2+j/5)
        expected=brute([v.factor(i) for i in range(5)])
        np.testing.assert_allclose(v.dense(),expected,atol=1e-8)

    def test_zero_root_factor(self):
        e=ChainEngine()
        base=e.seed(np.ones(16))
        impulse=e.seed(np.array([1.0]+[0.0]*15))
        ref=e.chain([base,impulse])
        test=ref.edit(0,3,0.75)
        np.testing.assert_allclose(test.dense(),fft.irfft(fft.rfft(test.factor(0).values())*fft.rfft(test.factor(1).values()),n=16),atol=1e-9)

    def test_zero_seed(self):
        e=ChainEngine()
        z=e.seed(np.zeros(16))
        d=e.seed(np.arange(16,dtype=float))
        v=e.chain([z,d]).edit(0,3,1.0)
        expected=np.roll(d.seed.signal,3)
        np.testing.assert_allclose(v.dense('sparse'),expected)

    def test_fork_is_immutable(self):
        a=self.root.edit(1,10,2.0)
        b=self.root.edit(1,10,-2.0)
        self.assertTrue(self.root.factor(1).is_base())
        self.assertNotEqual(a.root.uid,b.root.uid)
        np.testing.assert_allclose(self.root.dense(),brute(self.seeds))

    def test_hash_consing_cancels_version(self):
        v=self.root.shift(3,4).shift(3,-4)
        self.assertEqual(v.root.uid,self.root.root.uid)

    def test_structural_sharing(self):
        v=self.root.edit(3,11,1.0)
        reuse=self.root.count_reused_nodes(v)
        self.assertGreater(reuse['shared_nodes'],0)
        self.assertLess(reuse['new_nodes'],self.root.root.size)

    def test_bins_caching_and_version(self):
        bins=[0,1,17,63]
        self.root.frequencies(bins)
        v=self.root.edit(1,20,0.5)
        before=self.engine.stats['bin_hits']
        v.frequencies(bins)
        self.assertGreater(self.engine.stats['bin_hits'],before)
        np.testing.assert_allclose(v.frequencies(bins),fft.fft(brute([v.factor(i) for i in range(5)]))[bins],atol=1e-9)

    def test_bounded_caches(self):
        eng=ChainEngine(max_complement_bytes=64*8,max_bin_cache=5)
        seeds=[eng.seed(np.arange(64)+i) for i in range(5)]
        v=eng.chain(seeds)
        v.frequencies([0,1,2,3,4,5])
        self.assertLessEqual(eng.memory_report()['bin_cache_entries'],5)
        for j in range(5):
            v.edit(j,4,1.0).time([3])
        self.assertLessEqual(eng.memory_report()['complement_bytes'],64*8)

    def test_product_chain_composition(self):
        a=self.engine.chain(self.seeds[:2]); b=self.engine.chain(self.seeds[2:])
        c=a.convolve_with(b)
        np.testing.assert_allclose(c.dense(),self.root.dense(),atol=1e-9)

    def test_floating_not_bit_exact(self):
        self.assertEqual(self.root.dense().dtype,np.float64)

    def test_bad_input(self):
        with self.assertRaises(ValueError): self.engine.seed([1.0,float('nan')])
        with self.assertRaises(ValueError): self.engine.chain([])
        with self.assertRaises(IndexError): self.root.frequencies([self.n])
        with self.assertRaises(IndexError): self.root.edit(100,4,1)
        with self.assertRaises(ValueError): self.root.edit(2,1,float('inf'))
        with self.assertRaises(ValueError): self.root.convolve_with(ChainEngine().chain([ChainEngine().seed([1.0])]))

    def test_randomized_combinations(self):
        for _ in range(24):
            e=ChainEngine(max_bin_cache=128)
            n=int(self.rng.choice([8,16,32,64]))
            seeds=[e.seed(self.rng.normal(size=n)*0.3) for _ in range(4)]
            v=e.chain(seeds)
            for step in range(10):
                j=int(self.rng.integers(4))
                kind=int(self.rng.integers(3))
                if kind==0:v=v.edit(j,int(self.rng.integers(n)),float(self.rng.normal()))
                elif kind==1:v=v.shift(j,int(self.rng.integers(-n,n)))
                else:v=v.scale(j,float(self.rng.normal()))
            expected=brute([v.factor(j) for j in range(4)])
            np.testing.assert_allclose(v.dense(),expected,atol=1e-7,rtol=1e-7)
            bins=[0,n-1,int(self.rng.integers(n))]
            np.testing.assert_allclose(v.frequencies(bins),fft.fft(expected)[bins],atol=1e-6,rtol=1e-6)


if __name__=='__main__':unittest.main()
