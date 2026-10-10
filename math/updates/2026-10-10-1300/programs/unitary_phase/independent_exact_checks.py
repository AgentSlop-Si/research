#!/usr/bin/env python3
"""Fresh exact reviewer controls. Standard library only; no external code loaded.

Arithmetic is Q[z]/Phi_L(z), with L=6,12,30 as appropriate. Every result is
exact. This program does not parse or execute the author's or uploaded code.
"""
from fractions import Fraction as F
from itertools import product
from collections import Counter
from pathlib import Path
import json
import platform


class Ring:
    def __init__(self, order, modulus):
        self.order = order
        self.mod = tuple(F(v) for v in modulus)
        assert self.mod[-1] == 1
        self.degree = len(modulus) - 1
        self.zero = (F(0),) * self.degree
        self.one = (F(1),) + (F(0),) * (self.degree - 1)
        z = (F(0), F(1)) + (F(0),) * (self.degree - 2)
        self.roots = [self.one]
        for _ in range(1, order):
            self.roots.append(self.mul(self.roots[-1], z))
        assert self.mul(self.roots[-1], z) == self.one
        assert len(set(self.roots)) == order
        assert self.polynomial_at_root(self.mod, 1) == self.zero

    def add(self, a, b):
        return tuple(x+y for x, y in zip(a,b))

    def neg(self, a):
        return tuple(-x for x in a)

    def scale(self, a, k):
        return tuple(x*k for x in a)

    def const(self, k):
        return self.scale(self.one, F(k))

    def mul(self, a, b):
        n = self.degree
        tmp = [F(0)] * (2*n - 1)
        for i,x in enumerate(a):
            if x:
                for j,y in enumerate(b):
                    if y:
                        tmp[i+j] += x*y
        for k in range(2*n-2, n-1, -1):
            v = tmp[k]
            if v:
                for j,c in enumerate(self.mod[:-1]):
                    tmp[k-n+j] -= v*c
        return tuple(tmp[:n])

    def root(self, exponent):
        return self.roots[exponent % self.order]

    def polynomial_at_root(self, coeffs, exponent):
        out = self.zero
        for i,c in enumerate(coeffs):
            if c:
                out = self.add(out, self.scale(self.root(i*exponent), c))
        return out

    def conj(self, a):
        return self.polynomial_at_root(a, -1)

    def text(self, a):
        return [str(x) for x in a]


def ring_for(n):
    if n == 4:
        return Ring(12, [1,0,-1,0,1])
    if n == 5:
        return Ring(30, [1,1,0,-1,-1,-1,0,1,1])
    return Ring(6, [1,-1,1])


def matmul(R, A, B):
    n, m, p = len(A), len(B), len(B[0])
    C = [[R.zero for _ in range(p)] for _ in range(n)]
    for a in range(n):
        for b in range(p):
            for k in range(m):
                if A[a][k] != R.zero and B[k][b] != R.zero:
                    C[a][b] = R.add(C[a][b], R.mul(A[a][k],B[k][b]))
    return C


def identity(R,n):
    return [[R.one if a==b else R.zero for b in range(n)] for a in range(n)]


def legal_orbit_matrices(R, n, t, holonomy, d):
    # Independently construct the directed edges and the geometric path kernel.
    zstep=R.order//3
    W=[[R.zero for _ in range(n)] for _ in range(n)]
    for b in range(n):
        a=(b+1)%n
        edge=holonomy if b==n-1 else R.one
        W[a][b]=R.mul(edge,R.root(zstep*(t[a]-t[b])))
    G=[]
    for a in range(n):
        row=[]
        for b in range(n):
            path=holonomy if a<b else R.one
            row.append(R.mul(R.mul(d,path),R.root(zstep*(t[a]-t[b]))))
        G.append(row)
    return W,G


def assert_legal(R,W,G,holonomy):
    n=len(W)
    eye=identity(R,n)
    star=[[R.conj(W[b][a]) for b in range(n)] for a in range(n)]
    assert matmul(R,star,W)==eye
    assert all(sum(v!=R.zero for v in row)==1 for row in W)
    assert all(sum(W[a][b]!=R.zero for a in range(n))==1 for b in range(n))
    # The successor walk covers the whole vertex set once, not a cycle cover.
    successor=[next(a for a in range(n) if W[a][b]!=R.zero) for b in range(n)]
    walk=[]
    p=0
    h=R.one
    for _ in range(n):
        walk.append(p)
        h=R.mul(h,W[successor[p]][p])
        p=successor[p]
    assert p==0 and len(set(walk))==n and h==holonomy and h!=R.one
    IminusW=[[R.add(eye[a][b],R.neg(W[a][b])) for b in range(n)] for a in range(n)]
    assert matmul(R,IminusW,G)==eye
    assert matmul(R,G,IminusW)==eye
    assert all(G[a][b]!=R.zero for a in range(n) for b in range(n))
    assert len({G[a][a] for a in range(n)})==1
    assert all(R.add(G[a][b],R.conj(G[b][a]))==eye[a][b]
               for a in range(n) for b in range(n))


def complex_construction(n, arbitrary=False):
    R=ring_for(n)
    q=3**(n-1)
    zstep=R.order//3
    wstep=R.order//n
    if arbitrary:
        x=R.add(R.const(2),R.root(zstep))
        X=[[x if a==b else R.add(R.const(2*a-3*b+1),R.scale(R.root(zstep),a+b+2))
            for b in range(n)] for a in range(n)]
    else:
        x=R.one
        X=[[R.root(wstep*(a*b-b*b)) for b in range(n)] for a in range(n)]
    total=[[R.zero for _ in range(n)] for _ in range(n)]
    coeffs=[]
    for tail in product(range(3),repeat=n-1):
        t=(0,)+tail
        W,G=legal_orbit_matrices(R,n,t,R.const(-1),R.const(F(1,2)))
        assert_legal(R,W,G,R.const(-1))
        alpha=x
        for a in range(n):
            for b in range(n):
                if a!=b:
                    term=R.mul(X[a][b],R.root(-zstep*(t[a]-t[b])))
                    alpha=R.add(alpha,R.scale(term,1 if a>b else -1))
        alpha=R.scale(alpha,F(2,q))
        coeffs.append((t,alpha))
        for a in range(n):
            for b in range(n):
                total[a][b]=R.add(total[a][b],R.mul(alpha,G[a][b]))
    assert total==X
    sumalpha=R.zero
    for _,a in coeffs:
        sumalpha=R.add(sumalpha,a)
    assert sumalpha==R.scale(x,2)
    result={"N":n,"terms":q,"field_order":R.order,"field_degree":R.degree,
            "target":"arbitrary_constant_diagonal" if arbitrary else "column_gauged_positive_Fourier",
            "all_orbit_unitarity_cycle_holonomy_inverse_and_skew_checks":True,
            "exact_sum_matches_target":True,"sum_coefficients_equals_x_over_d":True}
    if n==4 and not arbitrary:
        witness=None
        for t,a in coeffs:
            if a==R.zero: continue
            for u,b in coeffs:
                abstar=R.mul(a,R.conj(b))
                defect=R.add(abstar,R.neg(R.conj(abstar)))
                if defect!=R.zero:
                    witness={"t":t,"u":u,"alpha_t":R.text(a),"alpha_u":R.text(b),
                             "alpha_t_conj_alpha_u_minus_conjugate":R.text(defect)}
                    break
            if witness: break
        assert witness
        result["explicit_noncollinearity_witness"]=witness
        wrong=[[R.root(wstep*(a*b+b*b)) for b in range(n)] for a in range(n)]
        assert len({wrong[a][a] for a in range(n)})>1
        result["wrong_positive_quadratic_gauge_rejected"]=True
    return result


def n3_real_witness():
    R=ring_for(3)
    w=R.root(2)
    h=R.root(4)
    d=R.scale(R.add(R.one,R.neg(w)),F(1,3))
    assert R.mul(d,R.add(R.one,R.neg(h)))==R.one
    table=[[4,4,1],[1,-2,1],[4,-2,-2]]
    S=[[R.zero for _ in range(3)] for _ in range(3)]
    for u,v in product(range(3),repeat=2):
        W,G=legal_orbit_matrices(R,3,(0,u,v),h,d)
        assert_legal(R,W,G,h)
        expression=R.one
        for exponent in (u,-u,v,-v,2-u+v,-2+u-v):
            expression=R.add(expression,R.root(2*exponent))
        assert expression==R.const(table[u][v])
        alpha=F(table[u][v],9)
        for a in range(3):
            for b in range(3):
                S[a][b]=R.add(S[a][b],R.scale(G[a][b],alpha))
    X=[[R.mul(d,R.root(2*(a*b-b*b))) for b in range(3)] for a in range(3)]
    assert S==X
    assert sum(sum(row) for row in table)==9
    assert all(R.add(X[a][b],R.conj(X[b][a]))==R.zero for a in range(3) for b in range(3) if a!=b)
    return {"N":3,"field_order":6,"nine_real_coefficients_numerator":table,"denominator":9,
            "exact_sum_matches_d_times_column_gauged_F3":True,"all_nine_resolvents_legal":True,
            "coefficient_sum":1,"offdiagonal_skew_Hermitian":True}


def boundary_controls():
    R=ring_for(2)
    W,G=legal_orbit_matrices(R,2,(0,0),R.const(-1),R.const(F(1,2)))
    assert_legal(R,W,G,R.const(-1))
    expected=[[R.const(F(1,2)),R.const(F(-1,2))],[R.const(F(1,2)),R.const(F(1,2))]]
    assert G==expected
    # N=1: allowing a weighted loop, W=-1 and 2(I-W)^(-1)=F1.
    assert R.scale(R.const(F(1,2)),2)==R.one
    # Singular holonomy H=1: the directed shift fixes the all-ones vector.
    n=4
    shift=[[int(a==(b+1)%n) for b in range(n)] for a in range(n)]
    assert all(sum((int(a==b)-shift[a][b]) for b in range(n))==0 for a in range(n))
    # Binary diagonal phases alias opposite directed entries, already at N=2.
    assert [(-1)**(0-t) for t in (0,1)]==[(-1)**(t-0) for t in (0,1)]
    # Two disjoint anti-periodic 2-cycles are unitary but cannot fill cross-block entries.
    B=[[R.zero for _ in range(4)] for _ in range(4)]
    H=[[R.zero for _ in range(4)] for _ in range(4)]
    for k in (0,2):
        for a in range(2):
            for b in range(2):
                B[k+a][k+b]=W[a][b]
                H[k+a][k+b]=G[a][b]
    assert matmul(R,[[R.conj(B[b][a]) for b in range(4)] for a in range(4)],B)==identity(R,4)
    assert H[0][2]==R.zero
    return {"N2_exact_single_positive_real_Green_witness":True,
            "N1_loop_allowed_exact_witness":True,
            "N1_without_loops_has_no_legal_cycle": "convention-dependent exclusion, not claimed",
            "H_equals_1_singularity_detected":True,
            "mod2_opposite_entry_character_collision_detected":True,
            "disjoint_cycle_cover_fails_full_support":True}


def character_controls():
    cases=[]
    for n in range(2,9):
        chars=[]
        for a in range(n):
            for b in range(n):
                if a==b: continue
                chars.append(tuple((int(k==a)-int(k==b))%3 for k in range(1,n)))
        zero=(0,)*(n-1)
        assert len(set(chars))==n*(n-1) and zero not in chars
        cases.append({"N":n,"nontrivial_distinct_characters":len(chars),"constant_diagonal_dimension":len(chars)+1})
    # Full exact Gram sums at N=4: a polynomial in zeta vanishes iff all
    # three coefficients coincide, using 1+zeta+zeta^2=0.
    n=4
    chars=[(0,0,0)] + [tuple((int(k==a)-int(k==b))%3 for k in range(1,n))
                       for a in range(n) for b in range(n) if a!=b]
    T=list(product(range(3),repeat=n-1))
    for i,x in enumerate(chars):
        for j,y in enumerate(chars):
            counts=Counter(sum((a-b)*t for a,b,t in zip(x,y,v))%3 for v in T)
            if i==j: assert counts=={0:27}
            else: assert [counts[k] for k in range(3)]==[9,9,9]
    return {"character_distinctness":cases,"N4_full_13_by_13_character_Gram":True}


def main():
    here=Path(__file__).resolve().parent
    results={"method":"fresh standard-library exact cyclotomic quotient-ring arithmetic; no imported or executed author programs",
             "python":platform.python_version(),"characters":character_controls(),
             "boundary_controls":boundary_controls(),"N3_real_witness":n3_real_witness(),
             "complex_constructions":[]}
    for n in range(2,7):
        results["complex_constructions"].append(complex_construction(n))
        print("PASS Fourier",n,flush=True)
    for n in (2,3,4):
        results["complex_constructions"].append(complex_construction(n,arbitrary=True))
        print("PASS arbitrary",n,flush=True)
    # Source hashes are recorded separately in SOURCE_MANIFEST.json.
    results["all_checks_passed"]=True
    (here/"EXACT_CHECK_RESULTS.json").write_text(json.dumps(results,indent=2)+"\n")
    print("All exact checks passed",flush=True)


if __name__=="__main__":
    main()
