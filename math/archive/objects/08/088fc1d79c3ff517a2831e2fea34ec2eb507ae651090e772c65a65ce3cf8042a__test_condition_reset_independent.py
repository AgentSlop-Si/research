#!/usr/bin/env python3
"""Independent exact condition-reset checks; NOT an implementation of #130.

Python 3 + SymPy + NumPy. No network, installation, or imported research code.
Run: python3 test_condition_reset_independent.py --output results.json
Exact assertions are separate from illustrative numerical SVD/roundoff results.
"""
import argparse
import json
import math
import sys
import unittest
from pathlib import Path

import numpy as np
import sympy as s

I = s.I
R = s.Rational
RESULTS = {}


def canonical(M):
    return M.applyfunc(s.expand)


def exact_equal(A, B):
    if A.shape != B.shape or any(s.expand(x) != 0 for x in A - B):
        raise AssertionError(f"Exact matrices differ: {A.shape}, {B.shape}")


def is_unitary(M):
    exact_equal(canonical(M.conjugate().T * M), s.eye(M.cols))


def shear_left(M, target, source, coefficient):
    """One actual scalar shear, not a simultaneous block operation."""
    if target == source:
        raise ValueError("A shear needs distinct coordinates")
    N = M.copy()
    for k in range(M.cols):
        N[target, k] = s.expand(M[target, k] + coefficient * M[source, k])
    return N


def shear_inverse_right(M, target, source, coefficient):
    N = M.copy()
    for k in range(M.rows):
        N[k, source] = s.expand(M[k, source] - coefficient * M[k, target])
    return N


def embed(M, coordinates, dimension):
    N = s.eye(dimension)
    for i, a in enumerate(coordinates):
        for j, b in enumerate(coordinates):
            N[a, b] = M[i, j]
    return N


def borrowed_add_word(U, source, target, scratch):
    """Dense O(B^2) ADD_U via four-shear commutators; arbitrary scratch.

    z += c*x; y += z; z -= c*x; y -= z gives y += c*x.
    This is an independent toy compiler, not the manuscript's replay compiler.
    """
    gates = []
    for j in range(U.rows):
        for i in range(U.cols):
            c = U[j, i]
            if c != 0:
                gates += [(scratch, source[i], c), (target[j], scratch, s.Integer(1)),
                          (scratch, source[i], -c), (target[j], scratch, s.Integer(-1))]
    return gates


def exchange_word(U):
    n = U.rows
    a, b, z = list(range(n)), list(range(n, 2*n)), 2*n
    return (borrowed_add_word(U, a, b, z) +
            borrowed_add_word(-U.conjugate().T, b, a, z) +
            borrowed_add_word(U, a, b, z))


def expected_exchange(U):
    n = U.rows
    zero = s.zeros(n)
    W = zero.row_join(-U.conjugate().T).col_join(U.row_join(zero))
    return s.diag(W, s.Integer(1))


def to_numpy(M):
    return np.array(M.evalf(17).tolist(), dtype=np.complex128)


def local_prefixes(U):
    d = 2*U.rows + 1
    P = s.eye(d)
    Pinv = s.eye(d)
    prefixes = [(P, Pinv)]
    for j, i, c in exchange_word(U):
        P = shear_left(P, j, i, c)
        Pinv = shear_inverse_right(Pinv, j, i, c)
        exact_equal(P * Pinv, s.eye(d))
        # Determinants are also implied by the elementary form of each gate.
        if s.expand(P.det()) != 1:
            raise AssertionError("Non-unimodular exact prefix")
        prefixes.append((P, Pinv))
    exact_equal(P, expected_exchange(U))
    return prefixes


def check_serial_fiber(Q, coordinates, U, prefixes, numeric=False):
    """Check every scalar prefix against embed(P_t) Q, with unitary Q."""
    is_unitary(Q)
    M = Q.copy()
    worst = 1.0
    for t, (j, i, c) in enumerate(exchange_word(U), 1):
        M = shear_left(M, coordinates[j], coordinates[i], c)
        P, _ = prefixes[t]
        exact_equal(M, canonical(embed(P, coordinates, Q.rows) * Q))
        if numeric:
            worst = max(worst, float(np.linalg.cond(to_numpy(M))))
    is_unitary(M)
    return M, worst


def permutation(p):
    M = s.zeros(len(p))
    for j, i in enumerate(p):
        M[j, i] = 1
    return M


class ExactResetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.H = s.Matrix([[1, 1], [1, -1]]) / s.sqrt(2)
        cls.Hprefix = local_prefixes(cls.H)
        cls.U4 = s.Matrix([[(-I)**(j*k) / 2 for k in range(4)] for j in range(4)])

    def test_01_scalar_anchor_counterexample(self):
        S = 8 * s.eye(2)
        whole = s.diag(S, s.eye(2))
        exact_equal(S.conjugate().T * S, 64 * s.eye(2))
        exact_equal(whole.conjugate().T * whole, s.diag(64, 64, 1, 1))
        # From these exact Gram spectra: kappa(S)=1, kappa(S direct-sum I)=8.
        tiny = s.diag(R(1, 8), 1)
        exact_equal(tiny.T * tiny, s.diag(R(1, 64), 1))
        RESULTS['scalar_anchor'] = {'local_condition': 1, 'global_condition': 8,
                                    'small_scale_global_condition': 8}

    def test_02_asynchronous_unimodular_blocks(self):
        P = s.diag(4, R(1, 2), R(1, 2))
        Q = s.diag(2, 2, R(1, 4))
        self.assertEqual(P.det(), 1)
        self.assertEqual(Q.det(), 1)
        # Exact diagonal singular values, no numerical SVD needed.
        self.assertEqual(4 / R(1, 2), 8)
        self.assertEqual(2 / R(1, 4), 8)
        self.assertEqual(4 / R(1, 4), 16)
        RESULTS['asynchronous_blocks'] = {'each_condition': 8, 'joint_condition': 16}

    def test_03_arbitrary_borrowed_scratch(self):
        c = 3 + 2*I
        word = borrowed_add_word(s.Matrix([[c]]), [0], [1], 2)
        M = s.eye(3)
        for j, i, a in word:
            M = shear_left(M, j, i, a)
            self.assertEqual(s.expand(M.det()), 1)
        exact_equal(M, s.Matrix([[1, 0, 0], [c, 1, 0], [0, 0, 1]]))
        # Full matrix equality covers arbitrary, nonzero and correlated scratch.
        RESULTS['borrowed_scratch_commutator'] = {'scalar_shears': len(word),
                                                'full_state_identity_verified': True}

    def test_04_exact_fourier_bank_exchange(self):
        is_unitary(self.U4)
        prefix = local_prefixes(self.U4)
        is_unitary(prefix[-1][0])
        actual = prefix[-1][0][:, :4]
        expected = s.zeros(9, 4)
        expected[4:8, :] = self.U4
        exact_equal(actual, expected)
        RESULTS['fourier4_exchange'] = {'scalar_shears': len(prefix)-1,
                                       'exact_all_prefix_determinants': 1,
                                       'scratch_restored_for_all_contents': True}

    def test_05_actual_dft4_serial_fft_schedule(self):
        # State = four coordinates in bank A, four in bank B, one scratch.
        # Bit reversal in A and B, first H fibers, twiddle -i, crossed H fibers.
        bitrev = permutation([0, 2, 1, 3])
        Q = s.diag(bitrev, bitrev, s.Integer(1))
        worst = 1.0
        fiber_count = 0
        for fiber in ([0, 1], [2, 3]):
            positions = fiber + [4+i for i in fiber] + [8]
            Q, k = check_serial_fiber(Q, positions, self.H, self.Hprefix, True)
            worst = max(worst, k)
            fiber_count += 1
        twiddle = s.eye(9)
        twiddle[7, 7] = -I
        Q = twiddle * Q
        is_unitary(Q)
        for fiber in ([0, 2], [1, 3]):
            positions = [4+i for i in fiber] + fiber + [8]
            Q, k = check_serial_fiber(Q, positions, self.H, self.Hprefix, True)
            worst = max(worst, k)
            fiber_count += 1
        desired = s.zeros(9, 4)
        desired[:4, :] = self.U4
        exact_equal(Q[:, :4], desired)
        exact_equal(Q[8:9, :], s.eye(9)[8:9, :])
        localmax = max(float(np.linalg.cond(to_numpy(P))) for P, _ in self.Hprefix)
        self.assertAlmostEqual(worst, localmax, delta=1e-10)
        RESULTS['actual_dft4'] = {'scalar_shears': fiber_count*48,
                                'serial_fibers': fiber_count, 'macro_levels': 2,
                                'exact_matrix_equal_to_normalized_dft4': True,
                                'all_exact_prefix_factorizations_verified': True,
                                'numeric_max_global_condition': worst,
                                'numeric_max_local_condition': localmax,
                                'numeric_final_condition': float(np.linalg.cond(to_numpy(Q)))}

    def test_06_repeated_unitary_macro_resets(self):
        Q = s.eye(9)
        worst = 1.0
        for level in range(10):
            source_offset, target_offset = (0, 4) if level % 2 == 0 else (4, 0)
            fibers = ([0, 1], [2, 3]) if level % 2 == 0 else ([0, 2], [1, 3])
            for fiber in fibers:
                coordinates = ([source_offset+i for i in fiber] +
                               [target_offset+i for i in fiber] + [8])
                Q, k = check_serial_fiber(Q, coordinates, self.H, self.Hprefix, True)
                worst = max(worst, k)
            # Explicit exact unit-modulus twiddle and permutation on full state.
            D = s.eye(9)
            D[target_offset+3, target_offset+3] = -I
            Q = D * Q
            p = list(range(9))
            p[0], p[1] = p[1], p[0]
            Q = permutation(p) * Q
            is_unitary(Q)
        localmax = max(float(np.linalg.cond(to_numpy(P))) for P, _ in self.Hprefix)
        self.assertAlmostEqual(worst, localmax, delta=1e-9)
        RESULTS['ten_macro_resets'] = {'scalar_shears': 960, 'macro_levels': 10,
                                      'exact_unitary_fiber_boundaries': 20,
                                      'numeric_max_global_condition': worst,
                                      'numeric_max_local_condition': localmax}

    def test_07_zero_clean_is_not_full_state_reset(self):
        T = s.diag(1, 2)
        x = s.symbols('x')
        for levels in (1, 2, 8):
            M = T**levels
            exact_equal(M * s.Matrix([x, 0]), s.Matrix([x, 0]))
            self.assertEqual(M[1, 1], 2**levels)
        RESULTS['zero_clean_counterexample'] = {'levels': 8, 'restricted_map_condition': 1,
                                               'full_state_condition': 256}

    def test_08_retained_garbage_prevents_reset(self):
        # Two inputs and one scratch, accumulating only the first input in scratch.
        G = s.Matrix([[1, 0, 0], [0, 1, 0], [1, 0, 1]])
        M = G**8
        F = M[:, :2]
        exact_equal(F.T * F, s.diag(65, 1))
        self.assertEqual(M[2, 0], 8)
        self.assertNotEqual(M.T * M, s.eye(3))
        RESULTS['retained_garbage'] = {'levels': 8, 'restricted_condition_exact': 'sqrt(65)',
                                     'full_state_condition_exact': '33 + 8*sqrt(17)'}

    def test_09_finished_unitarity_does_not_erase_roundoff(self):
        # In binary64, round-to-nearest-even loses the 1 in 2^53+1 exactly.
        x = np.float64(1)
        y = np.float64(1)
        a = np.float64(2**53)
        y = np.float64(y + a*x)
        y = np.float64(y - a*x)
        self.assertEqual(float(y), 0.0)
        exact = s.Matrix([[1, 0], [2**53, 1]])
        inverse = s.Matrix([[1, 0], [-2**53, 1]])
        exact_equal(inverse*exact, s.eye(2))
        RESULTS['roundoff_cancellation'] = {'arithmetic': 'binary64, nearest-even',
                                           'exact_macro': 'identity',
                                           'input': [1, 1], 'computed_output': [1, 0],
                                           'absolute_error_l2': 1}

    def test_10_unitary_roundoff_accumulates(self):
        # The exact rational rotation is unitary at EVERY macro boundary.
        # This numerical section illustrates, rather than proves, drift rates.
        U = s.Matrix([[R(3, 5), -R(4, 5)], [R(4, 5), R(3, 5)]])
        is_unitary(U)
        c, d = np.float32(3/5), np.float32(4/5)
        x, y = np.float32(1), np.float32(0)
        rows = []
        for k in range(1, 10001):
            x, y = (np.float32(np.float32(c*x)-np.float32(d*y)),
                    np.float32(np.float32(d*x)+np.float32(c*y)))
            if k in (1, 10, 100, 1000, 10000):
                rows.append({'macro_steps': k, 'computed_norm': math.hypot(float(x), float(y)),
                             'exact_norm': 1.0})
        self.assertTrue(all(math.isfinite(r['computed_norm']) for r in rows))
        RESULTS['unitary_roundoff_drift'] = rows

    def test_11_exact_computable_condition_certificates(self):
        records = []
        for label, U, maximum in [('H2', self.H, R(171, 2)),
                                   ('U4', self.U4, R(1769, 8))]:
            products = []
            for P, Pinv in local_prefixes(U):
                norm_p_sq = s.expand(sum(a*s.conjugate(a) for a in P))
                norm_inverse_sq = s.expand(sum(a*s.conjugate(a) for a in Pinv))
                product = s.expand(norm_p_sq*norm_inverse_sq)
                self.assertTrue(product.is_Rational)
                self.assertLessEqual(product, maximum)
                products.append(product)
            self.assertEqual(max(products), maximum)
            # ||P||_2 ||P^-1||_2 <= ||P||_F ||P^-1||_F.
            # Determinant anchoring then transfers this local bound to serial
            # global prefixes, without adding a global-dimension factor.
            records.append({'local_transform': label,
                            'exact_condition_squared_upper_bound': str(maximum),
                            'display_condition_upper_bound': float(s.sqrt(maximum))})
        RESULTS['exact_condition_certificates'] = records

    def test_12_all_length_bluestein_numerical_identities(self):
        # Bounded numerical sanity checks only. No spectral-norm SVD sweep.
        # Fourier convention: exp(+2*pi*i*j*k/N); normalized output 1/sqrt(N).
        rng = np.random.default_rng(20261009)
        rows = []
        for n in (1, 2, 3, 5, 6, 7, 9, 10, 15, 17):
            m = 1 << ((2*n-2).bit_length())
            j = np.arange(n)
            positive_chirp = np.exp(1j*np.pi*j*j/n)
            b = np.zeros(m, dtype=np.complex128)
            b[0] = 1
            for k in range(1, n):
                b[k] = np.exp(-1j*np.pi*k*k/n)
                b[m-k] = b[k]
            self.assertEqual(int(np.count_nonzero(b)), 2*n-1)
            # The signed support is -(n-1),...,(n-1); neither endpoint +/-n
            # is inserted. For m=2n this is exactly one missing periodic term.
            if m == 2*n:
                self.assertEqual(b[n], 0)
            D = m*np.fft.ifft(b)/math.sqrt(n)
            bound = 9+4*math.log(2*n)
            self.assertLessEqual(float(np.max(np.abs(D))), bound)

            # Full small matrix identity: Y V* D V X = normalized F_n.
            X = np.zeros((m, n), dtype=np.complex128)
            X[:n] = np.diag(positive_chirp)
            actual = np.fft.fft(D[:, None]*np.fft.ifft(X, axis=0, norm='ortho'),
                                 axis=0, norm='ortho')[:n]
            actual = positive_chirp[:, None]*actual
            reference = np.exp(2j*np.pi*j[:, None]*j[None, :]/n)/math.sqrt(n)
            matrix_error = float(np.max(np.abs(actual-reference)))
            self.assertLess(matrix_error, 2e-12)

            # Dirty buffers are arbitrary AND correlated with the source.
            x = rng.normal(size=n)+1j*rng.normal(size=n)
            y0 = rng.normal(size=n)+1j*rng.normal(size=n)
            z0 = rng.normal(size=m)+1j*rng.normal(size=m)
            z0[:n] += x
            w0 = rng.normal(size=m)+1j*rng.normal(size=m)+0.3*z0
            y, z, w = y0.copy(), z0.copy(), w0.copy()

            def pass_once(with_source, sign):
                nonlocal y, z, w
                if with_source:
                    z[:n] += positive_chirp*x
                z = np.fft.ifft(z, norm='ortho')
                w += D*z
                w = np.fft.fft(w, norm='ortho')
                y += sign*positive_chirp*w[:n]
                w = np.fft.ifft(w, norm='ortho')
                w -= D*z
                z = np.fft.fft(z, norm='ortho')
                if with_source:
                    z[:n] -= positive_chirp*x

            pass_once(True, 1)
            first_restore = max(np.max(np.abs(z-z0)), np.max(np.abs(w-w0)))
            pass_once(False, -1)
            dirty_error = float(np.max(np.abs(y-y0-reference@x)))
            scratch_error = float(max(np.max(np.abs(z-z0)), np.max(np.abs(w-w0))))
            self.assertLess(float(first_restore), 2e-12)
            self.assertLess(dirty_error, 3e-12)
            self.assertLess(scratch_error, 3e-12)

            qj = np.arange(2*n)
            gauss_spectrum = (2*n)*np.fft.ifft(np.exp(-1j*np.pi*qj*qj/n))
            magnitudes = np.abs(gauss_spectrum)
            gauss_error = float(np.max(np.minimum(magnitudes, np.abs(magnitudes-2*math.sqrt(n)))))
            self.assertLess(gauss_error, 2e-11)
            self.assertEqual(int(np.count_nonzero(magnitudes > math.sqrt(n))), n)
            gj = np.arange(4*n)
            G4n = np.sum(np.exp(2j*np.pi*gj*gj/(4*n)))
            sqrt_from_gauss = G4n/(2*(1+1j))
            normalization_error = float(abs(sqrt_from_gauss-math.sqrt(n)))
            self.assertLess(normalization_error, 2e-11)
            rows.append({'Fourier_sign': '+', 'N': n, 'M': m, 'max_abs_diagonal_D': float(np.max(np.abs(D))),
                         'proposed_diagonal_bound': bound,
                         'matrix_identity_max_abs_error': matrix_error,
                         'dirty_add_max_abs_error': dirty_error,
                         'scratch_restore_max_abs_error': scratch_error,
                         'complete_gauss_magnitude_error': gauss_error,
                         'gauss_sqrt_normalization_error': normalization_error})
        RESULTS['bluestein_numerical_only'] = rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='Optional JSON results path')
    args = parser.parse_args()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ExactResetTests)
    outcome = unittest.TextTestRunner(verbosity=2).run(suite)
    payload = {'status': 'PASS' if outcome.wasSuccessful() else 'FAIL',
               'tests_run': outcome.testsRun, 'sympy_version': s.__version__,
               'numpy_version': np.__version__,
               'claim_boundary': 'Independent toy validation. No #130 implementation, speedup, '
                                 'Ailon model equivalence, or numerical stability claim.',
               'results': RESULTS}
    if args.output:
        args.output.write_text(json.dumps(payload, indent=2) + '\n')
    print(json.dumps(payload, indent=2))
    return 0 if outcome.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(main())
