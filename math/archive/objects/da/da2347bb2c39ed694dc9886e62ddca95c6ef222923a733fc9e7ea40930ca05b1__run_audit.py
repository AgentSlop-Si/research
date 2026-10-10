"""Reproducible exact report: all-basis Fourier/chirp audit and random controls."""
import json
import random
from pathlib import Path
from chirp_exact import (P, make_chirp, dft_direct, dft_ntt, cyclic_convolution,
                         chirp_dft_direct, variable_filter, modular_rank,
                         matrix_lc_h, matrix_c_h, moment_matrix, cyclic_hankel,
                         predicted_full_spectral_probability)


def main():
    rng = random.Random(20261009)
    report = {'field_prime':P, 'seed':20261009,'convention':'positive DFT exponent',
              'scope':'exact modulo P; powers of 2 with even N and 2N dividing P-1',
              'interpretation':'algebraic and rank audit, no speedup claim','sizes':[]}
    for n in (2,4,8,16,32,64):
        c=make_chirp(n)
        # Every basis vector checked, so the full matrix identity is checked.
        for col in range(n):
            basis=[0]*n;basis[col]=1
            assert chirp_dft_direct(basis,c)==dft_direct(basis,c.omega)
        gauss=sum(c.h)%P
        assert gauss
        spectrum=dft_ntt(c.h,c.omega)
        assert spectrum==[gauss*v%P for v in c.d]
        inv=[pow(a,P-2,P) for a in c.h]
        assert cyclic_convolution(c.h,inv)==[n]+[0]*(n-1)
        ch_rank=modular_rank(matrix_c_h(c))
        lc_rank=modular_rank(matrix_lc_h(c))
        m_rank=modular_rank(moment_matrix(c))
        assert (ch_rank,lc_rank,m_rank)==(n,n-1,n)
        cases=24
        dense_filtered=0
        full_recurrence=0
        all_correct=True
        for _ in range(cases):
            x=[rng.randrange(P) for j in range(n)]
            y=cyclic_convolution(x,c.h)
            assert chirp_dft_direct(x,c)==dft_direct(x,c.omega)
            assert dft_ntt(x,c.omega)==dft_direct(x,c.omega)
            assert dft_ntt(y,c.omega)==dft_direct(y,c.omega)
            filt=variable_filter(y,c)
            dense_filtered+= (all(t!=0 for t in filt))
            full_recurrence+= (modular_rank(cyclic_hankel(y))==n)
        report['sizes'].append({
            'n':n,'all_basis_columns_verified':n,'random_fresh_inputs_verified':cases,
            'chirp_convolution_rank':ch_rank,'filtered_operator_rank':lc_rank,
            'moment_matrix_rank':m_rank,'random_filters_all_nonzero':dense_filtered,
            'random_outputs_full_periodic_recurrence_order':full_recurrence,
            'probability_full_spectral_order_exact_formula':f'(1-1/{P})^{n}',
            'probability_full_spectral_order_approx':predicted_full_spectral_probability(n),
            'probability_filter_has_any_zero_at_most':n/P,
            'dense_chirp_matvec_products':n*n,
            'radix2_ntt_butterflies':(n//2)*(n.bit_length()-1),
            'note':'NTT butterfly count does not include roots, additions and indexing',
        })
    report['totals']={
        'basis_columns_checked':sum(r['all_basis_columns_verified'] for r in report['sizes']),
        'fresh_random_vectors_checked':sum(r['random_fresh_inputs_verified'] for r in report['sizes']),
        'random_filters_dense':sum(r['random_filters_all_nonzero'] for r in report['sizes']),
        'random_outputs_full_periodic_order':sum(r['random_outputs_full_periodic_recurrence_order'] for r in report['sizes']),
        'rank_certificates':len(report['sizes'])*3,
    }
    p=Path(__file__).with_name('audit_results.json')
    p.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__': main()
