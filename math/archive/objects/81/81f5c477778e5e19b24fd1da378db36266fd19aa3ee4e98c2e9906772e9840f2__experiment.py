"""Exhaustive small-size closest-pair experiments (numerical illustrations).

Distinctness is established SYMBOLICALLY by the cyclotomic basis proof,
not by floating point.  High-precision rechecks quantify numerical gaps.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import numpy as np
from scipy.spatial import cKDTree
import mpmath as mp

from orbit_stability import complementary_signal, folded_odd_coefficients, theoretical_lipschitz_bound, canonical_representatives, necessary_odd_representatives


def phase_values(n: int) -> np.ndarray:
    return np.exp(2j * np.pi * np.arange(n//2) / n)


def complex_orbit_representatives(n: int) -> np.ndarray:
    """Evaluate X[1] exactly in structure, numerically for exhaustive masks."""
    m = n // 2
    if m > 16:
        raise ValueError("only m<=16 supported for exhaustive Python audit")
    values = np.array([0j])
    phases = phase_values(n)
    # For each new independent bit, update sums +/- zeta^j, no FFT or cache.
    for p in phases:
        values = np.concatenate((values-p, values+p))
    return values


def closest_pair(n: int) -> dict:
    alpha = complex_orbit_representatives(n)
    xy = np.column_stack((alpha.real, alpha.imag))
    tree = cKDTree(xy)
    distances, indices = tree.query(xy, k=2, workers=1)
    pos = int(np.argmin(distances[:, 1]))
    partner = int(indices[pos, 1])
    if not pos != partner:
        raise AssertionError("unexpected trivial closest pair")
    mp.mp.dps = 90
    m = n // 2
    diff = tuple(a-b for a,b in zip(folded_odd_coefficients(pos,n),folded_odd_coefficients(partner,n)))
    z = sum(mp.mpc(v)*mp.e**(2*mp.pi*mp.j*j/n) for j,v in enumerate(diff))
    precise = mp.fabs(z)
    x = np.array(complementary_signal(pos,n))
    y = np.array(complementary_signal(partner,n))
    spectra = np.fft.fft(x-y)  # numerical independent full-spectrum reference
    max_full = float(np.max(np.abs(spectra)))
    even_difference = float(np.max(np.abs(spectra[::2])))
    assert even_difference < 1e-8
    return {
        "N": n,
        "family_size": 1 << m,
        "mask_u": pos,
        "mask_v": partner,
        "different_coordinates_in_u": (pos ^ partner).bit_count(),
        "one_rep_gap_double": float(distances[pos,1]),
        "one_rep_gap_high_precision": mp.nstr(precise,60),
        "full_spectrum_gap_max": max_full,
        "empirical_decoder_lipschitz_lower_bound": mp.nstr(max_full / precise,30),
        "even_spectral_difference_max": even_difference,
        "cyclotomic_integer_difference_coeffs": list(diff),
        "analytical_universal_lower_bound": theoretical_lipschitz_bound(n,1),
    }


def run() -> dict:
    results = [closest_pair(n) for n in (8,16,32)]
    parameters = [{"N":n,"r":r,"packing":theoretical_lipschitz_bound(n,r)} for n in (32,64,128,256,1024) for r in (1,2,4) if r<=n//2]
    needed=[{"N":n,"target_condition":"N^2","at_least_r_odd_bins":necessary_odd_representatives(n,n*n)} for n in (32,64,128,256,1024)]
    return {"closest_pairs":results,"packing_cases":parameters,"stable_measurement_necessities":needed,"prior_art":"Frobenius FFT (2017/2018); this audit makes no novelty claims for orbit identities or information-packing"}


if __name__ == "__main__":
    r=run()
    out=Path(__file__).resolve().parent/"audit_results.json"
    out.write_text(json.dumps(r,indent=2)+"\n")
    print(json.dumps({"pairs":[{k:v for k,v in row.items() if k in ("N","one_rep_gap_high_precision","empirical_decoder_lipschitz_lower_bound","full_spectrum_gap_max")} for row in r["closest_pairs"]],"necessary":r["stable_measurement_necessities"]},indent=2))
