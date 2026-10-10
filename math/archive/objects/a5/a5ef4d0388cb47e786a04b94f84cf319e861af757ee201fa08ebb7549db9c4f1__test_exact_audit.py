import unittest
from exact_audit import (PRIME,nth_root,fourier_matrix,mod_rank,verify_displacement,
                         full_rank_rectangles,fft_mod,verify_fft,entropy_audit,
                         grouped_macro_audit,run_audit,evaluate_pole_representation)

class FourierCompressionAuditTests(unittest.TestCase):
    def test_root_primitive(self):
        for n in [2,4,8,16,32,64,128]:
            w=nth_root(n)
            self.assertEqual(pow(w,n,PRIME),1)
            self.assertNotEqual(pow(w,n//2,PRIME),1)

    def test_root_invalid(self):
        for n in (0,1,3,5,7,12):
            with self.assertRaises(ValueError):
                nth_root(n)

    def test_mod_rank_reference(self):
        self.assertEqual(mod_rank([[1,2,3],[2,4,6],[0,1,1]]),2)
        self.assertEqual(mod_rank([[0,0],[0,0]]),0)
        self.assertEqual(mod_rank([[1,0],[0,1]]),2)
        self.assertEqual(mod_rank([]),0)

    def test_displacement_identity(self):
        for n in (2,4,8,16,32,64):
            self.assertTrue(verify_displacement(n))

    def test_block_ranks(self):
        for n in (8,16,32,64):
            samples=full_rank_rectangles(n)
            self.assertGreater(len(samples),0)
            self.assertTrue(all(x['rank']==x['expected'] for x in samples))

    def test_fft_against_all_basis(self):
        for n in (2,4,8,16,32,64):
            self.assertEqual(verify_fft(n)[1],n*(n.bit_length()-1)//2)

    def test_fft_matches_direct_random(self):
        from random import Random
        rng=Random(0xF042)
        for n in (2,4,8,16,32):
            f=fourier_matrix(n)
            for _ in range(10):
                x=[rng.randrange(PRIME) for _ in range(n)]
                y,_=fft_mod(x)
                target=[sum(f[j][k]*x[k] for k in range(n))%PRIME for j in range(n)]
                self.assertEqual(y,target)

    def test_entropy_exact_stages(self):
        for n in (2,4,8,16,32,64,128,256):
            rows=entropy_audit(n)
            bits=n.bit_length()-1
            self.assertEqual(rows[-1].entropy_total_bits,n*bits)
            self.assertEqual(rows[-1].cumulative_gates,n*bits//2)
            for t,row in enumerate(rows):
                self.assertEqual(row.support_per_row,2**t)
                self.assertEqual(row.entropy_total_bits,n*t)
                self.assertEqual(row.cumulative_gates,n*t//2)

    def test_grouping_does_not_erase_primitive_work(self):
        for n in (4,16,64,256,4096):
            self.assertTrue(all(r['total_primitives']==n*(n.bit_length()-1)//2
                                for r in grouped_macro_audit(n)))

    def test_numerical_budget_is_not_fake_macro_budget(self):
        rows=grouped_macro_audit(4096)
        one=rows[-1]
        self.assertEqual(one['macro_calls'],1)
        self.assertEqual(one['total_primitives'],24576)

    def test_pole_coefficients_are_the_fft(self):
        for n in (2,4,8,16,32,64):
            x=[((i+5)**3 - 11*i) % PRIME for i in range(n)]
            got,cost=evaluate_pole_representation(x)
            self.assertEqual(got,fft_mod(x)[0])
            self.assertEqual(cost['state_multiplies'],n*(n-1))
            self.assertEqual(cost['description_field_elements'],2*n)

    def test_general_audit(self):
        rows=run_audit((4,8,16))['results']
        self.assertEqual([r['n'] for r in rows],[4,8,16])
        self.assertTrue(all(r['displacement_rank']==1 for r in rows))

if __name__ == '__main__':
    unittest.main()
