"""Independent accounting audit; imported upload is never modified."""
from __future__ import annotations

from fractions import Fraction
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "fft_new_fusion_materials_20261009" / "shrinking" / "prototype.py"


def instrument_original():
    spec = importlib.util.spec_from_file_location("shrinking_v4_review_target", SOURCE)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    original = module.pack_nonnegative_lanes
    rows = []
    for n, b, k, g in ((256, 32, 32, 2), (257, 32, 32, 2), (4096, 128, 128, 2)):
        counter = {"calls": 0, "scalar_lane_visits": 0}

        def counted(values, field_bits, lanes_per_word):
            counter["calls"] += 1
            counter["scalar_lane_visits"] += len(values)
            return original(values, field_bits, lanes_per_word)

        module.pack_nonnegative_lanes = counted
        parameters = module.choose_params(n, k, B=b, g_override=g)
        # A single repeatedly hit cached row isolates repacking from table generation.
        samples = [(0, 0)] * parameters.k
        output, counts = module.packed_decode(n, 1.0, samples, parameters)
        blocks = (n+b-1)//b
        assert counts["table_entries"] == 1
        assert counter["calls"] == 2*blocks*parameters.G
        assert counter["scalar_lane_visits"] == 2*blocks*parameters.G*b
        assert counter["scalar_lane_visits"] >= 2*n*parameters.G
        assert max(abs(z - 1/math.sqrt(n)) for z in output) < 1e-12
        rows.append({"N": n, "B": b, "K": parameters.k, "g": g,
                     "G": parameters.G, "cached_rows": counts["table_entries"],
                     "lookup_count": counts["lookup_count"],
                     "reported_packed_word_adds": counts["packed_word_adds"],
                     "actual_scalar_packing_lane_visits": counter["scalar_lane_visits"],
                     "packing_calls": counter["calls"],
                     "minimum_2NG": 2*n*parameters.G})
    module.pack_nonnegative_lanes = original
    return rows


def power_two_at_least(value):
    return 1 << (math.ceil(value)-1).bit_length()


def check_tradeoffs():
    rows = []
    for L in (128, 512, 2048, 8192):
        ell = math.log2(L)
        for mode in ("linear", "uploaded_subfft", "slower_h_subfft"):
            if mode == "linear":
                tau = 1.0
            elif mode == "uploaded_subfft":
                tau = L/ell
            else:
                tau = L/math.log2(ell)
            k0 = math.ceil(16*tau*L*L/(ell*ell))
            B = k0
            eta = math.sqrt(L/k0)
            Q0 = power_two_at_least(64/eta)
            Q1 = power_two_at_least(B*Q0)
            p = (Q0.bit_length()-1)+(Q1.bit_length()-1)
            g = L//(2*p)
            if not g:
                rows.append({"L": L, "mode": mode, "base_case": True})
                continue
            K = g*((k0+g-1)//g)
            G = K//g
            H = power_two_at_least(32/eta)
            q = (2*H*G).bit_length()
            w = 8*L
            lanes = w//q
            W = (B+lanes-1)//lanes
            N = 1 << L
            R = (N+B-1)//B
            assert p*g <= L//2
            assert q <= w
            assert W*w <= w+2*B*q
            raw = R*K+2*R*G*W
            upper = (Fraction(N,B)+1)*(K+2*G*(1+Fraction(2*B*q,w)))
            assert raw <= upper
            assert R*B >= N and R*B < N+B
            rows.append({"L": L, "mode": mode, "K": K, "B": B,
                         "p": p, "g": g, "G": G, "q": q, "W": W,
                         "descriptor_work_over_N": float(Fraction(R*K,N)),
                         "packed_adds_over_N": float(Fraction(2*R*G*W,N)),
                         "modeled_work_over_N_tau": float(Fraction(raw,N))/tau,
                         "sampling_scale": eta,
                         "target_error_scale": ell/math.sqrt(tau*L),
                         "key_bits_fraction_of_L": p*g/L})
    return rows


def exact_norm_checks():
    checks = 0
    ratios = []
    for n in (8, 32, 128):
        residual = [(1 if i % 2 else -1, 0) if i < n//4 else (0,0)
                    for i in range(n)]
        template = [(7, -3)]*n
        x = [(a+c,b+d) for (a,b),(c,d) in zip(template,residual)]
        Lx = sum(abs(a)+abs(b) for a,b in x)
        Lr = sum(abs(a)+abs(b) for a,b in residual)
        x2 = sum(a*a+b*b for a,b in x)
        r2 = sum(a*a+b*b for a,b in residual)
        assert Lr <= Lx
        assert Lx*Lx <= 2*n*x2
        assert Lr*Lr <= 2*n*r2
        ratios.append({"N": n, "Lx": Lx, "Lres": Lr,
                       "certified_mass_improvement": str(Fraction(Lr,Lx))})
        checks += 3
    return {"integer_inequality_checks": checks, "control_variate_examples": ratios}


def main():
    report = {"status": "PASS",
              "uploaded_source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
              "uploaded_research_sha256": hashlib.sha256(SOURCE.with_name("RESEARCH.md").read_bytes()).hexdigest(),
              "review_script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "repacking_instrumentation": instrument_original(),
              "exact_ceiling_tradeoff_checks": check_tradeoffs(),
              "norm_and_control_variate_checks": exact_norm_checks(),
              "scope": "The prototype's hidden repacking cost is demonstrated; corrected-theorem cost is analytic, not a timing benchmark."}
    Path(__file__).with_name("results.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"status": "PASS", "repacking_cases": len(report["repacking_instrumentation"]),
                      "tradeoff_cases": len(report["exact_ceiling_tradeoff_checks"]),
                      "norm_checks": report["norm_and_control_variate_checks"]["integer_inequality_checks"]}))


if __name__ == "__main__":
    main()
