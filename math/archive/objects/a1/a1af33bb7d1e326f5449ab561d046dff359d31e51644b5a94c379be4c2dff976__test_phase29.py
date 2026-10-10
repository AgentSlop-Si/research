import os
import sys
import unittest
import json
from pathlib import Path
from random import Random
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from phase29_two_parameter import (P,SEEDS,build_family,certificate,validate,
             slice_family,third_green,bezout,poly_add,poly_mul,
             trace_power_from_matrix,trace_moment_poly)
from phase29_macaulay import (all_permutations_audit,verify_saved_audit,
            exhaustive_anchor_audit,partial_anchor_rows,rank_and_pivots,
            random_partial_trial)
from phase29_executor import three_term_executor
from phase28_synthesis import permuted_scaled,matmul,green_components

ROOT=Path(__file__).resolve().parents[1]
class Phase29(unittest.TestCase):
    def test_one_parameter_full_coprimality_n4(self):
        c=json.loads((ROOT/'certificates/bezout_two_param_N4.json').read_text())
        self.assertTrue(validate(c))
        self.assertEqual(c['upper_bound_joint_complex_solutions_with_multiplicity'],512)

    def test_one_parameter_full_coprimality_n8(self):
        c=json.loads((ROOT/'certificates/bezout_two_param_N8.json').read_text())
        self.assertTrue(validate(c))
        self.assertEqual(c['upper_bound_joint_complex_solutions_with_multiplicity'],8192)

    def test_one_parameter_full_coprimality_n16(self):
        c=json.loads((ROOT/'certificates/bezout_two_param_N16.json').read_text())
        self.assertTrue(validate(c))
        self.assertEqual(c['upper_bound_joint_complex_solutions_with_multiplicity'],131072)

    def test_symbolic_slice_direct_trace_check(self):
        for n in (4,8):
            t,g0,g1,g2=build_family(n,SEEDS[n])
            lam=0 if n==8 else 1
            base=slice_family(g0,g1,lam)
            for s in (1,2):
                poly=trace_moment_poly(trace_power_from_matrix(t,s),base,g2,s)
                for mu in (0,2,3,11):
                    m=[[ (base[i][j]+mu*g2[i][j])%P for j in range(n)] for i in range(n)]
                    if any(not v for row in m for v in row):continue
                    D=1
                    for row in m:
                        for v in row:D=D*v%P
                    from phase28_polynomial import eval_poly
                    self.assertEqual(eval_poly(poly,mu),
                        pow(D,s,P)*(trace_power_from_matrix(m,s)-trace_power_from_matrix(t,s))%P)

    def test_spurious_zero_entry_parameter(self):
        # A gcd at an unlucky slice can come solely from forbidden zero entries.
        n=4;seed=SEEDS[n]
        t,g0,g1,g2=build_family(n,seed)
        p1=trace_moment_poly(trace_power_from_matrix(t,1),g0,g2,1)
        p2=trace_moment_poly(trace_power_from_matrix(t,2),g0,g2,2)
        from phase28_polynomial import gcd_modp
        g=gcd_modp(p1,p2)
        self.assertEqual(len(g),2)
        mu=(-g[0]*pow(g[1],-1,P))%P
        m=[[ (g0[i][j]+mu*g2[i][j])%P for j in range(n)] for i in range(n)]
        self.assertGreater(sum(v==0 for row in m for v in row),0)

    def test_N4_all_full_permutations(self):
        c=json.loads((ROOT/f'certificates/degree4_all_permutations_N4_p{P}.json').read_text())
        self.assertTrue(verify_saved_audit(c))
        self.assertEqual(c['full_rank_cases'],576)

    def test_N8_all_anchor_triples(self):
        c=json.loads((ROOT/f'certificates/anchored_exhaustive_N8_p{P}.json').read_text())
        self.assertEqual(c['tested_partial_mapping_pairs'],112896)
        self.assertEqual(c['rank_histogram'],{'15':112896})
        self.assertEqual(c['failures'],[])
        # Recompute a deterministic subset independently from its saved witnesses.
        t,g0,g1,g2=build_family(8,SEEDS[8])
        from phase29_macaulay import determinant_modp
        for q in c['sample_nonzero_minors']:
            rows=partial_anchor_rows(t,g0,g1,g2,tuple(q['source_rows']),tuple(q['source_cols']))
            minor=[rows[k] for k in q['selected_rows']]
            self.assertEqual(determinant_modp(minor),q['determinant_modp'])

    def test_N8_exhaustive_recompute(self):
        a=exhaustive_anchor_audit(8)
        self.assertEqual(a['rank_histogram'],{'15':112896})
        old=json.loads((ROOT/f'certificates/anchored_exhaustive_N8_p{P}.json').read_text())
        self.assertEqual(a['rank_stream_sha256'],old['rank_stream_sha256'])

    def test_N4_planted_exact_positive_control(self):
        t,g0,g1,g2=build_family(4,SEEDS[4])
        m=[[ (g0[i][j]+2*g1[i][j]+3*g2[i][j])%P for j in range(4)] for i in range(4)]
        rp=[2,0,3,1];cp=[1,3,0,2]
        shifted=permuted_scaled(m,rp,cp,[2,3,4,5],[7,11,13,17])
        rows=partial_anchor_rows(shifted,g0,g1,g2,tuple(rp[:3]),tuple(cp[:3]))
        rank,_=rank_and_pivots(rows)
        self.assertLess(rank,15)

    def test_O_N_executor_matches_dense(self):
        for n in (4,8,16,32,64,128):
            seed=SEEDS.get(n,2800+n)
            lam,mu=3*pow(2,-1,P)%P,5*pow(3,-1,P)%P
            g0,g1=green_components(n,seed*3+2)
            g2=third_green(n,seed*3+4)
            exe=three_term_executor(n,lam,mu,seed)
            rng=Random(n)
            x=[rng.randrange(P) for _ in range(n)]
            candidate=exe.apply(x)
            expected=[sum((g0[i][j]+lam*g1[i][j]+mu*g2[i][j])*x[j]
                          for j in range(n))%P for i in range(n)]
            self.assertEqual(candidate,expected)

    def test_several_random_partial_controls(self):
        self.assertEqual(random_partial_trial(8,100),{15:100})

if __name__=='__main__':unittest.main()
