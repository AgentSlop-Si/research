"""Phase33 independent regression tests. Run python -m unittest -v tests_phase33."""
import unittest
from random import Random
from phase33_two_sided import (
  P1,P2,GEN1,GEN2,inverse,root_of_unity,CyclicGreen,make_cycles,
  is_affine_cycle,field_rank,determinant,first_three_column_certificate,
  setup_left_gauges,extra_column_extension,q_column_tangent,
  phase17_bound,solve,inverse_small,
)


def separated_groups(cycles):
    n=len(cycles[0]);assert n%2==0
    R=set(cycles[0][:n//2]);C=set(cycles[0][n//2:])
    for cyc in cycles[1:]:
        active=R|C
        S=[j for j in cyc if j in active]
        half=len(S)//2
        left=set(S[:half]);right=set(S[-half:])
        A=(R&left,C&right)
        B=(R&right,C&left)
        R,C=max((A,B),key=lambda t:len(t[0]))
    return sorted(R),sorted(C)


class Phase33Tests(unittest.TestCase):
    def test_independently_ordered_nonaffine(self):
        for n in (8,16,64,128):
            cycles=make_cycles(n,5)
            self.assertTrue(all(not is_affine_cycle(c) for c in cycles))
            maps=[]
            for c in cycles:
                nxt=[0]*n
                for k,j in enumerate(c):nxt[j]=c[(k+1)%n]
                for old in maps:
                    self.assertTrue(any(nxt[old[x]]!=old[nxt[x]] for x in range(n)))
                maps.append(nxt)

    def test_green_recurrence_independent_dense_matrix(self):
        rng=Random(3301)
        for p in (P1,P2):
            for n in (8,16):
                c=make_cycles(n,2)[0];g=CyclicGreen(c,3,p)
                B=[[int(i==j) for j in range(n)] for i in range(n)]
                for t,j in enumerate(c):
                    B[j][c[(t-1)%n]]=(B[j][c[(t-1)%n]]-3)%p
                x=[rng.randrange(p) for _ in range(n)]
                by_ref=solve(B,x,p)
                self.assertEqual(g.apply(x),by_ref)
                for j in (0,1,n-1):
                    self.assertEqual(g.apply([int(i==j) for i in range(n)]),
                                     [g.entry(i,j) for i in range(n)])

    def test_two_couplings_both_primes_char_zero_witness(self):
        for n in (8,16,32,64,128,256,512,1024):
            cycles=make_cycles(n,2)
            for p,primitive in ((P1,GEN1),(P2,GEN2)):
                r=first_three_column_certificate(n,cycles,p,primitive)
                self.assertEqual(r['rank'],6)
                self.assertEqual(len(r['pivots']),6)
                self.assertNotEqual(r['determinant_mod_p'],0)

    def test_rank_generic_in_alpha_at_sampled_orderings(self):
        for n in (8,16,32,64):
            cycles=make_cycles(n,2)
            for alphas in ((3,5),(7,11),(13,17)):
                r=first_three_column_certificate(n,cycles,P1,GEN1,alphas)
                self.assertEqual(r['rank'],6)

    def test_six_monomial_identity_independently(self):
        rng=Random(4407)
        for n in (8,16):
            g,h=[CyclicGreen(c,a) for c,a in zip(make_cycles(n,2),(3,5))]
            w=root_of_unity(n,P1,GEN1)
            for i in range(n):
                A,C,E=(g.entry(i,j) for j in (0,1,2))
                B,D,H=(h.entry(i,j) for j in (0,1,2))
                f1=pow(w,-i%n,P1);f2=pow(w,-2*i%n,P1)
                coeff=[C*H,-D*E,-B*C*f2,A*D*f2,B*E*f1,-A*H*f1]
                a,b,c,d=(rng.randrange(1,P1) for _ in range(4))
                # Independent Laplace expansion of a 3x3 determinant.
                mat=[[A,B,1],[a*C%P1,b*D%P1,f1],
                     [c*E%P1,d*H%P1,f2]]
                det=determinant(mat,P1)
                z=[a*d,b*c,a,b,c,d]
                self.assertEqual(det,sum(x*y for x,y in zip(coeff,z))%P1)

    def test_valid_two_term_control_not_falsely_excluded(self):
        rng=Random(905)
        for n in (8,16):
            w=root_of_unity(n,P1,GEN1)
            F=[[pow(w,-i*j%n,P1) for j in range(n)] for i in range(n)]
            # Plant a valid F=G1+G2 with all four two-sided gauges =identity.
            H=[[rng.randrange(1,P1) for _ in range(n)] for _ in range(n)]
            G1=[[(F[i][j]-H[i][j])%P1 for j in range(n)] for i in range(n)]
            G2=H
            K=[]
            for i in range(n):
                A,C,E=G1[i][:3];B,D,I=G2[i][:3]
                f1=F[i][1];f2=F[i][2]
                K.append([C*I,-D*E,-B*C*f2,A*D*f2,B*E*f1,-A*I*f1])
            self.assertLess(field_rank(K,P1),6)
            self.assertTrue(all(sum(row)%P1==0 for row in K))

    def test_gauge_dimension_and_jacobian_rank(self):
        for n in (32,64,128,256):
            r=q_column_tangent(n)
            self.assertEqual(r['parameter_dimension'],25)
            self.assertEqual(r['jacobian_rank'],25)
            self.assertEqual(r['rank_with_residual'],26)
            self.assertEqual(r['missing_column_mismatch'],n)

    def test_jacobian_chain_rule(self):
        n=32;q=5
        greens=[CyclicGreen(c,7+2*s) for s,c in enumerate(make_cycles(n,q,320031))]
        left=setup_left_gauges(greens,list(range(q)),P1,GEN1)
        for i in (0,1,3):
            B=[[g.entry(i,j) for g in greens] for j in range(q)]
            BI=inverse_small(B,P1)
            x=[left[s][i] for s in range(q)]
            h=[g.entry(i,q) for g in greens]
            ell,s=2,3
            # Differentiate Bx=f with respect to a single input-side gauge.
            u=B[ell][s]*x[s]%P1
            delta_x=[-BI[t][ell]*u%P1 for t in range(q)]
            direct=sum(h[t]*delta_x[t] for t in range(q))%P1
            projected=-sum(h[t]*BI[t][ell] for t in range(q))*B[ell][s]*x[s]%P1
            self.assertEqual(direct,projected)

    def test_new_input_gauge_extends_five_columns_on_five_rows(self):
        for n in (8,16,32,64,128,256,1024):
            r=extra_column_extension(n)
            self.assertEqual(r['extra_column_exact_rows'],5)
            self.assertEqual(r['extra_column_mismatched_rows'],n-5)
            self.assertTrue(all(r['right_gauge_extra_column']))

    def test_original_five_columns_still_match_after_extension(self):
        n=32;q=5
        greens=[CyclicGreen(c,7+2*s) for s,c in enumerate(make_cycles(n,q,320031))]
        left=setup_left_gauges(greens,list(range(q)),P1,GEN1)
        w=root_of_unity(n,P1,GEN1)
        for j in range(q):
            src=[int(i==j) for i in range(n)]
            out=[0]*n
            for s,g in enumerate(greens):
                y=g.apply(src)
                for i in range(n):out[i]=(out[i]+left[s][i]*y[i])%P1
            self.assertEqual(out,[pow(w,-i*j%n,P1) for i in range(n)])

    def test_common_order_separation_and_rank_one_crossblock(self):
        for n,q in ((64,2),(256,3),(2048,4),(8192,5)):
            cycles=make_cycles(n,q,330033)
            R,C=separated_groups(cycles)
            self.assertEqual(len(R),len(C))
            self.assertGreaterEqual(len(R),n//(1<<q))
            for c in cycles:
                pos={x:t for t,x in enumerate(c)}
                self.assertTrue(max(pos[r] for r in R)<min(pos[x] for x in C)
                                or max(pos[x] for x in C)<min(pos[r] for r in R))
            for k,cycle in enumerate(cycles):
                g=CyclicGreen(cycle,3+2*k)
                for a,b in ((0,1),(1,2),(3,4)):
                    ri,rj=R[a],R[b];ci,cj=C[a],C[b]
                    self.assertEqual((g.entry(ri,ci)*g.entry(rj,cj) -
                                      g.entry(ri,cj)*g.entry(rj,ci))%P1,0)

    def test_exact_asymptotic_and_spectral_bound(self):
        for q,n in ((2,64),(3,256),(4,2048),(5,8192),(6,32768)):
            r=phase17_bound(n,q)
            self.assertTrue(r['exact_Fourier_ruled_out'])
            self.assertGreater(r['fourier_rank_lower'],q)
            self.assertGreater(r['normalized_DFT_spectral_error_floor'],0)
        self.assertFalse(phase17_bound(4096,5)['exact_Fourier_ruled_out'])

    def test_matrices_with_any_outer_gauges_preserve_certificate_rank(self):
        n=64;cycles=make_cycles(n,2)
        r=first_three_column_certificate(n,cycles,P1,GEN1)
        self.assertEqual(r['rank'],6)
        # Since the certificate rules out all nonzero gauges, it also rules out
        # any scalar rescaling of the two given Green matrices (absorbed in L).
        self.assertNotEqual(r['determinant_mod_p'],0)

if __name__=='__main__': unittest.main()
