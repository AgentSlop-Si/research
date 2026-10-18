#!/usr/bin/env python3
"""Fresh independent transcription checks, not an inverse executor or asymptotic proof.
No historical package is imported. All arithmetic below is exact modulo a prime.
"""
import json
from fractions import Fraction
from pathlib import Path


def mat(n, f): return [[f(i,j) for j in range(n)] for i in range(n)]
def eye(n): return mat(n,lambda i,j:int(i==j))
def add(A,B,p): return [[(a+b)%p for a,b in zip(x,y)] for x,y in zip(A,B)]
def neg(A,p): return [[-a%p for a in x] for x in A]
def sub(A,B,p): return add(A,neg(B,p),p)
def scale(a,A,p): return [[a*x%p for x in row] for row in A]
def mul(A,B,p):
    return [[sum(a*b for a,b in zip(row,col))%p for col in zip(*B)] for row in A]
def power(A,k,p):
    R=eye(len(A))
    while k:
        if k&1:R=mul(R,A,p)
        A=mul(A,A,p); k//=2
    return R
def inverse(A,p):
    n=len(A); B=[r[:]+e[:] for r,e in zip(A,eye(n))]
    for c in range(n):
        k=next((r for r in range(c,n) if B[r][c]),None)
        if k is None:raise ValueError('singular')
        B[c],B[k]=B[k],B[c]
        B[c]=[x*pow(B[c][c],-1,p)%p for x in B[c]]
        for r in range(n):
            if r!=c:
                v=B[r][c];B[r]=[(x-v*y)%p for x,y in zip(B[r],B[c])]
    return [r[n:] for r in B]
def rank(A,p):
    B=[r[:] for r in A];k=0
    for c in range(len(A[0])):
        r=next((r for r in range(k,len(A)) if B[r][c]),None)
        if r is None:continue
        B[k],B[r]=B[r],B[k]
        B[k]=[x*pow(B[k][c],-1,p)%p for x in B[k]]
        for r in range(k+1,len(A)):
            v=B[r][c];B[r]=[(x-v*y)%p for x,y in zip(B[r],B[k])]
        k+=1
    return k
def determinant(A,p):
    B=[r[:] for r in A];d=1
    for c in range(len(A)):
        k=next((r for r in range(c,len(A)) if B[r][c]),None)
        if k is None:return 0
        if k!=c:B[c],B[k]=B[k],B[c];d=-d
        v=B[c][c];d=d*v%p
        for r in range(c+1,len(A)):
            t=B[r][c]*pow(v,-1,p)%p
            B[r]=[(x-t*y)%p for x,y in zip(B[r],B[c])]
    return d%p
def prime(p):return p>=2 and all(p%d for d in range(2,int(p**0.5)+1))
def comm(A,B,p):return sub(mul(A,B,p),mul(B,A,p),p)
def primitive(n,p):
    for a in range(2,p):
        if pow(a,n,p)==1 and all(pow(a,k,p)!=1 for k in range(1,n)):
            return a
    raise ValueError('no primitive root')
def matrices(m,q,p):
    I=eye(m); U=mat(m,lambda i,j:int(j==(i-1)%m)); Q=mat(m,lambda i,j:pow(q,-i,p) if i==j else 0)
    V=power(U,m-1,p); W=add(V,Q,p)
    return I,U,Q,W

def check(m,p):
    omega=primitive(m*m,p);q=pow(omega,m,p)
    I,U,Q,W=matrices(m,q,p)
    assert mul(Q,U,p)==scale(pow(q,-1,p),mul(U,Q,p),p)
    assert power(W,m,p)==scale(2,I,p)
    R0=scale(pow(4,-1,p),W,p)
    E0=I;E1=scale(0,I,p)
    # Exact dual-number product for d/dz of T_(m-1)(z)...T_0(z) at z=0.
    for a in range(m):
        H=sub(I,scale(pow(q,a,p)*pow(4,-1,p)%p,U,p),p)
        T1=scale(pow(4,-1,p),sub(I,mul(H,W,p),p),p)
        E1=add(mul(T1,E0,p),mul(R0,E1,p),p)
        E0=mul(R0,E0,p)
    expected=scale(m*pow(pow(4,m,p),-1,p)%p,sub(power(W,m-1,p),scale(2,I,p),p),p)
    assert E1==expected
    ell=4+m*((2*m-1).bit_length());lam=pow(pow(2,ell,p),-1,p)
    s=(1+lam)%p; beta=lam*pow(4*s,-1,p)%p
    assert s and (1-pow(beta,m,p))%p
    E=I
    for a in range(m):
        D=sub(scale(s,I,p),scale(lam*pow(4,-1,p)*pow(q,a,p)%p,U,p),p)
        R=scale(pow(4,-1,p),add(W,scale(lam,I,p),p),p)
        E=mul(mul(inverse(D,p),R,p),E,p)
    F=sub(I,E,p);Finv=inverse(F,p)
    ranks={name:rank(comm(A,X,p),p) for name,A,X in [('F_U',F,U),('F_Q',F,Q),('Finv_U',Finv,U),('Finv_Q',Finv,Q)]}
    assert all(r==m for r in ranks.values())
    return {'m':m,'p':p,'omega_N':omega,'q':q,'ell':ell,'lambda_mod_p':lam,'beta_mod_p':beta,'derivative_identity':True,'ranks':ranks}

def guard_control():
    m=2;p=79;q=78;lam=pow(256,-1,p);s=(1+lam)%p
    beta=lam*pow(4*s,-1,p)%p
    I,U,Q,W=matrices(m,q,p)
    Ds=[sub(scale(s,I,p),scale(lam*pow(4,-1,p)*pow(q,a,p)%p,U,p),p) for a in range(m)]
    R=scale(pow(4,-1,p),add(W,scale(lam,I,p),p),p)
    K=mat(4,lambda i,j:((Ds[i//2][i%2][j%2] if i//2==j//2 else 0)-(R[i%2][j%2] if j//2==(i//2-1)%2 else 0))%p)
    L=mat(4,lambda i,j:(int(i==j)-pow(4,-1,p)*(int(j==((i//2-1)%2)*2+i%2)+pow(q,i//2,p)*int(j==(i//2)*2+(i%2-1)%2)))%p)
    assert p%4==3 and q==p-1  # omega_N=i in F_p[i]/(i^2+1), not in F_p.
    assert (1-pow(beta,m,p))%p==0
    assert rank(K,p)==4 and rank(L,p)==4
    # Explicit permutation conjugation independently verifies the K formula.
    P=mat(4,lambda i,j:int(i==((-j%2)%2)*2+((j//2+j%2)%2)))
    M=mul(mul(inverse(P,p),L,p),P,p)
    assert K==add(M,scale(lam,L,p),p)
    assert determinant(K,p)==39 and determinant(L,p)==determinant(M,p)==2
    return {'m':m,'p':p,'omega_N':'i in F_79[i]/(i^2+1)','q':q,'lambda_mod_p':lam,'beta_mod_p':beta,'row_guard':0,'row_ranks':[rank(D,p) for D in Ds],'rank_K':rank(K,p),'rank_L':rank(L,p),'det_K':determinant(K,p),'det_L':determinant(L,p),'det_M':determinant(M,p),'K':K,'permutation_formula_verified':True}

def main():
    assert prime(79) and prime(14401)
    result={'purpose':'transcription controls only; all-size proof is REPORT.md',
            'moduli_verified_prime':[79,14401],
            'source_or_historical_programs_executed':False,
            'controls':[check(m,14401) for m in (3,4,5,6)],
            'executor_guard_not_full_invertibility':guard_control(),
            'analytic_threshold_checks':[]}
    for m in range(4,101):
        ell=4+m*((2*m-1).bit_length());lam=Fraction(1,2**ell)
        assert lam<=Fraction(1,256*m*m*2**m)
        assert lam<Fraction(1,16*m)
    result['analytic_threshold_checks']={'range':[4,100],'all_exact_inequalities_pass':True,'not_used_as_all_m_proof':True}
    p=Path(__file__).with_name('CHECK_RESULTS.json');p.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
