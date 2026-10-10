#!/usr/bin/env python3
"""Independent SymPy-based checker of archived modular 4-/6-Green commutator witnesses."""
import json
from pathlib import Path
from sympy import Matrix, eye, diag, zeros
p=97
folder=Path(__file__).parent
witnesses=json.loads((folder/'CERTIFICATES.json').read_text())

def mod(M):return M.applyfunc(lambda a:int(a)%p)

def reconstruct(n,x):
    pi=x['cycle']; wi=x['weights']; P=eye(n)
    for i,j in enumerate(pi):P[i,j]-=wi[i]
    G=mod(P).inv_mod(p)
    out=mod(diag(*x['left_diag'])*G*diag(*x['right_diag']))
    pr=x['row_permutation'];pc=x['col_permutation']
    return Matrix([[int(out[pr[i],pc[j]])%p for j in range(n)] for i in range(n)])


def root(n):
    for g in range(2,p):
        z=pow(g,(p-1)//n,p)
        if pow(z,n,p)==1 and all(pow(z,n//q,p)!=1 for q in prime_factors(n)):
            return z
    raise ValueError

def prime_factors(n):
    f=[];z=2
    while z*z<=n:
        if n%z==0:
            f.append(z)
            while n%z==0:n//=z
        z+=1
    if n>1:f.append(n)
    return f

for c in witnesses:
    n=c['N']; z=root(n)
    leaves=[reconstruct(n,entry) for entry in c['branch_parameters']]
    A=mod(leaves[0]+leaves[1]);B=mod(leaves[2]+leaves[3]);C=mod(leaves[4]+leaves[5]) if not c['two_stage'] else eye(n)
    for letter,M in [('A',A),('B',B),('C',C)]:
        assert M==Matrix(c[letter]),(n,letter,'failed-reconstruction')
    F=Matrix([[pow(z,i*j,p) for j in range(n)] for i in range(n)])
    H=mod(F*C.inv_mod(p))
    P=[]
    AI=A.inv_mod(p)
    for j in range(n):
        bj=[int(B[i,j])%p for i in range(n)]
        hj=[int(H[i,j])%p for i in range(n)]
        assert all(bj)
        P.append(mod(diag(*[pow(t,-1,p) for t in bj])*AI*diag(*hj)))
    assert P[0].det()%p!=0
    P0i=P[0].inv_mod(p)
    T1=mod(P0i*P[1]);T2=mod(P0i*P[2]);comm=mod(T1*T2-T2*T1)
    d=int(comm.det())%p
    assert d==c['det_commutator']!=0
    print(f"independent PASS n={n}, two_stage={c['two_stage']}, det(comm) mod 97={d}")
print('All',len(witnesses),'independent signed-parameter Green certificates passed.')
