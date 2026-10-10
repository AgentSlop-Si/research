"""Fresh literal bounded-word-array conversion checks, not uploaded code."""
import random,json
class Bits:
    work=0
    def __init__(self,words,n,w):
        self.a=words;self.n=n;self.w=w
        self.mask=(1<<w)-1
        assert len(words)==(n+w-1)//w
        assert all(0<=a<=self.mask for a in words)
    @classmethod
    def fromint(cls,x,n,w):return cls([(x>>i)&((1<<w)-1) for i in range(0,n,w)],n,w)
    def asint(self):return sum(x<<(self.w*i) for i,x in enumerate(self.a))
    def cut(self,start,n):
        out=[];w=self.w
        for p in range(start,start+n,w):
            j,r=divmod(p,w);z=(self.a[j]>>r) if j<len(self.a) else 0
            if r and j+1<len(self.a):z|=(self.a[j+1]<<(w-r))&self.mask
            out.append(z);Bits.work+=4
        if n%w:out[-1]&=(1<<(n%w))-1
        return Bits(out,n,w)
    def put(self,start,b):
        # Each b word enters at most two output words, masking each output.
        w=self.w
        for i,z in enumerate(b.a):
            length=min(w,b.n-i*w);j,r=divmod(start+i*w,w)
            lo=min(length,w-r);lm=((1<<lo)-1)<<r
            self.a[j]=(self.a[j]&~lm)|((z<<r)&lm)
            if lo<length:
                hm=(1<<(length-lo))-1
                self.a[j+1]=(self.a[j+1]&~hm)|((z>>lo)&hm)
            Bits.work+=8
    def xor(self,b):
        Bits.work+=len(self.a)
        return Bits([a^c for a,c in zip(self.a,b.a)],self.n,self.w)
    def right(self,k):
        z=Bits([0]*len(self.a),self.n,self.w)
        if k<self.n:z.put(0,self.cut(k,self.n-k))
        return z
    def left(self,k):
        z=Bits([0]*len(self.a),self.n,self.w)
        if k<self.n:z.put(k,self.cut(0,self.n-k))
        return z

def to_y(f,m,k,h):
    if m==k:return f
    H=1<<(m-1);R=1<<(m-1-k)
    low=f.cut(0,H*h);high=f.cut(H*h,H*h)
    q=high.xor(high.right((H-R)*h));rem=low.xor(q.left(R*h))
    out=Bits([0]*len(f.a),f.n,f.w)
    out.put(0,to_y(rem,m-1,k,h));out.put(H*h,to_y(q,m-1,k,h))
    return out

def convert(f,m,h=1):
    if m<=1:return f
    k=1<<((m-1).bit_length()-1);D=1<<k
    upper=convert(to_y(f,m,k,h),m-k,h*D)
    out=Bits([0]*len(f.a),f.n,f.w)
    for i in range(1<<(m-k)):
        z=convert(upper.cut(i*h*D,h*D),k,h);out.put(i*h*D,z)
    return out

def polymul(a,b):
    z=0
    while b:
        if b&1:z^=a
        a<<=1;b>>=1
    return z

def basis_polys(m):
    s=[2]
    for i in range(m-1):
        p=s[-1];square=sum(1<<(2*j) for j in range(p.bit_length()) if p>>j&1);s.append(p^square)
    z=[]
    for j in range(1<<m):
        p=1
        for i in range(m):
            if j>>i&1:p=polymul(p,s[i])
        z.append(p)
    return z

def reference(a,m,h):
    out=0;basis=basis_polys(m)
    for lane in range(h):
        f=sum(((a>>(h*j+lane))&1)<<j for j in range(1<<m));v=0
        for j in range((1<<m)-1,-1,-1):
            if f>>j&1:f^=basis[j];v|=1<<j
        assert f==0
        out|=sum(((v>>j)&1)<<(h*j+lane) for j in range(1<<m))
    return out
rng=random.Random(58152);cases=0
for w in [3,7,13,32]:
 for m in [2,3,4,5,6,7,8]:
  for h in [1,3,9]:
   for _ in range(3):
    n=(1<<m)*h;a=rng.getrandbits(n)
    assert convert(Bits.fromint(a,n,w),m,h).asint()==reference(a,m,h);cases+=1
stats=[]
for m in [2,4,8,16]:
    Q=1<<m;w=max(4,m);a=rng.getrandbits(Q);Bits.work=0
    out=convert(Bits.fromint(a,Q,w),m)
    stats.append(dict(m=m,n=Q,w=w,instrumented_word_boundaries=Bits.work,work_over_n_log2m=Bits.work/(Q*m.bit_length()-Q)))
print(json.dumps(dict(exact_word_array_cases=cases,scaling=stats),indent=2))
