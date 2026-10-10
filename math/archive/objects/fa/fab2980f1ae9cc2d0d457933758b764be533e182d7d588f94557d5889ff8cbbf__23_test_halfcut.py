import unittest
from halfcut_certificate import verify, halfcut_selection, fourier_rect
from minor_certificate import permutation, rank_mod, MOD


class HalfcutTheoremTest(unittest.TestCase):
    def test_complementary_overlap(self):
        for n in (8,16,32,64,128):
            for shuffle in ('identity','reverse','bitrev','random'):
                c=halfcut_selection(permutation(n,shuffle))
                self.assertEqual(c['c_left']+c['c_right'],n//2)

    def test_exact_two_half_matrices(self):
        for n,r in ((16,1),(32,2),(32,3),(64,3)):
            for kind in ('identity','reverse','bitrev','random'):
                result=verify(n,r,r,shuf=kind)
                self.assertTrue(result['theoretical_rejection'])
                self.assertTrue(all(a['rank_fourier']==n//2 for a in result['audits']))

    def test_rank_gate_borderline(self):
        # At equality theorem is silent, not proof an identity exists.
        result=verify(32,4,4,shuf='random')
        self.assertFalse(result['theoretical_rejection'])

    def test_monomial_gains(self):
        for shuffle in ('random','bitrev'):
            result=verify(32,2,2,shuf=shuffle,weighted=True)
            self.assertTrue(result['theoretical_rejection'])

    def test_output_or_input_permutation_separately(self):
        for n in (16,32):
            for field in ('output_reordered','input_reordered'):
                r=1 if n==16 else 2
                args={field:True}
                result=verify(n,r,r,**args)
                self.assertTrue(result['theoretical_rejection'])

    def test_general_vandermonde_blocks(self):
        # The proof extends beyond roots of unity to distinct nonzero nodes.
        for n in (8,16,32):
            m=n//2
            rng=list(range(1,n+1))
            for lo in (0,m):
                V=[[pow(rng[i],lo+j,MOD) for j in range(m)] for i in range(m)]
                self.assertEqual(rank_mod(V),m)


if __name__=='__main__':
    unittest.main()

class ExactGreenHalfcutTest(unittest.TestCase):
    def test_supplied_green_stages_fail_at_32(self):
        from green_sum_audit import actual_green_halfcut_case
        for kind in ('identity','reverse','bitrev','random'):
            out=actual_green_halfcut_case(32,kind)
            self.assertTrue(any(d['product_rank']<16 for d in out['details']))
