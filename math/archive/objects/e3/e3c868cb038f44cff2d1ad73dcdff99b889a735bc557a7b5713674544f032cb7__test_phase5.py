import itertools
import random
import unittest
from math import gcd
import phase5 as pg


class Phase5Test(unittest.TestCase):
    def test_mask_rank_formula_all_phase_differences(self):
        for m in (2,3,4,5,6,7,8,9,10,12,16):
            p,omega=pg.field_for_m(m)
            a=list(range(m))
            for delta in range(1,m):
                E,L,R=pg.transition_factorization(m,p,omega,a,delta)
                self.assertEqual(len(L[0]),m//gcd(m,delta))
                self.assertEqual(pg.rank_mod(E,p),m//gcd(m,delta))

    def test_tunable_mask_rank_without_losing_universality(self):
        for m in (2,3,4,5,6,8,9,12):
            p,omega=pg.field_for_m(m)
            for r in range(1,m+1):
                a=[j%r for j in range(m)]
                self.assertEqual(pg.transition_mask_rank_formula(m,a,1),r)
                self.assertEqual(pg.rank_mod(pg.transition_mask(m,p,omega,a,1),p),r)
                for h in range(m):
                    V,lamb=pg.shear_vandermonde(m,p,omega,a,h)
                    self.assertEqual(len(set(lamb)),m)
                    self.assertEqual(pg.rank_mod(V,p),m)

    def test_transition_entrywise_identity(self):
        for m in (3,4,6,8,12):
            p,omega=pg.field_for_m(m)
            rng=random.Random(m*919)
            for _ in range(8):
                a=[rng.randrange(m) for _ in range(m)]
                h=rng.randrange(m);delta=rng.randrange(1,m)
                V0,_=pg.shear_vandermonde(m,p,omega,a,h)
                V1,_=pg.shear_vandermonde(m,p,omega,a,(h+delta)%m)
                E=pg.transition_mask(m,p,omega,a,delta)
                self.assertEqual(V1,[[V0[t][j]*E[t][j]%p for j in range(m)] for t in range(m)])

    def test_every_gauge_same_raw_full_dft(self):
        rng=random.Random(20261010)
        for m in (2,3,4,5,6,7,8,9,12):
            p,omega=pg.field_for_m(m)
            x=[rng.randrange(p) for _ in range(m*m)]
            expected=pg.direct_dft(x,p,omega)
            for r in sorted(set((1,2,3,max(1,m//2),m))):
                if r>m:continue
                a=[j%r for j in range(m)]
                got,cert=pg.full_orbit_execution(x,m,p,omega,a)
                self.assertEqual(got,expected)
                self.assertTrue(all(c['rank_V']==m for c in cert))
                self.assertEqual(sum(c['nonzero_K'] for c in cert),m**3-m**2+m)

    def test_orthogonal_fourier_gauge_circulant_and_all_outputs(self):
        rng=random.Random(1212)
        for m in (2,3,4,6,8,12,16):
            p,omega=pg.field_for_m(m)
            for h in range(m):
                V,K=pg.orthogonal_gauge_matrix(m,p,omega,h)
                self.assertEqual(sum(z!=0 for row in K for z in row), m if h==0 else m*m)
            x=[rng.randrange(p) for _ in range(m*m)]
            got,_=pg.full_orbit_execution(x,m,p,omega,[0]*m,'orthogonal')
            self.assertEqual(got,pg.direct_dft(x,p,omega))

    def test_mst_closed_form_and_kruskal(self):
        for m in range(2,129):
            pred,pieces=pg.optimal_mask_spanning_tree(m)
            actual,edges=pg.kruskal_mask_mst(m)
            self.assertEqual(pred,actual,(m,pred,actual))
            self.assertEqual(len(edges),m-1)
        for k in range(1,8):
            m=2**k
            pred,_=pg.optimal_mask_spanning_tree(m)
            self.assertEqual(pred,m*k)

    def test_mst_brute_force_all_trees(self):
        for m in range(2,8):
            minimum=min(pg.prufer_weight(code,m) for code in itertools.product(range(m),repeat=m-2))
            pred,_=pg.optimal_mask_spanning_tree(m)
            self.assertEqual(minimum,pred)

    def test_prime_orthogonal_gauge_rigidity(self):
        for m in (2,3,5):
            good=[]
            for a in itertools.product(range(m),repeat=m):
                if pg.affine_nodes_all_distinct_prime(m,a):good.append(a)
            self.assertEqual(len(good),m)
            self.assertTrue(all(len(set(a))==1 for a in good))
        m=7;rng=random.Random(77)
        for _ in range(200):
            a=[rng.randrange(m) for _ in range(m)]
            self.assertEqual(pg.affine_nodes_all_distinct_prime(m,a),len(set(a))==1)


if __name__=='__main__':unittest.main()
