from collections import deque
import unittest
from unittest.mock import patch
import numpy as np
from scipy import fft
from projected_circuit import ProjectedCircuit
from algebra_projection import import_algebra,prepare_projected_jet
from baseline_sum_product_v8.algebra_fft import AlgebraFFT,DegreeExceeded
from multi_view import SharedProjectedFourierStore
from view_optimizer import AdaptiveSpectralOrganizer
from test_replay_repairs import Counted


class AlgebraIntegration(unittest.TestCase):
    def test_import_and_repeated_leaf_jet_without_transforms(self):
        rng=np.random.default_rng(929)
        for n in (17,64):
            x=rng.normal(size=n)*.01;x[0]+=1
            b=rng.normal(size=n)*.01
            src=AlgebraFFT(n)
            a,bb=src.signal(x),src.signal(b)
            root=src.add(src.mul(a,a,a),src.scale(src.mul(a,bb),2),src.impulse(5,.25))
            bins=[0,1,n//2,n-1]
            with (patch.object(fft,'rfft',side_effect=AssertionError('no forward transform')),
                  patch.object(fft,'irfft',side_effect=AssertionError('no inverse transform'))):
                target=ProjectedCircuit(n,bins)
                node=import_algebra(src,[root],target)[0]
                jet=prepare_projected_jet(src,root,a,bins)
            base=fft.fft(x)**3+2*fft.fft(x)*fft.fft(b)+.25*np.exp(-2j*np.pi*np.arange(n)*5/n)
            np.testing.assert_allclose(target.query(node),base[bins],atol=2e-12)
            self.assertEqual(jet.degree,3)
            self.assertEqual(jet.coefficients.nbytes,4*len(bins)*16)
            edits=[(3,.02),(7,-.01),(3,.01)]
            revised=x.copy()
            for p,d in edits:revised[p]+=d
            expected=fft.fft(revised)**3+2*fft.fft(revised)*fft.fft(b)+.25*np.exp(-2j*np.pi*np.arange(n)*5/n)
            np.testing.assert_allclose(jet.many(edits),expected[bins],atol=2e-12)

    def test_degree_guard_and_empty_edits(self):
        src=AlgebraFFT(8);a=src.signal(np.arange(8)/8)
        root=src.mul(a,a,a,a,a)
        with self.assertRaises(DegreeExceeded):prepare_projected_jet(src,root,a,[0,1])
        jet=prepare_projected_jet(src,root,a,[0,1],max_degree=5)
        np.testing.assert_allclose(jet.many([]),fft.fft(np.arange(8)/8)[[0,1]]**5)


class OptimizerRepairs(unittest.TestCase):
    def make(self,budget=100000):
        store=SharedProjectedFourierStore(32,[0,1,2],np.ones((8,3)),
                     {'a':[0,1],'b':[1,2]},promote_after=None)
        opt=AdaptiveSpectralOrganizer(store,max_group_cache_bytes=budget,partition_history_limit=3)
        opt.groups.clear();opt.member_group.clear()
        g=opt._install_group(('a','b'),sync=1,overlap=4/3,benefit=4/3)
        opt._all_singletons=False;opt._seed_from_member_caches(g);opt._touch_group_cache(g)
        return store,opt,g

    def test_group_reads_only_unread_tail(self):
        s,o,g=self.make()
        for _ in range(10000):s.add_coefficient(0,.125)
        o._group_query(g,'a')
        s.events=Counted(s.events)
        s.add_coefficient(0,1)
        np.testing.assert_allclose(o._group_query(g,'a'),[1251,1251])
        self.assertEqual(s.events.visits,1)

    def test_group_publishes_only_requested_view(self):
        s,o,g=self.make();s.add_coefficient(0,1)
        o._group_query(g,'a')
        self.assertEqual(o.stats.published_bins,2)
        self.assertNotEqual(s.views['b'].version,s.version)
        o._group_query(g,'b')
        self.assertEqual(o.stats.published_bins,4)
        np.testing.assert_allclose(s.views['b'].cached,[1,1])

    def test_zero_budget_fallback_and_bounded_diagnostics(self):
        s,o,g=self.make(0)
        for _ in range(20):
            o.add_coefficient(0,.125);np.testing.assert_allclose(o.query('a'),s.query('a'))
            o.replan()
        self.assertEqual(o.memory_report()['group_cache_bytes'],0)
        self.assertLessEqual(len(o.stats.partitions),3)
        self.assertGreater(o.stats.planning_ns,0)

    def test_budget_eviction_and_missing_history(self):
        s,o,g=self.make(48)
        other=o._install_group(('a',),sync=1,overlap=1,benefit=1)
        other.cached=np.ones(2,dtype=complex);other.version=s.version;o._touch_group_cache(other)
        self.assertIsNone(g.cached)
        self.assertLessEqual(o.memory_report()['group_cache_bytes'],48)
        s.event_capacity=0;s.add_coefficient(0,2)
        np.testing.assert_allclose(o._group_query(g,'a'),[2,2])
        self.assertGreater(o.stats.group_rebuilds,0)


if __name__=='__main__':unittest.main()
