"""Fresh independent checks. No imported research/source checker is executed.

The packed conversion path uses arrays of w-bit words; unrestricted integers
are used only by slow algebraic reference routines and small field arithmetic.
This is an algebra/boundary control, not a benchmark or formal complexity proof.
"""
import hashlib
import json
import math
import random
from pathlib import Path

RNG = random.Random(202610100215)
COUNTS = {}

def record(key, n=1):
    COUNTS[key] = COUNTS.get(key, 0) + n

class Bits:
    ops = 0
    max_word_bits = 0
    def __init__(self, words, size, w):
        self.w, self.size = w, size
        self.words = list(words)
        assert len(self.words) == (size+w-1)//w
        assert all(0 <= x < 1 << w for x in self.words)
        if self.words and size % w:
            self.words[-1] &= (1 << (size % w))-1
        Bits.max_word_bits = max(Bits.max_word_bits, max((x.bit_length() for x in self.words), default=0))
    @classmethod
    def zero(cls, size, w):
        return cls([0]*((size+w-1)//w), size, w)
    @classmethod
    def reference_pack(cls, vals, h, w):
        # Input construction/reference only. The conversion never calls this.
        x = sum(v << (i*h) for i,v in enumerate(vals))
        return cls([(x >> i) & ((1<<w)-1) for i in range(0,len(vals)*h,w)],len(vals)*h,w)
    def reference_unpack(self, h):
        x = sum(v << (i*self.w) for i,v in enumerate(self.words))
        return [(x >> i)&((1<<h)-1) for i in range(0,self.size,h)]
    def read(self, start, count):
        assert 0 <= count <= self.w and 0 <= start and start+count <= self.size
        if not count:
            return 0
        i,off = divmod(start,self.w)
        out = self.words[i] >> off
        if off+count > self.w:
            out |= (self.words[i+1] << (self.w-off)) & ((1<<self.w)-1)
        Bits.ops += 8
        return out & ((1<<count)-1)
    def slice(self, start, count):
        return Bits([self.read(start+i,min(self.w,count-i)) for i in range(0,count,self.w)],count,self.w)
    def xor(self, other):
        assert self.size == other.size and self.w == other.w
        Bits.ops += len(self.words)
        return Bits([a^b for a,b in zip(self.words,other.words)],self.size,self.w)
    def shifted(self, amount):
        out = Bits.zero(self.size,self.w)
        for dst in range(0,self.size,self.w):
            cnt = min(self.w,self.size-dst)
            src = dst-amount
            lo,hi=max(0,src),min(self.size,src+cnt)
            if hi>lo:
                out.words[dst//self.w] = self.read(lo,hi-lo) << (lo-src)
            Bits.ops += 5
        return out
    @staticmethod
    def join(parts):
        assert parts
        w=parts[0].w
        out=Bits.zero(sum(p.size for p in parts),w)
        start=0
        for part in parts:
            assert part.w==w
            pos=0
            while pos < part.size:
                dst=start+pos
                cnt=min(w-dst%w,part.size-pos)
                out.words[dst//w] |= part.read(pos,cnt) << (dst%w)
                pos+=cnt
                Bits.ops+=5
            start+=part.size
        return out

def y_blocks(a,m,k,h,inverse=False):
    if m==k:
        return a
    H=1<<(m-1)
    R=1<<(m-1-k)
    low=a.slice(0,H*h)
    high=a.slice(H*h,H*h)
    if not inverse:
        q=high.xor(high.shifted(-(H-R)*h))
        rem=low.xor(q.shifted(R*h))
        return Bits.join([y_blocks(rem,m-1,k,h),y_blocks(q,m-1,k,h)])
    rem=y_blocks(low,m-1,k,h,True)
    q=y_blocks(high,m-1,k,h,True)
    high=q.xor(q.shifted(-(H-R)*h))
    low=rem.xor(q.shifted(R*h))
    return Bits.join([low,high])

def convert(a,m,h,inverse=False):
    if m<=1:
        return a.slice(0,a.size)
    k=1<<((m-1).bit_length()-1)
    t=m-k
    D=1<<k
    if not inverse:
        upper=convert(y_blocks(a,m,k,h),t,h*D)
        return Bits.join([convert(upper.slice(i*D*h,D*h),k,h) for i in range(1<<t)])
    lower=Bits.join([convert(a.slice(i*D*h,D*h),k,h,True) for i in range(1<<t)])
    return y_blocks(convert(lower,t,D*h,True),m,k,h,True)

def clmul(a,b):
    out=0
    while b:
        if b&1:
            out^=a
        a<<=1
        b>>=1
    return out

def basis(m):
    ss=[]
    s=2
    for _ in range(m):
        ss.append(s)
        sq=sum(1<<(2*i) for i in range(s.bit_length()) if s>>i&1)
        s=sq^s
    bb=[1]
    for s in ss:
        bb += [clmul(x,s) for x in bb]
    return bb

def reference_from_novel(vals,bb):
    out=[0]*len(vals)
    for v,p in zip(vals,bb):
        while p:
            bit=(p&-p).bit_length()-1
            out[bit]^=v
            p&=p-1
    return out

def field(d,mod):
    def mul(a,b):
        c=clmul(a,b)
        for i in range(c.bit_length()-1,d-1,-1):
            if c>>i&1:
                c^=mod<<(i-d)
        return c
    gens=[]
    tau=1
    for j in range(d.bit_length()-1):
        u=next(x for x in range(1<<d) if mul(x,x)^x==tau)
        gens.append(u)
        tau=mul(tau,u)
    vv=[1]
    for u in gens:
        vv += [mul(x,u) for x in vv]
    encode=[]
    for i in range(1<<d):
        x=0
        for j in range(d):
            if i>>j&1:
                x^=vv[j]
        encode.append(x)
    assert len(set(encode))==1<<d
    decode={x:i for i,x in enumerate(encode)}
    def tmul(a,b):
        return decode[mul(encode[a],encode[b])]
    return tmul

def subpoly(k,a,mul):
    for _ in range(k):
        a=mul(a,a)^a
    return a

def eval_poly(c,a,mul):
    z=0
    for x in reversed(c):
        z=mul(z,a)^x
    return z

def fafft(c,m,l,alpha,mul,events):
    if not m:
        return [(alpha,c[0])]
    H=1<<(m-1)
    tw=subpoly(m-1,alpha,mul)
    p0,p1=c[:H],c[H:]
    q0=[a^mul(tw,b) for a,b in zip(p0,p1)]
    if l and l&(l-1)==0:
        assert (tw>>l)==1
        assert all(x<1<<l for x in c)
        events['pruned']+=1
        return fafft(q0,m-1,l+1,alpha,mul,events)
    q1=[a^b for a,b in zip(q0,p1)]
    return fafft(q0,m-1,l if l==0 else l+1,alpha,mul,events)+fafft(q1,m-1,l+1,alpha^(1<<(m-1)),mul,events)

def inverse(leaves,m,l,alpha,mul,events):
    if not m:
        a,y=next(leaves)
        assert a==alpha
        return [y]
    tw=subpoly(m-1,alpha,mul)
    if l and l&(l-1)==0:
        q=inverse(leaves,m-1,l+1,alpha,mul,events)
        assert tw>>l==1 and all(x<1<<(2*l) for x in q)
        mask=(1<<l)-1
        c=tw^1<<l
        p1=[x>>l for x in q]
        p0=[(x&mask)^mul(c,y) for x,y in zip(q,p1)]
        events['inverse_pruned']+=1
        return p0+p1
    q0=inverse(leaves,m-1,l if l==0 else l+1,alpha,mul,events)
    q1=inverse(leaves,m-1,l+1,alpha^(1<<(m-1)),mul,events)
    p1=[a^b for a,b in zip(q0,q1)]
    return [a^mul(tw,b) for a,b in zip(q0,p1)]+p1

def affine(xs,d):
    beta=xs[0]
    rows=[]
    mus=[]
    labels=[]
    for x in xs:
        z=x^beta
        label=0
        for pivot,idx in rows:
            if z>>pivot&1:
                z^=mus[idx]
                label^=1<<idx
        if z:
            pivot=next(i for i in range(d-1,-1,-1) if z>>i&1)
            idx=len(mus)
            mus.append(z)
            rows.append((pivot,idx))
            rows.sort(reverse=True)
            label^=1<<idx
        labels.append(label)
    for x,label in zip(xs,labels):
        y=beta
        for i,mu in enumerate(mus):
            if label>>i&1:
                y^=mu
        assert x==y
    return beta,mus,labels

def run():
    packed_details=[]
    for m in range(12):
        bb=basis(m)
        for h in [1,3,9,19]:
            for w in [7,17,31]:
                vals=[RNG.randrange(1<<h) for _ in range(1<<m)]
                a=Bits.reference_pack(vals,h,w)
                old=Bits.ops
                cv=convert(a,m,h)
                nv=cv.reference_unpack(h)
                assert reference_from_novel(nv,bb)==vals
                back=convert(cv,m,h,True)
                assert back.words==a.words
                packed_details.append(dict(m=m,h=h,w=w,word_operations=Bits.ops-old,
                    scale=(1<<m)+(1<<m)*h/w*m*math.log2(m+2)))
                record('bounded_word_conversion_roundtrips')
    events={'pruned':0,'inverse_pruned':0}
    fields={d:field(d,p) for d,p in [(1,3),(2,7),(4,19),(8,283)]}
    for d,mul in fields.items():
        for m in range(d+1):
            n=1<<m
            bb=basis(m)
            cases=range(1<<n) if n<=8 else [RNG.getrandbits(n) for _ in range(16)]
            for bits in cases:
                c=[bits>>j&1 for j in range(n)]
                novel=convert(Bits.reference_pack(c,1,13),m,1).reference_unpack(1)
                leaves=fafft(novel,m,0,0,mul,events)
                assert all(y==eval_poly(c,a,mul) for a,y in leaves)
                recovered=inverse(iter(leaves),m,0,0,mul,events)
                assert recovered==novel
                reached=set()
                for a,y in leaves:
                    aa,yy=a,y
                    while aa not in reached:
                        assert aa<n and yy==eval_poly(c,aa,mul)
                        reached.add(aa)
                        aa,yy=mul(aa,aa),mul(yy,yy)
                    assert aa==a
                assert len(reached)==n
                record('pruned_forward_inverse_and_orbits')
        # Different operand lengths include arbitrary non-power-of-two m.
        for _ in range(100):
            L=RNG.randrange(1,(1<<d)+1)
            a=RNG.randrange(1,L+1)
            b=L-a+1
            m=(L-1).bit_length()
            n=1<<m
            aa,bb=RNG.getrandbits(a),RNG.getrandbits(b)
            ca=[aa>>j&1 for j in range(n)]
            cb=[bb>>j&1 for j in range(n)]
            na=convert(Bits.reference_pack(ca,1,11),m,1).reference_unpack(1)
            nb=convert(Bits.reference_pack(cb,1,11),m,1).reference_unpack(1)
            va=fafft(na,m,0,0,mul,events)
            vb=fafft(nb,m,0,0,mul,events)
            vp=[(x,mul(y,z)) for (x,y),(xx,z) in zip(va,vb) if x==xx]
            nc=inverse(iter(vp),m,0,0,mul,events)
            assert all(x in (0,1) for x in nc)
            cc=convert(Bits.reference_pack(nc,1,11),m,1,True).reference_unpack(1)
            assert sum(x<<i for i,x in enumerate(cc))==clmul(aa,bb)
            record('arbitrary_length_mod_two_products')
        N=(1<<d)-1
        def power(a,n):
            z=1
            while n:
                if n&1:
                    z=mul(z,a)
                a=mul(a,a)
                n>>=1
            return z
        root=next(a for a in range(1,1<<d) if len({power(a,j) for j in range(N)})==N)
        for b in range(d+1):
            for _ in range(3):
                beta=RNG.randrange(1<<d)
                mus=RNG.sample(range(1,1<<d),b)
                xs=[]
                for _j in range(N):
                    x=beta
                    for mu in mus:
                        if RNG.randrange(2):
                            x^=mu
                    xs.append(x)
                beta,mu,labels=affine(xs,d)
                accum=[beta]+[0]*(N-1)
                for i,v in enumerate(mu):
                    binary=[labels[j]>>i&1 for j in range(N)]
                    for k in range(N):
                        accum[k]^=mul(v,eval_poly(binary,power(root,k),mul))
                direct=[eval_poly(xs,power(root,k),mul) for k in range(N)]
                assert accum==direct
                record('adaptive_affine_cyclic_transforms')
    # Exhaustive positional field table control in tower coordinates.
    mul=fields[8]
    tt={(i,j,a,b):mul(a<<i,b<<j) for i in range(8) for j in range(8)
        for a in range(2) for b in range(2)}
    for a in range(256):
        for b in range(256):
            z=0
            for i in range(8):
                for j in range(8):
                    z^=tt[i,j,a>>i&1,b>>j&1]
            assert z==mul(a,b)
            record('exhaustive_positional_field_table_products')
    # Explicit table and independent prior-art comparison embedding.
    for h in range(1,5):
        width=2*h
        mask=(1<<width)-1
        table=[clmul(a,b)&mask for a in range(1<<width) for b in range(1<<width)]
        for _ in range(150):
            na,nb=RNG.randrange(1,70),RNG.randrange(1,70)
            a,b=RNG.getrandbits(na),RNG.getrandbits(nb)
            av=[(a>>j)&((1<<h)-1) for j in range(0,na,h)]
            bv=[(b>>j)&((1<<h)-1) for j in range(0,nb,h)]
            c=[0]*(len(av)+len(bv)-1)
            for i,x in enumerate(av):
                for j,y in enumerate(bv):
                    c[i+j]^=table[(x<<width)|y]
            out=0
            for i,x in enumerate(c):
                out^=x<<(i*h)
            assert out==clmul(a,b)
            record('small_ring_blocking_comparison_products')
    # Exact recurrence controls, independent of executable transform arithmetic.
    V=[0,0]
    j=[1.0,1.0]
    for m in range(2,4097):
        k=1<<((m-1).bit_length()-1)
        t=m-k
        V.append(V[k]+V[t]+t)
        e=2.0**(-k)
        j.append(j[k]+e*j[t]+e)
        assert V[m] <= m*math.log2(m)
        assert j[m] <= 5
        record('arbitrary_exponent_recurrence_controls')
    assert clmul(3,3)==5
    result={'status':'PASS','seed':202610100215,'counts':COUNTS,'tree_events':events,
      'word_array_operation_counter':Bits.ops,'largest_word_seen_bits':Bits.max_word_bits,
      'max_measured_conversion_cost_over_ledger_scale':max(p['word_operations']/p['scale'] for p in packed_details),
      'recurrence_max_normalized_constant_cost':max(j),
      'packed_details':packed_details,
      'limits':['Finite checks do not prove the infinite complexity theorem.',
                'Generic Cantor–Kaltofen algorithm is an imported theorem, not implemented here.',
                'Ring-blocking tests verify the embedding and recovery, using schoolbook outer convolution.',
                'Only the packed conversion path is explicitly represented by bounded-word arrays.']}
    out=Path(__file__).with_name('INDEPENDENT_CHECK_RESULTS.json')
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='packed_details'},indent=2))

if __name__=='__main__':
    run()
