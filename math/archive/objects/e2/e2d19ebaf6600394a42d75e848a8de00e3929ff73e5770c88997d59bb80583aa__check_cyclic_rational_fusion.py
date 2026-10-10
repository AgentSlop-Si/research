"""Exact cyclic rational sampling identities, including resonant poles.
Standard-library tests, not a faster-FFT benchmark.
"""
import random,json
from pathlib import Path
P=97

def root(n):
    factors=[q for q in range(2,n+1) if n%q==0 and all(q%d for d in range(2,int(q**.5)+1))]
    return next(z for z in range(1,P) if pow(z,n,P)==1 and all(pow(z,n//q,P)!=1 for q in factors))

def recover(samples,lam,omega):
    S=len(samples); invS=pow(S,-1,P)
    return [(sum(y*pow(omega,(-j*r)%S,P) for j,y in enumerate(samples))*invS*pow(lam,-r,P))%P for r in range(S)]

def mul(a,b):
    out=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): out[i+j]=(out[i+j]+x*y)%P
    return out

def mod(a,q):
    a=a[:]; k=len(q)-1; iq=pow(q[-1],-1,P)
    for i in range(len(a)-1,k-1,-1):
        c=a[i]*iq%P
        for j,v in enumerate(q): a[i-k+j]=(a[i-k+j]-c*v)%P
    return (a+[0]*k)[:k]

def modpow(a,n,q):
    out=[1]
    while n:
        if n&1: out=mod(mul(out,a),q)
        a=mod(mul(a,a),q); n//=2
    return mod(out,q)

def numerator(zs,weights):
    out=[0]*len(zs)
    for i,b in enumerate(weights):
        prod=[1]
        for j,z in enumerate(zs):
            if i!=j: prod=mul(prod,[1,-z%P])
        out=[(x+b*y)%P for x,y in zip(out,prod)]
    return out

def main():
    rng=random.Random(2026100909); counts=dict(cases=0,pole_free_cases=0,resonant_cases=0,resonant_grid_values=0,uncorrected_differs_from_target=0)
    for N in [3,4,6,8,12,16,24,32]:
        zeta=root(N)
        for S in [1,2,4,8,16,32]:
            omega=root(S)
            for _ in range(20):
                k=rng.randint(1,min(N,8)); js=rng.sample(range(N),k)
                zs=[pow(zeta,j,P) for j in js]; start=rng.randrange(2*N)
                bs=[rng.randrange(1,P)*pow(z,start,P)%P for z in zs]
                lam=rng.randrange(1,P); c=pow(lam,S,P)
                q=[1]
                for z in zs:q=mul(q,[1,-z%P])
                num=numerator(zs,bs)
                t_inverse=[-x%P for x in q[1:]]
                rS=modpow(t_inverse,S,q)
                factor=[-c*x%P for x in rS]; factor[0]=(factor[0]+1)%P
                corrected=mod(mul(factor,num),q)
                assert corrected==numerator(zs,[b*(1-c*pow(z,S,P))%P for b,z in zip(bs,zs)])
                target=[sum(b*pow(z,r,P) for b,z in zip(bs,zs))%P for r in range(S)]
                samples=[]; resonant=False
                for j in range(S):
                    t=lam*pow(omega,j,P)%P; y=0
                    for b,z in zip(bs,zs):
                        den=(1-z*t)%P; num=(1-c*pow(z,S,P))%P
                        if den==0:
                            assert num==0
                            y+=b*S; resonant=True; counts['resonant_grid_values']+=1
                        else: y+=b*num*pow(den,-1,P)
                    samples.append(y%P)
                assert recover(samples,lam,omega)==target
                if resonant: counts['resonant_cases']+=1
                else:
                    counts['pole_free_cases']+=1
                    raw=[sum(b*pow((1-z*lam*pow(omega,j,P))%P,-1,P) for b,z in zip(bs,zs))%P for j in range(S)]
                    aliased=[sum(b*pow(z,r,P)*pow((1-c*pow(z,S,P))%P,-1,P) for b,z in zip(bs,zs))%P for r in range(S)]
                    got=recover(raw,lam,omega); assert got==aliased
                    counts['uncorrected_differs_from_target']+=got!=target
                counts['cases']+=1
    result=dict(status='passed',field_prime=P,counts=counts,numerator_correction_checks=counts['cases'],
      limitation='Identities tested with direct quadratic-size summations; not a fast implementation or complexity proof.')
    Path(__file__).with_name('cyclic_rational_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
