import json,random
from pathlib import Path
from cyclotomic_orbits import OrbitDFT,reference_dft_mod


def audit():
    r=random.Random(20261009)
    summary=[]; vectors=0; total_coeff_values=0
    for n in (2,4,8,16,32,64,128):
        x=[r.randrange(2) for _ in range(n)]
        data=OrbitDFT.build(x)
        truth=reference_dft_mod(x)
        values=[data.evaluate_mod(k) for k in range(n)]
        assert values==truth
        for level,rep in enumerate(data.primitive_coefficients):
            m=n>>level; d=m//2
            w=pow(3,(998244353-1)//m,998244353)
            modulated=[v*pow(w,j,998244353)%998244353 for j,v in enumerate(rep)]
            assert reference_dft_mod(modulated)==[values[(1<<level)*(2*t+1)] for t in range(d)]
        vectors+=1;total_coeff_values+=n
        summary.append({'n':n,'construction_add_sub':data.add_sub_count,
                        'shared_basis_coefficients':data.stored_coefficients,
                        'expanded_cyclotomic_coefficients':data.expanded_coefficients,
                        'sharing_ratio':round(data.expanded_coefficients/data.stored_coefficients,3),
                        'all_outputs_verified_mod_p':True})
    return {'trials':vectors,'coefficients_checked':total_coeff_values,'results':summary}

if __name__=='__main__':
    d=audit()
    Path(__file__).with_name('orbit_results.json').write_text(json.dumps(d,indent=2))
    for row in d['results']:print(row)
