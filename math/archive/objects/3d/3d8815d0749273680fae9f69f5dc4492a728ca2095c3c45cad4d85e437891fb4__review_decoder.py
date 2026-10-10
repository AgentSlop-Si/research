"""Independent functional checks of sibling guarded_decoder implementation."""
from __future__ import annotations

import cmath
import hashlib
import json
import math
from pathlib import Path
import random
import sys
from fractions import Fraction

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "fft_wordram_decoder_research"))
from guarded_decoder import GuardedDecoder, WordAudit, _phasors
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "fft_wordram_integration"))
from sampling import sample_count_integer, sample_atoms


def main():
    rng = random.Random(93217)
    cases = []
    configurations = [
        # Meaningful precision, complete nontrivial table and a partial last block.
        dict(N=29, K=21, B=4, Q0=32, Q1=128, g=1, h=6),
        # Two atoms per key; several fields and words. This is a mechanics test.
        dict(N=73, K=202, B=64, Q0=4, Q1=4, g=2, h=10),
        # Boundary phases and sample groups, with all contributions identical.
        dict(N=37, K=14, B=5, Q0=4, Q1=8, g=2, h=5),
    ]
    for configuration in configurations:
        n, k = configuration["N"], configuration["K"]
        decoder = GuardedDecoder(n, k, block_size=configuration["B"],
                                 phase_grid=configuration["Q0"],
                                 slope_grid=configuration["Q1"],
                                 group_size=configuration["g"],
                                 lane_step_bits=configuration["h"],
                                 table_mode="eager")
        # Table construction must genuinely include all keys.
        assert isinstance(decoder.table, list), "eager table must be a directly indexed array"
        assert len(decoder.table) == decoder.D ** decoder.g
        samples = [(rng.randrange(n), rng.randrange(4)) for _ in range(k)]
        if n == 37:
            samples = [(n - 1, 3)] * k
        output = decoder.decode(samples)
        assert len(output["integer_outputs"]) == n
        exact = [sum((1j ** phase) * cmath.exp(-2j * math.pi * j * m / n)
                     for j, phase in samples) / k for m in range(n)]
        reconstructed = [complex(a, b) / output["denominator"]
                         for a, b in output["integer_outputs"]]
        error = max(abs(a - b) for a, b in zip(reconstructed, exact))
        assert error <= output["error_bound"] + 1e-12
        assert output["counts"]["max_operand_bits"] <= decoder.w
        assert output["counts"]["online"]["output_write"] == 2 * n
        cases.append({**configuration, "observed_error": error,
                      "bound": output["error_bound"],
                      "table_rows": len(decoder.table),
                      "words_per_row_per_component": decoder.words_per_row,
                      "max_operand_bits": output["counts"]["max_operand_bits"],
                      "word_bits": decoder.w})
    trig_checks = 0
    trig_max_ratios = []
    for bits in (8, 16, 24, 40):
        words = WordAudit(512)
        table, scale, info = _phasors(256, bits, words)
        max_error = max(abs(complex(a / scale, b / scale) - cmath.exp(2j * math.pi * t / 256))
                        for t, (a, b) in enumerate(table))
        assert max_error <= info["complex_error_bound"] + 1e-14
        trig_max_ratios.append({"bits": bits, "error": max_error,
                                "bound": info["complex_error_bound"]})
        trig_checks += len(table)
    parameter_checks = 0
    for n in (1, 3, 32, 1000, 1 << 40):
        for error in (Fraction(1, 2), Fraction(1, 7)):
            for failure in (Fraction(1, 3), Fraction(1, 1 << 50)):
                for group in (1, 3, 17):
                    count = sample_count_integer(n, error, failure, group)
                    ratio = 4*n/failure
                    upper = (ratio.numerator + ratio.denominator - 1) // ratio.denominator
                    log_upper = (upper - 1).bit_length()
                    assert count % group == 0
                    assert count * error * error >= 4*log_upper
                    parameter_checks += 1
    sampled = sample_atoms([(0, 0), (2, -3), (-1, 4)], 101,
                           cap_failure=Fraction(1, 1000000))
    assert not sampled["failed"]
    assert set(sampled["samples"]) <= {(1, 0), (1, 3), (2, 2), (2, 1)}
    cap = sampled["counts"]["rejection_cap"]
    assert Fraction(101, 1 << cap) <= Fraction(1, 1000000)
    report = {"status": "PASS", "decoder_cases": cases,
              "reviewed_source_sha256": hashlib.sha256((Path(__file__).resolve().parent.parent / "fft_wordram_decoder_research" / "guarded_decoder.py").read_bytes()).hexdigest(),
              "reviewed_sampler_sha256": hashlib.sha256((Path(__file__).resolve().parent.parent / "fft_wordram_integration" / "sampling.py").read_bytes()).hexdigest(),
              "exact_sampler_parameter_checks": parameter_checks,
              "trig_reference_comparisons": trig_checks,
              "trig_results": trig_max_ratios,
              "note": "Direct complex reference is binary64; certified trig bound rests on the algebraic proof."}
    Path(__file__).with_name("decoder_review_results.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "decoder_cases": len(cases), "trig_comparisons": trig_checks}))


if __name__ == "__main__":
    main()
