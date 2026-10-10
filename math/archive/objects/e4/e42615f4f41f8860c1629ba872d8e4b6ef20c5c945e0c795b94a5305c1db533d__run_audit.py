"""Deterministic full-table and packed arithmetic decoder audit."""
import cmath
import hashlib
import json
import math
import random
from pathlib import Path

from guarded_decoder import GuardedDecoder, _phasors, _trig_parameters, WordAudit, asymptotic_parameters


def main():
    rng = random.Random(928337)
    cases = []
    # Every case enumerates its entire table, including unused rows.
    configs = [
        dict(N=1, K=8, block_size=1, phase_grid=4, slope_grid=4, group_size=2),
        dict(N=17, K=30, block_size=4, phase_grid=16, slope_grid=64, group_size=1),
        dict(N=32, K=40, block_size=2, phase_grid=8, slope_grid=8, group_size=2),
        dict(N=65, K=112, block_size=4, phase_grid=32, slope_grid=128, group_size=1),
        dict(N=257, K=1000, block_size=80, phase_grid=4, slope_grid=16,
             group_size=2, lane_step_bits=2, trig_bits=8, word_bits=112),
    ]
    output_checks = 0
    for config in configs:
        config = dict(config)
        N, K = config.pop("N"), config.pop("K")
        decoder = GuardedDecoder(N, K, table_mode="eager", **config)
        assert len(decoder.table) == decoder.table_entries
        for family in ("zero_index", "single_atom", "random", "coherent", "alternating"):
            if family == "zero_index":
                samples = [(0, i % 4) for i in range(K)]
            elif family == "single_atom":
                samples = [(N - 1, 3)] * K
            elif family == "random":
                samples = [(rng.randrange(N), rng.randrange(4)) for _ in range(K)]
            elif family == "coherent":
                samples = [(i % N, (i // max(1, N // 4)) % 4) for i in range(K)]
            else:
                samples = [(N // 2, i % 2 * 2) for i in range(K)]
            result = decoder.decode(samples)
            reference = [sum((1j) ** phase * cmath.exp(-2j * math.pi * j * m / N)
                             for j, phase in samples) / K for m in range(N)]
            err = max(abs(a - b) for a, b in zip(result["values"], reference))
            assert err <= result["error_bound"] + 1e-11, (config, family, err)
            assert result["counts"]["max_operand_bits"] <= result["parameters"]["word_bits"]
            # Unpack exactly and compare with a scalar sum of the actual table
            # lanes, independently rebuilding each block key.
            integers = []
            for m0 in range(0, N, decoder.B):
                scalar = [[0, 0] for _ in range(decoder.B)]
                for start in range(0, K, decoder.g):
                    key = 0
                    for pos, (j, phase) in enumerate(samples[start:start + decoder.g]):
                        a0 = (phase * (decoder.Q0 // 4) - (2 * decoder.Q0 * (j * m0 % N) + N) // (2 * N)) % decoder.Q0
                        # Parentheses implement minus the nearest integer,
                        # including the away-from-zero half-tie convention.
                        a1 = (-((2 * decoder.Q1 * j + N) // (2 * N))) % decoder.Q1
                        desc = a0 + a1 * decoder.Q0
                        key += desc * decoder.D ** pos
                    row = decoder.table[key]
                    for t in range(decoder.B):
                        z, lane = divmod(t, decoder.L)
                        for c in range(2):
                            scalar[t][c] += (row[c][z] >> (lane * decoder.r)) & decoder.mask
                for t in range(min(decoder.B, N - m0)):
                    integers.append(tuple(v - decoder.G * decoder.H for v in scalar[t]))
            assert integers == result["integer_outputs"]
            output_checks += N
            cases.append({"N": N, "K": K, "family": family, "maximum_error": err,
                          "error_bound": result["error_bound"], "parameters": result["parameters"],
                          "counts": result["counts"]})
    trig_checks = []
    for bits in (8, 16, 24, 40):
        _, P = _trig_parameters(bits)
        W = WordAudit(4 * P + 128)
        values, S, info = _phasors(128, bits, W)
        error = max(abs(complex(a / S, b / S) - cmath.exp(2j * math.pi * i / 128))
                    for i, (a, b) in enumerate(values))
        assert error < info["complex_error_bound"], (bits, error)
        trig_checks.append({"bits": bits, "max_error": error, "bound": info["complex_error_bound"]})
    parameters = []
    for logN in (32, 64, 128, 256, 1024, 4096):
        p = asymptotic_parameters(1 << logN, 0.5)
        if p:
            descriptor_bits = p["phase_grid"].bit_length() + p["slope_grid"].bit_length() - 2
            assert descriptor_bits * p["group_size"] <= logN // 2
        parameters.append({"log2_N": logN, "epsilon": 0.5, "parameters": p})
    report = {"status": "PASS", "full_table_configurations": len(configs),
              "decoded_sample_lists": len(cases), "output_checks": output_checks,
              "trigonometric_table_checks": trig_checks, "asymptotic_tuning": parameters,
              "cases": cases,
              "source_sha256": hashlib.sha256(Path("guarded_decoder.py").read_bytes()).hexdigest(),
              "limitations": ["Python timings do not establish an asymptotic speedup.",
                              "Finite full-table configurations intentionally differ from the eventual asymptotic schedule.",
                              "Only the deterministic sample decoder is tested here; upstream sampling is integrated separately.",
                              "Counters are selected explicit word primitives; theorem also charges control/index overhead."]}
    Path("results.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in ("status", "full_table_configurations", "decoded_sample_lists", "output_checks")}))


if __name__ == "__main__":
    main()
