"""Exact small-sparse-Green forcing density theorems and finite-field audit.

Given F_N and an invertible local operator L, a Green-style solver
L y=B x computing y=F_N x requires B=L F_N. Sparsity of L does NOT
imply sparsity of B. In fact:
  any nonzero L row with <=w entries yields >=ceil(N/w) nonzero B entries
  (Donoho-Stark support uncertainty, complex field);
  for a row with w consecutive positions, at least N-w+1;
  for a two-entry row at distance a, at least N-gcd(a,N);
  for a coprime shift: >=N-1.
All bounds have explicit (model-specific) sharp examples below.

These are *nonzero-count* barriers for entrywise forcing, not general
arithmetic circuit lower bounds. Dense LF can still have fast algebraic
multiplication through sharing, which remains the true open problem.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import ceil, gcd
import json
from pathlib import Path
from field_gram_audit import primitive_root


def poly_mul_linear(coeff:list[int],root:int,p:int)->list[int]:
    out=[0]*(len(coeff)+1)
    for i,c in enumerate(coeff):
        out[i]=(out[i]-root*c)%p
        out[i+1]=(out[i+1]+c)%p
    return out


def count_frequency_support(n:int,p:int,positions:list[int],values:list[int]):
    """A row of L acts on Fourier matrix, exact over F_p."""
    root=primitive_root(n,p)
    row=[sum(c*pow(root,(j*k)%n,p) for j,c in zip(positions,values))%p
         for k in range(n)]
    return sum(z!=0 for z in row),row


def verify_case(n:int,p:int)->dict:
    assert (p-1)%n==0
    z=primitive_root(n,p)
    checked=0
    # Two coordinate entries at coprime a=1, alpha=-z^(a*n0).
    for a in sorted({1,2,3,max(1,n//4)}):
        if a%n==0:continue
        alpha=(-pow(z,a*3%n,p))%p
        support,row=count_frequency_support(n,p,[0,a],[alpha,1])
        assert support==n-gcd(a,n),(n,p,a,support)
        assert support>=ceil(n/2)
        checked+=n
    # For w consecutive positions, a degree-w-1 nonzero polynomial can
    # vanish at exactly w-1 distinct roots. Row0 has nonzero coefficient
    # (constant term), so L=identity except this row is INVERTIBLE.
    consecutive=[]
    for w in (2,3,4,min(n,6)):
        if w>=n:continue
        coeff=[1]
        for j in range(w-1):
            coeff=poly_mul_linear(coeff,pow(z,j,p),p)
        assert coeff[0] !=0
        support,row=count_frequency_support(n,p,list(range(w)),coeff)
        assert support==n-w+1,(n,p,w,support)
        consecutive.append({'window':w,'support':support})
        checked+=n
    # Universal uncertainty |supp row|*|supp Fourier row| >=N. A row
    # supported on a subgroup of w positions has exactly N/w outputs.
    subgroup=[]
    for w in (2,3,4,5):
        if w>=n or n%w:continue
        pos=[(n//w)*j for j in range(w)]
        support,row=count_frequency_support(n,p,pos,[1]*w)
        assert support==n//w
        subgroup.append({'row_support':w,'forcing_support':support})
        checked+=n
    return {'N':n,'prime':p,'frequency_values_checked':checked,
            'two_term_shift_support':{str(a):n-gcd(a,n) for a in sorted({1,2,3,max(1,n//4)})},
            'sharp_consecutive_examples':consecutive,
            'sharp_uncertainty_subgroups':subgroup}


def main():
    cases=[(16,97),(24,97),(32,97),(40,641),(48,97),(64,641),(96,97)]
    res=[verify_case(*v) for v in cases]
    obj={'statement':'Green forcing density, exact finite field rows. Complexity lower bound NOT claimed.',
         'verified_cases':res,
         'total_row_frequency_values_checked':sum(e['frequency_values_checked'] for e in res)}
    path=Path(__file__).parent/'GREEN_FORCING_RESULTS.json'
    path.write_text(json.dumps(obj,indent=2)+'\n')
    print(json.dumps({'tested_sizes':[v[0] for v in cases],
                      'total_exact_frequency_values':obj['total_row_frequency_values_checked'],
                      'sharp_consecutive':True,'sharp_general_uncertainty':True},indent=2))

if __name__=='__main__':main()
