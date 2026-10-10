#!/usr/bin/env python3
"""Fresh independent arithmetic controls; imports no prior research programs."""
from pathlib import Path
from fractions import Fraction
import hashlib, json, math, random, time
BASE=Path(__file__).resolve().parent

def trim(a,p):
    a=[x%p for x in a]
    while a and a[-1]==0:a.pop()
    return a

def mul(a,b,p):
    c=[0]*(len(a)+len(b)-1) if a and b else []
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]=(c[i+j]+x*y)%p
    return trim(c,p)

def rem(a,b,p):
    a=trim(a,p); b=trim(b,p)
    assert b
    v=pow(b[-1],-1,p)
    while len(a)>=len(b):
        z=a[-1]*v%p; k=len(a)-len(b)
        for j,x in enumerate(b):a[k+j]=(a[k+j]-z*x)%p
        a=trim(a,p)
    return a

def gcd(a,b,p):
    while b:a,b=b,rem(a,b,p)
    return [(x*pow(a[-1],-1,p))%p for x in a] if a else []

def quotient(a,b,p):
    a=trim(a,p); b=trim(b,p); out=[0]*max(0,len(a)-len(b)+1)
    while len(a)>=len(b):
        k=len(a)-len(b); z=a[-1]*pow(b[-1],-1,p)%p;out[k]=z
        for j,x in enumerate(b):a[k+j]=(a[k+j]-z*x)%p
        a=trim(a,p)
    assert not a
    return trim(out,p)

def derivative(a,p):return trim([i*a[i] for i in range(1,len(a))],p)
def evalp(a,x,p):
    y=0
    for v in reversed(a):y=(y*x+v)%p
    return y

def rr(rows,p,n=None):
    a=[[v%p for v in r] for r in rows]; n=n if n is not None else (len(a[0]) if a else 0)
    piv=[]; r=0
    for j in range(n):
        i=next((i for i in range(r,len(a)) if a[i][j]),None)
        if i is None:continue
        a[r],a[i]=a[i],a[r]
        iv=pow(a[r][j],-1,p);a[r]=[(v*iv)%p for v in a[r]]
        for k in range(len(a)):
            if k!=r and a[k][j]:
                z=a[k][j];a[k]=[(v-z*w)%p for v,w in zip(a[k],a[r])]
        piv.append(j);r+=1
        if r==len(a):break
    return a,piv

def rank(rows,p,n=None):return len(rr(rows,p,n)[1])
def kernel(rows,p,n):
    a,piv=rr(rows,p,n);out=[]
    for j in range(n):
        if j in piv:continue
        v=[0]*n;v[j]=1
        for i,k in enumerate(piv):v[k]=-a[i][j]%p
        out.append(v)
    return out

def solve(rows,b,p,n):
    aug=[list(r)+[v] for r,v in zip(rows,b)];a,piv=rr(aug,p,n)
    assert all(any(r[:n]) or r[n]==0 for r in a)
    x=[0]*n
    for i,j in enumerate(piv):x[j]=a[i][n]
    assert all(sum(u*v for u,v in zip(r,x))%p==w%p for r,w in zip(rows,b))
    return x

def isprime(n):return n>=2 and all(n%v for v in range(2,math.isqrt(n)+1))
def factors(n):return [v for v in range(2,n+1) if n%v==0 and isprime(v)]
def field(N):
    p=N+1
    while not isprime(p):p+=N
    fs=factors(N)
    q=next(a for a in range(2,p) if pow(a,N,p)==1 and all(pow(a,N//r,p)!=1 for r in fs))
    return p,q

def moments(g,N,p):
    m=len(g)-1; out=[];v=[0]*m;v[0]=1
    for k in range(N):
        out.append(v);w=[0]+v[:-1];z=v[-1]
        for j in range(m):w[j]=(w[j]-z*g[j])%p
        v=w
    return out

def axis(g,N,p):
    ps=moments(g,N,p)
    return [ps[a]+[1]+ps[(-a)%N] for a in range(N)]

def qpascal(N,q,p):
    a=[[1]]
    for n in range(1,N):
        r=[1]*(n+1)
        for k in range(1,n):r[k]=(a[-1][k-1]+pow(q,k,p)*a[-1][k])%p
        a.append(r)
    return a

def physical_data(N,d,p,q):
    h=pow(4,-1,N); qp=qpascal(N,q,p);qm=qpascal(N,pow(q,-1,p),p)
    def G(a,b,e,s):
        r=(e*a)%N;l=(s*b)%N
        return 0 if r+l>=N else (qp if e*s==1 else qm)[r+l][l]
    vals={};A=[]
    for b in range(1,(N-1)//2+1):
        T=pow(G(N-b,b,-1,1),-1,p)
        v=[((pow(q,h*(a+b)*(a+b),p)-T*G(a,b,-1,1))*pow(G(a,b,1,1),-1,p))%p for a in range(1,N-b)]
        vals[b]=(T,v)
        if b<=d-2:
            for a in range(1,d-b):A.append(v[a-1:a+N-d])
    assert len(A)==(d-1)*(d-2)//2
    return A,vals,G

def check_physical(g,N,d,p,q,vals,G):
    m=N-d;ps=moments(g,N,p);h=pow(4,-1,N)
    for b,(T,v) in vals.items():
        l=min(m,len(v));u=solve(ps[1:l+1],v[:l],p,m)
        assert all(sum(x*y for x,y in zip(ps[a],u))%p==v[a-1] for a in range(1,N-b))
        target=[(pow(q,h*b*b,p)-T-sum(u[j]*ps[0][j] for j in range(m)))%p]
        for r in range(1,b):
            target.append((pow(q,h*(N-r+b)**2,p)-T*G(N-r,b,-1,1))*pow(G(N-r,b,-1,-1),-1,p)%p)
        z=solve(ps[:b],target,p,m)
        for a in range(N):
            ga=sum(x*y for x,y in zip(ps[a],u))%p
            gb=sum(x*y for x,y in zip(ps[-a%N],z))%p
            got=(ga*G(a,b,1,1)+gb*G(a,b,-1,-1)+T*G(a,b,-1,1))%p
            assert got==pow(q,h*(a+b)**2,p),(N,b,a,got)
        # Rebuild every reflected negative row explicitly, swapping both sign groups.
        for a in range(N):
            ga=sum(x*y for x,y in zip(ps[a],z))%p
            gb=sum(x*y for x,y in zip(ps[-a%N],u))%p
            got=(ga*G(a,N-b,1,1)+gb*G(a,N-b,-1,-1)+T*G(a,N-b,1,-1))%p
            assert got==pow(q,h*(a+N-b)**2,p),(N,N-b,a,got)
    X=axis(g,N,p)
    solve(X,[pow(q,h*a*a,p) for a in range(N)],p,2*m+1)
    return True

def sample_monic(basis,m,p,rng,predicate):
    for trial in range(10000):
        w=[rng.randrange(p) for _ in basis]
        g=[sum(c*v[j] for c,v in zip(w,basis))%p for j in range(m+1)]
        if not g[-1]:continue
        g=[x*pow(g[-1],-1,p)%p for x in g]
        if predicate(g):return g,trial+1
    raise AssertionError('No witness found')

def case(N,d):
    t0=time.time();m=N-d;p,q=field(N);h=pow(4,-1,N);rho=pow(q,pow(2,-1,N),p)
    D=[1]
    for j in range(2,d):D=mul(D,[1,-pow(q,j,p)],p)
    ds=[evalp(D,pow(q,k,p),p) for k in range(m+1)]
    assert all(ds)
    E=[]
    for j in range(3*d-6):E.append([pow(q,h*k*k,p)*pow(rho,j*k,p)*pow(ds[k],-1,p)%p for k in range(m+1)])
    for j in range(d-1):E.append([pow(q,j*k,p)*pow(ds[k],-1,p)%p for k in range(m+1)])
    re=rank(E,p);assert re==4*d-7
    V=kernel(E,p,m+1)
    c0=[1]+[0]*m;c1=[0,1]+[0]*(m-1);cm=[0]*m+[1]
    assert rank(E+[c0,c1,cm],p)==re+3
    V0=kernel(E+[c0],p,m+1)
    assert len(V)==N-5*d+8 and len(V0)==N-5*d+7
    fixed=[]
    for g in V:fixed=gcd(fixed,trim(g,p),p)
    fixed0=[]
    for g in V0:fixed0=gcd(fixed0,trim(g,p),p)
    assert fixed==[p-1,1] and fixed0==[0,p-1,1]
    assert rank(E+[c0,[k%p for k in range(m+1)]],p)==re+2
    # All finite evaluation functionals are tested over this finite field only.
    eval_good=True
    for x in range(1,p):
        vanishes=all(evalp(v,x,p)==0 for v in V0)
        assert vanishes==(x==1)
    assert rank([[(-v[1])%p,v[m]] for v in V0],p)==2
    A,vals,G=physical_data(N,d,p,q)
    assert rank(E+A,p)==re
    assert all(sum(a*b for a,b in zip(row,g))%p==0 for row in A for g in V)
    rng=random.Random(1830000+N*100+d)
    def zero_guard(g):
        if len(gcd(g,derivative(g,p),p))!=1:return False
        f=quotient(g,[0,p-1,1],p)
        return f[0]!=0 and len(gcd(f,list(reversed(f)),p))==1
    g0,n0=sample_monic(V0,m,p,rng,zero_guard)
    assert g0[0]==0 and rank(axis(g0,N,p),p)==N
    def legal_guard(g):
        return g[0]!=0 and len(gcd(g,derivative(g,p),p))==1 and rank(axis(g,N,p),p)==N
    g,n1=sample_monic(V,m,p,rng,legal_guard)
    assert evalp(g,1,p)==0
    assert check_physical(g,N,d,p,q,vals,G)
    return dict(N=N,d=d,m=m,p=p,q=q,envelope_rank=re,dim_V=len(V),dim_V0=len(V0),kernel_gcd=fixed,zero_slice_gcd=fixed0,sparse_functional_rank=3,endpoint_rank=2,physical_recurrence_rank=rank(A,p),zero_witness=g0,zero_witness_trials=n0,zero_axis_rank=N,legal_witness=g,legal_witness_trials=n1,legal_axis_rank=N,all_physical_rows_and_axis_verified=True,seconds=round(time.time()-t0,3))

def main():
    cases=[(N,(N+10)//8) for N in range(23,82,2)]+[(N,(N+10)//8) for N in [87,95,103,119,127,151]]
    out=[]
    for N,d in cases:
        r=case(N,d);out.append(r)
        print('PASS',N,d,r['seconds'],flush=True)
    result=dict(status='PASS',method='Independent enlarged-envelope construction, q-Pascal physical coefficients, exact modular row reduction; no inherited program execution/import.',cases=out,limits='Finite controls support implementation and endpoints, not universal proof. Modular witness coefficients are not claimed to lift without an exact characteristic-zero definition.')
    (BASE/'INDEPENDENT_EXACT_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n')

def determinant(rows,p):
    a=[r[:] for r in rows];n=len(a);z=1
    assert all(len(r)==n for r in a)
    for j in range(n):
        k=next((k for k in range(j,n) if a[k][j]%p),None)
        if k is None:return 0
        if k!=j:a[k],a[j]=a[j],a[k];z=-z
        v=a[j][j]%p;z=z*v%p;iv=pow(v,-1,p)
        for k in range(j+1,n):
            c=a[k][j]*iv%p
            for l in range(j,n):a[k][l]=(a[k][l]-c*a[j][l])%p
    return z%p

def author_records():
    source=Path('research_cycle_1824/axis_nonvanishing/FRESH_ZERO_NODE_CONTROLS.json')
    obj=json.loads(source.read_text());records=[]
    for r in obj['pairs']:
        N,d,m,p,q=(r[k] for k in ['N','d','m','p','q'])
        assert isprime(p) and p>N and pow(q,N,p)==1 and all(pow(q,N//s,p)!=1 for s in factors(N))
        assert N-d==m and r['threshold']==8*d-10 and N>=r['threshold']
        h=pow(4,-1,N);rho=pow(q,pow(2,-1,N),p);D=[1]
        for j in range(2,d):D=mul(D,[1,-pow(q,j,p)],p)
        ds=[evalp(D,pow(q,k,p),p) for k in range(m+1)];assert all(ds)
        E=[[pow(q,h*k*k,p)*pow(rho,j*k,p)*pow(ds[k],-1,p)%p for k in range(m+1)] for j in range(3*d-6)]
        E += [[pow(q,j*k,p)*pow(ds[k],-1,p)%p for k in range(m+1)] for j in range(d-1)]
        assert E==r['envelope_rows'] and D==r['D_coefficients']
        R,piv=rr(E,p);assert len(piv)==r['envelope_rank'] and piv==r['envelope_pivot_columns']
        assert determinant([[v[j] for j in piv] for v in E],p)==r['envelope_pivot_minor_determinant']
        A,vals,G=physical_data(N,d,p,q);assert A==r['recurrence_rows']
        assert r['recurrence_row_labels']==[[a,b] for b in range(1,d-1) for a in range(1,d-b)]
        V=r['kernel_basis'];V0=r['zero_constant_kernel_basis']
        assert len(V)==r['kernel_dimension']==m+1-len(piv) and rank(V,p)==len(V)
        assert len(V0)==len(V)-1 and rank(V0,p)==len(V0)
        for B in [V,V0]:assert all(sum(x*y for x,y in zip(e,v))%p==0 for e in E for v in B)
        assert all(v[0]==0 for v in V0)
        for B,key,want in [(V,'kernel_gcd',[p-1,1]),(V0,'zero_constant_kernel_gcd',[0,p-1,1])]:
            z=[]
            for v in B:z=gcd(z,trim(v,p),p)
            assert z==r[key]==want
        assert rank(E+[[1]+[0]*m,[0,1]+[0]*(m-1),[0]*m+[1]],p)==len(piv)+3
        for prefix in ['zero_constant','legal']:
            base=r[prefix+'_affine_base'];B=r[prefix+'_affine_basis'];w=r[prefix+'_witness'];g=w['g']
            assert base[-1]==1 and all(v[-1]==0 for v in B)
            assert rank(B,p)==len(B)==len(V)-(2 if prefix=='zero_constant' else 1)
            assert all(sum(x*y for x,y in zip(e,v))%p==0 for e in E for v in [base]+B)
            assert g==[(base[j]+sum(c*v[j] for c,v in zip(w['affine_parameters'],B)))%p for j in range(m+1)]
            if prefix=='zero_constant':
                assert g[0]==0 and base[0]==0 and all(v[0]==0 for v in B)
                f=quotient(g,[0,p-1,1],p);assert f==w['f'] and f[0] and evalp(f,1,p)
                assert gcd(f,list(reversed(f)),p)==w['residual_reciprocal_gcd']==[1]
                assert gcd(f,derivative(f,p),p)==w['residual_derivative_gcd']==[1]
            else:
                assert g[0]==w['constant']!=0 and gcd(g,derivative(g,p),p)==w['derivative_gcd']==[1]
                check_physical(g,N,d,p,q,vals,G)
            X=axis(g,N,p);pivx=rr(X,p)[1];assert len(pivx)==N==w['axis']['rank']
            assert pivx==w['axis']['pivot_columns']
            assert determinant([[v[j] for j in pivx] for v in X],p)==w['axis']['pivot_minor_determinant']
        records.append(dict(N=N,d=d,p=p,q=q,status='PASS'))
        print('AUTHOR DATA PASS',N,d,flush=True)
    out=dict(status='PASS',source=str(source),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),cases=records,coverage='All recorded matrices, field/order claims, ranks, selected determinants, bases, affine parameterizations, gcds, witnesses and axis minors independently reconstructed; every legal witness additionally checked on all physical rows.')
    (BASE/'AUTHOR_DATA_RECHECK.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':
    main()
    author_records()
