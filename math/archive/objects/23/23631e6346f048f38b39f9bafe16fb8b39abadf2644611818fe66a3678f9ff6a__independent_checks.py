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

def det(a,p):
    z=[r[:] for r in a];out=1;n=len(a)
    for j in range(n):
        ks=[k for k in range(j,n) if z[k][j]%p]
        if not ks:return 0
        k=ks[0]
        if k!=j:z[j],z[k]=z[k],z[j];out=-out
        c=z[j][j];out=out*c%p;ci=pow(c,-1,p)
        for k in range(j+1,n):
            t=z[k][j]*ci%p;z[k]=[(x-t*y)%p for x,y in zip(z[k],z[j])]
    return out%p

def prime(p):return p>=2 and all(p%d for d in range(2,int(p**0.5)+1))
def choose_chirp_field(n):
    for k in range(2,1000):
        p=k*n+1
        if prime(p):
            w=root(n,p);h=(n+1)//2;G=sum(pow(w,h*j*j,p) for j in range(n))%p;c=n*G%p
            if (1+c)%p:return p,w
    raise AssertionError('test field not found')
def rectangle(M,I,J):return [[M[i][j] for j in J] for i in I]
def cycle_order(order):
    pi=[0]*len(order)
    for i,j in zip(order,order[1:]+order[:1]):pi[i]=j
    return pi

def target(n,p=None,w=None):
    if p is None:p,w=choose_chirp_field(n)
    I=ident(n);FF=fourier(n,p,w);FI=inv(FF,p);h=(n+1)//2;A=diag([pow(w,h*j*j,p) for j in range(n)]);G=sum(A[j][j] for j in range(n))%p;c=n*G%p;check((1+c)%p!=0,'chirp feedback guard')
    X=add(A,FI,p);B=inv(X,p);check(stat(X)['max_row']==n,'at least one full inverse row');check(all(X[i][j] for i in range(n) for j in range(n) if i!=j),'all offdiagonals nonzero')
    rng=random.Random(765+n);order=list(range(n));rng.shuffle(order);perms=[[(i+1)%n for i in range(n)],[(i+n//2)%n for i in range(n)],cycle_order(order)]
    greenchecks=0;cutchecks=0;displacements=[];m=n//2
    for which,pi in enumerate(perms):
        weights=[rng.randrange(1,p) for _ in range(n)]
        if which==2:weights[n//2]=0
        rho=1
        for v in weights:rho=rho*v%p
        if rho==1:weights[0]=0
        W=zero(n)
        for i,j in enumerate(pi):W[i][j]=weights[i]
        Q=sub(I,W,p);GG=inv(Q,p);sume=0
        for start in range(n):
            rows=[(start+k)%n for k in range(m)];comp=[j for j in range(n) if j not in rows]
            e=sum(pi[i] in comp for i in rows);sume+=e
            rr=rank(rectangle(GG,rows,comp),p);rq=rank(rectangle(Q,rows,comp),p)
            check(rr==rq and rr<=e,'inverse cut rank and edge budget');greenchecks+=1
            # Singular diagonal endpoints remain valid under the cut bound.
            left=diag([0]+[1]*(n-1));right=diag([1]*(n-1)+[0]);singular=mul(mul(left,GG,p),right,p)
            check(rank(rectangle(singular,rows,comp),p)<=e,'singular endpoint cut retention')
            if which==0:
                rb=rank(rectangle(B,rows,comp),p);rx=rank(rectangle(X,rows,comp),p);rf=rank(rectangle(FI,rows,comp),p)
                check(rb==rx==rf==m,'cyclic half target rank');cutchecks+=1;check(e==1,'natural-cycle single crossing')
            if which==1:check(e==m,'long-jump cut gate passes')
        dist=sum(min((i-pi[i])%n,(pi[i]-i)%n) for i in range(n));check(sume==dist,'circular displacement identity');displacements.append(dict(kind=which,cut_sum=sume,displacement_sum=dist))
    defects=[]
    for d in [0,1,2,3]:
        S=zero(n)
        for i in range(n):
            for j in rng.sample(range(n),d):S[i][j]=rng.randrange(1,p)
        E=sub(X,S,p);rr=rank(E,p);bound=n//(d+2);check(rr>=bound,'inherited chirp inverse rigidity');defects.append(dict(row_degree=d,bound=bound,actual_rank=rr))
    return dict(N=n,p=p,root=w,c=c,diagonal=[X[i][i] for i in range(n)],maximum_inverse_row_support=stat(X)['max_row'],half_cut_checks=cutchecks,Green_cut_checks=greenchecks,circular_displacement=displacements,inverse_defects=defects),B,X,FI

def monomial(n,p,rng):
    pi=list(range(n));rng.shuffle(pi);M=zero(n)
    for i,j in enumerate(pi):M[i][j]=rng.randrange(1,p)
    return M

def products(n,p):
    rng=random.Random(687+n);out=[]
    for length in [1,2,3]:
        factors=[];inversefactors=[]
        for ell in range(length):
            order=list(range(n));rng.shuffle(order);pi=cycle_order(order);W=zero(n)
            for i,j in enumerate(pi):W[i][j]=rng.randrange(1,p)
            rho=1
            for i,j in enumerate(pi):rho=rho*W[i][j]%p
            if rho==1:W[0][pi[0]]=0
            Q=sub(ident(n),W,p);L=monomial(n,p,rng);R=monomial(n,p,rng)
            GG=mul(mul(L,inv(Q,p),p),R,p);GI=mul(mul(inv(R,p),Q,p),inv(L,p),p)
            check(mul(GG,GI,p)==ident(n) and stat(GI)['max_row']<=2,'monomial-ended sparse inverse')
            factors.append(GG);inversefactors.append(GI)
        product=ident(n)
        for G in factors:product=mul(G,product,p)
        inverseproduct=ident(n)
        for GI in inversefactors:inverseproduct=mul(inverseproduct,GI,p)
        check(inverseproduct==inv(product,p),'inverse factor order');degree=stat(inverseproduct)['max_row'];check(degree<=2**length,'pure inverse product support')
        out.append(dict(N=n,p=p,layers=length,actual_degree=degree,degree_bound=2**length))
    return out

def defect_telescope(n,p):
    rng=random.Random(484+n);sparse=[];full=[];errors=[]
    for ell in range(3):
        S=zero(n)
        for i in range(n):
            for j in rng.sample(range(n),2):S[i][j]=rng.randrange(1,p)
        u=[rng.randrange(1,p) for _ in range(n)];v=[rng.randrange(1,p) for _ in range(n)];E=[[x*y%p for y in v] for x in u];sparse.append(S);errors.append(E);full.append(add(S,E,p))
    AA=ident(n);SS=ident(n)
    for a,s in zip(full,sparse):AA=mul(AA,a,p);SS=mul(SS,s,p)
    total=zero(n)
    for j in range(3):
        term=ident(n)
        for z in full[:j]+[errors[j]]+sparse[j+1:]:term=mul(term,z,p)
        total=add(total,term,p)
    check(total==sub(AA,SS,p),'full-prefix sparse-suffix telescope');check(rank(total,p)<=3 and stat(SS)['max_row']<=8,'defect rank degree bounds')
    return dict(N=n,p=p,rank_difference=rank(total,p),rank_budget=3,sparse_degree=stat(SS)['max_row'])

def main():
    controls=[];productcases=[];telescopes=[]
    for n in [3,5,7,9,15,21]:
        report,B,X,FI=target(n);controls.append(report);productcases+=products(n,report['p']);telescopes.append(defect_telescope(n,report['p']))
    cancel,B,X,FI=target(5,521,104);check(cancel['diagonal']==[418,24,0,0,24] and cancel['c']==47,'published finite cancellation control')
    _,BB,XX,FFI=target(9);rows=[0,3,6];cols=[i for i in range(9) if i not in rows];p=choose_chirp_field(9)[0]
    br=rank(rectangle(BB,rows,cols),p);fr=rank(rectangle(FFI,rows,cols),p);check(br==fr==2,'noncontiguous complementary cut not necessarily full')
    result=dict(status='PASS',target_controls=controls,finite_diagonal_cancellation=cancel,monomial_ended_products=productcases,defect_telescoping=telescopes,noncontiguous_cut_control=dict(N=9,p=p,rows=rows,rank_B=br,rank_F_inverse=fr,maximum_possible=3),uploaded_or_constructor_code_executed=False)
    path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('INDEPENDENT_RESULTS.json');path.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
