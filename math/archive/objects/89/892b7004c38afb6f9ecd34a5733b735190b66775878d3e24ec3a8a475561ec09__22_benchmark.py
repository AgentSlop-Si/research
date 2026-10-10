#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
import time
from pathlib import Path
import numpy as np

import arbitrary_block_core as core


def timed(fn, repeat=3):
    vals=[]; result=None
    for _ in range(repeat):
        t=time.perf_counter(); result=fn(); vals.append(time.perf_counter()-t)
    return min(vals), result


def safe_error(a,b):
    diff=np.asarray(a)-np.asarray(b)
    if not np.all(np.isfinite(diff)):
        return float('inf')
    return float(np.max(np.abs(diff)))


def main():
    rng=np.random.default_rng(20261010)
    rows=[]
    for n in [1009, 2039, 4093, 8191, 16381]:
        x=rng.normal(size=n)+1j*rng.normal(size=n)
        base=max(3,round(math.log2(n)))
        for blocks in sorted(set([base, min(n-1,2*base), min(n-1,round(math.log2(n)**2))])):
            state=core.draw_state(n,rng)
            with np.errstate(over='ignore',invalid='ignore'):
                t_rec, got=timed(lambda:core.one_row_estimate(x,blocks,state,'recurrence'),2)
            t_dir, direct=timed(lambda:core.one_row_estimate(x,blocks,state,'direct'),2)
            t_fft, _=timed(lambda:np.fft.fft(x)/math.sqrt(n),4)
            ref=core.reference_row(x,blocks,state)
            rec_err=safe_error(got,ref)
            rows.append({
                'n':n,'blocks':blocks,
                'recurrence_seconds':t_rec,
                'direct_forcing_seconds':t_dir,
                'numpy_fft_seconds':t_fft,
                'recurrence_over_numpy_fft':t_rec/t_fft,
                'direct_over_recurrence':t_dir/t_rec,
                'recurrence_stable_binary64':int(math.isfinite(rec_err) and rec_err<1e-5),
                'decoder_error':rec_err,
                'recurrence_vs_direct_error':safe_error(got,direct),
            })
    path=Path('benchmark_results.csv')
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    for row in rows:print(row)

if __name__=='__main__':main()
