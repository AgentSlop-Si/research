"""Phase17 independent exhaustive basis-vector audit.

Comparison target is direct Vandermonde evaluation (no NTT, Green, fractions).
Two bases are tested: e_j (usual input basis) and P^-1 e_j
(dense structured Green-response basis). Results count full output entries.
"""
from rational_forcing import AllLengthGreen,direct_dft_any,P0,G0
import json,random
from pathlib import Path

SIZES=[(7,998244353,3),(17,998244353,3),(30,P0,G0),
       (60,P0,G0),(119,998244353,3),(128,P0,G0),(256,P0,G0)]


def run():
    rows=[];count=0;impulses=0; max_ntt_len=0
    for n,p,g in SIZES:
        eng=AllLengthGreen(n,p,g)
        checks=0
        for j in range(n):
            standard=[0]*n;standard[j]=1
            yi,_=eng.transform(standard,method='rational')
            assert yi==direct_dft_any(standard,eng.omega,p),(n,j,'ordinary')
            checks+=n
            dense=eng.structured_dense({j:1})
            assert all(dense),(n,j,'not dense')
            yd,meta=eng.transform(dense,method='rational')
            assert meta['K']==1,(n,j,'not sparse residual')
            assert meta['stats'].max_ntt_length==0
            assert yd==direct_dft_any(dense,eng.omega,p),(n,j,'green impulse')
            checks+=n;impulses+=1
        rows.append({'N':n,'prime':p,'primitive_generator':g,
                     'input_basis_vectors':n,'dense_green_impulses':n,
                     'checked_Fourier_output_entries':checks})
        count+=checks
        print('basis',n,checks,flush=True)

    # Exact noncommuting intertwining for every column and every row over 2 fields.
    intertwines=0
    for n,p,g in [(17,998244353,3),(60,P0,G0),(128,P0,G0)]:
        eng=AllLengthGreen(n,p,g)
        for j in range(n):
            col=[pow(eng.omega,k*j,p) for k in range(n)]
            left=eng.L.apply(col)
            basis=[0]*n;basis[j]=1
            right=direct_dft_any(eng.P.apply(basis),eng.omega,p)
            assert left==right,(n,j,'intertwining')
            intertwines+=n
    result={'project':'FFT Hero1 Phase17',
            'finite_field_basis_checks':count,'intertwining_matrix_entries':intertwines,
            'total_field_entries_checked':count+intertwines,
            'dense_impulses_verified':impulses,
            'rows':rows,'passed':True,
            'scope':'Exact finite-field tests for selected N, not all-size numerical proof'}
    path=Path(__file__).with_name('FIELD_BASIS_RESULTS.json')
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    return result

if __name__=='__main__':run()
