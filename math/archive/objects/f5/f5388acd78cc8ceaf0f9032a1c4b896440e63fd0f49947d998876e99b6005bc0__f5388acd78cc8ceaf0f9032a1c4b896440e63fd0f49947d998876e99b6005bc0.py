"""Independent unit/mutation tests for Phase17. Run: python3 -m unittest -v test_phase17"""
import random,unittest,sys,cmath,math
sys.path.insert(0,__file__.rsplit('/',1)[0])
from green_sparse import (GreenSparse, candidate_library, transform_adaptive, direct_dft,
                          P0,G0,CyclicSolver,Cost)
from rational_forcing import (AllLengthGreen, general_root, rational_fraction,forcing_from_sparse,
                              direct_dft_any,bluestein_transform,inv_series,conv,PolyStats,prime_divisors)

PAIRS=[(3,P0,G0),(5,P0,G0),(7,998244353,3),(8,P0,G0),(15,P0,G0),
       (17,998244353,3),(30,P0,G0),(34,998244353,3),(60,P0,G0),
       (119,998244353,3),(128,P0,G0),(256,P0,G0)]

class Tests(unittest.TestCase):
    def setUp(self):self.rng=random.Random(20261010)

    def test_root_orders(self):
        for n,p,g in PAIRS:
            w=general_root(n,p,g)
            self.assertEqual(pow(w,n,p),1)
            self.assertTrue(all(pow(w,n//q,p)!=1 for q in prime_divisors(n)))

    def test_all_length_pruned_forcing(self):
        for n,p,g in PAIRS:
            e=AllLengthGreen(n,p,g)
            for k in sorted(set((0,1,2,3,min(7,n),n))):
                if k>n:continue
                entries={j:self.rng.randrange(1,p) for j in self.rng.sample(range(n),k)}
                actual,st=forcing_from_sparse(entries,n,e.omega,p,g)
                expected=direct_dft_any([entries.get(j,0) for j in range(n)],e.omega,p)
                self.assertEqual(actual,expected,(n,k))
                if k:
                    self.assertEqual(st.max_den_degree,k)
                    self.assertLessEqual(st.max_ntt_length,4*max(1,k))
                else:self.assertEqual(actual,[0]*n)

    def test_rational_polynomial_identity(self):
        for n,p,g in PAIRS:
            e=AllLengthGreen(n,p,g)
            for k in (1,2,min(7,n)):
                entries={j:self.rng.randrange(1,p) for j in self.rng.sample(range(n),k)}
                num,den=rational_fraction(entries,e.omega,p,g)
                self.assertEqual(len(num),k)
                self.assertEqual(len(den),k+1)
                b=min(32,1<<(k-1).bit_length())
                inv=inv_series(den,b,p,g)
                check=conv(den,inv,p,g)[:b]
                self.assertEqual(check,[1]+[0]*(b-1))
                out,_=forcing_from_sparse(entries,n,e.omega,p,g)
                check=conv(den,out,p,g)[:n]
                self.assertEqual(check,num+[0]*(n-len(num)))

    def test_green_intertwining_entire_basis(self):
        for n,p,g in [(3,P0,G0),(7,998244353,3),(17,998244353,3),(32,P0,G0),(60,P0,G0)]:
            e=AllLengthGreen(n,p,g)
            for j in range(n):
                x=[0]*n;x[j]=1
                f=direct_dft_any(x,e.omega,p)
                lf=e.L.apply(f)
                fp=direct_dft_any(e.P.apply(x),e.omega,p)
                self.assertEqual(lf,fp,(n,j))

    def test_dense_green_impulses(self):
        for n,p,g in PAIRS:
            e=AllLengthGreen(n,p,g)
            for j in sorted(set((0,n//3,n-1))):
                x=e.structured_dense({j:1})
                self.assertEqual(sum(bool(z) for z in x),n,(n,j))
                y,info=e.transform(x,'rational')
                self.assertEqual(info['K'],1)
                self.assertEqual(info['stats'].max_ntt_length,0) # K=1 never calls NTT
                self.assertEqual(y,direct_dft_any(x,e.omega,p))

    def test_all_length_full_vs_bluestein(self):
        for n,p,g in PAIRS:
            e=AllLengthGreen(n,p,g)
            for _ in range(4):
                x=[self.rng.randrange(p) for _ in range(n)]
                expected=direct_dft_any(x,e.omega,p)
                act,_=e.transform(x,method='bluestein')
                self.assertEqual(act,expected,(n,'full'))
                act,_=e.transform(x,method='auto')
                self.assertEqual(act,expected,(n,'auto'))

    def test_all_length_rational_dense_inputs(self):
        for n,p,g in PAIRS:
            e=AllLengthGreen(n,p,g)
            for k in (2,3,min(8,n)):
                entries={j:self.rng.randrange(1,p) for j in self.rng.sample(range(n),k)}
                x=e.structured_dense(entries)
                actual,info=e.transform(x,'rational')
                self.assertEqual(info['K'],k,(n,k))
                self.assertEqual(actual,direct_dft_any(x,e.omega,p),(n,k))

    def test_dyadic_input_pruning(self):
        for n in (2,4,8,16,64,256):
            e=GreenSparse(n)
            for k in sorted(set((0,1,2,min(9,n),n))):
                entries={j:self.rng.randrange(1,P0) for j in self.rng.sample(range(n),k)}
                y,co=e.pruned.from_entries(entries)
                self.assertEqual(y,direct_dft([entries.get(j,0) for j in range(n)],e.omega))
                if k:
                    self.assertLessEqual(co.node_size_sum,n*((k-1).bit_length()+2))
                self.assertLessEqual(co.ntt_mults,n*(n.bit_length()-1)//2)

    def test_dyadic_adaptive_multi_green(self):
        for n in (8,32,128):
            cs=candidate_library(n)
            for cand in cs:
                entries={self.rng.randrange(n):self.rng.randrange(1,P0)}
                x=cand.structured_dense(entries)
                actual,meta=transform_adaptive(x,cs)
                self.assertLessEqual(meta['K'],1)
                self.assertEqual(actual,direct_dft(x,cand.omega))
            x=[self.rng.randrange(P0) for _ in range(n)]
            actual,meta=transform_adaptive(x,cs)
            self.assertEqual(actual,direct_dft(x,cs[0].omega))

    def test_short_kernel_cache_is_exact_and_paid(self):
        for n,p,g in ((119,998244353,3),(256,P0,G0),(1024,P0,G0)):
            e=AllLengthGreen(n,p,g)
            k=min(32,n)
            data={j:self.rng.randrange(1,p) for j in self.rng.sample(range(n),k)}
            cached,stat=forcing_from_sparse(data,n,e.omega,p,g,cache_fixed_kernels=True)
            plain,oldstat=forcing_from_sparse(data,n,e.omega,p,g,cache_fixed_kernels=False)
            self.assertEqual(cached,plain)
            self.assertEqual(cached,direct_dft_any([data.get(j,0) for j in range(n)],e.omega,p))
            self.assertEqual(stat.cached_kernel_transforms,2)
            self.assertGreater(stat.cached_kernel_hits,0)
            self.assertGreater(stat.twiddle_tables_built,0)
            self.assertGreater(stat.twiddle_table_hits,0)
            self.assertGreater(stat.twiddle_plan_setup_mults,0)
            if n>=256:
                self.assertLess(stat.total_field_ops(),oldstat.total_field_ops())

    def test_kernel_cache_must_change_on_changed_support(self):
        e=AllLengthGreen(60,P0,G0)
        dat1={0:19,3:89,7:101}
        dat2={0:19,4:89,7:101}
        _,den1=rational_fraction(dat1,e.omega,e.p,e.primitive_gen)
        _,den2=rational_fraction(dat2,e.omega,e.p,e.primitive_gen)
        self.assertNotEqual(den1,den2)
        y1,st1=forcing_from_sparse(dat1,e.n,e.omega,e.p,e.primitive_gen)
        y2,st2=forcing_from_sparse(dat2,e.n,e.omega,e.p,e.primitive_gen)
        self.assertNotEqual(y1,y2)
        self.assertEqual(y2,direct_dft_any([dat2.get(j,0) for j in range(e.n)],e.omega,e.p))

    def test_mutation_wrong_fourier_phase(self):
        for n,p,g in ((8,P0,G0),(17,998244353,3),(60,P0,G0)):
            e=AllLengthGreen(n,p,g)
            x=[self.rng.randrange(p) for _ in range(n)]
            rwrong=[( (7+2*e.powers[j])*x[j]+x[j-1])%p for j in range(n)]
            wrong=e.L.solve(direct_dft_any(rwrong,e.omega,p))
            self.assertNotEqual(wrong,direct_dft_any(x,e.omega,p))

    def test_mutation_wrong_rational_denominator(self):
        e=AllLengthGreen(17,998244353,3)
        data={2:59,7:79,13:91}
        num,den=rational_fraction(data,e.omega,e.p,e.primitive_gen)
        mutated=list(den)
        mutated[1]=(-mutated[1])%e.p
        self.assertNotEqual(mutated,den)
        self.assertNotEqual(conv(mutated,direct_dft_any([data.get(j,0) for j in range(e.n)],e.omega,e.p),e.p,e.primitive_gen)[:e.n],num+[0]*(e.n-len(num)))

    def test_green_solve_both_directions(self):
        for n,p,g in PAIRS:
            e=AllLengthGreen(n,p,g)
            for solver in (e.L,e.P):
                rhs=[self.rng.randrange(p) for _ in range(n)]
                self.assertEqual(solver.apply(solver.solve(rhs)),rhs)

    def test_rational_ntt_small_call_restriction(self):
        for n,p,g in ((60,P0,G0),(119,998244353,3),(256,P0,G0)):
            e=AllLengthGreen(n,p,g)
            k=4
            data={j:11+j for j in range(k)}
            _,stat=forcing_from_sparse(data,n,e.omega,p,g)
            self.assertLessEqual(stat.max_ntt_length,4*k)
            self.assertGreaterEqual(stat.rational_blocks,(n+k-1)//k)

    def test_complex_norm_certificate(self):
        try:import numpy as np
        except ImportError:self.skipTest('numpy is not installed')
        for n in (8,16,32):
            w=np.exp(-2j*np.pi/n)
            diag=7+w**np.arange(n)
            mat=np.diag(diag)+2*np.roll(np.eye(n),1,axis=0)
            self.assertLessEqual(np.linalg.cond(mat),2.5+1e-9)
            rng=np.random.default_rng(n)
            x=rng.normal(size=n)+1j*rng.normal(size=n)
            right=7*x+np.roll(x,1)+2*w**(-np.arange(n))*x
            true=np.fft.fft(x)/np.sqrt(n)
            out=np.linalg.solve(mat,np.fft.fft(right)/np.sqrt(n))
            self.assertLess(np.linalg.norm(out-true),1e-10)
            indices=np.argsort(np.abs(right))[-max(1,n//4):]
            short=np.zeros(n,dtype=complex);short[indices]=right[indices]
            approx=np.linalg.solve(mat,np.fft.fft(short)/np.sqrt(n))
            err=np.linalg.norm(true-approx)
            tail=np.linalg.norm(right-short)
            self.assertLessEqual(err,tail/4+1e-10)
            self.assertGreaterEqual(err,tail/10-1e-10)

if __name__=='__main__':unittest.main(verbosity=2)
