#!/usr/bin/env python3
"""Exact unbalanced/balanced Fourier operator-Schmidt rank and flat spectrum.

Let N=A*B with A,B powers of two, A<=B, and index input x=aB+b,
output y=cB+d (a,c in [A], b,d in [B]). Let R be the realignment
of the *unitary* Fourier matrix with rows (a,c), cols (b,d):
 R[(a,c),(b,d)] = (1/sqrt(N))*omega_N^(-(aB+b)(cB+d)).
As A divides B,
 R = (1/sqrt(N))*[omega_A^(-a*d-c*b)]*diag(omega_N^(-b*d)).
Each row of middle matrix is orthogonal to every other (inner product
B^2*delta_(a,a')*delta_(c,c')), hence
      R R* = (B/A) I_(A^2).
All A^2 nonzero singular values equal sqrt(B/A).
An exact sum of s tensor-separable operators requires s>=A^2.
Best relative Frobenius error of rank-s separable approximation:
 sqrt(1-s/A^2), for 0<=s<=A^2.

This is only about a ONE-SHOT sum of tensor-product operators across
this particular register partition, not a general arithmetic FFT lower bound.
"""
from __future__ import annotations
import json
import math
import numpy as np
from phase10_rational import P,root_table
from operator_schmidt_gate import rank_mod


def run(n,a):
    if n%a:raise ValueError
    b=n//a
    if a>b or a&(a-1) or b&(b-1) or a==0:raise ValueError
    tbl=root_table(n)
    tab_a=root_table(a)
    entries=[]
    for ia in range(a):
        for oc in range(a):
            row=[]
            for ib in range(b):
                for od in range(b):
                    x=ia*b+ib;y=oc*b+od
                    actual=tbl[(-x*y)%n]
                    predicted=tab_a[(-ia*od-oc*ib)%a]*tbl[(-ib*od)%n]%P
                    assert actual==predicted
                    row.append(actual)
            entries.append(row)
    rk=rank_mod(entries)
    assert rk==a*a
    # Independent numerical Gram verification, no numerical proof needed.
    aa=np.arange(a);bb=np.arange(b)
    # Rows correspond (ia,oc) columns (ib,od).
    rows=[]
    for ia in range(a):
        for oc in range(a):
            x=ia*b+bb[:,None]
            y=oc*b+bb[None,:]
            rows.append((np.exp(-2j*np.pi*(x*y)/n)/np.sqrt(n)).reshape(-1))
    matrix=np.array(rows)
    gram=matrix@matrix.conj().T
    gram_error=float(np.max(np.abs(gram-(b/a)*np.eye(a*a))))
    assert gram_error<1e-11*max(1,b/a)
    sv=np.linalg.svd(matrix,compute_uv=False)
    assert np.max(np.abs(sv-np.sqrt(b/a)))<1e-10
    return {'n':n,'left_register_dim':a,'right_register_dim':b,
            'exact_modular_realignment_rank':rk,
            'exact_theoretical_rank':a*a,
            'flat_schmidt_coefficient':math.sqrt(b/a),
            'max_gram_residual_complex128':gram_error,
            'checked_modular_entries':a*a*b*b,
            'relative_error_at_50pct_rank':math.sqrt(1-(a*a//2)/(a*a))}


def main():
    records=[]
    for n,a in [(16,2),(16,4),(64,2),(64,4),(64,8),(128,4),(256,4),(256,8),(256,16)]:
        v=run(n,a)
        records.append(v)
        print('N=%-3d A=%-2d B=%-2d rank=%-3d flat singular=%.4f gram max=%.2g' %
              (v['n'],v['left_register_dim'],v['right_register_dim'],
               v['exact_modular_realignment_rank'],
               v['flat_schmidt_coefficient'],v['max_gram_residual_complex128']))
    with open('SCHMIDT_GENERAL_AUDIT.json','w') as f:
        json.dump({'exact_theorem':'operator-Schmidt rank min(A,B)^2 and flat nonzero Schmidt spectrum for the Fourier operator at a contiguous bit cut',
        'approximation_consequence':'relative Frobenius error >=sqrt(1-s/A^2) for s separable terms across A|B and A<=B',
        'caveat':'one-shot tensor separability restriction; not an unrestricted exact FFT lower bound',
        'cases':records},f,indent=2)

if __name__=='__main__':main()
