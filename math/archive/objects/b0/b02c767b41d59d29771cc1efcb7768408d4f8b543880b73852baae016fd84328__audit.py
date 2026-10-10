"""Run independent exact audits for Boolean spectral completion candidate."""
from __future__ import annotations
import json
from math import comb
from pathlib import Path
from spectral_boolean import (primitive_root,dft,all_binary,spectrum_self_convolution,
        recover_one_from_others,signature_collision,half_complement_family,
        exact_poly_completion,evaluate_witness,witness_upper_operation_count,
        quadratic_rigidity_theorem,balance_failure_fraction)
from graded_certificate import rank_certificate,verify_certificate,graded_monomials,determinant_mod,evaluations_for_support


def negacyclic(a,b):
    # Exact product in Z[z]/(z^4+1), representing Q(zeta_8)
    c=[0]*4
    for i,u in enumerate(a):
        for j,v in enumerate(b):
            t=i+j
            c[t%4]+=(1 if t<4 else -1)*u*v
    return tuple(c)

def ring_add(*terms):
    return tuple(sum(a[j] for a in terms) for j in range(4))

def ring_neg(a):return tuple(-v for v in a)

def ring_scale(a,k):return tuple(v*k for v in a)

def ring_ff8(x):
    f=[]
    for k in range(8):
        c=[0]*4
        for j,v in enumerate(x):
            r=(k*j)%8
            c[r%4]+=v*(1 if r<4 else -1)
        f.append(tuple(c))
    return f

def cubic_paired_single_missing_exact_characteristic_zero():
    """Verify a degree-3 witness for one *single* omitted Fourier bin.
    This is noncompetitive with ordinary complex conjugation on binary inputs.
    Identity: 4X7 = -(X0-4)Q - R - 2 X1 X2 X4, with
    Q=X1X6+X2X5+X3X4 and R=X1²X5+X1X3²+X2²X3.
    """
    c0=(4,0,0,0)
    for x in all_binary(8):
        f=ring_ff8(x)
        mul=lambda *arr: _mul_many(arr)
        q=ring_add(mul(f[1],f[6]),mul(f[2],f[5]),mul(f[3],f[4]))
        r=ring_add(mul(f[1],f[1],f[5]),mul(f[1],f[3],f[3]),mul(f[2],f[2],f[3]))
        centered=ring_add(f[0],ring_neg(c0))
        rhs=ring_add(ring_neg(mul(centered,q)),ring_neg(r),ring_scale(mul(f[1],f[2],f[4]),-2))
        assert rhs==ring_scale(f[7],4),(x,rhs,ring_scale(f[7],4))
    return True

def _mul_many(arr):
    z=(1,0,0,0)
    for a in arr:z=negacyclic(z,a)
    return z


def run_audit():
    result={"date":"2026-10-09","model":"fresh Boolean input; exact full cyclic DFT, arithmetic over split fields and complex cyclotomic ring", "idempotence":{},"conjugate_pair_cubic_certificates":{},"single_missing":{},"half_spectrum_ambiguity":{}}
    for n in [8,16,32,64]:
        p=998244353;w=primitive_root(n,p)
        cases=all_binary(n) if n==8 else (tuple((i*i+37*i+seed*11)%13<6 for i in range(n)) for seed in range(32))
        tested=0;failures=0
        for x in cases:
            X=dft(x,p,w)
            assert spectrum_self_convolution(X,p)==tuple((n*v)%p for v in X)
            y=recover_one_from_others(X,1,p)
            if y is not None:assert y==X[1]
            else:failures+=1
            tested+=1
        result['idempotence'][str(n)]={"tested":tested,"singular_cases":failures,
            "balanced_fraction_exact":f"{balance_failure_fraction(n)[0]}/{balance_failure_fraction(n)[1]}"}
    for n in [8,16,32]:
        known=tuple(j for j in range(n) if j not in (1,n-1))
        cert=rank_certificate(n,998244353,1,degree=3,known=known)
        assert cert['status']=='no_completion_degree_at_most_d_over_C'
        assert verify_certificate(cert)
        root=primitive_root(n,998244353)
        powers=[[pow(root,(s*j)%n,998244353) for j in range(n)] for s in range(n)]
        a=[evaluations_for_support(n,998244353,powers,known,cert['monomials'],1,subset) for subset in cert['certificate_supports']]
        determinant=determinant_mod(a,998244353)
        assert determinant != 0
        result['conjugate_pair_cubic_certificates'][str(n)]={"source_bins":len(known),
            "candidate_monomials":len(cert['monomials']),
            "nonzero_augmented_determinant":True,"determinant_mod_998244353":determinant,
            "certificate_input_vectors":len(cert['certificate_supports']),
            "rows_examined":cert['rows_examined'],
            "supports":[list(s) for s in cert['certificate_supports']]}
    single=exact_poly_completion(8,97,tuple(range(7)),7,3)
    assert single['found'] and single['rank_audit'][-1]['degree']==3
    for x in all_binary(8):
        f=dft(x,97)
        assert evaluate_witness(f,single['witness'],97)==f[7]
    assert cubic_paired_single_missing_exact_characteristic_zero()
    result['single_missing']={"degree2_recoverable":False,"degree3_recoverable":True,
             "single_finite_field_witness": [ {"modes":list(mon),"coefficient_mod_97":coeff} for mon,coeff in single['witness']],
             "single_finite_field_naive_ops":witness_upper_operation_count(single['witness']),
             "characteristic_zero_all_256_binary_cases_exact_verified":True,
             "warning":"for real x, X[7] is simply conjugate of X[1]; not a speedup"}
    for n in [8,16]:
        w=primitive_root(n,998244353)
        signatures={}
        for x in half_complement_family(n):
            X=dft(x,998244353,w)
            even=tuple(X[j] for j in range(0,n,2))
            signatures[even]=signatures.get(even,0)+1
        assert len(signatures)==1
        assert next(iter(signatures.values()))==1<<(n//2)
        result['half_spectrum_ambiguity'][str(n)]={"different_binary_inputs":1<<(n//2),
            "identical_even_spectrum":True,"even_spectrum":[n//2]+[0]*(n//2-1)}
    return result

if __name__=='__main__':
    d=run_audit()
    path=Path(__file__).with_name('audit_results.json')
    path.write_text(json.dumps(d,indent=2)+'\n')
    print('Boolean spectral self-convolution: all tests pass.')
    print('Exact cubic pair omission no-go certificates:', {n:(v['candidate_monomials'],v['certificate_input_vectors']) for n,v in d['conjugate_pair_cubic_certificates'].items()})
    print('Positive single-frequency cubic identity verified over Q(zeta_8) for 256/256 binary inputs; not a speedup.')
    print('Half-even-spectrum ambiguity:',{n:v['different_binary_inputs'] for n,v in d['half_spectrum_ambiguity'].items()})
    print('Saved',path)
