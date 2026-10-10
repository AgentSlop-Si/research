"""Cold end-to-end numerical comparisons, with all preparation and outputs.

This does not claim a universal wall-clock win or certified floating accuracy.
"""
import json
import math
import time
from pathlib import Path
import numpy as np
from energy_pruned import energy_pruned_fft


def main():
    rng=np.random.default_rng(20261009)
    records=[]
    for n in (4096,16384,65536,262144):
        j=np.arange(n)
        families=dict(gaussian=rng.normal(size=n)+1j*rng.normal(size=n),
                      tone=np.exp(2j*np.pi*17*j/n))
        spectrum=np.zeros(n,dtype=complex)
        choices=rng.choice(n,size=15,replace=False)
        spectrum[choices]=np.exp(1j*rng.uniform(-np.pi,np.pi,len(choices)))
        families['fifteen_tones']=np.fft.ifft(spectrum,norm='ortho')
        for name,x in families.items():
            full_times=[]
            for _ in range(3):
                started=time.perf_counter()
                reference=np.fft.fft(x,norm='ortho')
                full_times.append(time.perf_counter()-started)
            for epsilon in (.125,.25,.5):
                times=[]
                for _ in range(3):
                    started=time.perf_counter()
                    out,stats=energy_pruned_fft(x,epsilon)
                    times.append(time.perf_counter()-started)
                ratio=float(np.max(np.abs(out-reference))/np.linalg.norm(x))
                assert ratio<=epsilon+1e-11
                full=float(np.median(full_times))
                approx=float(np.median(times))
                records.append(dict(n=n,family=name,epsilon=epsilon,
                    exact_fft_seconds=full,pruned_seconds=approx,
                    wall_ratio=approx/full,error_ratio=ratio,
                    split_value_volume=stats.get('split_value_volume',0),
                    full_fft_split_volume=n*(n.bit_length()-1),
                    butterfly_ratio=stats.get('butterflies',0)/(n*(n.bit_length()-1)/2),
                    norm_value_volume=stats.get('norm_value_volume',0),
                    root_exp_evaluations=stats.get('root_exponential_evaluations',0),
                    computed_outputs=stats.get('computed_output_count',0),
                    pruned_outputs=stats.get('pruned_output_count',0),
                    output_count=stats['returned_output_count']))
    result=dict(method='NumPy complex128; median 3 cold calls; given inputs',
        baseline='numpy.fft.fft(x,norm=ortho)',
        timed='validation, scaling, all coefficient setup, norm scans, splits and all output writes',
        results=records)
    out=Path(__file__).parent/'results';out.mkdir(exist_ok=True)
    (out/'benchmark.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(cases=len(records),min_wall_ratio=min(r['wall_ratio'] for r in records),
        max_wall_ratio=max(r['wall_ratio'] for r in records),
        wins=sum(r['wall_ratio']<1 for r in records)),indent=2))
    print(json.dumps([r for r in records if r['n']==262144],indent=2))


if __name__=='__main__':main()
