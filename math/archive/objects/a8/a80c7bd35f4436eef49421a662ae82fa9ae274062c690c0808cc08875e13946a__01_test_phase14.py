"""Phase14 isolated regression tests; exact claims checked numerically plus mod-p auditor."""
from __future__ import annotations
import itertools
import math
import unittest
import numpy as np
import phase_bank as bank
import gram_union as gu
import unit_step_core as core
import mixedradix as v13


class BankPhaseTests(unittest.TestCase):
    def setUp(self):
        self.rng=np.random.default_rng(99012)

    def random_x(self,n):
        return self.rng.normal(size=n)+1j*self.rng.normal(size=n)

    def check_output_and_energy(self,x,result,tol=1e-9):
        y=np.fft.fft(x)/math.sqrt(len(x))
        err=float(np.vdot(y-result.output,y-result.output).real)
        self.assertAlmostEqual(err,result.squared_error_certificate,delta=tol*max(1,len(x)))
        return err

    def test_all_bank_energy_is_exact_parseval(self):
        for g,m,M in [(16,3,4),(32,5,4),(64,1,8),(128,3,8)]:
            x=self.random_x(g*m)
            a=bank.analyze_banks(x,M)
            self.assertAlmostEqual(float(a.energy.sum()),float(np.vdot(x,x).real),delta=1e-9)
            for s in range(m):
                for t in range(M):
                    st=core.ChirpState(a.states[s].a,(a.states[s].beta+t*a.K)%g)
                    brute=core.compress_blocks(x.reshape(g,m)[:,s],M,st)
                    np.testing.assert_allclose(a.compressed[s,:,t],brute,atol=2e-12,rtol=2e-12)
                    self.assertAlmostEqual(a.energy[s,t],float(np.vdot(brute,brute).real/M),delta=1e-10)

    def test_known_arbitrary_masks_exact_energy_certificate(self):
        for g,m,M,mask in [
            (16,3,4,((1,2),(0,),())),
            (32,3,4,((),(),())),
            (64,1,8,((1,3,5),)),
            (128,5,8,((0,),(1,2),(3,),(),(2,4,5))),
        ]:
            x=self.random_x(g*m)
            res=bank.known_banks(x,mask,M)
            self.check_output_and_energy(x,res)
            p=bank.projected_input(x,mask,M)
            np.testing.assert_allclose(res.output,np.fft.fft(p)/math.sqrt(g*m),atol=2e-10)

    def test_known_exact_dense_structured_signal(self):
        g,m,M=128,3,8
        mask=((2,),(6,),(0,))
        x=bank.constructed_bank_signal(g,m,M,mask,seed=1)
        self.assertEqual(int(np.count_nonzero(abs(x)>1e-12)),x.size)
        r=bank.known_banks(x,mask,M)
        np.testing.assert_allclose(r.output,np.fft.fft(x)/math.sqrt(len(x)),atol=2e-11)
        self.assertLess(r.theoretical_relative_l2_error,1e-6)
        self.assertEqual(r.selected_column_banks,m)

    def test_adaptive_finds_known_banks(self):
        g,m,M=128,3,8
        mask=((5,),(4,),(3,))
        x=bank.constructed_bank_signal(g,m,M,mask,seed=3)
        a=bank.analyze_banks(x,M)
        pred=bank.budget_mask(a,1e-7)
        self.assertEqual(pred,mask)
        result=bank.evaluate_mask(a,pred)
        np.testing.assert_allclose(result.output,np.fft.fft(x)/math.sqrt(len(x)),atol=2e-11)
        self.assertLess(result.theoretical_relative_l2_error,1e-6)

    def test_adaptive_on_noisy_signal_meets_requested_energy(self):
        g,m,M=128,3,8
        mask=((1,),(2,),(3,))
        signal=bank.constructed_bank_signal(g,m,M,mask,seed=8)
        x=signal+0.008*self.random_x(g*m)
        r=bank.adaptive_banks(x,0.04,M)
        self.assertLessEqual(r.theoretical_relative_l2_error,0.0400001)
        self.check_output_and_energy(x,r)
        self.assertLessEqual(r.selected_column_banks,m+3)

    def test_greedy_is_optimal_at_fixed_pass_count(self):
        g,m,M=8,3,2
        a=bank.analyze_banks(self.random_x(g*m),M)
        for L in range(m*M+1):
            best=bank.fixed_count_mask(a,L)
            captured=sum(a.energy[s,t] for s in range(m) for t in best[s])
            brute=max((sum(a.energy.flat[i] for i in group)
                       for group in itertools.combinations(range(m*M),L)),default=0.)
            self.assertAlmostEqual(captured,brute,delta=1e-10)

    def test_exact_frame_matches_reference_for_arbitrary_x(self):
        for g,m,M in [(16,3,4),(32,5,4),(128,3,8)]:
            x=self.random_x(g*m)
            mask=[tuple(range(M)) for _ in range(m)]
            r=bank.known_banks(x,mask,M)
            np.testing.assert_allclose(r.output,np.fft.fft(x)/math.sqrt(len(x)),atol=3e-10)
            self.assertLess(r.squared_error_certificate,1e-8)
            a=bank.analyze_banks(x,M)
            ra=bank.evaluate_mask(a,mask)
            np.testing.assert_allclose(ra.output,r.output,atol=3e-10)
            self.assertLess(ra.work_proxy['odd_factor_fft_proxy'],
                            M*(len(x)*math.log2(m)))

    def test_uniform_bank_energy_is_adversarial_to_adaptivity(self):
        g,m,M=128,3,8
        x=np.zeros((g,m),dtype=np.complex128)
        x[::M,:]=1.0
        flat=x.reshape(-1)
        a=bank.analyze_banks(flat,M)
        np.testing.assert_allclose(a.energy,a.energy[0,0]*np.ones_like(a.energy),atol=1e-10)
        for eps in (0.01,0.1,0.25,0.5):
            selected=bank.budget_mask(a,eps)
            count=sum(map(len,selected))
            self.assertGreaterEqual(count,math.ceil((1-eps*eps)*m*M-1e-10))
            r=bank.evaluate_mask(a,selected)
            self.assertLessEqual(r.theoretical_relative_l2_error,eps+1e-8)

    def test_degenerate_odd_length_uses_exact_CT_for_full_mask(self):
        for n in (1,3,5,9,15):
            x=self.random_x(n)
            full=[(0,) for _ in range(n)]
            r=bank.known_banks(x,full,1)
            np.testing.assert_allclose(r.output,np.fft.fft(x)/math.sqrt(n),atol=1e-12)
            a=bank.analyze_banks(x,1)
            q=bank.evaluate_mask(a,full)
            np.testing.assert_allclose(q.output,r.output,atol=1e-12)

    def test_invalid_banks_and_budget_rejected(self):
        x=self.random_x(48)
        with self.assertRaises(ValueError):bank.known_banks(x,((0,),),4)
        with self.assertRaises(ValueError):bank.known_banks(x,((9,),(),()),4)
        a=bank.analyze_banks(x,4)
        with self.assertRaises(ValueError):bank.budget_mask(a,-0.1)


class NoncommutingGramTests(unittest.TestCase):
    def setUp(self):
        self.rng=np.random.default_rng(110)

    def test_noncommutator_and_gram_condition(self):
        for g,m,M in [(32,3,4),(64,3,8),(128,3,8),(256,3,8)]:
            states=gu.example_noncommuting_states(g,m,M)
            v=gu.sample_commutator(g,M,*states[0])
            self.assertGreater(v['commutator_frobenius'],0.01)
            self.assertEqual(v['commutator_rank_numerical'],2)
            self.assertGreater(v['overlap_absolute'],0.)
            self.assertLess(v['overlap_absolute'],1.)
            c=v['overlap_absolute']
            self.assertAlmostEqual(v['commutator_frobenius']**2,2*c*c*(1-c*c),delta=1e-10)

    def test_q2_exact_on_dense_noncommuting_chirp_union(self):
        for g,m,M in [(32,3,4),(64,3,8),(128,3,8)]:
            families=gu.example_noncommuting_states(g,m,M)
            x=gu.constructed_union_signal(g,m,M,families,seed=123)
            self.assertEqual(np.count_nonzero(abs(x)>1e-12),len(x))
            r=gu.union_projection(x,families,M,diagnostic_projected=True)
            np.testing.assert_allclose(r.output,np.fft.fft(x)/math.sqrt(len(x)),atol=2e-10)
            np.testing.assert_allclose(r.projected_input,x,atol=2e-11)
            self.assertLess(r.residual_squared,1e-8)
            self.assertLess(r.maximum_gram_condition,10)

    def test_q2_arbitrary_input_has_exact_l2_error_formula(self):
        for g,m,M in [(32,3,4),(128,5,8)]:
            fam=gu.example_noncommuting_states(g,m,M)
            x=self.rng.normal(size=g*m)+1j*self.rng.normal(size=g*m)
            r=gu.union_projection(x,fam,M,diagnostic_projected=True)
            err=np.linalg.norm(np.fft.fft(x)/math.sqrt(len(x))-r.output)**2
            self.assertAlmostEqual(err,r.residual_squared,delta=3e-9)
            np.testing.assert_allclose(r.output,np.fft.fft(r.projected_input)/math.sqrt(len(x)),atol=2e-10)
            self.assertAlmostEqual(np.linalg.norm(x-r.projected_input)**2,r.residual_squared,delta=3e-9)

    def test_q1_gram_matches_single_selected_bank(self):
        g,m,M=128,3,8
        sts=bank.base_states(g,m)
        fam=[(core.ChirpState(st.a,(st.beta+(s+1)*(g//M))%g),) for s,st in enumerate(sts)]
        masks=tuple(((s+1)%M,) for s in range(m))
        x=self.rng.normal(size=g*m)+1j*self.rng.normal(size=g*m)
        r=gu.union_projection(x,fam,M)
        p=bank.known_banks(x,masks,M,sts)
        np.testing.assert_allclose(r.output,p.output,atol=1e-10)
        self.assertAlmostEqual(r.residual_squared,p.squared_error_certificate,delta=1e-9)

    def test_singular_gram_is_not_silently_pseudoinverted(self):
        g,m,M=128,3,8
        st=core.ChirpState(1,0)
        fam=[(st,st)]*m
        x=self.rng.normal(size=g*m)+1j*self.rng.normal(size=g*m)
        with self.assertRaises(ValueError):gu.union_projection(x,fam,M)

    def test_no_selected_states_gives_zero_with_energy_certificate(self):
        g,m,M=64,3,8
        x=self.rng.normal(size=g*m)+1j*self.rng.normal(size=g*m)
        r=gu.union_projection(x,[()]*m,M)
        self.assertLess(np.linalg.norm(r.output),1e-10)
        self.assertAlmostEqual(r.residual_squared,r.energy,delta=1e-10)

    def test_q2_normalized_rank_is_twice_single(self):
        g,m,M=128,3,8
        K=g//M
        fam=gu.example_noncommuting_states(g,m,M)
        # Each block's 2x2 Gram is non-singular in this example. Hence the
        # union projector has rank 2Km = 2N/M (no miraculous full rank).
        expected_rank=2*K*m
        self.assertEqual(expected_rank,2*g*m//M)
        self.assertLess(expected_rank,g*m)

class RootTableTests(unittest.TestCase):
    def test_one_root_decoder_against_preserved_full_state_decoder(self):
        import one_root_chirp as orc
        rng=np.random.default_rng(101)
        for g,M in [(16,4),(32,4),(64,8),(128,8),(256,8)]:
            roots=orc.one_root_table(g)
            for a,beta in [(1,0),(1,g//3),(1+g//4,1)]:
                state=core.ChirpState(a,beta)
                x=rng.normal(size=g)+1j*rng.normal(size=g)
                c1=orc.compress(x,g,M,state,roots)
                c2=core.compress_blocks(x,M,state)
                np.testing.assert_allclose(c1,c2,atol=2e-10)
                z1=orc.decode(c1,g,M,state,roots)
                z2=core.decode_balanced_scan(c2,g,M,state)
                np.testing.assert_allclose(z1,z2,atol=3e-10)
                target=np.fft.fft(core.materialize_projected_signal(x,M,state))/math.sqrt(g)
                np.testing.assert_allclose(z1,target,atol=3e-10)

if __name__=="__main__":
    unittest.main(verbosity=2)
