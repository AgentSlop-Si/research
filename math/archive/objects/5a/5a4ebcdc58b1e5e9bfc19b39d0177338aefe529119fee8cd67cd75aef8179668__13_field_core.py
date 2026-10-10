"""Self-contained finite-field linear algebra for exact DFT/Green gate certificates.
All field tests use F_998244353, with transform lengths dividing p-1.
"""
from __future__ import annotations
P=998244353
GEN=3


def sqrt_mod(a:int,p:int=P)->int:
    a%=p
    if not a:return 0
    assert pow(a,(p-1)//2,p)==1
    if p%4==3:return pow(a,(p+1)//4,p)
    q=p-1;s=0
    while not q&1:q//=2;s+=1
    z=2
    while pow(z,(p-1)//2,p)!=p-1:z+=1
    c=pow(z,q,p);t=pow(a,q,p);r=pow(a,(q+1)//2,p);m=s
    while t!=1:
        i=1; t2=t*t%p
        while t2!=1:t2=t2*t2%p;i+=1
        b=pow(c,1<<(m-i-1),p)
        r=r*b%p;t=t*b*b%p;c=b*b%p;m=i
    assert r*r%p==a
    return r


def root_n(n):
    assert n>=4 and n&(n-1)==0 and (P-1)%n==0
    return pow(GEN,-((P-1)//n),P)


def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]


def matmul(A,B):
    n=len(A);m=len(B[0]);r=len(B)
    out=[[0]*m for _ in range(n)]
    for i in range(n):
        for k in range(r):
            a=A[i][k]
            if a:
                rowb=B[k]
                for j in range(m):out[i][j]+=a*rowb[j]
        out[i]=[v%P for v in out[i]]
    return out


def inverse(A):
    n=len(A);x=[[v%P for v in row]+[int(i==j) for j in range(n)] for i,row in enumerate(A)]
    for j in range(n):
        pivot=next((r for r in range(j,n) if x[r][j]),None)
        if pivot is None:raise ValueError('matrix singular in field')
        x[j],x[pivot]=x[pivot],x[j]
        row=x[j];scale=pow(row[j],-1,P)
        for k in range(j,2*n):row[k]=row[k]*scale%P
        for i in range(n):
            if i!=j:
                z=x[i][j]
                if z:
                    dst=x[i]
                    for k in range(j,2*n):dst[k]=(dst[k]-z*row[k])%P
    return [row[n:] for row in x]


def dft(n):
    w=root_n(n);u=pow(sqrt_mod(n),-1,P)
    return [[pow(w,i*j%n,P)*u%P for j in range(n)] for i in range(n)]


def cyclic_operators(n):
    w=root_n(n)
    v=[(pow(w,j,P)+pow(w,-j,P))%P for j in range(n)]
    T=[[0]*n for _ in range(n)]
    V=[[0]*n for _ in range(n)]
    for i in range(n):
        T[i][(i+1)%n]=(T[i][(i+1)%n]+1)%P
        T[i][(i-1)%n]=(T[i][(i-1)%n]+1)%P
        V[i][i]=v[i]
    return T,V


def add(A,B):return [[(v+w)%P for v,w in zip(a,b)] for a,b in zip(A,B)]


def reflection(n):return [[int(j==(-i)%n) for j in range(n)] for i in range(n)]


def monomial(q,perm):
    n=len(q);assert sorted(perm)==list(range(n)) and all(v%P for v in q)
    C=[[0]*n for _ in range(n)]
    for i,k in enumerate(perm):C[i][k]=q[i]%P
    return C


def conjugate_pair(A,B):
    """U_1=A^-1 V A; U_2=A^-1 T A; W_1=B T B^-1; W_2=B V B^-1."""
    n=len(A);T,V=cyclic_operators(n)
    Ai=inverse(A);Bi=inverse(B)
    return ((matmul(Ai,matmul(V,A)),matmul(Ai,matmul(T,A))),
            (matmul(B,matmul(T,Bi)),matmul(B,matmul(V,Bi))))


def defect_count(M):
    n=len(M);T,V=cyclic_operators(n)
    dt=matmul(M,T);vt=matmul(V,M)
    dv=matmul(M,V);tm=matmul(T,M)
    return (sum(a!=b for r,s in zip(dt,vt) for a,b in zip(r,s)),
            sum(a!=b for r,s in zip(dv,tm) for a,b in zip(r,s)))
