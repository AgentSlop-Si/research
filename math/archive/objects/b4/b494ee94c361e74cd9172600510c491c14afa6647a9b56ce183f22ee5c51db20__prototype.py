"""Prototype for the shrinking-error packed sparse-surrogate DFT branch.

This is an algebra/error/cost-model experiment, not a practical FFT replacement.
The asymptotic theorem uses much larger N than the toy tests below.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from typing import Dict, List, Tuple

import numpy as np

PHASES = np.asarray([1 + 0j, -1 + 0j, 1j, -1j], dtype=np.complex128)


@dataclass
class Params:
    N: int
    B: int
    k: int
    eps_phase: float
    h1: float
    h2: float
    Q_start: int
    Q_slope: int
    descriptor_bits: int
    gamma: float
    g_wordfit: int
    g_used: int
    G: int
    field_bits: int
    word_bits: int
    lanes_per_word: int
    words_per_vector: int


def unitary_fft(x: np.ndarray) -> np.ndarray:
    return np.fft.fft(x) / math.sqrt(len(x))


def decoder_bound_normalized(p: Params) -> float:
    """Error in units of L_box(x)/sqrt(N)."""
    return p.eps_phase + p.h1 / math.sqrt(2.0) + p.h2 / math.sqrt(2.0)


def concentration_k(N: int, eta_sample: float, delta: float) -> int:
    """Safe componentwise complex Hoeffding + union bound."""
    return math.ceil(4.0 * math.log(4.0 * N / delta) / (eta_sample**2))


def choose_params(
    N: int,
    k: int,
    B: int | None = None,
    eps_phase: float = 0.04,
    h1: float = 0.03,
    h2: float = 0.02,
    gamma: float = 0.72,
    word_constant: float = 8.0,
    g_override: int | None = None,
) -> Params:
    if N <= 1:
        raise ValueError("N must exceed 1")
    if k <= 0:
        raise ValueError("k must be positive")
    B = min(N, B if B is not None else k)
    if B <= 0:
        raise ValueError("B must be positive")

    # Nearest-bin phase errors obey pi/Q_start + pi*B/Q_slope <= eps_phase.
    Q_start = max(2, math.ceil(2.0 * math.pi / eps_phase))
    Q_slope = max(2, math.ceil(2.0 * math.pi * B / eps_phase))

    # Four phases (+1,-1,+i,-i), quantized start phase, quantized slope.
    alphabet_bound = 4 * Q_start * Q_slope
    descriptor_bits = math.ceil(math.log2(alphabet_bound + 1))

    logN = math.log2(N)
    g_wordfit = max(1, math.floor(gamma * logN / descriptor_bits))
    g = g_override if g_override is not None else g_wordfit
    if g < 1:
        raise ValueError("group size must be at least 1")

    # Pad k to a multiple of g. Repeating independent draws is equivalent to
    # simply drawing the rounded-up sample count in the actual algorithm.
    k_used = g * math.ceil(k / g)
    G = k_used // g

    qv = math.ceil(1.0 / h1) + 3
    max_accumulated_field = G * (2 * qv)
    field_bits = max(2, math.ceil(math.log2(max_accumulated_field + 1)) + 1)

    word_bits = max(64, math.ceil(word_constant * logN))
    lanes_per_word = max(1, word_bits // field_bits)
    words_per_vector = math.ceil(B / lanes_per_word)

    return Params(
        N=N,
        B=B,
        k=k_used,
        eps_phase=eps_phase,
        h1=h1,
        h2=h2,
        Q_start=Q_start,
        Q_slope=Q_slope,
        descriptor_bits=descriptor_bits,
        gamma=gamma,
        g_wordfit=g_wordfit,
        g_used=g,
        G=G,
        field_bits=field_bits,
        word_bits=word_bits,
        lanes_per_word=lanes_per_word,
        words_per_vector=words_per_vector,
    )


def signed_atom_distribution(x: np.ndarray) -> Tuple[float, np.ndarray, List[Tuple[int, int]]]:
    masses: List[float] = []
    atoms: List[Tuple[int, int]] = []
    for j, z in enumerate(x):
        a = float(z.real)
        b = float(z.imag)
        if a != 0.0:
            masses.append(abs(a))
            atoms.append((j, 0 if a > 0 else 1))
        if b != 0.0:
            masses.append(abs(b))
            atoms.append((j, 2 if b > 0 else 3))
    L = float(sum(masses))
    if L == 0.0:
        return 0.0, np.asarray([], dtype=float), []
    probs = np.asarray(masses, dtype=float) / L
    return L, probs, atoms


def sample_atoms(x: np.ndarray, k: int, rng: np.random.Generator) -> Tuple[float, List[Tuple[int, int]]]:
    L, probs, atoms = signed_atom_distribution(x)
    if L == 0.0:
        return 0.0, []
    idx = rng.choice(len(atoms), size=k, replace=True, p=probs)
    return L, [atoms[int(i)] for i in idx]


def exact_sampled_spectrum(N: int, L: float, samples: List[Tuple[int, int]]) -> np.ndarray:
    if not samples:
        return np.zeros(N, dtype=np.complex128)
    y = np.zeros(N, dtype=np.complex128)
    amp = L / len(samples)
    for j, phase_code in samples:
        y[j] += amp * PHASES[phase_code]
    return unitary_fft(y)


def quant_phase_bin(num: int, den: int, Q: int) -> int:
    r = num % den
    return int((Q * r + den // 2) // den) % Q


def group_key_for_block(
    samples: List[Tuple[int, int]], m0: int, p: Params, group_idx: int
) -> Tuple[Tuple[int, int, int], ...]:
    lo = group_idx * p.g_used
    hi = lo + p.g_used
    out: List[Tuple[int, int, int]] = []
    for j, phase_code in samples[lo:hi]:
        qa = quant_phase_bin(j * m0, p.N, p.Q_start)
        qb = quant_phase_bin(j, p.N, p.Q_slope)
        out.append((phase_code, qa, qb))
    return tuple(out)


def build_group_entry(
    key: Tuple[Tuple[int, int, int], ...], p: Params, lanes: int
) -> Tuple[np.ndarray, np.ndarray]:
    t = np.arange(lanes, dtype=float)
    v = np.zeros(lanes, dtype=np.complex128)
    for phase_code, qa, qb in key:
        alpha = qa / p.Q_start
        beta = qb / p.Q_slope
        v += PHASES[phase_code] * np.exp(-2j * np.pi * (alpha + t * beta))
    v /= p.g_used
    zr = np.rint(v.real / p.h1).astype(np.int64)
    zi = np.rint(v.imag / p.h1).astype(np.int64)
    qv = math.ceil(1.0 / p.h1) + 3
    zr = np.clip(zr, -qv, qv)
    zi = np.clip(zi, -qv, qv)
    return zr, zi


def pack_nonnegative_lanes(vals: np.ndarray, field_bits: int, lanes_per_word: int) -> List[int]:
    words: List[int] = []
    mask = (1 << field_bits) - 1
    for start in range(0, len(vals), lanes_per_word):
        word = 0
        for lane, val in enumerate(vals[start : start + lanes_per_word]):
            iv = int(val)
            if iv < 0 or iv > mask:
                raise ValueError((iv, field_bits))
            word |= iv << (lane * field_bits)
        words.append(word)
    return words


def unpack_nonnegative_lanes(
    words: List[int], count: int, field_bits: int, lanes_per_word: int
) -> np.ndarray:
    vals: List[int] = []
    mask = (1 << field_bits) - 1
    for word in words:
        for lane in range(lanes_per_word):
            vals.append((word >> (lane * field_bits)) & mask)
            if len(vals) == count:
                return np.asarray(vals, dtype=np.int64)
    return np.asarray(vals, dtype=np.int64)


def packed_decode(
    N: int, L: float, samples: List[Tuple[int, int]], p: Params
) -> Tuple[np.ndarray, Dict[str, int]]:
    if L == 0.0:
        return np.zeros(N, dtype=np.complex128), {
            "table_entries": 0,
            "lookup_count": 0,
            "packed_word_adds": 0,
            "descriptor_count": 0,
        }
    if len(samples) != p.k:
        raise ValueError((len(samples), p.k))

    cache: Dict[Tuple, Tuple[np.ndarray, np.ndarray]] = {}
    out = np.zeros(N, dtype=np.complex128)
    qv = math.ceil(1.0 / p.h1) + 3
    lookup_count = 0
    packed_word_adds = 0
    descriptor_count = 0

    for m0 in range(0, N, p.B):
        lanes = min(p.B, N - m0)
        word_count = math.ceil(lanes / p.lanes_per_word)
        wr_sum = [0] * word_count
        wi_sum = [0] * word_count

        for group_idx in range(p.G):
            key = group_key_for_block(samples, m0, p, group_idx)
            descriptor_count += len(key)
            entry = cache.get(key)
            if entry is None:
                entry = build_group_entry(key, p, lanes)
                cache[key] = entry
            zr, zi = entry
            pr = pack_nonnegative_lanes(zr + qv, p.field_bits, p.lanes_per_word)
            pi = pack_nonnegative_lanes(zi + qv, p.field_bits, p.lanes_per_word)
            for wi in range(word_count):
                wr_sum[wi] += pr[wi]
                wi_sum[wi] += pi[wi]
                packed_word_adds += 2
            lookup_count += 1

        sr = (
            unpack_nonnegative_lanes(wr_sum, lanes, p.field_bits, p.lanes_per_word)
            - p.G * qv
        )
        si = (
            unpack_nonnegative_lanes(wi_sum, lanes, p.field_bits, p.lanes_per_word)
            - p.G * qv
        )
        avg = (p.h1 / p.G) * (sr.astype(float) + 1j * si.astype(float))
        avg = p.h2 * (np.rint(avg.real / p.h2) + 1j * np.rint(avg.imag / p.h2))
        out[m0 : m0 + lanes] = (L / math.sqrt(N)) * avg

    return out, {
        "table_entries": len(cache),
        "lookup_count": lookup_count,
        "packed_word_adds": packed_word_adds,
        "descriptor_count": descriptor_count,
    }


def make_inputs(N: int, rng: np.random.Generator) -> Dict[str, np.ndarray]:
    flat = np.ones(N, dtype=np.complex128)
    random_phase = np.exp(2j * np.pi * rng.random(N))
    gaussian = rng.normal(size=N) + 1j * rng.normal(size=N)
    power_law = (rng.normal(size=N) + 1j * rng.normal(size=N)) / np.sqrt(
        np.arange(1, N + 1)
    )
    spike_noise = 0.02 * (rng.normal(size=N) + 1j * rng.normal(size=N))
    idx = rng.choice(N, size=max(1, N // 64), replace=False)
    spike_noise[idx] += 4.0 * (rng.normal(size=len(idx)) + 1j * rng.normal(size=len(idx)))
    return {
        "flat": flat,
        "random_phase": random_phase,
        "gaussian": gaussian,
        "power_law": power_law,
        "spike_noise": spike_noise,
    }


def symbolic_cost_model(
    log2N: int,
    failure_power: float = 1.0,
    mode: str = "linear",
    gamma: float = 0.72,
    word_constant: float = 8.0,
    error_constant: float = 1.0,
) -> Dict[str, float | int | str]:
    """Asymptotic scale model without constructing N=2^log2N.

    linear mode:
      eta ~= C loglog(N)/sqrt(log N), k from Hoeffding, B=k.

    subfft mode:
      k ~= log^3(N)/(loglog N)^3, giving time N logN/loglogN
      and sampling scale roughly (loglog N)^(3/2)/log N.
    """
    L = float(log2N)
    ell = max(1.0, math.log2(max(2.0, L)))
    ln_factor = math.log(4.0) + (1.0 + failure_power) * L * math.log(2.0)

    if mode == "linear":
        eta_sample = min(0.9, error_constant * ell / math.sqrt(L))
        k0 = math.ceil(4.0 * ln_factor / (eta_sample**2))
    elif mode == "subfft":
        k0 = max(1, math.ceil(L**3 / (ell**3)))
        eta_sample = math.sqrt(4.0 * ln_factor / k0)
    else:
        raise ValueError(mode)

    B = k0
    eta_total = min(0.95, 2.0 * eta_sample)
    eps_phase = eta_total / 4.0
    h1 = eta_total / (4.0 * math.sqrt(2.0))
    h2 = eta_total / (4.0 * math.sqrt(2.0))

    Q_start = max(2, math.ceil(2.0 * math.pi / eps_phase))
    Q_slope = max(2, math.ceil(2.0 * math.pi * B / eps_phase))
    pbits = math.ceil(math.log2(1 + 4 * Q_start * Q_slope))
    g = max(1, math.floor(gamma * L / pbits))
    k = g * math.ceil(k0 / g)
    G = k // g

    qv = math.ceil(1.0 / h1) + 3
    field_bits = max(2, math.ceil(math.log2(G * (2 * qv) + 1)) + 1)
    word_bits = max(64, math.ceil(word_constant * L))
    lanes_per_word = max(1, word_bits // field_bits)
    words_per_vector = math.ceil(B / lanes_per_word)

    # Normalize modeled online subcosts by N.
    descriptor_ratio = k / B
    lookup_ratio = G / B
    packed_add_ratio = 2.0 * G * words_per_vector / B
    table_exponent = pbits * g / L

    return {
        "mode": mode,
        "log2N": log2N,
        "log2log2N": ell,
        "eta_sample": eta_sample,
        "eta_total_budget": eta_total,
        "k": k,
        "B": B,
        "descriptor_bits": pbits,
        "g": g,
        "G": G,
        "field_bits": field_bits,
        "words_per_vector": words_per_vector,
        "descriptor_ops_over_N": descriptor_ratio,
        "lookups_over_N": lookup_ratio,
        "packed_word_adds_over_N": packed_add_ratio,
        "modeled_total_non_io_over_N": descriptor_ratio + lookup_ratio + packed_add_ratio,
        "table_exponent_logN": table_exponent,
        "predicted_sampling_scale": eta_sample,
    }


def packed_correctness_experiment(rng: np.random.Generator) -> List[Dict]:
    rows: List[Dict] = []
    N = 2048
    inputs = make_inputs(N, rng)
    for k in [16, 32, 64, 128]:
        # Shrink decoder precision mildly as k grows. Toy constants are chosen for
        # tractable tests, not to instantiate the asymptotic theorem literally.
        scale = math.sqrt(16.0 / k)
        eps_phase = 0.04 * scale
        h1 = 0.03 * scale
        h2 = 0.02 * scale
        p = choose_params(
            N=N,
            k=k,
            B=k,
            eps_phase=eps_phase,
            h1=h1,
            h2=h2,
            g_override=4,
        )
        for name, x in inputs.items():
            L, samples = sample_atoms(x, p.k, rng)
            exact_sampled = exact_sampled_spectrum(N, L, samples)
            approx, stats = packed_decode(N, L, samples, p)
            norm = L / math.sqrt(N) if L else 1.0
            decoder_error = float(np.max(np.abs(approx - exact_sampled)) / norm) if L else 0.0
            rows.append(
                {
                    "N": N,
                    "case": name,
                    "requested_k": k,
                    "params": asdict(p),
                    "decoder_error_normalized": decoder_error,
                    "decoder_bound_normalized": decoder_bound_normalized(p),
                    **stats,
                }
            )
    return rows


def sampling_scaling_experiment(rng: np.random.Generator) -> List[Dict]:
    rows: List[Dict] = []
    N = 2048
    cases = make_inputs(N, rng)
    selected = {k: cases[k] for k in ["flat", "random_phase", "gaussian", "spike_noise"]}
    for k in [16, 32, 64, 128, 256, 512]:
        for name, x in selected.items():
            exact = unitary_fft(x)
            L, _, _ = signed_atom_distribution(x)
            norm = L / math.sqrt(N) if L else 1.0
            errs: List[float] = []
            for _ in range(40):
                L2, samples = sample_atoms(x, k, rng)
                estimate = exact_sampled_spectrum(N, L2, samples)
                errs.append(float(np.max(np.abs(estimate - exact)) / norm))
            rows.append(
                {
                    "N": N,
                    "case": name,
                    "k": k,
                    "trials": len(errs),
                    "median_normalized_sampling_error": float(np.median(errs)),
                    "p90_normalized_sampling_error": float(np.quantile(errs, 0.9)),
                    "max_normalized_sampling_error": float(np.max(errs)),
                    "sqrt_logN_over_k": math.sqrt(math.log(N) / k),
                }
            )
    return rows


def rejected_energy_mixture_check(rng: np.random.Generator) -> List[Dict]:
    """Quantify why the half-length-squared/half-uniform shortcut is not stronger.

    It gives an additive O(||x||_2) scale, while L_box/sqrt(N) <= sqrt(2)||x||_2.
    For flat cancellation-heavy inputs the two scales differ only by a constant.
    """
    rows: List[Dict] = []
    for N in [256, 1024, 4096, 16384]:
        for name, x in {
            "flat": np.ones(N, dtype=np.complex128),
            "random_phase": np.exp(2j * np.pi * rng.random(N)),
            "single_spike": np.eye(1, N, int(rng.integers(0, N)), dtype=np.complex128).ravel(),
            "gaussian": rng.normal(size=N) + 1j * rng.normal(size=N),
        }.items():
            Lbox = float(np.sum(np.abs(x.real) + np.abs(x.imag)))
            l2 = float(np.linalg.norm(x))
            rows.append(
                {
                    "N": N,
                    "case": name,
                    "Lbox_over_sqrtN": Lbox / math.sqrt(N),
                    "l2": l2,
                    "ratio_Lbox_over_sqrtN_to_l2": (Lbox / math.sqrt(N)) / l2 if l2 else 0.0,
                }
            )
    return rows


def run() -> Dict:
    rng = np.random.default_rng(20261009)
    result = {
        "packed_correctness": packed_correctness_experiment(rng),
        "sampling_scaling": sampling_scaling_experiment(rng),
        "rejected_energy_mixture": rejected_energy_mixture_check(rng),
        "cost_model_linear": [
            symbolic_cost_model(m, mode="linear")
            for m in [64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384]
        ],
        "cost_model_subfft": [
            symbolic_cost_model(m, mode="subfft")
            for m in [64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384]
        ],
    }
    return result


if __name__ == "__main__":
    result = run()
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    pc = result["packed_correctness"]
    ss = result["sampling_scaling"]
    print("packed cases", len(pc))
    print("max decoder error", max(r["decoder_error_normalized"] for r in pc))
    print("max decoder bound", max(r["decoder_bound_normalized"] for r in pc))
    print(
        "decoder violations",
        sum(r["decoder_error_normalized"] > r["decoder_bound_normalized"] + 1e-12 for r in pc),
    )
    print("sampling rows", len(ss))
    print("random-phase medians")
    for row in ss:
        if row["case"] == "random_phase":
            print(row["k"], row["median_normalized_sampling_error"], row["sqrt_logN_over_k"])
    print("linear cost tail")
    for row in result["cost_model_linear"][-4:]:
        print(row)
    print("subfft cost tail")
    for row in result["cost_model_subfft"][-4:]:
        print(row)
