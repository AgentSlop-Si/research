import unittest
import random
from phase27_affine_gap import (MOD,random_hamiltonian,shift_successor,
    conjugate_by_transposition,permutation_rank_difference,cycle_count,
    affine_rank_audit,high_probability_threshold,mod_difference_rank_green,
    cyclotomic_zero_density,conjugate_zero_by_histogram)
from phase27_fourier_recovery import (P,MonomialFourier,recover,
    basis,fft_unscaled,root,batch_inverse)
from phase27_green_candidate import (seeded_nonaffine_circuit,dot)
from phase27_expansion_certificate import certify
from phase27_expander_mixer import audit_balanced_cuts,two_by_two_phase_report


class TestPermutationRank(unittest.TestCase):
    def test_cycle_formula_via_exact_green_rank(self):
        for n in (8,16,32):
            z=shift_successor(n)
            for seed in (0,1,2):
                w=random_hamiltonian(n,27+n+seed)
                expected=permutation_rank_difference(w,z)
                for alpha in (2,3):
                    self.assertEqual(mod_difference_rank_green(w,z,alpha),expected)

    def test_nonaffine_near_shift_is_rank_two(self):
        for n in (8,16,32,64,128):
            w=conjugate_by_transposition(n,0,n//4+1)
            self.assertEqual(cycle_count(w),1)
            self.assertEqual(permutation_rank_difference(w,shift_successor(n)),2)
            self.assertGreater(affine_rank_audit(w)['min_rank'],0)

    def test_uniform_hamiltonian_union_bound_integer(self):
        for n in (8,16,32,64,128,256,512,1024):
            report=high_probability_threshold(n)
            self.assertEqual(report['affine_count'],n*n//2)
            self.assertLessEqual(report['failure_bound_numerator']*n*n,
                                 report['failure_bound_denominator'])

    def test_all_affine_references_exhaustive(self):
        for n in (32,64,128,256):
            w=random_hamiltonian(n,2700+n)
            report=affine_rank_audit(w)
            self.assertTrue(report['exhaustive'])
            self.assertEqual(report['checked'],n*n//2)
            self.assertGreaterEqual(report['min_rank'],
                                    high_probability_threshold(n)['rank_at_least'])
            self.assertEqual(report['min_rank'],{32:24,64:52,128:114,256:240}[n])


class TestCyclotomicZeros(unittest.TestCase):
    def test_affine_fourier_conjugate_is_monomial(self):
        for n in (8,16,32):
            for u,b in ((1,1),(3,4),(n-1,3)):
                affine=[(u*j+b)%n for j in range(n)]
                self.assertEqual(cyclotomic_zero_density(affine)['nonzeros'],n)

    def test_random_dense_and_near_affine_dense(self):
        for n in (16,32,64):
            w=random_hamiltonian(n,2700+n)
            almost=conjugate_by_transposition(n,0,n//4+1)
            self.assertGreater(cyclotomic_zero_density(w)['fraction_nonzero'],0.8)
            self.assertGreater(cyclotomic_zero_density(almost)['fraction_nonzero'],0.8)
            self.assertEqual(permutation_rank_difference(almost,shift_successor(n)),2)

    def test_exact_dense_rank_two_trap_formula(self):
        # W=tau Z tau has rank-two difference from Z, but its exact
        # cyclotomic Fourier conjugate has N^2-3N+4 nonzeros.
        for n in (16,32,64,128):
            w=conjugate_by_transposition(n,0,n//4+1)
            self.assertEqual(permutation_rank_difference(w,shift_successor(n)),2)
            self.assertEqual(cyclotomic_zero_density(w)['nonzeros'],n*n-3*n+4)

    def test_symbolic_cyclotomic_criterion(self):
        # Independent polynomial reduction by z^(n/2)=-1 (not numerical FFT).
        rng=random.Random(2709)
        for n in (8,16,32):
            p=random_hamiltonian(n,2709+n)
            for _ in range(30):
                a=rng.randrange(n);b=rng.randrange(n)
                coeff=[0]*n
                for j,k in enumerate(p):coeff[(a*k-b*j)%n]+=1
                reduced=[coeff[r]-coeff[r+n//2] for r in range(n//2)]
                self.assertEqual(conjugate_zero_by_histogram(p,a,b),
                                 all(v==0 for v in reduced))


class TestFourierRecovery(unittest.TestCase):
    def test_batch_inverse(self):
        rng=random.Random(27)
        for n in (8,16,128):
            x=[rng.randrange(1,P) for _ in range(n)]
            out=batch_inverse(x)
            self.assertTrue(all(a*b%P==1 for a,b in zip(x,out)))

    def test_unnormalized_fft_direct(self):
        rng=random.Random(270)
        for n in (8,16,32):
            omega=root(n)
            for _ in range(2):
                x=[rng.randrange(P) for _ in range(n)]
                y=fft_unscaled(x)
                slow=[sum(x[j]*pow(omega,i*j,P) for j in range(n))%P
                      for i in range(n)]
                self.assertEqual(y,slow)

    def test_hidden_fourier_gauges_recovered(self):
        for n in (8,16,32,64,256):
            rng=random.Random(2700+n)
            row=list(range(n));col=list(range(n))
            rng.shuffle(row);rng.shuffle(col)
            c=MonomialFourier(row,col,
                [rng.randrange(1,P) for _ in range(n)],
                [rng.randrange(1,P) for _ in range(n)])
            report=recover(c.apply,c.transpose,n,max_other_columns=n-1,
                           trials=3,seed=2700+n)
            self.assertEqual(report.status,'passes_sample',report.reason)
            cert=report.certificate
            self.assertEqual(sorted(cert.row_perm),list(range(n)))
            self.assertEqual(sorted(cert.col_perm),list(range(n)))
            for _ in range(2):
                x=[rng.randrange(P) for _ in range(n)]
                self.assertEqual(c.apply(x),cert.predict(x))
                self.assertEqual(c.transpose(x),cert.predict_transpose(x))
            if n<=16:
                for i in range(n):
                    self.assertEqual(c.apply(basis(n,i)),cert.predict(basis(n,i)))

    def test_structural_rejection_of_random_green(self):
        for n in (16,64,256,1024):
            g=seeded_nonaffine_circuit(n,2700+n)
            report=recover(g.apply,g.transpose,n,max_other_columns=8,trials=2)
            self.assertEqual(report.status,'rejected')
            self.assertEqual(report.oracle_calls_forward,2)
            self.assertEqual(report.oracle_calls_transpose,0)

    def test_sparse_one_entry_corruption_detected(self):
        n=32
        exact=MonomialFourier(list(range(n)),list(range(n)),[1]*n,[1]*n)
        def corrupt(x):
            y=exact.apply(x)
            y[-1]=(y[-1]+7*x[-1])%P
            return y
        def corrupt_t(x):
            y=exact.transpose(x)
            y[-1]=(y[-1]+7*x[-1])%P
            return y
        report=recover(corrupt,corrupt_t,n,max_other_columns=1,
                       trials=2,seed=2727,randomize_candidates=False)
        self.assertEqual(report.status,'rejected')
        self.assertIsNotNone(report.certificate)
        self.assertGreater(report.mismatching_entries,0)

    def test_transpose_identity_for_greens(self):
        rng=random.Random(2717)
        for n in (8,16,64,128):
            g=seeded_nonaffine_circuit(n,2700+n)
            for _ in range(3):
                x=[rng.randrange(P) for _ in range(n)]
                y=[rng.randrange(P) for _ in range(n)]
                self.assertEqual(dot(g.apply(x),y),dot(x,g.transpose(y)))


class TestExactExpansion(unittest.TestCase):
    def test_finite_mixer_matrix_cut_ranks(self):
        # All balanced cuts at N=16; only a sampled diagnostic above 16.
        full=audit_balanced_cuts(16,2716,exhaustive=True)
        self.assertEqual(full['checked_cuts'],12870)
        self.assertEqual(full['min_rank'],4)
        for n,at_least in ((32,11),(64,23),(128,48)):
            d=audit_balanced_cuts(n,2700+n,trials=80)
            self.assertGreaterEqual(d['min_rank'],at_least)
            self.assertFalse(d['exhaustive'])

    def test_exact_modular_phase_obstruction(self):
        for n in (16,32,64,128,256):
            report=two_by_two_phase_report(n,2700+n)
            self.assertTrue(report['excluded_modular'])
            self.assertNotEqual(report['cross_ratio_power_n'],1)

    def test_exact_leading_minors(self):
        recorded={
            32:'f658a85e6008e4add90f83a32c0981bae80e06cb3ee96a7b03e14d7ae49ce253',
            64:'9fa0d244427f33ab5710b14993a359a2d2db0458727f0c2d4b89a9e6eb4b4ada',
            128:'8294ef2ac3f2e10f6cf76caa3fa03c3324b196439e2cee99674ff6e72faf28dd',
        }
        for n,digest in recorded.items():
            result=certify(n,2700+n,delta_den=2)
            self.assertEqual(result['exact_positive_pivots'],n)
            self.assertEqual(result['pivot_digest_sha256'],digest)
            self.assertEqual(result['every_balanced_cut_edges_strictly_greater'],n/8)


if __name__=='__main__':unittest.main()
