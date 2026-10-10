"""Audit new orbit rule only; previous factorization tests are not relabeled."""
import json
from pathlib import Path
from time import perf_counter

from fixed_kernel import apply, prepare
from orbit_rewrite import full_orbit_reference, collapsed_orbit, false_fourier_collapse
from prior_exact_arithmetic import PrimeField, CyclotomicField


def one_case(field, n, b, label):
    q = field.root(n)
    for j in range(n):
        x = [field.one if i == j else field.zero for i in range(n)]
        reference, _ = full_orbit_reference(field, n, q, b, x)
        result, counts = collapsed_orbit(field, n, q, b, x)
        assert result == reference, (label, n, b, j)
        if b == n:
            assert result == x
    m = n//b
    if m > 1:
        assert counts['field_operations'] == {
            'mul': b*m*(m+1)//2, 'add': b*m*(m-1)//2}
        assert counts['kernel_preparation']['mul'] == 6*m-4+m.bit_length()-1
    x = [field.integer((j*j+2*j+5) % 23-11) for j in range(n)]
    assert full_orbit_reference(field, n, q, b, x)[0] == collapsed_orbit(field, n, q, b, x)[0]
    return {'field': label, 'n': n, 'orbit_size': b, 'basis_vectors': n,
            'mixed_input': True, 'collapsed_cost': counts}


def counterexample():
    field, n = PrimeField(65537), 8
    plan = prepare(field, n, field.root(n))
    for j in range(n):
        x = [field.one if i == j else field.zero for i in range(n)]
        true, _ = apply(field, plan, x)
        wrong = false_fourier_collapse(field, plan, x)
        if true != wrong:
            return {'field': 'F_65537', 'n': n, 'basis_index': j,
                    'true_fourier': true, 'illegal_norm_replacement': wrong,
                    'wrong_outputs': sum(a != b for a, b in zip(true, wrong))}
    raise AssertionError('negative control unexpectedly passed')


def main():
    start, rows = perf_counter(), []
    for p in (65537, 998244353):
        field = PrimeField(p)
        for n in (2, 4, 8, 16, 32):
            for b in (2, 4, 8):
                if b <= n:
                    rows.append(one_case(field, n, b, f'F_{p}'))
            if n > 8:
                rows.append(one_case(field, n, n, f'F_{p}'))
    for n in (2, 4, 8):
        for b in (2, 4, 8):
            if b <= n:
                rows.append(one_case(CyclotomicField(n), n, b, f'Q(zeta_{n})'))
    result = {'status': 'PASS', 'cases': len(rows),
        'basis_vectors': sum(row['basis_vectors'] for row in rows),
        'elapsed_seconds': perf_counter()-start,
        'scope': 'Conditional exact graph compression, not an arbitrary Fourier speedup.',
        'negative_control': counterexample(), 'records': rows}
    path = Path(__file__).parent / 'results' / 'orbit_audit.json'
    path.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'records'}, indent=2))


if __name__ == '__main__':
    main()
