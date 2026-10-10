"""Independent tests: direct permutation and scalar-Gaussian references."""
import itertools
import json
import random
import unittest
from dataclasses import asdict
from pathlib import Path
from eliminant_extension import Ledger, Polynomials, degree_bound, phase_eliminant, evaluate, geometric_values, phase_eliminant_toeplitz

RESULTS = {'permutation_coefficient_comparisons':0,'scalar_determinant_comparisons':0,'structured_true_phase_checks':0,'geometric_scan_value_comparisons':0,'karatsuba_product_comparisons':0,'p_below_D_examples':[],'growing_rank_ledgers':[],'toeplitz_bareiss_comparisons':0,'toeplitz_ledgers':[]}


def leibniz(window,r,p):
    # Independently compute the original raw Hankel determinant term exponents.
    E = (r+1)*r*(r-1)//2
    out = [0]*(degree_bound(r)+1)
    for perm in itertools.permutations(range(r+1)):
        inversion_count = sum(perm[i]>perm[j] for i in range(r+1) for j in range(i+1,r+1))
        coeff = 1
        exponent = -E
        for i,j in enumerate(perm):
            coeff = coeff*window[i+j]%p
            exponent += (i+j)*(i+j-1)//2
        out[exponent] = (out[exponent]+(-1 if inversion_count%2 else 1)*coeff)%p
    while out and not out[-1]:out.pop()
    return out


def det_scalar(matrix,p):
    a = [row[:] for row in matrix]
    out = 1
    for i in range(len(a)):
        row = next((j for j in range(i,len(a)) if a[j][i]%p),None)
        if row is None:return 0
        if row != i:a[row],a[i]=a[i],a[row];out=-out
        pivot = a[i][i]%p
        out = out*pivot%p
        inverse = pow(pivot,-1,p)
        for j in range(i+1,len(a)):
            factor = a[j][i]*inverse%p
            for k in range(i,len(a)):
                a[j][k] = (a[j][k]-factor*a[i][k])%p
    return out%p


def primitive_root_of_order(N,p):
    # Deliberately exhaustive test-only root search; not a production setup claim.
    for w in range(1,p):
        if pow(w,N,p)==1 and all(pow(w,d,p)!=1 for d in range(1,N) if N%d==0):return w
    raise AssertionError('no root')


class ExtensionTests(unittest.TestCase):
    def test_01_all_small_prime_characteristics(self):
        rng = random.Random(208643)
        for p in (2,3,5,7,13,101):
            for r in range(1,6):
                for _ in range(7):
                    window = [rng.randrange(p) for _ in range(2*r+1)]
                    window[r] = rng.randrange(1,p)
                    self.assertEqual(phase_eliminant(window,r,p),leibniz(window,r,p))
                    RESULTS['permutation_coefficient_comparisons'] += 1

    def test_02_scalar_determinants(self):
        rng = random.Random(4010)
        for r,p in ((2,5),(4,13),(6,19),(8,29),(10,31)):
            for _ in range(4):
                window = [rng.randrange(p) for _ in range(2*r+1)]
                window[r] = rng.randrange(1,p)
                polynomial = phase_eliminant(window,r,p)
                E = (r+1)*r*(r-1)//2
                for t in range(p):
                    raw = [[window[i+j]*pow(t,(i+j)*(i+j-1)//2,p)%p for j in range(r+1)] for i in range(r+1)]
                    self.assertEqual(pow(t,E,p)*evaluate(polynomial,t,p)%p,det_scalar(raw,p))
                    RESULTS['scalar_determinant_comparisons'] += 1

    def test_03_structured_true_phases(self):
        rng = random.Random(6903)
        for N,p,r in ((9,19,3),(12,13,4),(15,31,5),(18,19,6),(24,73,8),(30,31,10)):
            w = primitive_root_of_order(N,p)
            if p < degree_bound(r):RESULTS['p_below_D_examples'].append({'N':N,'p':p,'r':r,'D':degree_bound(r)})
            for a in range(N):
                frequencies = rng.sample(range(N),rng.randint(1,r))
                amps = [rng.randrange(1,p) for _ in frequencies]
                x = [pow(w,a*j*j,p)*sum(c*pow(w,b*j,p) for b,c in zip(frequencies,amps))%p for j in range(N)]
                center = next(c for c in range(r,N-r) if x[c])
                polynomial = phase_eliminant(x[center-r:center+r+1],r,p)
                self.assertEqual(evaluate(polynomial,pow(w,-2*a,p),p),0)
                RESULTS['structured_true_phase_checks'] += 1

    def test_04_geometric_scan(self):
        rng = random.Random(7402)
        for N,p in ((1,2),(2,3),(3,7),(4,5),(6,7),(12,13),(15,31),(30,31),(48,97),(96,97),(256,257)):
            q = primitive_root_of_order(N,p)
            for length in (0,1,2,N//2+1,N,2*N+7,5*N+1):
                coefficients = [rng.randrange(p) for _ in range(length)]
                actual = geometric_values(coefficients,q,N,p)
                expected = [evaluate(coefficients,pow(q,a,p),p) for a in range(N)]
                self.assertEqual(actual,expected)
                RESULTS['geometric_scan_value_comparisons'] += N

    def test_05_karatsuba(self):
        rng = random.Random(62001)
        for p in (2,3,13,257):
            ring = Polynomials(p)
            for m,n in ((1,400),(25,27),(49,96),(65,65),(127,254),(400,12)):
                for _ in range(3):
                    a = [rng.randrange(p) for _ in range(m)]
                    b = [rng.randrange(p) for _ in range(n)]
                    self.assertEqual(ring.karatsuba(a,b),ring.mul(a,b))
                    RESULTS['karatsuba_product_comparisons'] += 1

    def test_06_sparse_center_witnesses(self):
        for p in (2,3,13):
            for r in range(1,13):
                window = [0]*(2*r+1)
                window[r] = 1
                self.assertEqual(phase_eliminant(window,r,p),[(-1)**(r*(r+1)//2)%p])
                window[r-1] = 1
                window[r+1] = 1
                polynomial = phase_eliminant(window,r,p)
                self.assertEqual(polynomial[0],(-1)**(r*(r+1)//2)%p)

    def test_07_growing_rank_ledgers(self):
        rng = random.Random(2287)
        for r in (1,2,4,6,8,10,12):
            p = 101
            window = [rng.randrange(p) for _ in range(2*r+1)]
            window[r] = rng.randrange(1,p)
            ledger = Ledger()
            polynomial = phase_eliminant(window,r,p,ledger)
            D = degree_bound(r)
            self.assertLessEqual(ledger.max_minor_degree,D)
            self.assertLessEqual(ledger.max_numerator_degree,2*D)
            self.assertLessEqual(ledger.field_inversions,max(0,r-1))
            self.assertEqual(ledger.exact_divisions,r*(r+1)*(2*r+1)//6)
            RESULTS['growing_rank_ledgers'].append({'r':r,'D':D,'output_degree':len(polynomial)-1,**asdict(ledger)})

    def test_08_toeplitz_recursion(self):
        rng = random.Random(384420)
        for p in (2,3,5,13,101):
            for r in range(1,9):
                for _ in range(3):
                    window = [rng.randrange(p) for _ in range(2*r+1)]
                    window[r] = rng.randrange(1,p)
                    self.assertEqual(phase_eliminant_toeplitz(window,r,p),phase_eliminant(window,r,p))
                    RESULTS['toeplitz_bareiss_comparisons'] += 1
        for r in (10,12,16):
            p = 101
            window = [rng.randrange(p) for _ in range(2*r+1)]
            window[r] = rng.randrange(1,p)
            ledger = Ledger()
            got = phase_eliminant_toeplitz(window,r,p,ledger)
            self.assertEqual(got,phase_eliminant(window,r,p))
            self.assertEqual(ledger.field_inversions,1)
            RESULTS['toeplitz_bareiss_comparisons'] += 1
            RESULTS['toeplitz_ledgers'].append({'r':r,'D':degree_bound(r),**asdict(ledger)})


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ExtensionTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    RESULTS['test_groups_run'] = result.testsRun
    RESULTS['success'] = result.wasSuccessful()
    Path(__file__).with_name('test_results.json').write_text(json.dumps(RESULTS,indent=2)+'\n')
    raise SystemExit(not result.wasSuccessful())
