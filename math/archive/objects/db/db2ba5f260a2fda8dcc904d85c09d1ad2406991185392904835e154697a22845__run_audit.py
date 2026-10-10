"""New finite-boundary identities, exact arithmetic, complete basis verification."""
import json
from pathlib import Path
from time import perf_counter

from fixed_kernel import prepare
from operators import (prepare_sparse, apply_c_charged, horner_c, build_operators,
    identity, lower_kernel, matrix_add, matrix_sub, matrix_scale)
from prior_exact_arithmetic import PrimeField, CyclotomicField, mm, mv, fourier


def power(field, matrix, exponent):
    out = identity(field, len(matrix))
    while exponent:
        if exponent & 1:
            out = mm(field, out, matrix)
        exponent >>= 1
        if exponent:
            matrix = mm(field, matrix, matrix)
    return out


def polynomial(field, matrix, coefficients):
    ident=identity(field,len(matrix))
    out=matrix_scale(field,coefficients[-1],ident)
    for coefficient in reversed(coefficients[:-1]):
        out=matrix_add(field,mm(field,matrix,out),matrix_scale(field,coefficient,ident))
    return out


def one_case(field, n, label):
    q = field.root(n)
    plan, sparse = prepare(field, n, q), prepare_sparse(field, n, q)
    ops = build_operators(field, sparse, plan.kernel)
    a, b, u, w, c = [ops[k] for k in ('A','B','U','W','C')]
    ha, hb = ops['H_A'], ops['H_B']
    ha_inverse = lower_kernel(field, plan.middle)
    ident = identity(field, n)
    zero = matrix_scale(field, field.zero, ident)
    q_inverse = field.power(q, n-1)
    # Weighted opposite shift and exact q-Weyl relation.
    actual = matrix_sub(field, mm(field,b,a), matrix_scale(field,q_inverse,mm(field,a,b)))
    assert actual == matrix_scale(field,field.sub(q,field.one),ident)
    # Exact conjugation retains the lower-left corner.
    assert mm(field,mm(field,ha,b),ha_inverse) == c
    # Check the alternate boundary formula B H(A)=H(q^-1 A)(B-I)-corner.
    modulated = [field.mul(value, field.power(q_inverse,j)) for j,value in enumerate(plan.kernel)]
    expected = matrix_sub(field,mm(field,lower_kernel(field,modulated),matrix_sub(field,b,ident)),ops['corner'])
    assert mm(field,b,ha) == expected
    # Cyclic q-commuting pair including the corner.
    assert mm(field,u,w) == matrix_scale(field,q,mm(field,w,u))
    assert power(field,u,n) == ident
    assert power(field,w,n) == matrix_scale(field,field.neg(field.one),ident)
    assert power(field,c,n) == zero
    # Actual Fourier-middle conjugation M A M^-1 = B.
    middle = [[plan.middle[i] if i+j == n-1 else field.zero for j in range(n)] for i in range(n)]
    middle_inverse = [[field.inv(plan.middle[j]) if i+j == n-1 else field.zero for j in range(n)] for i in range(n)]
    assert mm(field,mm(field,middle,a),middle_inverse) == b
    h_c_reference = mm(field,mm(field,ha,hb),ha_inverse)
    short_coefficients=[field.integer(v) for v in (2,-3,5,1)]
    short_reference=mm(field,mm(field,ha,polynomial(field,b,short_coefficients)),ha_inverse)
    h_c_columns = []
    for j in range(n):
        basis = [field.one if i == j else field.zero for i in range(n)]
        small, small_cost = apply_c_charged(field,sparse,basis)
        assert small == mv(field,c,basis)
        assert small_cost['field_operations'] == {'mul':2*n,'add':n}
        result, cost = horner_c(field,sparse,plan.kernel,basis)
        assert result == mv(field,h_c_reference,basis)
        assert cost['field_operations'] == {'mul':3*n*n-2*n,'add':2*n*n-2*n}
        short_result,short_cost=horner_c(field,sparse,short_coefficients,basis)
        assert short_result==mv(field,short_reference,basis)
        assert short_cost['field_operations']=={'mul':10*n,'add':6*n}
        h_c_columns.append(result)
    h_c = [[h_c_columns[j][i] for j in range(n)] for i in range(n)]
    assert mm(field,ha,hb) == mm(field,h_c,ha)
    # Order matters: F=P H(C) H(A) D P, not P H(C) D R H(A) R P.
    core=mm(field,h_c,ha)
    chirp=[field.mul(plan.middle[j],plan.factorial[j]) for j in range(n)]
    rewritten_fourier=[[field.mul(plan.factorial[i],field.mul(core[i][j],chirp[j]))
                       for j in range(n)] for i in range(n)]
    assert rewritten_fourier==fourier(field,n)
    assert sparse.preparation == {'mul':n+n.bit_length()-1,'sub':n-1,'constant_inverse':1,'neg':1}
    # Deliberately drop the boundary: the changed matrix cannot be nilpotent.
    no_corner = matrix_add(field,b,u)
    assert power(field,no_corner,n) == ident
    assert no_corner != c
    return {'field':label, 'n':n, 'basis_vectors':n,
        'exact_q_weyl_relation':True, 'conjugation_with_corner':True,
        'middle_conjugation':True, 'full_fourier_rewrite':True,
        'cyclic_pair':True, 'nilpotent_C':True,
        'omitted_corner_Nth_power':'identity, not zero',
        'sparse_preparation':sparse.preparation,'one_sparse_C':small_cost,
        'degree_three_macro':short_cost,'full_H_C_horner':cost}


def false_exponential_product():
    field=CyclotomicField(2)
    q=field.root(2)
    plan=prepare(field,2,q)
    ops=build_operators(field,prepare_sparse(field,2,q),plan.kernel)
    exact=polynomial(field,ops['C'],plan.kernel)
    false=mm(field,polynomial(field,ops['W'],plan.kernel),polynomial(field,ops['U'],plan.kernel))
    difference=matrix_sub(field,false,exact)
    witness=mv(field,difference,[field.one,field.zero])
    assert witness==[field.zero,field.inv(field.integer(8))]
    return {'n':2,'q':field.encode(q),
        'false_claim':'H_q(U+W)=H_q(W)H_q(U)',
        'difference_on_e0':[field.encode(value) for value in witness],
        'reason':'Product retains the degree-two WU/4 term although H_2 has degree one.'}


def main():
    start, rows = perf_counter(), []
    for p in (65537,998244353):
        field=PrimeField(p)
        for n in (2,4,8,16,32):
            rows.append(one_case(field,n,f'F_{p}'))
    for n in (2,4,8):
        rows.append(one_case(CyclotomicField(n),n,f'Q(zeta_{n})'))
    report={'status':'PASS','cases':len(rows),'basis_vectors':sum(r['basis_vectors'] for r in rows),
        'elapsed_seconds':perf_counter()-start,
        'scope':'Exact noncommuting graph rewrite with finite boundary; no arbitrary FFT speedup.',
        'finite_exponential_negative_control':false_exponential_product(),
        'cases_detail':rows}
    path=Path(__file__).parent/'results'/'boundary_audit.json'
    path.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='cases_detail'},indent=2))


if __name__=='__main__':
    main()
