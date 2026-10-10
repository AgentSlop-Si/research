"""Independent all-column tests for the fully blind *two unknown factors* branch."""
import json
from blind_inverse import RecurrenceGreen
from annihilator_engine import dense_from_shift_defects,far_coprime_shift
from rational_forcing import direct_dft_any

CASES=[(998244353,3,17),(2013265921,31,30),
       (2013265921,31,60),(2013265921,31,128),
       (2013265921,31,384)]

def main():
    entries=0;cases=[]
    for p,g,n in CASES:
        eng=RecurrenceGreen(n,p,g)
        d1,d2=far_coprime_shift(n),n-1
        for j in range(n):
            h=[0]*n;h[j]=(3+j)%p or 1
            r=dense_from_shift_defects(dense_from_shift_defects(h,d1,2,p),d2,3,p)
            x=eng.P.solve(r)
            y,m=eng.transform_blind_inverse(x,4)
            if m['selected']!='blind-sparse-circular-inverse' or m['inverse_support']!=4:
                raise AssertionError(('missing blind two-filter certificate',n,j,m))
            reference=direct_dft_any(x,eng.omega,p)
            if y!=reference:raise AssertionError(('DFT discrepancy',p,n,j))
        entries+=n*n
        cases.append({'N':n,'p':p,'unknown_factor_count':2,
                      'input_columns_checked':n,'matrix_entries':n*n})
        print('TWO-UNKNOWN-FACTOR BASIS',n,n*n,flush=True)
    result={'cases':cases,'total_matrix_entries':entries,
            'oracle':'Independent direct-sum DFT for each dense signal generated from a single-impulse defect at every support position. Adaptive algorithm is independently certified per input; basis checks alone are not treated as a linear-circuit proof.'}
    with open('EXACT_INVERSE_BASIS_AUDIT.json','w') as f:json.dump(result,f,indent=2)
    return result
if __name__=='__main__':main()
