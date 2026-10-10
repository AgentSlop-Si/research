"""Independent audit regressions and reference comparisons."""
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
from scipy import fft

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from cost_aware_fft import RelationFFT, Profile
from persistent_chain import ChainEngine
from relational_convolution import RelationalConvolver, subscribe_convolution


class HardeningTests(unittest.TestCase):
    def test_explicit_strategy_validation_independent_of_cache(self):
        for n in (7,8):
            for cached in (False,True):
                e=RelationFFT()
                s=e.register(np.arange(n,dtype=float)).edit(1,2.)
                if cached:s.spectrum('native',cache_output=True)
                for method in ('reuse','zero','linear'):
                    with self.subTest(n=n,cached=cached,method=method):
                        with self.assertRaises(ValueError):s.spectrum(method)
                if n==7:
                    with self.assertRaises(ValueError):s.spectrum('pruned')
                else:
                    e.max_temp_bytes=0
                    with self.assertRaises(MemoryError):s.spectrum('pruned')

    def test_compatible_cached_output_is_preserved(self):
        e=RelationFFT()
        s=e.register(np.arange(16.)).edit(2,.25)
        expected=s.spectrum('native',cache_output=True)
        for method in ('auto','native','direct','pruned'):
            np.testing.assert_array_equal(s.spectrum(method),expected)
        s.edit(2,-.25)
        self.assertIsNone(s._cached_output)
        np.testing.assert_allclose(s.spectrum('reuse'),fft.rfft(np.arange(16.)))

    def test_calibrated_pruned_choice_rechecks_changed_budget(self):
        e=RelationFFT()
        s=e.register(np.arange(16.)).edit(3,1.)
        # Deterministically model a valid calibration winner without making
        # the test depend on host timing or requiring slow fake benchmarks.
        e._profiles[e._profile_key(s)]=Profile(16,1,1,False,{'pruned':1e-6},'pruned')
        self.assertEqual(e.recommend(s),'pruned')
        e.max_temp_bytes=0
        self.assertNotEqual(e.recommend(s),'pruned')
        np.testing.assert_allclose(s.spectrum(),fft.rfft(s.signal()))

    def test_subscription_rejected_overflow_is_atomic(self):
        for side in ('left','right'):
            e=RelationFFT()
            big=e.register([0.,0.]).edit(0,1e308)
            small=e.register([1e-308,0.])
            a,b=(big,small) if side=='left' else (small,big)
            sub=subscribe_convolution(RelationalConvolver().product(a,b),[0,1])
            before=sub.values()
            with self.assertRaises(ValueError):sub.edit(side,0,1e308)
            np.testing.assert_array_equal(sub.values(),before)
            np.testing.assert_allclose(sub.values(),[sub.snapshot_view().at(i) for i in (0,1)])
            self.assertEqual(sub.events,0)
            sub.edit(side,0,-1e308)
            np.testing.assert_allclose(sub.values(),[0.,0.],atol=1e-14)

    def test_complex_seeds_rejected(self):
        for invalid in (np.array([1+2j,3+4j]),['1','2'],[np.inf],[np.nan],[],[[1,2]]):
            with self.subTest(invalid=repr(invalid)):
                with self.assertRaises(ValueError):ChainEngine().seed(invalid)

    def test_sequential_composition_deep_lookup_rewrite_and_bins(self):
        for budget in (0,1,10000):
            e=ChainEngine(max_bin_cache=budget)
            single=e.chain([e.seed([1.,0.,0.])])
            v=single
            for _ in range(1099):v=v.convolve_with(single)
            self.assertIs(v.factor(0),single.factor(0))
            w=v.edit(0,1,.25).edit(1,2,.5)
            expected=np.array([1.125,.25,.5])
            np.testing.assert_allclose(w.dense('native'),expected,atol=1e-12)
            np.testing.assert_allclose(w.frequencies([0,1,2]),fft.fft(expected),atol=1e-12)
            np.testing.assert_allclose(w.frequencies([0,1,2]),fft.fft(expected),atol=1e-12)
            np.testing.assert_allclose(v.dense(),[1.,0.,0.],atol=1e-12)
            self.assertEqual(v.root.size,1100)

    def test_cross_engine_operations_rejected(self):
        e1,e2=RelationFFT(),RelationFFT()
        a,b=e1.register([1.,2.]),e2.register([3.,4.])
        with self.assertRaises(ValueError):e1.combine([a,b],[1.,1.])
        c1,c2=ChainEngine(),ChainEngine()
        f1,f2=c1.seed([1.,2.]),c2.seed([3.,4.])
        v1,v2=c1.chain([f1]),c2.chain([f2])
        with self.assertRaises(ValueError):c1.chain([f2])
        with self.assertRaises(ValueError):v1.with_factor(0,f2)
        with self.assertRaises(ValueError):v1.convolve_with(v2)

    def test_cross_engine_sharing_diagnostic_uses_object_identity(self):
        c1,c2=ChainEngine(),ChainEngine()
        v1=c1.chain([c1.seed([1.,2.])])
        v2=c2.chain([c2.seed([3.,4.])])
        self.assertIsNot(v1.root,v2.root)
        self.assertEqual(v1.count_reused_nodes(v2)['shared_nodes'],0)
        self.assertEqual(v1.count_reused_nodes(v1)['shared_nodes'],1)


class IndependentReferenceTests(unittest.TestCase):
    @staticmethod
    def direct_convolution(arrays):
        n=len(arrays[0]);out=np.zeros(n);out[0]=1.
        for a in arrays:
            out=sum((a[t]*np.roll(out,t) for t in range(n)),np.zeros(n))
        return out

    def test_random_persistent_sequences(self):
        rng=np.random.default_rng(9175)
        for trial in range(400):
            n=int(rng.choice([1,2,3,5,7,8,16,17]))
            e=ChainEngine(max_bin_cache=int(rng.choice([0,1,7,1000])),
                          max_base_bytes=int(rng.choice([0,n*8,n*16])),
                          max_complement_bytes=int(rng.choice([0,n*8,n*16])))
            seeds=[e.seed(rng.normal(0,.25,size=n)) for _ in range(4)]
            m=int(rng.integers(1,7));v=e.chain([seeds[int(rng.integers(4))] for _ in range(m)])
            original=v
            old=self.direct_convolution([v.factor(i).values() for i in range(m)])
            for step in range(12):
                at=int(rng.integers(m));kind=int(rng.integers(4))
                if kind==0:v=v.edit(at,int(rng.integers(n)),float(rng.normal(0,.2)))
                elif kind==1:v=v.shift(at,int(rng.integers(-10*n,10*n)))
                elif kind==2:v=v.scale(at,float(rng.choice([0.,1.,-.5,1.25])))
                else:v=v.with_factor(at,seeds[int(rng.integers(4))])
            expected=self.direct_convolution([v.factor(i).values() for i in range(m)])
            for method in ('native','auto'):
                np.testing.assert_allclose(v.dense(method),expected,rtol=1e-10,atol=1e-11)
            if len(v._modified)<=1:
                np.testing.assert_allclose(v.dense('sparse'),expected,rtol=1e-10,atol=1e-11)
            qs=[0,n//2,n-1]
            np.testing.assert_allclose(v.time(qs),expected[qs],rtol=1e-10,atol=1e-11)
            np.testing.assert_allclose(v.frequencies(np.arange(n)),fft.fft(expected),rtol=1e-10,atol=1e-11)
            np.testing.assert_allclose(original.dense(),old,rtol=1e-10,atol=1e-11)

    def test_phase5_import_random_states(self):
        rng=np.random.default_rng(298)
        for n in (1,3,8,17,64):
            upstream=RelationFFT()
            a=upstream.register(rng.normal(size=n)).shift(-3).edit(0,.5)
            b=upstream.register(rng.normal(size=n)).edit(n-1,-.25)
            for states in ([a],[a,b],[upstream.combine([a,b],[.2,.8]),a],
                           [upstream.combine([a,a],[1.,-1.]),b]):
                engine=ChainEngine()
                v=engine.from_phase5(states)
                expected=self.direct_convolution([s.signal() for s in states])
                np.testing.assert_allclose(v.dense(),expected,rtol=1e-10,atol=1e-10)
                np.testing.assert_allclose(v.frequencies(np.arange(n)),fft.fft(expected),rtol=1e-10,atol=1e-10)

    def test_subscription_random_rebuilds(self):
        rng=np.random.default_rng(1021)
        for n in (1,3,16,31):
            upstream=RelationFFT()
            a=upstream.register(rng.normal(size=n)).shift(1)
            b=upstream.register(rng.normal(size=n)).shift(3)
            view=RelationalConvolver().product(a,b)
            sub=subscribe_convolution(view,range(n))
            for _ in range(200):
                side='left' if rng.integers(2) else 'right'
                sub.edit(side,int(rng.integers(n)),float(rng.normal()))
                rebuilt=sub.snapshot_view()
                expected=self.direct_convolution([rebuilt.left.signal(),rebuilt.right.signal()])
                np.testing.assert_allclose(sub.values(),expected,rtol=1e-10,atol=1e-10)

if __name__=='__main__':unittest.main()
