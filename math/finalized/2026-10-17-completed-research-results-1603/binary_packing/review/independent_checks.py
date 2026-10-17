#!/usr/bin/env python3
"""Independent fresh audit; imports no candidate or historical program."""
from math import comb, lcm, prod, log, log2
from functools import lru_cache
from pathlib import Path
import random,json,hashlib
OUT=Path(__file__).parent
SRC=Path(__file__).resolve().parent.parent/'source'
@lru_cache(None)
def plan(r):
    E=lcm(*range(1,r+1));d=E//r
    pps=[]
    for p in range(2,r+1):
        if all(p%q for q in range(2,int(p**.5)+1)):
            u=p
            while u*p<=r:u*=p
            q=1
            while d%(q*p)==0:q*=p
            if q>1:pps.append((q,(-pow(E//u,-1,q))%q))
    k=sum(v*(d//q)*pow(d//q,-1,q) for q,v in pps)%d if d>1 else 1
    assert 1<=k<=max(1,d-1)
    P=1+k*E;rad=[1+(P-1)//j for j in range(1,r+1)];W=[1]
    for t in rad:W.append(W[-1]*t)
    assert W[-1]%d==0
    beta=W[-1]//d;s=beta.bit_length()-1
    assert beta>W[-2]
    assert all(W[j]==comb(P+j-1,j) for j in range(r+1))
    return P,rad,tuple(W),beta,s

@lru_cache(None)
def bc(x,j):return comb(x,j) if x>=j>=0 else (0 if x>=0 else (-1)**j*comb(j-x-1,j))
@lru_cache(None)
def norm(r,x):return sum(abs(bc(x,j)) for j in range(r))
@lru_cache(None)
def layout(n):
    r=n.bit_length()-1;P,rad,W,beta,s=plan(r);L=(n+s-1)//s
    a=min(range(r),key=lambda a:max(norm(r,-a),norm(r,2*r-2-a)))
    xs=range(-a,2*r-1-a)
    widths=tuple(8*(((2*L*((P-1)*norm(r,x))**2).bit_length()+7)//8) for x in xs)
    return r,P,rad,W,beta,s,L,a,tuple(xs),widths

def enc(b,r,rad):
    cs=[]
    for q in rad:
        b,z=divmod(b,q);cs.append(z)
    assert b==0 and len(cs)==r
    return cs

def ev(cs,x):return sum((-1)**j*c*bc(x,j) for j,c in enumerate(cs) if c)

def pack(row,w):
    # Fresh control implementation only; operation count is not evidence.
    u=0
    for z in reversed(row):u=(u<<w)+z
    return u

def school(x,y):
    # Explicit elementary multiplication used by the independently built executor.
    z=0
    while y:
        if y&1:z+=x
        x<<=1;y>>=1
    return z

def multiply(x,y,n,stats):
    assert abs(x).bit_length()<=n and abs(y).bit_length()<=n
    stats[0]+=1;stats[1]=max(stats[1],n)
    sign=-1 if (x<0)^(y<0) else 1;x=abs(x);y=abs(y)
    if n<16:stats[2]+=1;return sign*school(x,y)
    r,P,rad,W,beta,s,L,a,xs,widths=layout(n)
    if max(L*w for w in widths)>=n:stats[2]+=1;return sign*school(x,y)
    stats[3]+=1
    mask=(1<<s)-1
    aa=[enc((x>>(s*i))&mask,r,rad) for i in range(L)]
    bb=[enc((y>>(s*i))&mask,r,rad) for i in range(L)]
    rows=[]
    for node,w in zip(xs,widths):
        ar=[ev(c,node) for c in aa];br=[ev(c,node) for c in bb]
        U,V=pack(ar,w),pack(br,w)
        assert abs(U).bit_length()<=L*w and abs(V).bit_length()<=L*w
        z=multiply(U,V,L*w,stats);Q=1<<w;row=[]
        for _ in range(2*L-1):
            t=z%Q
            if t>=Q//2:t-=Q
            row.append(t);z=(z-t)//Q
        assert z==0
        assert row==[sum(ar[j]*br[k-j] for j in range(L) if 0<=k-j<L) for k in range(2*L-1)]
        rows.append(row)
    out=[]
    for k in range(2*L-1):
        vals=[row[k] for row in rows];v=0
        for j in range(2*r-1):
            v+=vals[0]*bc(-P+a,j)
            vals=[vals[h+1]-vals[h] for h in range(len(vals)-1)]
        assert v>=0
        out.append(v)
    return sign*pack(out,s)

result={'scope':'Fresh independent controls, no historical code or candidate code executed.'}
# Check the complete manifest and all source hashes as data.
manifest=json.loads((SRC/'MANIFEST.json').read_text())
for z in manifest['files']:
    b=(SRC/z['name']).read_bytes();assert len(b)==z['bytes'];assert hashlib.sha256(b).hexdigest()==z['sha256']
for z in json.loads((SRC/'SOURCE_PINS.json').read_text())['sources']:
    b=Path(z['path']).read_bytes();assert len(b)==z['bytes'];assert hashlib.sha256(b).hexdigest()==z['sha256']
result['all_manifest_and_source_pins_verified']=True
print('Manifest and source pins passed.',flush=True)
# Elementary LCM inequalities and exact row/window claims.
for r in range(2,129):
    E=lcm(*range(1,r+1));assert all(E%comb(r,j)==0 for j in range(r+1))
    assert (lcm(*range(1,(r+1)//2+1))*comb(r,r//2))%E==0
    P,rad,W,beta,s=plan(r)
    cs=[[0]*r]
    for j in range(r-1):c=[0]*r;c[j]=(rad[j]-1)//2;cs.append(c)
    c=[0]*r;c[0]=P-1;cs.append(c)
    if r>=3:
        for c in cs:
            b=sum(v*w for v,w in zip(c,W));assert b<1<<s;assert enc(b,r,rad)==c
    for x in range(-r+1,2*r-1):
        assert abs(bc(x,r-1))<=2*abs(bc(x,r-2))
        if r>=3:
            A=max(abs(ev(c,x)) for c in cs)
            assert (P-1)*norm(r,x)<=12*r*r*A
    norms={x:norm(r,x) for x in range(-r-2,2*r+3)}
    products=[prod(norms[x] for x in range(-a,2*r-1-a)) for a in range(r)]
    maxima=[max(norms[-a],norms[2*r-2-a]) for a in range(r)]
    crossing=next(a for a in range(r) if norms[-a]>=norms[2*r-2-a])
    allowed={crossing-1,crossing}
    assert {a for a,v in enumerate(products) if v==min(products)}<=allowed
    assert {a for a,v in enumerate(maxima) if v==min(maxima)}<=allowed
    for a in range(r-1):assert products[a+1]*norms[2*r-2-a]==products[a]*norms[-a-1]
result['exact_rank_checks']={'first':2,'last':128,'count':127}
print('127 exact rank checks passed.',flush=True)
rng=random.Random(202610171559)
products=[]
for n in [1,7,15,16,17,31,32,63,64,127,128,255,256,511,512]:
    cases=[(0,0),(0,(1<<n)-1),((1<<n)-1,-((1<<n)-1)),(-rng.getrandbits(n),rng.getrandbits(n))]
    signatures=[]
    for x,y in cases:
        st=[0,0,0,0];got=multiply(x,y,n,st);assert got==x*y
        signatures.append(st)
    assert all(st==signatures[0] for st in signatures)
    products.append({'declared_bits':n,'products':len(cases),'calls':signatures[0][0],'leaves':signatures[0][2],'recursive_calls':signatures[0][3]})
result['complete_recursive_products']=products
print('Complete recursive products passed.',flush=True)
# Exact child-width arithmetic and actual-length leading coefficient bounds.
metadata=[]
for r in [8,12,16,24,32,48,64,96,128,192,256,384]:
    P,rad,W,beta,s=plan(r);L=3*(1<<(r-1))//s
    if L<r+1:continue
    N=(L-1)*s+(P-1).bit_length();assert N.bit_length()-1==r
    rr,_,_,_,_,ss,LL,a,xs,capws=layout(N);assert (rr,ss,LL)==(r,s,L)
    assert all(L*w<N for w in capws)
    cs=[]
    for j in range(r-1):c=[0]*r;c[j]=(rad[j]-1)//2;cs.append(c)
    c=[0]*r;c[0]=P-1;cs.append(c)
    actualws=[]
    for x in xs:
        A=max(abs(ev(c,x)) for c in cs)
        w=8*(((2*L*A*A).bit_length()+7)//8)
        Q=1<<w;assert Q>2*L*A*A and 2*A<Q-1
        actualws.append(w)
    kappa=log2(P)/r;J=1.5444697908028986
    metadata.append({'rank':r,'actual_input_rank':N.bit_length()-1,'cap_volume':L*sum(capws)/N,'witness_allocated_volume':L*sum(actualws)/N,'witness_actual_length_lower':sum((L-1)*w+(P-2).bit_length() for w in actualws)/N,'predicted_volume':4+(2+2*J)/kappa,'maximum_child_fraction':L*max(capws)/N})
result['large_exact_metadata']=metadata
(OUT/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'all_pins':True,'rank_checks':127,'recursive_products':sum(z['products'] for z in products),'recursive_calls':sum(4*z['calls'] for z in products),'metadata_ranks':len(metadata)},indent=2))
