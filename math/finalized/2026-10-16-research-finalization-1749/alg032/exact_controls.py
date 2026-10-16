#!/usr/bin/env python3
"""Fresh, self-authored exact integer controls; no supplied code imports.

For power-of-two M >= 2, z^(M/2) = -1. Count exponents of
S(a,s) times its conjugate and reduce in Z[z]/(z^(M/2)+1).
No floating-point arithmetic or third-party packages are used.
"""
from collections import Counter
from fractions import Fraction
import hashlib
import json
from pathlib import Path


def norm_coefficients(M, a, s):
    if M == 1:
        return (1,)
    assert M >= 2 and M & (M - 1) == 0
    exponents = [(a*t*t+s*t) % M for t in range(M)]
    counts = Counter(exponents)
    out = [0] * (M // 2)
    for p, cp in counts.items():
        for q, cq in counts.items():
            e = (p-q) % M
            out[e % (M//2)] += cp*cq*(1 if e < M//2 else -1)
    return tuple(out)


def scalar_norm(M, a, s):
    v = norm_coefficients(M, a, s)
    assert all(c == 0 for c in v[1:]), (M, a, s, v)
    return v[0]


def main():
    gauss_count = 0
    dc_count = 0
    odd_d_control_count = 0
    dimension_summaries = []
    for M in (2, 4, 8, 16, 32, 64):
        gauss = {}
        for a in range(1, M, 2):
            for s in range(M):
                actual = scalar_norm(M, a, s)
                expected = M*(1+((-1)**s if M >= 4 else -(-1)**s))
                assert actual == expected, (M, a, s, actual, expected)
                gauss[a, s] = actual
                gauss_count += 1
        ks = sorted({1, 2, 3, M//2, M-1, M, M+1, 2*M+1})
        this_dc_count = 0
        for a in range(1, M, 2):
            for b in range(M):
                for d in range(0, M, 2):
                    for K in ks:
                        actual = Fraction(sum(gauss[a, (b+d*r) % M] for r in range(K)), K*M)
                        expected = 1+((-1)**b if M >= 4 else -(-1)**b)
                        assert actual == expected, (M, K, a, b, d, actual, expected)
                        assert abs(actual-1) == 1
                        dc_count += 1
                        this_dc_count += 1
        # Odd-d controls confirm that the uniform DC-error claim cannot be
        # extended to every d; these do not test the source's non-DC theorem.
        for b in range(M):
            for d in range(1, M, 2):
                for K in ks:
                    actual = Fraction(sum(gauss[1, (b+d*r) % M] for r in range(K)), K*M)
                    sign = 1 if M >= 4 else -1
                    expected = 1+sign*Fraction(((-1)**b)*(K % 2), K)
                    assert actual == expected
                    odd_d_control_count += 1
        dimension_summaries.append({'M':M,'K_values':ks,'all_odd_a_residues':M//2,
                                    'all_b_residues':M,'all_even_d_residues':M//2,
                                    'even_step_dc_cases':this_dc_count})

    # Explicit minimal, endpoint and excluded-guard certificates.
    exceptions = {
        'M1': {'M':1,'a':1,'b':0,'d':0,'K_values':[1,2,3,17],
               'normalized_decoded_dc':'1','normalized_error':'0'},
        'M2_even_b_swaps_to_zero': {'M':2,'a':1,'b':0,'d':0,
                                  'normalized_decoded_dc':str(Fraction(scalar_norm(2,1,0),2))},
        'M4_minimum_admitted': {'M':4,'a':1,'b':0,'d':0,
                               'normalized_decoded_dc':str(Fraction(scalar_norm(4,1,0),4))},
        'a_even_formula_counterexample': {'M':4,'a':0,'b':0,'d':0,
                                         'normalized_decoded_dc':str(Fraction(scalar_norm(4,0,0),4))},
        'd_odd_even_K_DC_exact': {'M':4,'K':2,'a':1,'b':0,'d':1,
                                'normalized_decoded_dc':str(Fraction(scalar_norm(4,1,0)+scalar_norm(4,1,1),8))},
    }
    assert scalar_norm(1,1,0) == 1
    assert exceptions['M2_even_b_swaps_to_zero']['normalized_decoded_dc'] == '0'
    assert exceptions['M4_minimum_admitted']['normalized_decoded_dc'] == '2'
    assert exceptions['a_even_formula_counterexample']['normalized_decoded_dc'] == '4'
    assert exceptions['d_odd_even_K_DC_exact']['normalized_decoded_dc'] == '1'
    # Residue representatives, including negative parameters, are harmless.
    negative_representative_controls = 0
    for M in (2,4,8,16):
        for a,s in ((-1,-2),(-3,-1),(M+1,2*M+2),(-M-1,-M-2)):
            assert norm_coefficients(M,a,s) == norm_coefficients(M,a % M,s % M)
            negative_representative_controls += 1
    output = {
        'status':'PASS',
        'method':'Exact integer cyclotomic exponent-count reduction, then exact Fraction normalization.',
        'supplied_research_programs_executed':False,
        'self_authored_control_file_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'gauss_identity_cases':gauss_count,
        'even_step_dc_cases':dc_count,
        'odd_step_guard_controls':odd_d_control_count,
        'negative_representative_controls':negative_representative_controls,
        'dimensions':dimension_summaries,
        'exceptions':exceptions,
        'limits':'Finite exact controls are not the unbounded proof. REPORT.md gives the all-dimension proof under its stated guards.'
    }
    target = Path(__file__).with_name('CONTROL_RESULTS.json')
    target.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))


if __name__ == '__main__':
    main()
