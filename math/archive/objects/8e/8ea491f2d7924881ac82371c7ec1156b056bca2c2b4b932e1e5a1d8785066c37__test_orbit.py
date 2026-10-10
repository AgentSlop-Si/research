import unittest
from orbit_recovery import *
from cyclotomic_interpolation import *

class OrbitTests(unittest.TestCase):
    def test_orbits_partition(self):
        for n in (2,4,8,16,32,64):
            os=orbits(n)
            self.assertEqual(set(sum([list(s) for s in os.values()],[])), set(range(n)))
            self.assertEqual(sum(map(len,os.values())),n)

    def test_minimum_representatives(self):
        for n in (2,4,8,16,32,64):
            self.assertEqual(len(representatives(n)),n.bit_length())
            self.assertEqual({frequency_conductor(n,k) for k in representatives(n)},set(orbits(n)))

    def test_formal_fourier(self):
        self.assertEqual(dft_bin_exact([1,0,0,0,0,0,0,0],3),(1,0,0,0))
        self.assertEqual(dft_bin_exact([0,0,0,0,1,0,0,0],3),(-1,0,0,0))
        self.assertEqual(dft_bin_exact([1]*8,0),(8,0,0,0))
        for k in range(1,8):self.assertEqual(dft_bin_exact([1]*8,k),(0,0,0,0))

    def test_single_missing_orbit(self):
        for n in (2,4,8,16,32):
            for m,frequencies in orbits(n).items():
                a,b=binary_coset_collision_witness(n,m)
                self.assertEqual(orbit_support_of_difference(a,b),frequencies)

    def test_exhaustive_binary_unique(self):
        n=8; q=representatives(n)
        sigs={dft_selected_exact([(t>>j)&1 for j in range(n)],q) for t in range(1<<n)}
        self.assertEqual(len(sigs),1<<n)

    def test_linear_independence_subset_sums(self):
        for n in (4,8,16):
            vals={subset_sum_cyclotomic_coeffs(n,t) for t in range(1<<(n//2))}
            self.assertEqual(len(vals),1<<(n//2))

    def test_poly_degree_bound(self):
        self.assertEqual(lower_bounds(8)['poly_degree_lower_bound'],9)
        self.assertEqual(lower_bounds(16)['poly_degree_lower_bound'],129)
        self.assertEqual(lower_bounds(32)['poly_degree_lower_bound'],32769)

    def test_rational_degree_bound(self):
        self.assertEqual(lower_bounds(8)['rational_num_den_degree_lower_bound'],4)
        self.assertEqual(lower_bounds(16)['rational_num_den_degree_lower_bound'],64)

    def test_interpolation_small(self):
        a=interpolation_audit(4)
        b=interpolation_audit(8)
        self.assertGreaterEqual(a['exact_min_polynomial_degree'],lower_bounds(4)['poly_degree_lower_bound'])
        self.assertGreaterEqual(b['exact_min_polynomial_degree'],lower_bounds(8)['poly_degree_lower_bound'])
        self.assertTrue(b['all_samples_verified'])

    def test_field_mul_inverse(self):
        for m in (2,4,8):
            a=Cyclo.of([1,1]+[0]*(m-2))
            self.assertEqual(a*a.inv(),Cyclo.one(m))
            self.assertEqual((a*a).inv()*a,a.inv())

    def test_exact_rational_rank_and_solution(self):
        from cyclotomic_interpolation import rational_interpolation_rank,rational_interpolant
        for d in range(3,8):
            self.assertTrue(rational_interpolation_rank(8,3,d)['no_rational_solution_proved'])
        witness=rational_interpolant(8,3,8)
        self.assertTrue(witness['all_values_verified'])
        self.assertTrue(witness['denominator_nonzero_on_all'])

    def test_independent_modular_rank_certificate(self):
        from independent_modular_certificate import run
        r=run()
        self.assertTrue(r['polynomial_degree_at_most_10_excluded'])
        self.assertTrue(r['rational_num_den_degree_at_most_7_excluded'])

    def test_invalid_inputs(self):
        for bad in (0,1,3,12):
            with self.assertRaises(ValueError):orbits(bad)
        with self.assertRaises(ValueError):binary_collision_family(8,4,4)
        with self.assertRaises(ValueError):lower_bounds(2)

if __name__=='__main__':unittest.main()
