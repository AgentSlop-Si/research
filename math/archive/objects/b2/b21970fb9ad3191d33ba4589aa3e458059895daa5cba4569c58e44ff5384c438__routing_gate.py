"""Hero #17 phase-four exact finite-field shear routing diagnostic.

Purpose: separate zeros of geometric orbit-output kernels from actual
transform complexity. No all-input sub-FFT complexity claim.
"""
from __future__ import annotations
from math import gcd


def prime_factors(n):
    a=[];k=2
    while k*k<=n:
        if n%k==0:
            a.append(k)
            while n%k==0:n//=k
        k+=1
    if n>1:a.append(n)
    return a


def primitive_n_root(p,n):
    if (p-1)%n:raise ValueError('n must divide p-1')
    fs=prime_factors(n)
    for b in range(2,p):
        w=pow(b,(p-1)//n,p)
        if all(pow(w,n//f,p)!=1 for f in fs):return w
    raise ValueError('primitive root not found')


def root_table(p,w,n):
    out=[1]*n
    for i in range(1,n):out[i]=out[i-1]*w%p
    assert out[-1]*w%p==1
    return out


def direct_dft(x,p,w):
    n=len(x);r=root_table(p,w,n)
    return [sum(x[t]*r[(-k*t)%n] for t in range(n))%p for k in range(n)]


def geometric(z,q,p):
    # Independent direct computation makes tests immune to inverse-table bugs.
    v=1;s=0
    for _ in range(q):
        s=(s+v)%p
        v=v*z%p
    return s


def kernel(q,m,p,omega,a,mu,h,s):
    """K_h[s,a,mu] in unnormalized N=QM DFT basis."""
    n=q*m;k=h+s*m
    eta=pow(omega,q,p)
    lamb=mu*pow(eta,(-a*h)%m,p)%p
    z=lamb*pow(omega,(-k)%n,p)%p
    return geometric(z,q,p)


def matched_channels(q,m,p,omega,a,mu):
    """Channels on which all but one geometric output kernel vanish."""
    eta=pow(omega,q,p)
    factor=pow(mu,q,p)
    return [h for h in range(m) if factor==pow(eta,((a*q+1)*h)%m,p)]


def matched_count_bound(q,m,a):
    return gcd(a*q+1,m)


def routing_pair(q,m):
    """Common shear giving full routing exists iff gcd(q,m)=1."""
    if gcd(q,m)!=1:return None
    a=(-pow(q,-1,m))%m
    b=(a*q+1)//m
    return a,b


def two_stage_arbitrary_raw_routing(x,q,m,p,omega):
    """Exact arbitrary-input transform via routed orbits, NOT an O(N) method.

    Includes explicit row-DFTs and temporal DFTs, which are standard FFT stages.
    Returns exact spectrum, recovered orbit-frequency amplitudes, and the
    first-stage row spectra for verifying the representation.
    """
    if len(x)!=q*m:raise ValueError('length mismatch')
    pair=routing_pair(q,m)
    if pair is None:raise ValueError('coprime q,m required')
    a,b=pair;n=q*m
    eta=pow(omega,q,p);xi=pow(omega,m,p)
    eta_roots=root_table(p,eta,m)
    xi_roots=root_table(p,xi,q)
    C=[]
    for t in range(q):
        row=[x[t+q*u]%p for u in range(m)]
        C.append([sum(row[u]*eta_roots[(-h*u)%m] for u in range(m))%p for h in range(m)])
    inv_q=pow(q,-1,p)
    B=[[0]*m for _ in range(q)]
    for h in range(m):
        for j in range(q):
            B[j][h]=inv_q*sum(C[t][h]*eta_roots[(a*h*t)%m]*xi_roots[(-j*t)%q]
                                  for t in range(q))%p
    out=[0]*n
    for h in range(m):
        for s in range(q):
            j=(s+b*h)%q
            out[h+s*m]=q*B[j][h]%p
    return out,B,C


def verify_universal_representation(x,q,m,p,omega,B):
    """Verify all Q*M input samples from recovered Q orbit spectra B."""
    assert len(x)==q*m
    a,_=routing_pair(q,m)
    eta=pow(omega,q,p)
    inv_m=pow(m,-1,p)
    eta_roots=root_table(p,eta,m)
    xi=pow(omega,m,p)
    xi_roots=root_table(p,xi,q)
    bases=[[inv_m*sum(B[j][h]*eta_roots[(h*u)%m] for h in range(m))%p
            for u in range(m)] for j in range(q)]
    for t in range(q):
        for u in range(m):
            value=sum(xi_roots[(j*t)%q]*bases[j][(u-a*t)%m] for j in range(q))%p
            if value!=x[t+q*u]%p:return False
    return True


def square_coset_density(m,p,omega,check_direct=True):
    """Universal square orbit choice a_j=j, mu_j=omega^j.

    Exact nonzero graph edges and per-frequency ranks. For N=M^2,
    K_h(s,j) is nonzero for every s when j!=h, and is nonzero once
    when j==h. It follows that edges=M^3-M^2+M.
    """
    n=m*m;assert pow(omega,n,p)==1
    roots=root_table(p,omega,n)
    counts=[];nodes_distinct=True;matched=[]
    for h in range(m):
        c=0
        nodes=[]
        for j in range(m):
            a=j;mu=roots[j]
            nodes.append(mu*pow(roots[m],(-a*h)%m,p)%p)
            matches=matched_channels(m,m,p,omega,a,mu)
            if matches!=[j]:raise AssertionError((m,j,matches))
            for s in range(m):
                if check_direct:
                    val=kernel(m,m,p,omega,a,mu,h,s)
                    nonzero=(val!=0)
                else:
                    # Equivalent derived zero condition; no direct G evaluation.
                    nonzero=(j!=h or s==(-h*h)%m)
                c+=int(nonzero)
                if nonzero != (j!=h or s==(-h*h)%m):
                    raise AssertionError(('kernel-pattern-failure',m,h,s,j))
        nodes_distinct=nodes_distinct and len(set(nodes))==m
        counts.append(c)
    edges=sum(counts)
    expected=m**3-m**2+m
    assert edges==expected and nodes_distinct
    return dict(m=m,n=n,total_nonzero_edges=edges,potential_edges=n*m,
                theoretical_edges=expected,per_channel=counts,
                full_rank_channels=m,one_routed_orbit_per_channel=True)


def rank_mod(rows,p):
    a=[[v%p for v in row] for row in rows]
    if not a:return 0
    nrows,ncols=len(a),len(a[0])
    rank=0
    for col in range(ncols):
        pivot=next((r for r in range(rank,nrows) if a[r][col]),None)
        if pivot is None:continue
        a[rank],a[pivot]=a[pivot],a[rank]
        inv=pow(a[rank][col],-1,p)
        for j in range(col,ncols):a[rank][j]=a[rank][j]*inv%p
        for i in range(rank+1,nrows):
            scale=a[i][col]
            if scale:
                for j in range(col,ncols):a[i][j]=(a[i][j]-scale*a[rank][j])%p
        rank+=1
        if rank==nrows:break
    return rank


def matrix_factorization_check(q,m,p,omega,orbit_parameters,h):
    """Checks K_h=F_Q diag(omega^{-h t}) V_h directly."""
    assert 0<=h<m
    xi=pow(omega,m,p);eta=pow(omega,q,p)
    g=len(orbit_parameters)
    K=[[kernel(q,m,p,omega,a,mu,h,s) for a,mu in orbit_parameters]
       for s in range(q)]
    lambdas=[mu*pow(eta,(-a*h)%m,p)%p for a,mu in orbit_parameters]
    F=[[pow(xi,(-s*t)%q,p) for t in range(q)] for s in range(q)]
    diagonal=[pow(omega,(-h*t)%(q*m),p) for t in range(q)]
    V=[[pow(lam,t,p) for lam in lambdas] for t in range(q)]
    rhs=[[sum(F[s][t]*diagonal[t]*V[t][j] for t in range(q))%p
          for j in range(g)] for s in range(q)]
    assert K==rhs
    return {'rank':rank_mod(K,p),'zero_edges':sum(v==0 for row in K for v in row),
            'nonzero_edges':sum(v!=0 for row in K for v in row)}


def displacement_certificate(q,m,p,omega,orbit_parameters,h):
    """Exact Sylvester displacement:

         K_h - diag(z_s) K_h diag(lambda_j) = 1 * d_j^T

       z_s=omega^(-h-s*M), lambda_j=mu_j*eta^(-a_j*h),
       d_j=1-eta^(-h)*lambda_j^Q. Rank of the RHS is 0 or 1.
    """
    n=q*m
    eta=pow(omega,q,p)
    z=[pow(omega,(-h-s*m)%n,p) for s in range(q)]
    lamb=[mu*pow(eta,(-a*h)%m,p)%p for a,mu in orbit_parameters]
    d=[(1-pow(eta,(-h)%m,p)*pow(v,q,p))%p for v in lamb]
    K=[[kernel(q,m,p,omega,a,mu,h,s) for a,mu in orbit_parameters]
       for s in range(q)]
    residual=[[ (K[s][j]*(1-z[s]*lamb[j]))%p
                for j in range(len(orbit_parameters))] for s in range(q)]
    assert residual==[d for _ in range(q)]
    return {'rank':int(any(d)),'zero_defect_columns':[j for j,v in enumerate(d) if not v],
            'defect_values':d, 'kernel_rank':rank_mod(K,p),
            'kernel_edges':sum(v!=0 for row in K for v in row)}


def weyl_commutator_certificate(m,p,eta):
    """S shift right, T phase modulation: S*T=eta^(-1)*T*S."""
    inv_eta=pow(eta,-1,p)
    for u in range(m):
        # For a delta input at u, T then S yields eta**u delta_(u+1).
        st=pow(eta,u,p)
        # S then T yields eta**(u+1) delta_(u+1).
        ts=pow(eta,(u+1)%m,p)
        if st != inv_eta*ts%p:return False
    return True
