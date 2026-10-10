"""Integer/rational shrinking-error planner without constructing N=2**L.

All quantities below are polynomial in L except the first-table row count,
which is represented by its binary exponent. No input vector or table is
allocated. The existing certified decoder implements the resulting schedule.
"""
from fractions import Fraction
from math import factorial, isqrt
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "fft_wordram_decoder_research"))
from guarded_decoder import _trig_parameters


def ceil_div(a, b):
    return (a + b - 1) // b


def ceil_sqrt(a):
    root = isqrt(a)
    return root if root * root == a else root + 1


def ceil_log2(a):
    return (max(1, a) - 1).bit_length()


def power_two_ceiling_ratio(a, b=1):
    return 1 << ceil_log2(ceil_div(a, b))


def encode_fraction(value):
    value = Fraction(value)
    return {"numerator": value.numerator, "denominator": value.denominator}


def plan(log2_N, *, failure_power=1, gamma=Fraction(1, 2), mode="linear", tau=None):
    """Validated explicit schedule from L=ceil(log2 N), represented symbolically.

    ``linear``: eta=Theta(log L/sqrt L), work O(N).
    ``subfft``: eta=Theta((log L)**1.5/L), work O(N L/log L).
    ``frontier`` with 1<=tau<=L: eta=Theta(log L/sqrt(tau L)), work O(N tau).
    The base regime is explicitly reported instead of forcing g>=1.
    """
    L, c, gamma = log2_N, failure_power, Fraction(gamma)
    if type(L) is not int or L < 2 or type(c) is not int or c < 0 or not 0 < gamma < 1:
        raise ValueError("L>=2, integer c>=0 and rational gamma in (0,1) required")
    ell = ceil_log2(L)
    if mode == "linear":
        time_factor = Fraction(1)
    elif mode == "subfft":
        time_factor = Fraction(L, ell)
    elif mode == "frontier" and tau is not None:
        time_factor = Fraction(tau)
    else:
        raise ValueError("unknown cost/error regime")
    if not 1 <= time_factor <= L:
        raise ValueError("frontier requires 1<=tau<=L")
    eta = Fraction(ell, ceil_sqrt(ceil_div(time_factor.numerator * L, time_factor.denominator)))
    # With delta_sample=N^-c/2, ln(4N/delta_sample)
    # <= log2(8N**(c+1))=3+(c+1)L. Sampling budget is eta/4.
    logarithm_upper = 3 + (c + 1) * L
    K0 = ceil_div(64 * logarithm_upper * eta.denominator ** 2, eta.numerator ** 2)
    B = K0
    Q0 = max(4, power_two_ceiling_ratio(64 * eta.denominator, eta.numerator))
    Q1 = power_two_ceiling_ratio(B * Q0)
    H = power_two_ceiling_ratio(32 * eta.denominator, eta.numerator)
    b = max(8, ceil_log2(ceil_div(32 * eta.denominator, eta.numerator)))
    p = Q0.bit_length() + Q1.bit_length() - 2
    # L-1 <= log2 N for every N with this ceiling; no dyadic padding or
    # unjustified replacement of N**gamma by 2**(gamma*L) is necessary.
    g = gamma.numerator * (L - 1) // (gamma.denominator * p)
    d, P = _trig_parameters(b)
    result = {"log2_N": L, "log2_log2_N_ceiling": ell, "mode": mode,
              "failure_power": c, "gamma": encode_fraction(gamma),
              "time_factor_tau": encode_fraction(time_factor),
              "N_representation": "L=ceil(log2 N); N itself is not constructed",
              "high_probability_regime": c >= 1,
              "target_error_factor": encode_fraction(eta),
              "sampling_error_budget": encode_fraction(eta / 4),
              "sampling_logarithm_upper": logarithm_upper,
              "minimum_sample_count": K0, "block_size": B,
              "phase_grid": Q0, "slope_grid": Q1,
              "lane_step_bits": H.bit_length() - 1, "trig_bits": b,
              "trig_degree": d, "trig_working_precision": P,
              "descriptor_bits": p, "group_size": g,
              "trig_parameter_max_integer_bits": max(factorial(d + 1).bit_length(),
                                                     2 * (d + 1) + b + 5),
              "table_allocation_performed": False}
    if g < 1:
        result["status"] = "finite_base_regime_g_zero"
        return result
    G = ceil_div(K0, g)
    K = G * g
    key_bits = p * g
    # r-bit fields hold each complete sum with no inter-field carries.
    r = (2 * H * G).bit_length()
    # Includes sampling cap/exponent arithmetic; a larger fixed constant may
    # be needed for the stated input component width in the fused pipeline.
    w = max(4 * (L + 1) + 4 * P + 64, (c + 4) * L + 64, key_bits + 1, r + 1)
    lanes = w // r
    words = ceil_div(B, lanes)
    # Coarse scalar word-operation bounds for complete cold construction.
    # Store log2 bounds, never the exponential number of table rows.
    first_per_row = 512 * (g + 1) * (B + 1)
    phase_work = 128 * (P + 1) ** 2 * (Q1 + 1)
    cold_log_upper = max(key_bits + ceil_log2(first_per_row), ceil_log2(phase_work)) + 1
    memory_per_row = 2 * words + 4  # both coordinates and bounded row metadata
    memory_log_upper = max(key_bits + ceil_log2(memory_per_row), ceil_log2(2 * Q1 + 8)) + 1
    # pi<4, sqrt(2)<3/2 give a rational rigorous decoder-error upper bound.
    decoder_error_upper = Fraction(4, Q0) + Fraction(4 * (B - 1), Q1) + Fraction(1, 1 << b) + Fraction(3, 4 * H)
    assert decoder_error_upper <= eta / 4
    assert 4 * logarithm_upper <= K * (eta / 4) ** 2
    assert key_bits * gamma.denominator <= gamma.numerator * (L - 1)
    assert r * lanes <= w and 2 * H * G < 1 << r
    assert result["trig_parameter_max_integer_bits"] < w
    # R=ceil(N/B). If B<=N, R<=2N/B; this includes the final partial block.
    descriptor_ratio_bound = Fraction(2 * K, B)
    packed_add_ratio_bound = Fraction(4 * G * words, B)
    lookup_ratio_bound = Fraction(2 * G, B)
    # Check B<=N by bit length, without creating 2**L.
    block_fits = B.bit_length() <= L - 1  # B<2**(L-1)<=N, conservatively
    result.update({"status": "valid_growing_schedule" if block_fits else "finite_base_regime_B_gt_N",
                   "sample_count": K, "groups": G, "key_bits": key_bits,
                   "table_rows_log2": key_bits, "guarded_lane_bits": r,
                   "word_bits": w, "lanes_per_word": lanes, "words_per_row_per_coordinate": words,
                   "deterministic_error_upper": encode_fraction(decoder_error_upper),
                   "total_error_upper": encode_fraction(eta / 4 + decoder_error_upper),
                   "descriptor_operations_over_N_upper": encode_fraction(descriptor_ratio_bound),
                   "packed_adds_over_N_upper": encode_fraction(packed_add_ratio_bound),
                   "packed_adds_over_N_tau_upper": encode_fraction(packed_add_ratio_bound / time_factor),
                   "row_lookups_over_N_upper": encode_fraction(lookup_ratio_bound),
                   "cold_construction_log2_work_upper": cold_log_upper,
                   "cold_memory_log2_words_upper": memory_log_upper,
                   "cold_work_below_N_certified": cold_log_upper <= L - 1,
                   "cold_memory_below_N_certified": memory_log_upper <= L - 1,
                   "fusion": "same schedule applies to integer residual rho; multiply error scale by L_box(rho)/(n*sqrt(N))"})
    return result


if __name__ == "__main__":
    import json
    print(json.dumps([plan(L) for L in (32, 64, 128, 256, 1024, 65536)], indent=2))
