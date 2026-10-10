#!/usr/bin/env python3
"""Exact rational/cyclotomic control for the N=4 recorded frozen instance.
Uses data only; does not execute/import any submitted or other verifier code.
"""
import itertools
import json
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parent
P=65537
record=json.loads((ROOT/'FRESH_PAIR_OBSTRUCTION_RESULTS.json').read_text())['fourier_certificates'][0]
assert record['N']==4
weights=record['integer_weight_arrays']
s=2;n=4
maps=[]
for kind in range(4):
    q=[]
    for x in range(s):
        for y in range(s):
            xx=(x+2*y+(kind==1))%s if kind<2 else x
            yy=(y+2*x+(kind==3))%s if kind>=2 else y
            q.append(xx*s+yy)
    maps.append(q)
I=sp.eye(n)
Q=[]
for q in maps:
    m=sp.zeros(n)
    for i,j in enumerate(q):m[i,j]=1
    Q.append(m)
greens=[]
frozen_denominator_residues=[]
for t in range(2):
    stage=[]
    for k in range(4):
        pencil=I-sp.diag(*weights[t][k])*Q[k]
        g=pencil.inv();assert pencil*g==I
        stage.append(g)
        if (t==0 and k!=1) or (t==1 and k!=3):
            residue=int(pencil.det())%P
            assert residue!=0
            frozen_denominator_residues.append(residue)
    greens.append(stage)
a=sp.Rational(1,4)
A=a*(greens[1][0]+greens[1][1]+greens[1][2])
B=a*(greens[0][0]+greens[0][2]+greens[0][3])
F=sp.Matrix(n,n,lambda i,j:sp.I**(i*j))
X=F-A*B
R=(X-a*A-a*B-a*a*I)*Q[1].T
U=Q[3]*(X-a*A)*Q[1].T
W=X-a*B
Z=Q[3]*X
rows=[]
for j in range(n):
    rows.append([-R[0,j]*W[1,j]+R[1,j]*W[0,j],
                 U[0,j]*W[1,j]-R[1,j]*Z[0,j],
                 R[0,j]*Z[1,j]-U[1,j]*W[0,j],
                -U[0,j]*Z[1,j]+U[1,j]*Z[0,j]])
M=sp.Matrix(rows).applyfunc(sp.expand)
# Leibniz determinant avoids relying on the modular elimination routine.
d=0
for perm in itertools.permutations(range(4)):
    inversions=sum(perm[i]>perm[j] for i in range(4) for j in range(i+1,4))
    term=(-1)**inversions
    for i in range(4):term*=M[i,perm[i]]
    d+=sp.expand(term)
d=sp.expand(d)
real=sp.re(d);imag=sp.im(d)
assert real!=0 or imag!=0

def modrat(z):
    num,den=sp.fraction(z)
    return int(num)%P*pow(int(den)%P,-1,P)%P

omega=record['omega']
reduced=(modrat(real)+omega*modrat(imag))%P
assert reduced==27524==record['certificate']['determinant_mod_p']
modmatrix=[[int((modrat(sp.re(z))+omega*modrat(sp.im(z)))%P) for z in list(M.row(i))] for i in range(n)]
assert modmatrix==record['certificate']['minor_matrix']
result={'N':4,'method':'SymPy exact rational matrices with zeta=i; 24-term determinant expansion. Data-only input, no verifier imports.',
        'frozen_pencil_determinants_mod_p':frozen_denominator_residues,
        'minor_real_numerator':str(sp.numer(real)),'minor_real_denominator':str(sp.denom(real)),
        'minor_imag_numerator':str(sp.numer(imag)),'minor_imag_denominator':str(sp.denom(imag)),
        'minor_nonzero_in_Q_i':True,'zeta_mod_p':omega,'all_minor_entries_match_modular_data':True,
        'determinant_mod_p':reduced}
(ROOT/'FRESH_CHARACTERISTIC_ZERO_N4.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if 'numerator' not in k and 'denominator' not in k}))
