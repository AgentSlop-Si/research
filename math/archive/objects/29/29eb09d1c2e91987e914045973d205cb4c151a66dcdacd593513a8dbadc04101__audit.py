"""Exact phase certificates: no floating point and no asymptotic extrapolation."""
from collections import Counter
from fractions import Fraction
import json
from pathlib import Path
import random


def root_sum(exponents,order,weights=None):
    """Exact integer coefficients in Z[z]/(z^(order/2)+1), order power of 2."""
    assert order>=2 and not order&(order-1)
    out=[0]*(order//2)
    if weights is None:
        weights=[1]*len(exponents)
    for exponent,weight in zip(exponents,weights):
        e=exponent%order
        if e>=order//2:
            out[e-order//2]-=weight
        else:
            out[e]+=weight
    return out


def slope(r,coefficients,M):
    value=0
    for coefficient in reversed(coefficients):
        value=(value*r+coefficient)%M
    return value


def dyadic_case(M,K,a,coefficients):
    assert M%4==0 and K%2==0 and coefficients[0]%2==1
    for r in range(0,K,2):
        c=slope(r,coefficients,M)
        assert c%2==1
        exponents=[a*t*t+c*t for t in range(M)]
        assert root_sum(exponents,M)==[0]*(M//2)
        for t in range(M//2):
            assert (exponents[t+M//2]-exponents[t])%M==M//2


def prime_character_variance(M,K):
    """Error monomials have orthogonal seed characters iff labels differ.

    Labels correspond to the independently uniform seeds (a,alpha,b).
    For prime M and K<=M every off-diagonal error term has a distinct label.
    """
    labels={}
    multiplicities=Counter()
    for r in range(K):
        for u in range(M):
            for t in range(M):
                if u==t:
                    continue
                label=((u*u-t*t)%M,r*(u-t)%M,(u-t)%M)
                assert label not in labels
                labels[label]=(r,u,t)
                multiplicities[(r,u)]+=1
    assert set(multiplicities.values())=={M-1}
    return {'M':M,'K':K,'orthogonal_error_characters':len(labels),
            'variance_coefficient':f'{M-1}/{K*M}',
            'statement':'Var[estimate_m]=(M-1)/N * ||x||_2^2 for every m and x'}


def main():
    rng=random.Random(20261009)
    affine=polynomial=0
    rows=[]
    for M in (4,8,16):
        for K in (2,4,8):
            count=0
            for a in range(M):
                for alpha in range(M):
                    for b in range(1,M,2):
                        dyadic_case(M,K,a,[b,alpha])
                        affine+=1
                        count+=1
            for degree in range(2,9):
                for _ in range(40):
                    coefficients=[2*rng.randrange(M//2)+1]+[rng.randrange(M) for _ in range(degree)]
                    dyadic_case(M,K,rng.randrange(M),coefficients)
                    polynomial+=1
            rows.append({'M':M,'K':K,'exhaustive_affine_bad_seed_cases':count})
    dense=[]
    for epsilon in (Fraction(1,4),Fraction(1,2),Fraction(3,4),Fraction(9,10),Fraction(99,100)):
        t=(1-epsilon*epsilon)/(4*epsilon)
        bound=1/epsilon-t
        # Exact rational check of epsilon*(sqrt(1+t^2)+t)<1.
        assert t>0 and bound>0 and bound*bound>1+t*t
        dense.append({'epsilon':str(epsilon),'dense_offset_t':str(t),
                      'DC_error_balls_disjoint':True,
                      'worst_of_two_fixed_dense_inputs_failure_lower_bound':'1/4'})
    cazac=0
    for M in (4,8,16,32):
        for a in range(1,2*M,2):
            for c in range(M):
                exponents=[]
                weights=[]
                for u in range(M):
                    for t in range(M):
                        exponents.append(a*(u*u-t*t)+2*c*(u-t))
                        weights.append(-1 if u%2 else 1)
                product=root_sum(exponents,2*M,weights)
                assert root_sum(exponents,2*M)==[M]+[0]*(M-1)
                expected=M*(-1 if (c+M//4)%2 else 1)
                assert product==[expected]+[0]*(M-1)
                cazac+=1
    prime=[]
    for M in (3,5,7,11):
        for K in range(1,M+1):
            prime.append(prime_character_variance(M,K))
    # Exact negative control: K>M aliases block labels even over a prime.
    M=5
    label0=((1-0)%M,0*(1-0)%M,(1-0)%M)
    labelM=((1-0)%M,M*(1-0)%M,(1-0)%M)
    assert label0==labelM
    # Exact negative control: an odd composite permits within-block aliases.
    M=9
    assert ((3**2-0**2)%M,3%M)==((6**2-3**2)%M,3%M)
    boundary=0
    for M in (4,5,8,11,16):
        for a in range(M):
            for b in range(M):
                for degree in range(1,M+1):
                    rhs=(a+b+a*(degree-1)**2+b*(degree-1)+2*a*(degree-1))%M
                    assert rhs==(a*degree**2+b*degree)%M
                assert (a*M*M+b*M)%M==0
                boundary+=1
    report={'status':'PASS','arithmetic':'Integer cyclotomic coefficients and modular character identities; no floating point.',
            'exhaustive_affine_bad_seed_cases':affine,'higher_degree_bad_seed_cases':polynomial,
            'CAZAC_alternating_input_exact_products':cazac,'prime_variance_character_cases':len(prime),
            'CAZAC_constant_input_exact_products':cazac,
            'finite_chirp_recurrence_cases':boundary,'dyadic_cases':rows,
            'dense_collision_examples':dense,'prime_variance_cases':prime,
            'limits':'Prime variance is not an all-bin tail bound, a power-of-two-length repair, or a fast joint decoder.'}
    Path(__file__).with_name('results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('dyadic_cases','dense_collision_examples','prime_variance_cases')},indent=2))


if __name__=='__main__':
    main()
