"""Fresh integer controls. No source/predecessor program is imported or executed."""

import json
from pathlib import Path


def unpack(x, radix, lanes):
    out = []
    for _ in range(lanes):
        out.append(x % radix)
        x //= radix
    assert x == 0
    return out


def pack(xs, radix):
    answer = 0
    for x in reversed(xs):
        assert 0 <= x < radix
        answer = answer * radix + x
    return answer


def h(a, b, radix, variant):
    # Arbitrary total local maps, deliberately not a numerical FFT oracle.
    if variant == 0:
        return (a + 3 * b) % radix, (2 * a + b) % radix
    return (a ^ b), ((a * b + a + 1) % radix)


def direct(a, b, radix, lanes, variant):
    aa = unpack(a, radix, lanes)
    bb = unpack(b, radix, lanes)
    ys = [h(x, y, radix, variant) for x, y in zip(aa, bb)]
    return pack([z[0] for z in ys], radix), pack([z[1] for z in ys], radix)


cases = []
total_pairs = 0
for radix, lanes in [(2, 4), (2, 8), (4, 4), (8, 2)]:
    half = lanes // 2
    field = radix ** half
    state = radix ** lanes
    bits = (field - 1).bit_length()
    mask = field - 1
    for variant in [0, 1]:
        table = []
        for key in range(field * field):
            a, b = key & mask, key >> bits
            y, z = direct(a, b, radix, half, variant)
            table.append(y | (z << bits))
        assert len(table) == state
        for a in range(state):
            for b in range(state):
                z0 = table[(a & mask) | ((b & mask) << bits)]
                z1 = table[(a >> bits) | ((b >> bits) << bits)]
                y = (z0 & mask) | ((z1 & mask) << bits)
                z = (z0 >> bits) | ((z1 >> bits) << bits)
                assert (y, z) == direct(a, b, radix, lanes, variant)
        total_pairs += state * state
        cases.append({"radix": radix, "lanes": lanes, "map_variant": variant,
                      "pairs_checked": state * state,
                      "original_entries": state * state,
                      "replacement_entries": state})


parameter_cases = []
for v in [5120, 5888, 6912, 11904, 16384, 65536, 1048576]:
    for t in [2, 8, 16, 53]:
        p = t + 10 + v.bit_length()
        k = (2 * v + p + 5).bit_length()
        b = 2 * (p + k + 1)
        if b * 64 > v:
            continue
        limit = v // (16 * b)
        lanes = 1 << (limit.bit_length() - 1)
        g = p + 10
        log_s = b * lanes
        assert lanes >= 4
        assert g - log_s <= 2 - 7 * p - 8 * k
        assert g - log_s < 0
        assert 2 * log_s <= v // 8
        assert 32 * log_s > v
        # Exact entry identities, evaluated as integers.
        q, s, r = 1 << g, 1 << log_s, 1 << b
        d = lanes.bit_length() - 1
        old = s * s + (q - 1 + d) * s + q * r + r * r
        new = (q + d) * s + q * r + r * r
        assert old - new == s * s - s
        parameter_cases.append({"v": v, "t": t, "p": p, "k": k,
                                "b": b, "P": lanes, "g": g,
                                "log2_S": log_s,
                                "log2_Q_over_S": g - log_s})


result = {"status": "pass", "split_layout_cases": cases,
          "total_pair_controls": total_pairs,
          "parameter_cases": parameter_cases,
          "scope": ["Exact layout identity for arbitrary total local maps.",
                    "Exact finite-parameter exponent and entry-count controls.",
                    "No trigonometric accuracy, benchmark, or full executor claim.",
                    "No source/predecessor code imported or executed."]}
destination = Path(__file__).with_name("FRESH_REVIEW_RESULTS.json")
destination.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"status": result["status"], "pair_controls": total_pairs,
                  "parameter_cases": len(parameter_cases)}, sort_keys=True))
