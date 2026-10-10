"""Deterministic head + energy-pruned tail at eps*||x||_1/sqrt(N).

Ideal-arithmetic proof is in README. complex128 is a numerical prototype,
not a floating-point error certificate. Classical sparse-head decomposition.
"""
import heapq
import math
import numpy as np
from prior_energy_pruned import energy_pruned_fft


def sparse_head_fft(n, entries):
    """All outputs; h-sparse input, O(N[1+log(h+1)]) classical arithmetic."""
    h = len(entries)
    if h == 0:
        return np.zeros(n, dtype=complex), {'head_support': 0,
            'head_radix': 1, 'head_fft_butterflies': 0, 'head_phase_terms': 0}
    b = 1 << (h-1).bit_length()
    m = n//b
    values = np.zeros((m,b), dtype=complex)
    q = np.arange(m)
    residues = set()
    for j, value in entries:
        r, t = j % b, j//b
        values[:,r] += value*np.exp((-2j*np.pi*t/m)*q)
        residues.add(r)
    for r in residues:
        values[:,r] *= np.exp((-2j*np.pi*r/n)*q)
    result = np.fft.fft(values, axis=1).T.reshape(n)/math.sqrt(n)
    return result, {'head_support': h, 'head_radix': b,
        'head_fft_butterflies': n*(b.bit_length()-1)//2,
        'head_phase_terms': m*h, 'head_twiddle_terms': m*len(residues),
        'head_dense_initialization_writes': n, 'head_output_writes': n}


def head_energy_fft(values, epsilon, head_size=0):
    x = np.asarray(values, dtype=complex)
    n = len(x)
    if x.ndim != 1 or n < 1 or n & (n-1):
        raise ValueError('need power-of-two one-dimensional input')
    if not np.all(np.isfinite(x)) or not math.isfinite(epsilon) or epsilon <= 0:
        raise ValueError('need finite input and positive finite epsilon')
    if not isinstance(head_size, int) or not 0 <= head_size <= n:
        raise ValueError('head_size must be an integer in [0,N]')
    magnitudes = np.abs(x)
    norm_one = float(np.sum(magnitudes))
    # Deterministic heap selection; O(N log(h+2)), no full sort of N values.
    indices = heapq.nlargest(head_size, range(n), key=lambda j: (magnitudes[j],-j))
    entries = [(j,x[j]) for j in indices if x[j] != 0]
    tail = x.copy()
    tail[indices] = 0
    threshold = epsilon*norm_one/math.sqrt(n)
    norm_tail = float(np.linalg.norm(tail))
    head_out, stats = sparse_head_fft(n, entries)
    if norm_tail == 0:
        tail_out = np.zeros(n, dtype=complex)
        tail_stats = {'split_value_volume':0, 'butterflies':0, 'zero_tail':True}
    else:
        tail_out, tail_stats = energy_pruned_fft(tail, threshold/norm_tail)
    stats.update({'n':n, 'head_requested':head_size, 'input_scan_values':n,
                  'tail_copy_values':n, 'head_selection_method':'deterministic heap',
                  'norm_one':norm_one, 'tail_energy':norm_tail**2,
                  'requested_threshold':threshold, 'output_additions':n,
                  'tail':tail_stats,
                  'total_butterflies':stats['head_fft_butterflies']+
                      tail_stats.get('butterflies',0)})
    return head_out+tail_out, stats


def adversary_prefix_certificate(m, h, eps_numerator=1, eps_denominator=4):
    """Exact integer cost certificate for N=4^m, support [0,2^m).

    Counts head backend butterflies and tail butterflies forced in the first
    m levels. No numerical transform or floating norm comparison is used.
    """
    n, s = 4**m, 2**m
    if not 0 <= h <= s:
        raise ValueError('head size outside nonzero support')
    b = 1 << (max(1,h)-1).bit_length()
    head = n*(b.bit_length()-1)//2
    tail_levels = sum((s-h)*eps_denominator**2 >
                      eps_numerator**2*(2**d) for d in range(m))
    tail = n*tail_levels//2
    return {'m':m, 'n':n, 'support':s, 'head':h,
            'head_butterflies':head, 'forced_tail_prefix_levels':tail_levels,
            'forced_tail_butterflies':tail,
            'certified_total_lower_bound':head+tail,
            'universal_hybrid_lower_bound':n*m//2}
