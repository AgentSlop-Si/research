import random
import unittest
from chirp_exact import (P, make_chirp, dft_direct, dft_ntt,
    cyclic_convolution, chirp_dft_direct, chirp_convolution_from_ntt,
    variable_filter, modular_rank, matrix_c_h, matrix_lc_h, moment,
    moment_matrix, cyclic_hankel, predicted_full_spectral_probability)


class ExactGlobalReuseAudit(unittest.TestCase):
    def test_invalid_roots(self):
        for n in (0,1,3,6,10,1<<23):
            with self.assertRaises(ValueError):make_chirp(n)

    def test_ntt_independent_reference_and_round_trip(self):
        r=random.Random(8120)
        for n in (2,4,8,16,32,64,128):
            c=make_chirp(n)
            for _ in range(8):
                x=[r.randrange(P) for _ in range(n)]
                self.assertEqual(dft_ntt(x,c.omega),dft_direct(x,c.omega))
                self.assertEqual(dft_ntt(dft_ntt(x,c.omega),c.omega,True),x)

    def test_full_chirp_dft_factorization_fresh_inputs(self):
        r=random.Random(2026)
        for n in (2,4,8,16,32,64):
            c=make_chirp(n)
            for _ in range(8):
                x=[r.randrange(P) for _ in range(n)]
                self.assertEqual(chirp_dft_direct(x,c),dft_direct(x,c.omega))

    def test_chirp_convolution_is_an_fft_in_disguise(self):
        r=random.Random(12024)
        for n in (2,4,8,16,32,64):
            c=make_chirp(n)
            for _ in range(6):
                x=[r.randrange(P) for _ in range(n)]
                self.assertEqual(cyclic_convolution(x,c.h),chirp_convolution_from_ntt(x,c))

    def test_gauss_chirp_spectrum_nonzero(self):
        for n in (2,4,8,16,32,64,128):
            c=make_chirp(n)
            g=sum(c.h)%P
            self.assertNotEqual(g,0)
            self.assertEqual(dft_ntt(c.h,c.omega),[g*v%P for v in c.d])

    def test_kernel_first_order_variable_recurrence(self):
        for n in (2,4,8,16,32,64):
            c=make_chirp(n)
            self.assertEqual(variable_filter(c.h,c),[0]*n)
            # Wrong-sign recurrence must fail for N > 2.
            if n>=4:
                wrong=[(c.h[(k+1)%n]-pow(c.g[k],P-2,P)*c.h[k])%P
                       for k in range(n)]
                self.assertNotEqual(wrong,[0]*n)

    def test_variable_annihilator_does_not_sparsify_convolution(self):
        r=random.Random(995)
        for n in (4,8,16,32,64):
            c=make_chirp(n)
            LCh=matrix_lc_h(c)
            self.assertEqual(modular_rank(matrix_c_h(c)),n)
            self.assertEqual(modular_rank(LCh),n-1)
            for _ in range(6):
                x=[r.randrange(P) for _ in range(n)]
                out=cyclic_convolution(x,c.h)
                actual=variable_filter(out,c)
                expected=[sum(LCh[k][j]*x[j] for j in range(n))%P
                          for k in range(n)]
                self.assertEqual(actual,expected)
                self.assertEqual(sum(v!=0 for v in actual),n)

    def test_moment_ladder_and_independence(self):
        r=random.Random(357)
        for n in (4,8,16,32):
            c=make_chirp(n)
            x=[r.randrange(P) for _ in range(n)]
            self.assertEqual(modular_rank(moment_matrix(c)),n)
            for k in range(n):
                for s in range(n):
                    lhs=moment(x,c,s,(k+1)%n)
                    rhs=c.g[k]*moment(x,c,(s+1)%n,k)%P
                    self.assertEqual(lhs,rhs)

    def test_periodic_minimal_recurrence_order_equals_spectral_support(self):
        r=random.Random(9876)
        for n in (4,8,16,32):
            c=make_chirp(n)
            for _ in range(3):
                x=[r.randrange(P) for _ in range(n)]
                y=cyclic_convolution(x,c.h)
                support=sum(v!=0 for v in dft_ntt(x,c.omega))
                self.assertEqual(modular_rank(cyclic_hankel(y)),support)
                self.assertEqual(support,n)
            # A deliberately sparse frequency-domain input is a positive control.
            for s in (1,2,3):
                freq=[0]*n
                for j in range(s): freq[(3*j)%n]=j+1
                x=dft_ntt(freq,c.omega,True)
                y=cyclic_convolution(x,c.h)
                self.assertEqual(modular_rank(cyclic_hankel(y)),s)

    def test_all_chirp_shifts_are_independent_and_have_exact_inverse(self):
        for n in (2,4,8,16,32,64):
            c=make_chirp(n)
            inv_h=[pow(v,P-2,P) for v in c.h]
            # h * h_inverse = n * e_0, the exact CAZAC identity.
            impulse=cyclic_convolution(c.h,inv_h)
            self.assertEqual(impulse,[n]+[0]*(n-1))
            self.assertEqual(modular_rank(matrix_c_h(c)),n)

    def test_probability_and_work_lower_scope(self):
        for n in (8,64,4096):
            pr=predicted_full_spectral_probability(n)
            self.assertGreaterEqual(pr,1-n/P-1e-11)
            self.assertLessEqual(pr,1)


if __name__=='__main__':unittest.main()
