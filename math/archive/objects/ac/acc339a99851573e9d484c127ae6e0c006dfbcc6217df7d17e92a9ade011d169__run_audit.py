"""New H-specific identities, finite-boundary tests, and a restricted certificate."""
import json
from pathlib import Path

from prior_exact_arithmetic import PrimeField, CyclotomicField
from fixed_kernel import prepare
from operators import prepare_sparse, horner_c
from decimation import prepare_decimation, apply_family
from branch_fusion import (polynomial_action, shift, four_odd_kernel_rewrite,
                            two_odd_call_obstruction)


def basis(field, n, j):
    return [field.one if i == j else field.zero for i in range(n)]


def check_case(field, n, label):
    q = field.root(n)
    plan = prepare_decimation(field, n, q)
    sparse = prepare_sparse(field, n, q)
    m = n//2
    level = plan.levels[1]
    even, odd = plan.kernel[::2], plan.kernel[1::2]
    smaller = prepare(field, m, field.mul(q, q)).kernel
    def act(coefficients, values):
        return polynomial_action(field, level, coefficients, values)
    def at_cyclic_shift(coefficients, values):
        out = [field.mul(coefficients[-1], value) for value in values]
        for coefficient in reversed(coefficients[:-1]):
            out = [field.add(a, field.mul(coefficient, b))
                   for a, b in zip(shift(out), values)]
        return out
    for j in range(m):
        x = basis(field, m, j)
        ex, ox = act(even, x), act(odd, x)
        conjugated_ox = shift(act(odd, shift(x)), True)
        assert ex == [field.sub(a, field.mul(q, b))
                      for a, b in zip(ox, conjugated_ox)]
        conjugated_ex = shift(act(even, shift(x)), True)
        assert [field.sub(a, b) for a, b in zip(ex, conjugated_ex)] == apply_family(field, level, ox)
        norm = [field.sub(a, b) for a, b in zip(act(even, ex),
                        apply_family(field, level, act(odd, ox)))]
        assert norm == act(smaller, x)
        # D^m=0 licenses the finite remainder vanishing; J^m=I does not.
        scaled_even = [field.mul(value, field.power(q, 2*k))
                       for k, value in enumerate(even)]
        bad_lhs = [field.sub(field.sub(a, b), c)
                   for a, b, c in zip(at_cyclic_shift(even, x),
                        at_cyclic_shift(scaled_even, x),
                        shift(at_cyclic_shift(odd, x)))]
        expected_remainder = [field.neg(field.mul(odd[-1], z)) for z in x]
        assert bad_lhs == expected_remainder
        assert any(z != field.zero for z in bad_lhs)
    # Audit the exact scalar finite remainder before evaluating at D.
    residual = [field.zero]*(m+1)
    for k in range(m):
        residual[k] = field.mul(even[k], field.sub(field.one, field.power(q, 2*k)))
        if k:
            residual[k] = field.sub(residual[k], odd[k-1])
    residual[m] = field.neg(odd[-1])
    assert residual[:-1] == [field.zero]*m
    assert residual[-1] == field.neg(plan.kernel[-1]) != field.zero
    # Identify the J-eigenbasis and its single broken edge explicitly.
    lambdas = [field.neg(field.power(q, (-2*i) % n)) for i in range(m)]
    for j in range(m):
        eigenvector = [field.power(lambdas[j], i) for i in range(m)]
        assert shift(eigenvector) == [field.mul(lambdas[j], v) for v in eigenvector]
        destination = lambdas[(j+1) % m]
        weight = field.mul(field.add(field.one, destination),
                           field.add(field.one, field.mul(q, destination)))
        expected = [field.mul(weight, field.power(destination, i)) for i in range(m)]
        assert apply_family(field, level, eigenvector) == expected
        assert (weight == field.zero) == (j == m-1)
    # Every entry on or below the diagonal of O in that basis is nonzero.
    for j in range(m):
        product = field.one
        for i in range(j, m):
            if i > j:
                product = field.mul(product, field.mul(field.add(field.one, lambdas[i]),
                            field.add(field.one, field.mul(q, lambdas[i]))))
            assert field.mul(odd[i-j], product) != field.zero
    counts = None
    for j in range(n):
        x = basis(field, n, j)
        got, counts = four_odd_kernel_rewrite(field, plan, x)
        wanted, _ = horner_c(field, sparse, plan.kernel, x)
        assert got == wanted
    assert counts['field_operations'] == dict(mul=16*m*m+4*m-1,
                                              add=12*m*m-5*m,
                                              sub=6*m-2, neg=2)
    obstruction = two_odd_call_obstruction(field, n, q) if m >= 4 else None
    return dict(field=label, n=n, status='PASS', half_basis_vectors=m,
                complete_operator_basis_vectors=n,
                finite_remainder_coefficient=field.encode(residual[-1]),
                two_identical_odd_call_obstruction=obstruction,
                preparation=plan.preparation,
                four_odd_candidate_counts=counts)


def main():
    rows = []
    for p in (65537, 998244353):
        for n in (4, 8, 16, 32):
            rows.append(check_case(PrimeField(p), n, f'F_{p}'))
    for n in (4, 8):
        rows.append(check_case(CyclotomicField(n), n, f'Q(zeta_{n})'))
    result = dict(status='PASS', cases=len(rows),
                  half_basis_vectors=sum(row['half_basis_vectors'] for row in rows),
                  complete_operator_basis_vectors=sum(row['complete_operator_basis_vectors'] for row in rows),
                  nonzero_obstruction_certificates=sum(row['two_identical_odd_call_obstruction'] is not None for row in rows),
                  scope='H-specific finite contiguous/norm identities; exact four-call rewrite; restricted two-identical-O-call obstruction, not a general lower bound',
                  verdict='No reduction of the complete three-call decimation or the O(N log N) comparator',
                  rows=rows)
    destination = Path(__file__).parent/'results'/'branch_fusion_audit.json'
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({key:value for key,value in result.items() if key != 'rows'}, indent=2))


if __name__ == '__main__':
    main()
