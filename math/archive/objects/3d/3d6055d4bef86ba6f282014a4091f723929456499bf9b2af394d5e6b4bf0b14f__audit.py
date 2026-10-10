"""Reproducible exact arithmetic and Boolean quotient checks."""
from __future__ import annotations
import json, random
from pathlib import Path
from circuit import build_adaptive, differentiate, reference_dft
from boolean_cube import power_of_sum, coefficient_by_onto_functions


def run_audit():
    rng=random.Random(20261009)
    out=[]
    total_columns=0
    total_outputs=0
    max_ratio=0
    for n in (2,4,8,16,32,64):
        for mode in ('polynomial','rational','sign_branch'):
            base=[rng.randrange(1,900) for _ in range(n)]
            if mode=='sign_branch' and n%4==0: base[0]=998244352
            circuit,label=build_adaptive(n,base,mode=mode)
            lin=differentiate(circuit,base)
            if lin.cost>3*circuit.cost:raise AssertionError('gate bound')
            for j in range(n):
                v=[0]*n;v[j]=1
                expect=reference_dft(v)
                actual=lin.evaluate(v)
                if actual != expect:raise AssertionError(('linear',n,mode,j))
                total_columns+=1
                total_outputs+=n
            for _ in range(3):
                vec=[rng.randrange(998244353) for j in range(n)]
                if mode=='rational' and (1+vec[-1]**2)%998244353==0:
                    vec[-1]=0  # nonsingular path, no division by zero
                if circuit.evaluate(vec)!=reference_dft(vec):
                    raise AssertionError(('original',n,mode))
            ratio=lin.cost / max(1,circuit.cost)
            max_ratio=max(ratio,max_ratio)
            out.append(dict(n=n,branch=mode,selector=label,original_cost=circuit.cost,
                            extracted_linear_cost=lin.cost,ratio=round(ratio,3)))
    boolean=[]
    for n in (3,4,6,8,10,12):
        poly=power_of_sum(n,n)
        if len(poly)!=2**n-1:raise AssertionError('not dense')
        for mask,c in poly.items():
            if c!=coefficient_by_onto_functions(n,mask.bit_count()):
                raise AssertionError(('stirling',n,mask,c))
        boolean.append(dict(n=n,original_multiplications=(n.bit_length()-1)+(n.bit_count()-1),
                            multilinear_monomials=len(poly)))
    result={'prime':998244353,'cases':len(out),'basis_columns':total_columns,
            'matrix_entries':total_outputs,'largest_extracted_to_original_ratio':round(max_ratio,3),
            'circuit_runs':out,'boolean_expansion':boolean}
    return result


if __name__=='__main__':
    d=run_audit()
    dest=Path(__file__).with_name('audit_results.json')
    dest.write_text(json.dumps(d,indent=2))
    for row in d['circuit_runs']:
        if row['n'] in (8,32,64):
            print(f"n={row['n']:2} {row['branch']:13} original={row['original_cost']:5} extracted={row['extracted_linear_cost']:5}")
    print('exact basis vectors:',d['basis_columns'],'matrix entries:',d['matrix_entries'])
    print('Boolean quotient:')
    for b in d['boolean_expansion']:print(b)
