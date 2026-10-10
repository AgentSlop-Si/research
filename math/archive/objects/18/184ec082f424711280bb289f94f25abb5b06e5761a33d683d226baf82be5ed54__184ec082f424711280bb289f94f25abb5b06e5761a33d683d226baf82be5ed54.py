"""Independent exact checks for four-leg Fourier tensor cut ranks and basis costs."""
import itertools
import random
import unittest

import numpy as np

from phase6 import (
    field_for_length, fourier_tensor, flatten, rank_mod, cut_ranks,
    endpoint_sparse_core, endpoint_gauges, transform_legs, random_invertible,
    matmul, nnz, dft_matrix, invert_mod, exact_dft,
    charged_two_axis_fft, unitary_cut_singular_values,
    crossed_partial_fourier, identity,
)


def count_tensor(T):
    return sum(z!=0 for a in T for b in a for c in b for z in c)


class TestPhase6(unittest.TestCase):
    def test_raw_polyphase_factor_matches_raw_dft_matrix(self):
        for q,m in ((2,2),(3,4),(4,3),(4,4),(6,4),(8,8)):
            p,w=field_for_length(q*m)
            T=fourier_tensor(q,m,p,w)
            for s in range(q):
                for h in range(m):
                    for t in range(q):
                        for u in range(m):
                            self.assertEqual(T[s][h][t][u],pow(w,(-((h+m*s)*(t+q*u)))%(q*m),p))

    def test_all_three_exact_balanced_cut_ranks(self):
        for q,m in ((2,2),(2,3),(3,2),(3,4),(4,3),(4,4),(4,6),(6,4),(8,8)):
            p,w=field_for_length(q*m)
            self.assertEqual(cut_ranks(q,m,p,w),{
                'output_input':q*m,'crossed':min(q,m),'alternating':q*m})

    def test_explicit_optimal_cp_rank_n_decomposition(self):
        # The full Fourier 4-tensor has CP rank exactly N: flattening gives
        # lower bound N, the expansion below gives N separable four-leg atoms.
        for q,m in ((2,3),(3,4),(4,4)):
            n=q*m;p,w=field_for_length(n)
            xi=pow(w,m,p);eta=pow(w,q,p)
            T=fourier_tensor(q,m,p,w)
            self.assertEqual(rank_mod(flatten(T,'output_input'),p),n)
            for s in range(q):
                for h in range(m):
                    for t in range(q):
                        for u in range(m):
                            total=0
                            for a in range(q):
                                for b in range(m):
                                    total+= (pow(xi,(-s*a)%q,p)*
                                             pow(w,(-h*a)%n,p)*
                                             pow(eta,(-h*b)%m,p)*
                                             int(a==t)*int(b==u))
                            self.assertEqual(total%p,T[s][h][t][u])

    def test_partial_fourier_has_minimum_rank(self):
        for q,m in ((2,5),(4,3),(3,7),(6,6),(7,4)):
            p,w=field_for_length(q*m)
            self.assertEqual(rank_mod(crossed_partial_fourier(q,m,p,w),p),min(q,m))

    def test_cut_ranks_survive_all_four_independent_bases(self):
        rng=random.Random(61513)
        for q,m in ((2,3),(3,4),(4,3),(4,4)):
            p,w=field_for_length(q*m)
            original=fourier_tensor(q,m,p,w)
            for _ in range(5):
                transforms={dim:random_invertible(size,p,rng)
                            for dim,size in [('s',q),('h',m),('t',q),('u',m)]}
                T=transform_legs(original,transforms,p)
                rank_profile={key:rank_mod(flatten(T,key),p)
                              for key in ('output_input','crossed','alternating')}
                self.assertEqual(rank_profile,cut_ranks(q,m,p,w))

    def test_sparse_core_is_exact_and_has_n_nonzeros(self):
        for q,m in ((2,2),(2,3),(3,4),(4,3),(4,4),(6,4),(8,8)):
            p,w=field_for_length(q*m)
            T=fourier_tensor(q,m,p,w)
            A,B,expected=endpoint_sparse_core(q,m,p,w)
            observed=transform_legs(T,{'s':A,'u':B},p)
            self.assertEqual(expected,observed)
            self.assertEqual(count_tensor(observed),q*m)
            for a in range(q):
                for h in range(m):
                    for t in range(q):
                        for b in range(m):
                            self.assertEqual(observed[a][h][t][b],
                                             pow(w,(-h*t)%(q*m),p) if a==t and b==h else 0)

    def test_endpoint_support_product_and_minimum(self):
        rng=random.Random(1729)
        for q,m in ((2,3),(3,4),(4,4),(5,3)):
            p,w=field_for_length(q*m)
            T=fourier_tensor(q,m,p,w)
            for _ in range(20):
                A=random_invertible(q,p,rng)
                B=random_invertible(m,p,rng)
                core,P,R=endpoint_gauges(q,m,p,w,A,B)
                self.assertEqual(count_tensor(core),nnz(P)*nnz(R))
                self.assertEqual(core,transform_legs(T,{'s':A,'u':B},p))
                self.assertGreaterEqual(nnz(P)*nnz(R),q*m)

    def test_endpoint_minimum_rigidity_both_directions(self):
        rng=random.Random(2034)
        for q,m in ((2,2),(3,4),(4,5),(6,4)):
            p,w=field_for_length(q*m)
            A0,B0,_=endpoint_sparse_core(q,m,p,w)
            for _ in range(15):
                perma=list(range(q)); permb=list(range(m))
                rng.shuffle(perma);rng.shuffle(permb)
                scalara=[rng.randrange(1,p) for _ in range(q)]
                scalarb=[rng.randrange(1,p) for _ in range(m)]
                Pa=[[scalara[a] if t==perma[a] else 0 for t in range(q)] for a in range(q)]
                Pb=[[scalarb[h] if b==permb[h] else 0 for b in range(m)] for h in range(m)]
                A=matmul(Pa,A0,p)
                B=matmul([[Pb[j][i] for j in range(m)] for i in range(m)],B0,p)
                T,P,R=endpoint_gauges(q,m,p,w,A,B)
                self.assertEqual(P,Pa)
                self.assertEqual(R,Pb)
                self.assertEqual(count_tensor(T),q*m)
                self.assertEqual(nnz(P),q)
                self.assertEqual(nnz(R),m)
                # Conversely extracting transformed factors reconstructs the sole minimizer form.
                self.assertEqual(A,matmul(P,A0,p))

    def test_alternating_pair_is_unitary_complex(self):
        for q,m in ((2,3),(3,4),(4,4),(4,8),(8,8)):
            r=unitary_cut_singular_values(q,m)
            self.assertLess(np.max(abs(r['direct']-1)),1e-12)
            self.assertLess(np.max(abs(r['alternative']-1)),1e-12)

    def test_crossed_singular_values_equal_partial_vandermonde(self):
        for q,m in ((2,3),(3,4),(4,4),(4,8),(8,8)):
            r=unitary_cut_singular_values(q,m)
            k=min(q,m)
            self.assertLess(np.max(abs(r['crossed'][:k]-r['partial'])),1e-11)
            self.assertLess(np.max(abs(r['crossed'][k:])),1e-11)

    def test_unitary_leg_changes_preserve_all_singular_values(self):
        rng=np.random.default_rng(12)
        q,m=3,4
        r=unitary_cut_singular_values(q,m)
        n=q*m
        s=np.arange(q).reshape(q,1,1,1)
        h=np.arange(m).reshape(1,m,1,1)
        t=np.arange(q).reshape(1,1,q,1)
        u=np.arange(m).reshape(1,1,1,m)
        T=np.exp(-2j*np.pi*(h*t/n+h*u/m+s*t/q))/np.sqrt(n)
        for axis,dim in enumerate((q,m,q,m)):
            Z=rng.normal(size=(dim,dim))+1j*rng.normal(size=(dim,dim))
            unitary,_=np.linalg.qr(Z)
            T=np.moveaxis(T,axis,0)
            T=np.tensordot(unitary,T,axes=(1,0))
            T=np.moveaxis(T,0,axis)
        spectra=(
            np.linalg.svd(T.reshape(n,n),compute_uv=False),
            np.linalg.svd(np.transpose(T,(0,3,1,2)).reshape(n,n),compute_uv=False),
            np.linalg.svd(np.transpose(T,(0,2,1,3)).reshape(q*q,m*m),compute_uv=False),
        )
        for actual,reference in zip(spectra,(r['direct'],r['alternative'],r['crossed'])):
            self.assertLess(np.max(abs(actual-reference)),1e-11)

    def test_charged_two_axis_fft_is_exact(self):
        rng=random.Random(25)
        for q,m in ((2,2),(2,4),(4,4),(4,8),(8,8),(16,8),(16,16)):
            n=q*m;p,w=field_for_length(n)
            for _ in range(4):
                x=[rng.randrange(p) for _ in range(n)]
                result,count=charged_two_axis_fft(x,q,m,p,w)
                self.assertEqual(result,exact_dft(x,p,w))
                self.assertEqual(count['butterflies'],(n//2)*(q.bit_length()+m.bit_length()-2))
                self.assertEqual(count['cross_twiddle_multiplies'],n)
                self.assertEqual(count['root_table_multiplies'],n-1)
                self.assertEqual(count['scalar_arithmetic_total'],3*count['butterflies']+2*n-1)

    def test_sparse_core_without_basis_cost_is_not_a_fast_algorithm(self):
        # This test explicitly checks the count of the two charged Fourier stages.
        for k in range(2,9):
            n=2**k
            q=2**(k//2)
            m=n//q
            p,w=field_for_length(n)
            _,count=charged_two_axis_fft(list(range(n)),q,m,p,w)
            self.assertEqual(count['butterflies'],n*k//2)
            self.assertEqual(count['cross_twiddle_multiplies'],n)
            self.assertEqual(count['root_table_multiplies'],n-1)
            self.assertEqual(count['scalar_arithmetic_total'],3*count['butterflies']+2*n-1)

    def test_16_fourier_identity_gauge_table(self):
        for m in (2,3,4,6,8):
            q=m;p,w=field_for_length(m*m)
            eta=pow(w,q,p);xi=pow(w,m,p)
            i_q=invert_mod(dft_matrix(q,xi,p),p)
            i_m=invert_mod(dft_matrix(m,eta,p),p)
            T=fourier_tensor(q,m,p,w)
            counts={}
            for bits in itertools.product((0,1),repeat=4):
                dims='shtu'
                transforms={ax:X for ax,X,k in zip(dims,(i_q,i_m,i_q,i_m),bits) if k}
                counts[''.join(ax for ax,k in zip(dims,bits) if k) or 'none']=count_tensor(transform_legs(T,transforms,p))
            self.assertEqual(counts['none'],m**4)
            self.assertEqual(counts['su'],m*m)
            self.assertEqual(counts['s'],m**3)
            self.assertEqual(counts['u'],m**3)
            self.assertEqual(counts['sh'],m**3-m*m+m)
            self.assertEqual(counts['tu'],m**3-m*m+m)
            self.assertEqual(counts['t'],m**4-m**3+m*m)
            self.assertEqual(counts['h'],m**4-m**3+m*m)
            self.assertTrue(all(v>=m*m for v in counts.values()))
            self.assertEqual([k for k,v in counts.items() if v==m*m],['su'])

if __name__=='__main__':
    unittest.main()
