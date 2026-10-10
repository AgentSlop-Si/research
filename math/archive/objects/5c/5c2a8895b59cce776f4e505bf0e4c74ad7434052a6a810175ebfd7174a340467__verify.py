#!/usr/bin/env python3
"""Exact verification of the Fourier--Segre symmetric-square obstruction.

The arithmetic uses only Python integers modulo 97. The weighted Green
branches are RECONSTRUCTED using the finite geometric series (not inversion),
and the Fourier phases are primitive roots in GF(97).

This source is self-contained and requires no installed packages.
"""
from __future__ import annotations
import json
import itertools
from pathlib import Path

P = 97
HERE = Path(__file__).parent

def mm(A, B, p=P):
    assert len(A[0]) == len(B)
    return [[sum(a * b for a, b in zip(row, col)) % p for col in zip(*B)] for row in A]

def eye(n): return [[int(i == j) for j in range(n)] for i in range(n)]
def diag(x): return [[x[i] if i == j else 0 for j in range(len(x))] for i in range(len(x))]
def add(A, B): return [[(x+y) % P for x,y in zip(a,b)] for a,b in zip(A,B)]
def sub(A, B): return [[(x-y) % P for x,y in zip(a,b)] for a,b in zip(A,B)]
def matvec(A,x): return [sum(a*b for a,b in zip(row,x))%P for row in A]

def inverse(A):
    n = len(A)
    T = [[x % P for x in row] + E for row,E in zip(A, eye(n))]
    for j in range(n):
        k = next((i for i in range(j,n) if T[i][j]), None)
        if k is None: raise ValueError('matrix singular')
        T[j],T[k] = T[k],T[j]
        s = pow(T[j][j], -1, P)
        T[j] = [(s*x)%P for x in T[j]]
        for i in range(n):
            if i != j:
                s = T[i][j]
                T[i] = [(x-s*y)%P for x,y in zip(T[i],T[j])]
    return [row[n:] for row in T]

def det(A):
    n = len(A)
    T = [[v%P for v in row] for row in A]
    result = 1
    for j in range(n):
        k = next((i for i in range(j,n) if T[i][j]), None)
        if k is None: return 0
        if k != j: T[j],T[k] = T[k],T[j]; result = -result
        z = T[j][j]
        result = (result*z)%P
        inv = pow(z,-1,P)
        for i in range(j+1,n):
            mul = T[i][j]*inv%P
            for h in range(j,n):T[i][h] = (T[i][h]-mul*T[j][h])%P
    return result%P

def rref_rank(M, return_rows=False):
    if not M: return (0,[]) if return_rows else 0
    T = [row[:] for row in M]
    idx = list(range(len(T)))
    m = len(T); n = len(T[0]); r = 0
    for j in range(n):
        k = next((i for i in range(r,m) if T[i][j]%P),None)
        if k is None:continue
        T[r],T[k] = T[k],T[r]
        idx[r],idx[k]=idx[k],idx[r]
        fac = pow(T[r][j],-1,P)
        T[r] = [(u*fac)%P for u in T[r]]
        for i in range(r+1,m):
            fac = T[i][j]
            if fac: T[i] = [(x-fac*y)%P for x,y in zip(T[i],T[r])]
        r += 1
        if r == min(m,n):break
    return (r,idx[:r]) if return_rows else r

def power_green(b):
    """(I-D_w P_sigma)^-1 = sum_{k=0}^{n-1}(D_w P_sigma)^k/(1-prod w)."""
    perm = b['cycle']; weights = [w%P for w in b['weights']]; n=len(perm)
    assert sorted(perm)==list(range(n)) and all(weights)
    assert len({tuple([i]+[perm[i]]) for i in range(n)})==n
    orbit=[]; j=0
    for k in range(n):
        assert j not in orbit
        orbit.append(j);j=perm[j]
    assert j==0 and len(orbit)==n
    prod=1
    for w in weights:prod=prod*w%P
    assert (1-prod)%P != 0
    scale = pow((1-prod)%P,-1,P)
    G = [[0]*n for _ in range(n)]
    for i in range(n):
        j=i; coef=scale
        for _ in range(n):
            G[i][j] = coef
            coef = coef*weights[j]%P
            j = perm[j]
    ld=[x%P for x in b['left_diag']];rd=[x%P for x in b['right_diag']]
    G = [[ld[i]*G[i][j]*rd[j]%P for j in range(n)] for i in range(n)]
    p1=b['row_permutation'];p2=b['col_permutation']
    assert sorted(p1)==sorted(p2)==list(range(n))
    return [[G[p1[i]][p2[j]] for j in range(n)] for i in range(n)]

def reconstruct(cert):
    As=[power_green(b) for b in cert['trace_A']]
    Bs=[power_green(b) for b in cert['trace_B']]
    A=add(As[0],As[1]); B=add(Bs[0],Bs[1])
    assert A==cert['A'] and B==cert['B']
    assert [row[0] for row in Bs[0]] == cert['b_delta']
    return A,B,Bs[0]

def fourier(n,omega): return [[pow(omega,i*j,P) for j in range(n)] for i in range(n)]

def p_columns(A,B,omega):
    n=len(A); AI=inverse(A); out=[]
    for j in range(n):
        assert all(B[u][j] for u in range(n)), 'Hadamard quotient chart invalid'
        invb=[pow(B[u][j],-1,P) for u in range(n)]
        h=[pow(omega,i*j,P) for i in range(n)]
        out.append(mm(diag(invb),mm(AI,diag(h))))
    return out

def quadratic_matrix(Pjs):
    """Each row is one 2x2 minor, coefficients of v(c)=(c_a c_b)_{a<=b}."""
    n=len(Pjs[0]); pairs=[(a,b) for a in range(n) for b in range(a,n)]
    Q=[]
    for j,k in itertools.combinations(range(3),2):
        for u in range(n):
            for v in range(u+1,n):
                row=[]
                for a,b in pairs:
                    val=Pjs[j][u][a]*Pjs[k][v][b] - Pjs[k][u][a]*Pjs[j][v][b]
                    if a != b:
                        val += Pjs[j][u][b]*Pjs[k][v][a] - Pjs[k][u][b]*Pjs[j][v][a]
                    row.append(val%P)
                Q.append(row)
    return Q

def commutator_at_t(A,B,branch1,t,omega):
    """Input-gauge-invariant T_j(t) for first 3 Fourier columns.
       B(t) = B + (t-1) G_branch1 e0 e0^T.
       Although P0(t) can be undefined at isolated t, this formula is polynomial.
    """
    n=len(A); AI=inverse(A)
    b0=[(B[i][0]+(t-1)*branch1[i][0])%P for i in range(n)]
    Ts=[]
    for j in (1,2):
        ratios=[b0[i]*pow(B[i][j],-1,P)%P for i in range(n)]
        Ts.append(mm(A,mm(diag(ratios),mm(AI,diag([pow(omega,j*i,P) for i in range(n)])))))
    return sub(mm(Ts[0],Ts[1]), mm(Ts[1],Ts[0]))

def polynomial_interpolate(xs,ys):
    n=len(xs);a=ys[:]
    for j in range(1,n):
        for i in range(n-1,j-1,-1):
            a[i]=(a[i]-a[i-1])*pow(xs[i]-xs[i-j],-1,P)%P
    poly=[0]*n;basis=[1]
    for j in range(n):
        for k,b in enumerate(basis):poly[k]=(poly[k]+a[j]*b)%P
        next_basis=[0]*(len(basis)+1)
        for k,b in enumerate(basis):
            next_basis[k]=(next_basis[k]-xs[j]*b)%P
            next_basis[k+1]=(next_basis[k+1]+b)%P
        basis=next_basis
    while len(poly)>1 and poly[-1]==0:poly.pop()
    return poly

def eval_poly(cs,t):
    result=0
    for a in reversed(cs):result=(result*t+a)%P
    return result

def verify_cert(cert):
    n=cert['n']; omega=cert['root']
    assert pow(omega,n,P)==1
    assert all(pow(omega,n//f,P)!=1 for f in (2,3) if n%f==0)
    A,B,branch1=reconstruct(cert)
    assert det(A) and det(B) and all(v for row in B for v in row)
    Ps=p_columns(A,B,omega)
    Q=quadratic_matrix(Ps)
    expected=n*(n+1)//2
    rank,rows=rref_rank(Q,True)
    assert rank == expected and rank==cert['quadratic_rank']
    minor=det([Q[i] for i in rows])
    assert minor!=0
    C=commutator_at_t(A,B,branch1,1,omega)
    assert det(C)==0
    xs=list(range(2*n+1))
    ys=[det(commutator_at_t(A,B,branch1,t,omega)) for t in xs]
    poly=polynomial_interpolate(xs,ys)
    assert poly==cert['polynomial_modp'], (poly,cert['polynomial_modp'])
    deriv=sum(i*a for i,a in enumerate(poly))%P
    assert eval_poly(poly,1)==0 and deriv==cert['derivative_modp'] and deriv!=0
    for t in (2*n+1, 2*n+2, 37, 78, 96):
        assert eval_poly(poly,t)==det(commutator_at_t(A,B,branch1,t,omega))
    # Verify the quadratic polynomial coefficient identity on random c.
    for t in range(1,10):
        c=[(7*i+11*t)%P for i in range(n)]
        W=[[matvec(Pj,c)[i] for Pj in Ps[:3]] for i in range(n)]
        minors=[(W[u][j]*W[v][k]-W[u][k]*W[v][j])%P
            for j,k in itertools.combinations(range(3),2)
            for u in range(n) for v in range(u+1,n)]
        mom=[c[a]*c[b]%P for a in range(n) for b in range(a,n)]
        assert matvec(Q,mom)==minors
    # Positive factorization control: B need not itself be Green.
    F=fourier(n,omega)
    d=[2+i for i in range(n)]
    e=[5+i for i in range(n)]
    for shift in range(1,70):
        c=[(17+shift*(i+1))%P for i in range(n)]
        if not all(c):continue
        Bpos=mm(diag([pow(v,-1,P) for v in d]),mm(inverse(A),mm(diag(c),mm(F,diag([pow(v,-1,P) for v in e])))))
        if all(x for row in Bpos for x in row):break
    else: raise AssertionError('positive control chart not found')
    Ppos=p_columns(A,Bpos,omega)
    Qpos=quadratic_matrix(Ppos)
    mom=[c[a]*c[b]%P for a in range(n) for b in range(a,n)]
    assert all(z==0 for z in matvec(Qpos,mom))
    assert rref_rank(Qpos)<expected
    result={
        'N':n, 'field':P, 'primitive_root':omega,
        'commutator_det_at_t1':0,
        'quad_shape':[len(Q),len(Q[0])],
        'quad_rank':rank,'pivot_rows':rows,'nonzero_pivot_minor_mod97':minor,
        'commutator_det_polynomial_mod97':poly,
        'derivative_at_t1_mod97':deriv,
        'positive_control_quad_rank':rref_rank(Qpos),
        'char_zero_conclusion':'At a suitable algebraic parameter alpha over Q(zeta_N), the commutator is singular but the quadratic certificate is injective; follows by simple-root Hensel lifting.'
    }
    return result

def main():
    results=[]
    for n in (3,4):
        cert=json.loads((HERE/f'CERT_N{n}.json').read_text())
        results.append(verify_cert(cert))
    (HERE/'RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))

if __name__=='__main__':main()
