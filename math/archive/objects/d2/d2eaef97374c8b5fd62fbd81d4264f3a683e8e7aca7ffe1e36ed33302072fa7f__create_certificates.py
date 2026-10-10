"""Extract compact nonzero Macaulay minors over split fields.
A nonzero modular determinant certifies a nonzero characteristic-zero minor
when the Gaussian denominators and outer inverses reduce to units.
"""
import json
from pathlib import Path
from phase39_bivariate import build,macaulay,rank_mod,PRIMES


def determinant(matrix,p):
    m=[row[:] for row in matrix]
    n=len(m)
    if n!=len(m[0]):raise ValueError('Not square')
    result=1
    for col in range(n):
        pivot=next((r for r in range(col,n) if m[r][col]),None)
        if pivot is None:return 0
        if pivot!=col:
            m[pivot],m[col]=m[col],m[pivot]
            result=-result
        u=m[col][col]
        result=result*u%p
        inv=pow(u,p-2,p)
        for r in range(col+1,n):
            factor=m[r][col]*inv%p
            for c in range(col+1,n):m[r][c]=(m[r][c]-factor*m[col][c])%p
            m[r][col]=0
    return result%p


def witness(matrix,p):
    subset=[]
    for i,row in enumerate(matrix):
        if rank_mod([matrix[j] for j in subset]+[row],p)>len(subset):
            subset.append(i)
            if len(subset)==len(row):break
    if len(subset)!=len(matrix[0]):raise ValueError('Rank deficient')
    d=determinant([matrix[j] for j in subset],p)
    assert d!=0
    return {'pivot_rows':subset,'determinant_mod_prime':d,'size':len(subset)}


def create(output):
    results=[]
    for n in (4,8,16,32,64):
        for p,g in PRIMES:
            inst=build(n,p,g)
            A=macaulay(inst,kind='cubic')
            B=macaulay(inst,kind='quartic')
            d={'N':n,'prime':p,'cubic':witness(A,p),'quartic':witness(B,p)}
            results.append(d)
            print(n,p,'det',d['cubic']['determinant_mod_prime'],d['quartic']['determinant_mod_prime'],flush=True)
    result={'description':'Phase39 rank-witness determinants (not a speedup claim)',
            'fixed_ordered_rows':[0,1],'fixed_ordered_columns':[0,1,2,3],
            'results':results}
    Path(output).write_text(json.dumps(result,indent=2)+'\n')
    return result

if __name__=='__main__':create('certificates.json')
