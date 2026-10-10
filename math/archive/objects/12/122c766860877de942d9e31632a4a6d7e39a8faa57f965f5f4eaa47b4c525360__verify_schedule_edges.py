"""Independent finite endpoint checks for ceil(log2 N) schedule flags."""
import hashlib
import json
from pathlib import Path

from parameter_schedule import plan


def main():
    checks = 0
    transitions = []
    for mode in ("linear", "subfft"):
        last = None
        for L in range(2, 161):
            row = plan(L, mode=mode)
            # These are <=161-bit integers, not input arrays. The main planner
            # never constructs N, including its cases with L>10 million.
            smallest_N = (1 << (L - 1)) + 1
            largest_N = 1 << L
            if row["group_size"]:
                assert (1 << (2 * row["key_bits"])) <= smallest_N
                if row["status"] == "valid_growing_schedule":
                    assert row["block_size"] <= smallest_N <= largest_N
                    checks += 1
                if row["cold_work_below_N_certified"]:
                    assert (1 << row["cold_construction_log2_work_upper"]) <= smallest_N
                    checks += 1
                if row["cold_memory_below_N_certified"]:
                    assert (1 << row["cold_memory_log2_words_upper"]) <= smallest_N
                    checks += 1
            else:
                assert row["status"] == "finite_base_regime_g_zero"
                checks += 1
            state = (row["status"], row.get("cold_work_below_N_certified"),
                     row.get("cold_memory_below_N_certified"))
            if state != last:
                transitions.append({"mode": mode, "L": L, "status": row["status"],
                                    "group_size": row["group_size"],
                                    "cold_work_below_N": row.get("cold_work_below_N_certified"),
                                    "cold_memory_below_N": row.get("cold_memory_below_N_certified")})
                last = state
    report = {"status": "PASS", "planner_inputs": 318,
              "endpoint_and_flag_checks": checks, "transitions": transitions,
              "source_sha256": hashlib.sha256(Path("parameter_schedule.py").read_bytes()).hexdigest(),
              "scope": "Cheap independent checks supplement the already completed eager decoder audit; no wide decoder rerun required."}
    Path("schedule_edge_results.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in ("status", "planner_inputs", "endpoint_and_flag_checks")}))


if __name__ == "__main__":
    main()
