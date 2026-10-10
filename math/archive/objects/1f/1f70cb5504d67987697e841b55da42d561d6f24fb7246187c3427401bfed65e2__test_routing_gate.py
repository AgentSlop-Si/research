import random
import unittest
from math import gcd
import routing_gate as rg


class RoutingGateTest(unittest.TestCase):
    def test_gate_dichotomy_and_channel_congruence(self):
        for q,m,p in [(6,10,241),(7,8,998244353),(8,7,998244353),
                       (8,8,998244353),(16,16,998244353)]:
            w=rg.primitive_n_root(p,q*m)
            for a in range(m):
                for mu in (1,w,pow(w,5,p)):
                    matched=rg.matched_channels(q,m,p,w,a,mu)
                    self.assertIn(len(matched),(0,gcd(a*q+1,m)))
                    for h in range(m):
                        vals=[rg.kernel(q,m,p,w,a,mu,h,s) for s in range(q)]
                        if h in matched:
                            self.assertEqual(sum(z!=0 for z in vals),1)
                            self.assertEqual(set(vals),{0,q%p})
                        else:
                            self.assertEqual(sum(z!=0 for z in vals),q)

    def test_nontrivial_gcd_example(self):
        q,m,p,a,mu=6,10,241,4,1
        w=rg.primitive_n_root(p,q*m)
        self.assertEqual(rg.matched_count_bound(q,m,a),5)
        self.assertEqual(rg.matched_channels(q,m,p,w,a,mu),[0,2,4,6,8])
        self.assertIsNone(rg.routing_pair(q,m))

    def test_coprime_arbitrary_full_dfts_and_inverse_representation(self):
        p=998244353
        rng=random.Random(271828)
        for q,m in [(7,8),(8,7),(7,16),(16,7),(16,17),(17,16)]:
            w=rg.primitive_n_root(p,q*m)
            a,b=rg.routing_pair(q,m)
            self.assertEqual((a*q+1)%m,0)
            for _ in range(3):
                x=[rng.randrange(p) for j in range(q*m)]
                got,B,C=rg.two_stage_arbitrary_raw_routing(x,q,m,p,w)
                expected=rg.direct_dft(x,p,w)
                self.assertEqual(got,expected)
                self.assertTrue(rg.verify_universal_representation(x,q,m,p,w,B))
                for h in range(m):
                    for s in range(q):
                        j=(s+b*h)%q
                        self.assertEqual(got[h+s*m],q*B[j][h]%p)
                for j in range(q):
                    mu=pow(w,m*j,p)
                    self.assertEqual(rg.matched_channels(q,m,p,w,a,mu),list(range(m)))

    def test_square_dense_graph_exact_counts(self):
        p=998244353
        for m in (2,4,8,16,32):
            w=rg.primitive_n_root(p,m*m)
            result=rg.square_coset_density(m,p,w)
            self.assertEqual(result['total_nonzero_edges'],m**3-m**2+m)
            self.assertTrue(result['one_routed_orbit_per_channel'])
            self.assertEqual(result['full_rank_channels'],m)
            self.assertEqual(result['per_channel'],[m*m-m+1]*m)

    def test_full_rank_kernel_factorization(self):
        p=998244353
        for m in (2,4,8,16):
            w=rg.primitive_n_root(p,m*m)
            params=[(j,pow(w,j,p)) for j in range(m)]
            for h in range(m):
                got=rg.matrix_factorization_check(m,m,p,w,params,h)
                self.assertEqual(got['rank'],m)
                self.assertEqual(got['nonzero_edges'],m*m-m+1)

    def test_rank_one_displacement_and_quantum_weyl(self):
        p=998244353
        for m in (2,4,8,16):
            w=rg.primitive_n_root(p,m*m)
            eta=pow(w,m,p)
            self.assertTrue(rg.weyl_commutator_certificate(m,p,eta))
            params=[(j,pow(w,j,p)) for j in range(m)]
            for h in range(m):
                d=rg.displacement_certificate(m,m,p,w,params,h)
                self.assertEqual(d['rank'],1)
                self.assertEqual(d['zero_defect_columns'],[h])
                self.assertEqual(d['kernel_rank'],m)
        for q,m in ((7,8),(16,17)):
            w=rg.primitive_n_root(p,q*m)
            a,_=rg.routing_pair(q,m)
            params=[(a,pow(w,m*j,p)) for j in range(q)]
            for h in range(m):
                d=rg.displacement_certificate(q,m,p,w,params,h)
                self.assertEqual(d['rank'],0)
                self.assertEqual(d['zero_defect_columns'],list(range(q)))
                self.assertEqual(d['kernel_rank'],q)

    def test_noncoprime_impossibility(self):
        for q,m in [(2,4),(8,8),(16,16),(6,10),(12,18)]:
            self.assertIsNone(rg.routing_pair(q,m))
            self.assertTrue(all((a*q+1)%m!=0 for a in range(m)))


if __name__=='__main__':unittest.main()
