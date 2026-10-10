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

def nonzero(a):return any(any(row) for row in a)
def cayley(W,c,p):
    I=ident(len(W));return mul(add(I,scale(W,c,p),p),inv(sub(I,scale(W,c,p),p),p),p)
def cut(a,k):return [row[k:] for row in a[:k]]

def cycle_control(n,p):
    I=ident(n);P=trans(shift(n));sigma=list(range(n));sigma[2],sigma[4]=sigma[4],sigma[2]
    M=zero(n)
    for i,j in enumerate(sigma):M[i][j]=1
    Q=mul(mul(M,P,p),M,p);J=diag([(-1)**i%p for i in range(n)])
    check(nonzero(sub(mul(P,Q,p),mul(Q,P,p),p)),'noncommuting row shifts')
    check(mul(P,Q,p)[0][4]==1 and mul(Q,P,p)[0][2]==1,'explicit noncommuting witness')
    for W in [P,Q]:check(mul(mul(J,W,p),J,p)==scale(W,-1,p),'shared parity')
    check(pow(2,n,p)!=1 and pow(3,n,p)!=1,'denominator guard')
    U=cayley(P,2,p);Z=cayley(Q,3,p);Ui=inv(U,p);Zi=inv(Z,p)
    check(nonzero(sub(mul(U,Z,p),mul(Z,U,p),p)),'Cayley noncommutation')
    check(P==scale(mul(sub(U,I,p),inv(add(U,I,p),p),p),pow(2,-1,p),p),'inverse Cayley')
    directK=scale(mul(mul(Z,J,p),U,p),2,p)
    commutator=mul(mul(mul(Z,Ui,p),Zi,p),U,p)
    check(mul(directK,directK,p)==scale(commutator,4,p),'direct commutator formula')
    check(mul(directK,directK,p)!=scale(I,4,p),'direct closure rejection')
    C=mul(U,Z,p);Ci=mul(Zi,Ui,p);A=U;K=scale(mul(mul(C,J,p),Ci,p),2,p);B=mul(K,Ui,p)
    check(mul(B,A,p)==K and mul(K,K,p)==scale(I,4,p),'forced closure')
    Delta=scale(add(scale(J,2,p),scale(I,4,p),p),pow(-3,-1,p),p)
    T=mul(inv(sub(I,K,p),p),B,p);factored=mul(mul(mul(C,Delta,p),Ci,p),Ui,p)
    check(T==factored,'constant-product equivalence')
    horner=scale(add(B,mul(mul(B,A,p),B,p),p),pow(-3,-1,p),p)
    check(T==horner,'A/B-only evaluator')
    R=Ui;reconstructedA=inv(R,p);reconstructedB=mul(K,R,p)
    check(reconstructedA==A and reconstructedB==B,'converse construction')
    ranks=None
    if n>=10:
        k=n//2
        factors=[U,Z,Delta,Zi,Ui,Ui]
        rr=[rank(cut(f,k),p) for f in factors]
        check(all(r<=1 for r in rr),'factor cut bound')
        tr=rank(cut(T,k),p);check(tr<=5,'transfer cut bound')
        F=fourier(n,p);fr=rank(cut(F,k),p);check(fr==k,'Fourier Vandermonde cut rank')
        if n>=12:check(tr<fr and T!=F,'Fourier rejection')
        ranks=dict(factors=rr,transfer=tr,Fourier=fr)
    return dict(N=n,p=p,denominator_guards=True,Cayley_noncommuting=True,direct_ansatz_closure=False,forced_conjugation_closure=True,cut_ranks=ranks)

def general_involution(n,p,kind):
    I=ident(n);J=diag([1 if i%2==0 else p-1 for i in range(n)])
    if kind=='non_diagonal':
        J=ident(n);J[0][0]=J[1][1]=0;J[0][1]=J[1][0]=1
    if kind=='scalar':J=I
    # Fixed triangular invertibles, no Fourier data in their construction.
    C=ident(n);A=ident(n)
    for i in range(n):
        for j in range(i+1,n):C[i][j]=(i+j+1)%p;A[j][i]=(2*i+j+1)%p
    Ci=inv(C,p);Ai=inv(A,p);K=scale(mul(mul(C,J,p),Ci,p),2,p);B=mul(K,Ai,p)
    Delta=scale(add(scale(J,2,p),scale(I,4,p),p),pow(-3,-1,p),p)
    T=mul(inv(sub(I,K,p),p),B,p)
    check(T==mul(mul(mul(C,Delta,p),Ci,p),Ai,p),'general involution factorization')
    check(mul(T,A,p)==mul(mul(C,Delta,p),Ci,p),'target equation')
    check(A==mul(mul(mul(inv(T,p),C,p),Delta,p),Ci,p),'target equation inverse')
    if kind=='non_diagonal':check(any(Delta[i][j] for i in range(n) for j in range(n) if i!=j),'Delta not diagonal')
    scalar=all(K[i][j]==(K[0][0] if i==j else 0) for i in range(n) for j in range(n))
    check(scalar==(kind=='scalar'),'exact degree qualification')
    return dict(N=n,p=p,kind=kind,loop_minimal_polynomial_degree=1 if scalar else 2,Delta_is_diagonal=not any(Delta[i][j] for i in range(n) for j in range(n) if i!=j))

def main():
    cases=[cycle_control(n,65521) for n in [6,8,10,12,16,24,30]]
    general=[general_involution(3,17,kind) for kind in ['diagonal','non_diagonal','scalar']]
    result=dict(status='PASS',noncommuting_cases=cases,general_involution_controls=general,number_cases=len(cases)+len(general),uploaded_or_constructor_code_executed=False)
    target=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('INDEPENDENT_RESULTS.json')
    target.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
