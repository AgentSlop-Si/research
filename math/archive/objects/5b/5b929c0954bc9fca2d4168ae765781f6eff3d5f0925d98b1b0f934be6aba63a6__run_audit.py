"""Whole project cross-check and deterministic audit JSON generation."""
from __future__ import annotations
import json,random
from ordering_dp import optimal_orders
from analytic_certificate import run as analytic
from unitary_control import run as unitary
from exact_scan_macro import fft_via_mixed_scan_macros,dft_matrix,P
from reference_ntt import radix2_ntt

def main():
    report={'model':'Fresh exact full NTT, two supported primes; no cached input or threads.',
            'endpoint_orders':[optimal_orders(n) for n in (2,4,8)],
            'analytic_certificates':analytic(),
            'unitary_controls':unitary(),
            'whole_basis_checked':0,'fresh_random_checked':0,'root_prime':P,
            'macro_execution':[]}
    for n in (2,4,8,16,32,64,128):
        matrix=dft_matrix(n)
        for j in range(n):
            x=[int(i==j) for i in range(n)]
            y,info=fft_via_mixed_scan_macros(x)
            assert y==[row[j] for row in matrix]
            report['whole_basis_checked']+=1
        seed=random.Random(n+20261009)
        for _ in range(10):
            x=[seed.randrange(P) for _ in range(n)]
            y,info=fft_via_mixed_scan_macros(x)
            z,_=radix2_ntt(x)
            assert y==z
            report['fresh_random_checked']+=1
        report['macro_execution'].append({'n':n,'stages':info['macro_stages'],
            'scan_additions_upper':info['scan_additions_upper'],
            'scan_multiplications_upper':info['scan_multiplications_upper'],
            'twiddle_multiplications_upper':info['twiddle_multiplications_upper'],
            'permutation_index_steps':info['permutation_index_steps']})
    with open('audit_results.json','w') as f:json.dump(report,f,indent=2)
    return report
if __name__=='__main__':
    r=main()
    print('EXACT_AUDIT_OK')
    print('endpoint qsep ranks',[(e['n'],e['optimum']) for e in r['endpoint_orders']])
    print('independent 3x5 rank checks',sum(x['rank3_3x5_matrices'] for x in r['analytic_certificates']['primes']))
    print('independent Fourier basis columns',r['whole_basis_checked'])
    print('fresh dense random inputs',r['fresh_random_checked'])
    print('unitary controls',len(r['unitary_controls']))
