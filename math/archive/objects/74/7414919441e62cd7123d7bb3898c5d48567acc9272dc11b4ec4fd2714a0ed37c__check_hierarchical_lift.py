#!/usr/bin/env python3
"""Exact deterministic hierarchical geometry controls; no Fourier fitting."""
from pathlib import Path
import json
import random
import time
from check_n16_outer_gate import LABELS, PRIME, pivots
from check_lift_defects import cover_and_splice, project, fiber, fold, apply_green

HERE = Path(__file__).resolve().parent


def cover(a, b, label):
    axis, c, sign = label
    out = []
    for v in range(a * b):
        x, y = divmod(v, b)
        if axis == "H":
            x = (x + sign * (2 * y + c)) % a
        else:
            y = (y + sign * (2 * x + c)) % b
        out.append(x * b + y)
    return out


def lift(ts, ps, a, b, label):
    n = a * b
    assert ps[0] != ts[0], "Chosen-base invariant: zero is already an edited tail"
    eta = [0] * n
    hs = 0
    for v in range(n):
        eta[ts[v]] = ps[v]
        hs += ts[v] != ps[v]
    assert sum(v != w for v, w in enumerate(eta)) == hs
    tl = cover(2 * a, 2 * b, label)
    q = []
    for v, target in enumerate(tl):
        x, y = divmod(target, 2 * b)
        low = (x % a) * b + y % b
        nx, ny = divmod(eta[low], b)
        lifted = (nx + (x // a) * a) * (2 * b) + ny + (y // b) * b
        q.append(lifted)
        assert project(lifted, a, b) == ps[project(v, a, b)]
    h0 = sum(v != w for v, w in zip(q, tl))
    assert h0 == 4 * hs
    seen, tails, lengths = bytearray(4 * n), [], []
    for v in range(4 * n):
        if seen[v]:
            continue
        w, length, chosen = v, 0, None
        while not seen[w]:
            seen[w] = 1
            length += 1
            if project(w, a, b) == 0:
                chosen = w if chosen is None else min(chosen, w)
            w = q[w]
        assert w == v and chosen is not None and length % n == 0
        tails.append(chosen)
        lengths.append(length)
    assert len(tails) <= 4
    tails.sort()
    heads = [q[v] for v in tails]
    for j, v in enumerate(tails):
        q[v] = heads[(j + 1) % len(tails)]
    assert all(project(q[v], a, b) == ps[project(v, a, b)] for v in range(4 * n))
    seen, v = bytearray(4 * n), 0
    for _ in range(4 * n):
        assert not seen[v]
        seen[v] = 1
        v = q[v]
    assert v == 0
    hl = sum(v != w for v, w in zip(q, tl))
    assert hl <= 4 * hs + 4
    assert q[0] != tl[0]
    assert all((q[v] != tl[v]) == (ps[project(v, a, b)] != ts[project(v, a, b)])
               for v in range(4 * n))
    assert hl == 4 * hs
    return tl, q, {"small_N": n, "large_N": 4 * n, "label": label,
                   "small_edits": hs, "initial_large_edits": h0,
                   "premerge_cycle_lengths": lengths, "merge_tails": tails,
                   "large_edits": hl, "edit_bound": 4 * hs + 4,
                   "exact_edit_count_4_times_small": hl == 4 * hs,
                   "edited_zero_invariant": True,
                   "quotient_defect_columns": 0, "hamiltonian_cycles": 1}


def small_chains():
    rng, records = random.Random(9371), []
    for seed_k in range(2, 7):
        b0 = 1 << (seed_k // 2)
        a0 = (1 << seed_k) // b0
        for label in LABELS:
            a, b = a0, b0
            t, p, reps = cover_and_splice(a, b, label)
            for level in range(1, 4):
                tt, pp, rec = lift(t, p, a, b, label)
                rec.update({"seed_N": a0 * b0, "level": level})
                if a * b <= 128:
                    tau = pow(2, -1, PRIME)
                    x = [rng.randrange(PRIME) for _ in range(4 * a * b)]
                    lhs = fold(apply_green(pp, [tau] * len(pp), x), a, b)
                    rhs = apply_green(p, [tau] * len(p), fold(x, a, b))
                    assert lhs == rhs
                    rec["exact_resolvent_commutation_checked"] = True
                records.append(rec)
                a, b, t, p = 2 * a, 2 * b, tt, pp
        print("small chain seed", a0 * b0, flush=True)
    return records


def threshold_bases():
    records = []
    for k in (17, 18):
        b = 1 << (k // 2)
        a = (1 << k) // b
        n = a * b
        total_small, total_large, details = 0, 0, []
        for label in LABELS:
            t, p, reps = cover_and_splice(a, b, label)
            tt, pp, rec = lift(t, p, a, b, label)
            total_small += rec["small_edits"]
            total_large += rec["large_edits"]
            details.append(rec)
            print("threshold", n, label, rec["large_edits"], flush=True)
        assert total_large == 4 * total_small
        d0 = 7936 if k == 17 else 11264
        assert total_small == 2 * d0
        # Sixteen times a conservative margin using the actual edit count.
        margin16 = 3 * (4 * n) - 24 * total_large
        assert margin16 > 0
        records.append({"base_N": n, "large_N": 4 * n, "base_total_edits": total_small,
                        "large_total_edits": total_large,
                        "positive_rational_margin_times_16": margin16, "details": details})
    return records


def margins():
    records = []
    for n0, d0, coefficient in ((1 << 17, 7936, 752), (1 << 18, 11264, 15344)):
        for level in range(101):
            power = 4 ** level
            n = n0 * power
            # Three times half-edit upper bound = 3*power*d0+16*(power-1).
            margin = 3 * n // 16 - 3 * power * d0 - 16 * (power - 1)
            assert margin == coefficient * power + 16 and margin > 0
            sharpened_margin = 3 * n // 16 - 3 * power * d0
            assert sharpened_margin == (coefficient + 16) * power
            if level <= 4:
                records.append({"N0": n0, "level": level, "N": n,
                                "previous_general_rational_margin_lower_bound": margin,
                                "sharpened_exact_edit_rational_margin_lower_bound": sharpened_margin})
    return {"levels_checked": "0..100 in both parity chains", "displayed": records}


def fourier_defect_controls():
    out = []
    for a, b in ((2, 2), (4, 2), (4, 4), (8, 4), (8, 8), (16, 8)):
        n = a * b
        z = pow(3, (PRIME - 1) // (4 * n), PRIME)
        assert pow(z, 2 * n, PRIME) == PRIME - 1
        aa = [[sum(pow(z, v * j, PRIME) for v in fiber(i, a, b)) % PRIME
               for j in range(4 * n)] for i in range(n)]
        bb = [[pow(z, 4 * i * project(j, a, b), PRIME) for j in range(4 * n)]
              for i in range(n)]
        diff = [[(x - y) % PRIME for x, y in zip(u, v)] for u, v in zip(aa, bb)]
        assert len(pivots(diff)) == n
        out.append({"N": n, "rank_QF4N_minus_FNQ": n, "half_active_bank_defect_rank": n // 2})
    return out


def main():
    start = time.monotonic()
    result = {"status": "PASS", "scope": "New hierarchical geometry, separate from the N16 coefficient family; no Fourier coefficients supplied.",
              "small_chains": small_chains(), "threshold_bases": threshold_bases(),
              "margins": margins(), "fourier_defects": fourier_defect_controls(),
              "provenance": "Fresh checker using previously authored helpers from this same constructor track; no uploaded code executed."}
    result["elapsed_seconds"] = time.monotonic() - start
    (HERE / "HIERARCHICAL_LIFT_CONTROLS.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "elapsed_seconds": result["elapsed_seconds"]}), flush=True)


if __name__ == "__main__":
    main()
