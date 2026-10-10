#!/usr/bin/env python3
"""New independent exact controls; imports no supplied research program."""
import hashlib
import json
import math
from pathlib import Path
import random

HERE = Path(__file__).resolve().parent


def eye(n, p):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def zero(n):
    return [[0] * n for _ in range(n)]


def add(a, b, p):
    return [[(x+y) % p for x, y in zip(r, s)] for r, s in zip(a, b)]


def scale(a, c, p):
    return [[c*x % p for x in r] for r in a]


def mul(a, b, p):
    cols = list(zip(*b))
    return [[sum(x*y for x,y in zip(r,c)) % p for c in cols] for r in a]


def transpose(a):
    return list(map(list, zip(*a)))


def block(a,b,c,d):
    return [r+s for r,s in zip(a,b)] + [r+s for r,s in zip(c,d)]


def rank(a,p):
    a=[r[:] for r in a]
    i=0
    for j in range(len(a[0])):
        k=next((k for k in range(i,len(a)) if a[k][j]), None)
        if k is None:
            continue
        a[i],a[k]=a[k],a[i]
        f=pow(a[i][j],-1,p)
        a[i]=[x*f%p for x in a[i]]
        for k in range(i+1,len(a)):
            f=a[k][j]
            if f:
                a[k]=[(x-f*y)%p for x,y in zip(a[k],a[i])]
        i+=1
        if i==len(a):
            break
    return i


def inverse(a,p):
    n=len(a); a=[r[:] + e for r,e in zip(a,eye(n,p))]
    for j in range(n):
        k=next(k for k in range(j,n) if a[k][j])
        a[j],a[k]=a[k],a[j]
        f=pow(a[j][j],-1,p); a[j]=[x*f%p for x in a[j]]
        for k in range(n):
            if k!=j and a[k][j]:
                f=a[k][j]; a[k]=[(x-f*y)%p for x,y in zip(a[k],a[j])]
    return [r[n:] for r in a]


def off_diagonal_count(a):
    return sum(x!=0 for i,r in enumerate(a) for j,x in enumerate(r) if i!=j)


def signed_cycle(n,p,variant):
    rng=random.Random(610100+n*13+variant)
    order=list(range(n))
    if variant:
        rng.shuffle(order)
    signs=[1]*n
    if variant:
        signs=[rng.choice((-1,1)) for _ in range(n)]
    if math.prod(signs)!=-1:
        signs[-1]*=-1
    t=zero(n)
    for k,v in enumerate(order):
        t[order[(k+1)%n]][v]=signs[k]%p
    return t,order,signs


def green_scan(order,signs,t,x,p):
    n=len(x)
    carry=0
    for k,v in enumerate(order):
        carry=(x[v]+t*signs[(k-1)%n]*carry)%p
    last=carry*pow((1+pow(t,n,p))%p,-1,p)%p
    out=[0]*n
    for k,v in enumerate(order):
        last=(x[v]+t*signs[(k-1)%n]*last)%p
        out[v]=last
    return out


def matvec(a,x,p):
    return [sum(u*v for u,v in zip(r,x))%p for r in a]


def apply_fft_escape(x,z,p,ledger):
    N=len(x)
    if N==1:
        return x[:]
    if N==2:
        ledger['arithmetic']+=2
        return [(x[0]+x[1])%p,(x[0]-x[1])%p]
    n=N//2; half=pow(2,-1,p); t=pow(2,-1,p)
    order=list(range(n)); signs=[1]*(n-1)+[-1]
    assert pow(t,N,p)!=1
    def C(v,negative=False):
        g=green_scan(order,signs,t,v,p)
        h=green_scan(order,signs,-t%p,v,p)
        ledger['green_applications']+=2
        ledger['arithmetic']+=9*n+2
        return [((b-a) if negative else (a-b))%p for a,b in zip(g,h)]
    def Cinv(v,scalar=1):
        # Each output uses two signed permuted inputs and two scalar multiplies.
        out=[0]*n
        c1=scalar*pow(2*t%p,-1,p)%p; c2=-scalar*t*half%p
        for k,src in enumerate(order):
            nxt=order[(k+1)%n]; prev=order[(k-1)%n]
            out[src]=(c1*signs[k]*v[nxt]+c2*signs[(k-1)%n]*v[prev])%p
        ledger['signed_permutation_passes']+=2
        ledger['arithmetic']+=3*n
        return out
    u=[(x[j]+x[j+n])*half%p for j in range(n)]
    v=[(x[j]-x[j+n])*half%p for j in range(n)]
    ledger['arithmetic']+=4*n
    v=[pow(z,j,p)*v[j]%p for j in range(n)]
    ledger['arithmetic']+=n
    u=apply_fft_escape(u,z*z%p,p,ledger)
    v=apply_fft_escape(v,z*z%p,p,ledger)
    u=[2*a%p for a in u]; ledger['arithmetic']+=n
    v=Cinv(v)
    b=Cinv(u,-half)
    v=[(a+b)%p for a,b in zip(v,b)]; ledger['arithmetic']+=n
    a=C(v)
    u=[(a+b)%p for a,b in zip(u,a)]; ledger['arithmetic']+=n
    v=C(v,negative=True)
    out=[0]*N
    for j in range(n):
        out[2*j]=(u[j]+v[j])%p
        out[2*j+1]=(u[j]-v[j])%p
    ledger['arithmetic']+=2*n
    ledger['output_permutation_words']+=N
    return out


def main():
    for prime in (998244353,2013265921):
        assert all(prime%d for d in range(2,math.isqrt(prime)+1))
    records=[]; vector_records=[]; all_size_records=[]
    for p,generator in ((998244353,3),(2013265921,31)):
        for N in (4,8,16,32,64):
            n=N//2; I=eye(n,p); Z=zero(n); half=pow(2,-1,p)
            z=pow(generator,(p-1)//N,p)
            assert pow(z,N,p)==1 and pow(z,N//2,p)==p-1
            F=[[pow(z,i*j,p) for j in range(N)] for i in range(N)]
            E=block(I,I,I,scale(I,-1,p)); Einv=scale(E,half,p)
            raw=mul(mul(Einv,F,p),E,p)
            blocks=[ [r[j:j+n] for r in raw[i:i+n]] for i,j in ((0,0),(0,n),(n,0),(n,n)) ]
            ranks=[rank(a,p) for a in blocks]
            assert ranks==[n//2]*4
            parity=list(range(0,N,2))+list(range(1,N,2))
            shuffled=mul(mul(Einv,[F[i] for i in parity],p),E,p)
            f=[[pow(z,2*i*j,p) for j in range(n)] for i in range(n)]
            d=[[int(i==j)*pow(z,j,p)%p for j in range(n)] for i in range(n)]
            fd=mul(f,d,p)
            assert shuffled==block(f,fd,f,scale(fd,-1,p))
            H=block(I,I,I,scale(I,-1,p))
            for variant in range(3):
                T,order,signs=signed_cycle(n,p,variant)
                Ti=transpose(T)
                assert mul(T,Ti,p)==I
                for denom in (2,3):
                    t=pow(denom,-1,p)
                    assert pow(t,N,p)!=1
                    Gp=inverse(add(I,scale(T,-t,p),p),p)
                    Gm=inverse(add(I,scale(T,t,p),p),p)
                    C=add(Gp,scale(Gm,-1,p),p)
                    Ci=scale(add(Ti,scale(T,-t*t%p,p),p),pow(2*t%p,-1,p),p)
                    assert mul(C,Ci,p)==I and mul(Ci,C,p)==I
                    C2=mul(C,C,p); CCt=mul(C,transpose(C),p)
                    if n>=4: assert off_diagonal_count(C2)>0
                    else: assert off_diagonal_count(C2)==0
                    if n>=8: assert off_diagonal_count(CCt)>0
                    else: assert off_diagonal_count(CCt)==0
                    B=scale(Ci,-half,p)
                    S=mul(block(I,C,Z,I),block(I,Z,B,I),p)
                    assert S==block(scale(I,half,p),C,B,I)
                    L=block(I,Z,Z,scale(C,-1,p))
                    R=block(scale(I,2,p),Z,Z,Ci)
                    assert mul(mul(L,S,p),R,p)==H
                    full=mul(mul(mul(L,S,p),R,p),block(f,Z,Z,fd),p)
                    assert full==shuffled
                    # Same-kernel mask family: AB = Da C^2 Db remains non-diagonal.
                    aa=[i+2 for i in range(n)]; bb=[2*i+3 for i in range(n)]
                    AB=[[aa[i]*C2[i][j]*bb[j]%p for j in range(n)] for i in range(n)]
                    if n>=4: assert off_diagonal_count(AB)>0
                    x=[(i*i+7*i+11)%p for i in range(n)]
                    assert green_scan(order,signs,t,x,p)==matvec(Gp,x,p)
                    records.append({'prime':p,'N':N,'route_variant':variant,'pole_denominator':denom,
                        'raw_Fourier_sector_ranks':ranks,'C_squared_offdiagonal_entries':off_diagonal_count(C2),
                        'C_Ctranspose_offdiagonal_entries':off_diagonal_count(CCt),
                        'inverse_kernel_identity':True,'normalized_full_Fourier_identity':True})
        for N in (1,2,4,8,16,32,64,128,256):
            z=pow(generator,(p-1)//N,p)
            rng=random.Random(14471+N)
            x=[rng.randrange(p) for _ in range(N)]
            ledger={'arithmetic':0,'green_applications':0,'signed_permutation_passes':0,'output_permutation_words':0}
            y=apply_fft_escape(x,z,p,ledger)
            assert y==[sum(pow(z,i*j,p)*x[j] for j in range(N))%p for i in range(N)]
            if N>=2:
                assert ledger['arithmetic']==17*N*(N.bit_length()-1)-14*N-4
            vector_records.append({'prime':p,'N':N,'exact_seeded_vector_pass':True,**ledger})
    for p,generator,sizes in ((998244353,3,(7,14,17)),(2013265921,31,(3,5,6,10,12,15))):
        for N in sizes:
            M=1
            while M<2*N-1: M*=2
            eta=pow(generator,(p-1)//(2*N),p)
            assert pow(eta,N,p)==p-1
            z=eta*eta%p
            assert pow(z,N,p)==1 and all(pow(z,d,p)!=1 for d in range(1,N))
            w=pow(generator,(p-1)//M,p)
            x=[(7*j*j+9*j+31)%p for j in range(N)]
            a=[0]*M; b=[0]*M
            for j in range(N):
                a[j]=x[j]*pow(eta,j*j,p)%p
            for j in range(-(N-1),N):
                b[j%M]=pow(eta,(-j*j)%(2*N),p)
            ledger={'arithmetic':0,'green_applications':0,'signed_permutation_passes':0,'output_permutation_words':0}
            aa=apply_fft_escape(a,w,p,ledger); bb=apply_fft_escape(b,w,p,ledger)
            product=[u*v%p for u,v in zip(aa,bb)]
            forward=apply_fft_escape(product,w,p,ledger)
            conv=[forward[-j%M]*pow(M,-1,p)%p for j in range(M)]
            y=[pow(eta,j*j,p)*conv[j]%p for j in range(N)]
            expected=[sum(pow(z,i*j,p)*x[j] for j in range(N))%p for i in range(N)]
            assert y==expected
            arithmetic=ledger['arithmetic']+2*M+2*N
            assert arithmetic==3*(17*M*(M.bit_length()-1)-14*M-4)+2*M+2*N
            all_size_records.append({'prime':p,'N':N,'convolution_length':M,
                                     'three_FFTs_including_kernel_spectrum_charged':True,
                                     'exact_non_dyadic_vector_pass':True,'arithmetic_upper_bound':arithmetic})
    out={'status':'PASS','scope':'Exact finite controls supporting the separate uniform algebraic proof; no asymptotic speedup claimed.',
         'source_programs_executed_or_imported':False,'matrix_instances':len(records),'matrix_controls':records,
         'vector_controls':vector_records,'all_size_controls':all_size_records,'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE/'EXACT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':'PASS','matrix_instances':len(records),'vector_instances':len(vector_records),'non_dyadic_instances':len(all_size_records)}))

if __name__=='__main__':
    main()
