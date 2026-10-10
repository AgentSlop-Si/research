"""Focused independent checks of the root's fusion interface and edge cases."""
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import control_variate as candidate
from verify_fusion_identity import fit as reference_fit


class StubDecoder:
    """An intentionally artificial decoder isolates output scaling algebra."""
    N = 3
    K = 1
    w = 128
    called = False

    def decode(self, samples):
        self.called = True
        return {"integer_outputs": [(2, -1), (3, 4), (-5, 6)],
                "denominator": 7, "error_bound": 0.125, "counts": {}}


def main():
    checks = []
    examples = [
        [(0, 0)], [(7, -4)], [(1, 2), (3, 4)],
        [(1, 0), (2, 0), (2, 0)],  # A genuinely fractional retained mean.
        [(1, 1), (-1, -1), (0, 0)],  # q=1 nonzero residual, zero mean.
        [(100, 0)] + [(0, 0)] * 6,  # Mean worsens l1; must select zero.
        [(9, 2), (-4, 7), (0, -1), (2, 0),
         (0, 2), (-4, 0), (1, -1), (2, 0),
         (0, 3), (-5, 0), (1, -1), (2, 0)],
        [(2**120, -(2**119)), (2**120 + 1, -(2**119) + 3),
         (2**120 - 2, -(2**119) + 1)],
    ]
    for xs in examples:
        result = candidate.fit_periodic(xs)
        residual, spectrum, scale = reference_fit(xs, scaled=True)
        assert result["residual"] == residual and result["scale"] == scale
        assert all(result["baseline_spectrum"].get(i, (0, 0)) == v for i, v in enumerate(spectrum))
        assert result["residual_numerator_mass"] <= scale * result["input_mass"]
        checks.append({"check": "independent_fit_identity", "N": len(xs)})
    assert candidate.fit_periodic(examples[5])["chosen_sums"] == [[0, 0]]
    mixed = candidate.fit_periodic(examples[6])
    assert mixed["chosen_sums"][0] == [0, 7]
    assert mixed["chosen_sums"][1] == [-13, 0]
    checks.append({"check": "independent_coordinate_rollback"})

    # Explicit Gaussian rotations, including a negative-sign fourth root.
    spectrum = candidate.quarter_spectrum([(1, 2), (3, 4), (5, 6), (7, 8)], 3)
    assert spectrum == {0: (16, 20), 3: (-8, 0), 6: (-4, -4), 9: (0, -8)}
    checks.append({"check": "quarter_turn_sign_and_frequency_support"})

    exact_input = [(2, -1), (5, 3), (0, 7), (-4, -2)] * 3
    exact = candidate.fuse(exact_input)
    assert exact["exact"] and not exact["failed"] and exact["denominator"] == 1
    assert exact["decoder_counts"] is None and exact["sampler_counts"] is None
    assert exact["integer_outputs"][1] == (0, 0)
    assert exact["output_component_writes"] == 2 * len(exact_input) + 2 * exact["fit"]["period"]
    checks.append({"check": "zero_residual_exact_bypass"})

    xs = [(1, 0), (2, 0), (2, 0)]
    decoder = StubDecoder()
    with patch.object(candidate, "sample_atoms", return_value={"failed": False, "samples": [(0, 0)], "counts": {}}):
        output = candidate.fuse(xs, decoder)
    # n=3; rho=(-2,1,1); mass=4; denominator=3*7=21.
    # DC is corrected to the exact raw sum 5, independent of stub output.
    assert decoder.called and output["denominator"] == 21
    assert output["integer_outputs"] == [(105, 0), (12, 16), (-20, 24)]
    assert output["output_component_writes"] == 8
    checks.append({"check": "scaled_residual_denominator_and_exact_DC_override"})

    decoder = StubDecoder()
    with patch.object(candidate, "sample_atoms", return_value={"failed": True, "samples": [], "counts": {"sentinel": 1}}):
        output = candidate.fuse(xs, decoder)
    assert output["failed"] and not output["exact"] and not decoder.called
    assert output["sampler_counts"] == {"sentinel": 1}
    assert output["integer_outputs"] == [(0, 0)] * 3
    assert output["output_component_writes"] == 6
    checks.append({"check": "sampling_cap_failure_is_explicit_and_skips_decode"})

    # Check the stated conservative word-growth bound with a very large input
    # magnitude. This is a bit-growth check, not an asymptotic claim for
    # unrestricted integer magnitudes.
    xs = examples[-1]
    decoder = StubDecoder()
    with patch.object(candidate, "sample_atoms", return_value={"failed": False, "samples": [(0, 0)], "counts": {}}):
        output = candidate.fuse(xs, decoder)
    b = max(abs(v).bit_length() for p in xs for v in p)
    bound = b + 2 * len(xs).bit_length() + (7).bit_length() + 4
    assert max(abs(v).bit_length() for p in output["integer_outputs"] for v in p) <= bound
    assert output["required_word_bits"] >= bound
    checks.append({"check": "final_numerator_word_growth", "conservative_bits": bound})

    rejected = 0
    for xs in ([], [(1.5, 2)], [(True, 2)]):
        try:
            candidate.fit_periodic(xs)
        except ValueError:
            rejected += 1
        else:
            raise AssertionError("invalid input accepted")
    for wrong in (None, type("Wrong", (), {"N": 7})()):
        try:
            candidate.fuse([(1, 0), (2, 0), (2, 0)], wrong)
        except ValueError:
            rejected += 1
        else:
            raise AssertionError("missing/mismatched decoder accepted")
    checks.append({"check": "invalid_input_or_decoder_rejections", "count": rejected})
    report = {"status": "PASS", "checks": checks, "check_groups": len(checks),
              "source_sha256": hashlib.sha256(Path(candidate.__file__).read_bytes()).hexdigest(),
              "scope": "Independent edge/interface checks; stubs deliberately isolate algebra and failure semantics, not approximation accuracy."}
    Path("review_edge_results.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in ("status", "check_groups", "source_sha256")}))


if __name__ == "__main__":
    main()
