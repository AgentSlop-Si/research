"""Correctness tests: independent SciPy and direct exact modular convolution."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import unittest
from types import SimpleNamespace
import numpy as np
from scipy import fft
from algebra_fft import AlgebraFFT
from compiled_kernels import compile_expression, compile_prepared


class CompiledKernelTests(unittest.TestCase):
    def setUp(self):
        self.rng=np.random.default_rng(9001)

    def make(self,n,degree):
        engine=AlgebraFFT(n)
        arrays=[self.rng.standard_normal(n)/np.sqrt(n) for _ in range(4)]
        a,b,c,d=[engine.signal(v) for v in arrays]
        if degree==0:
            root=engine.add(engine.mul(b,c),d)
        elif degree==1:
            root=engine.add(engine.mul(a,b),engine.mul(c,d))
        elif degree==2:
            root=engine.add(engine.mul(a,a),engine.mul(b,c))
        elif degree==3:
            root=engine.add(engine.mul(a,a,a),engine.scale(engine.mul(a,b),2),engine.mul(c,d))
        elif degree==4:
            root=engine.add(engine.mul(a,a,a,a),engine.mul(b,c))
        else:
            raise ValueError(degree)
        return engine, root, a, arrays

    def test_python_backend_all_degrees(self):
        for n in (16,35,128):
            for degree in range(5):
                with self.subTest(n=n,degree=degree):
                    eng,root,leaf,arrays=self.make(n,degree)
                    pre=eng.prepare(root,leaf,max_degree=4)
                    jit=compile_prepared(pre,backend='python',max_degree=4)
                    for pos,delta in ((0,.13),(n-1,-.07),(n//2,.12)):
                        expected=arrays[0].copy();expected[pos]+=delta
                        a,b,c,d=expected,arrays[1],arrays[2],arrays[3]
                        A,B,C,D=[fft.rfft(v) for v in (a,b,c,d)]
                        if degree==0: spectrum=B*C+D
                        elif degree==1:spectrum=A*B+C*D
                        elif degree==2:spectrum=A*A+B*C
                        elif degree==3:spectrum=A*A*A+2*A*B+C*D
                        else:spectrum=A**4+B*C
                        desired=fft.irfft(spectrum,n=n)
                        np.testing.assert_allclose(jit.single(pos,delta),desired,rtol=2e-9,atol=2e-9)
                        inds=np.array([0,1,n//2,n-1])
                        np.testing.assert_allclose(jit.single(pos,delta,inds),desired[inds],atol=2e-9)
                    self.assertLess(len(jit.generated_source),20000)

    def test_numba_backend_quadratic_cubic_sparse(self):
        for degree in (1,2,3,4):
            eng,root,leaf,arrays=self.make(128,degree)
            plan=compile_expression(eng,root,leaf,backend='numba',max_degree=4)
            orig=eng.prepare(root,leaf,max_degree=4)
            self.assertEqual(plan.backend,'numba')
            self.assertGreater(len(plan._full.signatures),0)
            for pos,delta in ((0,.01),(5,-.003),(127,.2)):
                np.testing.assert_allclose(plan.single(pos,delta),orig.single(pos,delta),atol=1e-9,rtol=1e-9)
                idx=np.array([0,12,127,5,5])
                np.testing.assert_allclose(plan.single(pos,delta,idx),orig.single(pos,delta,indices=idx),atol=1e-9)

    def test_partial_empty_and_errors(self):
        eng,root,leaf,_=self.make(64,3)
        plan=compile_expression(eng,root,leaf)
        self.assertEqual(plan.single(0,0.0,indices=[]).size,0)
        with self.assertRaises(IndexError):plan.single(-1,0.1)
        with self.assertRaises(IndexError):plan.single(64,0.1)
        with self.assertRaises(ValueError):plan.single(0,float('nan'))
        with self.assertRaises(IndexError):plan.single(0,.1,[64])
        with self.assertRaises(TypeError):plan.single(0,.1,[0.2])
        self.assertEqual(plan.data_bytes,plan.base.nbytes+plan.dense.nbytes+plan.sparse_positions.nbytes+plan.sparse_amplitudes.nbytes)

    def test_compilation_bound(self):
        eng,root,leaf,_=self.make(32,4)
        with self.assertRaises(ValueError):compile_expression(eng,root,leaf,max_degree=3)


def circular_mod(a,b,p):
    n=len(a)
    out=[0]*n
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            out[(i+j)%n]=(out[(i+j)%n]+x*y)%p
    return out

class ExactModularAudit(unittest.TestCase):
    def test_exact_jet_kernel_120_trials(self):
        rng=np.random.default_rng(700)
        for prime in (17,97,257):
            for trial in range(40):
                n=11 if trial%2 else 16
                a=rng.integers(0,prime,size=n).tolist()
                b=rng.integers(0,prime,size=n).tolist()
                c=rng.integers(0,prime,size=n).tolist()
                pos=int(rng.integers(0,n)); d=int(rng.integers(-5,6))
                # F(a)=a*a*a+2a*b+c.  Independent schoolbook modular oracle.
                aa=circular_mod(a,a,prime)
                aaa=circular_mod(aa,a,prime)
                ab=circular_mod(a,b,prime)
                k0=[(aaa[i]+2*ab[i]+c[i])%prime for i in range(n)]
                k1=[(3*aa[i]+2*b[i])%prime for i in range(n)]
                k2=[(3*a[i])%prime for i in range(n)]
                src=SimpleNamespace(n=n,degree=3,kernels=(np.array(k0,dtype=np.float64),np.array(k1,dtype=np.float64),np.array(k2,dtype=np.float64),None),sparse_coefficients=(None,None,None,{0:1.0}))
                plan=compile_prepared(src,backend='python',max_degree=3)
                got=np.rint(plan.single(pos,d)).astype(np.int64)%prime
                changed=list(a); changed[pos]=(changed[pos]+d)%prime
                bb=circular_mod(changed,changed,prime)
                bbb=circular_mod(bb,changed,prime)
                cb=circular_mod(changed,b,prime)
                wanted=np.array([(bbb[i]+2*cb[i]+c[i])%prime for i in range(n)],dtype=np.int64)
                np.testing.assert_array_equal(got,wanted)

if __name__=='__main__':unittest.main()
