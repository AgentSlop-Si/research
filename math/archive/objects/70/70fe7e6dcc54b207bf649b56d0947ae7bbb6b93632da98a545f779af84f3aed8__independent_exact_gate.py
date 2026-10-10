"""An independent, simpler cyclotomic-degree certificate at selected lengths.

For any k x k submatrix F_N[R,C] with R,C in {0,...,B-1},
P(x)=det(x**(i*j)) has degree <= k*(B-1)^2. P is a NONZERO
integer polynomial because the rearrangement inequality makes its
highest-degree monomial unique for sorted, distinct row/column labels.
If Euler phi(N)>k*(B-1)^2, then a primitive Nth root cannot annihilate P.

Unlike small_arc_gate, this result requires a totient inequality and hence
may not apply to all N>2300; it is an independent check at N=4096.
"""
from __future__ import annotations
import math


def euler_phi(n:int)->int:
    assert n>0
    rem=n; tot=n;k=2
    while k*k<=rem:
        if rem%k==0:
            tot=tot//k*(k-1)
            while rem%k==0:rem//=k
        k+=1
    if rem>1:tot=tot//rem*(rem-1)
    return tot


def full_minors_by_degree(n:int,B:int,k:int)->dict:
    degree=k*(B-1)**2
    phi=euler_phi(n)
    return {'N':n,'grid_size':B,'minor_size':k,
            'max_formal_degree':degree,'cyclotomic_degree':phi,
            'all_minors_proved_nonzero':phi>degree,
            'reason':'Unique largest exponent from rearrangement inequality, followed by deg(P)<deg(Phi_N).'}

if __name__=='__main__':
    import json
    for n in (2301,4096,8192,16384):
        print(json.dumps(full_minors_by_degree(n,26,3)))
