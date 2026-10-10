"""Reproducible exact tests for Hero #17 Phase 15, stdlib only."""
import random
import unittest

from phase15 import (
    P, generator, root_of_unity, prime_factors, gauss_table, direct_dft,
    fourier_weyl_support_size, weyl_coefficients_fourier_inverse,
    three_atom_factor, multiply_weyl, multiscale_inverse_polynomial,
    apply_three_atom, apply_weyl_polynomial, weyl_stage_lower_bound,
    chirp_kernel, cyclic_convolution, chirp_direct_transform,
    dyadic_cross_ratio, dyadic_binomial_product, fused_dyadic_binomial,
    inverse_chirp_linear_generation, chirp_digit_cut_rank,
    oriented_three_atom_factor, oriented_inverse_chain_polynomial,
    exact_fourier_intertwining_certificate,
)


class Phase15Tests(unittest.TestCase):
    def test_01_primitive_roots(self):
        for n in (2, 4, 8, 16, 32, 128, 256, 1024):
            w = root_of_unity(n)
            self.assertEqual(pow(w, n, P), 1)
            for q in prime_factors(n):
                self.assertNotEqual(pow(w, n // q, P), 1)

    def test_02_gauss_even_support(self):
        for n in (4, 8, 16, 32, 64):
            G=gauss_table(n,root_of_unity(n))
            self.assertEqual([j for j,g in enumerate(G) if g],list(range(0,n,2)))

    def test_03_gauss_other_parity(self):
        for n,p in ((2,17),(3,97),(5,241),(6,97),(10,241)):
            w=root_of_unity(n,p)
            G=gauss_table(n,w,p)
            expected = list(range(n)) if n%2 else list(range(1,n,2))
            self.assertEqual([j for j,g in enumerate(G) if g],expected)

    def test_04_weyl_coeff_support(self):
        for n,p in ((3,97),(4,P),(5,241),(6,97),(8,P),(16,P),(32,P)):
            co=weyl_coefficients_fourier_inverse(n,root_of_unity(n,p),p)
            self.assertEqual(len(co),fourier_weyl_support_size(n))

    def test_05_weyl_inverse_reconstruction(self):
        for n in (4,8,16):
            w=root_of_unity(n)
            co=weyl_coefficients_fourier_inverse(n,w)
            w_inv=pow(w,-1,P)
            n_inv=pow(n,-1,P)
            for col in range(n):
                e=[0]*n;e[col]=1
                actual=apply_weyl_polynomial(e,co,w)
                expected=[n_inv*pow(w,row*col,P)%P for row in range(n)]
                self.assertEqual(actual,expected)
                # Independent inverse check, using F- acting on the column of F+.
                echeck=direct_dft(actual,w)
                self.assertEqual(echeck,e)

    def test_06_twisted_polynomial_product(self):
        for n in (4,8,16):
            w=root_of_unity(n)
            a={(1,2):3,(0,0):6}
            b={(2,1):7,(3,0):5}
            prod=multiply_weyl(a,b,n,w)
            for j in range(n):
                e=[int(i==j) for i in range(n)]
                ab=apply_weyl_polynomial(apply_weyl_polynomial(e,b,w),a,w)
                self.assertEqual(ab,apply_weyl_polynomial(e,prod,w))

    def test_07_magnetic_inverse_expansion(self):
        rand=random.Random(1517)
        for n in (4,8,16):
            w=root_of_unity(n)
            shifts=[1,2,3]
            mods=[2,1,3]
            alphas=[rand.randrange(1,P) for _ in shifts]
            betas=[rand.randrange(1,P) for _ in shifts]
            pol=multiscale_inverse_polynomial(n,shifts,mods,alphas,betas,w)
            for j in range(n):
                e=[int(i==j) for i in range(n)]
                direct=e
                for s,b,a,be in zip(reversed(shifts),reversed(mods),reversed(alphas),reversed(betas)):
                    direct=apply_three_atom(direct,s,b,a,be,w)
                self.assertEqual(apply_weyl_polynomial(e,pol,w),direct)

    def test_08_support_budget(self):
        for n in (4,8,16,32,64,256,65536):
            lower=weyl_stage_lower_bound(n)
            self.assertLess(3**(lower-1),fourier_weyl_support_size(n))
            self.assertGreaterEqual(3**lower,fourier_weyl_support_size(n))

    def test_09_disjoint_bit_dyadic_support(self):
        for m in (2,3,4,5,6):
            n=1<<m;w=root_of_unity(n)
            shifts=[1<<j for j in range(m)]
            alphas=[j+2 for j in range(m)]
            betas=[j+7 for j in range(m)]
            poly=multiscale_inverse_polynomial(n,shifts,shifts,alphas,betas,w)
            self.assertEqual(len(poly),3**m)
            for a,b in poly:
                self.assertEqual(a&b,0)
            self.assertNotIn((1,1),poly)
            self.assertIn((1,1),weyl_coefficients_fourier_inverse(n,w))

    def test_10_chirp_is_exact_full_dft(self):
        rand=random.Random(91)
        for n in (4,8,16,32,64):
            z=root_of_unity(2*n);w=z*z%P
            for _ in range(2):
                x=[rand.randrange(P) for _ in range(n)]
                self.assertEqual(chirp_direct_transform(x,z),direct_dft(x,w))

    def test_11_chirp_inverse_full_support(self):
        for n in (4,8,16,32,64):
            z=root_of_unity(2*n)
            c=chirp_kernel(n,z)
            ci=chirp_kernel(n,z,inverse=True)
            self.assertTrue(all(x!=0 for x in ci))
            self.assertEqual(cyclic_convolution(c,ci),[1]+[0]*(n-1))

    def test_12_chirp_parallelogram_impossible(self):
        for n in (4,8,16,32,64,128):
            z=root_of_unity(2*n)
            lhs,rhs=dyadic_cross_ratio(n,z)
            self.assertNotEqual(lhs,rhs)
            self.assertEqual(lhs*pow(rhs,-1,P)%P,pow(z,-4,P))

    def test_13_dyadic_factor_fusion(self):
        rand=random.Random(48)
        for n in (4,8,16,32,64,256,1024):
            x=[rand.randrange(P) for _ in range(n)]
            alpha=5
            staged,counts_s=dyadic_binomial_product(x,alpha)
            fused,counts_f=fused_dyadic_binomial(x,alpha)
            self.assertEqual(staged,fused)
            self.assertEqual(counts_s.writes, n*(n.bit_length()-1))
            self.assertEqual(counts_f.writes,2*n)

    def test_14_fused_recurrence(self):
        rng=random.Random(193)
        for n in (4,16,64,256):
            a=13
            x=[rng.randrange(P) for _ in range(n)]
            y,_=fused_dyadic_binomial(x,a)
            d=(1-pow(a,n,P))%P
            for i in range(n):
                self.assertEqual((y[i]-a*y[(i-1)%n])%P,(d*x[i])%P)

    def test_15_support_explicit_prime_length(self):
        p=337;n=7
        w=root_of_unity(n,p)
        coeffs=weyl_coefficients_fourier_inverse(n,w,p)
        self.assertEqual(len(coeffs),n*n)
        self.assertGreater(weyl_stage_lower_bound(n),2)

    def test_16_weyl_monomial_shifts_preserve_support(self):
        n=16;w=root_of_unity(n)
        poly=multiscale_inverse_polynomial(n,[1,2,4],[4,1,2],[3,5,7],[2,7,11],w)
        left={(5,7):13};right={(2,3):9}
        shifted=multiply_weyl(left,multiply_weyl(poly,right,n,w),n,w)
        self.assertEqual(len(poly),len(shifted))

    def test_17_chirp_tensor_cut_full_rank(self):
        for m in range(3,11):
            n=1<<m
            z=root_of_unity(2*n)
            for split in set((1,m//2,m-1)):
                rank=chirp_digit_cut_rank(n,z,split)
                self.assertEqual(rank,min(1<<split,1<<(m-split)))

    def test_18_chirp_kernel_linear_generation(self):
        for m in (3,4,5,8,12):
            n=1<<m
            z=root_of_unity(2*n)
            out,ops=inverse_chirp_linear_generation(n,z)
            expected=chirp_kernel(n,z,inverse=True)
            self.assertEqual(out,expected)
            self.assertLess(ops.total(),3*n)

    def test_19_rotated_weyl_directions(self):
        rng=random.Random(1522)
        for n in (4,8,16,32):
            w=root_of_unity(n)
            factors=[]
            for _ in range(4):
                dir1=(rng.randrange(n),rng.randrange(n))
                dir2=(rng.randrange(n),rng.randrange(n))
                factors.append((dir1,dir2,rng.randrange(1,P),rng.randrange(1,P)))
            poly=oriented_inverse_chain_polynomial(n,factors,w)
            self.assertLessEqual(len(poly),3**len(factors))
            for j in range(min(n,4)):
                e=[int(i==j) for i in range(n)]
                expected=e
                for d1,d2,alpha,beta in reversed(factors):
                    stage=oriented_three_atom_factor(n,d1,d2,alpha,beta)
                    expected=apply_weyl_polynomial(expected,stage,w)
                self.assertEqual(apply_weyl_polynomial(e,poly,w),expected)

    def test_20_weyl_frame_support_permutation(self):
        # A basis change with determinant invertible modulo n permutes atoms.
        for n in (4,8,16,32):
            omega=root_of_unity(n)
            coeffs=weyl_coefficients_fourier_inverse(n,omega)
            # (a,b) maps to (a+b,b), determinant=1 over Z_n.
            mapped={((a+b)%n,b) for a,b in coeffs}
            self.assertEqual(len(coeffs),len(mapped))

    def test_21_exact_intertwining_certificate(self):
        for n in (4,8,16):
            w=root_of_unity(n)
            mat=[[pow(w,-i*j,P) for j in range(n)] for i in range(n)]
            self.assertTrue(exact_fourier_intertwining_certificate(mat,w))
            mat[2][3]=(mat[2][3]+1)%P
            self.assertFalse(exact_fourier_intertwining_certificate(mat,w))


if __name__ == '__main__':
    unittest.main()
