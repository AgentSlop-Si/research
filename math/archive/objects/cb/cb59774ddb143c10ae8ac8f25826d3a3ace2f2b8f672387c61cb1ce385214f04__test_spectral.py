import unittest
from spectral_boolean import *
from graded_certificate import *
from audit import cubic_paired_single_missing_exact_characteristic_zero

class TestSpectralBool(unittest.TestCase):
    def test_primitive_root(self):
        for n in (2,4,8,16,32,64):
            w=primitive_root(n,998244353)
            self.assertEqual(pow(w,n,998244353),1)
            self.assertNotEqual(pow(w,n//2,998244353),1)

    def test_idempotence_all_binary_n8(self):
        n,p=8,97
        for x in all_binary(n):
            X=dft(x,p)
            self.assertEqual(spectrum_self_convolution(X,p),tuple((n*v)%p for v in X))

    def test_missing_one_formula_all_binary(self):
        p=97;balanced=0;success=0
        for x in all_binary(8):
            X=dft(x,p)
            got=recover_one_from_others(X,1,p)
            if sum(x)==4:self.assertIsNone(got);balanced+=1
            else:self.assertEqual(got,X[1]);success+=1
        self.assertEqual(balanced,70)
        self.assertEqual(success,186)

    def test_even_mode_ambiguous(self):
        for n in (8,16):
            p=998244353
            ss={tuple(dft(x,p)[::2]) for x in half_complement_family(n)}
            self.assertEqual(len(ss),1)
            self.assertEqual(next(iter(ss)),(n//2,)+tuple(0 for _ in range(n//2-1)))

    def test_noninjective_even_spectrum(self):
        collision=signature_collision(8,(0,2,4,6),1,97)
        self.assertIsNotNone(collision)
        self.assertNotEqual(collision['x_missing'],collision['y_missing'])

    def test_degree2_rigidity(self):
        for target in (1,3,7):
            known=tuple(i for i in range(8) if i!=target)
            r=exact_poly_completion(8,97,known,target,2)
            self.assertFalse(r['found'])
            self.assertTrue(quadratic_rigidity_theorem(8,known,target)['no_degree_le_2_completion'])

    def test_degree3_single_bin_exists(self):
        r=exact_poly_completion(8,97,tuple(range(7)),7,3)
        self.assertTrue(r['found'])
        self.assertEqual(len(r['witness']),10)
        self.assertTrue(all(evaluate_witness(dft(x,97),r['witness'],97)==dft(x,97)[7] for x in all_binary(8)))

    def test_exact_characteristic_zero_cubic_identity(self):
        self.assertTrue(cubic_paired_single_missing_exact_characteristic_zero())

    def test_graded_character_necessity(self):
        self.assertEqual(sumset_access(16,(0,2,4,6,8,10,12,14),100),set(range(0,16,2)))
        self.assertNotIn(1,sumset_access(16,(0,2,4,6),9))

    def test_no_cubic_pair_8(self):
        n=8
        r=rank_certificate(n,998244353,1,3,tuple(k for k in range(n) if k not in (1,n-1)))
        self.assertTrue(verify_certificate(r))
        self.assertEqual(r['num_columns'],8)

    def test_no_cubic_pair_16(self):
        n=16
        r=rank_certificate(n,998244353,1,3,tuple(k for k in range(n) if k not in (1,n-1)))
        self.assertTrue(verify_certificate(r))
        self.assertEqual(r['num_columns'],40)

    def test_no_cubic_pair_32(self):
        n=32
        r=rank_certificate(n,998244353,1,3,tuple(k for k in range(n) if k not in (1,n-1)))
        self.assertTrue(verify_certificate(r))
        self.assertEqual(r['num_columns'],168)

    def test_empty_bad(self):
        with self.assertRaises(ValueError):primitive_root(3,97)
        with self.assertRaises(ValueError):recover_one_from_others((1,2,3,4),0,97)
        with self.assertRaises(ValueError):quadratic_rigidity_theorem(8,(1,2),1)

if __name__=='__main__':unittest.main()
