"""Independent finite-field audit. Stdlib only, deterministic; exits on failure."""
from __future__ import annotations
import itertools
import json
import random
from pathlib import Path

from phase15 import (
 P, root_of_unity, gauss_table, fourier_weyl_support_size,
 weyl_coefficients_fourier_inverse, multiscale_inverse_polynomial,
 chirp_kernel, chirp_direct_transform, direct_dft,
 dyadic_binomial_product, fused_dyadic_binomial,
 inverse_chirp_linear_generation, chirp_digit_cut_rank,
 oriented_inverse_chain_polynomial,
 exact_fourier_intertwining_certificate,
)

ROOT=Path(__file__).resolve().parent


def complete_subset_sums(n: int, strides: tuple[int,...]) -> bool:
    sums={0}
    for stride in strides:
        sums=sums|{(t+stride)%n for t in sums}
    return len(sums)==n


def exact_direct_gauss(n:int,w:int,p:int=P)->list[int]:
    # Independent of the project gaussian-table evaluator: sum powers directly.
    return [sum(pow(w,(j*j+d*j)%n,p) for j in range(n))%p for d in range(n)]


def direct_chirp_matrix_check(n:int,p:int=P)->int:
    z=root_of_unity(2*n,p)
    w=z*z%p
    checked=0
    for row in range(n):
        for col in range(n):
            # Bluestein: D * F_- * D = C.
            assert pow(z,(row-col)**2,p) == (pow(z,row*row,p)*pow(w,-row*col,p)*pow(z,col*col,p))%p
            checked+=1
    # C*Cinv = Identity tested independently via explicit dot products.
    invn=pow(n,-1,p)
    for i in range(n):
        for j in range(n):
            zsum=sum(pow(z,(i-k)**2-(k-j)**2,p) for k in range(n))%p
            assert zsum*invn%p == (1 if i==j else 0)
            checked+=1
    return checked


def main():
    out={'status':'PASS','model':'exact modular field arithmetic, no FFT calls',
         'field_prime':P,'phase14_predecessor':'tested separately',
         'fourier_weyl_support':[], 'witnesses':{},'chirp_audits':[],
         'large_positive_control':{}}
    # Gaussian/Weyl coefficient support proof stress-tested for odd/even lengths.
    for n,p in [(3,97),(4,P),(5,241),(6,97),(7,337),(8,P),
                (16,P),(32,P),(64,P),(128,P)]:
        w=root_of_unity(n,p)
        gauss=exact_direct_gauss(n,w,p)
        calculated=gauss_table(n,w,p)
        assert gauss==calculated
        gnonzero={d for d,val in enumerate(gauss) if val!=0}
        if n&1: expected=set(range(n))
        elif n%4==0: expected=set(range(0,n,2))
        else: expected=set(range(1,n,2))
        assert gnonzero==expected
        num=n*len(gnonzero)
        assert num==fourier_weyl_support_size(n)
        out['fourier_weyl_support'].append({'n':n,'prime':p,'nonzero_weyl_atoms':num,
                                             'expected':fourier_weyl_support_size(n)})

    # Independently test Weyl coefficients against actual matrix trace expressions.
    # c_ab=(1/n)*trace((S^a T^b)^(-1) F_+ / n) for inverse F_-.
    trace_coefficients_checked=0
    for n in (4,8,16,32):
        w=root_of_unity(n)
        coeffs=weyl_coefficients_fourier_inverse(n,w)
        n2inv=pow(n*n,-1,P)
        for a in range(n):
            for b in range(n):
                trace=sum(pow(w,(j+a)*j-b*j,P) for j in range(n))%P
                expected=trace*n2inv%P
                assert coeffs.get((a,b),0)==expected
                trace_coefficients_checked+=1
    out['witnesses']['direct_trace_coefficients_checked']=trace_coefficients_checked
    # Exact global Fourier characterisation: M*S=T^-1*M, M*e0=ones.
    for n in (4,8,16,32):
        w=root_of_unity(n)
        negative=[[pow(w,-r*c,P) for c in range(n)] for r in range(n)]
        assert exact_fourier_intertwining_certificate(negative,w)
        negative[n//2][n//2]=(negative[n//2][n//2]+1)%P
        assert not exact_fourier_intertwining_certificate(negative,w)
    out['witnesses']['exact_intertwining_valid_invalid_pairs']=4

    # Enumerate *all multisets* of m nonzero strides for small dyadic lengths.
    # Full support requires a permutation of distinct v2-valuations.
    multiset_checked=0
    for n in (4,8,16):
        m=n.bit_length()-1
        full=0
        for strides in itertools.combinations_with_replacement(range(1,n),m):
            complete=complete_subset_sums(n,strides)
            valuations=[(s&-s).bit_length()-1 for s in strides]
            vexpected=len(set(valuations))==m
            assert complete==vexpected, (n,strides)
            full+=int(complete)
            multiset_checked+=1
        predict=1
        for j in range(m):
            predict*=2**(m-j-1)
        assert full==predict
        out['chirp_audits'].append({'n':n,'full_support_m_shift_multisets':full,
                                    'total_multisets_checked':'exhaustive'})
    out['witnesses']['exhaustive_shift_multisets_checked']=multiset_checked

    # Exact chirp=DFT and inverse chirp convolution checks, all complete outputs.
    rand=random.Random(0x17015)
    chirp_coefficients=0
    for n in (4,8,16,32,64,128):
        z=root_of_unity(2*n)
        checked=direct_chirp_matrix_check(n) if n<=32 else 0
        omega=z*z%P
        for _ in range(3):
            x=[rand.randrange(P) for _ in range(n)]
            outch=chirp_direct_transform(x,z)
            expected=direct_dft(x,omega)
            assert outch==expected
            chirp_coefficients+=n
        # q0q3!=q1q2 excludes an exactly m-stage binomial shift product.
        q=chirp_kernel(n,z,inverse=True)
        assert q[0]*q[3]%P != q[1]*q[2]%P
        assert q[0]*q[3]*pow(q[1]*q[2]%P,-1,P)%P==pow(z,-4,P)
        out['chirp_audits'].append({'n':n,'direct_matrix_entries_checked':checked,
                                   'inverse_chirp_has_full_support':all(q),
                                   'cross_ratio_obstruction':True})
    out['witnesses']['full_dft_coefficients_checked']=chirp_coefficients
    # Full binary-digit Schmidt ranks; finite-field row elimination is exact.
    tensor_rank_checks=[]
    for m in range(3,13):
        n=1<<m
        z=root_of_unity(2*n)
        for split in sorted(set((1,m//2,m-1))):
            actual=chirp_digit_cut_rank(n,z,split)
            expect=min(1<<split,1<<(m-split))
            assert actual==expect
            tensor_rank_checks.append({'n':n,'split_low_bits':split,'rank':actual})
    out['witnesses']['chirp_bit_cut_rank_checks']=tensor_rank_checks

    # Cheap kernel generation must not be mistaken for fast convolution.
    nlarge=65536
    zlarge=root_of_unity(2*nlarge)
    qlarge,qcount=inverse_chirp_linear_generation(nlarge,zlarge)
    for j in (0,1,2,3,11,199,4095,32767,65535):
        expected=pow(nlarge,-1,P)*pow(zlarge,-j*j,P)%P
        assert qlarge[j]==expected
    assert qcount.total()<3*nlarge
    out['witnesses']['chirp_kernel_linear_generation']={
       'n':nlarge,'charged_operations':qcount.as_dict(),
       'independent_sampled_coefficients':9,
       'warning':'Only generates the kernel. Does not apply its convolution to arbitrary input.'}

    # Multiscale 3-atom factor symbolic support, including n=4 small edge case.
    support_checks=0
    for m in range(2,9):
        n=2**m; w=root_of_unity(n)
        shifts=[2**j for j in range(m)]
        poly=multiscale_inverse_polynomial(n,shifts,shifts,
                                          [j+3 for j in range(m)],
                                          [j+7 for j in range(m)],w)
        assert len(poly)==3**m
        assert all((a&b)==0 for a,b in poly)
        assert (1,1) not in poly
        if n<=128:
            fcoeff=weyl_coefficients_fourier_inverse(n,w)
            assert (1,1) in fcoeff
            assert len(fcoeff)==n*n//2
        support_checks+=len(poly)
    out['witnesses']['dyadic_multiscale_weyl_atoms_checked']=support_checks
    # Independently test support invariance under changes of *Weyl monomial frame*.
    # This does not license free arbitrary basis conversions.
    frames=0; oriented_products=0
    for n in (4,8,16,32):
        omega=root_of_unity(n)
        support=set(weyl_coefficients_fourier_inverse(n,omega))
        for _ in range(40):
            a,b,c,d=[rand.randrange(n) for _ in range(4)]
            if (a*d-b*c)&1==0:continue   # determinant odd => unit in Z_2^m
            image={((a*u+c*v)%n,(b*u+d*v)%n) for u,v in support}
            assert len(image)==len(support)
            frames+=1
        for _ in range(20):
            factors=[]
            for layer in range(3):
                u=(rand.randrange(n),rand.randrange(n))
                v=(rand.randrange(n),rand.randrange(n))
                factors.append((u,v,rand.randrange(1,P),rand.randrange(1,P)))
            poly=oriented_inverse_chain_polynomial(n,factors,omega)
            assert len(poly)<=27
            oriented_products+=1
    out['witnesses']['weyl_coordinate_frames_checked']=frames
    out['witnesses']['arbitrarily_oriented_inverse_products_checked']=oriented_products

    # 65,536-entry *arbitrary fresh input*, fully charged positive CONTROL.
    n=65536
    alpha=7
    x=[rand.randrange(P) for _ in range(n)]
    stage,cstage=dyadic_binomial_product(x,alpha)
    fused,cfused=fused_dyadic_binomial(x,alpha)
    assert stage==fused
    d=(1-pow(alpha,n,P))%P
    assert d!=0
    for i in range(n):
        assert (fused[i]-alpha*fused[i-1])%P == d*x[i]%P
    # An independent reference on chosen output coefficients (O(n) each).
    independently_checked=0
    for k in (0,1,2,3,17,127,509,1023,4095,16384,32767,65535):
        acc=0;pw=1
        for t in range(n):
            acc=(acc + pw*x[(k-t)%n])%P
            if t!=n-1:pw=pw*alpha%P
        assert acc==fused[k]
        independently_checked+=1
    # Check that the operator is NOT the Fourier transform.
    omega=root_of_unity(n)
    dft_rows_checked=0;different=0
    for k in (0,1,2,7,31,127,511,1023):
        pw=1;step=pow(omega,-k,P);acc=0
        for val in x:
            acc=(acc+pw*val)%P
            pw=pw*step%P
        different+=int(acc!=fused[k]);dft_rows_checked+=1
    assert different>0
    out['large_positive_control']={
        'n':n,'input':'fresh unrelated modular random vector, fixed seed',
        'full_outputs_compared':n,'full_recurrence_equations_checked':n,
        'independent_convolution_coefficients':independently_checked,
        'separate_dft_rows_checked':dft_rows_checked,
        'separate_dft_rows_different':different,
        'literal_stages':n.bit_length()-1,
        'literal_operation_ledger':cstage.as_dict(),
        'fused_operation_ledger':cfused.as_dict(),
        'ratio_literal_over_fused':round(cstage.total()/cfused.total(),5),
        'note':'These two paths compute one Green-derived operator, not the DFT.'
    }
    (ROOT/'AUDIT_RESULTS.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print('PASS Phase 15 independent audit')
    print(json.dumps({'support_counts':out['fourier_weyl_support'],
                      'exhaustive_multisets':multiset_checked,
                      'chirp_dft_coefficients':chirp_coefficients,
                      'large_n':n,
                      'stage_ops':cstage.total(),
                      'fused_ops':cfused.total(),
                      'stage_vs_fused':round(cstage.total()/cfused.total(),3),
                      'not_dft':different},indent=2))

if __name__=='__main__':
    main()
