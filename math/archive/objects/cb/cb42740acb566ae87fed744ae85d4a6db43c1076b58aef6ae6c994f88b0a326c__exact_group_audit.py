"""Independent finite-field verification of grouped FFT stage identity.

Modulus 998244353 admits all tested power-of-two roots. Arithmetic is exact
mod p, so no approximate/floating-point equality enters this audit.
"""
import random
P=998244353
GEN=3

def reverse(i,b):
    o=0
    for _ in range(b): o=(o<<1)|(i&1);i>>=1
    return o

def iterative_stage_group(a,s,t):
    a=list(a); n=len(a); inv2=pow(2,-1,P)
    for h in range(s+1,s+t+1):
        span=1<<h;half=span//2
        root=pow(GEN,(P-1)//span,P)
        for base in range(0,n,span):
            w=1
            for j in range(half):
                u=a[base+j];v=a[base+j+half]*w%P
                a[base+j]=(u+v)*inv2%P
                a[base+j+half]=(u-v)*inv2%P
                w=w*root%P
    return a

def reused_template_stage_group(a,s,t):
    a=list(a);n=len(a);K=1<<t;J=1<<s;M=J*K
    kroot=pow(GEN,(P-1)//K,P)
    mroot=pow(GEN,(P-1)//M,P)
    kinv=pow(K,-1,P)
    res=a[:]
    for base in range(0,n,M):
        for j in range(J):
            z=[0]*K
            for r in range(K):
                b=reverse(r,t)
                z[b]=a[base+j+J*r]*pow(mroot,j*b,P)%P
            for k in range(K):
                wk=pow(kroot,k,P)
                power=1;tot=0
                for v in z:
                    tot=(tot+v*power)%P
                    power=power*wk%P
                res[base+j+J*k]=tot*kinv%P
    return res

def run():
    rng=random.Random(708)
    cases=0;basis_cases=0
    for L in range(2,9):
        n=1<<L
        for s in range(L):
            for t in range(1,L-s+1):
                values=[rng.randrange(P) for _ in range(n)]
                a=iterative_stage_group(values,s,t)
                b=reused_template_stage_group(values,s,t)
                assert a==b,('random input',n,s,t)
                cases+=1
                if n<=32:
                    for i in range(n):
                        basis=[0]*n;basis[i]=1
                        assert iterative_stage_group(basis,s,t)==reused_template_stage_group(basis,s,t),(n,s,t,i)
                        basis_cases+=1
    print(f'PASS exact finite-field stage group: {cases} random vector configurations')
    print(f'PASS full-input-matrix check: {basis_cases} basis vectors')
    print('Scope: finite-size evidence. General all-length formula follows from the Cooley-Tukey factorization.')
    return cases,basis_cases
if __name__=='__main__':run()
