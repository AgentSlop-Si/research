#!/usr/bin/env python3
"""Review-authored exact controls for all-scalar folding and exact edit lifts."""
import json
from pathlib import Path
from exact_utils import Field,root

P=998244353
F=Field(P)
LABELS=[(axis,c,sign) for axis in ('H','V') for c in (0,1) for sign in (-1,1)]


def fourier(n,z):
    return [[pow(z,i*j,P) for j in range(n)] for i in range(n)]


def valuation(t,b):
    y=t%b
    return b.bit_length()-1 if y==0 else (y&-y).bit_length()-1


def folding():
    out=[]
    for b in (1,2,4,8):
        for a in (b,2*b):
            n=a*b;r=b.bit_length()-1
            pi=[((v//(2*b))%a)*b+(v%(2*b))%b for v in range(4*n)]
            selected=[2*b*x+(y if y else b) for x in range(a) for y in range(b)]
            assert [pi[j] for j in selected]==list(range(n)) and len(set(selected))==n
            for orientation in (1,-1):
                w=pow(root(4*n,P,3),orientation,P)
                z=pow(w,4,P)
                fn=fourier(n,z)
                fl=fourier(4*n,w)
                qfl=[[0]*(4*n) for _ in range(n)]
                for v,row in enumerate(fl):
                    qfl[pi[v]]=[(x+y)%P for x,y in zip(qfl[pi[v]],row)]
                chosen=[[row[j] for j in selected] for row in qfl]
                finv=[[pow(z,-i*j,P)*F.inv(n)%P for j in range(n)] for i in range(n)]
                assert F.mul(finv,fn)==F.eye(n)
                k=F.mul(finv,chosen)
                nonzero=0
                for s in range(n):
                    for t,j in enumerate(selected):
                        if k[s][t]:
                            assert j%2==0 and (s-j//2)%a==0
                            assert valuation(s,b)==valuation(t,b)-1
                            nonzero+=1
                power=F.eye(n)
                for _ in range(r+1):power=F.mul(power,k)
                assert not any(x for row in power for x in row)
                detf=F.det(fn);assert detf
                determinants=[]
                for gamma in (1,2,7,P-1):
                    delta=[[(x-gamma*y)%P for x,y in zip(ar,fr)] for ar,fr in zip(chosen,fn)]
                    det=F.det(delta)
                    assert det==detf*pow(-gamma,n,P)%P and det
                    determinants.append({'gamma':gamma,'selected_determinant':det})
                assert F.rank(qfl)==n
                out.append({'a':a,'b':b,'N':n,'orientation':orientation,'selected_columns':selected,
                            'K_nonzero_entries':nonzero,'nilpotent_power':r+1,
                            'fourier_determinant':detf,'determinant_controls':determinants,
                            'gamma_zero_full_row_rank':n})
    return out


def cover(a,b,label):
    axis,c,sign=label;out=[]
    for x in range(a):
        for y in range(b):
            out.append(((x+sign*(2*y+c))%a)*b+y if axis=='H' else x*b+(y+sign*(2*x+c))%b)
    return out


def cycle_lists(p):
    seen=set();out=[]
    for v in range(len(p)):
        if v in seen:continue
        c=[];w=v
        while w not in seen:seen.add(w);c.append(w);w=p[w]
        assert w==v;out.append(c)
    return out


def splice_at(p,tails):
    q=p[:]
    if len(tails)>1:
        for j,v in enumerate(tails):q[v]=p[tails[(j+1)%len(tails)]]
    return q


def exact_edit_chains():
    out=[]
    for rectangular in (False,True):
        for label in LABELS:
            a,b=((4,2) if rectangular else (2,2))
            base=cover(a,b,label)
            current=splice_at(base,[min(c) for c in cycle_lists(base)])
            assert current[0]!=base[0]
            for level in range(1,5):
                n=a*b;small=cover(a,b,label);large=cover(2*a,2*b,label)
                eta=[0]*n
                for v in range(n):eta[small[v]]=current[v]
                pi=[((v//(2*b))%a)*b+(v%(2*b))%b for v in range(4*n)]
                pre=[]
                for v in large:
                    x,y=divmod(v,2*b)
                    bx,by=divmod(eta[(x%a)*b+y%b],b)
                    pre.append((bx+a*(x//a))*2*b+by+b*(y//b))
                orbits=cycle_lists(pre);assert len(orbits)<=4
                tails=sorted(min(v for v in c if pi[v]==0) for c in orbits)
                lifted=splice_at(pre,tails)
                assert len(cycle_lists(lifted))==1
                assert all(pi[lifted[v]]==current[pi[v]] for v in range(4*n))
                assert all(pre[v]!=large[v] and lifted[v]!=large[v] for v in range(4*n) if pi[v]==0)
                hs=sum(x!=y for x,y in zip(current,small));hl=sum(x!=y for x,y in zip(lifted,large))
                assert hl==4*hs and lifted[0]!=large[0]
                out.append({'shape':'rectangle' if rectangular else 'square','label':label,'level':level,
                            'small_N':n,'small_edits':hs,'large_edits':hl,'zero_tail_changed':True})
                current=lifted;a,b=2*a,2*b
    margins=[]
    for n0,d0,margin0 in [(1<<17,7936,768),(1<<18,11264,15360)]:
        for level in range(65):
            margin=3*(n0*4**level)//16-3*d0*4**level
            assert margin==margin0*4**level>0
        margins.append({'seed_N':n0,'seed_loss':d0,'exact_rational_margin':f'{margin0}*4^level','levels_checked':65})
    return {'instances':out,'margin_controls':margins}


def mask_defects():
    rows=[]
    for a,b in [(2,2),(4,2),(4,4),(8,4)]:
        n=a*b
        pi=[((v//(2*b))%a)*b+(v%(2*b))%b for v in range(4*n)]
        small=[i+2 for i in range(n)]
        large=[((-1)**((v%(2*b))//b))*small[pi[v]]%P for v in range(4*n)]
        assert all(large)
        for gamma in (0,1,2,P-1,7):
            e=[[0]*(4*n) for _ in range(n)]
            for v in range(4*n):e[pi[v]][v]=(large[v]-gamma*small[pi[v]])%P
            affected=sum(any(x for x in row) for row in e)
            assert F.rank(e)==affected==n
            rows.append({'N':n,'gamma':gamma,'affected_fibers':affected,'defect_rank':n})
    return rows


def main():
    result={'status':'PASS','field':P,'folding':folding(),'hierarchy':exact_edit_chains(),
            'nonconstant_fiber_mask_controls':mask_defects(),
            'scope':'Separate all-scalar rank theorem and exact-edit addendum; no Fourier coefficients or general four-fiber law.'}
    Path('VERIFIED_RESULTS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','fold_layouts_and_orientations':len(result['folding']),
                      'nonzero_gamma_determinants':4*len(result['folding']),
                      'full_rank_fiber_mask_cases':len(result['nonconstant_fiber_mask_controls']),
                      'exact_edit_lifts':len(result['hierarchy']['instances'])},sort_keys=True))


if __name__=='__main__':main()
