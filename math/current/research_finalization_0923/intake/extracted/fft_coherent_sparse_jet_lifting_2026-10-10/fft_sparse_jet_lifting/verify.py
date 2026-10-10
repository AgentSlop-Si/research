"""Independent exact controls for sparse-jet lifting. Run: python verify.py.

The reference Fourier potentials deliberately have quadratic-size circuits.
No run of this verifier constitutes a sub-NlogN FFT construction.
"""
from __future__ import annotations
import json
from itertools import product
from pathlib import Path
from random import Random
from circuit import (Circuit, compile_hessian_at_zero, dense_fourier_potential,
                     four_point_potential, prefix_square_potential,
                     two_direction_jet, direct_dft)


def is_prime(p):
    return p >= 2 and all(p % d for d in range(2, int(p**0.5)+1))


def root_of_order(n, p):
    if (p-1) % n:
        raise ValueError('order unavailable')
    for g in range(2,p):
        r = pow(g,(p-1)//n,p)
        if pow(r,n,p)==1 and (n==1 or pow(r,n//2,p)!=1):
            return r
    raise RuntimeError('root not found')


def rank(mat,p):
    if not mat:
        return 0
    a=[row[:] for row in mat]
    r=0
    for col in range(len(a[0])):
        pivot=next((i for i in range(r,len(a)) if a[i][col]%p),None)
        if pivot is None:
            continue
        a[r],a[pivot]=a[pivot],a[r]
        inv=pow(a[r][col]%p,-1,p)
        a[r]=[v*inv%p for v in a[r]]
        for i in range(r+1,len(a)):
            v=a[i][col]%p
            if v:
                a[i]=[(z-v*t)%p for z,t in zip(a[i],a[r])]
        r+=1
        if r==len(a):
            break
    return r


def basis(n,j):
    return [int(i==j) for i in range(n)]


def test_fourier_lift(rng):
    report={'basis_vectors':0,'dense_vectors':0,'output_coordinates':0,
            'two_direction_formal_jets':0,'two_sparse_values':0,'programs':[]}
    for p in (12289,65537):
        assert is_prime(p)
        for n in (2,4,8,16,32):
            root=root_of_order(n,p)
            for noise in ('none','polynomial','rational'):
                c=dense_fourier_potential(n,root,p,noise)
                linear,stats=compile_hessian_at_zero(c)
                stats.update(n=n,prime=p,noise=noise)
                report['programs'].append(stats)
                for j in range(n):
                    x=basis(n,j)
                    assert linear.apply(x)==direct_dft(x,root,p)
                    report['basis_vectors']+=1
                    report['output_coordinates']+=n
                for _ in range(5):
                    x=[rng.randrange(p) for _ in range(n)]
                    assert linear.apply(x)==direct_dft(x,root,p)
                    report['dense_vectors']+=1
                    report['output_coordinates']+=n
                pairs=[(i,j) for i in range(n) for j in range(i,n)] if n<=8 else [tuple(rng.randrange(n) for _ in range(2)) for __ in range(12)]
                for i,j in pairs:
                    v,w=basis(n,i),basis(n,j)
                    jet=two_direction_jet(c,v,w)
                    expected=[0,0,0,pow(2,-1,p)*pow(root,i*i,p)%p,
                              pow(root,i*j,p),pow(2,-1,p)*pow(root,j*j,p)%p]
                    assert jet==expected,(p,n,noise,i,j,jet,expected)
                    report['two_direction_formal_jets']+=1
                    for a,b in ((2,3),(0,5),(7,0)):
                        x=[(a*v[k]+b*w[k])%p for k in range(n)]
                        if noise=='rational' and n>=3 and x[0]==p-1:
                            continue
                        got=c.evaluate(x)
                        fx=direct_dft(x,root,p)
                        expected_value=sum(x[k]*fx[k] for k in range(n))*pow(2,-1,p)%p
                        assert got==expected_value
                        report['two_sparse_values']+=1
    return report


def test_general_compiler(rng):
    report={'regular_circuits':0,'independent_hessian_bilinear_checks':0}
    for p in (12289,65537):
        for n in (3,5,8):
            for _ in range(5):
                c=Circuit(n,p)
                nodes=list(range(n))
                for j in range(35):
                    a=rng.choice(nodes)
                    b=rng.choice(nodes)
                    op=j%4
                    if op==0:
                        z=c.add(a,b)
                    elif op==1:
                        z=c.mul(a,b)
                    elif op==2:
                        z=c.sub(a,b)
                    else:
                        value=c.values([0]*n)[a]
                        shift=rng.randrange(1,p)
                        if (shift+value)%p==0:
                            shift=(shift+1)%p
                        z=c.inv(c.add(a,c.const(shift)))
                    nodes.append(z)
                c.output=nodes[-1]
                prog,_=compile_hessian_at_zero(c)
                for __ in range(6):
                    v=[rng.randrange(p) for i in range(n)]
                    w=[rng.randrange(p) for i in range(n)]
                    hv=prog.apply(v)
                    expected=two_direction_jet(c,v,w)[4]
                    assert sum(a*b for a,b in zip(w,hv))%p==expected
                    report['independent_hessian_bilinear_checks']+=1
                report['regular_circuits']+=1
    return report


def test_nonlinear_dense_nonfourier():
    records=[]
    p=65537
    for n in (4,8,16,32,64,128):
        c=prefix_square_potential(n,p)
        prog,stats=compile_hessian_at_zero(c)
        for j in (0,n//2,n-1):
            assert prog.apply(basis(n,j))==[(n-max(i,j))%p for i in range(n)]
        h=[[n-max(i,j) for j in range(n)] for i in range(n)]
        assert rank(h,p)==n
        assert all(v%p for row in h for v in row)
        root=root_of_order(n,p)
        assert prog.apply(basis(n,0))!=direct_dft(basis(n,0),root,p)
        stats.update(n=n,full_rank=True,dense=True,fourier=False)
        records.append(stats)
    return {'examples':records}


def test_four_point(rng):
    records=[]
    for p in (12289,65537):
        root=root_of_order(4,p)
        c=four_point_potential(root,p)
        prog,stats=compile_hessian_at_zero(c)
        for _ in range(40):
            v=[rng.randrange(p) for j in range(4)]
            assert prog.apply(v)==direct_dft(v,root,p)
        stats.update(prime=p,root=root,valid_vectors=40)
        records.append(stats)
    return records


def test_negative_controls():
    p,n=65537,8
    root=root_of_order(n,p)
    # Fast support-selected scalar oracle: zero-input execution is the constant 0.
    zero=Circuit(n,p);zero.output=zero.const(0)
    prog,_=compile_hessian_at_zero(zero)
    assert prog.apply(basis(n,0))==[0]*n
    assert direct_dft(basis(n,0),root,p)==[1]*n
    # Matching every one-sparse quadratic restriction does not fix mixed terms.
    diag=Circuit(n,p);out=diag.const(0)
    for j in range(n):
        out=diag.add(out,diag.mul(diag.const(pow(2,-1,p)*pow(root,j*j,p)),diag.mul(j,j)))
    diag.output=out
    assert two_direction_jet(diag,basis(n,0),basis(n,1))[4]==0
    assert pow(root,0*1,p)==1
    # An intermediate inverse at zero must be rejected even if later cancelled.
    bad=Circuit(2,p);bad.output=bad.mul(0,bad.inv(0))
    try:
        compile_hessian_at_zero(bad)
    except ZeroDivisionError:
        pass
    else:
        raise AssertionError('singular circuit admitted')
    # Exhaustive finite-field agreement is NOT a formal derivative identity.
    p=17;n=2;root=16
    c=dense_fourier_potential(n,root,p)
    old=c.output
    power=0
    for _ in range(4):
        power=c.mul(power,power)
    power=c.mul(power,0)  # x0^17
    c.output=c.add(old,c.mul(c.sub(power,0),1))
    point_checks=0
    for a,b in product(range(p),repeat=2):
        x=[a,b];fx=direct_dft(x,root,p)
        assert c.evaluate(x)==sum(u*v for u,v in zip(x,fx))*pow(2,-1,p)%p
        point_checks+=1
    prog,_=compile_hessian_at_zero(c)
    assert prog.apply([0,1])!=direct_dft([0,1],root,p)
    assert two_direction_jet(c,[1,0],[0,1])[4] != 1
    return {'zero_branch_rejected':True,'one_sparse_only_rejected':True,
            'singular_intermediate_rejected':True,'frobenius_exhaustive_values':point_checks,
            'frobenius_formal_jet_mismatch':True}


def test_rigidity_and_products(rng):
    result={'fourier_diagonal_rank_checks':0,'separable_product_checks':0,
            'zero_anchor_counts_tested':[0,1,2,3]}
    for p in (12289,65537):
        for n in (4,8,16,32):
            root=root_of_order(n,p)
            f=[[pow(root,i*j,p) for j in range(n)] for i in range(n)]
            for _ in range(8):
                a=[row[:] for row in f]
                for i in range(n):
                    a[i][i]=(a[i][i]-rng.randrange(p))%p
                assert rank(a,p)>=n//2
                result['fourier_diagonal_rank_checks']+=1
            for zeros in (0,1,2,3):
                aa=[rng.randrange(1,p) for _ in range(n)]
                bb=[rng.randrange(1,p) for _ in range(n)]
                for j in range(zeros):
                    bb[j]=0
                c=Circuit(n,p);out=c.const(1)
                for j in range(n):
                    out=c.mul(out,c.add(c.const(bb[j]),c.mul(c.const(aa[j]),j)))
                c.output=out
                prog,_=compile_hessian_at_zero(c)
                columns=[prog.apply(basis(n,j)) for j in range(n)]
                h=[[columns[j][i] for j in range(n)] for i in range(n)]
                if zeros==0:
                    bprod=1
                    for b in bb:bprod=bprod*b%p
                    v=[aa[j]*pow(bb[j],-1,p)%p for j in range(n)]
                    for j in range(n):h[j][j]=(h[j][j]+bprod*v[j]*v[j])%p
                    assert rank(h,p)<=1
                else:
                    assert rank(h,p)<= (2 if zeros<=2 else 0)
                result['separable_product_checks']+=1
    return result


def test_moment_rank():
    n,p=8,65537
    c=Circuit(n,p)
    m0=m1=c.const(0)
    for i in range(n):
        m0=c.add(m0,i)
        m1=c.add(m1,c.mul(c.const(i),i))
    # A regular rational function of only two linear measurements.
    c.output=c.mul(c.mul(m0,m1),c.inv(c.add(c.const(1),m0)))
    prog,_=compile_hessian_at_zero(c)
    cols=[prog.apply(basis(n,j)) for j in range(n)]
    mat=[[cols[j][i] for j in range(n)] for i in range(n)]
    assert rank(mat,p)<=2
    root=root_of_order(n,p)
    assert rank([[pow(root,i*j,p) for j in range(n)] for i in range(n)],p)==n
    return {'input_dimension':n,'linear_measurements':2,'hessian_rank':rank(mat,p)}


def main():
    rng=Random(26061010)
    result={
        'status':'exact reduction and compiler verified; NO new sub-NlogN Fourier circuit constructed',
        'seed':26061010,
        'groups':{
            'fourier_lift':test_fourier_lift(rng),
            'general_compiler':test_general_compiler(rng),
            'nonfourier_linear_size':test_nonlinear_dense_nonfourier(),
            'four_point_control':test_four_point(rng),
            'negative_controls':test_negative_controls(),
            'rigidity_products':test_rigidity_and_products(rng),
            'moment_rank':test_moment_rank(),
        }
    }
    result['passed_groups']=len(result['groups'])
    dest=Path(__file__).with_name('RESULTS.json')
    dest.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('PASS',result['passed_groups'],'groups')
    print(json.dumps({k:({kk:vv for kk,vv in v.items() if kk not in ('programs','examples')} if isinstance(v,dict) else v) for k,v in result['groups'].items()},indent=2))

if __name__=='__main__':
    main()
