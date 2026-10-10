import unittest
from random import Random
from itertools import combinations
from cut_budget import fourier,rank,permute
from prime_endpoints import field

class TestPrimeEndpointCorollary(unittest.TestCase):
    def test_exhaustive_small_minor(self):
        for n in (5,7):
            p,g=field(n,1);f=fourier(n,p,g)
            m=n//2
            subsets=list(combinations(range(n),m))
            for rows in subsets:
                for cols in subsets:
                    self.assertEqual(rank([[f[i][j] for j in cols] for i in rows],p),m)
    def test_independent_endpoint_permutations(self):
        rng=Random(321)
        for n in (5,7,11,13,17,31):
            p,g=field(n,1);f=fourier(n,p,g);m=n//2
            for _ in range(5):
                ro=list(range(n));co=list(range(n))
                rng.shuffle(ro);rng.shuffle(co)
                w=permute(f,ro,co)
                self.assertEqual(rank([row[:m] for row in w[:m]],p),m)
                self.assertEqual(rank([row[m:] for row in w[:m]],p),m)
if __name__=='__main__':unittest.main()
