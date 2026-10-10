"""Independent matrix-entry verification of every tangent FFT circuit.

Deliberately does NOT call direct_dft, eval_dual or the reference FFT builder.
It validates the complete matrix represented by the extracted linear DAG.
"""
from jet_linearize import P,ROOT,build_nonlinear_fft,build_fft,linearize
import json
from pathlib import Path


def check():
    results=[]
    num_columns=0
    num_entries=0
    for n in (2,4,8,16,32,64):
        omega=pow(ROOT,(P-1)//n,P)
        for mode in ('standard','square','rational','baseline'):
            if mode=='standard':
                dag,_,out,_=build_fft(n)
            else:
                dag,_,out=build_nonlinear_fft(n,mode)
            L, idx=linearize(dag,out,[0]*n)
            for j in range(n):
                basis=[0]*n
                basis[j]=1
                got=L.evaluate(basis,idx)
                want=[pow(omega,j*k,P) for k in range(n)]
                if got!=want:
                    raise AssertionError(f'mode={mode} n={n} col={j} got={got} want={want}')
                num_columns+=1
                num_entries+=n
            results.append({'n':n,'mode':mode,'independently_verified_matrix_columns':n,
                            'matrix_entries':n*n,'linear_gates':L.cost()})
    status={'p':P,'modes':4,'size_count':6,'full_matrix_columns_verified':num_columns,
            'full_matrix_entries_verified':num_entries,'results':results}
    Path(__file__).with_name('matrix_certificate.json').write_text(json.dumps(status,indent=2)+'\n')
    print('Independent full matrix certificate PASSED')
    print(f'{num_columns} full matrix columns, {num_entries} matrix entries, 24 extracted circuits')
    return status

if __name__=='__main__':check()
