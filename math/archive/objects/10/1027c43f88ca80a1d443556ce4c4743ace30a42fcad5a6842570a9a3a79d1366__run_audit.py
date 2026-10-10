"""Audit the symbolic growing schedule and finite complete-table wide blocks."""
import cmath
from decimal import Decimal, localcontext
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import random
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "fft_wordram_decoder_research"))
sys.path.insert(0, str(HERE.parent / "fft_control_variate_fusion_research"))
from guarded_decoder import GuardedDecoder, _phasors, _trig_parameters, WordAudit
from control_variate import fuse
from parameter_schedule import plan


def as_fraction(value):
    return Fraction(value["numerator"], value["denominator"])


def main():
    schedules = []
    for mode in ("linear", "subfft"):
        for c in (0, 1, 3):
            for L in (8, 32, 64, 128, 256, 1024, 4096, 65536, 1 << 20, 1 << 24):
                row = plan(L, failure_power=c, mode=mode)
                if row["status"] == "valid_growing_schedule":
                    assert row["key_bits"] <= L // 2
                    assert as_fraction(row["total_error_upper"]) <= as_fraction(row["target_error_factor"]) / 2
                    if L >= 256:
                        assert row["cold_work_below_N_certified"]
                        assert row["cold_memory_below_N_certified"]
                    # Widths in this finite audit stay within these conservative
                    # uniform constants; the proof gives the general bounds.
                    ell = row["log2_log2_N_ceiling"]
                    assert row["descriptor_bits"] <= 12 * ell + 30
                    assert row["trig_working_precision"] <= 8 * ell + 64
                    assert row["trig_degree"] <= 8 * ell + 64
                schedules.append(row)
    for L in (128, 256, 1024, 65536, 1 << 20):
        for tau in (Fraction(1), Fraction(L, 2), Fraction(L, max(1, L.bit_length() - 1) ** 2), Fraction(L)):
            if tau < 1:
                continue
            row = plan(L, mode="frontier", tau=tau)
            if row["status"] == "valid_growing_schedule":
                assert as_fraction(row["packed_adds_over_N_tau_upper"]) < 100_000
                assert as_fraction(row["total_error_upper"]) <= as_fraction(row["target_error_factor"]) / 2
            schedules.append(row)

    rng = random.Random(550124)
    records = []
    configurations = [
        # Wide B > log2 N, complete g=2 table, multiple packed words. Coarse
        # grids keep literal table enumeration finite; these are functional
        # tests, not points in the eventual asymptotic N**gamma regime.
        dict(N=129, sample_count=256, block_size=16, phase_grid=4,
             slope_grid=64, group_size=2, lane_step_bits=4,
             trig_bits=8, word_bits=112),
        # More accurate wide-block complete table, still finite enough to run.
        dict(N=257, sample_count=1024, block_size=32, phase_grid=32,
             slope_grid=1024, group_size=1, lane_step_bits=5,
             trig_bits=24),
    ]
    decoder_output_checks = 0
    fusion_checks = 0
    for config in configurations:
        decoder = GuardedDecoder(table_mode="eager", **config)
        assert isinstance(decoder.table, list)
        assert len(decoder.table) == decoder.table_entries
        assert decoder.words_per_row >= 2
        N, K = decoder.N, decoder.K
        for family in ("coherent", "random", "opposite_pairs"):
            if family == "coherent":
                samples = [(N - 1, 3)] * K
            elif family == "opposite_pairs":
                samples = [(i // 2 % N, 2 * (i % 2)) for i in range(K)]
            else:
                samples = [(rng.randrange(N), rng.randrange(4)) for _ in range(K)]
            result = decoder.decode(samples)
            reference = [sum((1j) ** phase * cmath.exp(-2j * math.pi * j * m / N)
                             for j, phase in samples) / K for m in range(N)]
            error = max(abs(a - b) for a, b in zip(reference, result["values"]))
            assert error <= result["error_bound"] + 1e-10
            assert result["counts"]["max_operand_bits"] <= decoder.w
            if family == "opposite_pairs":
                assert all(a == 0 and b == 0 for a, b in result["integer_outputs"])
            records.append({"kind": "complete_table_decoder", "family": family,
                            "parameters": result["parameters"], "max_error": error,
                            "error_bound": result["error_bound"],
                            "cold_operations_counted": sum(decoder.cold_counts.values()),
                            "online_operations_counted": sum(result["counts"]["online"].values())})
            decoder_output_checks += N
        # A real fresh-input fusion call reuses the already constructed table
        # here, but its complete cold ledger is included again in the record.
        coordinates = [(1000 + rng.randrange(-3, 4), -500 + rng.randrange(-2, 3)) for _ in range(N)]
        answer = fuse(coordinates, decoder, seed=98231, cap_failure=Fraction(1, 100))
        assert not answer["failed"]
        actual = [complex(a / answer["denominator"], b / answer["denominator"])
                  for a, b in answer["integer_outputs"]]
        exact = [sum(complex(*pair) * cmath.exp(-2j * math.pi * j * m / N)
                     for j, pair in enumerate(coordinates)) for m in range(N)]
        residual_mass = answer["fit"]["residual_numerator_mass"] / answer["fit"]["scale"]
        sample_budget = math.sqrt(4 * math.log(4 * N / 0.01) / K)
        allowance = (sample_budget + decoder.decoder_bound) * residual_mass
        error = max(abs(a - b) for a, b in zip(actual, exact))
        assert error <= allowance + 1e-6
        for m, pair in answer["fit"]["exact_corner_spectrum"].items():
            assert answer["integer_outputs"][m] == tuple(v * answer["denominator"] for v in pair)
        records.append({"kind": "complete_table_fusion", "N": N, "K": K,
                        "max_error": error, "probabilistic_allowance": allowance,
                        "residual_mass": residual_mass, "input_mass": answer["fit"]["input_mass"],
                        "cold_operations_counted": sum(decoder.cold_counts.values()),
                        "required_word_bits": answer["required_word_bits"],
                        "exact_corner_outputs": answer["fit"]["period"]})
        fusion_checks += N

    trig = []
    for bits in (8, 16, 24, 40, 64):
        d, P = _trig_parameters(bits)
        W = WordAudit(4 * P + 128)
        values, scale, info = _phasors(64, bits, W)
        # Separate high-precision Decimal sine/cosine series are an oracle
        # only. The production phasors use bounded integer Machin/Taylor.
        with localcontext() as context:
            context.prec = 100
            decimal_pi = Decimal("3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679")
            error = Decimal(0)
            for m, (a, b) in enumerate(values):
                angle = 2 * decimal_pi * m / 64
                square = angle * angle
                real, imaginary = Decimal(1), angle
                real_term, imaginary_term = real, imaginary
                for n in range(1, 150):
                    real_term *= -square / ((2 * n - 1) * (2 * n))
                    imaginary_term *= -square / ((2 * n) * (2 * n + 1))
                    real += real_term
                    imaginary += imaginary_term
                distance = ((Decimal(a) / scale - real) ** 2 + (Decimal(b) / scale - imaginary) ** 2).sqrt()
                error = max(error, distance)
            assert error <= Decimal(2) ** (-bits)
            trig.append({"target_bits": bits, "working_bits": P, "degree": d,
                         "maximum_error": str(error), "certified_bound": str(Decimal(2) ** (-bits)),
                         "largest_operand_bits": W.max_bits, "word_bits": W.width})

    dependencies = [HERE / "parameter_schedule.py", HERE / "run_audit.py",
                    HERE.parent / "fft_wordram_decoder_research" / "guarded_decoder.py",
                    HERE.parent / "fft_control_variate_fusion_research" / "control_variate.py"]
    result = {"status": "PASS", "schedule_cases": len(schedules),
              "complete_table_configurations": len(configurations),
              "decoder_output_comparisons": decoder_output_checks,
              "fusion_output_comparisons": fusion_checks,
              "certified_trig_configurations": len(trig), "schedules": schedules,
              "finite_records": records, "trig": trig,
              "source_sha256": {str(p.relative_to(HERE.parent)): hashlib.sha256(p.read_bytes()).hexdigest() for p in dependencies},
              "scope": "Symbolic schedule does not allocate N or its table. Finite complete-table tests verify implementation, not practical asymptotic crossover."}
    (HERE / "results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ("status", "schedule_cases", "complete_table_configurations", "decoder_output_comparisons", "fusion_output_comparisons", "certified_trig_configurations")}))


if __name__ == "__main__":
    main()
