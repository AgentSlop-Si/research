import random
import unittest
from math import gcd
from phase_union import (phase_table,witness_coefficients,recognize,
    transform_if_recognized,direct_dft,make_signal)

# Checked primitive roots of the indicated orders in these prime fields.
CASES=[(7,29,16),(17,103,72),(31,311,260), (63,127,9),
       (119,239,49),(127,509,16),(255,1021,811),(511,3067,64),
       (1023,4093,16)]

class TestHero17(unittest.TestCase):
    def test_root_orders(self):
        for n,p,omega in CASES:
            self.assertEqual(len(phase_table(n,p,omega)),n)

    def test_true_rank_one_chirp(self):
        rng=random.Random(1717)
        for n,p,omega in CASES:
            for _ in range(4):
                a=rng.choice([a for a in range(n) if gcd(a,n)==1])
                b=rng.randrange(n);c=rng.randrange(1,p)
                x=make_signal(n,p,omega,a,[(b,c)])
                out,cert=transform_if_recognized(x,p,omega)
                self.assertIsNotNone(cert,(n,p,a,b,c))
                self.assertEqual(cert.a,a,(n,a,cert))
                self.assertLessEqual(cert.candidate_count,4)
                if n <= 255:
                    self.assertEqual(out,direct_dft(x,p,omega),(n,a,b))
                else:
                    # Independent direct checks on selected frequency bins.
                    phase=phase_table(n,p,omega)
                    for k in [0,1,n//2,n-1, rng.randrange(n)]:
                        self.assertEqual(out[k],sum(x[j]*phase[(-j*k)%n] for j in range(n))%p)

    def test_true_rank_two_chirp(self):
        rng=random.Random(202617)
        for n,p,omega in CASES:
            for _ in range(5):
                a=rng.choice([0]+[a for a in range(n) if gcd(a,n)==1])
                b1,b2=rng.sample(range(n),2)
                c1=rng.randrange(1,p)
                c2=rng.choice([(-c1)%p,rng.randrange(1,p)])
                if c2==0:c2=1
                x=make_signal(n,p,omega,a,[(b1,c1),(b2,c2)])
                out,cert=transform_if_recognized(x,p,omega)
                self.assertIsNotNone(cert,(n,p,a,b1,b2,c1,c2))
                self.assertEqual(cert.a,a,(n,a,cert))
                self.assertEqual(len(cert.modes),2,(n,cert))
                self.assertLessEqual(cert.candidate_count,4)
                if n<=255:
                    self.assertEqual(out,direct_dft(x,p,omega),(n,a,b1,b2))
                else:
                    phase=phase_table(n,p,omega)
                    for k in [0,1,n//2,n-1,rng.randrange(n)]:
                        self.assertEqual(out[k],sum(x[j]*phase[(-j*k)%n] for j in range(n))%p)

    def test_zero_and_nonchired_rank_two(self):
        n,p,omega=119,239,49
        out,cert=transform_if_recognized([0]*n,p,omega)
        self.assertEqual(out,[0]*n)
        self.assertEqual(cert.modes,())
        x=make_signal(n,p,omega,0,[(13,3),(29,4)])
        out,cert=transform_if_recognized(x,p,omega)
        self.assertEqual(cert.a,0)
        self.assertEqual(out,direct_dft(x,p,omega))

    def test_random_dense_must_not_false_accept(self):
        rng=random.Random(171717)
        for n,p,omega in CASES[:7]:
            for _ in range(12):
                x=[rng.randrange(p) for _ in range(n)]
                cert=recognize(x,p,omega)
                self.assertIsNone(cert,(n,p,cert))

    def test_mutation_rejected(self):
        rng=random.Random(171)
        for n,p,omega in CASES[:7]:
            a=next(a for a in range(1,n) if gcd(a,n)==1)
            x=make_signal(n,p,omega,a,[(0,3),(1,4)])
            x[n//2]=(x[n//2]+1)%p
            self.assertIsNone(recognize(x,p,omega),(n,p))

    def test_empty_witness_handling(self):
        n,p,omega=119,239,49
        x=[0]*n
        x[0]=4
        self.assertIsNone(recognize(x,p,omega))

if __name__=='__main__':unittest.main()
