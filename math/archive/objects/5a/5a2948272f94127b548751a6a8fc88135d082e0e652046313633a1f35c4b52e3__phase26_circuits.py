"""Hero #1 Phase 26: model-separated, exact finite-field circuit audit.

This is a research demonstrator, not a sub-NlogN FFT. The pure Python
reference counts field additions/subtractions and nontrivial scalar field
multiplications, treating even multiplication by a square root of -1 as paid.
All root tables are paid separately; polynomial modular arithmetic is exact.
"""
from dataclasses import dataclass
from math import log2

P = 2013265921
GENERATOR = 31

@dataclass
class Ledger:
    adds: int = 0
    muls: int = 0
    data_reads: int = 0
    data_writes: int = 0
    def arithmetic(self): return self.adds + self.muls


def n_root(n, p=P, g=GENERATOR):
    if (p-1) % n:
        raise ValueError('N does not divide p-1')
    w=pow(g, (p-1)//n, p)
    assert pow(w,n,p)==1
    for ell in prime_factors(n):
        assert pow(w,n//ell,p)!=1
    return w


def prime_factors(n):
    factors=[]
    d=2
    while d*d<=n:
        if n%d==0:
            factors.append(d)
            while n%d==0:n//=d
        d+=1
    if n>1:factors.append(n)
    return factors


def root_table(n,p=P,g=GENERATOR):
    w=n_root(n,p,g)
    powers=[1]*n
    for k in range(1,n):powers[k]=powers[k-1]*w%p
    return powers, n-1


def scalar_radix2(x, powers, p=P, *, shear=False):
    """Optimized DIF radix2, optional nonunitary lift (not an improvement)."""
    n=len(x)
    if n<2 or n&(n-1):raise ValueError('power-of-2 n >=2')
    if len(powers)!=n:raise ValueError('mismatched root table')
    a=[v%p for v in x]
    c=Ledger()
    h=n//2
    while h:
        step=n//(2*h)
        for start in range(0,n,2*h):
            for j in range(h):
                u=a[start+j];v=a[start+h+j]
                if shear:
                    # H = L(1) * diag(1,-2) * U(1)
                    # t=u+v; diff=t-2v; this is a nonunitary LDU implementation.
                    top=(u+v)%p; neg2v=(-2*v)%p; bottom=(top+neg2v)%p
                    c.adds+=2;c.muls+=1
                else:
                    top=(u+v)%p;bottom=(u-v)%p
                    c.adds+=2
                if j>0:
                    bottom=bottom*powers[j*step]%p
                    c.muls+=1
                a[start+j]=top;a[start+h+j]=bottom
                c.data_reads+=2;c.data_writes+=2
        h//=2
    t=n.bit_length()-1
    out=[a[int(f'{k:0{t}b}'[::-1],2)] for k in range(n)]
    return out,c


def split_radix_dif(x, powers, p=P):
    """Exact split-radix DIF with charged sqrt(-1) multiplication.

    For n divisible by 4: Q_j=(x_j-x_{j+n/2}) + i(x_{j+n/4}-x_{j+3n/4}),
    R_j with a minus sign; odd indices split 4r+1 and 4r+3.
    Recurrence C(n)=C(n/2)+2C(n/4)+(9n/4-2), n>=4.
    This precisely matches optimized radix2 in this scalar field model.
    """
    n=len(x)
    if n<2 or n&(n-1):raise ValueError('power-of-2 n >=2')
    if len(powers)!=n:raise ValueError('mismatched root table')
    c=Ledger()
    def rec(v,stride):
        m=len(v)
        if m==1:return [v[0]]
        if m==2:
            c.adds+=2
            c.data_reads+=2;c.data_writes+=2
            return [(v[0]+v[1])%p,(v[0]-v[1])%p]
        q=m//4;h=m//2
        even=[0]*h
        minus=[0]*h
        for j in range(h):
            even[j]=(v[j]+v[j+h])%p
            minus[j]=(v[j]-v[j+h])%p
        c.adds+=m;c.data_reads+=m;c.data_writes+=m
        left=[0]*q;right=[0]*q
        imag=powers[q*stride]
        for j in range(q):
            t=imag*minus[j+q]%p
            u=(minus[j]+t)%p;z=(minus[j]-t)%p
            if j:
                u=u*powers[j*stride]%p
                z=z*powers[3*j*stride]%p
                c.muls+=2
            left[j]=u;right[j]=z
        c.adds+=2*q;c.muls+=q
        c.data_reads+=2*q;c.data_writes+=2*q
        evens=rec(even,stride*2)
        odds1=rec(left,stride*4)
        odds3=rec(right,stride*4)
        ans=[0]*m
        for j in range(h):ans[2*j]=evens[j]
        for j in range(q):ans[4*j+1]=odds1[j];ans[4*j+3]=odds3[j]
        return ans
    return rec([v%p for v in x],1),c


def radix2_predicted(n):
    t=n.bit_length()-1
    assert 1<<t==n
    return n*t,(n//2)*t-n+1


def independent_dft(x,powers,p=P):
    n=len(x);a=[]
    for k in range(n):
        out=0
        for j,v in enumerate(x):
            out=(out+v*powers[(j*k)%n])%p
        a.append(out)
    return a


def gt3_split(x,p=P,g=GENERATOR,method='split'):
    """Good-Thomas factorization with independently implemented dyadic branch."""
    N=len(x)
    if N%3:raise ValueError('N must be 3*2^t')
    G=N//3
    if G<2 or G&(G-1):raise ValueError('N must be 3*2^t')
    powers,_=root_table(N,p,g)
    a=pow(3,-1,G);b=pow(G,-1,3)
    eG=3*a;e3=G*b
    gr=[powers[3*j] for j in range(G)]
    ins=[[x[(j*eG+t*e3)%N] for j in range(G)] for t in range(3)]
    outputs=[];counter=Ledger()
    for row in ins:
        if method=='split':r,c=split_radix_dif(row,gr,p)
        elif method=='shear':r,c=scalar_radix2(row,gr,p,shear=True)
        else:r,c=scalar_radix2(row,gr,p)
        outputs.append(r)
        counter.adds+=c.adds;counter.muls+=c.muls
    eta=powers[G]
    inv2=(p+1)//2
    v=-inv2%p
    w=(eta-powers[2*G])*inv2%p
    out=[0]*N
    for j in range(G):
        a0,b0,c0=(outputs[t][j] for t in range(3))
        t=(b0+c0)%p;d=(b0-c0)%p
        y0=(a0+t)%p;mid=(a0+v*t)%p;z=w*d%p
        y1=(mid+z)%p;y2=(mid-z)%p
        counter.adds+=6;counter.muls+=2
        out[(3*j)%N]=y0
        out[(3*j+G)%N]=y1
        out[(3*j+2*G)%N]=y2
    return out,counter
