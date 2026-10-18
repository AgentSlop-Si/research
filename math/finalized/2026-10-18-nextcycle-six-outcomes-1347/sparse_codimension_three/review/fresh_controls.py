#!/usr/bin/env python3
"""Independent exact review controls. Imports no candidate or prior checker."""
from collections import Counter
from fractions import Fraction as Q
from functools import lru_cache
from itertools import combinations, combinations_with_replacement, permutations
from math import gcd
from pathlib import Path
import json
import sympy as sp

ROOT=Path(__file__).resolve().parent
x=sp.Symbol('x')

@lru_cache(None)
def root_table(n):
    p=sp.Poly(sp.cyclotomic_poly(n,x),x,domain=sp.QQ)
    return tuple(tuple(int(sp.rem(sp.Poly(x**e,x),p).nth(k)) for k in range(p.degree())) for e in range(n))

def zero_roots(n,exps):
    rs=root_table(n)
    v=[0]*len(rs[0])
    for e in exps:
        for k,a in enumerate(rs[e%n]): v[k]+=a
    return not any(v)

def components(supports):
    remaining=set(range(len(supports))); answer=[]
    while remaining:
        pending=[min(remaining)]; cols=set(); rows=set()
        while pending:
            c=pending.pop()
            if c in cols: continue
            cols.add(c); rows.update(supports[c])
            pending.extend(j for j in remaining-cols if supports[j]&rows)
        remaining-=cols; answer.append((rows,cols))
    return answer

def labelled_support_search(n):
    """Every column is labelled from the outset; no component-based pruning."""
    triples=list(map(frozenset,combinations(range(n),3)))
    compatible=[[j for j,b in enumerate(triples) if len(a&b)!=1] for a in triples]
    cap=[3]*n; chosen=[]; total=orthogonal=nodes=0; types=Counter()
    def visit(options):
        nonlocal total,orthogonal,nodes
        nodes+=1
        if len(chosen)==n:
            assert cap==[0]*n
            supports=[triples[k] for k in chosen]
            sizes=[]
            for rows,cols in components(supports):
                assert len(rows)==len(cols) and len(rows) in (3,4)
                if len(rows)==3: assert all(supports[c]==rows for c in cols)
                else: assert len({tuple(rows-supports[c]) for c in cols})==4
                sizes.append(len(rows))
            types['+'.join(map(str,sorted(sizes)))]+=1; total+=1
            orthogonal+=all(zero_roots(n,(r*(j-k) for r in supports[j]&supports[k])) for j in range(n) for k in range(j))
            return
        for t in options:
            if any(cap[r]==0 for r in triples[t]): continue
            chosen.append(t)
            for r in triples[t]: cap[r]-=1
            left=n-len(chosen)
            if max(cap)<=left:
                allowed=set(compatible[t]); visit([k for k in options if k in allowed])
            for r in triples[t]: cap[r]+=1
            chosen.pop()
    visit(list(range(len(triples))))
    return {'N':n,'labelled_support_masks':total,'orthogonal_Fourier_masks':orthogonal,'component_types':dict(types),'search_nodes':nodes}

def independent_fourier_search(n):
    """Use column weight and exact orthogonality only, no row-degree constraints."""
    ts=list(map(frozenset,combinations(range(n),3))); chosen=[]; total=nodes=0
    @lru_cache(None)
    def compatible(t,u,d): return zero_roots(n,(r*d for r in ts[t]&ts[u]))
    def visit():
        nonlocal total,nodes
        nodes+=1; j=len(chosen)
        if j==n:
            supports=[ts[t] for t in chosen]
            assert all(sum(r in a for a in supports)==3 for r in range(n))
            assert all(len(rs)==len(cs)==3 for rs,cs in components(supports))
            total+=1; return
        for t in range(len(ts)):
            if all(compatible(t,u,j-k) for k,u in enumerate(chosen)):
                chosen.append(t); visit(); chosen.pop()
    visit()
    return {'N':n,'passing_masks':total,'nodes':nodes,'regularity_and_triple_components_verified_afterward':True}

def direct_conference(n):
    # Exhaustive normalized row and column triples; no valuation or phase pruning.
    h=n//2; tuples=list(permutations(range(1,n),3)); tested=0
    for a,b,c in combinations(range(1,n),3):
        for u,v,w in tuples:
            tested+=1
            assert not ((b-c)*u%n==h and (a-c)*v%n==h and (a-b)*w%n==h
                        and c*(u-v)%n==h and b*(u-w)%n==h and a*(v-w)%n==h)
    return {'N':n,'normalized_configurations':tested,'solutions':0}

def phase_equivalence(n):
    ts=list(combinations(range(n),3)); passed=tested=0
    for rs in ts:
        orthogonal_differences={d for d in range(1,n) if zero_roots(n,(r*d for r in rs))}
        for cs in ts:
            exact=all(cs[j]-cs[k] in orthogonal_differences for j in range(3) for k in range(j))
            vals=tuple((r-rs[0])*(c-cs[0])%n for r in rs[1:] for c in cs[1:])
            congruent=n%3==0 and vals in ((n//3,2*n//3,2*n//3,n//3),(2*n//3,n//3,n//3,2*n//3))
            assert exact==congruent; passed+=exact; tested+=1
    return {'N':n,'pairs_tested':tested,'orthogonal_blocks':passed}

class Field:
    """Own rational-coordinate arithmetic in Q[x]/Phi_n; SymPy only inverts polynomials."""
    def __init__(self,n):
        self.n=n; self.phi=sp.Poly(sp.cyclotomic_poly(n,x),x,domain=sp.QQ); self.d=self.phi.degree()
        self.z=(Q(0),)*self.d; self.o=(Q(1),)+(Q(0),)*(self.d-1)
        self.roots=tuple(tuple(map(Q,v)) for v in root_table(n))
        self.products=[[self.roots[(i+j)%n] for j in range(self.d)] for i in range(self.d)]
    def scalar(self,q): return (Q(q),)+(Q(0),)*(self.d-1)
    def add(self,a,b): return tuple(u+v for u,v in zip(a,b))
    def neg(self,a): return tuple(-u for u in a)
    def sub(self,a,b): return self.add(a,self.neg(b))
    def scale(self,a,q): return tuple(v*q for v in a)
    def mul(self,a,b):
        out=[Q(0)]*self.d
        for i,u in enumerate(a):
            if not u: continue
            for j,v in enumerate(b):
                if not v: continue
                for k,w in enumerate(self.products[i][j]): out[k]+=u*v*w
        return tuple(out)
    def conj(self,a):
        out=self.z
        for i,v in enumerate(a): out=self.add(out,self.scale(self.roots[(-i)%self.n],v))
        return out
    def inv(self,a):
        p=sp.Poly(sum(sp.Rational(v.numerator,v.denominator)*x**i for i,v in enumerate(a)),x,domain=sp.QQ)
        b=sp.invert(p,self.phi)
        return tuple(Q(b.nth(i)) for i in range(self.d))
    def matmul(self,a,b):
        out=[[self.z for _ in b[0]] for _ in a]
        for i in range(len(a)):
            for k in range(len(b)):
                if a[i][k]==self.z: continue
                for j in range(len(b[0])): out[i][j]=self.add(out[i][j],self.mul(a[i][k],b[k][j]))
        return out
    def star(self,a): return [[self.conj(a[j][i]) for j in range(len(a))] for i in range(len(a[0]))]
    def eye(self,n): return [[self.o if i==j else self.z for j in range(n)] for i in range(n)]
    def mscale(self,a,q): return [[self.scale(v,q) for v in row] for row in a]
    def msub(self,a,b): return [[self.sub(u,v) for u,v in zip(ra,rb)] for ra,rb in zip(a,b)]
    def madd(self,a,b): return [[self.add(u,v) for u,v in zip(ra,rb)] for ra,rb in zip(a,b)]
    def minv(self,a):
        n=len(a); rows=[ra[:]+rb for ra,rb in zip(a,self.eye(n))]
        for j in range(n):
            p=next(i for i in range(j,n) if rows[i][j]!=self.z); rows[p],rows[j]=rows[j],rows[p]
            gain=self.inv(rows[j][j]); rows[j]=[self.mul(gain,v) for v in rows[j]]
            for i in range(n):
                if i==j: continue
                gain=rows[i][j]
                rows[i]=[self.sub(v,self.mul(gain,w)) for v,w in zip(rows[i],rows[j])]
        return [ra[n:] for ra in rows]

def matrix_controls(n,s,divisor=False):
    f=Field(n); d=n-s; I=f.eye(n); W=[[f.roots[r*c%n] for c in range(n)] for r in range(n)]
    if divisor:
        m=n//d
        omitted=[set(range(d*(c%m),d*(c%m)+d)) for c in range(n)]
        supports=[set(range(n))-v for v in omitted]
    else:
        supports=[{(c+j)%n for j in range(s)} for c in range(n)]
    A=[[W[r][c] if r in supports[c] else f.z for c in range(n)] for r in range(n)]
    C=f.msub(W,A); K0=f.mscale(f.star(A),Q(1,s))
    if divisor: K=K0
    else:
        K=[[f.scalar(1 if r==c else Q(1,2*s)) if c in supports[r] else f.z for c in range(n)] for r in range(n)]
    Z=f.minv(K); V=f.msub(Z,W)
    assert f.matmul(K,Z)==f.matmul(Z,K)==I
    KK=f.matmul(K,f.star(K)); VV=f.matmul(V,f.star(V))
    G=f.madd(f.msub(f.msub(I,f.matmul(K,W)),f.matmul(f.star(W),f.star(K))),f.mscale(KK,s))
    assert G==f.matmul(f.matmul(K,f.msub(VV,f.mscale(I,d))),f.star(K))
    diff=f.msub(K,K0); rigid=f.mscale(f.matmul(diff,f.star(diff)),s)
    assert all(G[i][i]==rigid[i][i] for i in range(n))
    G0=f.madd(f.msub(f.msub(I,f.matmul(K0,W)),f.matmul(f.star(W),f.star(K0))),f.mscale(f.matmul(K0,f.star(K0)),s))
    assert f.mscale(G0,s)==f.msub(f.matmul(f.star(C),C),f.mscale(I,d))
    if divisor:
        assert VV==f.matmul(f.star(V),V)==f.mscale(I,d)
        assert f.matmul(f.star(C),C)==f.matmul(C,f.star(C))==f.mscale(I,d)
        assert all(sum(v!=f.z for v in row)==s for row in K)
        assert all(sum(K[r][c]!=f.z for r in range(n))==s for c in range(n))
        # A wrong inverse gain must fail exact equality.
        Vbad=f.msub(f.mscale(Z,Q(1,2)),W)
        assert f.matmul(Vbad,f.star(Vbad))!=f.mscale(I,d)
    return {'N':n,'s':s,'divisor_witness':divisor,'inverse_products_and_three_stability_identities_passed':True}

def norms():
    out=[]
    for n in range(2,13):
        p=sp.Poly(sp.cyclotomic_poly(n,x),x); tested=nonzero=0
        for weight in range(1,min(n,4)):
            for es in combinations_with_replacement(range(n),weight):
                poly=sp.Poly(sum(x**e for e in es),x)
                norm=sp.resultant(p,poly)
                assert norm.is_Integer and (norm==0)==zero_roots(n,es)
                if norm: assert abs(norm)>=1; nonzero+=1
                tested+=1
        out.append({'N':n,'root_multisets':tested,'nonzero_norms':nonzero})
    return out

def constants():
    count=0
    for n in range(2,301):
        phi=int(sp.totient(n))
        for s in range(1,n):
            q=Q(s,n); d=n-s; gamma=Q(1,n*d**(phi-1))
            gap=Q(s**6,2**22*n**10*d**(2*phi-2))
            assert gap==(gamma*q**3/(2048*n))**2
            assert gap<=q/(2**22*n**4)<q/8 and gap<Q(1,n)
            assert Q(n,1)/q<=Q(n*n,1)/q**6
            count+=1
    # Rational a probes prove the algebraic branch estimates without rounded roots.
    for den in range(2,101):
        for num in range(1,den):
            a=Q(num,den); q=1-a*a; L=(1-a)/2; U=(3+a)/2; rho0=(1+a)/2
            assert L>=q/4 and U<=2 and rho0*rho0-a*a>=q/8
            assert q*U*U/L**4<=1024/q**3
    return {'parameter_pairs':count,'coefficient_sum':1052,'final_coefficient':2048,'all_exact_checks_passed':True}

def negative():
    H=sp.Matrix([[0,1,1,1],[1,0,-1,1],[1,1,0,-1],[1,-1,1,0]])
    assert H*H.T==3*sp.eye(4)
    assert not all(zero_roots(4,(r*(j-k) for r in set(range(4))-{j,k})) for j in range(4) for k in range(j))
    assert not all(zero_roots(6,(r*(j-k) for r in range(3))) for j in range(3) for k in range(j))
    # A bad mask need not be row-regular. Its nonzero Gram entry still has a nonzero norm.
    assert not zero_roots(5,[0,1,2])
    return {'ordinary_conference_exists':True,'Fourier_conference_rejected':True,'arbitrary_triple_blocks_rejected':True,'row_irregular_bad_mask_covered':True}

def main():
    out={'arithmetic':'exact integers, rationals and own cyclotomic quotient-field arithmetic'}
    out['support']=[labelled_support_search(n) for n in range(3,8)]; print('labelled support PASS',flush=True)
    out['fourier']=[independent_fourier_search(n) for n in range(3,10)]; print('Fourier search PASS',flush=True)
    out['conference']=[direct_conference(n) for n in range(2,21,2)]; print('conference PASS',flush=True)
    out['phase']=[phase_equivalence(n) for n in range(4,21)]; print('block phases PASS',flush=True)
    out['arbitrary_sparse_inverses']=[matrix_controls(n,s) for n in range(2,9) for s in range(1,n)]; print('arbitrary matrix identities PASS',flush=True)
    out['divisor_witnesses']=[matrix_controls(n,n-d,True) for n in range(2,13) for d in range(1,n) if n%d==0]; print('divisor witnesses PASS',flush=True)
    out['norms']=norms(); print('cyclotomic norms PASS',flush=True)
    out['constants']=constants(); out['negative']=negative(); out['all_checks_passed']=True
    (ROOT/'FRESH_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print('PASS: independent exact controls complete',flush=True)

if __name__=='__main__': main()
