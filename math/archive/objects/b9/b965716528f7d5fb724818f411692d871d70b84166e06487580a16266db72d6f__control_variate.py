"""Exact short-period baseline plus the bounded-word approximate residual.

DFT sign is negative. Inputs/output numerators are Gaussian integers.
All input fits and residuals are formed afresh; only input-independent decoder
tables may be shared, and their cold preparation must still be charged.
"""
from math import gcd
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'fft_wordram_integration'))
from sampling import sample_atoms


def rotate(pair,phase):
    a,b=pair
    return ((a,b),(-b,a),(-a,-b),(b,-a))[phase%4]


def quarter_spectrum(sums,n):
    q=len(sums)
    if q not in (1,2,4) or n<1:
        raise ValueError('invalid short period')
    values={}
    for t in range(q):
        real=imag=0
        for s,pair in enumerate(sums):
            a,b=rotate(pair,(-4*t*s//q)%4)
            real+=a;imag+=b
        values[t*n]=(real,imag)
    return values


def fit_periodic(coordinates):
    N=len(coordinates)
    if N<1 or any(len(p)!=2 or any(type(v)is not int for v in p) for p in coordinates):
        raise ValueError('nonempty Gaussian-integer input required')
    q=gcd(N,4); n=N//q
    sums=[[0,0] for _ in range(q)]; masses=[[0,0] for _ in range(q)]; input_bits=0
    for j,pair in enumerate(coordinates):
        s=j%q
        for c,value in enumerate(pair):
            input_bits=max(input_bits,abs(value).bit_length())
            sums[s][c]+=value;masses[s][c]+=abs(value)
    costs=[[0,0] for _ in range(q)]
    for j,pair in enumerate(coordinates):
        s=j%q
        for c,value in enumerate(pair):
            costs[s][c]+=abs(n*value-sums[s][c])
    chosen=[[sums[s][c] if costs[s][c]<=n*masses[s][c] else 0 for c in range(2)] for s in range(q)]
    residual=[tuple(n*pair[c]-chosen[j%q][c] for c in range(2)) for j,pair in enumerate(coordinates)]
    mass=sum(abs(a)+abs(b) for a,b in residual)
    input_mass=sum(sum(v) for v in masses)
    assert mass<=n*input_mass
    return {'N':N,'period':q,'scale':n,'chosen_sums':chosen,'input_component_bits':input_bits,
            'input_mass':input_mass,'residual_numerator_mass':mass,
            'residual':residual,'baseline_spectrum':quarter_spectrum(chosen,n),
            'exact_corner_spectrum':quarter_spectrum(sums,n),
            'counts':{'input_validation_component_visits':2*N,
                      'fitting_component_visits':6*N,
                      'residual_mass_component_visits':2*N,
                      'short_DFT_terms':2*q*q}}


def fuse(coordinates,decoder=None,*,seed=None,cap_failure=0.01):
    """Explicit rational all-output approximation, or a flagged sampling failure.

    On a zero residual all coefficients are exact. Otherwise caller supplies
    the finite decoder configuration; its sample error allocation must be
    added to the returned deterministic decoder error bound.
    """
    fit=fit_periodic(coordinates)
    N=fit['N']; scale=fit['scale']; mass=fit['residual_numerator_mass']
    if not mass:
        out=[(0,0)]*N
        for k,pair in fit['baseline_spectrum'].items(): out[k]=pair
        return {'integer_outputs':out,'denominator':1,'exact':True,'failed':False,
                'fit':fit,'decoder_counts':None,'sampler_counts':None,
                'output_component_writes':2*N+2*fit['period'],
                'required_word_bits':fit['input_component_bits']+2*N.bit_length()+4}
    if decoder is None or decoder.N!=N:
        raise ValueError('matching prepared decoder required for nonzero residual')
    sampled=sample_atoms(fit['residual'],decoder.K,seed=seed,cap_failure=cap_failure)
    if sampled['failed']:
        return {'integer_outputs':[(0,0)]*N,'denominator':1,'exact':False,'failed':True,
                'fit':fit,'decoder_counts':None,'sampler_counts':sampled['counts'],
                'output_component_writes':2*N}
    approx=decoder.decode(sampled['samples'])
    denominator=scale*approx['denominator']
    out=[]
    for k,(a,b) in enumerate(approx['integer_outputs']):
        u,v=fit['baseline_spectrum'].get(k,(0,0))
        out.append((u*denominator+mass*a,v*denominator+mass*b))
    # These q frequencies were already computed exactly in the input scan.
    # Replacing their estimates cannot worsen the error guarantee.
    for k,(u,v) in fit['exact_corner_spectrum'].items():
        out[k]=(u*denominator,v*denominator)
    # Conservative common machine width for exact fitting and rescaling.
    # It is Theta(log N) under the stated O(log N)-bit input contract.
    required=max(decoder.w,fit['input_component_bits']+2*N.bit_length()+approx['denominator'].bit_length()+4)
    assert all(abs(z)<(1<<(required-1)) for pair in out for z in pair)
    return {'integer_outputs':out,'denominator':denominator,'exact':False,'failed':False,
            'fit':fit,'decoder_counts':approx['counts'],'sampler_counts':sampled['counts'],
            'decoder_error_over_residual_mass':approx['error_bound'],
            'required_word_bits':required,
            'output_component_writes':2*N+2*fit['period'],'extra_output_integer_operations_upper':6*N+4*fit['period']+2}
