import itertools
import random
import unittest
from phase9 import (fixture,ExchangeBridge,AdaptiveExchangeBridge,Ledger,gen_roots,
                    rank,correction_rank_certificate,single_swap_closed_form,
                    direct_remainder,full_dft_via_explicit_children,classical_dif_fft,
                    horner)


class ExchangeTests(unittest.TestCase):
    def test_no_swap_gives_exact_butterfly_and_inverse(self):
        for n in (2,4,8,16,32,64):
            p,w=fixture(n);m=n//2
            bridge=ExchangeBridge(n,p,w,[],[])
            rng=random.Random(n)
            for i in range(4):
                x=[rng.randrange(p) for _ in range(n)]
                a,b=bridge.pair(x[:m],x[m:])
                self.assertEqual(a,[(x[j]+x[j+m])%p for j in range(m)])
                self.assertEqual(b,[(x[j]-x[j+m])%p for j in range(m)])
                self.assertEqual(sum(bridge.invert_pair(a,b),[]),x)

    def test_single_swap_closed_formula(self):
        for n in (4,8,16,32):
            p,w=fixture(n);m=n//2
            for e in range(0,n,2):
                for o in range(1,n,2):
                    rng=random.Random((n*131+e)*131+o)
                    x=[rng.randrange(p) for _ in range(n)]
                    bridge=ExchangeBridge(n,p,w,[e],[o])
                    self.assertEqual(bridge.pair(x[:m],x[m:]),
                                     single_swap_closed_form(n,p,w,e,o,x[:m],x[m:]))

    def test_exact_random_remainders(self):
        rng=random.Random(171709)
        for n in (4,8,16,32,64,128):
            p,w=fixture(n);m=n//2;roots=gen_roots(n,p,w,Ledger())
            for t in sorted({0,1,min(2,m),m//2,m}):
                e=rng.sample(list(range(0,n,2)),t)
                o=rng.sample(list(range(1,n,2)),t)
                bridge=ExchangeBridge(n,p,w,e,o)
                for _ in range(3):
                    x=[rng.randrange(p) for _ in range(n)]
                    a,b=bridge.pair(x[:m],x[m:])
                    self.assertEqual(a,direct_remainder(x,[roots[j] for j in bridge.A],p))
                    self.assertEqual(b,direct_remainder(x,[roots[j] for j in bridge.B],p))
                    self.assertEqual(sum(bridge.invert_pair(a,b),[]),x)

    def test_independent_eval_identity(self):
        rng=random.Random(902)
        for n in (8,16,32,64):
            p,w=fixture(n);m=n//2;roots=gen_roots(n,p,w,Ledger())
            for t in sorted({0,1,2,m//2}):
                bridge=ExchangeBridge(n,p,w,
                     rng.sample(list(range(0,n,2)),t),rng.sample(list(range(1,n,2)),t))
                x=[rng.randrange(p) for _ in range(n)]
                a,b=bridge.pair(x[:m],x[m:])
                for labels,poly in ((bridge.A,a),(bridge.B,b)):
                    for j in labels:
                        self.assertEqual(horner(poly,roots[j],p,Ledger()),horner(x,roots[j],p,Ledger()))

    def test_inverse_from_arbitrary_pair(self):
        rng=random.Random(101901)
        for n in (4,8,16,32,64):
            p,w=fixture(n);m=n//2
            for t in range(m+1):
                bridge=ExchangeBridge(n,p,w,
                    rng.sample(list(range(0,n,2)),t),rng.sample(list(range(1,n,2)),t))
                a=[rng.randrange(p) for _ in range(m)]
                b=[rng.randrange(p) for _ in range(m)]
                lo,hi=bridge.invert_pair(a,b)
                self.assertEqual(bridge.pair(lo,hi),(a,b))

    def test_cauchy_cross_nodes(self):
        rng=random.Random(201720)
        for n in (8,16,32,64):
            p,w=fixture(n);m=n//2
            for t in range(1,min(m,5)+1):
                bridge=ExchangeBridge(n,p,w,
                    rng.sample(list(range(0,n,2)),t),rng.sample(list(range(1,n,2)),t))
                for i in range(t):
                    for j in range(t):
                        self.assertEqual(bridge.C[i][j],horner(bridge.LB[j],bridge.o[i],p,Ledger()))
                        self.assertEqual(bridge.D[j][i],horner(bridge.LA[i],bridge.e[j],p,Ledger()))
                self.assertEqual(rank(bridge.C,p),t)
                self.assertEqual(rank(bridge.D,p),t)

    def test_exact_rank_defects(self):
        rng=random.Random(1707)
        for n in (4,8,16,32):
            p,w=fixture(n);m=n//2
            for t in range(m+1):
                bridge=ExchangeBridge(n,p,w,
                    rng.sample(list(range(0,n,2)),t),rng.sample(list(range(1,n,2)),t))
                cert=correction_rank_certificate(bridge)
                self.assertEqual((cert['rank_delta_A'],cert['rank_delta_B'],cert['joint_rank']),
                                 (t,t,min(m,2*t)))

    def test_adaptive_orientation(self):
        rng=random.Random(303)
        for n in (4,8,16,32,64):
            p,w=fixture(n);m=n//2;roots=gen_roots(n,p,w,Ledger())
            for _ in range(20):
                A=rng.sample(list(range(n)),m)
                bridge=AdaptiveExchangeBridge(n,p,w,A)
                t=len(set(A)&set(range(1,n,2)))
                self.assertEqual(bridge.effective_swaps,min(t,m-t))
                x=[rng.randrange(p) for _ in range(n)]
                a,b=bridge.pair(x[:m],x[m:])
                self.assertEqual(a,direct_remainder(x,[roots[j] for j in bridge.A],p))
                self.assertEqual(b,direct_remainder(x,[roots[j] for j in bridge.B],p))
                self.assertEqual(sum(bridge.invert_pair(a,b),[]),x)

    def test_full_dft_matches_classical(self):
        rng=random.Random(1001)
        for n in (4,8,16,32,64,128):
            p,w=fixture(n)
            for _ in range(3):
                bridge=AdaptiveExchangeBridge(n,p,w,rng.sample(list(range(n)),n//2))
                x=[rng.randrange(p) for _ in range(n)]
                got=full_dft_via_explicit_children(x,bridge.bridge)
                # .bridge's group may be swapped; evaluate directly against FFT,
                # since either group ordering still generates all N outputs.
                ref,_=classical_dif_fft(x,p,w)
                self.assertEqual(got,ref)

    def test_charge_monotonicity(self):
        for n in (8,32,128,512):
            p,w=fixture(n);m=n//2
            for t in (0,1,2):
                bridge=ExchangeBridge(n,p,w,list(range(0,2*t,2)),list(range(1,2*t+1,2)))
                rng=random.Random(n+t)
                x=[rng.randrange(p) for _ in range(n)]
                bridge.pair(x[:m],x[m:])
                L=bridge.online_ledger()
                scalar=L['online_adds']+L['online_muls']
                self.assertLessEqual(scalar, 5*n*(t+1))
                self.assertEqual(L['writes'],n)
                self.assertEqual(L['online_invs'],0)
                plan=bridge.plan_ledger
                self.assertLessEqual(plan['plan_adds']+plan['plan_muls'],40*n*(t+1)**3)

    def test_hybrid_nonperiodic_full_fft(self):
        from phase9 import full_dft_via_hybrid_children,combined_scalar_cost
        rng=random.Random(993)
        for n in (4,8,16,32,64,128):
            p,w=fixture(n);m=n//2
            for t in sorted({0,1,2,m//2}):
                bridge=ExchangeBridge(n,p,w,
                    rng.sample(list(range(0,n,2)),t),
                    rng.sample(list(range(1,n,2)),t))
                x=[rng.randrange(p) for _ in range(n)]
                got,cost=full_dft_via_hybrid_children(x,bridge)
                ref,ref_cost=classical_dif_fft(x,p,w)
                self.assertEqual(got,ref)
                self.assertGreater(combined_scalar_cost(cost),0)
                self.assertGreaterEqual(cost['outer_online']['writes'],2*n)

    def test_one_swap_beats_dense_transfer_but_not_full_fft(self):
        from phase9 import full_dft_via_hybrid_children,combined_scalar_cost
        n=128;p,w=fixture(n);m=n//2
        bridge=ExchangeBridge(n,p,w,[0],[1])
        rng=random.Random(1002)
        x=[rng.randrange(p) for _ in range(n)]
        left,right=bridge.pair(x[:m],x[m:])
        split_cost=bridge.L.online_adds+bridge.L.online_muls
        self.assertLess(split_cost,4*m*m)  # dense two-matrix multiply is quadratic
        got,cost=full_dft_via_hybrid_children(x,bridge)
        ref,ref_cost=classical_dif_fft(x,p,w)
        self.assertEqual(got,ref)
        self.assertGreater(combined_scalar_cost(cost),
                           ref_cost.online_adds+ref_cost.online_muls+
                           ref_cost.plan_adds+ref_cost.plan_muls)

    def test_involution_and_commutator_rank_invariant(self):
        rng=random.Random(765433)
        for n in (4,8,16,32):
            p,w=fixture(n);m=n//2
            eye=[[int(i==j) for j in range(m)] for i in range(m)]
            def mul(A,B):
                return [[sum(A[i][k]*B[k][j] for k in range(m))%p for j in range(m)] for i in range(m)]
            for t in range(m+1):
                b=ExchangeBridge(n,p,w,
                    rng.sample(list(range(0,n,2)),t),
                    rng.sample(list(range(1,n,2)),t))
                RA=[[0]*m for _ in range(m)]
                RB=[[0]*m for _ in range(m)]
                for j in range(m):
                    h=[0]*m;h[j]=1
                    a,c=b.pair([0]*m,h)
                    for i in range(m):RA[i][j]=a[i];RB[i][j]=c[i]
                self.assertEqual(mul(RA,RA),eye)
                self.assertEqual(mul(RB,RB),eye)
                self.assertEqual(rank([[(RA[i][j]-RB[i][j])%p for j in range(m)]
                                       for i in range(m)],p),m)
                AB=mul(RA,RB);BA=mul(RB,RA)
                target=2*min(t,m-t)
                self.assertEqual(rank([[(RA[i][j]+RB[i][j])%p for j in range(m)]
                                       for i in range(m)],p),target)
                self.assertEqual(rank([[(AB[i][j]-BA[i][j])%p for j in range(m)]
                                       for i in range(m)],p),target)
                self.assertEqual(rank([[(AB[i][j]+eye[i][j])%p for j in range(m)]
                                       for i in range(m)],p),target)

    def test_swap_histogram_combinatorics(self):
        # Exact balanced partitions by t parity swaps are binom(m,t)^2.
        import math
        for m in (2,4,8):
            seen=[0]*(m+1)
            for group in itertools.combinations(range(2*m),m):
                t=sum(k%2 for k in group)
                seen[t]+=1
            self.assertEqual(seen,[math.comb(m,t)**2 for t in range(m+1)])

    def test_all_16_single_swap_nontrivial_dense(self):
        # R_A-I has rank1 but may have many nonzero matrix entries.
        from phase9 import rank
        n=16;p,w=fixture(n);m=n//2
        bridge=ExchangeBridge(n,p,w,[0],[1])
        da=[[0]*m for _ in range(m)]
        for col in range(m):
            high=[0]*m;high[col]=1
            a,b=bridge.pair([0]*m,high)
            for row in range(m):da[row][col]=(a[row]-high[row])%p
        self.assertEqual(rank(da,p),1)
        self.assertGreater(sum(bool(v) for row in da for v in row),m*m//2)
        # Although the correction is rank one, its actual transfer is dense.
        ra=[[(da[i][j]+int(i==j))%p for j in range(m)] for i in range(m)]
        self.assertEqual(sum(bool(v) for row in ra for v in row),m*m)

if __name__=='__main__':unittest.main()
