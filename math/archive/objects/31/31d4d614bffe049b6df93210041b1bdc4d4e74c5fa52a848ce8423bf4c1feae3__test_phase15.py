import unittest
import numpy as np
import math
from phase15_symmetry import (
    PRIME,margulis_maps,half_translation,perm_commutes,complex_commutator_spectrum,
    modular_commutator_certificate,modular_dft,rank_mod,mixed_green_network,
    green_apply,dense_green_matrix,graph_symmetry_delta,matrix_network_and_breaking_budget,
    finite_rank_defect_audit,group_twirl,normalized_dft,commutator_from_permutation
)

class Phase15ExactSymmetryTests(unittest.TestCase):
    def test_all_four_margulis_permutations_commute_with_three_half_translations(self):
        for s in (2,4,6,8,10,12,16):
            maps=margulis_maps(s)
            for a in ('x','y','xy'):
                q=half_translation(s,a)
                for p in maps:self.assertTrue(perm_commutes(p,q),(s,a))

    def test_original_mixed_graph_is_not_polarized(self):
        for s in (4,8):
            maps=margulis_maps(s)
            # Two x-shear permutations and two y-shear permutations per layer.
            self.assertTrue(any(p[i]//s!=i//s for p in maps[:2] for i in range(s*s)))
            self.assertTrue(any(p[i]%s!=i%s for p in maps[2:] for i in range(s*s)))

    def test_involution_and_four_group_product(self):
        for s in (2,4,6,8,16):
            n=s*s;T={a:half_translation(s,a) for a in ('x','y','xy')}
            for a,v in T.items():self.assertTrue(np.array_equal(v[v],np.arange(n)))
            self.assertTrue(np.array_equal(T['x'][T['y']],T['xy']))

    def test_odd_side_no_halves(self):
        for s in (3,5,7):
            with self.assertRaises(ValueError):half_translation(s,'x')

    def test_modular_2x2_tensor_commutator_polynomials(self):
        for s in (2,4,8,16):
            for a in ('x','y','xy'):
                v=modular_commutator_certificate(s,a)
                self.assertEqual(v['nonzero_residual_entries'],0)
                self.assertEqual(v['trace_H_mod_p'],2*s*s)

    def test_complex_singular_spectra(self):
        for s in (2,4,6,8,10,12):
            for a in ('x','y','xy'):
                v=complex_commutator_spectrum(s,a)
                self.assertLess(v['max_spectrum_error'],1e-9)
                self.assertAlmostEqual(v['normalized_frobenius'],math.sqrt(2),places=8)

    def test_translation_invariant_green_solvers_commute_exactly(self):
        for s in (2,4,8):
            n=s*s;p=margulis_maps(s)[1];w=[2]*n
            for axis in ('x','y','xy'):
                tau=half_translation(s,axis)
                for i in (0,1,2,n//2,n-1):
                    x=[0]*n;x[i]=1
                    y=[0]*n;y[int(tau[i])]=1
                    lhs=green_apply(p,w,y,PRIME)
                    rhs=green_apply(p,w,x,PRIME)
                    rhs_shift=[0]*n
                    for k in range(n):rhs_shift[int(tau[k])]=rhs[k]
                    self.assertEqual(lhs,rhs_shift)

    def test_double_mixed_green_network_commutes(self):
        for s in (2,4,8):
            n=s*s;tau=half_translation(s,'x')
            for i in (0,1,n//2,n-1):
                x=[0]*n;x[i]=1
                y=[0]*n;y[int(tau[i])]=1
                lhs=mixed_green_network(s,y)
                rhs=mixed_green_network(s,x)
                self.assertTrue(all(lhs[int(tau[k])]==rhs[k] for k in range(n)))

    def test_seed_orbit_is_formally_incompatible_with_fourier(self):
        for s in (2,4,8,16):
            U=modular_dft(s)
            n=s*s;tau=half_translation(s,'x')
            self.assertEqual(tau[0],n//2)
            self.assertFalse(np.array_equal(U[:,0],U[:,n//2]))
            self.assertTrue(np.array_equal(U[:,0],np.full(n,pow(s,-1,PRIME))))
            expected=np.array([(pow(s,-1,PRIME) if j%2==0 else -pow(s,-1,PRIME))%PRIME for j in range(n)])
            self.assertTrue(np.array_equal(U[:,n//2],expected))

    def test_no_symmetry_breaking_operator_bound_sharp(self):
        for s in (2,4,6,8):
            U=normalized_dft(s);tau=half_translation(s,'x')
            # Zero operator commutes and achieves operator-norm error 1.
            self.assertAlmostEqual(np.linalg.norm(U,2),1.,places=9)
            T0=(U+U[np.ix_(tau,tau)])/2
            self.assertLess(np.linalg.norm(T0[:,tau]-T0[tau,:]),1e-10)
            self.assertAlmostEqual(np.linalg.norm(U-T0)/np.linalg.norm(U),1/math.sqrt(2),places=9)

    def test_fourfold_twirl_sharp_frobenius_obstruction(self):
        for s in (2,4,6,8,10,12):
            value=group_twirl(s)
            self.assertAlmostEqual(value['relative_min_frobenius'],math.sqrt(3)/2,places=8)
            self.assertAlmostEqual(value['relative_projection_norm'],1/2,places=8)

    def test_actual_green_inverse_matches_cycle_solver(self):
        s=4;n=s*s;p=margulis_maps(s)[0]
        rng=np.random.default_rng(1511)
        w=.12+.03*rng.standard_normal(n)
        G=dense_green_matrix(p,w)
        x=rng.standard_normal(n)
        self.assertLess(np.linalg.norm(G@x-np.array(green_apply(p,w,x))),1e-10)

    def test_weight_asymmetry_bound(self):
        for s in (2,4):
            for amount in (0,.00001,.002):
                r=matrix_network_and_breaking_budget(s,amount)
                self.assertLessEqual(r['computed_commutator_norm'],r['upper_commutator_budget']+1e-9)
                self.assertGreaterEqual(r['actual_operator_error']+1e-9,r['necessary_operator_error'])
                if amount==0:self.assertAlmostEqual(r['upper_commutator_budget'],0.)

    def test_exact_finite_field_rank_perturbations(self):
        for s,k in ((2,0),(4,0),(4,1),(4,3),(8,1),(8,5)):
            n=s*s
            mods={((j//4)%2,j%4,(j*7+1)%n):3 for j in range(k)}
            for axis in ('x','y','xy'):
                v=finite_rank_defect_audit(s,mods,axis=axis)
                self.assertLessEqual(v['rank_difference'],k)
                self.assertEqual(v['Fourier_commutator_rank'], n//2 if axis=='x' else n)
                self.assertGreaterEqual(v['residual_commutator_rank'],v['Fourier_commutator_rank']-2*k)

    def test_full_rank_y_commutator_requires_half_N_changes_for_exactness(self):
        for s in (2,4,8):
            n=s*s
            mods={(0,j%4,(5*j+1)%n):3 for j in range(min(n//2-1,5))}
            v=finite_rank_defect_audit(s,mods,axis='y')
            self.assertEqual(v['Fourier_commutator_rank'],n)
            self.assertGreater(v['residual_commutator_rank'],0)

    def test_rank_perturbation_can_be_nontrivial(self):
        s=4;n=s*s
        v=finite_rank_defect_audit(s,{(0,1,3):3,(1,2,6):5})
        self.assertEqual(v['rank_difference'],2)
        self.assertGreaterEqual(v['commutator_rank'],1)

if __name__=='__main__':unittest.main(verbosity=2)
