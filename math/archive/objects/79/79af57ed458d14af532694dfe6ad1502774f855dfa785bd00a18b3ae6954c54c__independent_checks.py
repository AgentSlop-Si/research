"""Independently authored audit checker; never imports or executes supplied files.
Only standard library, exact arithmetic, deterministic fixtures.
"""
from itertools import product, combinations
from math import gcd, isqrt, comb
from random import Random
from collections import Counter
from pathlib import Path
import json, hashlib, time

COUNTS=Counter()
RNG=Random(195417)

def prime(p):
    return p>=2 and all(p%d for d in range(2,isqrt(p)+1))

def field(n):
    p=n+1
    while not prime(p): p+=n
    for w in range(1,p):
        if pow(w,n,p)==1 and all(pow(w,d,p)!=1 for d in range(1,n) if n%d==0): return p,w
    raise AssertionError(n)

def dft(x,p,w):
    n=len(x)
    return [sum(x[j]*pow(w,(-j*k)%n,p) for j in range(n))%p for k in range(n)]

def rank(matrix,p):
    a=[list(row) for row in matrix]
    h=0
    for j in range(len(a[0]) if a else 0):
        candidates=[i for i in range(h,len(a)) if a[i][j]%p]
        if not candidates: continue
        z=candidates[0]; a[h],a[z]=a[z],a[h]
        f=pow(a[h][j],-1,p); a[h]=[v*f%p for v in a[h]]
        for i in range(h+1,len(a)):
            f=a[i][j]; a[i]=[(v-f*u)%p for v,u in zip(a[i],a[h])]
        h+=1
        if h==len(a): break
    return h

def recurrence(seq,p,limit):
    # Textbook dynamically allocated BM, independently implemented.
    connection=[1]; previous=[1]; length=0; gap=1; last=1
    for index,value in enumerate(seq):
        delta=(value+sum(connection[j]*seq[index-j] for j in range(1,length+1)))%p
        if not delta:
            gap+=1; continue
        new_length=index+1-length if 2*length<=index else length
        if new_length>limit:return None
        old=connection[:]
        scale=delta*pow(last,-1,p)%p
        connection += [0]*max(0,gap+len(previous)-len(connection))
        for j,v in enumerate(previous):connection[j+gap]=(connection[j+gap]-scale*v)%p
        if 2*length<=index:
            length=new_length; previous=old; last=delta; gap=1
        else:gap+=1
    return connection[:length+1]

def linear_solve(matrix,rhs,p):
    a=[list(row)+[v] for row,v in zip(matrix,rhs)]; n=len(rhs)
    for j in range(n):
        pivot=next((i for i in range(j,n) if a[i][j]%p),None)
        if pivot is None:return None
        a[j],a[pivot]=a[pivot],a[j]
        inv=pow(a[j][j],-1,p);a[j]=[v*inv%p for v in a[j]]
        for i in range(n):
            if i!=j:
                scale=a[i][j];a[i]=[(v-scale*u)%p for v,u in zip(a[i],a[j])]
    return [row[-1] for row in a]

def decode(seq,p,w,r):
    m=len(seq)
    if m<3*r:
        z=dft(seq,p,w); inv=pow(m,-1,p)
        return [(h,v*inv%p) for h,v in enumerate(z) if v] if sum(bool(v) for v in z)<=r else None
    c=recurrence(seq,p,r)
    if c is None:return None
    s=len(c)-1
    if not s:return [] if all(v%p==0 for v in seq) else None
    nodes=[]
    for h in range(m):
        z=pow(w,h,p)
        if sum(c[j]*pow(z,s-j,p) for j in range(s+1))%p==0:nodes.append((h,z))
    if len(nodes)!=s:return None
    weights=linear_solve([[pow(z,j,p) for _,z in nodes] for j in range(s)],seq[:s],p)
    if weights is None or 0 in weights:return None
    if any((seq[j]-sum(v*pow(z,j,p) for v,(_,z) in zip(weights,nodes)))%p for j in range(m)):return None
    return [(h,v) for (h,_),v in zip(nodes,weights)]

def fibers(x,p,w,q,r):
    n=len(x);m=n//q
    rows=[decode(x[t::q],p,pow(w,q,p),r) for t in range(q)]
    if any(row is None for row in rows):return None
    out=[0]*n
    for t,row in enumerate(rows):
        for h,c in row:
            for k in range(h,n,m):out[k]=(out[k]+m*c*pow(w,(-t*k)%n,p))%p
    return out,rows

def make_fibers(n,p,w,q,modes):
    m=n//q
    return [sum(c*pow(w,q*h*(j//q),p) for h,c in modes[j%q])%p for j in range(n)]

def eliminant(x,center,r,p):
    # Generic subset dynamic-programming determinant over polynomials.
    # Build same mathematical Hankel, no source implementation reused.
    n=r+1;states={0:{0:1}}
    for i in range(n):
        nxt={}
        for mask,poly in states.items():
            for j in range(n):
                if mask>>j&1:continue
                sign=-1 if sum(mask>>k&1 for k in range(j+1,n))%2 else 1
                e=(i+j)*(i+j-1)//2;v=x[center-r+i+j]*sign
                dest=nxt.setdefault(mask|(1<<j),{})
                for deg,a in poly.items():dest[deg+e]=(dest.get(deg+e,0)+a*v)%p
        states=nxt
    shift=(r+1)*r*(r-1)//2; poly=states[(1<<n)-1]
    assert all(v==0 for d,v in poly.items() if d<shift)
    out=[poly.get(shift+j,0)%p for j in range(comb(r+2,3)+1)]
    assert out[0]==((-1)**(r*(r+1)//2)*pow(x[center],r+1,p))%p
    return out

def chirp_decode(x,p,w,r):
    n=len(x)
    if not any(x):return 0,[]
    c=next((j for j in range(r,n-r) if x[j]),None)
    if c is None:return None
    pol=eliminant(x,c,r,p);candidates=[]
    for a in range(n//gcd(n,2)):
        t=pow(w,(-2*a)%n,p)
        if sum(v*pow(t,j,p) for j,v in enumerate(pol))%p==0:candidates.append(a)
    assert len(candidates)<=comb(r+2,3)
    for a in candidates:
        modes=decode([x[j]*pow(w,(-a*j*j)%n,p)%p for j in range(n)],p,w,r)
        if modes is not None:return a,modes
    return None

def gauss_row(n,p,w,a):
    d=gcd(n,a);m=n//d
    if m==1:return [n%p if c%n==0 else 0 for c in range(n)]
    aa=a//d;eta=pow(w,d,p)
    b=0 if m%2 else (m//2)%2
    base=sum(pow(eta,(aa*j*j+b*j)%m,p) for j in range(m))%p
    out=[]
    for c in range(n):
        if c%d:out.append(0);continue
        cc=c//d
        if m%2:
            shift=cc*pow(2*aa,-1,m)%m
        else:
            if (cc-b)%2:out.append(0);continue
            shift=0 if m==2 else ((cc-b)//2)*pow(aa,-1,m//2)%(m//2)
        out.append(d*base*pow(eta,(-aa*shift*shift-b*shift)%m,p)%p)
    return out

def run():
    start=time.time()
    # Exact spectral membership oracle independent of recurrence.
    for m,p,w,r in [(3,7,2,1),(4,5,2,1),(6,7,3,2)]:
        for tup in product(range(p),repeat=m):
            spec=dft(tup,p,w);want=sum(bool(v) for v in spec)<=r
            modes=decode(tup,p,w,r)
            assert (modes is not None)==want,(m,p,r,tup)
            if modes is not None:
                assert [sum(c*pow(w,h*j,p) for h,c in modes)%p for j in range(m)]==list(tup)
            COUNTS['exhaustive_row_membership_vectors']+=1
            COUNTS['exhaustive_row_membership_accepts']+=want
    # Every factorization at a diverse range of lengths, endpoint sizes included.
    for n in [1,2,3,4,6,8,9,12,15,16,18,20,24,25,27,32,36,45,49,60,64,72,81,125]:
        p,w=field(n)
        for q in range(1,isqrt(n)+1):
            if n%q:continue
            m=n//q
            for r in sorted(set([1,min(2,m),min(3,m)])):
                for trial in range(3):
                    modes=[]
                    for _ in range(q):
                        k=RNG.randrange(min(r,m)+1)
                        modes.append([(h,RNG.randrange(1,p)) for h in RNG.sample(range(m),k)])
                    x=make_fibers(n,p,w,q,modes);res=fibers(x,p,w,q,r)
                    assert res is not None and res[0]==dft(x,p,w)
                    COUNTS['raw_fiber_cases']+=1;COUNTS['direct_dft_bins']+=n
    # CRT factorization identities with arbitrary factor vectors, not chirps.
    for a,b in [(2,3),(3,4),(3,5),(4,5),(5,6),(5,7),(7,9),(8,9),(9,10),(11,13)]:
        n=a*b;p,w=field(n);ea=b*pow(b,-1,a);eb=a*pow(a,-1,b)
        for r in range(1,4):
            f=[[RNG.randrange(p) for _ in range(a)] for _ in range(r)]
            g=[[RNG.randrange(p) for _ in range(b)] for _ in range(r)]
            mat=[[sum(f[l][u]*g[l][v] for l in range(r))%p for v in range(b)] for u in range(a)]
            assert rank(mat,p)<=r
            x=[0]*n
            for u,v in product(range(a),range(b)):x[(u*ea+v*eb)%n]=mat[u][v]
            ff=[dft(row,p,pow(w,b,p)) for row in f];gg=[dft(row,p,pow(w,a,p)) for row in g]
            out=[0]*n
            for s,t in product(range(a),range(b)):out[(s*b+t*a)%n]=sum(ff[l][s]*gg[l][t] for l in range(r))%p
            assert out==dft(x,p,w)
            transformed=[[out[(s*b+t*a)%n] for t in range(b)] for s in range(a)]
            assert rank(mat,p)==rank(transformed,p)
            COUNTS['tensor_identity_and_rank_cases']+=1;COUNTS['direct_dft_bins']+=n
    # Full-rank sparse fibers and growing r, with varying field/root.
    for q in range(2,11):
        n=q*q;p,w=field(n)
        x=make_fibers(n,p,w,q,[[(t,t+1)] for t in range(q)])
        assert rank([x[t::q] for t in range(q)],p)==q
        assert fibers(x,p,w,q,1)[0]==dft(x,p,w)
        COUNTS['maximal_rank_fiber_cases']+=1;COUNTS['direct_dft_bins']+=n
    # Entire common-chirp phase quotient, including endpoints and nonunit phases.
    for n in range(3,31):
        p,w=field(n)
        for r in range(1,min(3,n//3)+1):
            for a in range(n):
                modes=[(h,RNG.randrange(1,p)) for h in RNG.sample(range(n),r)]
                x=[sum(c*pow(w,(a*j*j+h*j)%n,p) for h,c in modes)%p for j in range(n)]
                res=chirp_decode(x,p,w,r)
                assert res is not None,(n,r,a)
                aa,mm=res;row=gauss_row(n,p,w,aa)
                out=[sum(c*row[(h-k)%n] for h,c in mm)%p for k in range(n)]
                assert out==dft(x,p,w)
                COUNTS['common_chirp_phase_coverage_cases']+=1;COUNTS['direct_dft_bins']+=n
    for n in range(1,41):
        p,w=field(n)
        for a in range(n):
            expected=[sum(pow(w,(a*j*j+c*j)%n,p) for j in range(n))%p for c in range(n)]
            assert gauss_row(n,p,w,a)==expected
            COUNTS['all_length_gauss_rows']+=1;COUNTS['all_length_gauss_entries']+=n
    # New degree-independent square-multiplier bound: N=d*s*s, Q=s, support <=d.
    for d in range(1,9):
        for s in [2,3,4,5]:
            n=d*s*s;p,w=field(n)
            for degree in [2,3,4,7,13]:
                coefficients=[RNG.randrange(n) for _ in range(degree+1)]
                x=[pow(w,sum(c*pow(j,k,n) for k,c in enumerate(coefficients))%n,p) for j in range(n)]
                row_supports=[sum(bool(z) for z in dft(x[t::s],p,pow(w,s,p))) for t in range(s)]
                assert max(row_supports)<=d
                res=fibers(x,p,w,s,d)
                assert res is not None and res[0]==dft(x,p,w)
                COUNTS['square_multiplier_polynomial_cases']+=1;COUNTS['direct_dft_bins']+=n
    # Concrete default-divisor coverage gap at N=12.
    n,p,w,q,r=12,13,2,2,1
    x=make_fibers(n,p,w,q,[[(0,1)],[(1,2)]])
    assert x==[1,2,1,8,1,6,1,11,1,5,1,7]
    assert fibers(x,p,w,2,1)[0]==dft(x,p,w)
    assert fibers(x,p,w,3,1) is None
    ea,eb=4,9
    matrix=[[x[(u*ea+v*eb)%n] for v in range(4)] for u in range(3)]
    assert rank(matrix,p)==2
    assert chirp_decode(x,p,w,1) is None
    assert all(x) # maximal support coset is the whole group.
    gap={'N':n,'p':p,'omega':w,'r':1,'raw_input':x,'accepted_Q':2,'default_Q':3,'default_CRT_rank':2,'common_chirp_rank_1':False,'support_step':1}
    # Extension coefficient recovery formula checked against independent linear solve.
    for p in [17,37,101,257]:
        for s in range(1,min(12,p)):
            z=RNG.sample(range(p),s);c=[RNG.randrange(p) for _ in range(s)]
            y=[sum(v*pow(node,j,p) for node,v in zip(z,c))%p for j in range(s)]
            recovered=[]
            for i,node in enumerate(z):
                poly=[1];denom=1
                for k,other in enumerate(z):
                    if k==i:continue
                    new=[0]*(len(poly)+1)
                    for j,v in enumerate(poly):new[j]=(new[j]-other*v)%p;new[j+1]=(new[j+1]+v)%p
                    poly=new;denom=denom*(node-other)%p
                recovered.append(sum(poly[j]*y[j] for j in range(s))*pow(denom,-1,p)%p)
            assert recovered==c
            COUNTS['independent_vandermonde_cases']+=1
    report={'status':'PASS','seed':195417,'method':'independently authored standard-library code; no supplied source imported or executed','counts':dict(COUNTS),'default_divisor_counterexample':gap,'seconds_diagnostic_only':round(time.time()-start,3)}
    Path(__file__).with_name('independent_results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':run()
