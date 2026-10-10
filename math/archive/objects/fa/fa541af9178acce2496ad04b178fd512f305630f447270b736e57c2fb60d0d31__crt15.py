"""Phase 27: exact CRT15 FFT vs comparably optimized Cooley-Tukey.

Research prototype over root-rich prime fields. Addition/subtraction=1,
multiplication by any nonidentity field scalar=1; phase roots counted even if
they are e.g. square roots of -1. Input permutations not treated as arithmetic.
All codelets are explicitly expanded. Not a sub-NlogN algorithm.
"""
from dataclasses import dataclass
from math import log2

P=2013265921
GENERATOR=31
ALT_P=754974721
ALT_GENERATOR=11   # verified primitive root by n_root

@dataclass
class Cost:
    adds:int=0
    muls:int=0
    reads:int=0
    writes:int=0
    def total(self):return self.adds+self.muls
    def merge(self,other):
        self.adds+=other.adds;self.muls+=other.muls
        self.reads+=other.reads;self.writes+=other.writes


def factors(n):
    ans=[]; d=2
    while d*d<=n:
        if n%d==0:
            ans.append(d)
            while n%d==0:n//=d
        d+=1
    if n>1:ans.append(n)
    return ans


def n_root(n,p=P,gen=GENERATOR):
    if (p-1)%n:raise ValueError('transform length must divide p-1')
    root=pow(gen,(p-1)//n,p)
    if pow(root,n,p)!=1 or any(pow(root,n//q,p)==1 for q in factors(n)):
        raise ValueError('generator did not give primitive root')
    return root


def table(root,n,p):
    arr=[1]*n
    for j in range(1,n):arr[j]=arr[j-1]*root%p
    return arr,n-1


def dft3(a,w,p,c=None):
    """6 additions, 2 scalar mul; w primitive cube root."""
    if c is None:c=Cost()
    x0,x1,x2=a
    iw=pow(2,-1,p)
    v=(w+pow(w,2,p))*iw%p
    u=(w-pow(w,2,p))*iw%p
    s=(x1+x2)%p;d=(x1-x2)%p
    y0=(x0+s)%p;base=(x0+v*s)%p;t=u*d%p
    y1=(base+t)%p;y2=(base-t)%p
    c.adds+=6;c.muls+=2;c.reads+=3;c.writes+=3
    return [y0,y1,y2]


def dft5(a,w,p,c=None):
    """17 additions, 5 scalar mul, explicitly expanded Winograd DFT5."""
    if c is None:c=Cost()
    x0,x1,x2,x3,x4=a
    w2=w*w%p;w3=w2*w%p;w4=w3*w%p
    inv2=pow(2,-1,p)
    c1=(w+w4)*inv2%p
    c2=(w2+w3)*inv2%p
    h1=(w-w4)*inv2%p
    h2=(w2-w3)*inv2%p
    ca=(c1+c2)*inv2%p
    cd=(c1-c2)*inv2%p
    s1=(x1+x4)%p;s2=(x2+x3)%p
    d1=(x1-x4)%p;d2=(x2-x3)%p
    s=(s1+s2)%p;t=(s1-s2)%p
    mid=(x0+ca*s)%p
    v=cd*t%p
    e1=(mid+v)%p;e2=(mid-v)%p
    pair=(d1+d2)%p
    k1=h1*pair%p;k2=(h2-h1)*d2%p;k3=(h1+h2)*d1%p
    o1=(k1+k2)%p;o2=(k3-k1)%p
    y0=(x0+s)%p
    y1=(e1+o1)%p;y4=(e1-o1)%p
    y2=(e2+o2)%p;y3=(e2-o2)%p
    c.adds+=17;c.muls+=5;c.reads+=5;c.writes+=5
    return [y0,y1,y2,y3,y4]


def dft15(a,w,p,c=None):
    """GT3x5: five exact DFT3 and three exact DFT5. No twiddle gates."""
    if c is None:c=Cost()
    assert len(a)==15
    ea=5*pow(5,-1,3);eb=3*pow(3,-1,5)
    grid=[[a[(ea*u+eb*v)%15] for u in range(3)] for v in range(5)]
    w3=pow(w,5,p);w5=pow(w,3,p)
    g=[dft3(row,w3,p,c) for row in grid]
    out=[None]*15
    for r in range(3):
        z=dft5([g[v][r] for v in range(5)],w5,p,c)
        for s in range(5):out[(5*r+3*s)%15]=z[s]
    return out


def fft_dyadic(a,w,p,c=None):
    """In-place DIF radix2, per stage root exponent, bit-reverse output."""
    if c is None:c=Cost()
    n=len(a)
    if n==1:return [a[0]%p]
    if n&(n-1):raise ValueError('dyadic length required')
    powers,_=table(w,n,p)
    b=[x%p for x in a]
    h=n//2
    while h:
        stride=n//(2*h)
        for start in range(0,n,2*h):
            for j in range(h):
                v1=b[start+j];v2=b[start+h+j]
                s=(v1+v2)%p;d=(v1-v2)%p
                c.adds+=2;c.reads+=2;c.writes+=2
                if j:
                    d=d*powers[j*stride]%p;c.muls+=1
                b[start+j]=s;b[start+h+j]=d
        h//=2
    t=n.bit_length()-1
    return [b[int(f'{k:0{t}b}'[::-1],2)] for k in range(n)]


def gt15(a,p=P,gen=GENERATOR):
    """CRT N=15*2^t, dyadic subtransforms and full 15 point codelets."""
    N=len(a)
    if N%15:raise ValueError('N divisible by 15 required')
    G=N//15
    if G&(G-1):raise ValueError('N/15 must be dyadic')
    w=n_root(N,p,gen);wG=pow(w,15,p);w15=pow(w,G,p)
    eg=15*pow(15,-1,G) if G>1 else 0
    e15=G*pow(G,-1,15)
    cost=Cost();z=[]
    for v in range(15):
        row=[a[(eg*u+e15*v)%N] for u in range(G)]
        z.append(fft_dyadic(row,wG,p,cost))
    out=[None]*N
    for r in range(G):
        row=dft15([z[v][r] for v in range(15)],w15,p,cost)
        for s in range(15):out[(15*r+G*s)%N]=row[s]
    return out,cost


def ct15(a,p=P,gen=GENERATOR,drop_twiddle=False):
    """Independent CT N=15*2^t with 15 x G and G x15 subtransforms."""
    N=len(a)
    if N%15:raise ValueError('N divisible by 15 required')
    G=N//15
    if G&(G-1):raise ValueError('N/15 must be dyadic')
    w=n_root(N,p,gen);wG=pow(w,15,p);w15=pow(w,G,p)
    roots,_=table(w,N,p)
    cost=Cost();z=[]
    for u in range(15):
        row=[a[u+15*v] for v in range(G)]
        z.append(fft_dyadic(row,wG,p,cost))
    out=[None]*N
    for q in range(G):
        row=[z[u][q] for u in range(15)]
        for u in range(1,15):
            if q:
                if not drop_twiddle:row[u]=row[u]*roots[u*q]%p
                cost.muls+=1
        yy=dft15(row,w15,p,cost)
        for r in range(15):out[q+G*r]=yy[r]
    return out,cost


def direct_dft(a,p=P,gen=GENERATOR):
    N=len(a);w=n_root(N,p,gen);powers,_=table(w,N,p)
    return [sum(a[j]*powers[(j*k)%N] for j in range(N))%p for k in range(N)]


def closed_cost(g):
    t=g.bit_length()-1
    assert g>0 and (1<<t)==g
    adds=15*g*t +81*g
    muls=15*(g*t//2-g+1) +25*g if g>=2 else 25
    return adds,muls,adds+muls


if __name__=='__main__':
    import random
    for g in [1,2,4,8,16,32,64,128]:
        N=15*g
        if (P-1)%N:continue
        rng=random.Random(N)
        x=[rng.randrange(P) for _ in range(N)]
        a,ca=gt15(x);b,cb=ct15(x)
        assert a==b
        if N<=240:assert a==direct_dft(x)
        assert ca.total()==closed_cost(g)[2]
        assert cb.total()-ca.total()==14*(g-1)
        print(N, ca.adds,ca.muls,ca.total(),cb.total(),round((cb.total()-ca.total())/cb.total()*100,3))
