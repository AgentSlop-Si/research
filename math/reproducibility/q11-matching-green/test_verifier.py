"""New regression and executable mutation controls for the public-safe derivative."""
import copy
import unittest

import verifier as v

if not __debug__:
    raise RuntimeError('Run tests without -O or PYTHONOPTIMIZE.')


class MatchingGreenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.q = 3
        cls.data = v.setup(cls.q)
        (cls.n, cls.s, cls.h, cls.p, cls.w, cls.P, cls.G, cls.c,
         cls.rho, cls.target, cls.u, cls.right, cls.D, cls.prep) = cls.data

    def branch(self, t=0, mode=0, direction=1):
        return v.branch(self.n, self.s, self.q, t, mode, direction,
                        self.data[10], self.data[11])

    def matrix(self, branch):
        out = [[0] * self.n for _ in range(self.n)]
        v.add_inverse_to_matrix(out, *branch, self.p)
        return out

    def test_small_full_matrix_and_defining_inverse(self):
        result = v.full_control(3)
        self.assertEqual(result['full_matrix_entries'], 2025)
        self.assertEqual(result['full_two_sided_inverse_entries'], 4050)
        self.assertEqual(result['optimized_vectors'], 49)

    def test_preparation_and_paid_application_counts(self):
        self.assertEqual(self.prep, {'multiplications': 179, 'additions': 90})
        x = [(i * 7 + 3) % self.p for i in range(self.n)]
        y, mul, add = v.optimized(self.q, self.data, x)
        self.assertEqual((mul, add), (2925, 2400))
        reference = [sum(self.data[9](i,j)*x[j] for j in range(self.n)) % self.p
                     for i in range(self.n)]
        self.assertEqual(y, reference)

    def test_every_round_partitions_original_coordinates(self):
        seen = set()
        for t in range(self.s):
            paths = v.round_paths(self.s, self.q, t)
            self.assertEqual(sorted(i for path, _, _ in paths for i in path),
                             list(range(self.n)))
            for _, a, b in paths[:-1]:
                pair = tuple(sorted((a,b)))
                self.assertNotIn(pair, seen)
                seen.add(pair)
            for direction in (1,-1):
                sig, weights, _, _ = self.branch(t=t,direction=direction)
                self.assertEqual(v.validate_branch(sig,weights,self.p),0)
        self.assertEqual(len(seen), self.s*(self.s-1)//2)

    def test_paid_diagonal_is_a_legal_green_branch(self):
        branch = (list(range(1,self.n))+[0], [0]*self.n,
                  self.D, [1]*self.n)
        got = self.matrix(branch)
        expected = [[self.D[i] if i == j else 0 for j in range(self.n)]
                    for i in range(self.n)]
        self.assertEqual(got,expected)

    def test_omitted_calibration_is_detected(self):
        mutated = list(self.data)
        mutated[12] = [0] * self.n
        x = [1] * self.n
        correct = v.optimized(self.q,self.data,x)[0]
        wrong = v.optimized(self.q,tuple(mutated),x)[0]
        self.assertNotEqual(correct,wrong)
        self.assertEqual([(a-b)%self.p for a,b in zip(correct,wrong)],self.D)

    def test_live_endpoint_mutation_is_detected(self):
        branch = self.branch()
        altered = copy.deepcopy(branch)
        i = next(i for i,z in enumerate(altered[2]) if z)
        altered[2][i] = (altered[2][i] + 1) % self.p
        self.assertNotEqual(self.matrix(branch),self.matrix(altered))

    def test_removed_zero_boundary_creates_forbidden_crossblock(self):
        branch = self.branch()
        paths = v.round_paths(self.s,self.q,0)
        i = paths[0][0][0]
        j = paths[1][0][self.q]
        altered = copy.deepcopy(branch)
        altered[1][paths[0][0][-1]] = 1
        before = self.matrix(branch)
        after = self.matrix(altered)
        self.assertEqual(before[i][j],0)
        self.assertNotEqual(after[i][j],0)
        self.assertNotEqual(before,after)

    def test_wrong_reverse_boundaries_are_detected(self):
        branch = self.branch(direction=-1)
        altered = copy.deepcopy(branch)
        altered[1][:] = [1]*self.n
        for path, _, _ in v.round_paths(self.s,self.q,0):
            altered[1][path[-1]] = 0
        self.assertNotEqual(self.matrix(branch),self.matrix(altered))

    def test_imprimitive_root_is_rejected(self):
        with self.assertRaises(ValueError):
            v.validate_root(self.n,self.p,1)
        with self.assertRaises(ValueError):
            v.validate_root(self.n,self.p,pow(self.w,3,self.p))

    def test_composite_modulus_is_rejected(self):
        with self.assertRaises(ValueError):
            v.validate_root(5,341,1)

    def test_unit_holonomy_is_rejected(self):
        with self.assertRaises(ValueError):
            v.validate_branch([1,2,0],[1,1,1],self.p)

    def test_nonhamiltonian_permutation_is_rejected(self):
        with self.assertRaises(ValueError):
            v.validate_branch([1,0,3,2],[0,0,0,0],self.p)

    def test_invalid_control_sizes_are_rejected(self):
        for q in (0,-1,2,5,10):
            with self.assertRaises(ValueError):
                v.setup(q)


if __name__ == '__main__':
    unittest.main(verbosity=2)
