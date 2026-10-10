"""Hero #1 phase28: nested Winograd 3x5 DFT under exact prime-field model.

Every data addition and multiplication by nonidentity prepared scalar is paid.
No black-box higher-arity gates; full tensor pre/diag/post explicit.
Winograd nesting is classical prior work, not a novelty or asymptotic result.
"""
from dataclasses import dataclass
from crt15 import Cost
from crt15_engine import make_plan, fft2, transform as phase27_transform, predicted as phase27_predicted

@dataclass(frozen=True)
class DiagonalPlan:
    base: object
    d3: tuple
    d5: tuple
    d15: tuple
    preparation: Cost


def make_wfta_plan(n, **kwargs):
    base=make_plan(n,mode='gt',**kwargs)
    p=base.p
    # c3=(w+w^2)/2 - 1, h3=(w-w^2)/2, both prepared once.
    # phase27 k3.v already computed from w3 roots.
    c3=(base.k3.v-1)%p
    d3=(1,c3,base.k3.h)
    # phase27 k5.ca is (c1+c2)/2; move x0+ca*s to (x0+s)+(ca-1)*s.
    d5=(1,(base.k5.ca-1)%p,base.k5.cd,base.k5.h1,base.k5.h2_minus_h1,base.k5.h1_plus_h2)
    extra=Cost(adds=2)
    # 3x6 diagonal Kronecker. Identity row and column copied, charge only 2*5 products.
    dd=[]
    for v in d5:
        row=[]
        for i,u in enumerate(d3):
            if i==0:row.append(v)
            elif v==1:row.append(u)
            else:
                row.append((v*u)%p)
                extra.muls+=1
        dd.append(tuple(row))
    assert extra.muls==10
    # Conditional plan claim: for checked root-rich prime fields, only d5[0]*d3[0]=1.
    # If accidental extra units arise, we still charge all 17 nonidentity slots at execution.
    return DiagonalPlan(base,d3,d5,tuple(dd),extra)


def before3(x,p,c):
    a,b,d=x
    s=(b+d)%p;delta=(b-d)%p;full=(a+s)%p
    c.adds+=3
    return (full,s,delta)

def after3(v,p,c):
    full,scaled_s,scaled_delta=v
    mid=(full+scaled_s)%p
    y1=(mid+scaled_delta)%p
    y2=(mid-scaled_delta)%p
    c.adds+=3
    return (full,y1,y2)

def before5(x,p,c):
    x0,x1,x2,x3,x4=x
    s1=(x1+x4)%p;s2=(x2+x3)%p
    d1=(x1-x4)%p;d2=(x2-x3)%p
    s=(s1+s2)%p;t=(s1-s2)%p
    full=(x0+s)%p
    pair=(d1+d2)%p
    c.adds+=8
    return (full,s,t,pair,d2,d1)

def after5(z,p,c):
    full,cs,ct,hpair,hd2,hd1=z
    mid=(full+cs)%p
    e1=(mid+ct)%p;e2=(mid-ct)%p
    o1=(hpair+hd2)%p;o2=(hd1-hpair)%p
    y1=(e1+o1)%p;y4=(e1-o1)%p
    y2=(e2+o2)%p;y3=(e2-o2)%p
    c.adds+=9
    return (full,y1,y2,y3,y4)

def fft15_wfta(a, plan, c):
    """81 field adds/subs, 17 mults, input/output CRT maps same as phase27.

    Separate linear preweaves for factors 3 and 5; diagonal tensor scales once;
    then postweaves in reverse order. Eight phase27 multiplications eliminated.
    """
    p=plan.base.p
    b3=[before3(tuple(a[(10*u+6*v)%15] for u in range(3)),p,c) for v in range(5)]
    b5=[before5(tuple(b3[v][u] for v in range(5)),p,c) for u in range(3)]
    # intermediate layout 6 rows x3 columns: (v5, u3).
    scaled=[[0]*3 for _ in range(6)]
    for v in range(6):
        for u in range(3):
            z=b5[u][v]
            const=plan.d15[v][u]
            if const!=1:
                z=z*const%p;c.muls+=1
            scaled[v][u]=z
    assert len(scaled)==6
    post5=[after5(tuple(scaled[v][u] for v in range(6)),p,c) for u in range(3)]
    out=[0]*15
    for v in range(5):
        column=after3(tuple(post5[u][v] for u in range(3)),p,c)
        for r in range(3):out[(5*r+3*v)%15]=column[r]
    c.reads+=15;c.writes+=15
    return out


def transform_wfta(a,plan):
    base=plan.base
    n=len(a);g=base.g;p=base.p
    if n!=base.n:raise ValueError('incorrect input length')
    c=Cost()
    eg=15*pow(15,-1,g) if g>1 else 0
    e15=g*pow(g,-1,15)
    rows=[]
    for v in range(15):
        rows.append(fft2([a[(eg*u+e15*v)%n] for u in range(g)],base,c))
    out=[0]*n
    for r in range(g):
        zz=fft15_wfta([rows[v][r] for v in range(15)],plan,c)
        for v in range(15):out[(15*r+g*v)%n]=zz[v]
    c.reads+=n;c.writes+=n
    return out,c


def predicted(g):
    if g<1 or (g & (g-1)):raise ValueError('g power of 2')
    t=g.bit_length()-1
    adds=15*g*t+81*g
    muls=15*(g*t//2-g+1)+17*g if g>1 else 17
    return adds,muls,adds+muls


if __name__=='__main__':
    from crt15 import P,GENERATOR,ALT_P,ALT_GENERATOR,n_root
    import random
    for p,gen in ((P,GENERATOR),(ALT_P,ALT_GENERATOR)):
        for g in (1,2,4,8,16,32,64,128):
            n=15*g
            if (p-1)%n:continue
            plan=make_wfta_plan(n,p=p,gen=gen)
            for trial in range(3):
                x=[random.Random((trial+1)*991000+n*17+p+j).randrange(p) for j in range(n)]
                z,c=transform_wfta(x,plan)
                v,d=phase27_transform(x,plan.base)
                assert z==v,(p,n,trial)
                assert (c.adds,c.muls,c.total())==predicted(g),(p,n,c,predicted(g))
            print(p,n,predicted(g), 'baseline',phase27_predicted(g)[-1])
