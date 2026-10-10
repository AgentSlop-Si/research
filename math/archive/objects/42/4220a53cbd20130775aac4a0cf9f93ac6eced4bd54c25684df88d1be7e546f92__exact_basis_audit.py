"""Independent exact full-basis and adversarial Fourier comparisons.

Each phase19 hidden-delay input family x=P^{-1}(I-alpha*S^delta)^{-1}e_j
is an invertible image of the N standard basis vectors. The oracle is an
independently computed O(N^2) direct DFT; no shared forcing/Green implementation.
"""
import json
from math import gcd
from blind_discovery import RecurrenceGreen
from annihilator_engine import dense_from_shift_defects,far_coprime_shift
from rational_forcing import direct_dft_any

CASES=[(998244353,3,7),(998244353,3,17),
       (2013265921,31,30),(2013265921,31,60),
       (2013265921,31,128),(2013265921,31,384)]

def hidden(n):
    d=n//3+1
    while gcd(d,n)!=1 or d in (1,n-1,far_coprime_shift(n)):d+=1
    return d

def main():
    rows=[];total=0
    for p,g,n in CASES:
        e=RecurrenceGreen(n,p,g)
        d=hidden(n)
        for j in range(n):
            h=[0]*n;h[j]=j+3
            r=dense_from_shift_defects(h,d,2,p)
            x=e.P.solve(r)
            y,meta=e.transform_blind_one(x)
            if meta['selected']!='blind-one-defect':
                raise AssertionError(('incorrectly rejected genuine one-defect',n,d,j))
            expected=direct_dft_any(x,e.omega,p)
            if y!=expected:raise AssertionError(('mismatch',n,d,j))
        total+=n*n
        rows.append({'p':p,'N':n,'unknown_delay':d,'basis_vectors_checked':n,
                     'exact_fourier_entries_checked':n*n})
        print('FULL BASIS',p,n,'hidden shift',d,'entries',n*n,flush=True)
    result={'rows':rows,'total_matrix_entries':total,
        'oracle':'Independent direct nested-sum DFT for every input column from the invertible hidden-shift structured basis.'}
    with open('EXACT_BASIS_AUDIT.json','w') as f:json.dump(result,f,indent=2)
    return result
if __name__=='__main__':main()
