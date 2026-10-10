"""Independent exact field audits for Phase 32.
Run: python -m unittest -v tests_phase32
"""
import unittest
from itertools import permutations
from random import Random
from phase32_interpolation import (
    P,inv,CyclicGreen,InterpolatedGreen,reference_ntt,root_of_unity,
    modular_rank,is_affine_cycle,audit,
)


def direct_solve(M,b):
    n=len(M)
    x=[list(M[i])+[b[i]%P] for i in range(n)]
    for j in range(n):
        pos=next(i for i in range(j,n) if x[i][j])
        x[j],x[pos]=x[pos],x[j]
        fac=inv(x[j][j]);x[j]=[(v*fac)%P for v in x[j]]
        for r in range(n):
            if r!=j and x[r][j]:
                f=x[r][j];x[r]=[(v-f*w)%P for v,w in zip(x[r],x[j])]
    return [x[i][-1] for i in range(n)]


class Phase32Tests(unittest.TestCase):
    def test_cycle_solver_vs_independent_gaussian(self):
        rng=Random(6232)
        for n in (4,8,16):
            for _ in range(3):
                cycle=list(range(n));rng.shuffle(cycle)
                g=CyclicGreen(cycle,rng.randint(2,1000))
                matrix=[[int(i==j) for j in range(n)] for i in range(n)]
                for t,i in enumerate(cycle):
                    prev=cycle[(t-1)%n]
                    matrix[i][prev]=(matrix[i][prev]-g.alpha)%P
                x=[rng.randrange(P) for _ in range(n)]
                self.assertEqual(g.apply(x),direct_solve(matrix,x))
                self.assertEqual(g.apply([int(j==1) for j in range(n)]),[g.entry(i,1) for i in range(n)])

    def test_exact_five_columns_and_nonaffine_orders(self):
        for n in (8,16,32,64,128):
            m=InterpolatedGreen(n,range(5))
            self.assertTrue(all(not is_affine_cycle(g.cycle) for g in m.greens))
            self.assertTrue(all(all(v for v in gate) for gate in m.gauges))
            for j in range(5):
                y=m.apply([int(t==j) for t in range(n)])
                self.assertEqual(y,[m.expected_fourier_entry(i,j) for i in range(n)])

    def test_two_overlapping_windows_pass_third_fails(self):
        for n in (8,16,32):
            m=InterpolatedGreen(n,range(5))
            for cols in ((0,1,2,3),(1,2,3,4)):
                for rows in ((0,1,2),(3,4,5)):
                    for i in rows:
                        for j in cols:
                            self.assertEqual(m.entry(i,j),m.expected_fourier_entry(i,j))
            self.assertTrue(any(m.entry(i,5)!=m.expected_fourier_entry(i,5) for i in range(n)))

    def test_weyl_partial_success_and_global_failure(self):
        for n in (8,16,64):
            m=InterpolatedGreen(n,range(5))
            omega=m.root
            for j in range(n):
                # Correct: F Z = D F with Z e_j=e_(j+1), D_i=omega^(-i)
                lhs=[m.entry(i,(j+1)%n) for i in range(n)]
                rhs=[m.entry(i,j)*pow(omega,(-i)%n,P)%P for i in range(n)]
                if j<4:self.assertEqual(lhs,rhs)
                # Correct: F D = Z^-1 F, i.e., row i of Z^-1 F is row i+1 of F
                lhs2=[m.entry(i,j)*pow(omega,(-j)%n,P)%P for i in range(n)]
                rhs2=[m.entry((i+1)%n,j) for i in range(n)]
                if j<5:self.assertEqual(lhs2,rhs2)
            self.assertTrue(any(m.entry(i,5)!=m.expected_fourier_entry(i,5) for i in range(n)))

    def test_generic_augmented_rank_six(self):
        for n in (8,16,32):
            m=InterpolatedGreen(n,range(5))
            for i in range(n):
                A=[[g.entry(i,j) for j in range(6)] for g in m.greens]
                A.append([m.expected_fourier_entry(i,j) for j in range(6)])
                self.assertEqual(modular_rank(A),6)

    def test_residual_has_maximal_sampled_rank(self):
        for n in (8,16,32,64):
            m=InterpolatedGreen(n,range(5))
            err=[[m.entry(i,j)-m.expected_fourier_entry(i,j) for j in range(5,n)] for i in range(n)]
            self.assertEqual(modular_rank(err),n-5)

    def test_generic_monomial_uniqueness(self):
        # q=3, N=8, all cycle orders permitted. Check symbolic determinant
        # terms are distinct. Also check the Cramer numerator terms remain distinct.
        n=8;m=InterpolatedGreen(n,range(3),seed=423)
        for i in range(n):
            exps=[]
            for perm in permutations(range(3)):
                exps.append(tuple((g.position[i]-g.position[m.columns[perm[s]]])%n
                                  for s,g in enumerate(m.greens)))
            self.assertEqual(len(set(exps)),6)
            for omitted in range(3):
                exps2=[tuple((m.greens[s].position[i]-m.greens[s].position[m.columns[perm[s]]])%n
                               for s in range(3) if s!=omitted)
                        for perm in permutations(range(3))]
                self.assertEqual(len(set(exps2)),6)

    def test_q_equals_n_exact_full_fourier_small(self):
        rng=Random(9921)
        for n in (8,16):
            m=InterpolatedGreen(n,range(n),seed=320031)
            for i in range(n):
                for j in range(n):
                    self.assertEqual(m.entry(i,j),m.expected_fourier_entry(i,j))
            x=[rng.randrange(P) for _ in range(n)]
            self.assertEqual(m.apply(x),reference_ntt(x))

    def test_extra_null_direction(self):
        for n in (8,16,64):
            m=InterpolatedGreen(n,range(4),extra=1)
            self.assertEqual(m.q,5)
            for i in range(n):
                for j in range(4):
                    self.assertEqual(m.entry(i,j),m.expected_fourier_entry(i,j))

    def test_online_matches_independent_radix_two(self):
        for n in (8,16,32,256,1024):
            result=audit(n,k=5)
            self.assertEqual(result['out_of_sample_column_mismatches'],n)
            self.assertGreater(result['Weyl_shift_defect_nonzeros'],0)

    def test_nonprobed_column_not_rescalable(self):
        for n in (8,16,32):
            m=InterpolatedGreen(n,range(5))
            # If M[:,0]=F[:,0], diagonal equivalence with no permutations
            # forces every further M[:,j] to be proportional to F[:,j].
            self.assertTrue(any(
                m.entry(i,5)*m.expected_fourier_entry(0,5)%P !=
                m.entry(0,5)*m.expected_fourier_entry(i,5)%P
                for i in range(n)))

    def test_parameter_count_and_input_independent_cost(self):
        for n in (8,32,128):
            m=InterpolatedGreen(n,range(5))
            self.assertEqual(len(m.greens),5)
            self.assertEqual(sum(len(x) for x in m.gauges),5*n)
            self.assertEqual(sum(len(g.cycle) for g in m.greens),5*n)


if __name__=='__main__':unittest.main()
