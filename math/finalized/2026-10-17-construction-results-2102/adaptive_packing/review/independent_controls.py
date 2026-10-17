#!/usr/bin/env python3
"""Independent exact arithmetic checks; imports no reviewed implementation.
Finite controls are diagnostics, never the asymptotic proof.
"""
from fractions import Fraction as F
from functools import lru_cache
from math import gcd, lcm, comb, isqrt
import hashlib, json
from pathlib import Path
HERE=Path(__file__).resolve().parent
SOURCE=Path(__file__).resolve().parent.parent/'candidate/REPORT.md'

def flog2(q):
    q=F(q); a,b=q.numerator,q.denominator
    k=a.bit_length()-b.bit_length()
    if k>=0:
        return k-int(a<(b<<k))
    return k-int((a<<(-k))<b)

@lru_cache(None)
def plan(r):
    L=lcm(*range(1,r+1)); d=L//r
    primepowers=[]; rem=d; p=2
    while p*p<=rem:
        if rem%p:
            p+=1; continue
        q=1
        while rem%p==0:
            q*=p; rem//=p
        primepowers.append((p,q)); p+=1
    if rem>1: primepowers.append((rem,rem))
    k=0
    for p,q in primepowers:
        u=p
        while u*p<=r:u*=p
        residue=(-pow(L//u,-1,q))%q
        D=d//q
        k+=residue*D*pow(D,-1,q)
    k=k%d if d>1 else 1
    assert 0<k<=max(1,d-1)
    P=1+k*L
    top=comb(P+r-1,r)
    assert top%d==0
    beta=top//d
    s=beta.bit_length()-1
    assert beta>comb(P+r-2,r-1)
    return P,s

def partition(R,D,C):
    c=C.bit_length(); cells=[(F(1<<R),F(3*(1<<(R-1))),F(1),())]
    stage_counts=[]
    for j in range(D):
        children=[]
        for lo,hi,alpha,path in cells:
            rlo=flog2(alpha*lo+c); rhi=flog2(alpha*hi+c)
            assert rhi-rlo<=1
            per_parent=0
            for r in range(rlo,rhi+1):
                a=max(lo,F((1<<r)-c)/alpha)
                b=min(hi,F((1<<(r+1))-c)/alpha)
                if not a<b:continue
                P,s=plan(r)
                qlo=flog2(2*(alpha*a/s+1)*C*C)//8
                qhi=flog2(2*(alpha*b/s+1)*C*C)//8
                assert qhi-qlo<=1
                for q in range(qlo,qhi+1):
                    low=max(a,(F(1<<(8*q),2*C*C)-1)*s/alpha)
                    high=min(b,(F(1<<(8*q+8),2*C*C)-1)*s/alpha)
                    if not low<high:continue
                    w=8*(q+1)
                    children.append((low,high,alpha*F(w,s),path+((r,s,w),)))
                    per_parent+=1
            assert per_parent<=4
        cells=sorted(children,key=lambda cell:cell[0])
        assert cells[0][0]==1<<R and cells[-1][1]==3*(1<<(R-1))
        assert all(a[1]==b[0] for a,b in zip(cells,cells[1:]))
        assert sum((b-a for a,b,_,_ in cells),F(0))==1<<(R-1)
        assert len(cells)<=4**(j+1)
        stage_counts.append(len(cells))
    lo,hi,alpha,path=max(cells,key=lambda cell:cell[1]-cell[0])
    S=1
    for r,s,w in path:S*=s
    E=(lo//S+1)*S
    assert lo<E<hi
    e=E; levels=[]
    for r,s,w in path:
        P,s2=plan(r)
        assert s==s2 and e%s==0 and c<s and C<P
        assert (e+c).bit_length()-1==r
        K=e//s
        w2=8*(( (2*(K+1)*C*C).bit_length()+7)//8)
        assert w==w2
        ep=K*w
        assert ep+c<e+c
        V=F((2*r-1)*(ep+c),e+c)
        levels.append({'rank':r,'block_bits':s,'slot_bits':w,'volume':float(V),
                       'volume_numerator':V.numerator,'volume_denominator':V.denominator})
        e=ep
    return {'R':R,'D':D,'cell_counts_by_stage':stage_counts,
            'selected_cell_width_over_S':str((hi-lo)/S),'selected_modulus_bits':S.bit_length(),
            'root_exponent':E,'levels':levels,
            'all_volumes_exceed_six_fifths':all(F(x['volume_numerator'],x['volume_denominator'])>=F(6,5) for x in levels)}

def small_actual_control():
    R=17; C=(1<<(3*R//4-1))+1
    record=partition(R,1,C); E=record['root_exponent']; P,s=plan(R)
    assert E%s==0; K=E//s; w=record['levels'][0]['slot_bits']
    X=C<<E; Y=X+P; H=C<<(K*w)
    assert X.bit_length()==E+C.bit_length() and Y%2==1
    def bn(x,j):
        return comb(x,j) if x>=j>=0 else (0 if x>=0 else (-1)**j*comb(-x+j-1,j))
    def norm(x):return sum(abs(bn(x,j)) for j in range(R))
    shift=min(range(R),key=lambda a:(max(norm(-a),norm(2*R-2-a)),a))
    xs=list(range(-shift,2*R-1-shift)); children=[]
    for x in xs:
        U=H-x; children.append(U)
        assert U.bit_length()==H.bit_length()
        assert U*U==(C*C<<(2*K*w))-(2*C*x<<(K*w))+x*x
    assert len(set(children))==2*R-1
    assert sum(z%2 for z in children)>=R-1
    assert Y*Y==P*P+(2*C*P<<E)+(C*C<<(2*E))
    # Verify the three ordinary column evaluations at -P, independently.
    def interp(vals,t):
        coeff=[]
        while vals:
            coeff.append(vals[0]); vals=[b-a for a,b in zip(vals,vals[1:])]
        return sum(a*bn(t-xs[0],j) for j,a in enumerate(coeff))
    assert interp([x*x for x in xs],-P)==P*P
    assert interp([-2*C*x for x in xs],-P)==2*C*P
    assert interp([C*C for x in xs],-P)==C*C
    return {'rank':R,'root_bits':Y.bit_length(),'child_bits':H.bit_length(),
            'distinct_children':len(set(children)),'odd_children':sum(z%2 for z in children),
            'shared_three_term_and_interpolation':'passed'}

if __name__=='__main__':
    out={'portable_report_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
         'independent_cells':[],'no_reviewed_code_imported':True}
    assert out['portable_report_sha256']=='926c1c628ce5a4ea1fe5e1b99b9576d3b54980a819aaa146ab4a43b35febe285'
    for R in (64,128,256,512,1024):
        D=R//(16*((R-1).bit_length()))
        C=(1<<(3*R//4-1))+1
        row=partition(R,max(D,1),C)
        row['theorem_D']=D; out['independent_cells'].append(row)
        print('R',R,'D',D,'cells',row['cell_counts_by_stage'],'min volume',min(t['volume'] for t in row['levels']),flush=True)
    out['materialized_sparse_control']=small_actual_control()
    # Check every offset on both sides of strict byte-width boundaries.
    for q in range(1,100):
        for delta in (-1,0,1):
            B=(1<<(8*q))+delta
            assert 8*(flog2(B)//8+1)==8*((B.bit_length()+7)//8)
    out['strict_width_checks']=297
    (HERE/'INDEPENDENT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print('PASSED',flush=True)
