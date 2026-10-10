"""Bounded matched-q benchmark. No downloads, installs, or shipped binaries.

Run with OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python benchmark.py.
All timed engines receive identical already-generated updates, projection and
prepared phase values. Common preparation is timed and charged to each total.
The original class is unchanged; compact() runs after EVERY timed query.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
import platform
import statistics
import time
import numpy as np

from coalesced_projected import CoalescedProjectedFourier, AlwaysRebuild, EagerProjected, modular_phase
from vendor.projected_fourier import ProjectedFourierState

METHODS = {
    "original_replay_compact": ProjectedFourierState,
    "always_rebuild": AlwaysRebuild,
    "eager_projected": EagerProjected,
    "coalesced_snapshot": CoalescedProjectedFourier,
}


def fixture(name, q, r, k, batches, edits, mode, seed):
    rng = np.random.default_rng(seed)
    n = 4096 if mode == "delete" else 2048
    basis = rng.normal(size=(r, n)) + 1j*rng.normal(size=(r, n))
    bins = rng.choice(n, q, replace=False)
    coefficients = (rng.normal(size=r) + 1j*rng.normal(size=r)) * 0.1
    sparse = [(j, complex(0.5, -0.25)) for j in range(k)]
    events = []
    for batch in range(batches):
        updates = []
        for i in range(edits):
            if mode == "repeat":
                kind, key = ("c", 0) if i % 2 == 0 else ("p", 0)
                delta = complex(1/128, -1/256)
            elif mode == "cancel":
                kind, key = "p", (i//2) % max(1, k)
                delta = complex(1/128, -1/256) * (1 if i % 2 == 0 else -1)
            elif mode == "delete":
                kind, key, delta = "p", i, -sparse[i][1]
            elif mode == "distinct":
                kind, key = "p", i
                delta = complex(1/128, -1/256)
            else:
                kind, key = (("c", batch % r) if r and batch % 2 == 0 else ("p", batch % max(1, k)))
                delta = complex(1/128, -1/256)
            updates.append((kind, key, delta))
        events.append(updates)
    positions = sorted({j for j, _ in sparse} | {key for updates in events for kind, key, _ in updates if kind == "p"})
    return dict(name=name, n=n, q=q, r=r, k=k, basis=basis, bins=bins,
                coefficients=coefficients, sparse=sparse, batches=events, positions=positions, mode=mode)


def prepare(f):
    # The shared producer-projection setup uses a full NumPy FFT of the basis.
    # Its cost is included; this experiment makes no faster-registration claim.
    start = time.perf_counter_ns()
    projection = np.fft.fft(f["basis"], axis=1)[:, f["bins"]].copy()
    phase = np.asarray([modular_phase(f["n"], f["bins"], j) for j in f["positions"]], dtype=complex).reshape(len(f["positions"]), f["q"])
    rows = {j: i for i, j in enumerate(f["positions"])}
    return projection, phase, rows, time.perf_counter_ns() - start


def construct(method, f, prepared):
    projection, phase, rows, _ = prepared
    state = METHODS[method](f["n"], f["bins"], projection, f["coefficients"])
    # Configure the existing preparation fields equally for all four engines.
    # The original engine code is not patched or monkey-patched. Each engine
    # owns a copy of the phase table; projection copying remains per its API.
    state._prepared_phase = phase.copy()
    state._prepared_row = rows.copy()
    # Populate the same already-normalized residual in each engine, then use
    # the same prepared phases. This avoids accidentally charging each engine
    # a second, differently implemented phase-generation pass at construction.
    state.sparse = dict(f["sparse"])
    state.cached = state._rebuild_value()
    return state


def execute(method, f, prepared):
    start = time.perf_counter_ns()
    state = construct(method, f, prepared)
    construction = time.perf_counter_ns() - start
    update_ns = query_ns = 0
    answers = []
    # No garbage is parked for untimed disposal: pending.clear and compact
    # both execute within the query timer. Answers are retained equally.
    loop_start = time.perf_counter_ns()
    for updates in f["batches"]:
        t = time.perf_counter_ns()
        for kind, key, delta in updates:
            if kind == "c":
                state.add_coefficient(key, delta)
            else:
                state.add_point(key, delta)
        update_ns += time.perf_counter_ns() - t
        t = time.perf_counter_ns()
        answer = state.query()
        if method == "original_replay_compact":
            state.compact()
        query_ns += time.perf_counter_ns() - t
        answers.append(answer)
    stream_ns = time.perf_counter_ns() - loop_start
    # Sum includes the complete stream loop, constructor and measured common
    # projection/phase preparation, but excludes input RNG and oracle checks.
    total = prepared[3] + construction + stream_ns
    return dict(prepare_ns=prepared[3], construction_ns=construction,
                update_ns=update_ns, query_and_compaction_ns=query_ns,
                stream_ns=stream_ns, end_to_end_ns=total), answers, state


def oracle(f):
    c = f["coefficients"].copy()
    sparse = dict(f["sparse"])
    answers = []
    for updates in f["batches"]:
        for kind, key, delta in updates:
            if kind == "c":
                c[key] += delta
            else:
                value = sparse.get(key, 0j) + delta
                if value == 0j:
                    sparse.pop(key, None)
                else:
                    sparse[key] = value
        dense = c @ f["basis"]
        for key, value in sparse.items():
            dense[key] += value
        answers.append(np.fft.fft(dense)[f["bins"]])
    return answers


def main():
    specs = [
        ("repeat_wide", 128, 16, 64, 40, 200, "repeat"),
        ("repeat_narrow", 1, 4, 4, 100, 50, "repeat"),
        ("one_edit_per_query", 16, 4, 8, 1000, 1, "few"),
        ("distinct_keys", 64, 8, 0, 40, 128, "distinct"),
        ("cancel_pairs", 64, 4, 8, 50, 128, "cancel"),
        ("delete_support", 1, 0, 2048, 1, 2048, "delete"),
        ("query_only", 32, 8, 16, 1000, 0, "none"),
        ("long_compacted_history", 1, 2, 2, 4000, 1, "few"),
    ]
    repetitions = 7
    result = {"schema_version": 1, "python": platform.python_version(),
              "numpy": np.__version__, "platform": platform.platform(),
              "threads": {k: os.environ.get(k) for k in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS")},
              "repetitions": repetitions, "statistic": "median of seven matched trials, randomized method order",
              "setup": "Common full NumPy basis FFT, selected projection and modular phase table are charged to each method; input generation and correctness checks excluded.",
              "workloads": []}
    rng_order = np.random.default_rng(9959)
    for i, spec in enumerate(specs):
        f = fixture(*spec, seed=500+i)
        expected = oracle(f)
        prepared = prepare(f)
        errors = {}
        for method in METHODS:
            _, answers, state = execute(method, f, prepared)
            errors[method] = max(float(np.max(np.abs(a-e))) for a, e in zip(answers, expected))
            for a, e in zip(answers, expected):
                np.testing.assert_allclose(a, e, rtol=3e-10, atol=3e-9)
        trials = {method: [] for method in METHODS}
        for trial in range(repetitions):
            prepared = prepare(f)
            for method in rng_order.permutation(list(METHODS)):
                timing, _, _ = execute(method, f, prepared)
                trials[method].append(timing)
        medians = {method: {key: statistics.median(t[key] for t in rows) for key in rows[0]} for method, rows in trials.items()}
        coalesced = medians["coalesced_snapshot"]["end_to_end_ns"]
        speedups = {method: medians[method]["end_to_end_ns"] / coalesced for method in METHODS if method != "coalesced_snapshot"}
        row = dict(name=f["name"], n=f["n"], q=f["q"], r=f["r"], initial_k=f["k"],
                   queries=len(f["batches"]), edits=sum(map(len, f["batches"])),
                   prepared_positions=len(f["positions"]), medians=medians,
                   comparator_over_coalesced=speedups, max_abs_error=errors, raw_trials=trials)
        result["workloads"].append(row)
        print(f["name"], {m: round(v["end_to_end_ns"]/1e6, 4) for m, v in medians.items()}, "ratios", {m: round(v, 3) for m, v in speedups.items()}, flush=True)
    output = Path("results/benchmark_results.json")
    output.write_text(json.dumps(result, indent=2)+"\n")
    print(output)


if __name__ == "__main__":
    main()
