from pathlib import Path
import json
from grading import prepare_grading, apply_r, apply_d, split_pairs, join_pairs
from fixed_kernel import Counted, prepare
from operators import prepare_sparse, build_operators, horner_c, identity
from prior_exact_arithmetic import PrimeField, CyclotomicField, mm, mv


def matrix_of(field, n, action):
    columns = [action([field.one if i==j else field.zero for i in range(n)]) for j in range(n)]
    return [[columns[j][i] for j in range(n)] for i in range(n)]


def scaled(field, s, a):
    return [[field.mul(s, v) for v in row] for row in a]


def power(field, a, k):
    out = identity(field, len(a))
    while k:
        if k&1: out = mm(field, out, a)
        k >>= 1
        if k: a = mm(field, a, a)
    return out


def one_case(field, n, label):
    q = field.root(n); plan = prepare_grading(field, n, q)
    base = prepare(field, n, q); sparse = prepare_sparse(field, n, q)
    C = build_operators(field, sparse, base.kernel)['C']
    R = matrix_of(field, n, lambda x: apply_r(field, plan, x))
    D = matrix_of(field, n, lambda x: apply_d(field, plan, x))
    H = matrix_of(field, n, lambda x: horner_c(field, sparse, base.kernel, x)[0])
    ident = identity(field, n)
    assert mm(field, R, C) == scaled(field, field.power(q,n-1), mm(field,C,R))
    assert mm(field, H, R) == mm(field, D, H)
    assert power(field,R,n) == ident == power(field,D,n)
    K = power(field,R,n//2)
    assert mm(field,K,K) == ident
    assert mm(field,K,C) == scaled(field,field.neg(field.one),mm(field,C,K))
    S = matrix_of(field,n,lambda x:split_pairs(field,plan,x))
    Si = matrix_of(field,n,lambda x:join_pairs(field,plan,x))
    assert mm(field,S,Si) == ident == mm(field,Si,S)
    split = mm(field,mm(field,S,C),Si)
    m=n//2
    assert all(split[i][j]==field.zero for i in range(n) for j in range(n) if (i<m)==(j<m))
    outputs=0
    for j in range(n):
        x=[field.one if i==j else field.zero for i in range(n)]
        assert apply_r(field,plan,apply_r(field,plan,x),inverse=True)==x
        assert join_pairs(field,plan,split_pairs(field,plan,x))==x
        y=mv(field,H,x)
        for _ in range(4):
            x=apply_r(field,plan,x); y=apply_d(field,plan,y)
            assert y==mv(field,H,x)
            assert sum(v!=field.zero for v in x)==1
            outputs+=1
    mixed=[field.integer((3*i+2)%11-5) for i in range(n)]
    counted=Counted(field)
    apply_r(counted,plan,mixed); apply_d(counted,plan,mixed)
    assert dict(counted.count)=={'mul':3*n-1,'add':n-1}
    c=Counted(field); split_pairs(c,plan,mixed)
    assert dict(c.count)=={'mul':3*m,'add':m,'sub':m}
    c=Counted(field); join_pairs(c,plan,mixed)
    assert dict(c.count)=={'add':m,'sub':m,'mul':m}
    assert all(field.mul(plan['r'][i],plan['inverse_r'][i])==field.one for i in range(n))
    assert all(field.mul(plan['h'][i],plan['h'][(i+m)%n])==field.one for i in range(n))
    # This version duplicates a root table deliberately; count the complete setup.
    assert plan['preparation']=={'mul':21*n//2+(n.bit_length()-1)-3,
        'sub':2*n-1,'constant_inverse':2,'neg':n+1}
    return dict(n=n,field=label,basis_vectors=n,related_outputs=outputs,
                preparation=plan['preparation'],input_output_update=dict(counted.count))


if __name__=='__main__':
    rows=[]
    for p in (65537,998244353):
        for n in (2,4,8,16,32): rows.append(one_case(PrimeField(p),n,str(p)))
    for n in (2,4,8): rows.append(one_case(CyclotomicField(n),n,'Q(root_'+str(n)+')'))
    result=dict(status='PASS',configurations=len(rows),
        basis_vectors=sum(r['basis_vectors'] for r in rows),
        related_outputs=sum(r['related_outputs'] for r in rows),rows=rows,
        scope='Exact sparse grading, pair split and related-query update; first H(C) is paid and no new fresh FFT is claimed.')
    out=Path(__file__).with_name('results.json'); out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='rows'}))
