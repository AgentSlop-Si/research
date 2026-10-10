"""Exact Galois spectral obstruction for ONE polynomial Fourier-phase mask.

Let N=2^m >=16, L=N/8, K=Q(zeta_8), and sigma(zeta_N)=zeta_N^9.
If F = S2 * diag(zeta_N^f(j)) * S1 for projectively K matrices,
P_9 must be similar to a scalar multiple of diag(zeta_L^f(j)).
The first has an eigenvalue of multiplicity exactly 4 (primitive L root).
The second has every eigenvalue multiplicity divisible by 8 if f has
integer coefficients, so such an exact factorization is impossible.
"""
from collections import Counter
from galois_gate import n_power_of_two,cycle_count_multiplier


def cycle_lengths(n, a=9):
    seen=bytearray(n)
    lengths=[]
    for j in range(n):
        if seen[j]:continue
        v=j;k=0
        while not seen[v]:
            seen[v]=1;k+=1;v=a*v%n
        lengths.append(k)
    return lengths


def permutation_spectrum(n):
    """Exponent e represents eigenvalue zeta_{L}^e; L=n//8."""
    assert n_power_of_two(n)
    L=n//8
    spectrum=Counter()
    for d in cycle_lengths(n):
        assert L%d==0
        for j in range(d):
            spectrum[j*(L//d)] += 1
    return dict(spectrum)


def phase_ratio_spectrum(n,exponent):
    """Eigenvalue exponents of sigma(Q) Q^-1 for q_j=zeta_N^f(j)."""
    assert n_power_of_two(n)
    L=n//8
    return dict(Counter(exponent(j)%L for j in range(n)))


def invariant(n, kind):
    polys={'linear':lambda j:j,
           'quadratic':lambda j:j*j,
           'cubic':lambda j:j**3,
           'quintic':lambda j:3*j**5+7*j**2+2*j+1,
           'large_coeff':lambda j:257*j**4-17*j*j+1021}
    if kind not in polys:raise ValueError(kind)
    p=permutation_spectrum(n)
    q=phase_ratio_spectrum(n,polys[kind])
    L=n//8
    assert p[1] == 4, (n,p[1])
    assert all(count%8==0 for count in q.values()),(n,kind,q)
    return {'n':n,'mask':kind,'L':L,
            'primitive_L_eigenvalue_multiplicity_in_P9':p[1],
            'all_phase_ratio_eigenvalue_multiplicities_divisible_by_8':True,
            'p9_number_of_cycles':len(cycle_lengths(n)),
            'impossible_single_polynomial_mask_sandwich':True}


if __name__=='__main__':
    import json
    print(json.dumps([invariant(n,kind) for n in (16,32,64,128,256,1024)
                      for kind in ('linear','quadratic','cubic','quintic')],indent=2))
