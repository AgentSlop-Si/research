"""Fresh independent enclosure oracle: direct DFT, no Bluestein or FFT.

Uses pi=4*(atan(1/2)+atan(1/3)), independent of the backend Machin formula.
Uses separately written alternating sine/cosine recurrences and directed
outward dyadic interval endpoints. No imports from certified_fft.
"""
from fractions import Fraction

F=Fraction


def ceil_fraction(x):
    return -((-x.numerator)//x.denominator)


def oracle_pi(q):
    goal=F(1,1 << (q+12))
    sums=[]; errors=[]
    for denominator in (2,3):
        k=0; partial=F(0)
        while True:
            partial += F((-1)**k,(2*k+1)*denominator**(2*k+1))
            k+=1
            tail=F(1,(2*k+1)*denominator**(2*k+1))
            if tail <= goal:
                break
        sums.append(partial); errors.append(tail)
    midpoint=4*sum(sums)
    scale=1 << (q+8)
    rounded=F(midpoint.numerator*scale//midpoint.denominator,scale)
    error=4*sum(errors)+abs(rounded-midpoint)
    return rounded,error


def oracle_roots(N,q):
    pi,pi_error=oracle_pi(q)
    target=F(1,1 << (q+8))
    result=[]
    for residue in range(N):
        centered=residue if 2*residue<=N else residue-N
        a=F(2*centered,N)*pi
        assert abs(a)<4
        square=a*a
        cosine=F(1); cterm=F(1)
        sine=a; sterm=a
        r=0
        while True:
            nextc=-cterm*square/F((2*r+1)*(2*r+2))
            nexts=-sterm*square/F((2*r+2)*(2*r+3))
            # Past this point alternating magnitudes decrease geometrically.
            if r>=3 and max(abs(nextc),abs(nexts))<=target:
                break
            cosine+=nextc; sine+=nexts
            cterm=nextc;sterm=nexts;r+=1
        radius=max(abs(nextc),abs(nexts))+pi_error
        result.append((cosine,sine,radius))
    return result


def enclose_dft(x,epsilon):
    N=len(x); S=sum(abs(v) for z in x for v in z)
    q=1
    while F(S+1,1 << q)>epsilon/256:
        q+=1
    roots=oracle_roots(N,q)
    scale=1 << q
    boxes=[]
    for k in range(N):
        re=F(0);im=F(0);radius=F(0)
        for j,(a,b) in enumerate(x):
            c,s,e=roots[(j*k)%N]
            re+=a*c-b*s;im+=a*s+b*c
            radius+=(abs(a)+abs(b))*e
        bounds=[]
        for value in (re,im):
            lower=(value-radius)*scale;upper=(value+radius)*scale
            bounds.append((F(lower.numerator//lower.denominator,scale),
                           F(ceil_fraction(upper),scale)))
        boxes.append(tuple(bounds))
    return boxes,{'q':q,'formula':'pi=4*(atan(1/2)+atan(1/3))',
                  'method':'direct sum, alternating component bounds, outward dyadic boxes'}


def certifies(y,boxes,epsilon):
    if len(y)!=len(boxes): return False
    for z,box in zip(y,boxes):
        # Farthest box corner from y bounds distance to every enclosed target.
        d0=max(abs(z[0]-box[0][0]),abs(z[0]-box[0][1]))
        d1=max(abs(z[1]-box[1][0]),abs(z[1]-box[1][1]))
        if d0*d0+d1*d1>epsilon*epsilon:
            return False
    return True
