"""Rejected Phase29 experiment: naive weighted-4 single-layer diagonal tensor.

Attempt to absorb Cooley-Tukey stage twiddles into the 15-point Winograd
scaling: W4(a) = F4 diag(1,a,a^2,a^3), where a is a stage twiddle.
The six-channel realization uses zero pre-additions, eight post-additions,
but expands the 15-point tensor to width 18*6 and costs MORE than Phase28.
No global impossibility theorem for other weighted-4 circuits is claimed.
"""
from crt15 import Cost
from wfta15 import before3,after3,before5,after5,fft15_wfta

def weighted4_coefficients(a,i,p):
    a2=a*a%p;a3=a2*a%p
    return (1,a2,a,i*a%p,a3,(-i*a3)%p)

def before_weighted4(x):
    x0,x1,x2,x3=x
    return (x0,x2,x1,x1,x3,x3)

def after_weighted4(z,p,c):
    eplus=(z[0]+z[1])%p;eminus=(z[0]-z[1])%p
    oplus=(z[2]+z[4])%p;ominus=(z[3]+z[5])%p
    c.adds+=8
    return [(eplus+oplus)%p,(eminus+ominus)%p,
            (eplus-oplus)%p,(eminus-ominus)%p]

def tensor_weighted4(a,plan,alpha,i):
    """4x15 tensor I/O. Does not include preparing the 18*6 scalars."""
    if len(a)!=60:raise ValueError('60 input fields')
    p=plan.base.p;c=Cost()
    b3=[[[0]*4 for _ in range(3)] for _ in range(5)]
    for v5 in range(5):
        for t4 in range(4):
            vv=before3(tuple(a[((10*u3+6*v5)%15)*4+t4] for u3 in range(3)),p,c)
            for u3 in range(3):b3[v5][u3][t4]=vv[u3]
    b5=[[[0]*4 for _ in range(3)] for _ in range(6)]
    for u3 in range(3):
        for t4 in range(4):
            vv=before5(tuple(b3[v5][u3][t4] for v5 in range(5)),p,c)
            for v5 in range(6):b5[v5][u3][t4]=vv[v5]
    w=weighted4_coefficients(alpha,i,p)
    intermediate=[[[0]*6 for _ in range(3)] for _ in range(6)]
    nonidentity=0
    for v5 in range(6):
        for u3 in range(3):
            dup=before_weighted4(b5[v5][u3])
            for t6 in range(6):
                co=plan.d15[v5][u3]*w[t6]%p
                v=dup[t6]
                if co!=1:
                    v=v*co%p;c.muls+=1;nonidentity+=1
                intermediate[v5][u3][t6]=v
    a4=[[[0]*4 for _ in range(3)] for _ in range(6)]
    for v5 in range(6):
        for u3 in range(3):a4[v5][u3]=after_weighted4(intermediate[v5][u3],p,c)
    p5=[[[0]*4 for _ in range(3)] for _ in range(5)]
    for u3 in range(3):
        for t4 in range(4):
            vv=after5(tuple(a4[v5][u3][t4] for v5 in range(6)),p,c)
            for v5 in range(5):p5[v5][u3][t4]=vv[v5]
    out=[0]*60
    for v5 in range(5):
        for t4 in range(4):
            vv=after3(tuple(p5[v5][u3][t4] for u3 in range(3)),p,c)
            for u3 in range(3):out[((5*u3+3*v5)%15)*4+t4]=vv[u3]
    c.reads+=60;c.writes+=60
    assert c.adds==468
    return out,c,nonidentity

def reference_weighted4(a,plan,alpha,i):
    p=plan.base.p;c=Cost()
    # Twiddle each input lane of its length4 DFT, all rows 15.
    b=[a[4*v:4*v+4] for v in range(15)]
    for v in range(15):
        for j in range(1,4):
            b[v][j]=b[v][j]*pow(alpha,j,p)%p
            if alpha!=1:c.muls+=1
    rows=[[0]*4 for _ in range(15)]
    for j in range(4):
        xs=[b[v][j] for v in range(15)]
        out=fft15_wfta(xs,plan,c)
        for v in range(15):rows[v][j]=out[v]
    # Direct F4 butterfly, eight additions + one i multiply per row.
    out=[]
    for v in range(15):
        x0,x1,x2,x3=rows[v]
        e=(x0+x2)%p;d=(x0-x2)%p
        s=(x1+x3)%p;t=(x1-x3)%p
        it=t*i%p;c.muls+=1;c.adds+=8
        out.extend(((e+s)%p,(d+it)%p,(e-s)%p,(d-it)%p))
    return out,c

if __name__=='__main__':
    from crt15 import P,GENERATOR,ALT_P,ALT_GENERATOR,n_root
    from wfta15 import make_wfta_plan
    import random
    for p,gen in ((P,GENERATOR),(ALT_P,ALT_GENERATOR)):
        plan=make_wfta_plan(120,p=p,gen=gen)
        rootg=n_root(8,p,gen);i=pow(rootg,2,p)
        for q in (0,1,2,3):
            alpha=pow(rootg,q,p)
            rng=random.Random(197*q+p)
            a=[rng.randrange(p) for j in range(60)]
            new,c,paid=tensor_weighted4(a,plan,alpha,i)
            old,d=reference_weighted4(a,plan,alpha,i)
            assert new==old,(p,q)
            # compare 15x F15 (4*98=392) +15x F4 (15*9=135) +twiddle(45)
            print('p',p,'q',q,'new',c.total(),'old',d.total(),'difference',c.total()-d.total(),'paid',paid)
