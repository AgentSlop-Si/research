"""Whole-basis exact audits for both cyclic graph factor and Green FFT engine.

Checks individual matrix entries over prime fields, not numerical sampling.
"""
from __future__ import annotations
import json, time
from annihilator_engine import RecurrenceGreen, decode_graph_polynomial,far_coprime_shift
from rational_forcing import bluestein_transform

CASES=[(2013265921,31,[3,5,15,30,60,128,256,384]),
       (998244353,3,[7,17,119,128,256])]


def main():
    records=[]; fixed=0;green=0; singular=0
    t0=time.perf_counter()
    for p,g,ns in CASES:
        for n in ns:
            e=RecurrenceGreen(n,p,g)
            delta=far_coprime_shift(n)
            q=[1,-2]
            entry_checks=0;basis_checks=0
            for j in range(n):
                r=[0]*n;r[j]=1
                got,meta=decode_graph_polynomial(r,delta,q,e)
                expected=[pow(e.omega,(j*k)%n,p) for k in range(n)]
                if got!=expected:raise AssertionError(('graph basis mismatch',p,n,j))
                entry_checks+=n
                if n<=128:
                    x=[0]*n;x[j]=1
                    got2,meta2=e.transform_recurrence(x)
                    if got2!=expected:raise AssertionError(('Green basis mismatch',p,n,j))
                    basis_checks+=n
            fixed+=entry_checks;green+=basis_checks
            records.append({'prime':p,'N':n,'delta':delta,'graph_entries':entry_checks,
                            'full_green_entries':basis_checks})
            print('AUDIT',p,n, 'graph',entry_checks,'green',basis_checks,flush=True)
    result={'fixed_graph_matrix_entries':fixed,'full_green_matrix_entries':green,
            'total_entries':fixed+green,'cases':records,'elapsed_seconds':round(time.perf_counter()-t0,3)}
    with open('BASIS_AUDIT.json','w') as f:json.dump(result,f,indent=2)
    print('TOTAL',fixed+green)
    return result
if __name__=='__main__':main()
