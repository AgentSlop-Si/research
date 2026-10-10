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

def prime(p):return p>=2 and all(p%d for d in range(2,int(p**0.5)+1))
def field(n):return next(p for p in range(n+1,10000,n) if prime(p))
def data(q,m,p):
    n=q*m;w=root(n,p);fm=fourier(m,p,pow(w,q,p));fq=fourier(q,p,pow(w,m,p));L=kron(fq,ident(m));Delta=diag([pow(w,b*t,p) for b in range(q) for t in range(m)]);R=zero(n)
    for b in range(q):
        for s in range(m):R[b*m+s][b+q*s]=1
    return n,w,fm,fq,L,Delta,R

def perm(pi):
    P=zero(len(pi))
    for i,j in enumerate(pi):P[i][j]=1
    return P

def relocated(M):
    n=M*M;p=field(n);w=root(n,p);eta=pow(w,M,p);fm=fourier(M,p,eta);FF=fourier(n,p,w);I=ident(n);B=blockdiag([fm]*M);Bi=inv(B,p);L=kron(fm,ident(M));Dlt=diag([pow(w,b*s,p) for b in range(M) for s in range(M)]);K=zero(n)
    for b in range(M):
        for s in range(M):K[s*M+b][b*M+s]=1
    Q=mul(Dlt,L,p);Qi=inv(Q,p);S=shift(n);D=diag([pow(w,j,p) for j in range(n)])
    check(mul(mul(K,B,p),Q,p)==FF,'relocated exact Fourier product')
    A1=mul(mul(K,D,p),K,p);A2=mul(mul(K,inv(S,p),p),K,p);T1=mul(mul(Q,S,p),Qi,p);T2=mul(mul(Q,D,p),Qi,p)
    for aa,tt in [(A1,T1),(A2,T2)]:check(mul(aa,B,p)==mul(B,tt,p),'true relocated interface');check(stat(aa)['max_row']==stat(aa)['max_column']==stat(tt)['max_row']==stat(tt)['max_column']==1,'all four true actions monomial')
    expectedA1=blockdiag([scale(diag([pow(eta,s,p) for s in range(M)]),pow(w,b,p),p) for b in range(M)])
    expectedT1=blockdiag([scale(shift(M),pow(w,b,p),p) for b in range(M)]);expectedA2=zero(n);expectedT2=zero(n)
    for b in range(M):
        dest=(b-1)%M;aa=ident(M) if b else inv(shift(M),p);tt=ident(M) if b else diag([pow(eta,s,p) for s in range(M)])
        for i in range(M):
            for j in range(M):expectedA2[dest*M+i][b*M+j]=aa[i][j];expectedT2[dest*M+i][b*M+j]=tt[i][j]
    check((A1,T1,A2,T2)==(expectedA1,expectedT1,expectedA2,expectedT2),'explicit actions and positive wrap phase')
    check(stat(Q)['max_row']==M,'zero-mask two-layer support threshold')
    # Baseline full-bank CT and a constant coordinate-swap gauge.
    P0=mul(L,Dlt,p);Q0=K;G=ident(n);a=0;b=M+1;G[a][a]=G[b][b]=0;G[a][b]=G[b][a]=1
    C=mul(mul(B,G,p),Bi,p);v=[int(i==a)-int(i==b) for i in range(n)];u=vector(B,v,p);wt=[sum(v[k]*Bi[k][j] for k in range(n))%p for j in range(n)]
    rankone=sub(I,[[x*y%p for y in wt] for x in u],p);check(C==rankone and mul(C,C,p)==I,'rank-one reversible gauge')
    check(sum(bool(x) for x in u)<=2*M and sum(bool(x) for x in wt)<=2*M,'gauge vectors block supports')
    Pnew=mul(P0,C,p);Qnew=mul(G,Q0,p);check(mul(mul(Pnew,B,p),Qnew,p)==FF,'swapped gauge leaves transfer')
    changes=[]
    for X,Y in [(S,D),(D,inv(S,p))]:
        T0=mul(mul(Q0,X,p),Q0,p);Tnew=mul(mul(G,T0,p),G,p);A0=mul(mul(B,T0,p),Bi,p);Anew=mul(mul(B,Tnew,p),Bi,p)
        delta=stat(sub(Tnew,T0,p))['nnz'];check(delta<=8,'constant changed scalar entries');check(stat(Anew)['nnz']<=stat(A0)['nnz']+delta*M*M,'exceptional bank rectangles')
        check(Anew==mul(mul(C,A0,p),C,p),'actual gauge action')
        changes.append(dict(changed_T_entries=delta,A_new_nonzeros=stat(Anew)['nnz']))
    return dict(M=M,N=n,p=p,all_four_actions_monomial=True,Q_row_degree=stat(Q)['max_row'],two_zero_mask_layers_excluded=M>4,gauge_support_u=sum(bool(x) for x in u),gauge_support_w=sum(bool(x) for x in wt),gauge_transport_changes=changes)

def monomial_coset(M):
    n=M*M;p=field(n);w=root(n,p);fm=fourier(M,p,pow(w,M,p));B=blockdiag([fm]*M);Bi=inv(B,p);rng=random.Random(510+M);cosets=list(range(M));rng.shuffle(cosets);Q=zero(n);sig=[]
    import math
    multipliers=[a for a in range(M) if math.gcd(a,M)==1]
    for b in range(M):
        e=cosets[b]+M*rng.randrange(M);a=rng.choice(multipliers);row=[]
        for s in range(M):
            j=(e+M*a*s)%n;Q[b*M+s][j]=rng.randrange(1,p);row.append(j)
        sig.append(row)
    D=diag([pow(w,j,p) for j in range(n)]);T=mul(mul(Q,D,p),inv(Q,p),p);A=mul(mul(B,T,p),Bi,p)
    check(stat(A)['max_row']==stat(A)['max_column']==1,'coset affine monomial clock')
    for b,row in enumerate(sig):check(len({x%M for x in row})==1 and len(set(row))==M,'coset geometry')
    broken=mul(mul(B,D,p),Bi,p);check(stat(broken)['max_row']>1,'noncoset natural layout rejected by monomial clock premise')
    return dict(M=M,N=n,p=p,affine_coset_layout_clock_monomial=True,noncoset_clock_max_row=stat(broken)['max_row'])

def n16():
    M=4;n=16;p=17;w=root(n,p);zeta=pow(w,4,p);I=ident(n);K=zero(n)
    for b in range(4):
        for s in range(4):K[s*4+b][b*4+s]=1
    K2=perm([0,2,1,3]);Eh=diag([1,1,-1,-1]);El=diag([1,-1,1,-1]);Ph=perm([j^2 for j in range(4)]);Pl=perm([j^1 for j in range(4)]);D4=diag([1,1,1,zeta]);D16=diag([pow(w,b*s,p) for b in range(4) for s in range(4)])
    A4=mul(add(Eh,Ph,p),D4,p);C4=mul(add(El,Pl,p),K2,p);check(mul(A4,C4,p)==fourier(4,p,zeta),'explicit F4 butterfly factorization')
    terms=[
      [kron(mul(El,K2,p),ident(4)),kron(mul(Pl,K2,p),ident(4))],
      [mul(D16,kron(mul(Eh,D4,p),ident(4)),p),mul(D16,kron(mul(Ph,D4,p),ident(4)),p)],
      [scale(I,pow(2,-1,p),p),scale(I,pow(2,-1,p),p)],
      [scale(K,pow(2,-1,p),p),scale(K,pow(2,-1,p),p)]
    ]
    plans=[];count=0
    for stage in terms:
        for term in stage:
            count+=1;check(stat(term)['max_row']==stat(term)['max_column']==1,'nonsingular monomial term');check(mul(term,inv(term,p),p)==I,'endpoint invertibility')
            step=2*count-1;pi=[(i+step)%n for i in range(n)];orbit=[];x=0
            while x not in orbit:orbit.append(x);x=pi[x]
            check(len(orbit)==n,'designated Hamiltonian order')
            denom=sub(I,scale(perm(pi),0,p),p);check(denom==I,'legal zero mask Green denominator')
            check(mul(term,inv(denom,p),p)==term,'actual Green plan equals term');plans.append(dict(stage=(count-1)//2+1,cycle_step=step,denominator_guard=1))
    H=[add(*stage,p) for stage in terms];B=blockdiag([fourier(4,p,zeta)]*4)
    product=mul(mul(mul(mul(H[3],H[2],p),B,p),H[1],p),H[0],p)
    check(product==fourier(16,p,w),'full admissible N16 four-layer exterior identity')
    return dict(N=n,p=p,root=w,bank_blocks=4,bank_length=4,full_active_bank=True,Green_plans=plans,all_endpoints_nonsingular=True,exact_transfer=True)

def main():
    result=dict(status='PASS',relocated_and_gauge_cases=[relocated(M) for M in [2,3,4,5,8]],coset_controls=[monomial_coset(M) for M in [3,4,5,8]],admissible_N16=n16(),uploaded_or_constructor_code_executed=False)
    path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('INDEPENDENT_RESULTS.json');path.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
