"""End-to-end fresh dense input checks for the approximate construction.

NumPy FFT is used only as an independent reference / timing comparator.
Tables are eagerly, fully built per N; no lazy row cache is used. A plan is
reused for test efficiency, but each reported cold-call cost includes all
table setup. These small examples exercise correctness, not asymptotic tuning.
"""
import hashlib
import json
from math import cos, sin, pi
from pathlib import Path
from random import Random
import sys
from time import perf_counter
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent/'fft_wordram_decoder_research'))
from guarded_decoder import GuardedDecoder
from sampling import sample_atoms, sample_count, sample_count_integer, exact_atom_probabilities


def workload(name, n):
    r = Random(712+n)
    if name == 'flat':
        return [(97, -31)]*n
    if name == 'gaussian':
        return [(round(r.gauss(0,100)), round(r.gauss(0,100))) for _ in range(n)]
    if name == 'random_phase':
        angles = [2*pi*r.random() for _ in range(n)]
        return [(round(100*cos(a)), round(100*sin(a))) for a in angles]
    if name == 'power_law':
        return [(round(10000/(j+1)**0.8)*r.choice((-1,1)),
                 round(5000/(j+1)**0.7)*r.choice((-1,1))) for j in range(n)]
    if name == 'spike_noise':
        x = [(r.randrange(-10,11), r.randrange(-10,11)) for _ in range(n)]
        x[n//3] = (1000*n, -700*n)
        return x
    if name == 'dense_tone':
        return [(round(1000*cos(2*pi*7*j/n)), round(1000*sin(2*pi*7*j/n))) for j in range(n)]
    if name == 'tone_mixture':
        v = [(700*cos(2*pi*3*j/n)+400*cos(2*pi*11*j/n),
              700*sin(2*pi*3*j/n)-400*sin(2*pi*11*j/n)) for j in range(n)]
        return [(round(a)+r.randrange(-20,21), round(b)+r.randrange(-20,21)) for a,b in v]
    if name == 'cancelling_comb':
        return [((100 if j%2 else -100)+(150 if j%7==0 else 0),
                 71 if j%3 else -142) for j in range(n)]
    raise ValueError(name)


def check_sampler():
    from fractions import Fraction
    x = [(3,-5),(-7,11),(0,0)]
    dist = exact_atom_probabilities(x)
    expected = [0j]*len(x)
    for j, phase, prob in dist:
        expected[j] += complex((1j)**phase)*float(prob)*26
    assert expected == [complex(*v) for v in x]
    assert sum(p for j,phase,p in dist) == Fraction(1)
    single = sample_atoms([(0,0),(-1,0)],100,seed=71)
    assert single['samples'] == [(1,2)]*100
    assert not single['failed']
    zero = sample_atoms([(0,0)]*3,100)
    assert zero['mass'] == 0 and not zero['samples'] and not zero['failed']
    invalid = 0
    for bad in [[(1.2,0)],[(1,)],[(1,True)]]:
        try:
            sample_atoms(bad,10)
        except ValueError:
            invalid += 1
    assert invalid == 3
    for n in (4,31,1000,65537):
        delta = Fraction(1,n*n)
        count = sample_count_integer(n,Fraction(1,4),delta,7)
        assert count >= sample_count(n,0.25,float(delta),7)
        assert count % 7 == 0
    return {'exact_unbiased_small_distribution': True,
            'single_atom_and_zero': True, 'invalid_inputs_rejected': invalid,
            'integer_parameter_selection_cases':4}


def main():
    epsilon, a, delta = 0.5, 0.25, 0.02
    names = ['flat','gaussian','random_phase','power_law','spike_noise',
             'dense_tone','tone_mixture','cancelling_comb']
    records, setup = [], []
    for n in (64,257,1024):
        k = sample_count(n,a,delta/2)
        before = perf_counter()
        decoder = GuardedDecoder(n,k,block_size=4,phase_grid=64,slope_grid=256,
                                 group_size=1,lane_step_bits=5,trig_bits=24,
                                 table_mode='eager')
        setup_time = perf_counter()-before
        assert a+decoder.decoder_bound < epsilon
        setup.append({'N':n,'sample_count':k,'setup_seconds':setup_time,
                      'complete_rows':decoder.table_entries,
                      'charged_setup_operations':sum(decoder.cold_counts.values())})
        for idx,name in enumerate(names):
            x = workload(name,n)
            before = perf_counter()
            sampled = sample_atoms(x,k,seed=9101+idx+n,cap_failure=delta/2)
            assert not sampled['failed']
            sampling_seconds = perf_counter()-before
            mass = sampled['mass']
            before = perf_counter()
            answer = decoder.decode(sampled['samples'])
            decode_seconds = perf_counter()-before
            v = np.array([complex(*p) for p in x])
            before = perf_counter()
            reference = np.fft.fft(v)
            fft_seconds = perf_counter()-before
            # Materialize an independent exact-integer atom histogram, then
            # apply the reference FFT to check every surrogate coefficient.
            hist = np.zeros(n,dtype=complex)
            for j,phase in sampled['samples']:
                hist[j] += (1j)**phase
            sample_ref = np.fft.fft(hist)/k
            normalized_answer = np.array(answer['values'])
            sample_err = float(max(abs(sample_ref-reference/mass)))
            decode_err = float(max(abs(normalized_answer-sample_ref)))
            total_err = float(max(abs(normalized_answer-reference/mass)))
            assert decode_err <= answer['error_bound']+1e-12
            assert total_err <= epsilon
            assert len(answer['integer_outputs']) == n
            assert answer['counts']['online']['output_write'] == 2*n
            assert answer['counts']['max_operand_bits'] <= answer['parameters']['word_bits']
            # All numerators and common denominator are explicit; multiplication
            # by mass produces actual unnormalized rational output coordinates.
            rational_numerators = [(u*mass,v*mass) for u,v in answer['integer_outputs']]
            assert len(rational_numerators) == n
            numerator_bits = max(abs(z).bit_length() for pair in rational_numerators for z in pair)
            assert numerator_bits+1 <= answer['parameters']['word_bits']
            records.append({'N':n,'workload':name,'sample_count':k,'mass':mass,
                            'sampling_error_over_mass':sample_err,
                            'decoder_error_over_mass':decode_err,
                            'total_error_over_mass':total_err,
                            'allowed_total_error_over_mass':epsilon,
                            'decoder_error_bound':answer['error_bound'],
                            'largest_true_coefficient_over_mass':float(max(abs(reference))/mass),
                            'sampling_seconds':sampling_seconds,
                            'decode_seconds':decode_seconds,
                            'cold_setup_plus_sampling_and_decode_seconds':setup_time+sampling_seconds+decode_seconds,
                            'reference_numpy_fft_seconds':fft_seconds,
                            'online_counted_decoder_operations':sum(answer['counts']['online'].values()),
                            'cold_counted_decoder_operations':sum(decoder.cold_counts.values())+sum(answer['counts']['online'].values()),
                            'output_scaling_integer_multiplications':2*n,
                            'max_scaled_output_numerator_bits':numerator_bits,
                            'sampler_counts':sampled['counts'],
                            'parameters':answer['parameters'],
                            'all_outputs_checked':True})
    result = {'status':'PASS','scope':'finite-word randomized global-additive approximation; not exact FFT',
              'epsilon':epsilon,'sampling_error_allocation':a,'failure_bound':delta,
              'sampler_checks':check_sampler(),'fresh_cases':len(records),
              'checked_coefficients':sum(r['N'] for r in records),
              'max_observed_total_error_over_mass':max(r['total_error_over_mass'] for r in records),
              'timing_note':'Table built once per N for audit efficiency; every cold-call cost/timing adds entire setup. Python implementation is not faster than NumPy FFT. B=4,g=1 finite demonstrations do not use the asymptotic parameter schedule.',
              'setup':setup,'records':records,
              'source_sha256':{str(p.relative_to(HERE.parent)):hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in [HERE/'sampling.py',HERE/'run_audit.py',HERE.parent/'fft_wordram_decoder_research/guarded_decoder.py']}}
    (HERE/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','fresh_cases','checked_coefficients','max_observed_total_error_over_mass']}))


if __name__ == '__main__':
    main()
