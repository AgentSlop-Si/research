"""Phase 14: exact Galois phase-budget and cyclotomic two-stage tests.

The proof is in THEOREM.md. These tests are finite corroboration, not a
replacement for its characteristic-zero arguments.
"""
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
P13 = ROOT.parent/'fft_green_phase13_phase_coherence'
P12 = ROOT.parent/'fft_green_phase12_unitary_escape'
sys.path.insert(0, str(P13))
sys.path.insert(0, str(P12))
from unitary_mixer import MOD, UnitaryGreenMixer, rank_mod
from haar_adapter_mod import HaarEscapeMixerMod, StrongHaarEscapeMixerMod, OMEGA8


def n_power_of_two(n):
    return n >= 16 and n & (n-1) == 0


def cycle_count_multiplier(n, a=9):
    seen = bytearray(n)
    cycles = 0
    for j in range(n):
        if not seen[j]:
            cycles += 1
            k = j
            while not seen[k]:
                seen[k] = 1
                k = a*k % n
    return cycles


def cycle_count_formula(n):
    assert n_power_of_two(n)
    return 4*(n.bit_length()-1)-4


def field_automorphism_rank(n):
    return n - cycle_count_multiplier(n, 9)


def phase_projective_rank(n, power_fn):
    """For q_j=omega^f(j), sigma(q_j)/q_j=omega^(8 f(j)).

    min_c rank(sigma(Q)-c Q) = n - max population of f(j) modulo n/8.
    """
    assert n_power_of_two(n)
    count = Counter(power_fn(j) % (n//8) for j in range(n))
    return n - max(count.values())


def all_orders_cyclotomic_coefficient(n, stage, col=1):
    """Exact finite-field image of coefficient of omega^(col mod L) in
    the expansion (S^-1 D S)[col,col] on basis 1,omega,...,omega^(L-1)
    of Q(zeta_N) over K=Q(zeta_8), L=n/8. Nonzero proves nonzero in char0.
    """
    assert n_power_of_two(n)
    L=n//8
    e=[0]*n;e[col]=1
    forward_col=stage.apply(e)
    # Recover the relevant inverse row from N exact inverse black-box calls.
    inv_row=[]
    for k in range(n):
        ek=[0]*n;ek[k]=1
        inv_row.append(stage.apply(ek,inverse=True)[col])
    weights=[inv_row[k]*forward_col[k]%MOD for k in range(n)]
    assert sum(weights)%MOD==1
    coefficients=[]
    for r in range(L):
        c=0
        for t in range(8):
            k=r+t*L
            c+=weights[k]*pow(OMEGA8,t,MOD)
        coefficients.append(c%MOD)
    omega=pow(3,(MOD-1)//n,MOD)
    beta=sum(weights[k]*pow(omega,k,MOD) for k in range(n))%MOD
    reconstructed=sum(coefficients[r]*pow(omega,r,MOD) for r in range(L))%MOD
    assert beta==reconstructed
    return dict(n=n, col=col, class_residue=col%L,
                cyclotomic_reconstruction_matches=beta==reconstructed,
                class_coefficient_mod_p=coefficients[col%L],
                class_coefficient_nonzero=coefficients[col%L]!=0,
                nonzero_nonconstant_coeffs=sum(bool(c) for c in coefficients[1:]),
                normalizer_galois_independent=True)


def fourier_galois_diff_rank_mod(n):
    """Independent direct F(omega^9)-F(omega) rank over F_998244353."""
    assert n_power_of_two(n)
    omega=pow(3,(MOD-1)//n,MOD)
    mat=[[ (pow(omega,9*k*j,MOD)-pow(omega,k*j,MOD))%MOD
            for j in range(n)] for k in range(n)]
    return rank_mod(mat,MOD)


def stage_kind(n,kind,seed):
    if kind=='tree':return UnitaryGreenMixer(n,p=MOD,seed=seed)
    if kind=='haar':return HaarEscapeMixerMod(n,seed=seed)
    if kind=='strong':return StrongHaarEscapeMixerMod(n,seed=seed)
    raise ValueError(kind)


def gate_summary():
    return [dict(n=n, cycles=cycle_count_multiplier(n), predicted_cycles=cycle_count_formula(n),
                 required_nonbase_phase_coordinates=field_automorphism_rank(n),
                 linear_ramp_budget=phase_projective_rank(n,lambda j:j),
                 quadratic_chirp_budget=phase_projective_rank(n,lambda j:j*j),
                 sparse_patch_8_budget=min(8,n)) for n in (16,32,64,128,256,512,1024)]

if __name__=='__main__':
    import json
    print(json.dumps(gate_summary(),indent=2))
    print('CYCL FIELD CERTIFICATES')
    for n in (16,32,64,128):
        for kind in ('tree','haar','strong'):
            s=stage_kind(n,kind,seed=14701+n)
            print(kind, all_orders_cyclotomic_coefficient(n,s))
    print('DFT DIRECT RANK')
    for n in (16,32,64,128):
        print(n,fourier_galois_diff_rank_mod(n),field_automorphism_rank(n))
