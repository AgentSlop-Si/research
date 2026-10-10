"""Universal all-length phase-12 obstruction via Schur-positive Fourier minors.

For any n > 2*(k-1)*(B-k)*(B-1), ALL k x k minors of the top-left
B x B block of the complex n-DFT are nonzero. This follows from the
bialternant/Vandermonde formula and nonnegative coefficients of Schur
polynomials. No prime-length assumption is needed.

Combined with iterated Erdos-Szekeres and independent quasi-separable
orderings of r Green inverses, this excludes one sum of r resolvents
(and optional rank-t/row-sparse corrections) above an explicit n bound.
"""
from __future__ import annotations
import math
import random


def top_left_fourier_full_minors_threshold(B:int,k:int)->int:
    """If N>this value, every k x k minor in indices [0,B) is nonzero."""
    if not 2<=k<=B:raise ValueError('2<=k<=B required')
    return 2*(k-1)*(B-k)*(B-1)


def common_order_size(r:int,k:int,sparse_row_degree:int=0)->int:
    if r<1 or k<2 or sparse_row_degree<0:raise ValueError
    target=k*(sparse_row_degree+2)
    return (target-1)**(2**(r-1))+1


def green_sum_no_go_threshold(r:int,rank_correction:int=0,sparse_row_degree:int=0)->dict:
    """For n>n0, no length-n DFT equals sum of r Green inverses
    plus rank<=rank_correction and row-degree<=sparse_row_degree corrections.
    Applies to independent arbitrary (multi-cycle) monomial permutations.
    This DOES NOT apply to products of such sums or arbitrary graph operators.
    """
    k=r+rank_correction+1
    B=common_order_size(r,k,sparse_row_degree)
    n0=top_left_fourier_full_minors_threshold(B,k)
    return {'green_summands':r,'low_rank_correction':rank_correction,
            'sparse_row_degree_correction':sparse_row_degree,
            'required_minor_size':k,'test_grid_size':B,
            'all_N_strict_threshold':n0,
            'smallest_excluded_N':n0+1}


def three_minor_schur_lower_bound(N:int, rows, cols, dps:int=80)->tuple[float,float]:
    """Return high-precision |det Fourier minor| and proved lower bound.
    Independent numerical audit of the exact Schur small-arc theorem.
    Provided only when the angle-bound is strict, not as a proof tool.
    """
    import mpmath as mp
    assert len(rows)==len(cols)==3
    rr=sorted(rows);cc=sorted(cols)
    a=rr[1]-rr[0];b=rr[2]-rr[0]
    d=a+b-3
    with mp.workdps(dps):
        phases=[2*mp.pi*c/N for c in cc]
        z=[mp.e**(1j*ph) for ph in phases]
        A=mp.matrix([[z[j]**int(i) for j in range(3)]for i in rr])
        measured=abs(mp.det(A))
        vand=mp.fprod(abs(z[j]-z[i]) for i in range(3) for j in range(i+1,3))
        tableau_at_ones=mp.mpf(a)*b*(b-a)/2
        span=d*(phases[-1]-phases[0])
        if span>=mp.pi:raise ValueError('outside certified small arc')
        lower=vand*tableau_at_ones*mp.cos(span/2)
        assert lower>0
        return float(measured),float(lower)


def numerical_audit(N:int=2301,B:int=26,k:int=3,samples:int=120,seed:int=19)->dict:
    assert N>top_left_fourier_full_minors_threshold(B,k)
    assert k==3
    rng=random.Random(seed)
    ratios=[]
    for _ in range(samples):
        rr=rng.sample(range(B),3);cc=rng.sample(range(B),3)
        measured,lower=three_minor_schur_lower_bound(N,rr,cc)
        ratios.append(measured/lower)
        assert measured+max(measured,lower)*1e-12>=lower
    return {'n':N,'B':B,'k':k,'samples':samples,
            'min_measured_over_analytical_lower_bound':min(ratios),
            'max_measured_over_analytical_lower_bound':max(ratios),
            'strict_nonzero_analytical':True}


if __name__=='__main__':
    import json
    for r in [1,2,3,4]:
        print(json.dumps(green_sum_no_go_threshold(r)))
    for n in [2301,4096,8192]:
        print(json.dumps(numerical_audit(n)))
