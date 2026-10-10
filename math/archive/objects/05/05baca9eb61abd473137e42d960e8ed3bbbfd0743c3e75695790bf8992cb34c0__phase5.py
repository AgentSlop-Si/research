"""Hero #17 phase 5: exact gauge-rescaling and cross-channel rank gates.

Exact finite-field experiments, no universal sub-FFT claim.
The full-input Fourier target is N=M*M with root omega of order N.
"""
from __future__ import annotations
from collections import defaultdict
from itertools import combinations
from math import gcd, lcm


def factors(n):
    z = []
    d = 2
    while d*d <= n:
        if n % d == 0:
            z.append(d)
            while n%d == 0:
                n //= d
        d += 1
    if n > 1:
        z.append(n)
    return z


def is_prime(n):
    if n < 2: return False
    for d in range(2, int(n**0.5)+1):
        if n%d == 0: return False
    return True


def field_for_m(m):
    n=m*m
    for k in range(1,1000):
        p=k*n+1
        if is_prime(p):
            for base in range(2,p):
                root=pow(base, (p-1)//n,p)
                if all(pow(root,n//q,p)!=1 for q in factors(n)):
                    return p, root
    raise RuntimeError('no field found')


def roots_table(p,w,n):
    roots=[1]*n
    for j in range(1,n):roots[j]=roots[j-1]*w%p
    if roots[-1]*w%p!=1:raise ValueError('not an Nth root')
    return roots


def dot(a,b,p):
    return sum(u*v for u,v in zip(a,b))%p


def matmul(a,b,p):
    if not a: return []
    rows=len(a);inner=len(b); cols=len(b[0])
    assert len(a[0])==inner
    return [[sum(a[i][k]*b[k][j] for k in range(inner))%p for j in range(cols)] for i in range(rows)]


def inv_mod(matrix,p):
    n=len(matrix)
    assert all(len(row)==n for row in matrix)
    a=[[v%p for v in row]+[int(i==j) for j in range(n)] for i,row in enumerate(matrix)]
    for c in range(n):
        pivot=next((i for i in range(c,n) if a[i][c]),None)
        if pivot is None:raise ValueError('singular matrix')
        a[c],a[pivot]=a[pivot],a[c]
        k=pow(a[c][c],-1,p)
        for j in range(c,2*n): a[c][j]=a[c][j]*k%p
        for i in range(n):
            if i==c:continue
            v=a[i][c]
            if v:
                for j in range(c,2*n):a[i][j]=(a[i][j]-v*a[c][j])%p
    return [row[n:] for row in a]


def rank_mod(matrix,p):
    if not matrix:return 0
    a=[[x%p for x in row] for row in matrix]
    rows=len(a);cols=len(a[0]);r=0
    for c in range(cols):
        z=next((i for i in range(r,rows) if a[i][c]),None)
        if z is None:continue
        a[r],a[z]=a[z],a[r]
        iv=pow(a[r][c],-1,p)
        for j in range(c,cols):a[r][j]=a[r][j]*iv%p
        for i in range(r+1,rows):
            v=a[i][c]
            if v:
                for j in range(c,cols):a[i][j]=(a[i][j]-v*a[r][j])%p
        r+=1
        if r==rows:break
    return r


def raw_fiber_spectra(x,m,p,omega):
    """C[t][h] = sum_u x[t+M*u]*eta^(-h*u). Direct (charged) row DFTs."""
    if len(x)!=m*m: raise ValueError('square input expected')
    eta=pow(omega,m,p)
    e=roots_table(p,eta,m)
    return [[sum(x[t+m*u]*e[(-h*u)%m] for u in range(m))%p for h in range(m)] for t in range(m)]


def direct_dft(x,p,omega):
    n=len(x); powers=roots_table(p,omega,n)
    return [sum(x[j]*powers[(-k*j)%n] for j in range(n))%p for k in range(n)]


def shear_vandermonde(m,p,omega,a,h,mu_kind='clustered'):
    """Different valid universal gauges: mu_j=omega^j or eta^j."""
    assert len(a)==m
    eta=pow(omega,m,p)
    mu=[pow(omega,j,p) if mu_kind=='clustered' else pow(eta,j,p) for j in range(m)]
    lamb=[mu[j]*pow(eta,(-h*a[j])%m,p)%p for j in range(m)]
    return [[pow(lamb[j],t,p) for j in range(m)] for t in range(m)],lamb


def temporal_matrix(m,p,omega,h):
    eta=pow(omega,m,p)
    return [[pow(eta,(-s*t)%m,p)*pow(omega,(-h*t)%(m*m),p)%p for t in range(m)] for s in range(m)]


def geometric_mod(z,m,p):
    zpow=1;ans=0
    for _ in range(m):
        ans=(ans+zpow)%p
        zpow=zpow*z%p
    return ans


def direct_kernel(m,p,omega,a,h,mu_kind='clustered'):
    eta=pow(omega,m,p)
    mu=[pow(omega,j,p) if mu_kind=='clustered' else pow(eta,j,p) for j in range(m)]
    out=[]
    for s in range(m):
        z=pow(omega,(-h-s*m)%(m*m),p)
        out.append([geometric_mod(z*mu[j]*pow(eta,(-h*a[j])%m,p)%p,m,p) for j in range(m)])
    return out


def full_orbit_execution(x,m,p,omega,a,mu_kind='clustered'):
    """Completely charged direct exact implementation; intentionally not asymptotically fast."""
    c=raw_fiber_spectra(x,m,p,omega)
    out=[0]*(m*m)
    certificates=[]
    for h in range(m):
        V,lamb=shear_vandermonde(m,p,omega,a,h,mu_kind)
        B=matmul(inv_mod(V,p),[[c[t][h]] for t in range(m)],p)
        K=direct_kernel(m,p,omega,a,h,mu_kind)
        y=matmul(K,B,p)
        for s in range(m):out[h+s*m]=y[s][0]
        A=temporal_matrix(m,p,omega,h)
        if matmul(A,V,p)!=K:raise AssertionError('kernel factorization')
        if matmul(V,B,p)!=[[c[t][h]] for t in range(m)]:raise AssertionError('raw recovery')
        if y != matmul(A,[[c[t][h]] for t in range(m)],p):raise AssertionError('gauge invariance')
        certificates.append({'h':h,'rank_V':m,'nonzero_K':sum(z!=0 for row in K for z in row)})
    return out,certificates


def transition_mask(m,p,omega,a,delta):
    eta=pow(omega,m,p)
    return [[pow(eta,(-delta*t*a[j])%m,p) for j in range(m)] for t in range(m)]


def transition_mask_rank_formula(m,a,delta):
    return len({(delta*x)%m for x in a})


def transition_factorization(m,p,omega,a,delta):
    """Explicit minimal-rank decomposition of E by frequency classes."""
    E=transition_mask(m,p,omega,a,delta)
    labels=sorted({(delta*x)%m for x in a})
    eta=pow(omega,m,p)
    left=[[pow(eta,(-t*d)%m,p) for d in labels] for t in range(m)]
    right=[[int((delta*x)%m ==d) for x in a] for d in labels]
    assert matmul(left,right,p)==E
    assert rank_mod(E,p)==len(labels)
    return E,left,right


def optimal_mask_spanning_tree(m):
    """Weighted MST for edges h->h', w=M/gcd(M,h'-h).

    Kruskal's component partitions correspond to the unique additive subgroup of
    Z/M generated by all differences with additive order <= current weight.
    """
    ds=[d for d in range(2,m+1) if m%d==0]
    L=1;cost=0;pieces=[]
    for d in ds:
        Lnext=lcm(L,d)
        merges=m//L - m//Lnext
        if merges:
            pieces.append({'weight':d,'edges_added':merges,'cost':d*merges,'subgroup_size':Lnext})
        cost+=d*merges; L=Lnext
    assert L==m
    assert sum(x['edges_added'] for x in pieces)==m-1
    return cost,pieces


def kruskal_mask_mst(m):
    edges=sorted((m//gcd(m,j-i),i,j) for i in range(m) for j in range(i+1,m))
    parent=list(range(m))
    def find(x):
        while parent[x]!=x:
            parent[x]=parent[parent[x]];x=parent[x]
        return x
    total=0;chosen=[]
    for cost,i,j in edges:
        a=find(i);b=find(j)
        if a!=b:
            parent[a]=b
            total+=cost;chosen.append((i,j,cost))
    assert len(chosen)==m-1
    return total,chosen


def prufer_weight(code,m):
    """Brute-force Prüfer labeled-tree enumeration validation, independent of MST formula."""
    degrees=[1]*m
    for v in code:degrees[v]+=1
    total=0
    for v in code:
        leaf=next(i for i in range(m) if degrees[i]==1)
        total+=m//gcd(m,abs(leaf-v))
        degrees[leaf]-=1;degrees[v]-=1
    a,b=[i for i in range(m) if degrees[i]==1]
    return total+m//gcd(m,abs(a-b))


def orthogonal_gauge_matrix(m,p,omega,h):
    """All shears zero and mu_j=eta^j, gives V independent of h and Fourier orthogonality."""
    V,_=shear_vandermonde(m,p,omega,[0]*m,h,'orthogonal')
    VT=[[V[j][i] for j in range(m)] for i in range(m)]
    # V^{-1} = (1/M) F with negative exponent; check independently.
    eta=pow(omega,m,p)
    neg=[[pow(eta,(-j*t)%m,p) for t in range(m)] for j in range(m)]
    actual=matmul(V,neg,p)
    assert actual==[[m%p if i==j else 0 for j in range(m)] for i in range(m)]
    K=direct_kernel(m,p,omega,[0]*m,h,'orthogonal')
    assert matmul(temporal_matrix(m,p,omega,h),V,p)==K
    assert all(K[s][j]==K[(s+1)%m][(j+1)%m] for s in range(m) for j in range(m))
    return V,K


def affine_nodes_all_distinct_prime(m,a):
    """For mu_j=eta^j, lambda_j(h)=eta^(j-h*a_j)."""
    assert is_prime(m)
    return all(len({(j-h*a[j])%m for j in range(m)})==m for h in range(m))
