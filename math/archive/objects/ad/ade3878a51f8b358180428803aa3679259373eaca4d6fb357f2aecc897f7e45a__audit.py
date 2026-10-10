"""Independent check, exact equality and observational costs. No hidden free macros."""
from __future__ import annotations
import json
import math
from pathlib import Path
from random import Random
from statistics import median
from time import perf_counter

from global_bottleneck import P, packed_dft, ntt_reference, packing_possible, block_digits
from tests.test_rank_barrier import fourier_matrix, rank_mod

ROOT=Path(__file__).resolve().parent


def audit():
    rng=Random(20261009)
    records=[]
    for n in (64,256,1024,4096,16384):
        samples=[[rng.randrange(0,P) for _ in range(n)] for j in range(5)]
        observations=[]
        times_pack=[]
        times_ntt=[]
        for inp in samples:
            t=perf_counter(); got,model=packed_dft(inp); times_pack.append((perf_counter()-t)*1000)
            t=perf_counter(); expected=ntt_reference(inp);times_ntt.append((perf_counter()-t)*1000)
            assert got==expected
            observations.append(model)
        rec={
            'N':n,'correct_all':True,
            'field_modulus':P,'constant_root_modulus':True,
            'cell_bits':observations[0].cell_bits,
            'each_packed_operand_bits':observations[0].operand_bits,
            'naive_scalar_mult_calls':1,
            'critical_note':'big integer multiplication NOT unit cost: M(N * cell_bits) bit work',
            'packed_median_ms':round(median(times_pack),3),
            'python_ntt_median_ms':round(median(times_ntt),3),
            'relative_packed_speed':round(median(times_ntt)/median(times_pack),3),
        }
        records.append(rec)
    # Rigorous exact grid-capacity cases: geometric lower bound on decoder L.
    sample_bounds=[]
    for n,w in [(64,6),(256,8),(1024,10),(4096,12)]:
        exact_L_gt=(2**(n/(2*w))-2)/4
        # Width/condition lower bound: L > max(0, (2^(N/(2w))-2)/(4M)), with M=1.
        sample_bounds.append({'N':n,'w':w,'M':1,
            'necessary_decoder_L_greater_than':round(exact_L_gt,4),
            'min_bits_log2_L_approximately':round(math.log2(exact_L_gt),3),
            'check_small_L_rejected':not packing_possible(n,w,1,1)})
    # Known w=N/b encoder gets exponential L, sharp (up to constants).
    block_cases=[]
    for n,b in ((16,4),(64,8),(256,16),(1024,64)):
        block_cases.append({'N':n,'width':n//b,'bits_per_register':b,
                            'constructive_L_at_least':2**b})
    result={'date':'2026-10-09','scope':'one fresh exact modular DFT per call; all N outputs; no cached inputs',
            'backend':'Python one-bigint multiplication vs independent Python radix-2 NTT; no claimed universal performance superiority',
            'packed_dft':records,
            'nonlinear_compression_general_bound':'2**N <= (ceil(4*M*L/(1-2*epsilon))+1)**(2*w)',
            'bottleneck_lower_bounds':sample_bounds,
            'explicit_block_encoder':block_cases,
            'jacobian_bottleneck':'for arbitrary complex domain smooth E:C^N->C^w, D:C^w->C^N, D(E(x))=F_N x implies w>=N',
            'exact_fourier_matrix_rank_32':rank_mod(fourier_matrix(32)),
            'warning':'Bit complexity and local conditioning prevent a false O(N) DFT conclusion.'}
    (ROOT/'audit_results_run.json').write_text(json.dumps(result,indent=2)+'\n')
    for rec in records:
        print(f"N={rec['N']:>5}  integer operand bits={rec['each_packed_operand_bits']:>8}  "
              f"one big multiply, correct={rec['correct_all']}  "
              f"packed_ms={rec['packed_median_ms']:.3f}  python_ntt_ms={rec['python_ntt_median_ms']:.3f}")
    print('Rank check for N=32:',result['exact_fourier_matrix_rank_32'])
    for row in sample_bounds:
        print(f"N={row['N']:>5} with width={row['w']:>2}: required L > {row['necessary_decoder_L_greater_than']:.3g}")
    print('JSON:',ROOT/'audit_results_run.json')

if __name__=='__main__':audit()
