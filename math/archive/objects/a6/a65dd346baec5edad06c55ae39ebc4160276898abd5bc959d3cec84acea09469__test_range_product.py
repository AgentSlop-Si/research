import unittest
import numpy as np
from range_product import FrozenProductIndex, SegmentProductIndex
from projected_circuit import ProjectedCircuit


class RangeProducts(unittest.TestCase):
    def test_all_intervals_odd_and_power_two_lengths(self):
        rng=np.random.default_rng(821)
        for m in (1,2,3,7,16,65):
            a=1+rng.normal(0,.01,(m,7))+1j*rng.normal(0,.01,(m,7))
            a[m//2,2]=0
            index=FrozenProductIndex(64,range(7),a)
            for lo in range(m+1):
                for hi in range(lo,m+1):
                    np.testing.assert_allclose(index.interval(lo,hi),np.prod(a[lo:hi],axis=0),rtol=2e-12,atol=1e-12)

    def test_replacements_zeros_and_persistence(self):
        rng=np.random.default_rng(822)
        for m in (1,7,64,512):
            n,q=64,5
            a=1+rng.normal(0,.01,(m,q))
            a[m//2,3]=0
            ix=FrozenProductIndex(n,[0,1,7,31,63],a)
            root=ix.branch()
            cases=[(root,a.astype(complex))]
            for _ in range(15):
                v,reference=cases[int(rng.integers(len(cases)))];reference=reference.copy()
                edits=[]
                for _ in range(3):
                    at=int(rng.integers(m));pos=int(rng.integers(n));d=.01j
                    edits.append((at,pos,d))
                    reference[at] += d*np.exp((-2j*np.pi/n)*((ix.bins*pos)%n))
                nv=v.edit_many(edits)
                expected=np.prod(reference,axis=0)
                for method in ('range','vector','auto'):
                    np.testing.assert_allclose(nv.query(method),expected,rtol=2e-12,atol=1e-12)
                cases.append((nv,reference))
            np.testing.assert_allclose(root.query(),np.prod(a,axis=0))

    def test_circuit_adapter(self):
        e=ProjectedCircuit(16,[0,1,9])
        nodes=[e.register_projection([1+i*.01]*3) for i in range(8)]
        v=e.product(nodes)
        ix=FrozenProductIndex.from_circuit(v)
        np.testing.assert_allclose(ix.branch().edit_many([(2,3,.1)]).query('range'),v.edit(2,3,.1).frequencies())

    def test_segment_api_and_all_intervals(self):
        rng=np.random.default_rng(888)
        for m in (1,7,16,65):
            values=1+rng.normal(0,.01,(m,3))
            values[m//2,1]=0
            a=FrozenProductIndex(16,[0,1,15],values)
            b=SegmentProductIndex(16,[0,1,15],values)
            for lo in range(m+1):
                for hi in range(lo,m+1):
                    np.testing.assert_allclose(a.interval(lo,hi),b.interval(lo,hi),atol=1e-12)
            events=[(0,2,.01),(m-1,3,.02)]
            np.testing.assert_allclose(a.branch().edit_many(events).query('range'),
                                       b.branch().edit_many(events).query('range'))

    def test_memory_gate_and_input_validation(self):
        with self.assertRaises(MemoryError):FrozenProductIndex(8,[0,1],np.ones((64,2)),max_table_bytes=1)
        ix=FrozenProductIndex(8,[0,1],np.ones((4,2)))
        with self.assertRaises(IndexError):ix.interval(-1,2)
        with self.assertRaises(IndexError):ix.branch().edit_many([(4,1,1)])
        with self.assertRaises(TypeError):ix.branch().edit_many([(1.5,1,1)])
        with self.assertRaises(ValueError):ix.branch().edit_many([(1,1,np.inf)])
        self.assertEqual(ix.memory_report()['interval_table_bytes'],2*4*2*16)


if __name__=='__main__':unittest.main()
