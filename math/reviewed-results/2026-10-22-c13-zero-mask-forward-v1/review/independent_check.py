"""Reviewer-authored exact checks. Imports no constructor or historical code."""
from fractions import Fraction
from itertools import product
from collections import deque
from random import Random
from pathlib import Path
import json

class F:
    def __init__(self, p=None): self.p=p
    def n(self,x): return x%self.p if self.p else Fraction(x)
    def add(self,a,b): return self.n(a+b)
    def sub(self,a,b): return self.n(a-b)
    def mul(self,a,b): return self.n(a*b)
    def div(self,a,b):
        assert b
        return self.n(a*pow(int(b),-1,self.p)) if self.p else a/b

def ident(n): return [[int(i==j) for j in range(n)] for i in range(n)]
def diag(d): return [[d[i] if i==j else 0 for j in range(len(d))] for i in range(len(d))]
def pm(p): return [[int(j==p[i]) for j in range(len(p))] for i in range(len(p))]
def add(A,B,f): return [[f.add(x,y) for x,y in zip(a,b)] for a,b in zip(A,B)]
def sub(A,B,f): return [[f.sub(x,y) for x,y in zip(a,b)] for a,b in zip(A,B)]
def mul(A,B,f):
    n=len(A)
    return [[f.n(sum(A[i][k]*B[k][j] for k in range(n))) for j in range(n)] for i in range(n)]
def inv(A,f):
    n=len(A); a=[list(map(f.n,row))+e for row,e in zip(A,ident(n))]
    for j in range(n):
        r=next((i for i in range(j,n) if a[i][j]),None)
        if r is None: raise ValueError('singular')
        a[j],a[r]=a[r],a[j]
        d=a[j][j];a[j]=[f.div(v,d) for v in a[j]]
        for i in range(n):
            if i!=j:
                d=a[i][j];a[i]=[f.sub(x,f.mul(d,y)) for x,y in zip(a[i],a[j])]
    return [row[n:] for row in a]
def mv(A,v,f): return [f.n(sum(x*y for x,y in zip(row,v))) for row in A]
def flat(A): return tuple(x for row in A for x in row)
def cycles(p):
    unseen=set(range(len(p)));out=[]
    while unseen:
        u=min(unseen);c=[]
        while u in unseen: unseen.remove(u);c.append(u);u=p[u]
        assert u==c[0];out.append(c)
    return out

def cyclic_solve(p,w,b,f):
    """Uses one cycle denominator, never an edge inverse."""
    z=[f.n(0) for _ in p]
    for c in cycles(p):
        coeff=f.n(1);numer=f.n(0)
        for u in c:
            numer=f.add(numer,f.mul(coeff,b[u]));coeff=f.mul(coeff,w[u])
        z[c[0]]=f.div(numer,f.sub(f.n(1),coeff))
        for i in range(len(c)-1,0,-1):
            u=c[i];z[u]=f.add(b[u],f.mul(w[u],z[p[u]]))
    return z

def graph_mask(U,V,K,mask,f):
    """Fresh graph implementation of the mathematical criterion, not imported."""
    n=len(U);m=2*n;adj=[[] for _ in range(m)];eq=[]
    for i in range(n):
        for j in range(n):
            A=V[i][j];B=U[i][j];k=K[i][j];v=n+j
            if not A and not B:
                if k:return None
                continue
            eq.append((i,v,A,B,k))
            if A and B:
                adj[i].append((v,f.div(-A,B),f.div(k,B)))
                adj[v].append((i,f.div(-B,A),f.div(k,A)))
    ab={};cs=[]
    for start in range(m):
        if start in ab:continue
        c=[];ab[start]=(f.n(1),f.n(0));q=deque([start])
        while q:
            u=q.popleft();c.append(u);a,b=ab[u]
            for v,A,B in adj[u]:
                if v not in ab:
                    ab[v]=(f.mul(A,a),f.add(f.mul(A,b),B));q.append(v)
        cs.append(c)
    owner={v:i for i,c in enumerate(cs) for v in c};pins=[[] for _ in cs]
    for i,j,A,B,k in eq:
        ci=owner[i] if A else owner[j]
        a=f.add(f.mul(A,ab[i][0]),f.mul(B,ab[j][0]));b=f.add(f.mul(A,ab[i][1]),f.mul(B,ab[j][1]))
        if not a:
            if b!=k:return None
        else:pins[ci].append(f.div(f.sub(k,b),a))
    for v in range(m):
        if mask[v]:pins[owner[v]].append(f.div(-ab[v][1],ab[v][0]))
    out=[None]*m
    for ci,c in enumerate(cs):
        roots=pins[ci]
        if roots and any(t!=roots[0] for t in roots):return None
        candidates=[roots[0]] if roots else range(f.p if f.p else len(c)+1)
        selected=None
        for t in candidates:
            vals={v:f.add(f.mul(ab[v][0],t),ab[v][1]) for v in c}
            if all((vals[v]==0)==bool(mask[v]) for v in c):selected=vals;break
        if selected is None:return None
        for v,z in selected.items():out[v]=z
    assert all(f.add(f.mul(A,out[i]),f.mul(B,out[j]))==k for i,j,A,B,k in eq)
    return out

def exhaustive():
    result=[]
    for p,n in [(2,3),(3,2),(5,2)]:
        f=F(p);I=ident(n);cycle=list(range(1,n))+[0]
        w=[f.n(1) for _ in range(n)];w[0]=0
        z=[f.n(1) for _ in range(n)];z[-1]=0
        U=sub(I,mul(diag(w),pm(cycle),f),f)
        V=sub(I,mul(diag(z),pm(cycle),f),f)
        Ui=inv(U,f);Vi=inv(V,f)
        feasible={mask:set() for mask in product([False,True],repeat=2*n)}
        for xy in product(range(p),repeat=2*n):
            B=add(mul(Ui,diag(xy[:n]),f),mul(diag(xy[n:]),Vi,f),f)
            feasible[tuple(x==0 for x in xy)].add(flat(B))
        checks=0;yes=0
        for entries in product(range(p),repeat=n*n):
            B=[list(entries[i*n:(i+1)*n]) for i in range(n)];K=mul(mul(U,B,f),V,f)
            for mask,targets in feasible.items():
                got=graph_mask(U,V,K,mask,f)
                assert (got is not None)==(entries in targets),(p,n,entries,mask,got)
                if got is not None:
                    recovered=add(mul(Ui,diag(got[:n]),f),mul(diag(got[n:]),Vi,f),f)
                    assert recovered==B;yes+=1
                checks+=1
        result.append({'prime':p,'N':n,'target_mask_checks':checks,'accepted':yes})
    return result

def construction_checks():
    rng=Random(20261022);cases=0;columns=0;allzero=0;singular_branches=0;gauge_checks=0;nonzero_edges=0
    for p in [None,2,3,5,7]:
        f=F(p)
        for n in range(2,11):
            for mode in range(8):
                # Nontrivial endpoint permutations, two distinct cycle grammars.
                r0=list(range(n));s0=list(range(n));rng.shuffle(r0);rng.shuffle(s0)
                pi0=list(range(1,n))+[0]
                pi1=list(range(n-1,-1,-1))
                if n>=4:
                    cut=n//2
                    pi1=list(range(1,cut))+[0]+list(range(cut+1,n))+[cut]
                else:pi1=pi0[:]
                def nz():return f.n(rng.randrange(1,p) if p else rng.choice([1,2,3,-1,-2]))
                a=[nz() for _ in range(n)];d=[nz() for _ in range(n)]
                w0=[nz() for _ in range(n)];w1=[nz() for _ in range(n)]
                # Every cycle has a zero edge. No route changes or edge division.
                for c in cycles(pi0):w0[c[0]]=f.n(0)
                for c in cycles(pi1):w1[c[-1]]=f.n(0)
                if mode==5:w0=[f.n(0)]*n;w1=[f.n(0)]*n
                if mode>=6 and p!=2:
                    w0=[f.n(1)]*n;w1=[f.n(1)]*n
                    for c in cycles(pi0):w0[c[0]]=f.n(2)
                    for c in cycles(pi1):w1[c[-1]]=f.n(2)
                    nonzero_edges+=1
                W0=mul(diag(w0),pm(pi0),f);W1=mul(diag(w1),pm(pi1),f)
                G0=sub(ident(n),W0,f);G1=sub(ident(n),W1,f)
                U=mul(mul(diag(a),G0,f),pm(r0),f)
                V=mul(mul(pm(s0),G1,f),diag(d),f)
                Ui=inv(U,f);Vi=inv(V,f)
                if mode==0:x=[f.n(0)]*n;y=[f.n(0)]*n;allzero+=1
                elif mode==1:x=[f.n(0)]*n;y=[nz() for _ in range(n)]
                elif mode==2:x=[nz() for _ in range(n)];y=[f.n(0)]*n
                else:
                    x=[nz() if (i+mode)%3 else f.n(0) for i in range(n)]
                    y=[nz() if (i+mode)%2 else f.n(0) for i in range(n)]
                singular_branches+=int(any(t==0 for t in x))+int(any(t==0 for t in y))
                T0=mul(Ui,diag(x),f);T1=mul(diag(y),Vi,f);B=add(T0,T1,f)
                K=mul(mul(U,B,f),V,f)
                assert K==add(mul(U,diag(y),f),mul(diag(x),V,f),f)
                mask=tuple(t==0 for t in x+y);sol=graph_mask(U,V,K,mask,f);assert sol is not None
                assert add(mul(Ui,diag(sol[:n]),f),mul(diag(sol[n:]),Vi,f),f)==B
                lam=[nz() for _ in range(n)];mu=[nz() for _ in range(n)]
                Ug=mul(diag(lam),U,f);Vg=mul(V,diag(mu),f)
                xg=[f.mul(t,l) for t,l in zip(x,lam)];yg=[f.mul(t,l) for t,l in zip(y,mu)]
                assert tuple(t==0 for t in xg+yg)==mask
                assert add(mul(inv(Ug,f),diag(xg),f),mul(diag(yg),inv(Vg,f),f),f)==B
                gauge_checks+=1
                ri=inv(pm(r0),f);si=inv(pm(s0),f)
                for j in range(n):
                    e=[f.n(i==j) for i in range(n)]
                    q=[f.div(f.mul(x[i],e[i]),a[i]) for i in range(n)]
                    t0=mv(ri,cyclic_solve(pi0,w0,q,f),f)
                    q=mv(si,e,f);g=cyclic_solve(pi1,w1,q,f)
                    t1=[f.div(f.mul(y[i],g[i]),d[i]) for i in range(n)]
                    assert t0==[T0[i][j] for i in range(n)]
                    assert t1==[T1[i][j] for i in range(n)]
                    columns+=1
                cases+=1
    return dict(cases=cases,basis_columns=columns,allzero_masks=allzero,singular_branch_instances=singular_branches,gauge_checks=gauge_checks,all_nonzero_edge_cases=nonzero_edges)

def denominator_checks():
    cases=0
    for p in [2,3,5,7]:
        f=F(p)
        for n in [2,3,4]:
            pi=list(range(1,n))+[0]
            for w in product(range(p),repeat=n):
                q=1
                for x in w:q=f.mul(q,x)
                G=sub(ident(n),mul(diag(w),pm(pi),f),f)
                try:inv(G,f);invertible=True
                except ValueError:invertible=False
                assert invertible==(q!=1)
                if invertible:
                    b=[f.n(i+1) for i in range(n)]
                    assert mv(G,cyclic_solve(pi,w,b,f),f)==b
                cases+=1
    return cases

def controls():
    f=F(2);U=[[1,0],[0,1]];V=U;K=[[1,0],[0,0]]
    assert graph_mask(U,V,K,(False,False,False,False),f) is None
    assert graph_mask(U,V,K,(False,True,True,True),f)==[1,0,0,0]
    assert graph_mask(U,V,K,(True,True,True,True),f) is None
    assert graph_mask(U,V,[[0,1],[0,0]],(True,True,True,True),f) is None
    # A genuine two-sided singular endpoint is outside the accepted grammar.
    q=F();U=sub(ident(3),[[2*x for x in row] for row in pm([1,2,0])],q)
    Ui=inv(U,q);V=ident(3)
    B=mul(mul(diag([1,0,0]),Ui,q),diag([0,1,0]),q)
    assert B[0][1]==Fraction(-2,7) and Ui[2][1]==Fraction(-4,7)
    K=mul(U,B,q)
    assert all(graph_mask(U,V,K,mask,q) is None for mask in product([False,True],repeat=6))
    return ['F2 field exhaustion','mixed-mask feasible control','allzero rejects nonzero target','off-support rejection','two-sided singular endpoint not representable in one-sided grammar']

if __name__=='__main__':
    result={'status':'PASS','execution_scope':'Reviewer-authored program only; no supplied programs imported or executed.','exhaustive':exhaustive(),'construction':construction_checks(),'cycle_denominator_cases':denominator_checks(),'controls':controls()}
    Path(__file__).with_name('INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
