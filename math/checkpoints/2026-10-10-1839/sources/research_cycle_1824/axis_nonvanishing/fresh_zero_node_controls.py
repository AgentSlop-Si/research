#!/usr/bin/env python3
"""Fresh exact finite-field controls; no predecessor program is imported or run."""
import hashlib
import json
from pathlib import Path
from random import Random

ROOT = Path(__file__).resolve().parent
PAIRS = [(23,4),(31,5),(39,6),(47,7),(55,8),(63,9),(71,10),(79,11),(87,12),(95,13),(103,14),(111,15)]


def prime(n):
    if n < 2: return False
    j = 2
    while j*j <= n:
        if n % j == 0: return False
        j += 1
    return True


def prime_factors(n):
    out=[]; j=2
    while j*j<=n:
        if n%j==0:
            out.append(j)
            while n%j==0: n//=j
        j+=1
    if n>1: out.append(n)
    return out


def field(N):
    for k in range(1,201):
        p=k*N+1
        if not prime(p): continue
        for a in range(2,p):
            q=pow(a,k,p)
            if pow(q,N,p)==1 and all(pow(q,N//l,p)!=1 for l in prime_factors(N)):
                return p,q
    raise RuntimeError('Bounded field search exhausted')


def trim(a):
    a=list(a)
    while len(a)>1 and a[-1]==0: a.pop()
    return a


def poly_mul(a,b,p):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[i+j]=(c[i+j]+x*y)%p
    return trim(c)


def poly_div(a,b,p):
    a=trim(a); b=trim(b)
    if b==[0]: raise ZeroDivisionError
    q=[0]*max(1,len(a)-len(b)+1); bi=pow(b[-1],-1,p)
    while a!=[0] and len(a)>=len(b):
        s=len(a)-len(b); v=a[-1]*bi%p; q[s]=v
        for j,bj in enumerate(b): a[s+j]=(a[s+j]-v*bj)%p
        a=trim(a)
    return trim(q),a


def gcd(a,b,p):
    a=trim(a); b=trim(b)
    while b!=[0]: a,b=b,poly_div(a,b,p)[1]
    if a==[0]: return a
    return [(v*pow(a[-1],-1,p))%p for v in a]


def derivative(a,p): return trim([(i*a[i])%p for i in range(1,len(a))] or [0])
def evaluate(a,x,p):
    y=0
    for v in reversed(a): y=(y*x+v)%p
    return y


def rref(A,p,ncoef=None):
    B=[[v%p for v in row] for row in A]
    n=len(B[0]) if B else ncoef
    limit=n if ncoef is None else ncoef
    row=0; piv=[]; det=1
    for col in range(limit):
        k=next((k for k in range(row,len(B)) if B[k][col]),None)
        if k is None: continue
        if k!=row: B[row],B[k]=B[k],B[row]; det=-det%p
        v=B[row][col]; det=det*v%p; iv=pow(v,-1,p)
        B[row]=[x*iv%p for x in B[row]]
        for j in range(len(B)):
            if j==row or not B[j][col]: continue
            v=B[j][col]
            B[j]=[(x-v*y)%p for x,y in zip(B[j],B[row])]
        piv.append(col); row+=1
        if row==len(B): break
    return B,piv,det


def nullspace(A,p,n):
    B,piv,_=rref(A,p,n)
    free=[j for j in range(n) if j not in piv]
    basis=[]
    for f in free:
        v=[0]*n; v[f]=1
        for i,c in enumerate(piv): v[c]=-B[i][f]%p
        basis.append(v)
    return basis


def affine_monic(A,p,n,zero_constant):
    rows=[list(row)+[0] for row in A]
    if zero_constant: rows.append([1]+[0]*(n-1)+[0])
    rows.append([0]*(n-1)+[1,1])
    B,piv,_=rref(rows,p,n)
    if any(all(x==0 for x in row[:n]) and row[n] for row in B):
        raise AssertionError('Monic slice empty')
    base=[0]*n
    for i,c in enumerate(piv): base[c]=B[i][n]
    basis=[]
    for f in range(n):
        if f in piv: continue
        v=[0]*n; v[f]=1
        for i,c in enumerate(piv): v[c]=-B[i][f]%p
        basis.append(v)
    return base,basis


def sample(base,basis,p,rng):
    coeff=[rng.randrange(p) for _ in basis]
    v=list(base)
    for c,b in zip(coeff,basis): v=[(x+c*y)%p for x,y in zip(v,b)]
    return v,coeff


def envelope(N,d,p,q):
    m=N-d; h=pow(4,-1,N); rho=pow(q,pow(2,-1,N),p)
    D=[1]
    for j in range(2,d): D=poly_mul(D,[1,-pow(q,j,p)%p],p)
    Dval=[evaluate(D,pow(q,k,p),p) for k in range(m+1)]
    assert all(Dval)
    chirp=[pow(q,h*k*k,p) for k in range(m+1)]
    E=[]
    for j in range(3*d-6):
        E.append([chirp[k]*pow(rho,j*k,p)*pow(Dval[k],-1,p)%p for k in range(m+1)])
    for j in range(d-1):
        E.append([pow(q,j*k,p)*pow(Dval[k],-1,p)%p for k in range(m+1)])
    return E,D


def gaussian_table(N,q,p):
    T=[[1]]
    for n in range(1,N):
        row=[1]+[0]*(n-1)+[1]
        for k in range(1,n):
            row[k]=(T[n-1][k-1]+pow(q,k,p)*T[n-1][k])%p
        T.append(row)
    return T


def recurrence(N,d,p,q):
    m=N-d; h=pow(4,-1,N)
    plus=gaussian_table(N,q,p); minus=gaussian_table(N,pow(q,-1,p),p)
    def G(eps,delta,a,b):
        r=eps*a%N; ell=delta*b%N
        if r+ell>N-1: return 0
        return (plus if eps*delta==1 else minus)[r+ell][ell]
    rows=[]; labels=[]
    for b in range(1,d-1):
        T=pow(G(-1,1,N-b,b),-1,p)
        for a in range(1,d-b):
            row=[]
            for k in range(m+1):
                s=a+k
                val=(pow(q,h*(s+b)**2,p)-T*G(-1,1,s,b))*pow(G(1,1,s,b),-1,p)%p
                row.append(val)
            rows.append(row); labels.append([a,b])
    return rows,labels


def axis(g,N,p):
    m=len(g)-1
    rem=[]; v=[1]+[0]*(m-1)
    for j in range(N):
        rem.append(list(v))
        lead=v[-1]
        v=[(x-lead*c)%p for x,c in zip([0]+v[:-1],g[:-1])]
    X=[rem[a]+[1]+rem[(-a)%N] for a in range(N)]
    _,piv,det=rref(X,p)
    return {'rank':len(piv),'pivot_columns':piv,'pivot_minor_determinant':det if len(piv)==N else None}


def common_gcd(basis,p):
    out=[0]
    for b in basis: out=gcd(out,b,p)
    return out


def run_pair(N,d):
    p,q=field(N); m=N-d; E,D=envelope(N,d,p,q)
    _,epiv,edet=rref(E,p)
    U=nullspace(E,p,m+1)
    d0=[1]+[0]*m; d1=[0,1]+[0]*(m-1); dm=[0]*m+[1]
    U0=nullspace(E+[d0],p,m+1)
    assert len(epiv)==4*d-7
    assert len(rref(E+[d0,d1,dm],p)[1])==len(epiv)+3
    assert common_gcd(U,p)==[p-1,1]
    assert common_gcd(U0,p)==[0,p-1,1]
    A,labels=recurrence(N,d,p,q)
    assert all(sum(x*y for x,y in zip(a,u))%p==0 for a in A for u in U)
    assert all(sum(u)%p==0 for u in U)
    assert any(evaluate(derivative(u,p),1,p) for u in U0)
    base0,basis0=affine_monic(E,p,m+1,True)
    base1,basis1=affine_monic(E,p,m+1,False)
    rng=Random(20261010+1000*N+d)
    zero=None
    for trial in range(100):
        g,c=sample(base0,basis0,p,rng)
        f,rem=poly_div(g,[0,p-1,1],p)
        assert rem==[0]
        if not f[0] or gcd(f,list(reversed(f)),p)!=[1]: continue
        ax=axis(g,N,p)
        assert ax['rank']==N
        zero={'trial':trial,'affine_parameters':c,'g':g,'f':f,'residual_reciprocal_gcd':[1],
              'residual_derivative_gcd':gcd(f,derivative(f,p),p),'axis':ax}
        break
    assert zero is not None
    legal=None
    for trial in range(100):
        g,c=sample(base1,basis1,p,rng)
        if not g[0] or gcd(g,derivative(g,p),p)!=[1]: continue
        ax=axis(g,N,p)
        if ax['rank']!=N: continue
        legal={'trial':trial,'affine_parameters':c,'g':g,'constant':g[0],
               'derivative_gcd':[1],'axis':ax}
        break
    assert legal is not None
    print(f'N={N}, d={d}: envelope rank {len(epiv)}, zero and legal axis rank {N}',flush=True)
    return {'N':N,'d':d,'m':m,'p':p,'q':q,'threshold':8*d-10,
            'envelope_rows':E,'envelope_rank':len(epiv),'envelope_pivot_columns':epiv,
            'envelope_pivot_minor_determinant':edet,'D_coefficients':D,
            'recurrence_rows':A,'recurrence_row_labels':labels,
            'kernel_dimension':len(U),'kernel_basis':U,'zero_constant_kernel_basis':U0,
            'kernel_gcd':[p-1,1],'zero_constant_kernel_gcd':[0,p-1,1],
            'zero_constant_affine_base':base0,'zero_constant_affine_basis':basis0,
            'legal_affine_base':base1,'legal_affine_basis':basis1,
            'zero_constant_witness':zero,'legal_witness':legal,
            'all_checks_passed':True}


def main():
    result={'status':'pass','arithmetic':'exact prime-field arithmetic',
            'scope':'Bounded fresh controls; not a substitute for the uniform characteristic-zero proof.',
            'no_predecessor_program_imported_or_run':True,
            'pairs':[run_pair(N,d) for N,d in PAIRS]}
    out=ROOT/'FRESH_ZERO_NODE_CONTROLS.json'
    out.write_text(json.dumps(result,indent=2)+'\n')
    print('Wrote',out)

if __name__=='__main__': main()
