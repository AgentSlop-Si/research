"""Exact checks for Phase 14; every claimed mathematical statement has an independent test."""
import unittest
from random import Random
from math import isclose,sqrt

from transverse_green import (
    FIELD,graphs_polarized,green_apply,run_network,run_layer,root,
    network_block,fblock,rank_mod,cut_budget,prefix_gate,
    graph_gap_lower_bound,graph_gap_numeric,transverse_error_bound,
    modular_dft,graphs_mixed_original,
)
from weyl_gate import weyl_certificate,shift,backward_shift,modulation
from exact_audit import exhaustive_cut_gate_16,sharp_q_s_paths_exact,unitary_block_singulars


class Phase14(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.g2=graphs_polarized(2)
        cls.g4=graphs_polarized(4)

    def test_green_cycle_solver_residual(self):
        rng=Random(14)
        for gg,n in [(self.g2,16),(self.g4,256)]:
            for graph in gg[0][:4]+gg[1][:4]:
                x=[rng.randrange(FIELD) for _ in range(n)]
                v=green_apply(graph,x)
                for i in range(n):
                    self.assertEqual((v[i]-graph.weights[i]*v[graph.pi[i]])%FIELD,x[i])

    def test_each_graph_is_a_valid_permutation(self):
        for gg,n in [(self.g2,16),(self.g4,256)]:
            for g in gg[0]+gg[1]:
                self.assertEqual(sorted(g.pi),list(range(n)))
                self.assertTrue(all(w!=0 for w in g.weights))

    def test_polarization_support(self):
        for gg,s in [(self.g2,4),(self.g4,16)]:
            for g in gg[0]:
                self.assertTrue(all(i%s==g.pi[i]%s for i in range(s*s)))
            for g in gg[1]:
                self.assertTrue(all(i//s==g.pi[i]//s for i in range(s*s)))

    def test_transverse_rank_16(self):
        for x,yp in [(0,1),(1,3),(3,0)]:
            A=network_block(self.g2,4,x,yp)
            B=fblock(16,x,yp)
            self.assertEqual(rank_mod(A),1)
            self.assertEqual(rank_mod(B),4)

    def test_transverse_rank_256(self):
        for x,yp in [(0,1),(8,5),(15,14)]:
            A=network_block(self.g4,16,x,yp)
            B=fblock(256,x,yp)
            self.assertEqual(rank_mod(A),1)
            self.assertEqual(rank_mod(B),16)

    def test_rank_one_minors_vanish(self):
        a=network_block(self.g2,4,1,2)
        for i in range(4):
            for j in range(i+1,4):
                for k in range(4):
                    for l in range(k+1,4):
                        self.assertEqual((a[i][k]*a[j][l]-a[i][l]*a[j][k])%FIELD,0)

    def test_fourier_minor_nonzero(self):
        b=fblock(16,1,2)
        self.assertNotEqual((b[0][0]*b[1][1]-b[0][1]*b[1][0])%FIELD,0)

    def test_mixed_axis_escape_has_full_transverse_rank(self):
        # Crucial scope check: Phase 13's original arrangement has both axes
        # within stages and does NOT obey the new rank-one polarized bound.
        layers=graphs_mixed_original(4,copies=3)
        for x,yp in [(0,1),(1,2),(3,0)]:
            B=network_block(layers,4,x,yp)
            self.assertEqual(rank_mod(B),4)

    def test_all_subset_expander_gate_N16(self):
        out=exhaustive_cut_gate_16(self.g2[0]+self.g2[1])
        self.assertEqual(out['subsets_checked'],65534)
        self.assertGreaterEqual(out['minimal_capacity_slack'],0)

    def test_prefix_expander_gate_N256(self):
        v=prefix_gate(self.g4)
        self.assertEqual(v['failed_prefixes'],[])
        self.assertGreaterEqual(v['min_slack'],0)

    def test_random_subset_gate_N256(self):
        rng=Random(20261010);gs=self.g4[0]+self.g4[1]
        for _ in range(80):
            size=rng.randrange(1,256)
            R=set(rng.sample(range(256),size))
            self.assertGreaterEqual(cut_budget(gs,R),min(size,256-size))

    def test_analytic_graph_gap(self):
        self.assertGreater(graph_gap_lower_bound(),2.)
        for t in [2,3,4,8]:
            self.assertGreaterEqual(graph_gap_numeric(t),graph_gap_lower_bound()-1.e-8)

    def test_complex_flat_singulars(self):
        for s in [2,4,8,16]:
            vals=unitary_block_singulars(s,x=1,yp=s-1)
            self.assertTrue(all(abs(z-1/sqrt(s))<1.e-10 for z in vals))

    def test_exact_q_paths_sharpness(self):
        for s in [2,4,8]:
            result=sharp_q_s_paths_exact(s)
            self.assertEqual(result['exact_fourier_entries_checked'],s**4)

    def test_error_lower_bound(self):
        self.assertAlmostEqual(transverse_error_bound(16),sqrt(15/16))
        self.assertAlmostEqual(transverse_error_bound(16,2),sqrt(14/16))
        self.assertEqual(transverse_error_bound(16,16),0.)

    def test_full_network_differs_from_DFT(self):
        rng=Random(18)
        x=[rng.randrange(FIELD) for _ in range(16)]
        self.assertNotEqual(run_network(self.g2,x),modular_dft(x))

    def test_weyl_positive_control(self):
        cert=weyl_certificate(lambda v:modular_dft(v),16,rounds=4)
        self.assertTrue(cert['passes'])
        self.assertEqual(cert['shift_modulation_defect_nonzeros'],[0]*4)

    def test_weyl_false_candidate_with_correct_seed(self):
        def fake(v):
            out=modular_dft(v)
            out[0]=(out[0]+v[1])%FIELD
            return out
        cert=weyl_certificate(fake,16,rounds=5,seed=41)
        self.assertTrue(cert['seed_matches_F'])
        self.assertFalse(cert['passes'])
        self.assertTrue(any(cert['shift_modulation_defect_nonzeros']))

    def test_weyl_negative_green(self):
        cert=weyl_certificate(lambda v:run_network(self.g2,v),16,rounds=2)
        self.assertFalse(cert['passes'])

    def test_complex_direct_inverse_and_error_bound(self):
        # Independent from finite-field cycle solvers: invert complex matrices.
        from numerical_weight_audit import run
        result=run()
        self.assertGreaterEqual(result['operator_norm_error_after_optimal_scalar'],
                                result['rigorous_lower_bound']-1.e-8)
        self.assertGreaterEqual(result['relative_Frobenius_error_after_optimal_scalar'],
                                result['rigorous_lower_bound']-1.e-8)

    def test_dimension_count_mixed_rook(self):
        # Two arbitrary rook-supported layers, including mixed-axis sums.
        for s in [4,8,16]:
            n=s*s;d=n*(2*s-1)
            codim=n*n-(2*d-n)
            self.assertEqual(codim,s*s*(s-1)*(s-3))
            self.assertGreater(codim,0)

    def test_shift_modulation_identity(self):
        n=16;w=root(n)
        rng=Random(15)
        for _ in range(3):
            x=[rng.randrange(FIELD) for _ in range(n)]
            Fx=modular_dft(x)
            self.assertEqual(modular_dft(shift(x)),modulation(Fx,w,FIELD))
            self.assertEqual(modular_dft(modulation(x,w,FIELD)),backward_shift(Fx))

if __name__=='__main__':unittest.main()
