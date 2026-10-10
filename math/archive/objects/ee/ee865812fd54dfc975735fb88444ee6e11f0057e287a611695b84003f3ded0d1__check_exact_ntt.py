"""Independently authored checks. No imported research code.
Python integer packing checks algebra, NOT unit-time operations on huge integers.
"""
from functools import lru_cache
import itertools, random, json, math

@lru_cache(None)
def mul(a,b,d):
    if d == 1: return a & b
    h=d//2; mask=(1<<h)-1
    a0,a1=a&mask,a>>h; b0,b1=b&mask,b>>h
    t=mul(a1,b1,h)
    lo=mul(a0,b0,h)^mul(t,1<<(h-1),h)
    hi=mul(a0,b1,h)^mul(a1,b0,h)^t
    return lo^(hi<<h)

def power(a,n,d):
    z=1
    while n:
        if n&1:z=mul(z,a,d)
        a=mul(a,a,d);n//=2
    return z

def s_eval(i,a,d):
    for _ in range(i):a=mul(a,a,d)^a
    return a

@lru_cache(None)
def s_poly(i):
    if i==0:return 2
    f=s_poly(i-1); z=f
    for j in range(f.bit_length()):
        if f>>j&1:z^=1<<(2*j)
    return z

def poly_mul(a,b):
    z=0
    while b:
        if b&1:z^=a
        a<<=1;b>>=1
    return z

@lru_cache(None)
def x_poly(j):
    z=1;i=0
    while j:
        if j&1:z=poly_mul(z,s_poly(i))
        j>>=1;i+=1
    return z

def slow_basis(bits,m):
    out=0
    for j in range((1<<m)-1,-1,-1):
        if bits>>j&1:
            bits^=x_poly(j);out|=1<<j
    assert bits==0
    return out

def to_y(f,m,k,h):
    # Coefficients are h-bit vectors. y=x^(2^k)+x.
    if m==k:return f
    H=1<<(m-1);R=1<<(m-1-k)
    mask=(1<<(H*h))-1
    high=f>>(H*h); low=f&mask
    q=high^(high>>((H-R)*h))
    rem=low^((q<<(R*h))&mask)
    return to_y(rem,m-1,k,h)^(to_y(q,m-1,k,h)<<(H*h))

def packed_basis(f,m,h=1):
    if m<=1:return f
    k=1<<((m-1).bit_length()-1)
    D=1<<k
    fy=to_y(f,m,k,h)
    upper=packed_basis(fy,m-k,h*D)
    out=0; width=h*D; mask=(1<<width)-1
    for i in range(1<<(m-k)):
        out^=packed_basis((upper>>(i*width))&mask,k,h)<<(i*width)
    return out

def direct_eval(f,a,d):
    y=0
    for j in range(f.bit_length()-1,-1,-1):
        y=mul(y,a,d)^(f>>j&1)
    return y

def fafft(coeff,k,l,alpha,d,stats):
    if k==0:return [(alpha,coeff[0])]
    half=1<<(k-1); c=s_eval(k-1,alpha,d)
    stats['nodes']+=1;stats['coefficient_units']+=half;stats['twiddle_steps']+=k-1
    q0=[coeff[i]^mul(c,coeff[i+half],d) for i in range(half)]
    if l and l&(l-1)==0:
        return fafft(q0,k-1,l+1,alpha,d,stats)
    q1=[q0[i]^coeff[i+half] for i in range(half)]
    return fafft(q0,k-1,l if l==0 else l+1,alpha,d,stats)+fafft(q1,k-1,l+1,alpha^(1<<(k-1)),d,stats)

def full_evaluation(f,d):
    bits=packed_basis(f,d)
    coeff=[bits>>j&1 for j in range(1<<d)]
    stats=dict(nodes=0,coefficient_units=0,twiddle_steps=0)
    reps=fafft(coeff,d,0,0,d,stats);out={}
    for a,y in reps:
        start=a
        while True:
            assert a not in out
            out[a]=y
            a=mul(a,a,d);y=mul(y,y,d)
            if a==start:break
    assert len(out)==1<<d
    stats['representatives']=len(reps)
    return out,stats

def primitive(d):
    n=(1<<d)-1
    for a in range(1,1<<d):
        x=1;seen=set()
        for _ in range(n):seen.add(x);x=mul(x,a,d)
        if len(seen)==n:return a
    assert False

def test_chunk_tables(d,chunks):
    h=d//chunks; mask=(1<<h)-1
    tables={}
    for i in range(chunks):
        for j in range(chunks):
            tables[i,j]=[mul(a<<(i*h),b<<(j*h),d) for a in range(1<<h) for b in range(1<<h)]
    for a in range(1<<d):
        for b in range(1<<d):
            z=0
            for i in range(chunks):
                for j in range(chunks):z^=tables[i,j][(((a>>(i*h))&mask)<<h)|((b>>(j*h))&mask)]
            assert z==mul(a,b,d)
    return (1<<d)**2

@lru_cache(None)
def recurrence(k,l):
    if not k:return (0,0,1)
    children=[recurrence(k-1,l if l==0 else l+1)]
    if l==0 or l&(l-1):children.append(recurrence(k-1,l+1))
    return ((1<<(k-1))+sum(z[0] for z in children),k-1+sum(z[1] for z in children),sum(z[2] for z in children))

rng=random.Random(20261010)
result={}
# Exhaustive all binary polynomials through 16 coefficients.
nb=0
for m in range(5):
    vals=range(1<<(1<<m))
    for f in vals:
        assert packed_basis(f,m)==slow_basis(f,m);nb+=1
# Multi-lane coefficient-ring checks, lane-wise independent reference.
lanes=0
for m in range(2,8):
    for h in [2,3,7]:
        for _ in range(20):
            a=rng.getrandbits(h*(1<<m));out=packed_basis(a,m,h)
            for lane in range(h):
                bits=sum(((a>>(h*j+lane))&1)<<j for j in range(1<<m))
                ref=slow_basis(bits,m)
                actual=sum(((out>>(h*j+lane))&1)<<j for j in range(1<<m))
                assert actual==ref
            lanes+=1
result['basis_exhaustive_cases']=nb;result['basis_vector_lane_cases']=lanes
cantor=0
for d in [1,2,4,8]:
    for i in range(d):
        assert s_eval(i,1<<i,d)==1
        for a in range(1<<i):assert s_eval(i,a,d)==0
        cantor+=1
result['cantor_basis_indices']=cantor
result['chunk_table_pairs']=test_chunk_tables(8,4)
nttcases=[]
for d in [1,2,4,8]:
    Q=1<<d;N=Q-1;g=primitive(d)
    inputs=list(range(1<<N)) if d<=2 else [0,1,(1<<N)-1]+[rng.getrandbits(N) for _ in range(25)]
    for f in inputs:
        E,stats=full_evaluation(f,d)
        for a in range(Q):assert E[a]==direct_eval(f,a,d)
        a=1
        for j in range(N):
            direct=0
            for i in range(N):
                if f>>i&1:direct^=power(g,(i*j)%N,d)
            assert E[a]==direct;a=mul(a,g,d)
        assert tuple(stats[k] for k in ['coefficient_units','twiddle_steps','representatives'])==recurrence(d,0)
    nttcases.append(dict(d=d,N=N,root=g,inputs=len(inputs),stats=stats))
result['ntt_cases']=nttcases
result['recurrence_scaling']=[dict(d=d,Q_log2=d,units_div_Q=recurrence(d,0)[0]/(1<<d),twiddle_div_Q=recurrence(d,0)[1]/(1<<d),reps_div_Q=recurrence(d,0)[2]/(1<<d)) for d in [8,16,32,64,128,256]]
print(json.dumps(result,indent=2))
