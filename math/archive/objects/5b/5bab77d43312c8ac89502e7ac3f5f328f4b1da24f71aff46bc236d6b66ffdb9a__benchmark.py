#!/usr/bin/env python3
from __future__ import annotations

import csv
import time
from pathlib import Path

import numpy as np

import prototype as p
import unit_step_core as core
import v11_fused_reference as v11


def median_time(fn, repeats: int = 3) -> float:
    values = []
    for _ in range(repeats):
        start = time.perf_counter()
        fn()
        values.append(time.perf_counter() - start)
    return float(np.median(values))


def run(output: Path = Path("benchmark_results.csv")) -> None:
    rng = np.random.default_rng(20261009)
    rows = []
    for n in [768, 1280, 3072, 5120, 12288]:
        x = rng.normal(size=n) + 1j * rng.normal(size=n)
        q = p.next_prime_power(n, 2)
        block = p.choose_prime_power_block(q, 2)
        rank = p.bessel_rank_for_tail(n ** (-1.0 / 3.0))
        state = core.draw_state(q, rng)

        # Warm-up imports/plans/FFT caches.
        p.offset_class_row(x, 2, state, block)
        p.offset_class_row_batched(x, 2, state, block)
        v11.fused_addition_bessel_chirp_row(x, rank, block, state, 0)
        np.fft.fft(x)

        t_class = median_time(lambda: p.offset_class_row(x, 2, state, block))
        t_batch = median_time(lambda: p.offset_class_row_batched(x, 2, state, block))
        t_bessel = median_time(
            lambda: v11.fused_addition_bessel_chirp_row(x, rank, block, state, 0)
        )
        t_fft = median_time(lambda: np.fft.fft(x) / np.sqrt(n))
        rows.append({
            "N": n,
            "Q": q,
            "M": block,
            "classes": p.offset_class_count(n, q),
            "bessel_rank": rank,
            "offset_stream_seconds": t_class,
            "offset_batch_seconds": t_batch,
            "bessel_seconds": t_bessel,
            "numpy_fft_seconds": t_fft,
            "offset_stream_over_bessel": t_class / t_bessel,
            "offset_batch_over_bessel": t_batch / t_bessel,
            "offset_stream_over_numpy_fft": t_class / t_fft,
            "offset_batch_over_numpy_fft": t_batch / t_fft,
            "offset_work_proxy": p.offset_class_work_proxy(n, 2, block),
            "bessel_work_proxy": p.bessel_lift_work_proxy(n, rank),
        })

    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    run()
