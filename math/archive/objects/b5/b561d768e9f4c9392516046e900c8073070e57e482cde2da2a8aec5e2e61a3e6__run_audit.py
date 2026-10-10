"""Exact finite audit of the all-N rational degree theorem, not a time bound."""
from pathlib import Path
import sys
import json

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'fft_qweyl_boundary_research'))
from fixed_kernel import prepare, hankel_determinant_formula
from prior_exact_arithmetic import PrimeField, CyclotomicField


def solve(field, a, b, variables):
    rows = [list(row) + [value] for row, value in zip(a, b)]
    pivots, used = [], 0
    for col in range(variables):
        pivot = next((i for i in range(used, len(rows)) if rows[i][col] != field.zero), None)
        if pivot is None:
            continue
        rows[used], rows[pivot] = rows[pivot], rows[used]
        inv = field.inv(rows[used][col])
        rows[used] = [field.mul(inv, v) for v in rows[used]]
        for i in range(len(rows)):
            if i != used and rows[i][col] != field.zero:
                factor = rows[i][col]
                rows[i] = [field.sub(v, field.mul(factor, w)) for v, w in zip(rows[i], rows[used])]
        pivots.append(col)
        used += 1
    if any(all(v == field.zero for v in row[:-1]) and row[-1] != field.zero for row in rows):
        return None
    result = [field.zero] * variables
    for i, col in enumerate(pivots):
        result[col] = rows[i][-1]
    return result


def product(field, a, b, n):
    result = [field.zero] * n
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if i+j < n:
                result[i+j] = field.add(result[i+j], field.mul(x, y))
    return result


def pade(field, kernel, m, d):
    n = len(kernel)
    a, b = [], []
    for j in range(m+1, n):
        a.append([kernel[j-ell] if j >= ell else field.zero for ell in range(1, d+1)])
        b.append(field.neg(kernel[j]))
    solution = solve(field, a, b, d)
    if solution is None:
        return None
    denominator = [field.one] + solution
    coefficients = product(field, denominator, kernel, n)
    assert all(v == field.zero for v in coefficients[m+1:])
    return coefficients[:m+1], denominator


def one_case(field, n, name, exhaustive=True):
    q = field.root(n)
    plan = prepare(field, n, q)
    inverse_plan = prepare(field, n, field.power(q, n-1))
    inverse = [field.mul(v, field.power(q, (-j) % n)) for j, v in enumerate(inverse_plan.kernel)]
    assert inverse == plan.middle
    assert product(field, plan.kernel, inverse, n) == [field.one] + [field.zero]*(n-1)
    rejects, direct, reciprocal = 0, 0, 0
    for total in range(n-1):
        for d in range(total+1):
            m = total-d
            if not exhaustive and total != n-2:
                continue
            assert pade(field, plan.kernel, m, d) is None
            if m >= d-1:
                assert hankel_determinant_formula(field, plan, d+1, m+1-d) != field.zero
                direct += 1
            else:
                assert hankel_determinant_formula(field, inverse_plan, m+1, d+1-m) != field.zero
                reciprocal += 1
            rejects += 1
    sharp = []
    for d in range(n):
        m = n-1-d
        value = pade(field, plan.kernel, m, d)
        assert value is not None
        p, r = value
        assert p[0] == r[0] == field.one
        assert p[-1] != field.zero and r[-1] != field.zero
        sharp.append({'numerator_degree':m,'denominator_degree':d})
    return {'field':name,'n':n,'exhaustive_below_bound':exhaustive,
            'inconsistent_pade_systems':rejects,'direct_hankel_certificates':direct,
            'reciprocal_hankel_certificates':reciprocal,'sharp_approximants':sharp}


def main():
    records=[]
    for prime in (65537,998244353):
        f=PrimeField(prime)
        for n in (2,4,8,16):
            records.append(one_case(f,n,f'F_{prime}'))
        records.append(one_case(f,32,f'F_{prime}',False))
    for n in (2,4,8):
        records.append(one_case(CyclotomicField(n),n,f'Q(zeta_{n})'))
    result={'status':'PASS','configurations':len(records),
            'inconsistent_pade_systems':sum(x['inconsistent_pade_systems'] for x in records),
            'sharp_approximants':sum(len(x['sharp_approximants']) for x in records),
            'scope':'Exact representation degree only; no general FFT time lower bound.',
            'cases':records}
    out=Path(__file__).parent/'results'
    out.mkdir(exist_ok=True)
    (out/'rational_degree_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='cases'},indent=2))


if __name__=='__main__':
    main()
