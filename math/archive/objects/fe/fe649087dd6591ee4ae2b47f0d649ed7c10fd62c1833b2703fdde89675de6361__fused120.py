"""Hero #1 Phase29: full exact 120-point WFTA diagonal tensor fused into noncoprime (8,H).

Length N=120h=15*(8h), h=2^t, prime p with a primitive N-th root.
The 120-point (15x8) tensor has 1038 additions, 140 nonidentity
field multiplies for tested root-rich primes, with every scalar expanded.

Compared with prior Phase28 length N=60*(2h), saves 13h field operations
at the same input length and using the same 8h base root-table plan.
"""
from dataclasses import dataclass
from types import SimpleNamespace
from crt15 import Cost
from crt15_engine import fft2
from wfta15 import make_wfta_plan,before3,after3,before5,after5
from wfta8 import before8,after8,prepare_diag8

@dataclass(frozen=True)
class Fused120Plan:
    wfta:object
    h:int
    d8:tuple
    d120:tuple
    extra_setup:Cost
    diagonal_ones:int


def make_fused120_plan(n,**kwargs):
    if n%120:raise ValueError('N must be divisible by 120')
    h=n//120
    if h<1 or h&(h-1):raise ValueError('N/120 must be power of two')
    wfta=make_wfta_plan(n,**kwargs)
    p=wfta.base.p
    assert wfta.base.g == 8*h
    omega8=wfta.base.roots_g[h]
    extra=Cost()
    d8=prepare_diag8(omega8,p,extra,known_i=wfta.base.roots_g[2*h])
    # Prepare one tensor product scalar per nontrivial pair; unit factors reused.
    d120=[]
    for v5 in range(6):
        row=[]
        for u3 in range(3):
            d15=wfta.d15[v5][u3]
            vals=[]
            for d in d8:
                if d==1: val=d15
                elif d15==1: val=d
                else:
                    val=d15*d%p
                    extra.muls+=1
                vals.append(val)
            row.append(tuple(vals))
        d120.append(tuple(row))
    ones=sum(val==1 for row in d120 for cell in row for val in cell)
    return Fused120Plan(wfta,h,d8,tuple(d120),extra,ones)


def kernel120(a,plan,c):
    """Tensor I/O layout: a[v15*8 + j8], y[k15*8+k8].
    B8 -> B3 -> B5 -> D120 -> A5 -> A3 -> A8, all scalar operations charged.
    """
    if len(a)!=120:raise ValueError('kernel120 requires 120 inputs')
    p=plan.wfta.base.p
    # B8 on each of 15 rows, 15*14=210 adds.
    b8=[list(before8(tuple(a[8*v+j] for j in range(8)),p,c)) for v in range(15)]
    # B3 on each group of five CRT3 blocks and eight B8 channels, 5*8*3=120 adds.
    b3=[[[0]*8 for _ in range(3)] for _ in range(5)]
    for v5 in range(5):
        for t8 in range(8):
            xs=tuple(b8[(10*u3+6*v5)%15][t8] for u3 in range(3))
            vv=before3(xs,p,c)
            for u3 in range(3):b3[v5][u3][t8]=vv[u3]
    # B5 on three columns and eight B8 channels, 3*8*8=192 adds.
    b5=[[[0]*8 for _ in range(3)] for _ in range(6)]
    for u3 in range(3):
        for t8 in range(8):
            xs=tuple(b3[v5][u3][t8] for v5 in range(5))
            vv=before5(xs,p,c)
            for v5 in range(6):b5[v5][u3][t8]=vv[v5]
    # One complete diagonal pass, 144 channels, includes every scaling.
    scaled=[[[0]*8 for _ in range(3)] for _ in range(6)]
    for v5 in range(6):
        for u3 in range(3):
            for t8 in range(8):
                co=plan.d120[v5][u3][t8]
                value=b5[v5][u3][t8]
                if co!=1:
                    value=value*co%p;c.muls+=1
                scaled[v5][u3][t8]=value
    # A5 3*8*9=216 adds.
    p5=[[[0]*8 for _ in range(3)] for _ in range(5)]
    for u3 in range(3):
        for t8 in range(8):
            vv=after5(tuple(scaled[v5][u3][t8] for v5 in range(6)),p,c)
            for v5 in range(5):p5[v5][u3][t8]=vv[v5]
    # A3 5*8*3=120 adds.
    p3=[[0]*8 for _ in range(15)]
    for v5 in range(5):
        for t8 in range(8):
            vv=after3(tuple(p5[v5][u3][t8] for u3 in range(3)),p,c)
            for u3 in range(3):p3[(5*u3+3*v5)%15][t8]=vv[u3]
    # A8 on each of 15 tensor rows, 15*12=180 adds.
    out=[]
    for v in range(15):out.extend(after8(tuple(p3[v]),p,c))
    c.reads+=120;c.writes+=120
    return out


def transform_fused120(a,plan):
    """Arbitrary-input exact DFT of length N=15*(8h), h=2^t.
    Shared CRT across 15 and 8h, charged CT(8,h) internal twiddles.
    """
    base=plan.wfta.base
    n=len(a);h=plan.h;g=8*h;p=base.p
    if n!=base.n:raise ValueError('input length mismatch')
    c=Cost()
    eg=15*pow(15,-1,g)
    e15=g*pow(g,-1,15)
    roots_h=[base.roots_g[(8*j)%g] for j in range(h)]
    subplan=SimpleNamespace(g=h,p=p,roots_g=roots_h)
    # 120 independent h-point dyadic FFTs.
    rows=[[[0]*h for _ in range(8)] for _ in range(15)]
    for v in range(15):
        for j8 in range(8):
            xs=[a[(eg*(j8+8*t)+e15*v)%n] for t in range(h)]
            rows[v][j8]=fft2(xs,subplan,c)
    out=[0]*n
    for q in range(h):
        mid=[0]*120
        for v in range(15):
            for j8 in range(8):
                val=rows[v][j8][q]
                if j8 and q:
                    val=val*base.roots_g[(j8*q)%g]%p
                    c.muls+=1
                mid[8*v+j8]=val
        y=kernel120(mid,plan,c)
        for v in range(15):
            for j8 in range(8):
                k_g=q+h*j8
                out[(15*k_g+g*v)%n]=y[8*v+j8]
    c.reads+=n;c.writes+=n
    return out,c


def predicted_fused120(h,identities=4):
    if h<1 or h&(h-1):raise ValueError('h must be a power of two')
    t=h.bit_length()-1
    adds=120*h*t+1038*h
    # 120 dyadic h-FFTs, 105(h-1) CT twiddles, h diagonal tensors.
    muls=60*h*t-120*h+120+105*(h-1)+(144-identities)*h
    return adds,muls,adds+muls

if __name__=='__main__':
    from crt15 import P,GENERATOR,ALT_P,ALT_GENERATOR
    from fused60 import make_fused60_plan,transform_fused,predicted_fused
    import random
    for p,gen in ((P,GENERATOR),(ALT_P,ALT_GENERATOR)):
        for h in (1,2,4,8,16,32):
            n=120*h
            if (p-1)%n:continue
            plan=make_fused120_plan(n,p=p,gen=gen)
            oldplan=make_fused60_plan(n,p=p,gen=gen)
            for tr in range(2):
                rng=random.Random(910241*n+7*p+tr)
                a=[rng.randrange(p) for _ in range(n)]
                out,c=transform_fused120(a,plan)
                old,d=transform_fused(a,oldplan)
                assert out==old,(p,n,tr)
                assert(c.adds,c.muls,c.total())==predicted_fused120(h,plan.diagonal_ones),(p,n,c,predicted_fused120(h,plan.diagonal_ones))
                assert d.total()==predicted_fused(n//60)[-1]
            print('p',p,'n',n,'new',c.total(),'old',d.total(),'saved',d.total()-c.total(),'diag identities',plan.diagonal_ones)
