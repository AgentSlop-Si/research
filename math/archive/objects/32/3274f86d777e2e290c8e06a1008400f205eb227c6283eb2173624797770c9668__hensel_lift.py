#!/usr/bin/env python3
"""Optional constructive 97-adic check of the simple-root claim.
The coefficients are lifted from the saved INTEGER Green branch data.
A lifted root is not an ordinary complex numeric FFT factorization; it
supplies a characteristic-zero algebraic EXISTENCE certificate through Hensel.
"""
import json,math
from pathlib import Path
BASE=97
HERE=Path(__file__).parent

def mm(A,B,m):return [[sum(a*b for a,b in zip(row,col))%m for col in zip(*B)] for row in A]
def di(x):return [[x[i] if i==j else 0 for j in range(len(x))] for i in range(len(x))]
def inv(A,m):
    n=len(A);T=[[x%m for x in row]+[int(i==j) for j in range(n)] for i,row in enumerate(A)]
    for j in range(n):
        k=next((i for i in range(j,n) if math.gcd(T[i][j],BASE)==1),None)
        if k is None:raise ValueError('no unit pivot')
        T[j],T[k]=T[k],T[j]
        s=pow(T[j][j],-1,m)
        T[j]=[(x*s)%m for x in T[j]]
        for i in range(n):
            if i!=j:
                z=T[i][j]
                T[i]=[(x-z*y)%m for x,y in zip(T[i],T[j])]
    return [row[n:] for row in T]

def reconstruct_green(b,m):
    p=b['cycle'];w=b['weights'];n=len(p)
    prod=1
    for x in w:prod=prod*x%m
    s=pow((1-prod)%m,-1,m)
    G=[[0]*n for _ in range(n)]
    for i in range(n):
        j=i;c=s
        for k in range(n):
            G[i][j]=c;c=c*w[j]%m;j=p[j]
    ld=b['left_diag'];rd=b['right_diag']
    G=[[(ld[i]*G[i][j]*rd[j])%m for j in range(n)] for i in range(n)]
    a=b['row_permutation'];bcol=b['col_permutation']
    return [[G[a[i]][bcol[j]] for j in range(n)] for i in range(n)]

def lift_root(root,n,m):
    assert (root%BASE)**n%BASE==1
    omega=root
    while (omega**n-1)%m!=0:
        new=(omega-(pow(omega,n,m)-1)*pow(n*pow(omega,n-1,m),-1,m))%m
        if new==omega:break
        omega=new
    assert pow(omega,n,m)==1
    return omega

def commdet_at_t(cert,t,m):
    n=cert['n'];omega=lift_root(cert['root'],n,m)
    gs_A=[reconstruct_green(b,m) for b in cert['trace_A']]
    gs_B=[reconstruct_green(b,m) for b in cert['trace_B']]
    A=[[sum(G[i][j] for G in gs_A)%m for j in range(n)] for i in range(n)]
    B=[[sum(G[i][j] for G in gs_B)%m for j in range(n)] for i in range(n)]
    B0=[(B[i][0]+(t-1)*gs_B[0][i][0])%m for i in range(n)]
    AI=inv(A,m)
    T=[]
    for j in (1,2):
        ratio=[B0[i]*pow(B[i][j],-1,m)%m for i in range(n)]
        T.append(mm(A,mm(di(ratio),mm(AI,di([pow(omega,j*i,m) for i in range(n)]),m),m),m))
    comm=[[sum(T[0][i][k]*T[1][k][j]-T[1][i][k]*T[0][k][j] for k in range(n))%m for j in range(n)] for i in range(n)]
    # 3x3 / 4x4 Leibniz determinant independent of Gaussian elimination
    from itertools import permutations
    out=0
    for pi in permutations(range(n)):
        signs=(-1)**sum(pi[i]>pi[j] for i in range(n) for j in range(i+1,n))
        term=signs
        for i,j in enumerate(pi):term=term*comm[i][j]%m
        out=(out+term)%m
    return out

def main():
    result={}
    for n in (3,4):
        c=json.loads((HERE/f'CERT_N{n}.json').read_text())
        t=1
        residues=[]
        for k in range(1,5):
            m=BASE**k
            f=commdet_at_t(c,t,m)
            if k==1:assert f==0
            assert f % (BASE**(k-1))==0,(n,k,t,f)
            deriv=c['derivative_modp']
            digit=(-(f//(BASE**(k-1)))*pow(deriv,-1,BASE))%BASE
            t=t+digit*BASE**(k-1)
            assert commdet_at_t(c,t,m)==0,(n,k,t)
            residues.append({'modulus':m,'lifted_root_t':t,'lifted_Fourier_root_omega':lift_root(c['root'],n,m)})
        result[str(n)]=residues
        print(f'N={n}: Hensel lifts',residues)
    (HERE/'HENSEL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
