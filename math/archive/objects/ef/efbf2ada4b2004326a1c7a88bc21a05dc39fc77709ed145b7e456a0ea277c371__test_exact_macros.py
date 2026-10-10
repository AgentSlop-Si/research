"""Independent full-output exact tests, not timing-only regression."""
import random,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from exact_scan_macro import (P,make_scan4_plan,dft_matrix,direct_dft,
    fft_via_mixed_scan_macros,fft_via_scan4,ranks_at_all_cuts,rank_mod)
from ordering_dp import optimal_orders
from reference_ntt import radix2_ntt
from analytic_certificate import run as independent_rank_certificate
from unitary_control import run as unitary_control

class ScanMacroTests(unittest.TestCase):
    def test_four_point_whole_matrix(self):
        for p,g in ((998244353,3),(2013265921,31)):
            plan=make_scan4_plan(p,g)
            mat=dft_matrix(4,p,g)
            for j in range(4):
                x=[int(i==j) for i in range(4)]
                self.assertEqual(plan.evaluate(x),[row[j] for row in mat])

    def test_direct_full_matrix_all_small_lengths(self):
        for n in (2,4,8,16,32,64):
            f=dft_matrix(n)
            for j in range(n):
                x=[int(i==j) for i in range(n)]
                got,_=fft_via_mixed_scan_macros(x)
                self.assertEqual(got,[row[j] for row in f])

    def test_fresh_dense_random_all_lengths(self):
        r=random.Random(20261009)
        for n in (2,4,8,16,32,64,128,256,512,1024):
            for _ in range(5 if n<=256 else 2):
                x=[r.randrange(P) for j in range(n)]
                a,_=fft_via_mixed_scan_macros(x)
                b,_=radix2_ntt(x)
                self.assertEqual(a,b)

    def test_arbitrary_integers_reduced_mod_p(self):
        for n in (2,4,8,16,32):
            x=[(-3 if i%3==0 else 3*P+11) for i in range(n)]
            self.assertEqual(fft_via_mixed_scan_macros(x)[0],direct_dft(x))

    def test_4power_wrapper(self):
        with self.assertRaises(ValueError):fft_via_scan4([1]*8)
        for n in (4,16,64,256):
            a=[((31*i*i+11)%P) for i in range(n)]
            self.assertEqual(fft_via_scan4(a)[0],direct_dft(a))

    def test_invalid_lengths(self):
        for n in (0,1,3,6,7):
            with self.assertRaises(ValueError):fft_via_mixed_scan_macros([1]*n)

    def test_root_moduli(self):
        for p,g in ((998244353,3),(2013265921,31)):
            for n in (4,8,16,32,64):
                x=[((i*71+19)%p) for i in range(n)]
                self.assertEqual(fft_via_mixed_scan_macros(x,p,g)[0],direct_dft(x,p,g))

    def test_macro_stage_count(self):
        for n in (2,4,8,16,32,64,128,256):
            x=[int(i==1) for i in range(n)]
            _,stats=fft_via_mixed_scan_macros(x)
            L=n.bit_length()-1
            self.assertEqual(stats['macro_stages'],(L+1)//2)
            self.assertEqual(stats['bidirectional_passes_per_element'],2*((L+1)//2))
            self.assertLessEqual(stats['permutation_index_steps'],2*n)

    def test_scan_cost_not_hidden(self):
        for n in (16,64,256):
            scan,sc=fft_via_mixed_scan_macros(list(range(n)))
            ordinary,rc=radix2_ntt(list(range(n)))
            self.assertEqual(scan,ordinary)
            self.assertGreater(sc['scan_additions_upper'],rc['additions'])
            self.assertGreater(sc['scan_multiplications_upper'],rc['data_twiddle_mult'])
            self.assertGreater(sc['permutation_moves'],rc['permutation_moves'])
            self.assertGreater(sc['modular_power_mult_upper'],0)

    def test_exact_endpoint_optimum_n4(self):
        result=optimal_orders(4)
        self.assertEqual(result['optimum'],1)
        self.assertEqual(result['states_examined'],69)

    def test_exact_endpoint_optimum_n8(self):
        result=optimal_orders(8)
        self.assertEqual(result['optimum'],3)
        self.assertEqual(result['states_examined'],12869)
        self.assertEqual(len(result['row_order']),8)

    def test_two_primes_independent_certificate(self):
        result=independent_rank_certificate()
        self.assertEqual([entry['rank3_3x5_matrices'] for entry in result['primes']],[3136,3136])
        for v in result['complex_balanced_determinants'].values():
            self.assertEqual(v,(0,0,0,0))

    def test_unitary_qsep_control(self):
        report=unitary_control((4,8,16))
        self.assertEqual([r['maximum_quasiseparable_offdiagonal_rank'] for r in report],[1,1,1])
        for record in report:
            self.assertLess(record['final_entropy_bits'],record['target_fourier_entropy_bits'])
            self.assertLessEqual(record['maximum_entropy_increase_per_gate'],2+1e-9)

    def test_parity_ranks(self):
        for n,expectedmax in ((4,1),(8,3),(16,6)):
            mat=dft_matrix(n)
            ordering=list(range(0,n,2))+list(range(1,n,2))
            vals=ranks_at_all_cuts(mat,ordering,ordering)
            self.assertEqual(max(max(x) for x in vals),expectedmax)

if __name__=='__main__':unittest.main()
