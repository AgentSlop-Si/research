import random
import unittest
from phase8 import (
 fixture, dft_matrix, submat, matrank, matinv, matmul, blockdiag, schur_cut_certificate,
 dense_star, bridge_network, eval_radix2_remainder, eval_generic_remainder, dft_ref,
 exhaustive_root_split, radix2_symbolic_merges, unitary_entropy_audit, lut_gate_bound,
)

class Phase8Tests(unittest.TestCase):
    def test_cut_rank_all_lengths(self):
        for n in (4,5,6,7,8,9,10,12,15,16,20):
            p,w=fixture(n);F=dft_matrix(n,p,w)
            for m in range(1,n):
                A=submat(F,range(m),range(m,n))
                self.assertEqual(matrank(A,p),min(m,n-m))

    def test_schur_sharp_even(self):
        for n in (4,6,8,10,16,20):
            p,w=fixture(n)
            got=schur_cut_certificate(n,p,w)
            self.assertEqual(got['bridge_rank'],n//2)

    def test_random_multistage_bridge_transport(self):
        for n in (8,10,16):
            p,w=fixture(n)
            for seed in range(6):
                d=bridge_network(n,p,w,seed=seed,steps=seed+1)
                self.assertLessEqual(d['offdiag_rank'],d['rank_budget'])

    def test_dense_star_invertible_but_not_dft(self):
        for n in (4,8,16,32):
            p,w=fixture(n)
            S,gates=dense_star(n,p)
            F=dft_matrix(n,p,w)
            self.assertEqual(gates,2*n-2)
            self.assertEqual(matrank(S,p),n)
            self.assertTrue(all(all(v!=0 for v in row) for row in S))
            self.assertNotEqual(S,F)

    def test_shared_binomial_evaluator_full_random(self):
        rng=random.Random(8037)
        for n in (2,4,8,16,32,64,128):
            p,w=fixture(n)
            for _ in range(5):
                x=[rng.randrange(p) for _ in range(n)]
                y,log=eval_radix2_remainder(x,p,w)
                self.assertEqual(y,dft_ref(x,p,w))
                self.assertEqual(log.butterflies,n*(n.bit_length()-1)//2)
                self.assertEqual(log.adds,2*log.butterflies)
                self.assertEqual(log.muls,log.butterflies)
                self.assertEqual(log.root_prep_muls,n-1)
                self.assertEqual(log.writes,n)

    def test_generic_root_division_evaluator(self):
        rng=random.Random(991)
        for n in (4,8,16,32):
            p,w=fixture(n)
            for policy in ('subgroup','contiguous','noncoset16'):
                for _ in range(2):
                    x=[rng.randrange(p) for _ in range(n)]
                    y,log=eval_generic_remainder(x,p,w,policy)
                    self.assertEqual(y,dft_ref(x,p,w))
                    self.assertGreater(log.plan_muls+log.plan_adds,0)
                    self.assertEqual(log.writes,n)

    def test_noncoset_partition_has_more_online_work(self):
        n=16;p,w=fixture(n)
        x=[(i*i+3*i+11)%p for i in range(n)]
        baseline,blog=eval_radix2_remainder(x,p,w)
        alternative,alog=eval_generic_remainder(x,p,w,'noncoset16')
        self.assertEqual(baseline,alternative)
        self.assertGreater(alog.muls+alog.adds,blog.muls+blog.adds)

    def test_exact_cyclotomic_root_histogram(self):
        d8=exhaustive_root_split(8)
        d16=exhaustive_root_split(16)
        self.assertEqual(d16['subsets'],12870)
        self.assertEqual(d16['complement_pairs'],6435)
        self.assertEqual(d16['support_histogram']['2'],2)
        self.assertEqual(d16['best_split_total_support'],4)
        self.assertEqual(d16['best_nonperiodic_total_support'],15)
        self.assertEqual(d8['support_histogram']['2'],2)

    def test_radix2_semantic_organizer_merges_zero(self):
        for n in (4,8,16,32,64):
            p,w=fixture(n)
            a=radix2_symbolic_merges(n,p,w)
            self.assertEqual(a['proportional_merges'],0)
            self.assertEqual(a['total_forms'],a['unique_forms'])

    def test_unitary_entropy_gate_bound_is_tight(self):
        for n in (4,8,16,32):
            d=unitary_entropy_audit(n)
            self.assertAlmostEqual(d['max_entropy_increment'],2,places=7)
            self.assertAlmostEqual(d['min_entropy_increment'],2,places=7)
            self.assertEqual(d['gates'],int(d['lower_bound']))

    def test_polynomial_sized_truth_tables_limit_gate_width(self):
        for n in (16,64,256):
            p,w=fixture(n)
            d=lut_gate_bound(n,p,3)
            self.assertLessEqual(d['max_complete_block_arity'],3)
            self.assertGreaterEqual(d['necessary_levels_if_full_width'],(n.bit_length()-1)//2)

if __name__=='__main__':unittest.main()

class CRTBridgeTests(unittest.TestCase):
    def test_every_balanced_split_has_full_bridge_rank(self):
        from phase8 import crt_bridge_certificate
        for n in (4,8,12,16):
            p,w=fixture(n);m=n//2
            candidates=[tuple(range(0,n,2)),tuple(range(m)),tuple(range(1,n,2))]
            if n==16:candidates.append((0,1,2,3,4,8,10,12))
            for a in candidates:
                d=crt_bridge_certificate(n,p,w,a)
                self.assertEqual(d['transfer_rank'],m)
                self.assertGreaterEqual(d['combined_support'],n)

    def test_crt_sparsity_exact_finite_field_search(self):
        from phase8 import enumerate_crt_transfer_supports
        p,w=fixture(16)
        d=enumerate_crt_transfer_supports(16,p,w)
        self.assertEqual(d['pairs'],6435)
        self.assertEqual(d['minimum_transfer_nnz'],16)
        self.assertEqual(d['histogram']['16_periodic'],1)
        self.assertGreater(d['best_nonperiodic_transfer_nnz'],16)
