"""Exact finite-prime projections of cyclotomic Fourier matrices.
For characteristic-zero rank LOWER bounds we reduce integer coefficient
matrices mod a prime: a nonzero minor mod p proves it is nonzero over Q.
A low rank mod p alone does NOT prove an upper bound over Q.
"""
import sympy as s, numpy as np, random, sys
P=998244353

def residue_vectors(n):
    x=s.Symbol('x')
    phi=s.Poly(s.cyclotomic_poly(n,x),x,domain=s.ZZ)
    d=phi.degree()
    z=s.Poly(1,x,domain=s.ZZ)
    out=[]
    for i in range(n):
        v=[int(z.nth(j)) for j in range(d)]
        out.append(v)
        z=(z*s.Poly(x,x,domain=s.ZZ)).rem(phi)
    return out

def rank_mod(M,prime=P):
    m=np.array(M,dtype=np.int64)%prime
    row=0
    pivots=[]
    for col in range(m.shape[1]):
        if row>=len(m):break
        nz=np.flatnonzero(m[row:,col])
        if not len(nz):continue
        j=row+int(nz[0]);m[[row,j]]=m[[j,row]]
        inv=pow(int(m[row,col]),-1,prime)
        m[row,col:]=(m[row,col:]*inv)%prime
        ids=np.flatnonzero(m[row+1:,col])+row+1
        if len(ids):
            block=(m[ids,col:]-m[ids,col,None]*m[row,col:])%prime
            m[ids,col:]=block
        pivots.append(col)
        row+=1
    return row,pivots

def run(n,seeds=(11,19)):
    vectors=residue_vectors(n)
    degree=len(vectors[0]);detail=[]
    for seed in seeds:
        rng=random.Random(seed+13000*n)
        l=[0]+[rng.randrange(1,P) for _ in range(degree-1)]
        vals=[sum((x*a for x,a in zip(l,v)))%P for v in vectors]
        M=[[vals[(j*k)%n] for k in range(n)] for j in range(n)]
        rank,pivots=rank_mod(M)
        detail.append((seed,rank,len(pivots)))
    return n,degree,detail

if __name__=='__main__':
    ns=[int(x) for x in sys.argv[1:]] or [8,16,32,60,120,240]
    for n in ns:print(run(n),flush=True)
