"""Illustrative twiddle-root drift tests, not a certified hardware FP theorem."""
import json,math
from pathlib import Path
import numpy as np
import mixedradix as mod

def generate(g,m,delta):
    n=g*m
    omega=np.exp(-2j*math.pi/n)+delta
    a=1.+0j
    table=np.ones((g,m),dtype=np.complex128)
    for k in range(g):
        b=1.+0j
        for s in range(1,m):
            b*=a
            table[k,s]=b
        a*=omega
    return table

def main():
    tests=[]
    for g,m in [(8,5),(64,3),(128,3),(512,3),(64,17)]:
        n=g*m
        target=np.exp(-2j*np.pi*np.arange(g)[:,None]*np.arange(m)[None,:]/n)
        for delta in [0.,1e-10]:
            approx=generate(g,m,delta)
            actual=float(np.max(np.abs(approx-target)))
            # conservative 2N+1 exponent, root initial error plus 4eps roundoff.
            eps=float(abs(np.exp(-2j*math.pi/n)-complex(math.cos(-2*math.pi/n),math.sin(-2*math.pi/n))))
            h=float(abs(delta)+eps+5*np.finfo(float).eps)
            predicted=math.expm1((2*n+1)*math.log1p(h))
            assert actual<=predicted+1e-12, (n,delta,actual,predicted)
            tests.append({'N':n,'G':g,'odd_part':m,'injected_root_delta':delta,
                          'max_observed_table_error':actual,'conservative_stated_bound':predicted})
    out={'scope':'single-root twiddle drift diagnostic; uses conservative assumed multiply error',
         'tests':tests}
    (Path(__file__).parent/'PRECISION_DIAGNOSTIC.json').write_text(json.dumps(out,indent=2)+'\n')
    print('twiddle precision diagnostic checks passed:',len(tests))

if __name__=='__main__':main()
