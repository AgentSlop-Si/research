"""Exception-resistant row-3 spectral minors: eliminate eta,V,gamma3.

Exact (mod p) 3x3 determinantal constraints D_k(gamma3)=0 for
k in (4,1,2,5), with D linear in gamma3. Pairwise polynomial
resultants in eight base variables are necessary for n8 factoring.
Not sufficient and not a generic FFT impossibility proof.
"""
import json
from sympy.polys.rings import ring
from sympy.polys.domains import GF
from dual_support import primitive_root,P8
from general_onion import build
from pathlib import Path
from column_minor import det4
import random

def det3(M):
    a,b,c=M[0];d,e,f=M[1];g,h,i=M[2]
    return a*(e*i-f*h)-b*(d*i-f*g)+c*(d*h-e*g)

def generate(p,w):
    R,t,h0,h1,h2,hl,beta,g1,g2=ring('t,h0,h1,h2,hl,beta,g1,g2',GF(p))
    xi=pow(w,-1,p);c1=(1+xi+xi*xi)%p;c2=(xi+xi*xi+xi**3)%p;c3=xi**3%p
    hs=[h0,h1,h2]
    for k in range(4):hs.append(c1*hs[k+2]-c2*hs[k+1]+c3*hs[k])
    H=hs[:6]+[hl]
    v0=(t-1+beta*(h0-1))
    def Lhat(k):
        if k==0:return R.zero
        if k==7:return t*(w-1)
        return (1-beta*h0)*(w-1)+v0*(pow(xi,k,p)-1)+beta*H[k]*(w-1)
    LL=[Lhat(k) for k in range(8)]
    def vec(a,k,gg):
        if gg is None:q=[pow(w,a*r,p) for r in range(8)]
        else:q=[pow(w,a*r,p)-gg for r in range(8)]
        return [sum((q[r]*H[r] for r in range(k)),R.zero),
                sum((q[r]*LL[r] for r in range(k+1,8)),R.zero),q[k]+R.zero]
    out={}
    for k in (4,1,2,5):
        row1=vec(1,k,g1);row2=vec(2,k,g2)
        aa=det3([row1,row2,vec(3,k,None)])
        # det(...,q^3_r= z^(3r)-g3) = aa-g3*bb
        bb=det3([row1,row2,[sum((H[r] for r in range(k)),R.zero),
                               sum((LL[r] for r in range(k+1,8)),R.zero),R.one]])
        assert aa and bb
        out[k]=(aa,bb)
    return R,out

def verify(p,w,samples=12):
    R,o=generate(p,w)
    rng=random.Random(p+w+20261009)
    example=[]
    for j in range(samples):
        v=[rng.randrange(1,p) for _ in range(8)]
        try:C,B,data=build(8,p,w,P8,v)
        except ZeroDivisionError:continue
        gamma3=rng.randrange(1,p)
        g1,g2=v[-2:]
        for k in o:
            A,BB=o[k];vv=list(zip(R.gens,v))
            left=(A.evaluate(vv)-gamma3*BB.evaluate(vv))%p
            q=lambda x: [(pow(w,x*r,p)-({1:g1,2:g2,3:gamma3}[x]))%p for r in range(8)]
            def ss(x):return sum(q(x)[r]*int(data['H'][r]) for r in range(k))%p
            def rr(x):return sum(q(x)[r]*int(data['L'][r]) for r in range(k+1,8))%p
            def kk(x):return q(x)[k]
            D=det3([[ss(x),rr(x),kk(x)] for x in (1,2,3)])%p
            assert (left-(v[0]*(w-1)*D))%p==0,(k,left,D)
            if k==4:example.append(dict(k=k,direct_D=int(D),scaled_det=int(left)))
    sizes={str(k):{'a_terms':len(v[0]),'b_terms':len(v[1]),
                   'a_degree':max(sum(m) for m,c in v[0].terms()),
                   'b_degree':max(sum(m) for m,c in v[1].terms())} for k,v in o.items()}
    pairs=[]
    ks=list(o)
    for j in range(1,len(ks)):
        k=ks[0];ell=ks[j]
        resultant=o[k][0]*o[ell][1]-o[ell][0]*o[k][1]
        pairs.append(dict(pair=[k,ell],terms=len(resultant),degree=max(sum(m) for m,c in resultant.terms()),nonzero=bool(resultant)))
    return dict(prime=p,root=w,verified=len(example),component_poly_sizes=sizes,elimination=resultant_summary(pairs))

def resultant_summary(pairs):return pairs
if __name__=='__main__':
    results=[]
    for p in (17,12289):
        for omega in (primitive_root(p,8),):
            results.append(verify(p,omega,12))
    Path(__file__).with_name('upper_minor_results.json').write_text(json.dumps(results,indent=2)+'\n')
    for x in results:print(json.dumps(x,indent=2))
