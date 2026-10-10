"""Budget-adaptive extension of user's Hero #17 fiber-character FFT.
For a promised TOTAL K modes across Q fibers (not max r per fiber),
with Q^2 = O(N), K = O(Q), supports exact O(N) field operations.
Unknown inputs are rejected (None) if certificate budget cannot be met.
No FFT is called in the recognition path; heavy fibers use O(M^2) direct DFT.
"""
from __future__ import annotations
from math import isqrt


def roots(n,p,omega):
    z=[1]*n
    for j in range(1,n):z[j]=z[j-1]*omega%p
    return z


def bm_bounded(y,p,r):
    C=[1]+[0]*r;B=C.copy();L=0;shift=1;inv_last=1
    for k in range(len(y)):
        delta=(y[k]+sum(C[i]*y[k-i] for i in range(1,L+1)))%p
        if not delta:
            shift+=1;continue
        grow=2*L<=k
        proposed=k+1-L if grow else L
        if proposed>r:return None
        old=C.copy()
        fac=delta*inv_last%p
        for i in range(shift,r+1):C[i]=(C[i]-fac*B[i-shift])%p
        if grow:
            L=proposed;B=old;inv_last=pow(delta,-1,p);shift=1
        else:shift+=1
    return C[:L+1]


def poly_value(poly,z,p):
    acc=0
    for c in reversed(poly):acc=(acc*z+c)%p
    return acc


def vandermonde_moments(nodes,y,p):
    """Solve y_j=sum c_l nodes[l]^j, exact O(r^2) field ops."""
    r=len(nodes)
    if not r:return []
    P=[1]
    for z in nodes:
        nxt=[0]*(len(P)+1)
        for i,c in enumerate(P):
            nxt[i]=(nxt[i]-z*c)%p
            nxt[i+1]=(nxt[i+1]+c)%p
        P=nxt
    coeff=[]
    for z in nodes:
        q=[0]*r;q[-1]=1
        for j in range(r-2,-1,-1):q[j]=(P[j+1]+z*q[j+1])%p
        deriv=0
        for j in range(r,0,-1):deriv=(deriv*z+j*P[j])%p
        assert deriv!=0
        coef=sum(q[j]*y[j] for j in range(r))%p
        coeff.append(coef*pow(deriv,-1,p)%p)
    return coeff


def try_light_modes(y,p,rt,budget):
    """Try sparse character recovery in O(M*r+r^2) for actual r<=budget."""
    seq=bm_bounded(y,p,budget)
    if seq is None:return None
    r=len(seq)-1
    if r==0:return () if not any(y) else None
    zlist=[(h,z) for h,z in enumerate(rt) if poly_value(list(reversed(seq)),z,p)==0]
    if len(zlist)!=r:return None
    weights=vandermonde_moments([z for _,z in zlist],y,p)
    if any(c==0 for c in weights):return None
    powers=[1]*r
    for val in y:
        if (sum(c*a for c,a in zip(weights,powers))-val)%p:return None
        for i,(_,z) in enumerate(zlist):powers[i]=powers[i]*z%p
    return tuple((h,c) for (h,_),c in zip(zlist,weights))


def direct_modes(y,p,rt):
    m=len(y); invm=pow(m,-1,p)
    out=[]
    for h in range(m):
        c=sum(v*rt[(-u*h)%m] for u,v in enumerate(y))%p * invm %p
        if c:out.append((h,c))
    return tuple(out)


def recognize_total_budget(x,p,omega,Q,K0):
    N=len(x)
    assert Q>=1 and K0>=0
    if N%Q or pow(omega,N,p)!=1 or (N>1 and len(set(roots(N,p,omega)))!=N):
        raise ValueError('N divides p-1, omega primitive Nth root, Q divides N required')
    M=N//Q
    rt=roots(M,p,pow(omega,Q,p))
    rows=[];remaining=K0
    for t in range(Q):
        y=[x[t+Q*u]%p for u in range(M)]
        if M<=2:
            found=direct_modes(y,p,rt)
        else:
            H=max(1,M//3)
            threshold=min(H,remaining)
            found=try_light_modes(y,p,rt,threshold)
            if found is None:
                # More than H characters is necessarily too expensive if
                # the remaining certificate budget is <= H.
                if remaining<=H:return None
                found=direct_modes(y,p,rt)
        if len(found)>remaining:return None
        remaining-=len(found)
        rows.append(found)
    return tuple(rows)


def transform_modes(rows,p,omega,N):
    Q=len(rows);M=N//Q;rt=roots(N,p,omega)
    out=[0]*N
    for t,modes in enumerate(rows):
        for h,c in modes:
            for s in range(Q):
                k=h+M*s
                out[k]=(out[k]+M*c*rt[(-k*t)%N])%p
    return out


def build_input(rows,p,omega,N):
    Q=len(rows);M=N//Q;rt=roots(M,p,pow(omega,Q,p))
    x=[0]*N
    for t,modes in enumerate(rows):
        for u in range(M):x[t+Q*u]=sum(c*rt[(h*u)%M] for h,c in modes)%p
    return x


def direct_dft(x,p,omega):
    N=len(x);rt=roots(N,p,omega)
    return [sum(v*rt[(-j*k)%N] for j,v in enumerate(x))%p for k in range(N)]
