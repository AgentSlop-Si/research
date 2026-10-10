#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
import statistics
import time
from pathlib import Path

import numpy as np

import prototype as p
import composite_cycle_core as core


def median_time(fn, repeats: int=5) -> float:
    values=[]
    for _ in range(repeats):
        t0=time.perf_counter(); fn(); values.append(time.perf_counter()-t0)
    return statistics.median(values)


def run(output: Path=Path('benchmark_results.csv')) -> None:
    rng=np.random.default_rng(20261010)
    rows=[]
    cases=[(10403,101),(47053,211),(899,29),(20736,16),(49152,12)]
    for n,m in cases:
        x=rng.normal(size=n)+1j*rng.normal(size=n)
        state=core.draw_state(n,rng)
        # Warm-up
        p.direct_composite_row(x,m,state)
        p.normalized_dft(x)
        t_row=median_time(lambda:p.direct_composite_row(x,m,state),3)
        t_fft=median_time(lambda:p.normalized_dft(x),7)
        ref=core.direct_row_estimate(x,m,state)
        got=p.direct_composite_row(x,m,state)
        rows.append({
            'N':n,'M':m,'K':n//m,
            'direct_row_seconds':t_row,
            'numpy_fft_seconds':t_fft,
            'row_over_numpy_fft':t_row/t_fft,
            'executor_vs_materialized_error':float(np.max(np.abs(got-ref))),
            'variance_factor':float(p.direct_divisor_variance_factor(n,m)),
            'coarse_variance_factor':float(p.coarse_composite_variance_factor(n,m)),
        })
    with output.open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader();writer.writerows(rows)
    for row in rows:
        print(row)

if __name__=='__main__':
    run()
