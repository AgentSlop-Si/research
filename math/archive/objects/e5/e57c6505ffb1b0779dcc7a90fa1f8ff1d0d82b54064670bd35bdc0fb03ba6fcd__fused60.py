"""Phase28: exact 3x5x4 nested scalar diagram and 15*(4H) CT dyadic fusion.

No black-box gate. All 444 additions and 69 scalar multiplications expanded.
Before and after tensors use the factor ordering minimizing intermediate expansion.
Works over odd prime fields with primitive N=60H root, H a power of 2.
"""
from dataclasses import dataclass
from types import SimpleNamespace
from crt15 import Cost
from crt15_engine import fft2
from wfta15 import make_wfta_plan, before3, after3, before5, after5, transform_wfta, predicted

@dataclass(frozen=True)
class Fused60Plan:
    wfta:object
    h:int
    d4:tuple
    d60:tuple
    extra_setup:Cost

def before4(x,p,c):
    a,b,d,e=x
    c.adds+=4
    return ((a+d)%p,(b+e)%p,(a-d)%p,(b-e)%p)

def after4(v,p,c):
    x0,x1,x2,x3=v
    c.adds+=4
    return ((x0+x1)%p,(x2+x3)%p,(x0-x1)%p,(x2-x3)%p)

def make_fused60_plan(n,**kwargs):
    if n%60:raise ValueError('60 divides n')
    h=n//60
    if h<1 or h&(h-1):raise ValueError('n/60 must be power of two')
    wfta=make_wfta_plan(n,**kwargs)
    g=4*h
    assert wfta.base.g==g
    p=wfta.base.p
    i=wfta.base.roots_g[h]  # primitive fourth root
    d4=(1,1,1,i)
    setup=Cost()
    # diag order [v5][u3][t4], prepare 17 additional constants for t4=3.
    arr=[]
    for v in range(6):
        cols=[]
        for u in range(3):
            d=wfta.d15[v][u]
            if d==1:x=i
            else:
                x=d*i%p;setup.muls+=1
            cols.append((d,d,d,x))
        arr.append(tuple(cols))
    assert setup.muls==17
    return Fused60Plan(wfta,h,d4,tuple(arr),setup)


def kernel60(a,plan,c):
    """a flattened a[i15*4 + j4] -> y[k15*4 + k4].

    Input F15 coordinates are CRT (3,5), F4 coordinates natural.
    """
    p=plan.wfta.base.p
    if len(a)!=60:raise ValueError('kernel60 requires 60 cells')
    # Tensor in layout [v5][u3][t4].
    arr=[[[a[((10*u+6*v)%15)*4+t] for t in range(4)] for u in range(3)] for v in range(5)]
    # pre B3: 5*4*3=60 additions
    b3=[[[0]*4 for u in range(3)] for v in range(5)]
    for v in range(5):
        for t in range(4):
            xx=before3(tuple(arr[v][u][t] for u in range(3)),p,c)
            for u in range(3):b3[v][u][t]=xx[u]
    # pre B4: 5*3*4=60 additions (before B5 expansion).
    b4=[[[0]*4 for u in range(3)] for v in range(5)]
    for v in range(5):
        for u in range(3):b4[v][u]=list(before4(b3[v][u],p,c))
    # pre B5: 3*4*8=96 additions
    b5=[[[0]*4 for u in range(3)] for v in range(6)]
    for u in range(3):
        for t in range(4):
            vout=before5(tuple(b4[v][u][t] for v in range(5)),p,c)
            for v in range(6):b5[v][u][t]=vout[v]
    # 72 cells, 3 identity coefficients, 69 paid multiplications.
    scaled=[[[0]*4 for u in range(3)] for v in range(6)]
    for v in range(6):
        for u in range(3):
            for t in range(4):
                val=b5[v][u][t]; coeff=plan.d60[v][u][t]
                if coeff!=1:
                    val=val*coeff%p;c.muls+=1
                scaled[v][u][t]=val
    # post A5: 3*4*9=108 additions
    p5=[[[0]*4 for u in range(3)] for v in range(5)]
    for u in range(3):
        for t in range(4):
            vout=after5(tuple(scaled[v][u][t] for v in range(6)),p,c)
            for v in range(5):p5[v][u][t]=vout[v]
    # post A4: 5*3*4=60 additions
    p4=[[[0]*4 for u in range(3)] for v in range(5)]
    for v in range(5):
        for u in range(3):p4[v][u]=list(after4(p5[v][u],p,c))
    # post A3: 5*4*3=60 additions
    out=[0]*60
    for v in range(5):
        for t in range(4):
            o=after3(tuple(p4[v][u][t] for u in range(3)),p,c)
            for u in range(3):out[((5*u+3*v)%15)*4+t]=o[u]
    c.reads+=60;c.writes+=60
    return out


def transform_fused(a,plan):
    """All-input DFT N=60H =15*(4H). GT across 15 and G, CT inside G.

    H-size DFTs first, CT twist only across inner (4,H) factors, then
    joint WFTA 60-point tensor for 15x4, so no extra twiddles across 15.
    """
    base=plan.wfta.base
    n=len(a);p=base.p;h=plan.h;g=4*h
    if n!=base.n:raise ValueError('incorrect full transform length')
    c=Cost()
    eg=15*pow(15,-1,g)
    e15=g*pow(g,-1,15)
    roots_h=[base.roots_g[(4*j)%g] for j in range(h)]
    subplan=SimpleNamespace(g=h,p=p,roots_g=roots_h)
    # 15*4 independent length-H dyadic FFTs.
    rows=[[[0]*h for j in range(4)] for v in range(15)]
    for v in range(15):
        for j4 in range(4):
            xx=[a[(eg*(j4+4*t)+e15*v)%n] for t in range(h)]
            rows[v][j4]=fft2(xx,subplan,c)
    # H fused tensor kernels, only pay 15*3*(H-1) stage twiddles.
    out=[0]*n
    for q in range(h):
        input60=[0]*60
        for v in range(15):
            for j4 in range(4):
                z=rows[v][j4][q]
                if j4 and q:
                    z=z*base.roots_g[(j4*q)%g]%p;c.muls+=1
                input60[4*v+j4]=z
        y=kernel60(input60,plan,c)
        for v in range(15):
            for j4 in range(4):
                kg=q+h*j4
                out[(15*kg+g*v)%n]=y[4*v+j4]
    c.reads+=n;c.writes+=n
    return out,c


def predicted_fused(h):
    if h<1 or h&(h-1):raise ValueError('h power of two')
    t=h.bit_length()-1
    adds=60*h*t+444*h
    muls=60*(h*t//2-h+1)+69*h+45*(h-1)
    return adds,muls,adds+muls

if __name__=='__main__':
    from crt15 import P,GENERATOR,ALT_P,ALT_GENERATOR
    import random
    for p,gen in ((P,GENERATOR),(ALT_P,ALT_GENERATOR)):
        for h in (1,2,4,8,16,32):
            n=60*h
            if (p-1)%n:continue
            plan=make_fused60_plan(n,p=p,gen=gen)
            for trial in range(2):
                rng=random.Random(p+n*823+trial)
                x=[rng.randrange(p) for _ in range(n)]
                y,c=transform_fused(x,plan)
                z,b=transform_wfta(x,plan.wfta)
                assert y==z,(p,n,trial,[(j,y[j],z[j]) for j in range(n) if y[j]!=z[j]][:3])
                assert (c.adds,c.muls,c.total())==predicted_fused(h),(p,n,c,predicted_fused(h))
            print('p',p,'n',n,'fused',c.total(),'wfta15',b.total(),'phase27',15, 'savings',b.total()-c.total())
