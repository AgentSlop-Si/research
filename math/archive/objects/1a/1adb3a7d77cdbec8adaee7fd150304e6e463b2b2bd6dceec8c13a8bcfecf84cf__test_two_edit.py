"""Numerical & exact modular independent checks for Phase 10."""
import ctypes
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
from scipy import fft

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from algebra_fft import AlgebraFFT, DegreeExceeded
from two_edit_engine import prepare_two


def circular_mod(a,b,p):
    n=len(a)
    out=[0]*n
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            out[(i+j)%n]=(out[(i+j)%n]+int(x)*int(y))%p
    return out


def slow_expression(a,b,c,d,p):
    aa=circular_mod(a,a,p)
    aab=circular_mod(aa,b,p)
    ab=circular_mod(a,b,p)
    bb=circular_mod(b,b,p)
    cd=circular_mod(c,d,p)
    return np.array([(aab[i]+ab[i]+bb[i]+cd[i])%p for i in range(len(a))], dtype=np.int64)


def experiment(n,seed=22):
    rng=np.random.default_rng(seed)
    arrays=[rng.normal(size=n)/np.sqrt(n) for _ in range(4)]
    eng=AlgebraFFT(n)
    a,b,c,d=[eng.signal(arr) for arr in arrays]
    root=eng.add(eng.mul(a,a,b),eng.mul(a,b),eng.mul(b,b),eng.mul(c,d))
    return eng,root,a,b,arrays


class TestTwoEdit(unittest.TestCase):
    def test_native_available_and_no_runtime_jit(self):
        eng,root,a,b,_=experiment(16)
        p=prepare_two(eng,root,a,b)
        self.assertTrue(p.shape_available)
        self.assertTrue(p.native_available,'AOT compilation missing from packaged distribution')
        self.assertEqual(p.total_degree,5)
        self.assertEqual(p.dense.shape[1],16)
        self.assertEqual(set(p.symbolic_terms),
            {(0,0),(0,1),(0,2),(1,0),(1,1),(2,0),(2,1)})
        self.assertTrue(all(v.flags.c_contiguous for v in [p.base,p.dense,p.dense_a,p.sparse_a]))
        self.assertFalse(p.base.flags.writeable)

    def test_both_edits_same_or_different_locations(self):
        for n in (11,16,32,127,1024):
            eng,root,a,b,arrays=experiment(n)
            plan=prepare_two(eng,root,a,b)
            for pos_a,pos_b in ((0,0),(1,n-1),(n//2,n//2),(n-1,0)):
                for da,db in ((.12,.03),(-.04,.01),(0.,-.06),(.07,0.),(0.,0.)):
                    a2=arrays[0].copy();b2=arrays[1].copy()
                    a2[pos_a]+=da;b2[pos_b]+=db
                    fa,fb,fc,fd=[fft.rfft(x) for x in (a2,b2,arrays[2],arrays[3])]
                    ref=fft.irfft(fa*fa*fb+fa*fb+fb*fb+fc*fd,n=n)
                    for backend in ('native','numpy','auto','aot_shape'):
                        got=plan.update(pos_a,da,pos_b,db,backend=backend)
                        np.testing.assert_allclose(got,ref,atol=8e-11,rtol=5e-10)
                        qs=np.array([0,n-1,0,n//2],dtype=np.int64)
                        part=plan.update(pos_a,da,pos_b,db,indices=qs,backend=backend)
                        np.testing.assert_allclose(part,ref[qs],atol=8e-11,rtol=5e-10)
            self.assertGreater(plan.number_symbolic_nodes,0)

    def test_exact_modular_independent_schoolbook(self):
        rng=np.random.default_rng(144)
        count=0
        for n in (7,12,17):
            for p in (7,17,101,257):
                for _ in range(32):
                    arrays=[rng.integers(0,6,size=n).tolist() for j in range(4)]
                    eng=AlgebraFFT(n)
                    a,b,c,d=[eng.signal(x) for x in arrays]
                    root=eng.add(eng.mul(a,a,b),eng.mul(a,b),eng.mul(b,b),eng.mul(c,d))
                    plan=prepare_two(eng,root,a,b)
                    sa=int(rng.integers(0,n));sb=int(rng.integers(0,n))
                    da=int(rng.integers(-4,5));db=int(rng.integers(-4,5))
                    edited_a=list(arrays[0]);edited_b=list(arrays[1])
                    edited_a[sa]+=da;edited_b[sb]+=db
                    expected=slow_expression(edited_a,edited_b,*arrays[2:],p)
                    for backend in ('numpy','native','aot_shape'):
                        got=np.rint(plan.update(sa,da,sb,db,backend=backend)).astype(np.int64)%p
                        np.testing.assert_array_equal(got,expected)
                    count+=1
        self.assertEqual(count,384)

    def test_other_dag_structures_and_shared_inputs(self):
        rng=np.random.default_rng(91)
        n=87
        v=[rng.normal(size=n)/np.sqrt(n) for _ in range(3)]
        eng=AlgebraFFT(n)
        a,b,c=[eng.signal(x) for x in v]
        roots=[eng.add(eng.mul(a,b),eng.mul(a,b)),
               eng.mul(eng.add(a,b),eng.add(a,b)),
               eng.add(eng.mul(a,a,a),eng.mul(b,b,b)),
               eng.add(eng.mul(a,c),eng.mul(b,c)),
               eng.mul(c,c)]
        for root in roots:
            plan=prepare_two(eng,root,a,b,max_total_degree=6)
            for pa,pb,da,db in ((3,19,.1,-.07),(5,5,.1,.2)):
                aa=v[0].copy();bb=v[1].copy();aa[pa]+=da;bb[pb]+=db
                x=eng.signal(aa);y=eng.signal(bb)
                edited=eng.replace(root,a,x)
                edited=eng.replace(edited,b,y)
                ref=eng.evaluate_time(edited)
                np.testing.assert_allclose(plan.update(pa,da,pb,db),ref,atol=2e-10,rtol=1e-9)

    def test_mixed_terms_not_independent_single_edits(self):
        eng,root,a,b,_=experiment(91)
        plan=prepare_two(eng,root,a,b)
        self.assertEqual(plan.linear_direct_coefficients,2)
        aa=plan.update(11,.3,23,0,backend='aot_shape')
        bb=plan.update(11,0,23,.5,backend='aot_shape')
        both=plan.update(11,.3,23,.5,backend='aot_shape')
        base=plan.update(11,0,23,0,backend='aot_shape')
        # Mixed degree (1,1) and (2,1) are genuine, not optional.
        self.assertGreater(float(np.linalg.norm(both-aa-bb+base)),1e-4)

    def test_offline_source_rejects_unbounded_code_generation(self):
        from offline_codegen import generate_source, DEFAULT_SHAPE
        good=generate_source(DEFAULT_SHAPE)
        self.assertIn('fft10_shape_eval',good)
        self.assertNotIn('exec(',good)
        with self.assertRaises(ValueError):
            generate_source({'dense':[[0,1],[0,1]],'sparse':[]})
        with self.assertRaises(ValueError):
            generate_source({'dense':[[99,0]],'sparse':[]})
        eng,root,a,b,_=experiment(27)
        mismatched=eng.mul(a,b)
        plan=prepare_two(eng,mismatched,a,b)
        self.assertFalse(plan.shape_available)
        with self.assertRaises(RuntimeError):
            plan.update(0,.1,0,.2,backend='aot_shape')
        # Auto must fall back without a runtime compiler.
        np.testing.assert_allclose(plan.update(0,.1,0,.2,backend='auto'),
                                   plan.update(0,.1,0,.2,backend='numpy'))

    def test_error_paths(self):
        eng,root,a,b,_=experiment(19)
        plan=prepare_two(eng,root,a,b)
        with self.assertRaises(ValueError):prepare_two(eng,root,a,a)
        with self.assertRaises(DegreeExceeded):prepare_two(eng,root,a,b,max_total_degree=2)
        with self.assertRaises(MemoryError):prepare_two(eng,root,a,b,max_kernel_bytes=10)
        with self.assertRaises(IndexError):plan.update(-1,1,1,1)
        with self.assertRaises(IndexError):plan.update(2,1,19,1)
        with self.assertRaises(ValueError):plan.update(1,float('nan'),1,1)
        with self.assertRaises(TypeError):plan.update(1,1,1,1,indices=[2.1])
        with self.assertRaises(IndexError):plan.update(1,1,1,1,indices=[19])
        with self.assertRaises(ValueError):plan.update(1,1,1,1,backend='broken')
        self.assertEqual(plan.update(1,0,1,0,indices=[]).size,0)
        from two_edit_engine import _native_path
        with patch('two_edit_engine._native_path',return_value=None), patch('two_edit_engine._matching_shape',return_value=None):
            with self.assertRaises(RuntimeError):plan.update(1,.1,1,.1,backend='native')
            got=plan.update(1,.1,1,.1,backend='auto')
            self.assertTrue(np.all(np.isfinite(got)))

if __name__=='__main__':
    unittest.main()
