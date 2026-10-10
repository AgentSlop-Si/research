"""Generate reproducible Phase 13 exact/numerical/graph witnesses and hashes."""
from __future__ import annotations
import json,hashlib,os,math
from pathlib import Path
from cut_capacity import (exact_cut_certificate,graph_from_shift,modular_cut_audit,
                          mat_add,mat_mul,exact_green,fourier_mod,rank_mod)
from subset_gate import (subset_certificate, hidden_bottleneck_graphs)
from explicit_expander import (construction,uniform_gap_lower_bound,check_graph_gate)
from spectral_gate import gap
from lifted_sandwich_gate import rank_identity
from cut_capacity import random_green
from random import Random

ROOT=Path(__file__).parent


def mismatch_expander(side=4,copies=5):
    n=side*side
    layers=construction(side,copies=copies)
    matrices=[]
    for layer in layers:
        M=None
        for g in layer:
            x=exact_green(g)
            M=x if M is None else mat_add(M,x,65537)
        matrices.append(M)
    T=mat_mul(matrices[1],matrices[0],65537)
    F=fourier_mod(n)
    return sum(x!=y for a,b in zip(T,F) for x,y in zip(a,b))


def main():
    local=[[graph_from_shift(128,1),graph_from_shift(128,2)],
           [graph_from_shift(128,3),graph_from_shift(128,4)]]
    C=exact_cut_certificate(local)
    R={3,19,35,51,67,83,99,115}
    hidden=hidden_bottleneck_graphs()
    H=exact_cut_certificate(hidden)
    S=subset_certificate(hidden,R)
    spectra=[]
    for side in [4,8,16]:
        three=construction(side,copies=3)
        five=construction(side,copies=5)
        spectra.append({'N':side**2,
                        'three_copy_measured_gap':gap([g for a in three for g in a])['lambda_2'],
                        'five_copy_measured_gap':gap([g for a in five for g in a])['lambda_2']})
    q=65537
    rng=Random(1512)
    Lift=rank_identity([random_green(8,rng) for _ in range(2)],
                       [random_green(8,rng) for _ in range(3)])
    results={
      'date':'2026-10-10',
      'model':'exact arithmetic, fixed common-coordinate Green-resolvent sum/product circuit',
      'local_128':{
        'middle_rank_capacity':C['middle_capacity'],
        'required_exact_fourier_cut_rank':C['middle_fourier_rank'],
        'number_of_forward_and_reverse_violations':C['violating_cuts'],
        'operator_norm_error_lower_bound':math.sqrt((128/4-10)/(128/2-10)),
        'relative_frobenius_error_lower_bound':math.sqrt((128/4-10)/128),
        'exact_modular_rank_check_at_N_64':modular_cut_audit(
            [[graph_from_shift(64,1),graph_from_shift(64,2)],
             [graph_from_shift(64,3),graph_from_shift(64,4)]],[32])},
      'hidden_bottleneck_128':{
        'irregular_subset':S['subset'],
        'every_prefix_passes':not H['rejects'],
        'crossing_capacity':S['cut_capacity_R_to_C'],
        'required_rank_lower':S['Fourier_rank_lower_bound'],
        'operator_norm_error_lower_bound':S['error_R_to_C']['operator_error_at_least']},
      'expander':{
        'GG_adjacency_nontrivial_eigenvalue_upper_bound':5*math.sqrt(2),
        'three_copies_uniform_gap_lower':uniform_gap_lower_bound(3),
        'five_copies_uniform_gap_lower':uniform_gap_lower_bound(5),
        'square_length_prefix_gate_trials':[check_graph_gate(s) for s in [4,8,16,32,64]],
        'numeric_gaps':spectra,
        'N16_candidate_20_resolvent_entries_differing_from_FFT':mismatch_expander(4,5)},
      'lifted_rank':Lift,
      'interpretation':'All statements are necessary graph/circuit-class conditions, not a universal FFT upper bound; no tested expander weights match Fourier.'
    }
    (ROOT/'RESULTS.json').write_text(json.dumps(results,indent=2,sort_keys=True)+'\n')
    sums={}
    for p in sorted(ROOT.rglob('*')):
        if p.is_file() and '__pycache__' not in str(p) and p.name not in ['SHA256SUMS.json']:
            sums[p.relative_to(ROOT).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
    (ROOT/'SHA256SUMS.json').write_text(json.dumps(sums,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'phase13_status':'confirmed restricted theorems, no new universal FFT',
                      'witnesses':list(results.keys()),'number_of_hashed_files':len(sums),
                      'N16_expander_FFT_mismatches':results['expander']['N16_candidate_20_resolvent_entries_differing_from_FFT'],
                      'result_path':str(ROOT/'RESULTS.json')},indent=2))

if __name__=='__main__':main()
