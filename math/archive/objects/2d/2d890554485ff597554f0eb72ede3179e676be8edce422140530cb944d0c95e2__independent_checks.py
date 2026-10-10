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

def scan(order,weights,c,v,p):
    # Solve y_i - c*w_i*y_pi(i)=v_i by scalar cycle closure.
    prod=1;acc=0
    for i in order:
        acc=(acc+prod*v[i])%p;prod=prod*c*weights[i]%p
    if prod==1:raise ValueError('resonant weighted cycle')
    y=[0]*len(order);y[order[0]]=acc*pow(1-prod,-1,p)%p
    for k in range(len(order)-1,0,-1):
        i=order[k];nxt=order[(k+1)%len(order)];y[i]=(v[i]+c*weights[i]*y[nxt])%p
    return y

def cayley_apply(order,w,c,v,p): return [(2*x-y)%p for x,y in zip(scan(order,w,c,v,p),v)]
def setup(n,p,kind):
    rng=random.Random(712*n+len(kind));order=list(range(n))
    if kind=='scrambled':rng.shuffle(order)
    weights=[rng.randrange(1,p) for _ in range(n)]
    if kind=='zero_edge':weights[n//2]=0
    if kind=='zero_operator':weights=[0]*n
    if kind=='seed':
        weights=[1]*n;weights[0]=3;weights[-1]=3*pow(5,-1,p)%p
    W=zero(n);parity=[0]*n
    for k,i in enumerate(order):W[i][order[(k+1)%n]]=weights[i];parity[i]=(-1)**k%p
    rho=1
    for w in weights:rho=rho*w%p
    if kind=='seed':a,b,l=0,1,2
    else:
        valid=[c for c in range(1,p) if (1-pow(c,n,p)*rho)%p]
        a,b=valid[0],valid[1];l=2
        if kind=='equal_cayley':b=a
        if kind=='opposite_cayley':b=-a%p
    return order,weights,W,diag(parity),rho,a,b,l

def check_case(n,p,kind):
    order,w,W,E,rho,a,b,l=setup(n,p,kind);I=ident(n)
    check(mul(mul(E,W,p),E,p)==scale(W,-1,p),'anticommutation')
    check(powmat(W,n,p)==scale(I,rho,p),'weighted cycle closure')
    G_a=inv(sub(I,scale(W,a,p),p),p);G_b=inv(sub(I,scale(W,b,p),p),p)
    Ca=sub(scale(G_a,2,p),I,p);Cb=sub(scale(G_b,2,p),I,p)
    check(mul(mul(E,Ca,p),E,p)==inv(Ca,p),'Cayley reciprocal')
    A=Ca;B=scale(mul(Cb,E,p),l,p);K=mul(B,A,p);H=sub(I,K,p);J=sub(I,mul(A,B,p),p)
    check(mul(K,K,p)==scale(I,l*l,p),'quadratic closure')
    scalar=all(K[i][j]==(K[0][0] if i==j else 0) for i in range(n) for j in range(n))
    check(not scalar,'exact degree two')
    T=mul(inv(H,p),B,p);den=pow(1-l*l,-1,p)
    formula=scale(add(scale(mul(Cb,E,p),l,p),scale(inv(Ca,p),l*l,p),p),den,p)
    check(T==formula,'oriented closed transfer')
    P=mul(sub(I,scale(W,b,p),p),add(I,scale(W,a,p),p),p)
    numerator=add(scale(mul(mul(add(I,scale(W,a,p),p),add(I,scale(W,b,p),p),p),E,p),l,p),scale(mul(sub(I,scale(W,b,p),p),sub(I,scale(W,a,p),p),p),l*l,p),p)
    PT=mul(P,T,p);check(PT==scale(numerator,den,p),'sparse denominator equation')
    bound=2 if a==0 or b==0 else 3
    check(stat(P)['max_row']<=bound and stat(PT)['max_row']<=bound,'row support gate')
    s=shift(n);omega=root(n,p);D=diag([pow(omega,j,p) for j in range(n)])
    residual=sub(mul(D,T,p),mul(T,s,p),p)
    C1=sub(mul(mul(H,D,p),B,p),mul(mul(B,s,p),J,p),p)
    check(C1==mul(mul(H,residual,p),J,p),'cubic covariance factorization')
    gate=stat(P)['max_row']*stat(PT)['max_row']
    if kind in ['equal_cayley','opposite_cayley']:check(gate<=6,'cancellation-branch bound')
    if n>gate:check(any(any(row) for row in residual),'structural covariance exclusion')
    seed=vector(T,[1]+[0]*(n-1),p)==[1]*n
    if kind=='seed':check(seed,'uniform Fourier seed')
    for j in range(n):
        x=[int(i==j) for i in range(n)]
        aa=cayley_apply(order,w,a,x,p)
        bb=[l*y%p for y in cayley_apply(order,w,b,vector(E,x,p),p)]
        check(aa==vector(A,x,p) and bb==vector(B,x,p),'scan basis map')
        ab=cayley_apply(order,w,a,bb,p)
        bab=[l*y%p for y in cayley_apply(order,w,b,vector(E,ab,p),p)]
        out=[(u+v)*den%p for u,v in zip(bb,bab)]
        check(out==vector(T,x,p),'three map evaluator')
    return dict(N=n,p=p,kind=kind,parameters=dict(a=a,b=b,lambda_=l,rho=rho),exact_loop_degree=2,seed_passes=seed,covariance_passes=not any(any(row) for row in residual),P=stat(P),PT=stat(PT),basis_vectors_checked=n)

def guards():
    n=6;p=241;order,w,W,E,rho,a,b,l=setup(n,p,'natural');I=ident(n)
    Ca=mul(add(I,scale(W,a,p),p),inv(sub(I,scale(W,a,p),p),p),p)
    Cb=mul(add(I,scale(W,b,p),p),inv(sub(I,scale(W,b,p),p),p),p)
    ranks=[]
    for lam in [1,p-1]:
        K=scale(mul(mul(Cb,E,p),Ca,p),lam,p)
        r=rank(sub(I,K,p),p);check(r<n,'lambda resonance rejected');ranks.append(r)
    try:scan(list(range(n)),[1]*n,1,[1]*n,p)
    except ValueError:resonance=True
    else:resonance=False
    check(resonance,'Green guard rejected')
    # Odd natural cycle cannot close an alternating parity assignment.
    nn=5;WW=trans(shift(nn));EE=diag([(-1)**i%p for i in range(nn)])
    check(mul(mul(EE,WW,p),EE,p)!=scale(WW,-1,p),'odd-cycle parity control')
    return dict(N=n,p=p,lambda_plus_minus_one_H_ranks=ranks,green_resonance_rejected=resonance,odd_cycle_anticommutation_fails=True)

def main():
    cases=[check_case(n,241,kind) for n in [2,4,6,8,10,12,16,24] for kind in ['natural','scrambled','zero_edge','zero_operator','seed','equal_cayley','opposite_cayley']]
    result=dict(status='PASS',arithmetic='exact prime field F_241',cases=cases,number_cases=len(cases),basis_vectors_checked=sum(c['basis_vectors_checked'] for c in cases),output_entries_checked=3*sum(c['N']**2 for c in cases),guard_controls=guards(),uploaded_or_constructor_code_executed=False)
    target=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('INDEPENDENT_RESULTS.json')
    target.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
