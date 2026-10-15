"""Fresh finite precision-adaptive Newton/NTT/CRT producer.

The producer's data products use explicit binary shift/add; reductions/divisions
use explicit binary long division. No Python big-integer data-product oracle
is used in this producer.
Parameter/index arithmetic and storage use Python integers. This is a
correctness/operation-ledger implementation, not a fast Python backend.
"""
from collections import Counter


class Arithmetic:
    def __init__(self):
        self.counts = Counter()
        self.native_children = Counter()

    def mul(self, a, b, tag='integer_product'):
        self.counts[tag] += 1
        if a and b:
            self.native_children[abs(a).bit_length()+abs(b).bit_length()] += 1
        self.counts['product_operand_bits'] += abs(a).bit_length()+abs(b).bit_length()
        sign = -1 if (a < 0) != (b < 0) else 1
        a, b = abs(a), abs(b)
        # Scan the shorter multiplier: O(u*v), not O(v*(u+v)).
        if a.bit_length() < b.bit_length():
            a, b = b, a
        z = 0
        while b:
            if b & 1:
                self.counts['shiftadd_addition_bits'] += max(z.bit_length(), a.bit_length())+1
                z += a
            a <<= 1
            b >>= 1
        return -z if sign < 0 else z

    def divmod(self, a, b):
        """Euclidean division with linear bit extraction/quotient packing.

        A w-bit remainder is updated once per dividend bit. Quotient bits are
        accumulated in a list and packed once; no growing integer is shifted.
        """
        assert b > 0
        negative = a < 0
        a = abs(a)
        if a < b:
            return ((-1, b-a) if negative and a else (0, a))
        n = a.bit_length()
        raw = a.to_bytes((n+7)//8, 'big')
        allbits = [(byte >> shift) & 1 for byte in raw for shift in range(7,-1,-1)]
        bits = allbits[len(allbits)-n:]
        quotient = []
        z = 0
        for bit in bits:
            z = (z << 1) | bit
            qb = int(z >= b)
            if qb:
                z -= b
            quotient.append(qb)
            self.counts['longdivision_steps'] += 1
            self.counts['longdivision_comparison_bits'] += b.bit_length()+1
        padded = [0]*((-len(quotient))%8)+quotient
        packed = bytearray()
        for i in range(0,len(padded),8):
            byte = 0
            for bit in padded[i:i+8]:
                byte = (byte << 1) | bit
            packed.append(byte)
        q = int.from_bytes(packed, 'big')
        self.counts['division_linear_bit_movement'] += 3*n
        if negative:
            return (-q-1, b-z) if z else (-q, 0)
        return q, z

    def mod(self, a, m):
        return self.divmod(a, m)[1]

    def low(self, a, k):
        self.counts['binary_reduction_bits'] += abs(a).bit_length()+k
        return a & ((1 << k)-1)

    def mm(self, a, b, m, tag='modular_product'):
        return self.mod(self.mul(a,b,tag),m)

    def pow(self, a, e, m, tag='setup_product'):
        a = self.mod(a,m)
        z = 1
        while e:
            if e & 1:
                z = self.mm(z,a,m,tag)
            e >>= 1
            if e:
                a = self.mm(a,a,m,tag)
        return z

    def addmod(self,a,b,q):
        self.counts['field_additions'] += 1
        z=a+b
        return z-q if z >= q else z

    def submod(self,a,b,q):
        self.counts['field_additions'] += 1
        z=a-b
        return z+q if z < 0 else z


def pow2ceil(n):
    return 1 << max(0,(n-1).bit_length())


def trial_prime(q, ar):
    if q < 2: return False
    d=2
    while ar.mul(d,d,'prime_certificate_product') <= q:
        if ar.mod(q,d)==0: return False
        d+=1
    return True


def next_prime_root(L,g,c,ar):
    """Exhaustive certified q=cL+1 search; every tested candidate is paid."""
    while True:
        q=(c << (L.bit_length()-1))+1
        c+=1
        ar.counts['prime_candidates']+=1
        if not trial_prime(q,ar) or ar.mod(g,q)==0:
            continue
        # L is a power of two. omega^(L/2)=-1 proves exact order L.
        a=2
        while True:
            omega=ar.pow(a,(q-1)//L,q)
            if ar.pow(omega,L//2,q)==q-1 and ar.pow(omega,L,q)==1:
                return q,omega,c
            a+=1


class NTT:
    def __init__(self,q,L,omega,ar):
        self.q,self.L,self.omega,self.ar=q,L,omega,ar
        self.tables={}

    def transform(self,data,n,inverse=False,tag='online'):
        assert n <= self.L and self.L % n==0
        ar,q=self.ar,self.q
        key=(n,inverse)
        if key not in self.tables:
            root=ar.pow(self.omega,self.L//n,q)
            if inverse: root=ar.pow(root,q-2,q)
            tab=[1]
            for _ in range(1,n//2): tab.append(ar.mm(tab[-1],root,q,'twiddle_setup_product'))
            ni=ar.pow(n,q-2,q) if inverse else None
            self.tables[key]=(tab,ni)
        tab,ni=self.tables[key]
        a=list(data)+[0]*(n-len(data))
        j=0
        for i in range(1,n):
            bit=n>>1
            while j & bit: j^=bit; bit>>=1
            j^=bit
            if i<j: a[i],a[j]=a[j],a[i]
        length=2
        while length <= n:
            half=length>>1
            step=n//length
            for start in range(0,n,length):
                for j in range(half):
                    u=a[start+j]
                    v=ar.mm(a[start+j+half],tab[j*step],q,tag+'_twiddle_product')
                    a[start+j]=ar.addmod(u,v,q)
                    a[start+j+half]=ar.submod(u,v,q)
                    ar.counts[tag+'_butterflies']+=1
            length<<=1
        if inverse:
            a=[ar.mm(x,ni,q,tag+'_normalization_product') for x in a]
        ar.counts['transform_cells_moved']+=n
        return a

    def kernel(self,k,n):
        return self.transform(k,n,False,'kernel_setup')

    def convolution(self,a,kernel,n):
        x=self.transform(a,n)
        x=[self.ar.mm(u,v,self.q,'fixed_kernel_product') for u,v in zip(x,kernel)]
        return self.transform(x,n,True)


def sample_interpolate(a,b,g,ell,q,L,omega,active,ar):
    """Recovered Newton factorial convolutions, only needed sample prefix."""
    r=len(a)
    assert len(b)==r and q>ell-1 and ar.mod(g,q)
    nE=pow2ceil(min(r,ell)+ell-1)
    nI=pow2ceil(2*ell-1)
    ctx=NTT(q,L,omega,ar)
    fact=[1]
    for j in range(1,ell):fact.append(ar.mm(fact[-1],j,q,'factorial_setup_product'))
    invfact=[0]*ell
    invfact[-1]=ar.pow(fact[-1],q-2,q)
    for j in range(ell-1,0,-1):invfact[j-1]=ar.mm(invfact[j],j,q,'factorial_setup_product')
    ng=ar.mod(-g,q)
    ngi=ar.pow(ng,q-2,q)
    gp=[1]; gip=[1]
    for j in range(1,ell):
        gp.append(ar.mm(gp[-1],ng,q,'power_setup_product'))
        gip.append(ar.mm(gip[-1],ngi,q,'power_setup_product'))
    ke=ctx.kernel(invfact,nE)
    ki=ctx.kernel([x if not j&1 else (q-x if x else 0) for j,x in enumerate(invfact)],nI)
    aa=[ar.mm(ar.mod(x,q),gp[j],q,'input_scaling_product') for j,x in enumerate(a[:ell])]
    bb=[ar.mm(ar.mod(x,q),gp[j],q,'input_scaling_product') for j,x in enumerate(b[:ell])]
    ua=ctx.convolution(aa,ke,nE)[:ell]
    ub=ctx.convolution(bb,ke,nE)[:ell]
    w=[]
    for j in range(ell):
        vb=ar.mm(ub[j],fact[j],q,'factorial_weight_product')
        w.append(ar.mm(ua[j],vb,q,'data_product'))
    dd=ctx.convolution(w,ki,nI)[:ell]
    out={j:ar.mm(dd[j],gip[j],q,'output_unscaling_product') for j in active}
    return out,dict(samples=ell,nE=nE,nI=nI,
                    online_butterflies=2*nE*(nE.bit_length()-1)+nI*(nI.bit_length()-1),
                    kernel_butterflies=(nE*(nE.bit_length()-1)+nI*(nI.bit_length()-1))//2)


def digitize(x,p,g,r,ar):
    out=[]
    radix=p
    for _ in range(r):
        x,d=ar.divmod(x,radix)
        out.append(d)
        radix+=g
    if x:raise ValueError('Input does not fit the declared one-block radices')
    return out


def channel_bounds(a,b,g,ar):
    r=len(a)
    B=max(max(a,default=0),max(b,default=0),1)
    bits=B.bit_length()
    shape=1+ar.mul(g,ar.mul(r-1,r-1,'bound_product'),'bound_product')
    c=(shape-1).bit_length()
    base=2*bits+(r-1).bit_length()
    return [base+ar.mul(min(j,2*r-2-j),c,'bound_product') for j in range(2*r-1)]


def adaptive_low(x,y,p,g,r,k):
    assert x>=0 and y>=0 and p>=2 and g>0 and r>=2 and k>=1
    ar=Arithmetic()
    a=digitize(x,p,g,r,ar); b=digitize(y,p,g,r,ar)
    h=channel_bounds(a,b,g,ar)
    d=2*r-1; L=pow2ceil(2*d-1)
    P=1; residues=[0]*d; D=[None]*d; stopped=[None]*d
    rounds=[]; c=1
    while any(v is None for v in D):
        active=[j for j in range(d) if D[j] is None]
        ell=max(active)+1
        q,omega,c=next_prime_root(L,g,c,ar)
        before=ar.counts.copy()
        out,row=sample_interpolate(a,b,g,ell,q,L,omega,active,ar)
        assert ar.counts['online_butterflies']-before['online_butterflies']==row['online_butterflies']
        assert ar.counts['kernel_setup_butterflies']-before['kernel_setup_butterflies']==row['kernel_butterflies']
        pm=ar.mod(P,q); inv=ar.pow(pm,q-2,q)
        newP=ar.mul(P,q,'crt_modulus_product')
        for j in active:
            delta=ar.mod(out[j]-ar.mod(residues[j],q),q)
            z=ar.mm(delta,inv,q,'crt_digit_product')
            residues[j]+=ar.mul(P,z,'crt_lift_product')
            if newP > (1 << (h[j]+1)):
                D[j]=residues[j]-newP if residues[j] > newP//2 else residues[j]
                stopped[j]=newP.bit_length()
                assert abs(D[j]) < (1<<h[j])
        row.update(q=q,root=omega,width=q.bit_length(),active=list(active),
                   prefix_modulus_bits=newP.bit_length())
        rounds.append(row); P=newP
    # Modular scalar Newton-Horner: all binary reductions are explicit and paid.
    modulus=1<<k
    z=0
    for j in range(d-1,-1,-1):
        radix=p+ar.mul(g,j,'radix_product')
        z=ar.low(ar.mul(radix,z,'scalar_horner_product')+D[j],k)
    return z,dict(coefficients=D,bounds=h,stopped_modulus_bits=stopped,
                  rounds=rounds,counts=dict(ar.counts),
                  native_wrapper_capacities=dict(sorted(ar.native_children.items())),input_digits=[a,b],
                  final_global_modulus_bits=P.bit_length(),k=k,L=L)


def v2(x):
    assert x
    x=abs(x)
    return (x & -x).bit_length()-1


def factorial_v2(n):
    return n-n.bit_count()


def odd_inverse(u,K,ar):
    """Paid Newton inverse, doubling the valid binary precision."""
    assert u&1 and K>=1
    x=1; t=1
    while t<K:
        t=min(2*t,K); m=1<<t
        x=ar.mod(ar.mul(x,2-ar.mul(u,x,'inverse_product'),'inverse_product'),m)
    assert ar.mod(ar.mul(u,x,'inverse_check_product'),1<<K)==1
    return x


def even_guarded_low(a,b,p,g,k):
    """Even-step scalar complement: no exact Newton coefficients or odd CRT."""
    assert p&1 and not g&1 and g>0 and len(a)==len(b) and k>=1
    r=len(a); s=2*r-2; d=s+1; ag=v2(g)
    Lam=ag*s+factorial_v2(s)
    ar=Arithmetic(); total=0; rows=[]
    for t in range(d):
        lam=ag*s+factorial_v2(t)+factorial_v2(s-t)
        K=k+lam; modulus=1<<K
        node=-ar.mul(g,t,'node_product')
        vals=[]
        for aa in (a,b):
            z=0
            for j in range(r-1,-1,-1):
                factor=node+ar.mul(g,j,'sample_constant_product')
                z=ar.mod(ar.mul(factor,z,'sample_horner_product')+aa[j],modulus)
            vals.append(z)
        f=ar.mm(vals[0],vals[1],modulus,'data_product')
        num=1
        for u in range(d):
            if u!=t:num=ar.mm(num,p+ar.mul(g,u,'weight_parameter_product'),modulus,'weight_product')
        den=ar.pow(g>>ag,s,modulus,'weight_product')
        for n in (t,s-t):
            for v in range(1,n+1):
                den=ar.mm(den,v>>v2(v),modulus,'weight_product')
        inv=odd_inverse(den,K,ar)
        term=ar.mm(ar.mm(f,num,modulus,'functional_product'),inv,modulus,'functional_product')
        if t&1:term=-term
        total+=term << (Lam-lam)
        rows.append(dict(sample=t,precision=K,denominator_valuation=lam))
    total=ar.mod(total,1<<(k+Lam))
    assert total % (1<<Lam)==0
    return total>>Lam,dict(Lambda=Lam,rows=rows,counts=dict(ar.counts))
