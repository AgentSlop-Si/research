"""Exact original-branch check of the uniform N3 construction, including GF4."""
import json
from pathlib import Path

def check(p,q):
    if p==4:
        add=lambda a,b:a^b;neg=lambda a:a;number=lambda a:a%2
        def mul(a,b):
            r=0
            while b:
                if b&1:r^=a
                a<<=1
                if a&4:a^=7
                b>>=1
            return r
        size=4
    else:
        add=lambda a,b:(a+b)%p;neg=lambda a:(-a)%p;number=lambda a:a%p;mul=lambda a,b:a*b%p;size=p
    def sm(vs):
        r=0
        for v in vs:r=add(r,v)
        return r
    def power(a,k):
        r=1
        while k:
            if k&1:r=mul(r,a)
            a=mul(a,a);k//=2
        return r
    inverse=lambda a:power(a,size-2)
    divide=lambda a,b:mul(a,inverse(b))
    def invert(A):
        a=[r[:]+[int(i==j) for j in range(3)] for i,r in enumerate(A)]
        for c in range(3):
            r=next(i for i in range(c,3) if a[i][c]);a[c],a[r]=a[r],a[c];iv=inverse(a[c][c]);a[c]=[mul(iv,x) for x in a[c]]
            for i in range(3):
                if i!=c:
                    f=a[i][c];a[i]=[add(x,neg(mul(f,y))) for x,y in zip(a[i],a[c])]
        return [r[3:] for r in a]
    assert power(q,3)==1 and q!=1
    C=divide(sm(power(q,(-j*j)%3) for j in range(3)),number(3));assert C
    f=lambda a,b:mul(C,power(q,((a+b)**2)%3))
    alphas={(1,1):1,(1,-1):q,(-1,1):q,(-1,-1):1};h={s:[0,0,0] for s in alphas}
    cs={k:divide(sm(mul(f(a,0),power(q,(-k*a)%3)) for a in range(3)),number(3)) for k in [0,1,-1]}
    h[1,1][0]=cs[0];h[1,-1][0]=cs[1];h[-1,1][0]=cs[-1]
    for (e,d),alpha in alphas.items():
        den=mul(alpha,add(1,power(q,(e*d)%3)));assert den;h[e,d][1]=divide(f(e,d),den)
    for d in [1,-1]:h[1,-d][2]=add(f(0,d),neg(add(h[1,d][1],h[-1,d][1])))
    result=[[0]*3 for _ in range(3)];records=[]
    for (e,d),alpha in alphas.items():
        assert add(add(1,neg(power(alpha,3))),neg(1))==neg(1)
        zeta=power(q,(e*d)%3);weights=[sm(mul(neg(h[e,d][ell]),power(zeta,(-j*ell)%3)) for ell in range(3)) for j in range(3)]
        for j,w in enumerate(weights):
            Q=[[int(i==v) for v in range(3)] for i in range(3)]
            for i in range(3):
                Q[i][i]=add(Q[i][i],neg(mul(power(zeta,j),power(q,(d*i)%3))))
                Q[i][(i-e)%3]=add(Q[i][(i-e)%3],neg(alpha))
            G=invert(Q)
            for i in range(3):
                for v in range(3):result[i][v]=add(result[i][v],divide(mul(w,G[i][v]),number(3)))
        records.append({'epsilon':e,'delta':d,'alpha':alpha,'weights':weights})
    F=[[power(q,(-i*j)%3) for j in range(3)] for i in range(3)];assert result==F
    return {'field':f'F{p}','q':q,'full_matrix_match':True,'banks':records}

out=[check(p,q) for p,q in [(4,2),(7,2),(13,3),(19,7),(31,5)]]
Path(__file__).with_name('reviewer_n3_results.json').write_text(json.dumps(out,indent=2)+'\n');print('DONE',len(out))
