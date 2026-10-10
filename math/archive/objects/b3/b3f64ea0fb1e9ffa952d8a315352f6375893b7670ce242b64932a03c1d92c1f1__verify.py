"""Independent, deterministic exact tests for the fixed-graph/marked-cycle note.

Run: python verify.py --output RESULTS.json
No external packages, network access, or historical research code is used.
Dense/dual-number computations below are verification oracles, NOT fast kernels.
"""
from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path
from typing import Callable, Sequence

from fixed_graph import Counts, Field, FixedGraph

Matrix = list[list[int]]
FIELDS = (Field(65537, 3), Field(998244353, 3))


def eye(n: int) -> Matrix:
    return [[int(i == j) for j in range(n)] for i in range(n)]


def mm(a: Matrix, b: Matrix, p: int) -> Matrix:
    columns = list(zip(*b))
    return [[sum(u * v for u, v in zip(row, col)) % p for col in columns] for row in a]


def mv(a: Matrix, x: Sequence[int], p: int) -> list[int]:
    return [sum(u * v for u, v in zip(row, x)) % p for row in a]


def add(a: Matrix, b: Matrix, p: int) -> Matrix:
    return [[(u + v) % p for u, v in zip(row, other)] for row, other in zip(a, b)]


def scale(a: Matrix, c: int, p: int) -> Matrix:
    return [[c * v % p for v in row] for row in a]


def inverse(a: Matrix, p: int) -> Matrix:
    n = len(a)
    aug = [row[:] + ident for row, ident in zip(a, eye(n))]
    for j in range(n):
        pivot = next((r for r in range(j, n) if aug[r][j] % p), None)
        if pivot is None:
            raise ValueError("Singular test matrix")
        aug[j], aug[pivot] = aug[pivot], aug[j]
        inv = pow(aug[j][j], -1, p)
        aug[j] = [v * inv % p for v in aug[j]]
        for r in range(n):
            if r == j:
                continue
            alpha = aug[r][j]
            if alpha:
                aug[r] = [(u - alpha * v) % p for u, v in zip(aug[r], aug[j])]
    return [row[n:] for row in aug]


def determinant(a: Matrix, p: int) -> int:
    a = [row[:] for row in a]
    result = 1
    for j in range(len(a)):
        pivot = next((r for r in range(j, len(a)) if a[r][j] % p), None)
        if pivot is None:
            return 0
        if pivot != j:
            a[j], a[pivot] = a[pivot], a[j]
            result = -result % p
        v = a[j][j]
        result = result * v % p
        inv = pow(v, -1, p)
        for r in range(j + 1, len(a)):
            q = a[r][j] * inv % p
            for c in range(j + 1, len(a)):
                a[r][c] = (a[r][c] - q * a[j][c]) % p
    return result


def q_matrix(N: int, w: int, p: int) -> Matrix:
    # Construct from graph edges, independently of the butterfly apply() method.
    a = [[0] * N for _ in range(N)]
    for s in range(N):
        a[2 * s % N][s] = 1
        a[(2 * s + 1) % N][s] = pow(w, s, p)
    return a


def direct_dft(x: Sequence[int], w: int, p: int) -> list[int]:
    return [sum(value * pow(w, k * j, p) for j, value in enumerate(x)) % p
            for k in range(len(x))]


def radix2_dft(x: Sequence[int], w: int, p: int) -> list[int]:
    # A separate ordinary even/odd recursive algorithm for larger exact controls.
    N = len(x)
    if N == 1:
        return [x[0] % p]
    even = radix2_dft(x[::2], w * w % p, p)
    odd = radix2_dft(x[1::2], w * w % p, p)
    out = [0] * N
    phase = 1
    for k in range(N // 2):
        t = phase * odd[k] % p
        out[k] = (even[k] + t) % p
        out[k + N // 2] = (even[k] - t) % p
        phase = phase * w % p
    return out


def matrix_from_map(length: int, func: Callable[[list[int]], list[int]]) -> Matrix:
    cols = [func([int(i == j) for i in range(length)]) for j in range(length)]
    return [list(row) for row in zip(*cols)]


def independent_phi(r: int) -> int:
    bits = bin(r)[2:]
    return sum(int(bits[t]) * (int(bits[:t], 2) if t else 0) for t in range(len(bits)))


def bitreverse(r: int, bits: int) -> int:
    return int(f'{r:0{bits}b}'[::-1], 2) if bits else 0


def test_fourier() -> dict:
    rng = random.Random(2026101001)
    basis_vectors = fresh_vectors = entries = 0
    records = []
    for field in FIELDS:
        for N in (2, 4, 8, 16, 32, 64, 128):
            plan = FixedGraph(N, field)
            count = Counts()
            for j in range(N):
                x = [int(i == j) for i in range(N)]
                expected = [pow(plan.w, k * j, field.p) for k in range(N)]
                assert plan.fourier(x) == expected
                basis_vectors += 1
                entries += N
            for x in ([1] * N, [rng.randrange(field.p) for _ in range(N)],
                      [1 if i % 2 else field.p - 1 for i in range(N)]):
                assert plan.fourier(x, count) == direct_dft(x, plan.w, field.p)
                fresh_vectors += 1
                entries += N
            n = plan.n
            expected_mul = n * (N // 2 - 1) + N - n - 1
            assert count.additions == 3 * N * n
            assert count.multiplications == 3 * expected_mul
            assert all(plan.phi[j] == independent_phi(j) for j in range(N))
            assert all(0 <= v < N for v in plan.phi)
            assert sum(v == 0 for v in plan.phi) == n + 1
            records.append({'p': field.p, 'N': N, 'online_additions': N * n,
                            'online_multiplications': expected_mul,
                            'root_table_multiplications': plan.root_table_multiplications})
        for N in (256, 1024, 4096):
            plan = FixedGraph(N, field)
            for _ in range(2):
                x = [rng.randrange(field.p) for _ in range(N)]
                assert plan.fourier(x) == radix2_dft(x, plan.w, field.p)
                fresh_vectors += 1
                entries += N
    return {'basis_vectors': basis_vectors, 'fresh_vectors': fresh_vectors,
            'output_entries': entries, 'operation_counts': records,
            'warning': 'The actual Fourier executor remains Theta(N log N).'}


def test_partial_powers() -> dict:
    cases = nonzeros = 0
    for field in FIELDS:
        p = field.p
        for N in (2, 4, 8, 16, 32, 64):
            plan = FixedGraph(N, field)
            Q = q_matrix(N, plan.w, p)
            power = eye(N)
            for t in range(plan.n + 1):
                L, m = 1 << t, N >> t
                formula = [[0] * N for _ in range(N)]
                for r in range(N):
                    prefix, v = divmod(r, L)
                    br = bitreverse(v, t)
                    for a in range(L):
                        s = a * m + prefix
                        formula[r][s] = pow(plan.w, s * br + independent_phi(v), p)
                assert power == formula, (p, N, t)
                assert all(sum(value != 0 for value in row) == L for row in power)
                assert sum(power[r][0] != 0 for r in range(N)) == L
                assert [r for r in range(N) if power[r][0]] == list(range(L))
                nonzeros += N * L
                cases += 1
                power = mm(Q, power, p)
    return {'matrix_identities': cases, 'nonzero_entries': nonzeros,
            'consequence': 'Q^t has exactly N*2^t nonzeros for 0<=t<=log2(N).'}


def test_branches_and_haar() -> dict:
    rng = random.Random(2026101002)
    branch_cases = haar_cases = schur_cases = 0
    for field in FIELDS:
        p = field.p
        for N in (2, 4, 8, 16, 32, 64, 128, 256):
            plan = FixedGraph(N, field)
            z = 7
            for _ in range(3):
                x = [rng.randrange(p) for _ in range(N)]
                assert plan.apply(x) == [(a + b) % p for a, b in zip(
                    plan.branch_apply(x, 0), plan.branch_apply(x, 1))]
                for bit in (0, 1):
                    y = plan.branch_solve(x, bit, z)
                    a = plan.branch_apply(y, bit)
                    assert [(u - z * v) % p for u, v in zip(y, a)] == x
                    branch_cases += 1
                v = [rng.randrange(p) for _ in range(N // 2)]
                injected = [0] * N
                injected[1::2] = v
                solved = plan.branch_solve(injected, 0, z)
                expected = [plan.roots[r] * (solved[r] - solved[r + N // 2]) % p
                            for r in range(N // 2)]
                actual = plan.haar_apply(v, z)
                assert actual == expected
                assert plan.haar_inverse(actual, z) == v
                haar_cases += 1
            if N <= 32:
                Q = q_matrix(N, plan.w, p)
                G0 = matrix_from_map(N, lambda v: plan.branch_solve(v, 0, z))
                m = N // 2
                H = matrix_from_map(m, lambda v: plan.haar_apply(v, z))
                J = [[int(r == 2 * s + 1) for s in range(m)] for r in range(N)]
                C = [[(plan.roots[r] * (int(j == r) - int(j == r + m))) % p
                      for j in range(N)] for r in range(m)]
                inv_small = inverse(add(eye(m), scale(H, -z, p), p), p)
                correction = mm(mm(mm(mm(G0, J, p), inv_small, p), C, p), G0, p)
                rhs = add(G0, scale(correction, z, p), p)
                lhs = inverse(add(eye(N), scale(Q, -z, p), p), p)
                assert lhs == rhs
                assert sum(v != 0 for row in H for v in row) == m * plan.n
                schur_cases += 1
    return {'branch_vector_solves': branch_cases, 'haar_apply_inverse_pairs': haar_cases,
            'complete_schur_matrix_checks': schur_cases,
            'warning': 'H and H^-1 are cheap. No cheap inverse of I-zH is supplied.'}


def test_traces_and_determinants() -> dict:
    trace_cases = det_jets = periodic_states = 0
    records = []
    for field in FIELDS:
        p = field.p
        for N in (2, 4, 8, 16, 32, 64):
            plan = FixedGraph(N, field)
            traces, states = plan.trace_prefix(extra=2)
            assert states == 8 * N - 2
            Q = q_matrix(N, plan.w, p)
            power = eye(N)
            for k, value in enumerate(traces, 1):
                power = mm(Q, power, p)
                assert sum(power[i][i] for i in range(N)) % p == value
                trace_cases += 1
            periodic_states += states
            # Independent determinant-polynomial interpolation, not Newton identities.
            if N <= 16:
                zs = list(range(N + 1))
                values = [determinant(add(eye(N), scale(Q, -z, p), p), p) for z in zs]
                V = [[pow(z, k, p) for k in range(N + 1)] for z in zs]
                coefficients = mv(inverse(V, p), values, p)
                coefficients += [0] * 4
                assert coefficients[:plan.n + 3] == plan.determinant_jet(extra=2)
                det_jets += 1
            records.append({'p': p, 'N': N, 'traces': traces,
                            'periodic_states': states, 'determinant_jet': plan.determinant_jet(extra=2)})
    return {'exact_trace_checks': trace_cases, 'independent_determinant_jets': det_jets,
            'enumerated_periodic_states': periodic_states, 'records': records}


def dual_trace_power(W0: Matrix, W1: Matrix, exponent: int, p: int) -> tuple[int, int]:
    # Compute in F[epsilon]/epsilon^2 by repeated dense products.
    n = len(W0)
    base, tangent = eye(n), [[0] * n for _ in range(n)]
    for _ in range(exponent):
        tangent = add(mm(tangent, W0, p), mm(base, W1, p), p)
        base = mm(base, W0, p)
    return sum(base[i][i] for i in range(n)) % p, sum(tangent[i][i] for i in range(n)) % p


def test_marked_cycle_gradient() -> dict:
    rng = random.Random(2026101003)
    input_cases = coordinates = 0
    scalar_independence = 0
    for field in FIELDS:
        p = field.p
        for N in (2, 4, 8, 16):
            plan = FixedGraph(N, field)
            Q = q_matrix(N, plan.w, p)
            L = plan.n + 2
            old_scalar = None
            for _ in range(2):
                x = [rng.randrange(p) for _ in range(N)]
                W0 = [row[:] + [x[i]] for i, row in enumerate(Q)] + [[0] * (N + 1)]
                expected_fourier = direct_dft(x, plan.w, p)
                expected_graph = [0] * N
                for k, r in enumerate(plan.reversal):
                    expected_graph[r] = plan.roots[plan.phi[r]] * expected_fourier[k] % p
                gradient = []
                for j in range(N):
                    W1 = [[0] * (N + 1) for _ in range(N + 1)]
                    W1[N][j] = 1
                    scalar, derivative = dual_trace_power(W0, W1, L, p)
                    gradient.append(derivative * pow(L, -1, p) % p)
                assert gradient == expected_graph
                if old_scalar is not None:
                    assert scalar == old_scalar  # value at t=0 forgets x, gradient does not.
                    scalar_independence += 1
                old_scalar = scalar
                input_cases += 1
                coordinates += N
    return {'arbitrary_input_cases': input_cases, 'dual_number_derivative_coordinates': coordinates,
            'input_independent_scalar_controls': scalar_independence,
            'warning': 'Dense dual arithmetic is an identity oracle, NOT the conjectured fast trace circuit.'}



def test_bordered_determinant() -> dict:
    rng = random.Random(2026101005)
    cases = affine_checks = 0
    for field in FIELDS:
        p = field.p
        for N in (2, 4, 8, 16):
            plan = FixedGraph(N, field)
            Q = q_matrix(N, plan.w, p)
            # Full polynomial interpolation is an independent small-size oracle.
            V = [[pow(z, k, p) for k in range(N + 2)] for z in range(N + 2)]
            Vi = inverse(V, p)
            d = plan.determinant_jet(extra=2)
            for _ in range(3):
                x = [rng.randrange(p) for _ in range(N)]
                t = [rng.randrange(p) for _ in range(N)]
                W = [row[:] + [x[i]] for i, row in enumerate(Q)] + [t[:] + [0]]
                vals = [determinant(add(eye(N + 1), scale(W, -z, p), p), p)
                        for z in range(N + 2)]
                e = mv(Vi, vals, p) + [0] * 4
                # Truncated formal quotient E/D has constant coefficient 1.
                quotient = []
                for j in range(plan.n + 3):
                    quotient.append((e[j] - sum(d[k] * quotient[j-k]
                                              for k in range(1, j+1))) % p)
                fx = direct_dft(x, plan.w, p)
                qx = [0] * N
                for k, r in enumerate(plan.reversal):
                    qx[r] = plan.roots[plan.phi[r]] * fx[k] % p
                expected = sum(a*b for a,b in zip(t,qx)) % p
                assert -quotient[plan.n + 2] % p == expected
                z = 7
                A = add(eye(N), scale(Q, -z, p), p)
                D = determinant(A, p)
                E = determinant(add(eye(N + 1), scale(W, -z, p), p), p)
                twot = [2*v % p for v in t]
                W2 = [row[:] + [x[i]] for i, row in enumerate(Q)] + [twot + [0]]
                E2 = determinant(add(eye(N + 1), scale(W2, -z, p), p), p)
                assert (E2-D) % p == 2*(E-D) % p
                cases += 1
                affine_checks += 1
    return {'independent_polynomial_quotient_checks': cases,
            'exact_affinity_in_markers_checks': affine_checks,
            'warning': 'Dense determinant interpolation is only an independent test oracle.'}


def test_simple_paths() -> dict:
    records = []
    for n in range(1, 8):
        N = 1 << n
        simple = 0
        for s in range(N):
            for emitted in range(N):
                current = s
                visited = {s}
                ok = True
                for t in range(n - 1, -1, -1):
                    current = (2 * current + ((emitted >> t) & 1)) % N
                    if current in visited:
                        ok = False
                    visited.add(current)
                simple += ok
        lower = max(0, N * N - math.comb(n + 1, 2) * N)
        assert simple >= lower
        records.append({'N': N, 'all_input_output_paths': N * N,
                        'internally_simple_paths': simple, 'proved_lower_bound': lower})
    return {'records': records, 'consequence': 'Even simple marked paths remain quadratically numerous.'}


def test_negative_controls() -> dict:
    rng = random.Random(2026101004)
    missing_phase = alias_rejections = singular_rejections = 0
    for field in FIELDS:
        p = field.p
        for N in (4, 8, 16, 32):
            plan = FixedGraph(N, field)
            x = [rng.randrange(1, p) for _ in range(N)]
            y = plan.power(x, plan.n)
            wrong = [y[r] for r in plan.reversal]
            assert wrong != direct_dft(x, plan.w, p)
            missing_phase += 1
        for N in (4, 8):
            plan = FixedGraph(N, field)
            Q = q_matrix(N, plan.w, p)
            b = 1 << (plan.n.bit_length())  # b > log2(N), b divides p-1 in our fields.
            xi, a = field.root(b), 7
            total = [[0] * N for _ in range(N)]
            for j in range(b):
                z = a * pow(xi, j, p) % p
                green = inverse(add(eye(N), scale(Q, -z, p), p), p)
                total = add(total, scale(green, pow(xi, -j * plan.n, p), p), p)
            total = scale(total, pow(b, -1, p), p)
            Qn, Qb = eye(N), eye(N)
            for _ in range(plan.n):
                Qn = mm(Q, Qn, p)
            for _ in range(b):
                Qb = mm(Q, Qb, p)
            rhs = scale(mm(Qn, inverse(add(eye(N), scale(Qb, -pow(a, b, p), p), p), p), p),
                        pow(a, plan.n, p), p)
            assert total == rhs
            assert total != scale(Qn, pow(a, plan.n, p), p)
            alias_rejections += 1
        plan = FixedGraph(8, field)
        for f in (lambda: plan.branch_solve([1] * 8, 0, 1),
                  lambda: plan.haar_inverse([1] * 4, field.inverse(2))):
            try:
                f()
                raise AssertionError('A singular control was not rejected.')
            except ZeroDivisionError:
                singular_rejections += 1
    return {'missing_phase_rejections': missing_phase, 'resolvent_alias_rejections': alias_rejections,
            'singular_parameter_rejections': singular_rejections}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('RESULTS.json'))
    args = parser.parse_args()
    tests = [test_fourier, test_partial_powers, test_branches_and_haar,
             test_traces_and_determinants, test_marked_cycle_gradient,
             test_bordered_determinant, test_simple_paths, test_negative_controls]
    results = {'status': 'Exact algebra verified; NO sub-N-log-N Fourier algorithm constructed.',
               'fields': [{'p': f.p, 'primitive_generator': f.generator} for f in FIELDS],
               'tests': {}}
    for test in tests:
        print(test.__name__, flush=True)
        results['tests'][test.__name__] = test()
    results['passed_groups'] = len(tests)
    args.output.write_text(json.dumps(results, indent=2) + '\n', encoding='utf-8')
    print(f'PASS: {len(tests)}/{len(tests)} groups. Results: {args.output}')


if __name__ == '__main__':
    main()
