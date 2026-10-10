#!/usr/bin/env python3
"""Independent SymPy check: reconstruct every Green via sparse-matrix inversion;
obtain the quadratic-lift coefficients by evaluating/polarizing minors rather
than by using the explicit four-term coefficient formula in verify.py.
Requires sympy; exact GF(97) computations.
"""
import json,itertools
from pathlib import Path
import sympy as sp
P=97
HERE=Path(__file__).parent

def red(M):return M.applyfunc(lambda x: int(x)%P)
def weighted_green(b):
    n=len(b['cycle']); W=sp.eye(n)
    for i,j in enumerate(b['cycle']):W[i,j]=(W[i,j]-b['weights'][i])%P
    G=W.inv_mod(P)
    G=sp.diag(*[x%P for x in b['left_diag']])*G*sp.diag(*[x%P for x in b['right_diag']])
    G=red(G)
    p1=b['row_permutation'];p2=b['col_permutation']
    return sp.Matrix([[int(G[p1[i],p2[j]]) for j in range(n)] for i in range(n)])

def pcols(A,B,root):
    n=A.rows;AI=A.inv_mod(P);out=[]
    for j in range(n):
        invb=[pow(int(B[i,j]),-1,P) for i in range(n)]
        h=[pow(root,j*i,P) for i in range(n)]
        out.append(red(sp.diag(*invb)*AI*sp.diag(*h)))
    return out

def all_minors(Ps,c):
    W=sp.Matrix.hstack(*[red(Pj*c) for Pj in Ps[:3]])
    n=W.rows;out=[]
    for j,k in itertools.combinations(range(3),2):
        for u,v in itertools.combinations(range(n),2):
            out.append((W[u,j]*W[v,k]-W[u,k]*W[v,j])%P)
    return sp.Matrix(out)

def main():
    for n in (3,4):
        cert=json.loads((HERE/f'CERT_N{n}.json').read_text())
        branches_A=[weighted_green(x) for x in cert['trace_A']]
        branches_B=[weighted_green(x) for x in cert['trace_B']]
        A=red(sum(branches_A,sp.zeros(n,n)))
        B=red(sum(branches_B,sp.zeros(n,n)))
        assert A.tolist()==cert['A'] and B.tolist()==cert['B']
        omega=cert['root']
        Ps=pcols(A,B,omega)
        pairs=list(itertools.combinations_with_replacement(range(n),2))
        Q=sp.zeros(3*(n*(n-1)//2),len(pairs))
        f0={}
        for i in range(n):
            u=sp.zeros(n,1);u[i]=1
            f0[i]=all_minors(Ps,u)
        for q,(a,b) in enumerate(pairs):
            if a==b:col=f0[a]
            else:
                v=sp.zeros(n,1);v[a]=v[b]=1
                col=all_minors(Ps,v)-f0[a]-f0[b]
            for k in range(Q.rows): Q[k,q]=col[k]%P
        sub=Q[cert['results_pivot_rows'],:] if False else sp.Matrix([list(Q.row(i)) for i in cert['pivot_rows']]) if 'pivot_rows' in cert else None
        # Calculate rank using modular arithmetic by checking the row set
        # separately saved by the primary verifier's results JSON.
        result=json.loads((HERE/'RESULTS.json').read_text())[0 if n==3 else 1]
        sub=sp.Matrix([list(Q.row(i)) for i in result['pivot_rows']])
        d=int(sub.det())%P
        assert d==result['nonzero_pivot_minor_mod97'] !=0, (n,d,result)
        assert int(A.det())%P!=0 and int(B.det())%P!=0
        print(f'N={n}: independent sparse-denominator inversion + polarization: pivot minor = {d} mod 97, PASSED')
    print('All independent checks passed')
if __name__=='__main__':main()
