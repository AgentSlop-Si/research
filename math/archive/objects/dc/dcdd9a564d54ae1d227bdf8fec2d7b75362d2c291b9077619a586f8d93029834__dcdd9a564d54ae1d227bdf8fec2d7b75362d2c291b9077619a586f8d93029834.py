#!/usr/bin/env python3
import json,random,time
from math import floor,log2
from phase9_dense_cycle import P,Costs,exact_reference_dft
from phase9_spectral_innovations import make_spectral_cycle,exact_spectral_innovation_cycle

def main():
    rows=[]
    for exponent in (8,9,10,11,12,13,14,15,16):
        n=1<<exponent
        m=1<<int(floor(log2(exponent)))
        k=n//m
        for s in (0,1,3):
            rng=random.Random(735+n+s)
            events={t:[(ell,rng.randrange(1,P)) for ell in rng.sample(range(k),s)]
                    for t in range(1,m-1)} if s else {}
            x,meta=make_spectral_cycle(k,m,events,seed=73+s)
            start=time.perf_counter()
            y,cert,c=exact_spectral_innovation_cycle(x,m,s,3,Costs(),random.Random(1984),True)
            elapsed=time.perf_counter()-start
            assert y is not None and y==exact_reference_dft(x)
            rows.append({'n':n,'k':k,'m':m,'spectral_modes_per_step':s,
                'innovation_modes_total':cert['total_innovation_modes'],
                'field_operations':c.total(),'operations_per_input':round(c.total()/n,3),
                'inversions':c.inversions,'ntt_butterflies':c.ntt_butterflies,
                'seconds_python':round(elapsed,4)})
            print('N=',n,'M=',m,'spectral modes=',s,'ops/N=',rows[-1]['operations_per_input'])
    open('SPECTRAL_AUDIT_RESULTS.json','w').write(json.dumps({'rows':rows,'note':
         'Measured modular field-operation counts, not CPU superiority or general-input FFT speedup.'},indent=2))
    print('ALL DUAL SPECTRAL SCALING TESTS EXACT')
if __name__=='__main__':main()
