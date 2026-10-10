#!/usr/bin/env python3
import csv, json, math, pathlib, time
import numpy as np
from polyphase_exact import joint_green_frame_exact, mixed_radix_collapsed, naive_complete_frame


def medtime(fn,reps=5):
    vals=[]
    for _ in range(reps):
        t=time.perf_counter();fn();vals.append(time.perf_counter()-t)
    return float(np.median(vals))


def run():
    rng=np.random.default_rng(20261010)
    rows=[]
    for q,m in [(55,5),(187,11),(517,11),(1067,11),(2057,11)]:
        x=rng.normal(size=q)+1j*rng.normal(size=q)
        ref=np.fft.fft(x)/math.sqrt(q)
        j=joint_green_frame_exact(x,m)
        c=mixed_radix_collapsed(x,m)
        row={
          'q':q,'m':m,'k':q//m,
          'joint_max_error':float(np.max(np.abs(j-ref))),
          'collapsed_max_error':float(np.max(np.abs(c-ref))),
          'joint_seconds':medtime(lambda:joint_green_frame_exact(x,m),3),
          'collapsed_seconds':medtime(lambda:mixed_radix_collapsed(x,m),5),
          'numpy_fft_seconds':medtime(lambda:np.fft.fft(x)/math.sqrt(q),10),
        }
        if q<=187:
            n=naive_complete_frame(x,m)
            row['naive_frame_max_error']=float(np.max(np.abs(n-ref)))
            row['naive_frame_seconds']=medtime(lambda:naive_complete_frame(x,m),2)
        rows.append(row)
    return rows

if __name__=='__main__':
    root=pathlib.Path(__file__).parent
    rows=run()
    (root/'benchmark_results.json').write_text(json.dumps(rows,indent=2))
    keys=sorted({k for r in rows for k in r})
    with (root/'benchmark_results.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(rows)
    print(json.dumps(rows,indent=2))
