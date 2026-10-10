#!/usr/bin/env python3
"""Independent exact controls; standard library only; no submitted code imported."""
import itertools, json, random, sys
from pathlib import Path

def ident(n): return [[int(i==j) for j in range(n)] for i in range(n)]
def zero(n,m=None): return [[0]*(n if m is None else m) for _ in range(n)]
def mul(a,b,p):
    out=zero(len(a),len(b[0]))
    for i,row in enumerate(a):
        for k,x in enumerate(row):
            if x:
                for j,y in enumerate(b[k]): out[i][j]=(out[i][j]+x*y)%p
    return out
def scale(a,c,p): return [[x*c%p for x in row] for row in a]
def add(a,b,p): return [[(x+y)%p for x,y in zip(r,s)] for r,s in zip(a,b)]
def sub(a,b,p): return add(a,scale(b,-1,p),p)
def trans(a): return list(map(list,zip(*a)))
def inv(a,p):
    n=len(a); u=[[(x%p) for x in a[i]]+ident(n)[i] for i in range(n)]
    for j in range(n):
        k=next(k for k in range(j,n) if u[k][j]); u[j],u[k]=u[k],u[j]
        u[j]=[x*pow(u[j][j],-1,p)%p for x in u[j]]
        for k in range(n):
            if k!=j:
                c=u[k][j]; u[k]=[(x-c*y)%p for x,y in zip(u[k],u[j])]
    return [r[n:] for r in u]
def powmat(a,n,p):
    z=ident(len(a))
    while n:
        if n&1:z=mul(z,a,p)
        a=mul(a,a,p);n//=2
    return z
def root(n,p):
    return next(w for w in range(1,p) if pow(w,n,p)==1 and all(pow(w,d,p)!=1 for d in range(1,n) if n%d==0))
def fourier(n,p,w=None):
    w=root(n,p) if w is None else w
    return [[pow(w,i*j,p) for j in range(n)] for i in range(n)]
def shift(n):
    z=zero(n)
    for j in range(n): z[(j+1)%n][j]=1
    return z
def diag(v): return [[x if i==j else 0 for j in range(len(v))] for i,x in enumerate(v)]
def blockdiag(blocks):
    n=sum(map(len,blocks)); z=zero(n); offset=0
    for b in blocks:
        for i,row in enumerate(b):z[offset+i][offset:offset+len(b)]=row
        offset+=len(b)
    return z
def kron(a,b): return [[x*y for x in ar for y in br] for ar in a for br in b]
def stat(a):
    rows=[sum(x!=0 for x in r) for r in a]; cols=[sum(x!=0 for x in r) for r in trans(a)]
    return dict(nnz=sum(rows),max_row=max(rows),max_column=max(cols))
def check(x,msg):
    if not x: raise AssertionError(msg)

def vector(a,v,p): return [sum(x*y for x,y in zip(row,v))%p for row in a]
def rank(a,p):
    z=[row[:] for row in a];r=0
    for j in range(len(z[0])):
        candidates=[i for i in range(r,len(z)) if z[i][j]%p]
        if not candidates:continue
        k=candidates[0];z[r],z[k]=z[k],z[r];c=pow(z[r][j],-1,p);z[r]=[x*c%p for x in z[r]]
        for i in range(len(z)):
            if i!=r:
                c=z[i][j];z[i]=[(x-c*y)%p for x,y in zip(z[i],z[r])]
        r+=1
        if r==len(z):break
    return r
from fractions import Fraction as F

def qm(a,b):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def qa(a,b):return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def qs(a,c):return [[x*c for x in r] for r in a]
def qi(a):
    n=len(a);u=[[F(x) for x in a[i]]+list(map(F,ident(n)[i])) for i in range(n)]
    for j in range(n):
        k=next(k for k in range(j,n) if u[k][j]);u[j],u[k]=u[k],u[j];c=u[j][j];u[j]=[x/c for x in u[j]]
        for k in range(n):
            if k!=j:
                c=u[k][j]
                if c:u[k]=[x-c*y for x,y in zip(u[k],u[j])]
    return [r[n:] for r in u]
def qv(a,v):return [sum(x*y for x,y in zip(r,v)) for r in a]
def residue(a,p):return [[x.numerator*pow(x.denominator,-1,p)%p if isinstance(x,F) else x%p for x in r] for r in a]
def realign(a,k):return [[a[i*k+j][u*k+v] for j in range(k) for v in range(k)] for i in range(k) for u in range(k)]
def swap(k):
    n=k*k;z=zero(n)
    for i in range(k):
        for j in range(k):z[i*k+j][j*k+i]=1
    return z

def qscan(weights,v):
    prod=F(1);acc=F(0);n=len(v)
    for i in range(n):acc+=prod*v[i];prod*=weights[i]
    y=[F(0)]*n;y[0]=acc/(1-prod)
    for i in range(n-1,0,-1):y[i]=v[i]+weights[i]*y[(i+1)%n]
    return y

def square_case(k):
    n=k*k;I=ident(n);S=swap(k);a=F(1,100*n);eps=F(1,10**6*n*n);b=F(n-1,n)
    weights=[b]*n;weights[0]*=F(2*n+1,2*n);rho=F(1)
    for w in weights:rho*=w
    G2=zero(n)
    for i in range(n):
        v=F(1)
        for d in range(n):
            G2[i][(i+d)%n]=v/(1-rho);v*=weights[(i+d)%n]
    G1=qs(qa(I,qs(S,a)),1/(1-a*a));T=qa(G1,qs(G2,eps));Ti=qi(T)
    check(min(x for r in G2 for x in r)>F(1,3) and max(x for r in G2 for x in r)<3,'G2 element bounds')
    check(min(abs(x) for r in Ti for x in r)>=eps/8,'inverse nonzero floor')
    check(all(Ti[i][j]<0 if i!=j else Ti[i][j]>F(1,2) for i in range(n) for j in range(n)),'inverse signs')
    rt=rank(residue(realign(T,k),1000003),1000003);check(rt==n,'source rational realignment full rank')
    ones=[F(1)]*n;check(len(set(qv(T,ones)))>1,'source nonconstant ones')
    for j in range(n):
        x=[F(i==j) for i in range(n)];gx=qscan(weights,x);sx=qv(S,x)
        out=[(v+a*s)/(1-a*a)+eps*g for v,s,g in zip(x,sx,gx)]
        check(out==qv(T,x),'independent linear scan')
    # All structural properties can coexist with inverse sparse+rank-one.
    u=[F(2)]+[F(1)]*(n-1);R=qs([[u[i] for j in range(n)] for i in range(n)],eps)
    sparse=qa(I,qs(S,-a));inv_counter=qa(sparse,R);gu=qv(G1,u);vg=[sum(r[j] for r in G1) for j in range(n)]
    denom=1+eps*sum(gu);counter=qa(G1,qs([[gu[i]*vg[j] for j in range(n)] for i in range(n)],-eps/denom))
    check(qm(counter,inv_counter)==I,'Sherman Morrison counterfamily')
    check(all(x for r in inv_counter for x in r),'counterfamily dense inverse')
    check(stat(sparse)['max_row']<=2 and rank(residue(R,1000003),1000003)==1,'counterfamily sparse rank one inverse')
    rc=rank(residue(realign(counter,k),1000003),1000003);check(rc==n,'counterfamily full Schmidt rank')
    check(len(set(qv(counter,ones)))>1,'counterfamily nonconstant response')
    return dict(N=n,A=k,source_inverse_min_abs=str(min(abs(x) for r in Ti for x in r)),source_inverse_floor=str(eps/8),source_realignment_rank=rt,basis_vectors_checked=n,counterfamily_inverse_max_row_sparse_degree=stat(sparse)['max_row'],counterfamily_inverse_correction_rank=1,counterfamily_inverse_dense=True,counterfamily_realignment_rank=rc,counterfamily_nonconstant_response=True)

def analytic():
    result=[]
    for n in [4,9,16,25,64,256,1024,4096]:
        a=F(1,100*n);e=F(1,10**6*n*n);b=F(n-1,n);d=F(2*n+1,2*n)
        check(b**(n-1)>F(1,3) and b**n<F(3,8),'rational geometric bounds')
        check(b*d<1 and b**n*d<1,'positive Green guards')
        hmin=F(1,3)-6*a;rem=64*n*n*e*e
        check(hmin>F(1,4) and rem<e/8,'dense inverse bounds')
        check(1-a-12*n*e-rem>F(1,2),'diagonal positivity')
        condition=(1/(1-a)+3*n*e)*(1+a)/(1-4*n*e);check(condition<2,'condition bound')
        check(3*n*e<a/(1-a*a),'Schmidt perturbation gap')
        near=a/(1-a)+3*n*e
        # Independent rank-one counterfamily bounds.
        delta=a+2*n*e;counter_condition=(1+delta)/(1-delta)
        check(counter_condition<2 and 4*n*e<a/(1-a*a),'counterfamily condition and Schmidt bounds')
        result.append(dict(N=n,condition_upper=str(condition),near_identity_upper=str(near),counterfamily_condition_upper=str(counter_condition),all_exact_inequalities=True))
    return result

def rigidity():
    rng=random.Random(1119);p=65537;results=[]
    for n in [4,8,16,32]:
        FF=fourier(n,p)
        for s in range(5):
            for rep in range(3):
                SS=zero(n)
                for i in range(n):
                    for j in rng.sample(range(n),min(s,n)):SS[i][j]=rng.randrange(1,p)
                m=n//(s+1);touched={j for row in SS[:m] for j,x in enumerate(row) if x};cols=[j for j in range(n) if j not in touched][:m]
                minor=[[FF[i][j] for j in cols] for i in range(m)]
                check(m==0 or rank(minor,p)==m,'Vandermonde witness')
                actual=rank(sub(FF,SS,p),p);check(actual>=m,'rigidity bound')
                results.append(dict(N=n,s=s,bound=m,actual_rank=actual))
    FF=fourier(4,p);E=[[1,1,p-1,p-1] for _ in range(4)];SS=sub(FF,E,p)
    check(rank(E,p)==1 and stat(SS)['max_row']==2,'N-s false stronger bound')
    return dict(random_cases=results,sharpness_control=dict(N=4,s=2,rank_defect=1))

def telescoping():
    rng=random.Random(871);p=65537;out=[]
    for n,L in [(8,2),(16,3),(32,4)]:
        sparse=[];errors=[];full=[]
        for ell in range(L):
            S=zero(n)
            for i in range(n):
                for j in rng.sample(range(n),2):S[i][j]=rng.randrange(1,p)
            u=[rng.randrange(1,p) for _ in range(n)];v=[rng.randrange(1,p) for _ in range(n)];E=[[x*y%p for y in v] for x in u]
            sparse.append(S);errors.append(E);full.append(add(S,E,p))
        A=ident(n);Sall=ident(n)
        for aa,ss in zip(full,sparse):A=mul(A,aa,p);Sall=mul(Sall,ss,p)
        total=zero(n)
        for j in range(L):
            term=ident(n)
            for f in sparse[:j]+[errors[j]]+full[j+1:]:term=mul(term,f,p)
            total=add(total,term,p)
        check(total==sub(A,Sall,p),'noncommuting telescope')
        rr=rank(total,p);check(rr<=L and stat(Sall)['max_row']<=2**L,'rank/sparsity product bounds')
        check(mul(full[0],full[1],p)!=mul(full[1],full[0],p),'genuinely noncommuting test')
        out.append(dict(N=n,layers=L,max_sparse_degree=stat(Sall)['max_row'],rank_difference=rr,rank_budget=L))
    return out

def sandwich():
    rng=random.Random(563);p=65537;out=[]
    for n in [4,8,16]:
        pi=list(range(n));sigma=list(range(n));rng.shuffle(pi);rng.shuffle(sigma)
        aa=[rng.randrange(1,p) for _ in range(n)];bb=[rng.randrange(1,p) for _ in range(n)];A=ident(n);B=ident(n)
        for i in range(n):A[i][pi[i]]=(A[i][pi[i]]-aa[i])%p;B[i][sigma[i]]=(B[i][sigma[i]]-bb[i])%p
        FF=fourier(n,p);q=[sigma.index(j) for j in range(n)]
        residual=sub(mul(mul(A,FF,p),B,p),add(A,B,p),p)
        direct=[[(FF[i][j]-aa[i]*FF[pi[i]][j]-bb[q[j]]*FF[i][q[j]]+aa[i]*bb[q[j]]*FF[pi[i]][q[j]]-A[i][j]-B[i][j])%p for j in range(n)] for i in range(n)]
        check(residual==direct,'four-root residual')
        summed=add(inv(A,p),inv(B,p),p)
        check(residual==mul(mul(A,sub(FF,summed,p),p),B,p),'sandwich equivalence')
        out.append(dict(N=n,entries_checked=n*n,residual_rank=rank(residual,p)))
    return out

def main():
    r=dict(status='PASS',source_square_cases=[square_case(k) for k in [2,3,4,5]],analytic_bounds=analytic(),rigidity=rigidity(),noncommuting_telescope=telescoping(),sandwich=sandwich(),uploaded_code_executed=False)
    path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('INDEPENDENT_RESULTS.json');path.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
if __name__=='__main__':main()
