import unittest,random,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from cyclotomic_orbits import OrbitDFT,reference_dft_mod

class TestOrbit(unittest.TestCase):
    def test_zero_ones_dc(self):
        for n in (2,4,8,16,32,64):
            for x in ([0]*n,[1]*n,[int(i%2==0) for i in range(n)]):
                o=OrbitDFT.build(x)
                self.assertEqual(o.add_sub_count,2*(n-1))
                self.assertEqual(o.stored_coefficients,n)
                self.assertEqual(o.expanded_coefficients,(n*n+2)//3)
                self.assertEqual([o.evaluate_mod(k) for k in range(n)],reference_dft_mod(x))
                ref=reference_dft_mod(x)
                self.assertEqual(o.representative_bins_mod(),{k:ref[k] for k in (0,*[1<<j for j in range(n.bit_length()-1)])})

    def test_random_bit_inputs(self):
        rng=random.Random(20261009)
        for n in (2,4,8,16,32,64,128):
            for _ in range(10):
                x=[rng.randrange(2) for _ in range(n)]
                o=OrbitDFT.build(x)
                self.assertEqual([o.evaluate_mod(k) for k in range(n)],reference_dft_mod(x))

    def test_random_integer_inputs(self):
        rng=random.Random(3306)
        for n in (2,4,8,16,32,64):
            for _ in range(8):
                x=[rng.randrange(-1000,1000) for _ in range(n)]
                o=OrbitDFT.build(x)
                self.assertEqual([o.evaluate_mod(k) for k in range(n)],reference_dft_mod(x))

    def test_signed_perm(self):
        rng=random.Random(22)
        for n in (4,8,16,32,64):
            x=[rng.randrange(-999,999) for _ in range(n)]
            o=OrbitDFT.build(x)
            for k in range(1,n):
                d=o.descriptor(k)
                self.assertEqual(d.u%2,1)
                self.assertEqual(sorted(map(abs,o.coefficients(k))),
                                 sorted(map(abs,o.primitive_coefficients[d.orbit_index])))

    def test_closed_counts(self):
        for n in (2,4,8,16,32,64,128,256):
            o=OrbitDFT.build(list(range(n)))
            self.assertEqual(o.stored_coefficients,n)
            self.assertEqual(o.add_sub_count,2*n-2)
            self.assertEqual(o.expanded_coefficients,(n*n+2)//3)

    def test_index_validation(self):
        o=OrbitDFT.build([1,2,3,4])
        for k in (-1,4):
            with self.assertRaises(IndexError):o.descriptor(k)
        with self.assertRaises(ValueError):OrbitDFT.build([1,2,3])

if __name__=='__main__':unittest.main()

class TestOrbitExpansionReduction(unittest.TestCase):
    def test_every_orbit_is_smaller_exact_fft(self):
        rng=random.Random(482)
        p=998244353
        for n in (2,4,8,16,32,64,128):
            for _ in range(3):
                x=[rng.randrange(-99,100) for _ in range(n)]
                store=OrbitDFT.build(x)
                for level, rep in enumerate(store.primitive_coefficients):
                    m=n>>level
                    d=m//2
                    wm=pow(3,(p-1)//m,p)
                    modulated=[r*pow(wm,j,p)%p for j,r in enumerate(rep)]
                    want=reference_dft_mod(modulated,p)
                    got=[store.evaluate_mod((1<<level)*(2*t+1),p) for t in range(d)]
                    self.assertEqual(got,want)

class TestComplexFormalIdentity(unittest.TestCase):
    def test_arbitrary_complex_inputs_not_galois_claim(self):
        import cmath, math
        rng=random.Random(678)
        for n in (4,8,16,32):
            x=[complex(rng.uniform(-1,1),rng.uniform(-1,1)) for _ in range(n)]
            # The rational/integer build deliberately does NOT accept arbitrary
            # complex x, so check the universal FORMAL fold identity separately.
            a=x[:]
            levels=[]
            while len(a)>1:
                d=len(a)//2
                levels.append([a[j]-a[j+d] for j in range(d)])
                a=[a[j]+a[j+d] for j in range(d)]
            for k in range(n):
                if not k: got=a[0]
                else:
                    s=(k&-k).bit_length()-1
                    m=n>>s
                    u=k>>s
                    got=sum(c*cmath.exp(2j*math.pi*u*j/m)
                            for j,c in enumerate(levels[s]))
                truth=sum(val*cmath.exp(2j*math.pi*k*j/n) for j,val in enumerate(x))
                self.assertLess(abs(got-truth),1e-10)
