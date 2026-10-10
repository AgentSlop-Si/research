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

def perm(pi):
    P=zero(len(pi))
    for i,j in enumerate(pi):P[i][j]=1
    return P

def rowpos(M):return [next(j for j,x in enumerate(r) if x) for r in M]
def colpos(M):return rowpos(trans(M))
def rows_of_gate(B,r0,r1,c0,c1,i,k,cols,p):
    result=[]
    for j in cols:
        a,c=B[r0[i]][c0[j]],B[r0[i]][c1[j]];b,d=B[r1[i]][c0[j]],B[r1[i]][c1[j]]
        e,g=B[r0[k]][c0[j]],B[r0[k]][c1[j]];f,h=B[r1[k]][c0[j]],B[r1[k]][c1[j]]
        result.append([(a*g-c*e)%p,(b*g-d*e)%p,(a*h-c*f)%p,(b*h-d*f)%p])
    return result

def target():
    n=13;p=65521;check(all(p%d for d in range(2,int(p**0.5)+1)),'test modulus prime');w=pow(17,(p-1)//n,p);check(w==56909 and pow(w,n,p)==1 and w!=1,'primitive thirteenth root')
    h=7;ph=[pow(w,h*j*j,p) for j in range(n)];G=sum(ph)%p;c=n*G%p;check((G,c,(1+c)%p)==(63693,41757,41758),'Gauss scalar and guard')
    FF=fourier(n,p,w);A=diag(ph);B=inv(add(inv(FF,p),A,p),p)
    formula=[[(pow(w,i*j,p)-G*pow(w,(-h*(i+j)**2)%n,p)+(c*pow(w,(-h*i*i)%n,p) if i==j else 0))*pow(1+c,-1,p)%p for j in range(n)] for i in range(n)]
    check(B==formula,'every explicit target entry')
    pi=[(i+6)%n for i in range(n)];sigma=list(range(n));sigma[0],sigma[1]=1,0;tau=[sigma[pi[sigma[i]]] for i in range(n)]
    check(tau==[7,6,8,9,10,11,12,1,0,2,3,4,5],'conjugate order')
    for order in [pi,tau]:
        orbit=[];x=0
        while x not in orbit:orbit.append(x);x=order[x]
        check(len(orbit)==n and x==0,'Hamiltonian order')
    check(pi[tau[0]]==0 and tau[pi[0]]==12,'explicit noncommutation')
    invtau=[tau.index(j) for j in range(n)];forbidden={0,pi[0],tau[0],1,pi[1],tau[1]};cols=[2,3,4,5]
    check(forbidden=={0,1,6,7} and not forbidden.intersection(cols),'structurally off-support columns');check([invtau[j] for j in cols]==[9,10,11,12],'column support orientation')
    R=rows_of_gate(B,list(range(n)),pi,list(range(n)),invtau,0,1,cols,p)
    expected=[[30388,12950,52923,20728],[30191,50630,14717,481],[27205,30796,53578,20728],[20815,59325,15216,39038]]
    check(R==expected,'exact displayed four by four matrix');dd=det(R,p);check(dd==60131,'exact determinant')
    budgets=[]
    for start in range(n):
        I={(start+k)%n for k in range(6)};ep=sum(pi[i] not in I for i in I);et=sum(tau[i] not in I for i in I)
        check(ep==6 and ep+et>=6,'all half-cut budgets pass');budgets.append([ep,et])
    return dict(N=n,p=p,omega=w,G=G,c=c,denominator=(1+c)%p,pi=pi,tau=tau,rows=[0,1],columns=cols,forbidden=sorted(forbidden),tau_inverse_columns=[invtau[j] for j in cols],coefficient_matrix=R,determinant=dd,half_cut_budgets=budgets),pi,tau

def branch(pi,p,rng,monomial,zero_edges,singular,zero_branch=False):
    n=len(pi);w=[rng.randrange(1,p) for _ in range(n)]
    if zero_edges:
        for i in range(0,n,3):w[i]=0
    rho=1
    for x in w:rho=rho*x%p
    if rho==1:w[0]=0
    W=zero(n)
    for i,j in enumerate(pi):W[i][j]=w[i]
    Q=sub(ident(n),W,p);qinv=inv(Q,p)
    lp=list(range(n));rp=list(range(n))
    if monomial:rng.shuffle(lp);rng.shuffle(rp)
    lw=[rng.randrange(1,p) for _ in range(n)];rw=[rng.randrange(1,p) for _ in range(n)]
    if singular:lw[1]=0;rw[4]=0
    if zero_branch:lw=[0]*n
    PL=perm(lp);PR=perm(rp);L=mul(diag(lw),PL,p);R=mul(diag(rw),PR,p);T=mul(mul(L,qinv,p),R,p)
    pattern0=mul(inv(PR,p),inv(PL,p),p);pattern1=mul(mul(inv(PR,p),perm(pi),p),inv(PL,p),p)
    result=dict(T=T,rows0=rowpos(pattern0),rows1=rowpos(pattern1),cols0=colpos(pattern0),cols1=colpos(pattern1),invertible=not singular and not zero_branch)
    if result['invertible']:
        result['Q']=mul(mul(inv(R,p),Q,p),inv(L,p),p)
        result['Qbase']=mul(inv(R,p),inv(L,p),p)
        result['Qedge']=scale(mul(mul(inv(R,p),W,p),inv(L,p),p),-1,p)
    return result

def positive_control(kind,pi,tau):
    n=len(pi);p=65521;rng=random.Random(926+sum(map(ord,kind)));mono=kind.startswith('monomial');zero='zero_edge' in kind;singular='singular' in kind;zero_branch='zero_branch' in kind
    t0=branch(pi,p,rng,mono,zero,singular,zero_branch);t1=branch(tau,p,rng,mono,zero,singular);B=add(t0['T'],t1['T'],p)
    r0,r1=t0['rows0'],t0['rows1'];c0,c1=t1['cols0'],t1['cols1'];count=0;maxrank=0
    invertible=t0['invertible'] and t1['invertible']
    if invertible:check(mul(mul(t0['Q'],B,p),t1['Q'],p)==add(t0['Q'],t1['Q'],p),'Q0 B Q1 orientation')
    for i in range(n):
        for k in range(i+1,n):
            forbid={r0[i],r1[i],t1['rows0'][i],t1['rows1'][i],r0[k],r1[k],t1['rows0'][k],t1['rows1'][k]};cols=[j for j in range(n) if j not in forbid];check(len(cols)>=4,'sufficient eligible structural columns')
            gate=rows_of_gate(B,r0,r1,c0,c1,i,k,cols,p);rr=rank(gate,p);check(rr<=3 and det(gate[:4],p)==0,'necessary polynomial gate for genuine sum');maxrank=max(maxrank,rr);count+=1
            if invertible:
                a=t0['Qbase'][i][r0[i]];b=t0['Qedge'][i][r1[i]];d=t0['Qbase'][k][r0[k]];e=t0['Qedge'][k][r1[k]];z=[a*d%p,b*d%p,a*e%p,b*e%p]
                check(any(z) and all(sum(x*y for x,y in zip(row,z))%p==0 for row in gate),'nonzero decomposable denominator tensor')
    return dict(kind=kind,row_pairs_checked=count,max_gate_rank=maxrank,inverse_identity_checked=invertible,singular_endpoints_retained=singular or zero_branch,zero_edges_retained=zero)

def main():
    report,pi,tau=target();kinds=['diagonal','diagonal_zero_edge','diagonal_singular','diagonal_zero_branch','monomial','monomial_zero_edge','monomial_singular']
    controls=[positive_control(k,pi,tau) for k in kinds]
    synthetic=[[0,1,0,0],[0,0,1,0],[1,0,0,-1]];z=[1,0,0,1];check(rank(synthetic,65521)==3 and all(sum(x*y for x,y in zip(row,z))==0 for row in synthetic) and z[0]*z[3]!=z[1]*z[2],'rank three still needs decomposability')
    result=dict(status='PASS',target_certificate=report,genuine_two_Green_controls=controls,total_positive_row_pairs=sum(x['row_pairs_checked'] for x in controls),rank_three_decomposability_control=True,uploaded_or_constructor_code_executed=False)
    path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('INDEPENDENT_RESULTS.json');path.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
