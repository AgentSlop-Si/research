#!/usr/bin/env python3
"""Fresh finite controls. No code or coefficients are imported from prior packets."""
from fractions import Fraction as F
from math import comb, factorial
import json, time
from pathlib import Path
OUT=Path(__file__).resolve().parent

def run(p):
    h=(p-1)//2; L=p+3*h; W=p+L; cutoff=W+2; e=p*(p-1)
    assert W<e
    c=pow(-1,h+1,p)
    d=1
    for i in range(1,p-1,2):d=d*i%p
    alpha=F(2*p-1,2*p); gamma=F(p+1,4)
    # Sparse bivariate polynomials in X,T over F_p; omit T^cutoff and above.
    def clean(a):return {k:v%p for k,v in a.items() if v%p and k[1]<cutoff}
    def add(a,b,sign=1):
        z=dict(a)
        for k,v in b.items():z[k]=(z.get(k,0)+sign*v)%p
        return clean(z)
    def mul(a,b):
        z={}
        for (i,j),v in a.items():
            for (k,l),w in b.items():
                if j+l<cutoff:z[i+k,j+l]=(z.get((i+k,j+l),0)+v*w)%p
        return clean(z)
    def shiftx(a,n=1):return {(i+n,j):v for (i,j),v in a.items()}
    def deriv(a):return clean({(i-1,j):i*v for (i,j),v in a.items() if i})
    def edge(n):return {(0,j):(-comb(n,j))%p for j in range(1,min(n,cutoff-1)+1) if comb(n,j)%p}
    def path(a,b):
        if b<a:return {(0,0):1}
        prev,cur={(0,0):1},{(1,0):1}
        for j in range(a,b):prev,cur=cur,add(shiftx(cur),mul(edge(j),prev),-1)
        return cur
    def residual(poly,beta,target):
        result={}; worst=None
        for (i,j),a in poly.items():
            excess=F(j)+i*beta-target
            if worst is None or excess<worst:worst=excess
            assert excess>=0,(p,'negative weight',i,j,str(excess))
            if excess==0:result[i]=(result.get(i,0)+a)%p
        return {i:a for i,a in result.items() if a},str(worst)
    def polygon(poly):
        points=[]
        for i in sorted({i for i,j in poly}):points.append((i,min(j for k,j in poly if k==i)))
        hull=[]
        for pt in points:
            while len(hull)>1:
                a,b=hull[-2:]
                if (b[1]-a[1])*(pt[0]-b[0]) >= (pt[1]-b[1])*(b[0]-a[0]):hull.pop()
                else:break
            hull.append(pt)
        return hull
    G=path(1,3*p); V=path(1,3*p-1); new=path(1,3*p+1)
    assert new==add(shiftx(G),mul(edge(3*p),V),-1)
    A0=path(1,p);A1=path(p+1,2*p);T=path(2*p+1,3*p-1)
    L0=path(1,p-1);R1=path(p+2,2*p);L1=path(p+1,2*p-1)
    U=path(2*p+2,3*p-1);M=path(p+2,2*p-1)
    rhs=mul(mul(A0,A1),T)
    rhs=add(rhs,mul(edge(p),mul(mul(L0,R1),T)),-1)
    rhs=add(rhs,mul(edge(2*p),mul(mul(A0,L1),U)),-1)
    rhs=add(rhs,mul(mul(edge(p),edge(2*p)),mul(mul(L0,M),U)))
    assert V==rhs
    checks={}
    def check(name,poly,beta,target,expected):
        r,gap=residual(poly,beta,target)
        expected={i:a%p for i,a in expected.items() if a%p}
        assert r==expected,(p,name,r,expected)
        checks[name]={'residual':r,'minimum_excess':gap}
    check('accepted_G_outer',G,alpha,3*p*alpha,{3*p:1,p:-3})
    check('accepted_G_inner',G,F(1),3*p-1,{p:-3,1:-3*c})
    check('accepted_G_derivative',deriv(G),alpha,3*p-2,{2*p:3*c,0:-3*c})
    check('V_outer',V,alpha,L,{2*p:d,0:-d})
    check('V_inner',V,F(1),L,{0:-d})
    check('F_outer',new,alpha,(3*p+1)*alpha,{3*p+1:1,p+1:-3})
    check('F_inner',new,F(1),3*p,{p+1:-3,2:-3*c})
    check('F_deep',new,gamma,W,{2:-3*c,0:-3*d})
    # R = X F' - F has a global derivative residual appropriate at an F root.
    R=add(shiftx(deriv(new)),new,-1)
    rr=add(shiftx(deriv(G),2),mul(edge(3*p),add(V,shiftx(deriv(V)),-1)))
    assert R==rr
    check('root_derivative_outer',R,alpha,2*alpha+3*p-2,{2*p+2:3*c,2:-3*c})
    check('F_inner_derivative',deriv(new),F(1),3*p-1,{p:-3,1:-6*c})
    check('F_deep_derivative',deriv(new),gamma,W-gamma,{1:-6*c})
    expected_hull=[(0,W),(2,3*p-2),(p+1,2*p-1),(3*p+1,0)]
    hull=polygon(new);assert hull==expected_hull,(p,hull,expected_hull)
    assert 6*c%p and -3*c%p and -6*c%p
    disc=2*p*(3*p-2+alpha)+(p-1)*(3*p-1)+2*(W-gamma)
    assert disc==9*p*p+F(p-7,2) and disc.denominator==1
    return {'p':p,'s_min':2,'e':e,'cutoff':cutoff,'W':W,'L':L,'alpha':str(alpha),'gamma':str(gamma),'newton_vertices':hull,'ordinary_discriminant_valuation':int(disc),'checks':checks}

if __name__=='__main__':
    t=time.time(); rows=[run(p) for p in [5,7,11,13,17,19,23]]
    data={'status':'PASS','scope':'Finite transcription checks only; the symbolic proof gives the infinite-prime theorem.','elapsed_seconds':time.time()-t,'cases':rows}
    (OUT/'UNIFORM_CHECKS.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({'status':data['status'],'primes':[r['p'] for r in rows],'elapsed_seconds':data['elapsed_seconds']}))
