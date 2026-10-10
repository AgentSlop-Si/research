import math
import json
from dataclasses import dataclass, asdict
from typing import List, Tuple, Dict
import numpy as np

PHASES = np.array([1+0j, -1+0j, 1j, -1j], dtype=np.complex128)

@dataclass
class Params:
    N: int
    B: int
    eps_sample: float
    eps_phase: float
    h1: float
    h2: float
    delta: float
    Q_start: int
    Q_slope: int
    descriptor_bits: int
    gamma: float
    g_wordfit: int
    g_used: int
    k_min: int
    k_used: int
    G: int
    field_bits: int
    lanes_per_word: int
    words_per_vector: int


def unitary_fft(x: np.ndarray) -> np.ndarray:
    return np.fft.fft(x) / math.sqrt(len(x))


def concentration_k(N: int, eps_sample: float, delta: float) -> int:
    # Safe componentwise Hoeffding + union bound:
    # P(max_m |err_m| > eps_sample * L/sqrt(N)) <= delta
    # using Re/Im <= eps_sample/sqrt(2).
    return math.ceil(4.0 * math.log(4.0 * N / delta) / (eps_sample ** 2))


def choose_params(N: int, eps_sample=0.35, eps_phase=0.08, h1=0.06, h2=0.04,
                  delta=0.05, gamma=0.75, B=None, g_override=None) -> Params:
    if B is None:
        B = max(2, math.ceil(math.log2(N)))
    # Ensure pi/Q_start + pi*B/Q_slope <= eps_phase.
    Q_start = max(2, math.ceil(2 * math.pi / eps_phase))
    Q_slope = max(2, math.ceil(2 * math.pi * B / eps_phase))
    alphabet = 1 + 4 * Q_start * Q_slope  # +1 null symbol (not used in full groups)
    p = math.ceil(math.log2(alphabet))
    logN = math.log2(N)
    g_wordfit = max(1, math.floor(gamma * logN / p))
    g = g_wordfit if g_override is None else max(1, int(g_override))
    k_min = concentration_k(N, eps_sample, delta)
    # Make k a multiple of g so every group has equal weight and no padding factor.
    k = g * math.ceil(k_min / g)
    G = k // g
    qv = math.ceil(1.0 / h1) + 2
    # Each table lane is stored as nonnegative z+qv. Adding G vectors must not carry across lanes.
    max_field_sum = G * (2 * qv)
    field_bits = max(2, math.ceil(math.log2(max_field_sum + 1)) + 1)
    # Use a sufficiently large constant-factor word so products/indices fit in the model.
    w = max(64, math.ceil(4 * logN))
    lanes_per_word = max(1, w // field_bits)
    words_per_vector = math.ceil(B / lanes_per_word)
    return Params(N, B, eps_sample, eps_phase, h1, h2, delta,
                  Q_start, Q_slope, p, gamma, g_wordfit, g,
                  k_min, k, G, field_bits, lanes_per_word, words_per_vector)


def signed_atom_distribution(x: np.ndarray):
    masses = []
    atoms = []
    for j, z in enumerate(x):
        a = float(z.real)
        b = float(z.imag)
        if a != 0.0:
            masses.append(abs(a)); atoms.append((j, 0 if a > 0 else 1))
        if b != 0.0:
            masses.append(abs(b)); atoms.append((j, 2 if b > 0 else 3))
    L = float(sum(masses))
    if L == 0.0:
        return L, np.array([], dtype=float), []
    return L, np.asarray(masses, dtype=float) / L, atoms


def sample_atoms(x: np.ndarray, k: int, rng: np.random.Generator):
    # Prototype sampling. The theorem note gives the O(N) two-pass sorted-threshold implementation.
    L, probs, atoms = signed_atom_distribution(x)
    if L == 0.0:
        return 0.0, []
    idx = rng.choice(len(atoms), size=k, replace=True, p=probs)
    return L, [atoms[int(i)] for i in idx]


def exact_sampled_spectrum(N: int, L: float, samples: List[Tuple[int,int]]) -> np.ndarray:
    if not samples:
        return np.zeros(N, dtype=np.complex128)
    y = np.zeros(N, dtype=np.complex128)
    amp = L / len(samples)
    for j, sc in samples:
        y[j] += amp * PHASES[sc]
    return unitary_fft(y)


def quant_phase_bin(num: int, den: int, Q: int) -> int:
    # nearest bin to num/den mod 1; prototype uses exact integer numerator.
    r = num % den
    return int((Q * r + den // 2) // den) % Q


def group_key_for_block(samples, m0: int, p: Params, group_idx: int):
    lo = group_idx * p.g_used
    hi = lo + p.g_used
    out = []
    for j, sc in samples[lo:hi]:
        qa = quant_phase_bin(j * m0, p.N, p.Q_start)
        qb = quant_phase_bin(j, p.N, p.Q_slope)
        out.append((sc, qa, qb))
    return tuple(out)


def build_group_entry(key, p: Params, lanes: int):
    t = np.arange(lanes, dtype=float)
    v = np.zeros(lanes, dtype=np.complex128)
    for sc, qa, qb in key:
        alpha = qa / p.Q_start
        beta = qb / p.Q_slope
        v += PHASES[sc] * np.exp(-2j * np.pi * (alpha + t * beta))
    v /= p.g_used
    zr = np.rint(v.real / p.h1).astype(np.int64)
    zi = np.rint(v.imag / p.h1).astype(np.int64)
    qv = math.ceil(1.0 / p.h1) + 2
    zr = np.clip(zr, -qv, qv)
    zi = np.clip(zi, -qv, qv)
    return zr, zi


def pack_nonnegative_lanes(vals: np.ndarray, field_bits: int, lanes_per_word: int):
    words = []
    mask = (1 << field_bits) - 1
    for start in range(0, len(vals), lanes_per_word):
        word = 0
        chunk = vals[start:start+lanes_per_word]
        for lane, val in enumerate(chunk):
            iv = int(val)
            if iv < 0 or iv > mask:
                raise ValueError((iv, field_bits))
            word |= iv << (lane * field_bits)
        words.append(word)
    return words


def unpack_nonnegative_lanes(words, count: int, field_bits: int, lanes_per_word: int):
    vals = []
    mask = (1 << field_bits) - 1
    for word in words:
        for lane in range(lanes_per_word):
            vals.append((word >> (lane * field_bits)) & mask)
            if len(vals) == count:
                return np.asarray(vals, dtype=np.int64)
    return np.asarray(vals, dtype=np.int64)


def packed_decode(N: int, L: float, samples, p: Params):
    if L == 0.0:
        return np.zeros(N, dtype=np.complex128), {"table_entries": 0, "lookup_count": 0, "packed_word_adds": 0}
    assert len(samples) == p.k_used and p.k_used % p.g_used == 0
    cache: Dict[Tuple, Tuple[np.ndarray,np.ndarray]] = {}
    out = np.zeros(N, dtype=np.complex128)
    qv = math.ceil(1.0 / p.h1) + 2
    lookup_count = 0
    packed_word_adds = 0

    for m0 in range(0, N, p.B):
        lanes = min(p.B, N - m0)
        wr_sum = [0] * math.ceil(lanes / p.lanes_per_word)
        wi_sum = [0] * math.ceil(lanes / p.lanes_per_word)
        for group_idx in range(p.G):
            key = group_key_for_block(samples, m0, p, group_idx)
            ent = cache.get(key)
            if ent is None:
                ent = build_group_entry(key, p, lanes)
                cache[key] = ent
            zr, zi = ent
            # Offset signed lane by qv before packed addition.
            pr = pack_nonnegative_lanes(zr + qv, p.field_bits, p.lanes_per_word)
            pi = pack_nonnegative_lanes(zi + qv, p.field_bits, p.lanes_per_word)
            for a in range(len(wr_sum)):
                wr_sum[a] += pr[a]
                wi_sum[a] += pi[a]
                packed_word_adds += 2
            lookup_count += 1

        sr = unpack_nonnegative_lanes(wr_sum, lanes, p.field_bits, p.lanes_per_word) - p.G * qv
        si = unpack_nonnegative_lanes(wi_sum, lanes, p.field_bits, p.lanes_per_word) - p.G * qv
        avg = (p.h1 / p.G) * (sr.astype(float) + 1j * si.astype(float))
        # Final fixed-point output rounding in normalized phasor-average units.
        avg = p.h2 * (np.rint(avg.real / p.h2) + 1j * np.rint(avg.imag / p.h2))
        out[m0:m0+lanes] = (L / math.sqrt(N)) * avg

    stats = {"table_entries": len(cache), "lookup_count": lookup_count,
             "packed_word_adds": packed_word_adds}
    return out, stats


def decoder_bound_normalized(p: Params):
    # Bound in units of L/sqrt(N): phase trajectory error + group rounding + final rounding.
    # |exp(i a)-exp(i b)| <= |a-b|; quantizer design makes <= eps_phase.
    return p.eps_phase + p.h1 / math.sqrt(2) + p.h2 / math.sqrt(2)


def cost_model(log2N: int, eps_sample=0.35, eps_phase=0.08, h1=0.06,
               delta_power=1.0, gamma=0.75):
    # Symbolic-scale model using N=2^m without constructing N.
    m = float(log2N)
    B = max(2, math.ceil(m))
    Q0 = max(2, math.ceil(2 * math.pi / eps_phase))
    Q1 = max(2, math.ceil(2 * math.pi * B / eps_phase))
    pbits = math.ceil(math.log2(1 + 4 * Q0 * Q1))
    g = max(1, math.floor(gamma * m / pbits))
    lnN = m * math.log(2)
    # delta=N^{-delta_power}
    lnfactor = math.log(4.0) + (1.0 + delta_power) * lnN
    k0 = math.ceil(4.0 * lnfactor / (eps_sample ** 2))
    k = g * math.ceil(k0 / g)
    G = k // g
    qv = math.ceil(1.0 / h1) + 2
    field_bits = max(2, math.ceil(math.log2(G * (2*qv) + 1)) + 1)
    w = max(64, math.ceil(4*m))
    lpw = max(1, w // field_bits)
    wpv = math.ceil(B / lpw)
    # Ratios of selected costs to N.
    key_ops_ratio = k / B
    lookup_ratio = G / B
    packed_add_ratio = 2 * G * wpv / B
    preprocess_log2_entries = pbits * g
    preprocess_exponent = preprocess_log2_entries / m
    return {
        "log2N": log2N, "B": B, "descriptor_bits": pbits, "g": g, "k": k, "G": G,
        "field_bits": field_bits, "words_per_vector": wpv,
        "key_ops_over_N": key_ops_ratio,
        "lookups_over_N": lookup_ratio,
        "packed_word_adds_over_N": packed_add_ratio,
        "table_exponent_logN": preprocess_exponent,
        "preprocess_polylog_factor_note": "entry construction/storage is polylog(N); exponent < gamma asymptotically"
    }


def make_inputs(N, rng):
    flat = np.ones(N, dtype=np.complex128)
    gaussian = rng.normal(size=N) + 1j*rng.normal(size=N)
    phase = np.exp(2j*np.pi*rng.random(N))
    power = (rng.normal(size=N)+1j*rng.normal(size=N)) / np.sqrt(np.arange(1, N+1))
    spike_noise = 0.03*(rng.normal(size=N)+1j*rng.normal(size=N))
    idx = rng.choice(N, size=max(1,N//64), replace=False)
    spike_noise[idx] += rng.normal(size=len(idx))*5 + 1j*rng.normal(size=len(idx))*5
    return {"flat":flat, "gaussian":gaussian, "random_phase":phase, "power_law":power, "spike_noise":spike_noise}


def run_experiment():
    rng = np.random.default_rng(20261009)
    results = {"experiments": [], "cost_model": []}
    # Small-N prototype: use g=4 to exercise grouped lookup/packing. This is algebra testing,
    # not a claim that the conservative word-fit inequality already gives g=4 at these N.
    for N in [256, 1024, 4096]:
        p = choose_params(N, eps_sample=0.45, eps_phase=0.08, h1=0.05, h2=0.04,
                          delta=0.05, gamma=0.75, g_override=4)
        for name, x in make_inputs(N, rng).items():
            L, samples = sample_atoms(x, p.k_used, rng)
            exact_sampled = exact_sampled_spectrum(N, L, samples)
            approx, stats = packed_decode(N, L, samples, p)
            exact_full = unitary_fft(x)
            scale = L / math.sqrt(N) if L else 1.0
            dec_err = float(np.max(np.abs(approx-exact_sampled))/scale) if L else 0.0
            total_err = float(np.max(np.abs(approx-exact_full))/scale) if L else 0.0
            sample_err = float(np.max(np.abs(exact_sampled-exact_full))/scale) if L else 0.0
            results["experiments"].append({
                "N":N, "case":name, "params":asdict(p), "decoder_error_normalized":dec_err,
                "sampling_error_normalized":sample_err, "total_error_normalized":total_err,
                "decoder_bound_normalized":decoder_bound_normalized(p), **stats
            })
    for m in [20, 32, 48, 64, 96, 128, 192, 256, 384, 512, 768, 1024]:
        results["cost_model"].append(cost_model(m))
    return results


if __name__ == "__main__":
    r = run_experiment()
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(r, f, indent=2)
    ex = r["experiments"]
    print("experiments", len(ex))
    print("max normalized decoder error", max(z["decoder_error_normalized"] for z in ex))
    print("max decoder bound", max(z["decoder_bound_normalized"] for z in ex))
    print("decoder bound violations", sum(z["decoder_error_normalized"] > z["decoder_bound_normalized"] + 1e-12 for z in ex))
    print("median normalized total error", float(np.median([z["total_error_normalized"] for z in ex])))
    print("cost tail")
    for z in r["cost_model"][-5:]:
        print(z)
