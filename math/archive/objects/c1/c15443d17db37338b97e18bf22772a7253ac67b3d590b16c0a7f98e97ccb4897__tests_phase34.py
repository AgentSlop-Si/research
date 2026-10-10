import unittest
from phase33_two_sided import P1, GEN1, field_rank, inverse_small, make_cycles
from phase34_products import (
    Fourier, green_matrix, denominator_matrix, add, matmul,
    permutation_successor, permutation_rank_difference,
    swapped_cycle, support_max, minimum_rank_certificate_for_sparse_core
)
from phase34_extensions import patched_two_stage, three_stage, far_cycle_control


class Phase34ExactTests(unittest.TestCase):
    def test_green_inverse_exact(self):
        for n in (8,16):
            cycle=make_cycles(n,1,seed=99)[0]
            for alpha in (3,5):
                B=denominator_matrix(cycle,alpha)
                G=green_matrix(cycle,alpha)
                product=matmul(B,G)
                self.assertTrue(all(product[i][j]==int(i==j) for i in range(n) for j in range(n)))

    def test_permutation_rank_identity(self):
        for n in (8,16,32):
            a,b=make_cycles(n,2,seed=343334)
            sa,sb=permutation_successor(a),permutation_successor(b)
            observed,cycles=permutation_rank_difference(sa,sb)
            self.assertEqual(observed,n-cycles)
            PA=[[int(i==sa[j]) for j in range(n)] for i in range(n)]
            PB=[[int(i==sb[j]) for j in range(n)] for i in range(n)]
            self.assertEqual(field_rank(add(PA,PB,sgn=-1),P1),observed)

    def test_swapped_rank_two(self):
        for n in (8,16,32,64):
            c=make_cycles(n,1,seed=111)[0]
            cs=swapped_cycle(c,1,n//2+1)
            defect,_=permutation_rank_difference(permutation_successor(c),
                                                  permutation_successor(cs))
            self.assertEqual(defect,2)

    def test_exact_stage_inverse_rank_conservation(self):
        for n in (8,16,32,64):
            a,b=make_cycles(n,2,seed=343334)
            defect,_=permutation_rank_difference(permutation_successor(a),
                                                  permutation_successor(b))
            G=add(green_matrix(a,3),green_matrix(b,3))
            GI=inverse_small(G,P1)
            B=denominator_matrix(a,3)
            inv2=pow(2,P1-2,P1)
            core=[[z*inv2%P1 for z in row] for row in B]
            self.assertEqual(field_rank(add(GI,core,sgn=-1),P1),defect)

    def test_sparse_core_fourier_vandermonde(self):
        for n,k in ((8,1),(16,2),(32,3),(64,4),(64,8)):
            c=minimum_rank_certificate_for_sparse_core(n,k)
            self.assertEqual(c['witness_rank_mod_p'],n//(k+1))

    def test_rank_gap_with_phase_patches(self):
        c=patched_two_stage(64)
        self.assertEqual(c['stage_rank_budgets'],[4,4])
        self.assertEqual(c['inverse_correction_rank'],8)
        self.assertEqual(c['Fourier_rigidity_rank_floor'],12)
        self.assertTrue(c['excluded_exact_fourier'])

    def test_rank_gap_with_three_noncommuting_stages(self):
        c=three_stage(64)
        self.assertEqual(c['correction_rank'],6)
        self.assertEqual(c['Fourier_rigidity_rank_floor'],7)
        self.assertTrue(c['excluded_exact_fourier'])

    def test_phase_aware_far_cycle_controls(self):
        for n in (32,64,256):
            c=far_cycle_control(n)
            self.assertEqual(c['first_Weyl_defect_nonzero'],n)
            self.assertEqual(c['second_Weyl_defect_nonzero'],n)
            self.assertGreaterEqual(min(c['independent_order_cycle_deficits']),n//2)

    def test_positive_fourier_weyl_control(self):
        from phase33_two_sided import root_of_unity
        n=16;p=P1
        F=Fourier(n,p)
        w=root_of_unity(n,p,GEN1)
        # (FZ)_ij=F_{i,j+1}, (DF)_ij=w^i F_ij
        # (FD)_ij=w^j F_ij, (Z^-1 F)_ij=F_{i+1,j}
        for i in range(n):
            for j in range(n):
                self.assertEqual(F[i][(j+1)%n],pow(w,i,p)*F[i][j]%p)
                self.assertEqual(pow(w,j,p)*F[i][j]%p,F[(i+1)%n][j])

    def test_positive_sparse_plus_lowrank_control(self):
        n=16;F=Fourier(n)
        P=[[int(i==j) for j in range(n)] for i in range(n)]
        E=add(F,P,sgn=-1)
        r=field_rank(E,P1)
        self.assertGreaterEqual(r,n//2)
        self.assertEqual(add(P,E),F)

    def test_all_size_budget_exclusions(self):
        for n,t,r in ((64,2,8),(64,3,6),(256,3,6),(1024,4,8),
                      (4096,5,10),(8192,6,12)):
            self.assertGreater(n//(2**t+1),r)

if __name__=='__main__':unittest.main()
