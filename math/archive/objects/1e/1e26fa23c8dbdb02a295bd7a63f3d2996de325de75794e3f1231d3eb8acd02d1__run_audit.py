"""Exact basis verification of the new tail seed, recurrence, and fast action."""
import json
from pathlib import Path
from time import perf_counter
from tail_layers import prepare_tail,apply_seed,apply_tail_prefix,fft_exact
from prior_exact_arithmetic import PrimeField,CyclotomicField,mm,mv,fourier
from operators import build_operators,identity,matrix_add,matrix_sub,matrix_scale


def polynomial(field,matrix,coefficients):
    ident=identity(field,len(matrix))
    out=matrix_scale(field,coefficients[-1],ident)
    for coefficient in reversed(coefficients[:-1]):
        out=matrix_add(field,mm(field,matrix,out),matrix_scale(field,coefficient,ident))
    return out


def normal_layers(field,plan):
    n=plan.n
    weights=[plan.sparse.corner]+plan.sparse.upper
    wp=[[field.one for _ in range(n)]]
    for s in range(1,n):
        wp.append([field.mul(wp[-1][j],weights[(j-s+1)%n]) for j in range(n)])
    result=[]
    for degree in range(n,2*n-1):
        layer=[[field.zero for _ in range(n)] for _ in range(n)]
        for s in range(degree-n+1,n):
            r=degree-s
            coefficient=field.mul(plan.kernel[r],plan.kernel[s])
            for j in range(n):
                value=field.mul(coefficient,field.mul(wp[s][j],plan.powers[(-j*r)%n]))
                layer[(j-s)%n][j]=value
        result.append(layer)
    return result


def case(field,n,label):
    q=field.root(n)
    plan=prepare_tail(field,n,q)
    assert all(field.mul(a,b)==field.one for a,b in zip(plan.sigma,plan.sigma_inverse))
    layers=normal_layers(field,plan)
    ops=build_operators(field,plan.sparse,plan.kernel)
    # Exact seed grading, and every homogeneous recurrence.
    assert matrix_sub(field,mm(field,layers[0],ops['C']),mm(field,ops['C'],layers[0]))==matrix_scale(field,plan.inverse_n,ops['C'])
    wpower=identity(field,n); upower=identity(field,n)
    for k in range(1,n):
        wpower=mm(field,wpower,ops['W']); upower=mm(field,upower,ops['U'])
        forcing=matrix_scale(field,field.mul(plan.kernel[k],plan.inverse_n),
            matrix_sub(field,matrix_scale(field,plan.powers[k],wpower),upower))
        next_layer=layers[k] if k<len(layers) else matrix_scale(field,field.zero,identity(field,n))
        assert mm(field,ops['C'],layers[k-1])==matrix_add(field,
            matrix_scale(field,field.sub(field.one,plan.powers[k]),next_layer),forcing)
    full_tail=matrix_scale(field,field.zero,identity(field,n))
    for layer in layers:
        full_tail=matrix_add(field,full_tail,layer)
    kproduct=mm(field,polynomial(field,ops['W'],plan.kernel),polynomial(field,ops['U'],plan.kernel))
    assert full_tail==matrix_sub(field,kproduct,polynomial(field,ops['C'],plan.kernel))
    # Same basis inputs independently audit the backend transform and tail action.
    f=fourier(field,n)
    endpoints=sorted({0,min(1,n-2),min(3,n-2),n-2})
    prefix_matrices={}
    for endpoint in endpoints:
        prefix_matrices[endpoint]=matrix_scale(field,field.zero,identity(field,n))
        for layer in layers[:endpoint+1]:
            prefix_matrices[endpoint]=matrix_add(field,prefix_matrices[endpoint],layer)
    for j in range(n):
        x=[field.one if i==j else field.zero for i in range(n)]
        assert fft_exact(field,x,plan.powers)==[f[i][j] for i in range(n)]
        seed,seed_cost=apply_seed(field,plan,x)
        assert seed==[layers[0][i][j] for i in range(n)]
        log=n.bit_length()-1
        assert seed_cost['field_operations']=={'mul':n*log+4*n,'add':n*log,'sub':n*log}
        for endpoint in endpoints:
            out,cost=apply_tail_prefix(field,plan,x,endpoint)
            assert out==[prefix_matrices[endpoint][i][j] for i in range(n)]
            assert cost['field_operations']=={'mul':n*log+4*n+7*n*endpoint,
                'add':n*log+2*n*endpoint,'sub':n*log+2*n*endpoint}
    assert plan.preparation['additional']=={'mul':7*n-3,'neg':n,'constant_inverse':1}
    return {'field':label,'n':n,'basis_vectors':n,'prefix_endpoints':endpoints,
        'grading_identity':True,'all_homogeneous_recurrences':True,
        'full_tail_identity':True,'seed_cost':seed_cost,'full_tail_cost':cost,
        'preparation':plan.preparation}


def main():
    start=perf_counter(); cases=[]
    for p in (65537,998244353):
        field=PrimeField(p)
        for n in (2,4,8,16,32):
            cases.append(case(field,n,f'F_{p}'))
    for n in (2,4,8):
        cases.append(case(CyclotomicField(n),n,f'Q(zeta_{n})'))
    output={'status':'PASS','cases':len(cases),
        'basis_vectors':sum(row['basis_vectors'] for row in cases),
        'elapsed_seconds':perf_counter()-start,
        'scope':'O(N log N) first tail layer and O(N log N+kN) exact tail prefixes; no faster full FFT.',
        'records':cases}
    path=Path(__file__).parent/'results'/'tail_audit.json'
    path.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k!='records'},indent=2))


if __name__=='__main__':
    main()
