import unittest, random
from math import gcd
from phase12 import (
 eye,mult,rank,inverse,subtract,add,fourier,green_inverse,monomial,
 column_support,build_sparse_inverse,full_spark_audit,matvec,
 green_commutator_audit,chirp,chirp_inversion_audit,
 direct_dft,primitive_root_of_order,
 shift_green_apply,modulation_green_apply,batch_inverse,
 stage_correction_network,lower_rank_budget,
 stride_green_apply,green_orbit_union_apply
)


class Phase12Test(unittest.TestCase):
    def test_exact_fourier_inverse(self):
        for n,q in [(3,7),(5,11),(7,29),(8,17),(16,97),(32,97)]:
            F=fourier(n,q); J=fourier(n,q,inv=True)
            self.assertEqual(mult(F,J,q),eye(n))
            rng=random.Random(n)
            for _ in range(5):
                x=[rng.randrange(q) for i in range(n)]
                y=matvec(F,x,q)
                self.assertEqual(matvec(J,y,q),x)

    def test_root_order(self):
        for n,q in [(3,7),(5,11),(7,29),(8,17),(16,97),(32,97),(64,193),(256,769)]:
            w=primitive_root_of_order(n,q)
            self.assertEqual(pow(w,n,q),1)
            for d in range(1,n):
                self.assertNotEqual(pow(w,d,q),1)

    def test_prime_full_spark_exhaustive(self):
        for n,q,counts in [(3,7,19),(5,11,251),(7,29,3431)]:
            a=full_spark_audit(n,q)
            self.assertTrue(a['full_spark'],a)
            self.assertEqual(a['minor_count'],counts)

    def test_small_arithmetic_uncertainty(self):
        rng=random.Random(120)
        for n,q in [(5,11),(7,29),(8,17),(12,97)]:
            F=fourier(n,q)
            for k in range(1, min(n,5)):
                for _ in range(60):
                    I=rng.sample(range(n),k)
                    x=[0]*n
                    for j in I:x[j]=rng.randrange(1,q)
                    b=sum(z!=0 for z in matvec(F,x,q))
                    self.assertGreaterEqual(k*b,n)
                    if n in (5,7):self.assertGreaterEqual(k+b,n+1)

    def test_sparse_inverse_product_bound(self):
        for n,q in [(5,11),(7,29),(8,17),(16,97),(32,97)]:
            for L in (1,2,3):
                B=build_sparse_inverse(n,q,L)
                self.assertLessEqual(column_support(B),2**L)

    def test_low_rank_update_inverse_telescoping(self):
        for n,q in [(5,11),(7,29),(8,17),(16,97)]:
            for L in (1,2,3):
                result=stage_correction_network(n,q,L,1,seed=2026)
                self.assertTrue(result['rank_telescoping_valid'],result)
                self.assertTrue(result['sparsity_valid'],result)

    def test_quantum_weyl_commutator_full_rank(self):
        for n,q in [(3,7),(5,11),(7,29),(8,17),(16,97),(32,97)]:
            a=next(z for z in range(2,q) if pow(z,n,q)!=1)
            out=green_commutator_audit(n,q,a,a)
            self.assertTrue(out['qcommutation_residual'],out)
            self.assertTrue(out['inverse_identity'],out)
            self.assertEqual(out['commutator_rank'],n)

    def test_chirp_dense_inverse(self):
        for n,q in [(3,7),(5,11),(7,29),(9,19),(15,31)]:
            a=chirp_inversion_audit(n,q)
            self.assertTrue(a['inverse_all_entries_nonzero'])
            self.assertEqual(a['inverse_column_support'],n)

    def test_chirp_bluestein_identity(self):
        for n,q in [(3,7),(5,11),(7,29),(9,19),(15,31)]:
            w=primitive_root_of_order(n,q)
            inv2=pow(2,-1,n)
            phases=[pow(w,(inv2*i*i)%n,q) for i in range(n)]
            C=chirp(n,q)
            reconstructed=[[(phases[i]*C[i][j]*phases[j])%q for j in range(n)] for i in range(n)]
            self.assertEqual(reconstructed,fourier(n,q))

    def test_shift_green_linear_executor(self):
        rng=random.Random(9102)
        for n,q in [(8,17),(16,97),(32,97),(64,193),(256,769)]:
            a=next(z for z in range(2,q) if pow(z,n,q)!=1)
            B=green_inverse(n,q,a,1)
            x=[rng.randrange(q) for _ in range(n)]
            y=shift_green_apply(x,a,q)
            self.assertEqual(matvec(B,y,q),x)

    def test_mod_green_linear_executor(self):
        rng=random.Random(9103)
        for n,q in [(8,17),(16,97),(32,97),(64,193),(256,769)]:
            a=next(z for z in range(2,q) if pow(z,n,q)!=1)
            x=[rng.randrange(q) for _ in range(n)]
            y=modulation_green_apply(x,a,q)
            w=primitive_root_of_order(n,q)
            check=[y[j]*(1-a*pow(w,j,q))%q for j in range(n)]
            self.assertEqual(check,x)

    def test_batch_inverse(self):
        rng=random.Random(1010)
        for q in (17,97,193,769):
            for n in (1,8,33,128):
                arr=[rng.randrange(1,q) for _ in range(n)]
                inv=batch_inverse(arr,q)
                self.assertEqual([(x*y)%q for x,y in zip(arr,inv)],[1]*n)

    def test_weyl_orbit_union_exact_fusion(self):
        rng=random.Random(12)
        for n,q in [(16,97),(64,193),(256,769),(1024,12289)]:
            a=next(z for z in range(2,q) if pow(z,n,q)!=1)
            x=[rng.randrange(q) for _ in range(n)]
            for K in [2,4,8,16]:
                if n<K:continue
                y=green_orbit_union_apply(x,a,K,q)
                z=stride_green_apply(x,pow(a,K,q),K,q)
                self.assertEqual(y,z,(n,K))
                beta=pow(a,K,q)
                for i in range(n):
                    self.assertEqual((z[i]-beta*z[(i-K)%n])%q,x[i])

    def test_lower_rank_bounds(self):
        self.assertEqual(lower_rank_budget(127,2,prime=True),42)
        self.assertEqual(lower_rank_budget(127,4,prime=True),25)
        self.assertEqual(lower_rank_budget(257,8,prime=True),28)
        self.assertEqual(lower_rank_budget(65536,2,prime=False),181)
        self.assertEqual(lower_rank_budget(65536,4,prime=False),127)

if __name__=='__main__': unittest.main()
