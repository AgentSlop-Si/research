"""Deterministic floating implementation checks, not certified error proofs."""
import itertools
import json
import math
from pathlib import Path
import numpy as np
from energy_pruned import energy_pruned_fft,ideal_split_volume_bound


def checked_case(x,epsilon,reference=None):
    n=len(x)
    y,stats=energy_pruned_fft(x,epsilon)
    scale=float(max(np.max(np.abs(np.real(x)),initial=0.0),
                    np.max(np.abs(np.imag(x)),initial=0.0)))
    if scale==0:
        assert not np.any(y)
        error=0.0
    else:
        scaled=(np.real(x)/scale)+1j*(np.imag(x)/scale)
        ref=np.fft.fft(scaled,norm='ortho') if reference is None else reference/scale
        error=float(np.max(np.abs(y/scale-ref))/np.linalg.norm(scaled))
        allowance=128*np.finfo(float).eps*max(1,n.bit_length()-1)
        assert error<=epsilon+allowance,(n,epsilon,error,allowance)
        # Away from the floating rounding band, this is the exact hard-threshold
        # mask, not merely an arbitrary approximation within the error budget.
        norm=float(np.linalg.norm(scaled))
        heavy=np.abs(ref)>(epsilon+allowance)*norm
        light=np.abs(ref)<max(0.0,epsilon-allowance)*norm
        recovered=y/scale
        assert np.all(np.abs(recovered[heavy]-ref[heavy])<=allowance*norm)
        if epsilon>0:
            assert np.all(recovered[light]==0)
    assert stats['returned_output_count']==n
    assert stats.get('computed_output_count',0)+stats.get('pruned_output_count',0)==n
    if 0<epsilon<1:
        actual=stats.get('split_value_volume',0)
        bound=ideal_split_volume_bound(n,epsilon)
        # For these finite checks, floating comparison errors never violate the
        # ideal-arithmetic aggregate work certificate.
        assert actual<=bound+1e-8,(n,epsilon,actual,bound)
        if not stats.get('all_zero_input'):
            assert stats['norm_value_volume']==n+actual
    return error,stats


def main():
    rng=np.random.default_rng(20261009)
    totals=dict(exhaustive_inputs=0,direct_dft_cases=0,adversarial_cases=0,
                scaling_cases=0,validation_cases=0)
    records=[]
    # All 655 complex vectors from this explicit alphabet at N=1,2,4.
    alphabet=(0,1,-1,1j,-1j)
    for n in (1,2,4):
        indices=np.arange(n)
        matrix=np.exp((-2j*np.pi/n)*np.outer(indices,indices))/math.sqrt(n)
        for values in itertools.product(alphabet,repeat=n):
            x=np.asarray(values,dtype=np.complex128)
            ref=matrix@x
            for epsilon in (0,.1,.5,.9,1):
                checked_case(x,epsilon,ref)
                totals['direct_dft_cases']+=1
            totals['exhaustive_inputs']+=1
    # Full basis columns, random complex vectors, and direct O(N^2) DFT oracle.
    for n in (2,4,8,16,32,64):
        indices=np.arange(n)
        matrix=np.exp((-2j*np.pi/n)*np.outer(indices,indices))/math.sqrt(n)
        vectors=[]
        for j in range(n):
            x=np.zeros(n,dtype=complex);x[j]=1
            vectors.extend((x,1j*x))
        vectors.extend(rng.normal(size=n)+1j*rng.normal(size=n) for _ in range(3))
        for x in vectors:
            ref=matrix@x
            for epsilon in (.05,.25,.75):
                checked_case(x,epsilon,ref)
                totals['direct_dft_cases']+=1
    for n in (64,256,1024,4096):
        j=np.arange(n)
        examples={
            'zero':np.zeros(n,dtype=complex),
            'impulse':np.eye(1,n,0,dtype=complex).reshape(n),
            'constant':np.ones(n,dtype=complex),
            'alternating':(-1.0)**j+0j,
            'pure_tone':np.exp(2j*np.pi*7*j/n),
            'gaussian':rng.normal(size=n)+1j*rng.normal(size=n),
            'near_constant':np.ones(n)+1e-12*(rng.normal(size=n)+1j*rng.normal(size=n)),
        }
        for epsilon in (.05,.125,.25,.5):
            # Equal Fourier tones just below/at/above the 1/epsilon^2 cutoff.
            for delta in (-1,0,1):
                support=max(1,min(n,round(epsilon**-2)+delta))
                spectrum=np.zeros(n,dtype=complex)
                chosen=rng.choice(n,size=support,replace=False)
                spectrum[chosen]=np.exp(1j*rng.uniform(-np.pi,np.pi,support))/math.sqrt(support)
                examples[f'boundary_tones_{epsilon}_{delta}']=np.fft.ifft(spectrum,norm='ortho')
            for name,x in examples.items():
                error,stats=checked_case(x,epsilon)
                totals['adversarial_cases']+=1
                records.append(dict(n=n,epsilon=epsilon,family=name,error_ratio=error,
                    split_volume=stats.get('split_value_volume',0),
                    norm_value_volume=stats.get('norm_value_volume',0),
                    full_fft_split_volume=n*(n.bit_length()-1),
                    computed_outputs=stats.get('computed_output_count',0),
                    pruned_outputs=stats.get('pruned_output_count',0)))
    for magnitude in (1e-300,1e-200,1e200,1e300):
        x=magnitude*(rng.normal(size=128)+1j*rng.normal(size=128))
        for epsilon in (0,.125,.5):
            checked_case(x,epsilon)
            totals['scaling_cases']+=1
    invalid=[([],0.1),([1,2,3],0.1),([float('inf'),0],.1),
             ([1,2],-1),([1,2],float('nan'))]
    for x,epsilon in invalid:
        try: energy_pruned_fft(x,epsilon)
        except ValueError: totals['validation_cases']+=1
        else: raise AssertionError('invalid argument accepted')
    result=dict(status='PASS',theorem_model='ideal arithmetic and exact norms',
        prototype='complex128; observed error uses explicit rounding allowance, not a certified bound',
        counts=totals,max_adversarial_error_ratio=max(r['error_ratio'] for r in records),
        adversarial_records=records)
    out=Path(__file__).parent/'results';out.mkdir(exist_ok=True)
    (out/'audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='adversarial_records'},indent=2))


if __name__=='__main__': main()
