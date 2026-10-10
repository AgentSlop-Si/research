"""Hero #17 Phase 9: exact charged rank-t root-exchange CRT bridge.

This is an alternative O(tm) evaluator of ONE balanced N=2m remainder
split when t roots are exchanged between parity cosets. It is NOT a
sub-NlogN Fourier transform for arbitrary fresh inputs.

The finite field F_p must contain an N-th primitive root w, with p odd.
No FFT, numpy, symbolic algebra libraries, or unchecked table accesses.
"""
from __future__ import annotations
from dataclasses import dataclass,asdict
from math import isqrt

@dataclass
class Ledger:
    plan_adds:int=0
    plan_muls:int=0
    plan_invs:int=0
    online_adds:int=0
    online_muls:int=0
    online_invs:int=0
    plan_accesses:int=0
    online_accesses:int=0
    writes:int=0
    def add(self,a,b,p,plan=False):
        if plan:self.plan_adds+=1
        else:self.online_adds+=1
        return (a+b)%p
    def sub(self,a,b,p,plan=False):
        if plan:self.plan_adds+=1
        else:self.online_adds+=1
        return (a-b)%p
    def mul(self,a,b,p,plan=False):
        if plan:self.plan_muls+=1
        else:self.online_muls+=1
        return (a*b)%p
    def inv(self,a,p,plan=True):
        if plan:self.plan_invs+=1
        else:self.online_invs+=1
        if a%p==0:raise ZeroDivisionError()
        return pow(a,-1,p)
    def snapshot(self):return asdict(self)

def _prime(n):
    if n<2:return False
    for d in range(2,isqrt(n)+1):
        if n%d==0:return False
    return True

def fixture(n):
    """Test-only prime/root search, NOT part of online complexity claim."""
    for i in range(1,10000):
        p=i*n+1
        if not _prime(p):continue
        for b in range(2,p):
            w=pow(b,(p-1)//n,p)
            if pow(w,n,p)!=1:continue
            if all(pow(w,n//q,p)!=1 for q in _factor(n)):
                return p,w
    raise ValueError('fixture not found')

def _factor(n):
    out=[];d=2
    while d*d<=n:
        if n%d==0:
            out.append(d)
            while n%d==0:n//=d
        d+=1
    if n>1:out.append(n)
    return out

def gen_roots(n,p,w,L):
    """Return z_j=w^(-j), with ALL N root prep operations charged."""
    # The supplied root is primitive; one modular inverse is charged.
    invw=L.inv(w,p,plan=True)
    roots=[1]
    for j in range(1,n):
        roots.append(L.mul(roots[-1],invw,p,plan=True))
    return roots

def horner(coeff,z,p,L,plan=False):
    v=0
    for a in coeff[::-1]:
        v=L.add(L.mul(v,z,p,plan),a,p,plan)
    return v

def divide_by_linear(poly,root,p,L):
    """Exact synthetic division by z-root, O(degree) charged prep work."""
    d=len(poly)-1
    assert d>=1
    q=[0]*d
    q[-1]=poly[-1]
    for j in range(d-1,0,-1):
        q[j-1]=L.add(poly[j],L.mul(root,q[j],p,True),p,True)
    rem=L.add(poly[0],L.mul(root,q[0],p,True),p,True)
    assert rem==0,(poly,root,rem)
    return q

def multiply_by_linear(poly,root,p,L):
    q=[0]*(len(poly)+1)
    for i,a in enumerate(poly):
        q[i]=L.sub(q[i],L.mul(root,a,p,True),p,True)
        q[i+1]=L.add(q[i+1],a,p,True)
    return q

def cardinal_polynomials(natural_removed,newcomers,m,sign,p,L):
    """Build cardinal coefficient polynomials for a t-root-replaced coset.

    sign=+1: original z^m-1, removed even roots, added odd roots.
    sign=-1: original z^m+1, removed odd roots, added even roots.
    """
    assert len(natural_removed)==len(newcomers)
    poly=[0]*(m+1);poly[-1]=1;poly[0]=(-sign)%p
    for removed in natural_removed:
        poly=divide_by_linear(poly,removed,p,L)
    for new in newcomers:
        poly=multiply_by_linear(poly,new,p,L)
    assert len(poly)==m+1 and poly[-1]==1
    cards=[];derivatives=[]
    for new in newcomers:
        q=divide_by_linear(poly,new,p,L)
        denom=horner(q,new,p,L,plan=True)
        assert denom
        inv=L.inv(denom,p,plan=True)
        cards.append([L.mul(a,inv,p,True) for a in q])
        derivatives.append(denom)
    return poly,cards,derivatives

def mat_inverse(A,p,L):
    """Prepared exact field elimination on small t-by-t matrix; cost charged."""
    n=len(A)
    if not n:return []
    W=[[int(v)%p for v in row]+[int(i==j) for j in range(n)] for i,row in enumerate(A)]
    for j in range(n):
        pivot=next((k for k in range(j,n) if W[k][j]!=0),None)
        if pivot is None:raise ValueError('singular cross-node interpolation')
        W[j],W[pivot]=W[pivot],W[j]
        inv=L.inv(W[j][j],p,True)
        for k in range(2*n):W[j][k]=L.mul(W[j][k],inv,p,True)
        for i in range(n):
            if i==j:continue
            x=W[i][j]
            if not x:continue
            for k in range(2*n):
                W[i][k]=L.sub(W[i][k],L.mul(x,W[j][k],p,True),p,True)
    return [row[n:] for row in W]

def matvec(M,v,p,L):
    out=[]
    for row in M:
        y=0
        for a,b in zip(row,v):y=L.add(y,L.mul(a,b,p),p)
        out.append(y)
    return out

class ExchangeBridge:
    """A,B are parity-coset Fourier roots with t distinct exchanges.

    Construct plan once; root prep, cardinal vectors, Cauchy cross matrices,
    and inverses are ALL charged. The same plan works on fresh arbitrary input.
    """
    def __init__(self,n,p,w,removed_even,added_odd):
        assert n%2==0 and n>=2
        m=n//2
        self.n=n;self.m=m;self.p=p;self.w=w
        self.L=Ledger()
        roots=gen_roots(n,p,w,self.L)
        ev=[roots[j] for j in range(0,n,2)]
        od=[roots[j] for j in range(1,n,2)]
        rem_even=[roots[j] for j in removed_even]
        add_odd=[roots[j] for j in added_odd]
        assert len(rem_even)==len(add_odd)
        assert len(set(removed_even))==len(removed_even)
        assert len(set(added_odd))==len(added_odd)
        assert all(j%2==0 and 0<=j<n for j in removed_even)
        assert all(j%2==1 and 0<=j<n for j in added_odd)
        self.t=len(rem_even);self.e=rem_even;self.o=add_odd
        self.A=tuple(sorted((set(range(0,n,2))-set(removed_even))|set(added_odd)))
        self.B=tuple(sorted(set(range(n))-set(self.A)))
        self.PA,self.LA,self.PAprime=cardinal_polynomials(rem_even,add_odd,m,+1,p,self.L)
        self.PB,self.LB,self.PBprime=cardinal_polynomials(add_odd,rem_even,m,-1,p,self.L)
        # Cross-node Cauchy matrices. C_{i,j}= ell_B,e_j(o_i)
        # D_{j,i}= ell_A,o_i(e_j).
        pa_on_e=[horner(self.PA,x,p,self.L,True) for x in rem_even]
        pb_on_o=[horner(self.PB,x,p,self.L,True) for x in add_odd]
        C=[]
        for i,o in enumerate(add_odd):
            row=[]
            for j,e in enumerate(rem_even):
                den=self.L.mul(self.L.sub(o,e,p,True),self.PBprime[j],p,True)
                row.append(self.L.mul(pb_on_o[i],self.L.inv(den,p,True),p,True))
            C.append(row)
        D=[]
        for j,e in enumerate(rem_even):
            row=[]
            for i,o in enumerate(add_odd):
                den=self.L.mul(self.L.sub(e,o,p,True),self.PAprime[i],p,True)
                row.append(self.L.mul(pa_on_e[j],self.L.inv(den,p,True),p,True))
            D.append(row)
        self.C=C;self.D=D
        self.Cinv=mat_inverse(C,p,self.L)
        self.Dinv=mat_inverse(D,p,self.L)
        # Half scalar for inverse CRT bridge. Explicitly charged.
        self.inv2=self.L.inv(2,p,True)
        self.plan_ledger=self.L.snapshot()
        # Every future call has independent online counters.
        self.L=Ledger()

    def pair(self,low,high):
        """Fully charged O(m t+m) simultaneous two-child remainders."""
        m=self.m;p=self.p;L=self.L
        assert len(low)==len(high)==m
        A=[L.add(a,b,p) for a,b in zip(low,high)]
        B=[L.sub(a,b,p) for a,b in zip(low,high)]
        # These t-vector corrections share evaluations across ALL output rows.
        for z,card in zip(self.o,self.LA):
            h=horner(high,z,p,L)
            minus2h=L.sub(0,L.add(h,h,p),p)
            for k in range(m):A[k]=L.add(A[k],L.mul(minus2h,card[k],p),p)
        for z,card in zip(self.e,self.LB):
            h=horner(high,z,p,L)
            plus2h=L.add(h,h,p)
            for k in range(m):B[k]=L.add(B[k],L.mul(plus2h,card[k],p),p)
        L.writes+=2*m
        return A,B

    def invert_pair(self,A,B):
        """Woodbury/Cauchy CRT inverse with two t×t precomputed solves.

        Invert (A-B)/2 = (I-U V) high. In the cross-node basis,
        I-VU = [[0,-C],[-D,0]], so solve C and D separately.
        """
        assert len(A)==len(B)==self.m
        m=self.m;p=self.p;L=self.L
        y=[L.mul(L.sub(a,b,p),self.inv2,p) for a,b in zip(A,B)]
        yo=[horner(y,z,p,L) for z in self.o]
        ye=[horner(y,z,p,L) for z in self.e]
        # z_o = -D^{-1} ye, z_e = -C^{-1} yo.
        zo=[L.sub(0,v,p) for v in matvec(self.Dinv,ye,p,L)]
        ze=[L.sub(0,v,p) for v in matvec(self.Cinv,yo,p,L)]
        H=y.copy()
        for val,card in list(zip(zo,self.LA))+list(zip(ze,self.LB)):
            for i in range(m):H[i]=L.add(H[i],L.mul(val,card[i],p),p)
        # A = low+high -2 sum high(o) ell_A,o
        low=[L.sub(a,h,p) for a,h in zip(A,H)]
        for val,card in zip(zo,self.LA):
            factor=L.add(val,val,p)
            for i in range(m):low[i]=L.add(low[i],L.mul(factor,card[i],p),p)
        L.writes+=2*m
        return low,H

    def online_ledger(self):return self.L.snapshot()


def direct_remainder(poly,root_set,p):
    """Independent reference using monic polynomial division, O(m²)."""
    P=[1]
    for z in root_set:
        Q=[0]*(len(P)+1)
        for i,a in enumerate(P):
            Q[i]=(Q[i]-z*a)%p
            Q[i+1]=(Q[i+1]+a)%p
        P=Q
    m=len(root_set);out=poly.copy()
    for k in range(len(poly)-1,m-1,-1):
        c=out[k]
        for j in range(m):out[k-m+j]=(out[k-m+j]-c*P[j])%p
        out[k]=0
    return out[:m]


def verify_split(bridge,x):
    p=bridge.p;m=bridge.m;z=gen_roots(bridge.n,p,bridge.w,Ledger())
    a,b=bridge.pair(x[:m],x[m:])
    expect_a=direct_remainder(x,[z[j] for j in bridge.A],p)
    expect_b=direct_remainder(x,[z[j] for j in bridge.B],p)
    assert a==expect_a and b==expect_b
    lo,hi=bridge.invert_pair(a,b)
    assert lo+hi==[q%p for q in x]
    return True


def rank(M,p):
    if not M:return 0
    w=[row.copy() for row in M];m=len(w);n=len(w[0]);r=0
    for k in range(n):
        pivot=next((i for i in range(r,m) if w[i][k]),None)
        if pivot is None:continue
        w[r],w[pivot]=w[pivot],w[r]
        inv=pow(w[r][k],-1,p)
        for i in range(r+1,m):
            f=w[i][k]*inv%p
            if f:
                for j in range(k,n):w[i][j]=(w[i][j]-f*w[r][j])%p
        r+=1
        if r==m:break
    return r

def correction_rank_certificate(bridge):
    m=bridge.m;p=bridge.p;t=bridge.t
    # Matrix: stacked delta_A = -2 sum ell_A(z_o)eval(z_o) ;
    #         delta_B = +2 sum ell_B(z_e)eval(z_e)
    da=[[0]*m for _ in range(m)]
    db=[[0]*m for _ in range(m)]
    for k in range(m):
        for j in range(t):
            for i in range(m):
                da[i][k]=(da[i][k]-2*bridge.LA[j][i]*pow(bridge.o[j],k,p))%p
                db[i][k]=(db[i][k]+2*bridge.LB[j][i]*pow(bridge.e[j],k,p))%p
    assert rank(da,p)==t
    assert rank(db,p)==t
    assert rank(da+db,p)==min(m,2*t)
    return {'n':2*m,'t':t,'rank_delta_A':t,'rank_delta_B':t,'joint_rank':min(m,2*t)}

class AdaptiveExchangeBridge:
    """Orient the two children to the nearer parity coset automatically.

    The worst-case t_eff is floor(m/2), with the same full arithmetic charge
    as ExchangeBridge. Output labels are ALWAYS in user-requested A,B order.
    """
    def __init__(self,n,p,w,A):
        if n%2:raise ValueError('even length required')
        self.n=n;self.m=n//2
        A=set(A)
        if len(A)!=self.m or any(j<0 or j>=n for j in A):
            raise ValueError('A must have exactly N/2 distinct root labels')
        B=set(range(n))-A
        E=set(range(0,n,2));O=set(range(1,n,2))
        t=len(A&O)
        self.swapped=t>self.m-t
        chosen=B if self.swapped else A
        self.effective_swaps=min(t,self.m-t)
        self.bridge=ExchangeBridge(n,p,w,sorted(E-chosen),sorted(O&chosen))
        assert set(self.bridge.A)==chosen
        self.A=tuple(sorted(A));self.B=tuple(sorted(B))
    def pair(self,low,high):
        a,b=self.bridge.pair(low,high)
        return (b,a) if self.swapped else (a,b)
    def invert_pair(self,A,B):
        return self.bridge.invert_pair(B,A) if self.swapped else self.bridge.invert_pair(A,B)
    @property
    def plan_ledger(self):return self.bridge.plan_ledger
    def online_ledger(self):return self.bridge.online_ledger()


def single_swap_closed_form(n,p,w,even_label,odd_label,low,high):
    """Independent explicit t=1 correction via geometric quotient powers."""
    assert even_label%2==0 and odd_label%2==1
    m=n//2
    e=pow(w,(-even_label)%n,p)
    o=pow(w,(-odd_label)%n,p)
    def ev(v,z):
        acc=0
        for a in reversed(v):acc=(acc*z+a)%p
        return acc
    he=ev(high,e);ho=ev(high,o)
    A=[];B=[]
    for i in range(m):
        qe=pow(e,m-1-i,p)
        qo=pow(o,m-1-i,p)
        A.append((low[i]+high[i]+(o-e)*ho*qe)%p)
        B.append((low[i]-high[i]+(e-o)*he*qo)%p)
    return A,B

def full_dft_via_explicit_children(x,bridge):
    """Honest arbitrary-input end-to-end executor, intentionally O(N²).

    The split itself is O(tN), but evaluating both degree-(N/2-1)
    remainder polynomials at all N roots is O(N²). Every operation is
    recorded, including root preparation and output writes.
    """
    n=bridge.n;p=bridge.p;L=bridge.L
    roots=[1]
    invw=L.inv(bridge.w,p,plan=False)
    for i in range(1,n):roots.append(L.mul(roots[-1],invw,p,plan=False))
    a,b=bridge.pair(x[:n//2],x[n//2:])
    out=[None]*n
    for idx in bridge.A:
        out[idx]=horner(a,roots[idx],p,L)
        L.writes+=1
    for idx in bridge.B:
        out[idx]=horner(b,roots[idx],p,L)
        L.writes+=1
    return out


def classical_dif_fft(x,p,w):
    """Independent classical radix-2 reference with charged scalar work."""
    n=len(x)
    assert n>=2 and n&(n-1)==0
    L=Ledger();roots=gen_roots(n,p,w,L)
    out=[None]*n
    def rec(poly,indices):
        length=len(indices)
        if length==1:
            out[indices[0]]=poly[0]
            L.writes+=1
            return
        h=length//2
        first=indices[::2]
        second=indices[1::2]
        c=roots[first[0]*h %n]
        a=[];b=[]
        for i in range(h):
            tw=L.mul(c,poly[i+h],p)
            a.append(L.add(poly[i],tw,p))
            b.append(L.sub(poly[i],tw,p))
        rec(a,first);rec(b,second)
    rec(x,list(range(n)))
    return out,L

def full_dft_via_hybrid_children(x,bridge):
    """FULL exact N-point DFT via an exotic split plus two classical m-FFTs.

    Charged O(N log N+tN), and therefore NOT a sub-NlogN improvement.
    Demonstrates that even a dense child transfer can be executed with
    sparse root-exchange correction, followed by ordinary Fourier stages.
    """
    n=bridge.n
    assert n>=4 and n&(n-1)==0
    m=n//2;p=bridge.p;w=bridge.w;L=bridge.L
    roots=[1]
    winv=L.inv(w,p,plan=False)
    for j in range(1,n):roots.append(L.mul(roots[-1],winv,p))
    a,b=bridge.pair(x[:m],x[m:])
    wsub=L.mul(w,w,p)
    # All E roots form the group of m-th roots, so evaluate a via m-FFT.
    fa,Lfa=classical_dif_fft(a,p,wsub)
    # Odd roots are the m roots w^-1*w^(-2s), twist before second m-FFT.
    twisted=[];tw=1
    for val in b:
        twisted.append(L.mul(tw,val,p))
        tw=L.mul(tw,winv,p)
    fb,Lfb=classical_dif_fft(twisted,p,wsub)
    out=[None]*n
    groupA=set(bridge.A)
    for k in range(n):
        if k in groupA:
            out[k]=fa[k//2] if k%2==0 else horner(a,roots[k],p,L)
        else:
            out[k]=fb[(k-1)//2] if k%2 else horner(b,roots[k],p,L)
        L.writes+=1
    ledgers={'outer_plan':bridge.plan_ledger,'outer_online':bridge.online_ledger(),
             'left_fft':Lfa.snapshot(),'right_fft':Lfb.snapshot()}
    return out,ledgers


def combined_scalar_cost(records):
    """All scalar additions/multiplications, including all charged plans."""
    fields=('online_adds','online_muls','plan_adds','plan_muls')
    return sum(sum(record.get(k,0) for k in fields) for record in records.values())
