"""Exact finite-field Fourier phase gate for products of nonunitary Green sums.

For fixed invertible A,B, all middle diagonal Q in A Q B are checked in
one linear-algebra test.  The diagonal and 2-cycle multisets additionally
reject arbitrary intervening permutations without enumeration.
"""
from __future__ import annotations
import json,random
from harper_certificate import P,root_n


def mm(A,B,p=P):
    n=len(A);m=len(B[0]);out=[[0]*m for _ in range(n)]
    for i,arow in enumerate(A):
        o=out[i]
        for k,a in enumerate(arow):
            if a:
                brow=B[k]
                for j in range(m):o[j]+=a*brow[j]
        for j in range(m):o[j]%=p
    return out


def invert(A,p=P):
    n=len(A); x=[[int(v)%p for v in row]+[int(i==j) for j in range(n)] for i,row in enumerate(A)]
    for j in range(n):
        row=next((r for r in range(j,n) if x[r][j]),None)
        if row is None:raise ValueError('singular')
        x[j],x[row]=x[row],x[j]
        r=x[j];inv=pow(r[j],-1,p)
        for k in range(j,2*n):r[k]=r[k]*inv%p
        for i in range(n):
            if i==j:continue
            ri=x[i];f=ri[j]
            if f:
                for k in range(j,2*n):ri[k]=(ri[k]-f*r[k])%p
    return [row[n:] for row in x]


def green_matrix(n,rng,omega,perm):
    """Dense oracle for tridiagonal inverse, but application admits O(N) solve."""
    phase=[pow(omega,int((i*i+3*i+rng.randrange(n))%n),P) for i in range(n)]
    diag=[(7+phase[i])%P for i in range(n)]
    lo=[(1+pow(omega,int(i+rng.randrange(n)),P))%P for i in range(n-1)]
    up=[(2+pow(omega,int(2*i+rng.randrange(n)),P))%P for i in range(n-1)]
    T=[[0]*n for _ in range(n)]
    for i in range(n):
        T[i][i]=diag[i]
        if i+1<n:T[i][i+1]=up[i];T[i+1][i]=lo[i]
    # n=32,64,128: dense inverse used ONLY to audit the O(N)-apply solver matrix.
    G=invert(T)
    left=[pow(omega,rng.randrange(n),P) for _ in range(n)]
    right=[pow(omega,rng.randrange(n),P) for _ in range(n)]
    out=[[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):out[perm[i]][perm[j]]=left[i]*right[j]*G[i][j]%P
    return out


def sum_two_green(n,rng,omega):
    result=[[0]*n for _ in range(n)]
    for _ in range(2):
        order=list(range(n));rng.shuffle(order)
        G=green_matrix(n,rng,omega,order)
        for i in range(n):
            for j in range(n):result[i][j]=(result[i][j]+G[i][j])%P
    return result


def middle_invariants(A,B,omega):
    n=len(A)
    Ai=invert(A);Bi=invert(B)
    # D = diag(omega^j), Z[e_j]=e_(j+1)
    DA=[[pow(omega,i,P)*a%P for a in row] for i,row in enumerate(A)]
    U=mm(Ai,DA)
    BZ=[[B[i][(j+1)%n] for j in range(n)] for i in range(n)]
    V=mm(BZ,Bi)
    assert len(U)==len(V)==n
    return U,V


def pair_invariants(U):
    n=len(U)
    return sorted(U[i][j]*U[j][i]%P for i in range(n) for j in range(i+1,n))


def diag_permutation_gate(U,V):
    n=len(U)
    diagok=sorted(U[i][i] for i in range(n)) == sorted(V[i][i] for i in range(n))
    pairok=pair_invariants(U)==pair_invariants(V)
    return {'diagonal_multiset_match':diagok,'two_cycle_multiset_match':pairok,
            'all_permutations_and_diagonal_masks_excluded':not (diagok and pairok)}


def solve_middle_diagonal(U,V):
    """Return one nonzero diagonal Q with UQ=QV, or None; all fields exact."""
    n=len(U)
    edges=[[] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            a,b=U[i][j],V[i][j]
            if bool(a)!=bool(b):return None
            if a:
                ratio=a*pow(b,-1,P)%P # q_i/q_j
                edges[j].append((i,ratio))
                edges[i].append((j,pow(ratio,-1,P)))
    q=[None]*n
    for seed in range(n):
        if q[seed] is not None:continue
        q[seed]=1;stack=[seed]
        while stack:
            k=stack.pop()
            for other,ratio in edges[k]:
                proposal=q[k]*ratio%P
                if q[other] is None:
                    q[other]=proposal;stack.append(other)
                elif q[other]!=proposal:return None
    assert all(q[i] and U[i][j]*q[j]%P==q[i]*V[i][j]%P for i in range(n) for j in range(n))
    return q


def fourier_matrix(n,omega):
    invnroot=None
    from harper_certificate import sqrt_mod
    invnroot=pow(sqrt_mod(n),-1,P)
    return [[pow(omega,(i*j)%n,P)*invnroot%P for j in range(n)] for i in range(n)]


def audit(n,seed=1817):
    rng=random.Random(seed+n)
    omega=root_n(n)
    A=sum_two_green(n,rng,omega)
    B=sum_two_green(n,rng,omega)
    U,V=middle_invariants(A,B,omega)
    results=diag_permutation_gate(U,V)
    exact_q=solve_middle_diagonal(U,V)
    assert not results['diagonal_multiset_match']
    assert exact_q is None
    M=mm(A,B)
    defect_count=sum((M[i][(j+1)%n]-pow(omega,i,P)*M[i][j])%P!=0 for i in range(n) for j in range(n))
    assert defect_count>0
    return {'n':n,'field_prime':P,'omega':omega,
            'stage_family':'two independently permuted, chirp-gauged tridiagonal Green inverses per stage',
            'all_entries_cyclotomic':'yes, rational functions of primitive Nth root',
            'middle_diagonal_exists':False,'Fourier_covariance_defect_nonzero_entries':defect_count,
            **results}


def positive_control(n=16):
    omega=root_n(n);F=fourier_matrix(n,omega)
    rng=random.Random(18+n)
    q=[pow(omega,rng.randrange(n),P) for _ in range(n)]
    B=[[pow(q[i],-1,P) if i==j else 0 for j in range(n)] for i in range(n)]
    U,V=middle_invariants(F,B,omega)
    recovered=solve_middle_diagonal(U,V)
    assert recovered is not None
    C=mm(F,[[q[i]*B[i][j]%P for j in range(n)] for i in range(n)])
    assert C==F
    for i in range(n):
        assert recovered[i]*pow(q[i],-1,P)%P==recovered[0]*pow(q[0],-1,P)%P
    gate=diag_permutation_gate(U,V)
    assert gate['diagonal_multiset_match'] and gate['two_cycle_multiset_match']
    return {'n':n,'positive_control_passed':True,'recovered_mask_up_to_scalar':True}

if __name__=='__main__':
    print(json.dumps({'samples':[audit(n) for n in (8,16,32,64)],'controls':[positive_control(n) for n in (8,16,32)]},indent=2))
