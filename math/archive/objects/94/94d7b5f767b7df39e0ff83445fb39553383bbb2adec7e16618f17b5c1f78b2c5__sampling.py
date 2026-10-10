"""Finite-integer signed atom sampler; no arbitrary real RAM operations.

Coordinates are pairs of signed integers, optionally sharing a fixed denominator.
Phase encoding: 0=+1, 1=+i, 2=-1, 3=-i. No floating input is silently accepted.
The rejection cap gives a declared failure event; it never biases accepted atoms.
"""
from bisect import bisect_right
from math import ceil, log
from random import Random
from fractions import Fraction


def sample_count(n, sampling_error, failure, group_size=1):
    """Union bound: P(max complex error > a) <= 4n exp(-k a^2/4)."""
    if n < 1 or not 0 < sampling_error < 1 or not 0 < failure < 1:
        raise ValueError('invalid sampling parameters')
    if type(group_size) is not int or group_size < 1:
        raise ValueError('group_size must be positive')
    k = ceil(4 * log(4*n/failure) / sampling_error**2)
    return ((k + group_size - 1)//group_size)*group_size


def sample_count_integer(n, sampling_error, failure, group_size=1):
    """Conservative uniform count from exact rational parameters, no logarithm.

    ceil(log2(4n/failure)) >= ln(4n/failure). Fixed dyadic error and a
    polynomial failure denominator require O(log n)-bit integer operations.
    """
    error, delta = Fraction(sampling_error), Fraction(failure)
    if n < 1 or not 0 < error < 1 or not 0 < delta < 1:
        raise ValueError('invalid sampling parameters')
    if type(group_size) is not int or group_size < 1:
        raise ValueError('group_size must be positive')
    ratio = Fraction(4*n,1)/delta
    upper_integer = (ratio.numerator+ratio.denominator-1)//ratio.denominator
    log_upper = (upper_integer-1).bit_length()
    rational_k = 4*log_upper/(error*error)
    k = (rational_k.numerator+rational_k.denominator-1)//rational_k.denominator
    return ((k+group_size-1)//group_size)*group_size


def sample_atoms(coordinates, k, *, seed=0, cap_failure=1e-9):
    if type(k) is not int or k < 1 or not 0 < cap_failure < 1:
        raise ValueError('invalid sampling parameters')
    rng = Random(seed)
    cumulative, labels = [], []
    total = 0
    for j, pair in enumerate(coordinates):
        if len(pair) != 2 or any(type(v) is not int for v in pair):
            raise ValueError('coordinates must be pairs of Python integers')
        for part, v in enumerate(pair):
            if v:
                total += abs(v)
                cumulative.append(total)
                labels.append((j, part + (2 if v < 0 else 0)))
    if total == 0:
        return {'samples': [], 'mass': 0, 'failed': False,
                'counts': {'input_coordinates': len(coordinates),
                           'random_words': 0, 'binary_search_comparison_bound': 0,
                           'rejection_cap': 0, 'mass_bits': 0}}
    # cap >= log2(k/cap_failure), conservatively computed via an integer ratio.
    numerator, denominator = Fraction(cap_failure).as_integer_ratio()
    ratio_ceiling = (k*denominator + numerator - 1)//numerator
    cap = max(1, (ratio_ceiling-1).bit_length())
    bits = (total-1).bit_length()
    random_words = 0
    samples = []
    for _ in range(k):
        for attempt in range(cap):
            ticket = rng.getrandbits(bits)
            random_words += 1
            if ticket < total:
                samples.append(labels[bisect_right(cumulative, ticket)])
                break
        else:
            return {'samples': samples, 'mass': total, 'failed': True,
                    'counts': {'input_coordinates': len(coordinates),
                               'random_words': random_words,
                               'binary_search_comparison_bound': len(samples)*len(cumulative).bit_length(),
                               'rejection_cap': cap, 'mass_bits': total.bit_length()}}
    return {'samples': samples, 'mass': total, 'failed': False,
            'counts': {'input_coordinates': len(coordinates),
                       'random_words': random_words,
                       'binary_search_comparison_bound': k*len(cumulative).bit_length(),
                       'rejection_cap': cap, 'mass_bits': total.bit_length()}}


def exact_atom_probabilities(coordinates):
    """Reference only: Fraction probabilities for small independent checks."""
    from fractions import Fraction
    mass = sum(abs(r)+abs(i) for r, i in coordinates)
    if not mass:
        return []
    return [(j, part+(2 if v < 0 else 0), Fraction(abs(v), mass))
            for j, pair in enumerate(coordinates)
            for part, v in enumerate(pair) if v]
