"""Independent exhaustive finite-field basis audit for the 60H transform.

Each Fourier matrix entry is compared with pow(omega,j*k,p), separately for
Phase 28 fused60, Phase 28 nested15, and Phase 27 original GT15.
No floating point tolerances, no FFT oracle required.
"""
import json,time
from pathlib import Path
from crt15 import P,GENERATOR,ALT_P,ALT_GENERATOR,n_root
from crt15_engine import transform as old_transform
from wfta15 import transform_wfta
from fused60 import make_fused60_plan,transform_fused

FIELDS=((P,GENERATOR),(ALT_P,ALT_GENERATOR))

def audit(lengths=(60,120,240,480,960)):
    rows=[];total_entries=0;total_comparisons=0
    for p,gen in FIELDS:
        for n in lengths:
            if (p-1)%n:continue
            plan=make_fused60_plan(n,p=p,gen=gen)
            root=n_root(n,p,gen)
            roots=[pow(root,i,p) for i in range(n)]
            passes=0
            start=time.perf_counter()
            for j in range(n):
                x=[0]*n;x[j]=1
                v,_=transform_fused(x,plan)
                w,_=transform_wfta(x,plan.wfta)
                z,_=old_transform(x,plan.wfta.base)
                for k in range(n):
                    expected=roots[(j*k)%n]
                    assert v[k]==expected,('fused60',p,n,j,k)
                    assert w[k]==expected,('wfta15',p,n,j,k)
                    assert z[k]==expected,('oldGT15',p,n,j,k)
                    passes+=1
            row={'prime':p,'length':n,'basis_vectors':n,'unique_DFT_matrix_entries':passes,
                 'independent_entry_comparisons':3*passes,
                 'three_exact_circuits_agreed':True,'elapsed_seconds':round(time.perf_counter()-start,4)}
            rows.append(row)
            total_entries+=passes;total_comparisons+=3*passes
            print(f'p={p} N={n:>4} basis={n} entries={passes} checks={3*passes} seconds={row["elapsed_seconds"]}',flush=True)
    summary={'unique_fourier_entries':total_entries,'independent_entry_comparisons':total_comparisons,
             'basis_vectors':sum(r['basis_vectors'] for r in rows),'rows':rows}
    with open(str(Path(__file__).resolve().parent / 'AUDIT_PHASE28.json'),'w') as f:json.dump(summary,f,indent=2)
    return summary

if __name__=='__main__':
    v=audit()
    print('TOTAL',v['unique_fourier_entries'],'COMPARISONS',v['independent_entry_comparisons'])
