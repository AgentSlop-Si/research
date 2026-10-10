"""Full charged-operation comparisons (not wall-clock FFT speed claims).

The quadratic gauge is evaluated for arbitrary field inputs. For binary input,
it vanishes identically; no speedup for computing a Fourier spectrum is claimed.
"""
from __future__ import annotations
import json
from pathlib import Path
from random import Random
from degree_boundary import P,Counter,wedge_gauge,wedge_coefficients,ntt,cubic_global_wedge_fft


def expanded_wedge(x,a,b,meter:Counter):
    n=len(x)
    squares=[meter.m(t,t) for t in x]
    result=0
    for i in range(n):
        for j in range(i+1,n):
            coeff=meter.s(meter.m(a[i],b[j]),meter.m(a[j],b[i]))
            poly=meter.s(meter.m(squares[i],x[j]),meter.m(x[i],squares[j]))
            result=meter.a(result,meter.m(coeff,poly))
    return result


def run():
    rng=Random(20261009)
    records=[]
    for n in (8,16,32,64,128,256,512,1024):
        a=[rng.randrange(P) for _ in range(n)]
        b=[rng.randrange(P) for _ in range(n)]
        x=[rng.randrange(P) for _ in range(n)]
        c=Counter()
        value=wedge_gauge(x,a,b,c)
        predicted=n+8*(n*(n-1)//2)
        if n<=128:
            baseline=Counter()
            value2=expanded_wedge(x,a,b,baseline)
            assert value2==value
            assert baseline.work==predicted,(n,baseline.work,predicted)
        cn=Counter();ntt(x,cn)
        cw=Counter();cubic_global_wedge_fft(x,a,b,[2]*n,cw)
        records.append({'N':n,'pair_coefficients':n*(n-1)//2,
                        'global_wedge_scalar_ops':c.work,
                        'fully_expanded_wedge_scalar_ops':predicted,
                        'wedge_ops_ratio':round(predicted/c.work,4),
                        'full_fft_reference_scalar_ops':cn.work,
                        'cubic_gauge_full_fft_scalar_ops':cw.work,
                        'cubic_vs_fft_ratio':round(cw.work/cn.work,4),
                        'FFT_speedup':False,
                        'note':'integer op count of specific prototype, not best transform circuit'})
    return records

if __name__=='__main__':
    data=run()
    out=Path(__file__).with_name('operation_counts.json')
    out.write_text(json.dumps(data,indent=2)+'\n')
    print('N   pair_terms   wedge_ops   expanded_ops  ratio    FFT_ops    cubic+gauge_ops')
    for d in data:
        print(f"{d['N']:4d} {d['pair_coefficients']:12d} {d['global_wedge_scalar_ops']:11d} {d['fully_expanded_wedge_scalar_ops']:14d} {d['wedge_ops_ratio']:6.1f} {d['full_fft_reference_scalar_ops']:10d} {d['cubic_gauge_full_fft_scalar_ops']:16d}")
