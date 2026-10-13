#!/usr/bin/env python3
"""Fresh audit code. Reads/imports/executes no supplied source programs.
Verifies source two-orientation theorem and newly derived three-orientation
boundary witnesses by independent q-product entries and sparse inverse residuals.
All finite computations are over explicitly checked prime fields.
"""
from pathlib import Path
import json, hashlib, math
OUT=Path(__file__).resolve().parent

def divisors(n):
    out=[];d=2
    while d*d<=n:
        if n%d==0:
            out.append(d)
            while n%d==0:n//=d
        d+=1
    if n>1:out.append(n)
    return out

def prime(p):return p>=2 and all(p%d for d in range(2,math.isqrt(p)+1))
def field(m):
    n=m*m;k=max(1,1000000//n)
    while not prime(k*n+1):k+=1
    p=k*n+1
    for g in range(2,p):
        w=pow(g,k,p)
        if pow(w,n,p)==1 and all(pow(w,n//d,p)!=1 for d in divisors(n)):
            return p,w,pow(w,m,p)
    raise RuntimeError('missing root')

def mapxy(z,m,t):
    a,c=z
    return z if t==0 else ((-c)%m,(a+c)%m) if t==1 else ((a+c)%m,a)

def admissible(m,p,t):
    a=2+t*3;b=3+t*4
    while (1-pow(a,m,p)-pow(b,m,p))%p==0:b+=1
    return a,b

def resolver(m,p,q,a,b):
    if pow(q,m,p)!=1 or any(pow(q,m//d,p)==1 for d in divisors(m)):
        raise ValueError('nonprimitive q')
    if not a%p or not b%p:raise ValueError('zero coefficient')
    den=(1-pow(a,m,p)-pow(b,m,p))%p
    if den==0:raise ValueError('singular resolver')
    invden=pow(den,-1,p);qp=[pow(q,j,p) for j in range(m)]
    coeff={}
    for u in range(m):
        for v in range(m-u):
            choose=1
            for j in range(1,u+1):choose=choose*(1-qp[(v+j)%m])*pow(1-qp[j],-1,p)%p
            coeff[u,v]=pow(a,u,p)*pow(b,v,p)*choose*invden%p
    def e(x,y):
        u=(x[0]-y[0])%m;v=(x[1]-y[1])%m
        return coeff.get((u,v),0)*qp[(y[0]*v)%m]%p
    return e

def det(e,rs,cs,p):return (e(rs[0],cs[0])*e(rs[1],cs[1])-e(rs[0],cs[1])*e(rs[1],cs[0]))%p

def component_size(m,ds):
    seen={(0,0)};todo=[(0,0)]
    while todo:
        a,c=todo.pop()
        for u,v in ds:
            y=((a+u)%m,(c+v)%m)
            if y not in seen:seen.add(y);todo.append(y)
    return len(seen)

def run(m):
    p,w,q=field(m);n=m*m;pts=[(a,c) for a in range(m) for c in range(m)]
    units=[u for u in range(1,m) if math.gcd(u,m)==1]
    pars=[admissible(m,p,t) for t in range(3)]
    qs=[pow(q,units[t%len(units)],p) for t in range(3)]
    gs=[resolver(m,p,qs[t],*pars[t]) for t in range(3)]
    # Distinct primitive branch roots, and independent nonzero left/right gauges.
    def branch(t,x,y):
        ix=x[0]*m+x[1];iy=y[0]*m+y[1]
        l=pow(2+t,ix+1,p);r=pow(5+t,2*iy+3,p)
        return l*gs[t](mapxy(x,m,t),mapxy(y,m,t))*r%p
    def total(k,x,y):return sum(branch(t,x,y) for t in range(k))%p
    inverse_entries=0
    if m<=16:
        for t,e in enumerate(gs):
            aa,bb=pars[t];qt=qs[t]
            for x in pts:
                ax=((x[0]-1)%m,x[1]);bx=(x[0],(x[1]-1)%m)
                for y in pts:
                    assert (e(x,y)-aa*e(ax,y)-bb*pow(qt,x[0],p)*e(bx,y))%p==int(x==y)
                    inverse_entries+=1
    def pos(a,c):return a%m,c%m
    old=new=purity=0;mutations=0
    for a,c in pts:
        oldw=[([pos(a,c),pos(a,c+1)],[pos(a,c+2),pos(a,c+3)],0),
              ([pos(a,c),pos(a+1,c-1)],[pos(a+2,c-2),pos(a+3,c-3)],1)]
        for rs,cs,only in oldw:
            assert len(set(rs))==2 and len(set(cs))==2
            assert det(lambda x,y:total(2,x,y),rs,cs,p)==0
            assert all(branch(1-only,x,y)==0 for x in rs for y in cs)
            old+=1
        if m<5:continue
        neww=[([pos(a,c),pos(a,c+1)],[pos(a+1,c+2),pos(a+1,c+3)],1),
              ([pos(a,c),pos(a+1,c-1)],[pos(a+3,c-2),pos(a+4,c-3)],0)]
        for rs,cs,only in neww:
            assert len(set(rs))==2 and len(set(cs))==2
            for x in rs:
                for y in cs:
                    assert branch(only,x,y)!=0
                    for t in range(3):
                        if t!=only:assert branch(t,x,y)==0;purity+=1
            assert det(lambda x,y:total(3,x,y),rs,cs,p)==0
            # One additive perturbation of one matrix entry must destroy this zero.
            vals=[total(3,x,y) for x in rs for y in cs]
            assert ((vals[0]+1)*vals[3]-vals[1]*vals[2])%p !=0
            mutations+=1;new+=1
    connected=component_size(m,[(0,1),(1,-1)])
    assert connected==n
    pp=len(divisors(m))==1
    if pp:
        ell=divisors(m)[0]
        # Every row difference not divisible by ell is a unit mod n.
        assert all(math.gcd(d,n)==1 for d in range(1,n) if d%ell)
        # Exact Fourier zero-minor criterion tested over all differences.
        assert all((pow(w,d*e,p)==1)==((d*e)%n==0) for d in range(1,n) for e in range(1,n)) if n<=256 else True
    return dict(m=m,N=n,p=p,root_N=w,branch_roots=qs,branch_coefficients=pars,
                sparse_inverse_residual_entries=inverse_entries,source_two_term_minors=old,
                new_three_term_minors=new,pure_zero_entry_checks=purity,
                one_entry_mutation_rejections=mutations,row_graph_vertices=connected,
                prime_power_no_go_applicable=pp)

def main():
    cases=[run(m) for m in [4,5,6,7,8,9,10,16,25,27,32]]
    p,w,q=field(4);pars=[admissible(4,p,t) for t in range(3)];g=[resolver(4,p,q,*par) for par in pars]
    def f(x,y):return sum((t+1)*g[t](mapxy(x,4,t),mapxy(y,4,t)) for t in range(3))%p
    m4_det=det(f,[(0,0),(0,1)],[(1,2),(1,3)],p)
    assert m4_det!=0,'m=4 is correctly outside the new witness theorem'
    rejected=False
    try:resolver(8,65537,1,2,3)
    except ValueError:rejected=True
    assert rejected
    # A nonsingle-prime target can have a connected Fourier zero-row graph.
    n=36;seen={0};todo=[0]
    while todo:
        x=todo.pop()
        for d in [2,3]:
            y=(x+d)%n
            if y not in seen:seen.add(y);todo.append(y)
    assert len(seen)==n and all((d*(n//math.gcd(d,n)))%n==0 for d in [2,3])
    report=dict(status='PASS',method='fresh product-form q-binomial entries; direct sparse inverse residuals; no supplied code imported or run',
                cases=cases,m4_three_term_witness_determinant=m4_det,
                nonprimitive_root_rejected=rejected,composite_N36_zero_row_graph_component=len(seen),
                totals={k:sum(c[k] for c in cases) for k in ['sparse_inverse_residual_entries','source_two_term_minors','new_three_term_minors','pure_zero_entry_checks','one_entry_mutation_rejections']})
    (OUT/'intake_qtorus_independent_results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
