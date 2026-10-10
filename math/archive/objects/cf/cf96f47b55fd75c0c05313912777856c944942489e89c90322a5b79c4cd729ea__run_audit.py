"""Reproducible exact verification; no floating-point tolerances."""
import json
from pathlib import Path
from time import perf_counter

from fixed_kernel import apply, prepare, hankel, hankel_determinant_formula
from prior_exact_arithmetic import PrimeField, CyclotomicField, fourier, mv


def determinant(field, matrix):
    a, out = [row[:] for row in matrix], field.one
    for j in range(len(a)):
        pivot = next((i for i in range(j, len(a)) if a[i][j] != field.zero), None)
        if pivot is None:
            return field.zero
        if pivot != j:
            a[j], a[pivot] = a[pivot], a[j]
            out = field.neg(out)
        value = a[j][j]
        out = field.mul(out, value)
        reciprocal = field.inv(value)
        for i in range(j+1, len(a)):
            scale = field.mul(a[i][j], reciprocal)
            for k in range(j+1, len(a)):
                a[i][k] = field.sub(a[i][k], field.mul(scale, a[j][k]))
    return out


def check_case(field, n, label):
    root = field.root(n)
    assert field.power(root, n) == field.one
    assert field.power(root, n//2) != field.one
    plan = prepare(field, n, root)
    assert plan.factorial[-1] == field.integer(n)
    assert all(field.mul(a, b) == field.one for a, b in zip(plan.factorial, plan.kernel))
    assert plan.preparation == {'mul': 6*n-4+n.bit_length()-1,
        'sub': n-1, 'constant_inverse': 1, 'neg': n-1}
    f = fourier(field, n)
    for j in range(n):
        basis = [field.one if i == j else field.zero for i in range(n)]
        result, cost = apply(field, plan, basis)
        assert result == [f[i][j] for i in range(n)], (label, n, j)
        assert cost['field_operations'] == {'mul': n*n+4*n, 'add': n*n-n}
    # A mixed input checks the public call independently of basis-only sparsity.
    x = [field.integer((i*i+3*i+7) % 19-9) for i in range(n)]
    assert apply(field, plan, x)[0] == mv(field, f, x)
    # Coefficients of (1-z)H(z) = H(qz) modulo z^N.
    for j in range(n):
        left = plan.kernel[j] if j == 0 else field.sub(plan.kernel[j], plan.kernel[j-1])
        right = field.mul(field.power(root, j), plan.kernel[j])
        assert left == right
    # Exact convolution inverse is the middle diagonal coefficients.
    for j in range(n):
        total = field.zero
        for k in range(j+1):
            total = field.add(total, field.mul(plan.kernel[k], plan.middle[j-k]))
        assert total == (field.one if j == 0 else field.zero)
    certificates = []
    for shift in (0, 1):
        r = n//2
        actual = determinant(field, hankel(field, plan, r, shift))
        formula = hankel_determinant_formula(field, plan, r, shift)
        assert actual == formula and actual != field.zero
        certificates.append({'shift': shift, 'dimension': r,
                             'determinant': field.encode(actual)})
    return {'field': label, 'n': n, 'basis_vectors_verified': n,
        'preparation': plan.preparation, 'direct_evaluator': cost,
        'hankel_certificates': certificates,
        'q_difference_identity': True, 'inverse_kernel_identity': True}


def main():
    start = perf_counter()
    rows = []
    for p in (65537, 998244353):
        field = PrimeField(p)
        for n in (2, 4, 8, 16, 32, 64, 128):
            rows.append(check_case(field, n, f'F_{p}'))
    for n in (2, 4, 8, 16):
        rows.append(check_case(CyclotomicField(n), n, f'Q(zeta_{n})'))
    output = {'status': 'PASS', 'case_count': len(rows),
        'basis_vector_count': sum(row['basis_vectors_verified'] for row in rows),
        'hankel_determinants_verified': 2*len(rows),
        'elapsed_seconds': perf_counter()-start,
        'scope': 'Exact factorization and restricted streaming barrier, not a fast FFT claim.',
        'cases': rows}
    path = Path(__file__).parent / 'results' / 'exact_audit.json'
    path.write_text(json.dumps(output, indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k != 'cases'}, indent=2))


if __name__ == '__main__':
    main()
