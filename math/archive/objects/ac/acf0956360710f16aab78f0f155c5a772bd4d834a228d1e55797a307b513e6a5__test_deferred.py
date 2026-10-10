import copy
import unittest
import numpy as np
import deferred_correction as d
from prior_exact_arithmetic import CyclotomicField,fourier,rank


class ExactAudit(unittest.TestCase):
    def test_full_telescope_and_all_basis_inputs(self):
        for n in (2,4,8,16,32):
            f,c,e=d.telescope(n);f0,c0=d.matrices(n)
            np.testing.assert_array_equal(f,f0);np.testing.assert_array_equal(c,c0)
            np.testing.assert_array_equal((c+e)%65537,f)

    def test_single_correction_expansion_misses_mixed_terms(self):
        f,c=d.matrices(8)
        self.assertTrue(np.any(((f-c)-d.naive_single_corrections(8))%65537))

    def test_certificates_and_corruption(self):
        for n in (2,4,8,16,32):
            cert=d.make_certificate(n);self.assertTrue(d.verify_certificate(cert))
            bad=copy.deepcopy(cert);bad['minor_determinant_mod_p']+=1
            self.assertFalse(d.verify_certificate(bad))

    def test_independent_cyclotomic_ranks(self):
        for n in (2,4,8,16):
            field=CyclotomicField(n);f=fourier(field,n);_,c=d.matrices(n)
            error=[[field.sub(f[i][j],field.integer(1 if c[i,j]==1 else -1))
                    for j in range(n)] for i in range(n)]
            self.assertEqual(rank(field,error),n-d.power_two(n)-1)

    def test_arbitrary_shared_core_and_tightness(self):
        rng=np.random.default_rng(443)
        for n in (4,8,16,32):
            m=n//2;f=d.matrices(m)[0];one=np.ones(m,dtype=np.int64)
            for _ in range(5):d.shared_core_audit(n,rng.integers(0,65537,(m,m)),one)
            record=d.shared_core_audit(n,f,one)
            self.assertEqual(record['rank_full_residual'],m-1)

    def test_modular_matrix_multiply_does_not_overflow(self):
        p=998244353;a=np.full((16,16),p-1,dtype=np.int64)
        np.testing.assert_array_equal(d.mm(a,a,p),np.full((16,16),16,dtype=np.int64))

    def test_exact_support_formula(self):
        for n in (2,4,8,16,32,64,128,256):
            f,c=d.matrices(n);e=(f-c)%65537
            self.assertEqual(np.count_nonzero(e),n*(n-d.power_two(n)-1))

    def test_root_and_size_validation(self):
        for n in (1,3,12):
            with self.assertRaises(ValueError):d.matrices(n)
        with self.assertRaises(ValueError):d.root_of_unity(16,65535)
        with self.assertRaises(ValueError):d.root_of_unity(16,17,generator=1)


if __name__=='__main__':unittest.main()
