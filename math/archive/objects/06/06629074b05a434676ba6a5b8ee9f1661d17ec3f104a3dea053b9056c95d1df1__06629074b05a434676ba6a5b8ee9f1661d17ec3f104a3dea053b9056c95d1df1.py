"""Deterministic exact checks of Phase 7 theorem and its model."""
import random
import unittest
from math import isqrt
from phase7 import (
    divisors,optimal_divisor,optimal_tile_cost, row_subgroup_order,
    rectangle_envelope,rank_one_rectangle,subgroup_tiles,verify_partition,
    tile_cost,test_field,one_pass_tiled_dft,shared_two_axis_dft,direct_dft,
    enumerate_rankone_tiles,
)

class Phase7Tests(unittest.TestCase):
    def test_divisors_and_optimum(self):
        for n in range(2,160):
            ds=divisors(n)
            self.assertEqual(ds,[d for d in range(1,n+1) if n%d==0])
            self.assertEqual(optimal_tile_cost(n),n*min(d+n//d for d in ds))

    def test_subgroup_tilings(self):
        for n in (2,3,4,5,6,8,9,10,12,15,16,18,24,25,36,49,60):
            for d in divisors(n):
                tiles=subgroup_tiles(n,d)
                verify_partition(n,tiles)
                self.assertEqual(len(tiles),n)
                self.assertEqual(tile_cost(tiles),n*(d+n//d))
            self.assertEqual(tile_cost(subgroup_tiles(n)),optimal_tile_cost(n))

    def test_max_area_and_subgroup_envelope(self):
        rng=random.Random(176)
        for n in (4,6,8,9,12,15,16,25):
            for d in divisors(n):
                for rows,cols in rng.sample(subgroup_tiles(n,d),min(n,4)):
                    subrows=sorted(rng.sample(rows,rng.randint(1,len(rows))))
                    subcols=sorted(rng.sample(cols,rng.randint(1,len(cols))))
                    env=rectangle_envelope(subrows,subcols,n)
                    self.assertLessEqual(env['area'],n)
                    self.assertTrue(set(subrows).issubset(env['row_coset']))
                    self.assertTrue(set(subcols).issubset(env['col_coset']))
                    self.assertEqual(env['row_capacity']*env['col_capacity'],n)

    def test_all_small_rectangles_rank_criterion(self):
        for n in range(2,7):
            p,w=test_field(n)
            roots=[pow(w,(-j)%n,p) for j in range(n)]
            subs=[tuple(k for k in range(n) if mask>>k&1) for mask in range(1,1<<n)]
            for I in subs:
                for J in subs:
                    desired=all((roots[(k*j)%n]*roots[(k0*j0)%n]-
                                roots[(k*j0)%n]*roots[(k0*j)%n])%p==0
                                for k in I for j in J for k0 in I for j0 in J)
                    self.assertEqual(rank_one_rectangle(I,J,n),desired)

    def test_prime_cost(self):
        for n in (2,3,5,7,11,13,17,19):
            self.assertEqual(optimal_tile_cost(n),n*(n+1))

    def test_exact_finite_field_transform(self):
        rng=random.Random(617)
        for n in (2,3,4,5,6,8,9,10,12,15,16,18,24,25,32,36,49,64,81,128,256):
            p,w=test_field(n)
            for _ in range(3):
                x=[rng.randrange(p) for _ in range(n)]
                y,cost=one_pass_tiled_dft(x,p,w)
                self.assertEqual(y,direct_dft(x,p,w),(n,p,w))
                self.assertEqual(cost.muls,optimal_tile_cost(n))
                self.assertEqual(cost.adds,optimal_tile_cost(n)-n)
                self.assertEqual(cost.root_muls,n-1)
                self.assertEqual(cost.output_writes,n)

    def test_two_axis_shared_fft(self):
        rng=random.Random(1717)
        for n in (4,8,16,32,64,128,256,512,1024):
            p,w=test_field(n)
            x=[rng.randrange(p) for _ in range(n)]
            z,lc=shared_two_axis_dft(x,p,w)
            self.assertEqual(z,direct_dft(x,p,w))
            self.assertEqual(lc.butterflies,n*(n.bit_length()-1)//2)
            self.assertEqual(lc.muls,lc.butterflies+n)
            self.assertEqual(lc.adds,2*lc.butterflies)
            self.assertEqual(lc.root_muls,n-1)

    def test_rankone_tile_count_model(self):
        for n in (2,3,4,5,6):
            tiles=enumerate_rankone_tiles(n)
            self.assertTrue(tiles)
            self.assertTrue(all(c==len(I)+len(J) for I,J,c,_ in tiles))
            self.assertTrue(all(len(I)*len(J)<=n for I,J,_,_ in tiles))

if __name__=='__main__':unittest.main()

class Phase7ExtraCertificates(unittest.TestCase):
    def test_plaquette_holonomy_is_diagonal_gauge_invariant(self):
        rng=random.Random(17007)
        for n in (4,6,8,9,12,16,25):
            p,w=test_field(n)
            phase=[pow(w,(-a)%n,p) for a in range(n)]
            a=[rng.randrange(1,p) for _ in range(n)]
            b=[rng.randrange(1,p) for _ in range(n)]
            F=lambda k,j: phase[(k*j)%n]
            G=lambda k,j: a[k]*b[j]*F(k,j)%p
            for _ in range(200):
                k,kk,j,jj=(rng.randrange(n) for _ in range(4))
                # Cross-ratio factor cancels all row/column gauge scalars.
                cross=phase[((k-kk)*(j-jj))%n]
                lhs=G(k,j)*G(kk,jj)%p
                rhs=G(k,jj)*G(kk,j)%p
                self.assertEqual(lhs,rhs*cross%p)

    def test_complex_submatrix_stable_rank(self):
        import numpy as np
        rng=random.Random(1776)
        for n in (4,6,8,9,12,16,25):
            for _ in range(24):
                rows=rng.sample(range(n),rng.randint(1,n))
                cols=rng.sample(range(n),rng.randint(1,n))
                A=np.array([[np.exp(-2j*np.pi*k*t/n) for t in cols] for k in rows])
                r=np.linalg.matrix_rank(A,tol=1e-7)
                self.assertGreaterEqual(r+1e-8,len(rows)*len(cols)/n)
                self.assertLessEqual(np.linalg.norm(A,2),np.sqrt(n)+1e-7)

    def test_noncyclic_finite_abelian_example(self):
        # Group G=Z2 x Z4. Character values in F_17 with i=4.
        p=17; imaginary=4
        G=[(a,b) for a in range(2) for b in range(4)]
        def character(k,j):
            return pow(-1,k[0]*j[0])*pow(imaginary,k[1]*j[1],p)%p
        # H={0}xZ4, H^perp=Z2x{0}, each block size 4x2.
        row_cosets=[[v for v in G if v[0]==a] for a in range(2)]
        col_cosets=[[v for v in G if v[1]==b] for b in range(4)]
        # These column cosets have exactly 2 elements each.
        used=set(); cost=0
        for I in row_cosets:
            for J in col_cosets:
                cost+=len(I)+len(J)
                for k in I:
                    for j in J:
                        used.add((k,j))
                        for kk in I:
                            for jj in J:
                                self.assertEqual(
                                    (character(k,j)*character(kk,jj)-
                                     character(k,jj)*character(kk,j))%p,0)
        self.assertEqual(len(used),64)
        self.assertEqual(cost,8*(4+2))
