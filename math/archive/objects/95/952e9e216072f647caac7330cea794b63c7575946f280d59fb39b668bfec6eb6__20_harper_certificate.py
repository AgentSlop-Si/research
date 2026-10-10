"""Phase 18: exact modular certificate for Fourier/Harper joint functional calculus.

N powers of two, 4 <= N <= 2**23.  All tests are in F_998244353,
with primitive Nth Fourier roots; proof over C is in THEOREM.md.
"""
from __future__ import annotations
import json
from math import isqrt

P = 998244353
GENERATOR = 3


def sqrt_mod(a:int, p:int=P)->int:
    # Tonelli-Shanks, p odd prime, no reliance on floating-point.
    a%=p
    if a==0:return 0
    assert pow(a,(p-1)//2,p)==1, 'not a quadratic residue'
    if p%4==3:return pow(a,(p+1)//4,p)
    q=p-1;s=0
    while q%2==0:
        q//=2;s+=1
    z=2
    while pow(z,(p-1)//2,p)!=p-1:z+=1
    c=pow(z,q,p);t=pow(a,q,p);r=pow(a,(q+1)//2,p);m=s
    while t!=1:
        i=1; t2=t*t%p
        while t2!=1:
            t2=t2*t2%p;i+=1
        b=pow(c,2**(m-i-1),p)
        r=r*b%p;t=t*b*b%p;c=b*b%p;m=i
    assert r*r%p==a
    return r


def root_n(n):
    assert n>=4 and (n&(n-1))==0 and (P-1)%n==0
    return pow(GENERATOR,-((P-1)//n),P)


def matvec_tridiag(diag,upper,v):
    n=len(diag)
    out=[0]*n
    for k in range(n):
        out[k]=diag[k]*v[k]%P
        if k>0:out[k]=(out[k]+upper[k-1]*v[k-1])%P
        if k+1<n:out[k]=(out[k]+upper[k]*v[k+1])%P
    return out


def rowstep(diag,upper,row):
    return matvec_tridiag(diag,upper,row)


def parity_basis(n,sgn,sqrt2):
    """Sparse columns for J=+1/-1 reflection subspaces, normalized mod P."""
    invsqrt2=pow(sqrt2,-1,P)
    half=n//2
    if sgn==1:
        cols=[{0:1}]
        cols.extend([{j:invsqrt2, n-j:invsqrt2} for j in range(1,half)])
        cols.append({half:1})
    else:
        cols=[{j:invsqrt2, n-j:(-invsqrt2)%P} for j in range(1,half)]
    return cols


def components(n):
    omega=root_n(n)
    sqrt2=sqrt_mod(2)
    sqrtn=sqrt_mod(n)
    pows=[pow(omega,j,P) for j in range(n)]
    invs=[pow(pows[j],-1,P) for j in range(n)]
    def component(sgn):
        cols=parity_basis(n,sgn,sqrt2)
        positions=list(range(n//2+1)) if sgn==1 else list(range(1,n//2))
        d=[(pows[j]+invs[j])%P for j in positions]
        off=([sqrt2]+[1]*(n//2-2)+[sqrt2]) if sgn==1 else [1]*(n//2-2)
        assert len(off)==len(d)-1
        v=[]
        for ca in cols:
            row=[]
            for cb in cols:
                z=sum(va*vb*pow(omega,(a*b)%n,P) for a,va in ca.items() for b,vb in cb.items())
                row.append(z*pow(sqrtn,-1,P)%P)
            v.append(row)
        return dict(sign=sgn,cols=cols,diag=d,off=off,F=v)
    return component(1), component(-1)


def reconstruct_polynomial(comp):
    """F=p(H) by cyclic Jacobi first-row upper triangular Krylov solve."""
    diag,off,F=comp['diag'],comp['off'],comp['F'];m=len(diag)
    rows=[]; row=[0]*m;row[0]=1
    for t in range(m):
        rows.append(row)
        row=rowstep(diag,off,row)
    coeff=[0]*m
    for j in range(m-1,-1,-1):
        rhs=(F[0][j]-sum(coeff[k]*rows[k][j] for k in range(j+1,m)))%P
        pivot=rows[j][j]
        assert pivot!=0
        coeff[j]=rhs*pow(pivot,-1,P)%P
    # Independent full matrix equality audit, testing each column against its F target.
    for k in range(m):
        b=[0]*m;b[k]=1
        pred=[0]*m
        for c in reversed(coeff):
            pred=matvec_tridiag(diag,off,pred)
            pred[k]=(pred[k]+c)%P
        target=[F[i][k] for i in range(m)]
        assert pred==target, (m,comp['sign'],k)
    return coeff


def null_eigenvector(comp):
    d=comp['diag'];off=comp['off'];m=len(d)
    v=[0]*m;v[0]=1
    for j in range(m-1):
        rhs=d[j]*v[j]
        if j>0:rhs+=off[j-1]*v[j-1]
        v[j+1]=(-rhs*pow(off[j],-1,P))%P
    assert matvec_tridiag(d,off,v)==[0]*m
    y=[sum(comp['F'][j][k]*v[k] for k in range(m))%P for j in range(m)]
    lam=y[0]
    assert lam!=0 and all(y[j]==lam*v[j]%P for j in range(m))
    assert lam*lam%P==(1 if comp['sign']==1 else P-1)
    return v,lam


def audit(n):
    even,odd=components(n)
    pe=reconstruct_polynomial(even)
    po=reconstruct_polynomial(odd)
    ve,le=null_eigenvector(even)
    vo,lo=null_eigenvector(odd)
    sqrtn=sqrt_mod(n)
    expected_even=pow(2*sqrtn,-1,P)
    assert pe[-1]==expected_even
    omega=root_n(n)
    # F_odd[0,-1] = (omega^(n/2-1)-omega^(-(n/2-1)))/sqrt(N)
    expected_odd=(omega**(n//2-1)-pow(omega,-(n//2-1),P))*pow(sqrtn,-1,P)%P
    assert po[-1]==expected_odd
    assert le!=lo
    return {
        'n':n,'field_prime':P,'root':omega,
        'even_dimension':len(pe),'odd_dimension':len(po),
        'even_polynomial_degree':len(pe)-1,'odd_polynomial_degree':len(po)-1,
        'even_top_coefficient_mod_p':pe[-1],
        'odd_top_coefficient_mod_p':po[-1],
        'even_zero_fourier_eigenvalue_mod_p':le,
        'odd_zero_fourier_eigenvalue_mod_p':lo,
        'exact_full_matrix_reconstruction':True,
        'exact_odd_even_zero_mode_certificate':True,
        'no_scalar_function_of_H':True
    }

if __name__=='__main__':
    print(json.dumps([audit(n) for n in (4,8,16,32,64,128)],indent=2))
