"""Independent exact field arithmetic audit of the Phase 7 formulas.

Checks both lazy Fourier products and leave-one-factor-out updates without
floating point. This validates algebraic identities, not numerical error or
runtime complexity of the Python production implementation.
"""
import random


def find_root(p,n):
    for w in range(2,p):
        if pow(w,n,p)==1 and all(pow(w,n//q,p)!=1 for q in prime_divisors(n)):
            return w
    raise ValueError('no suitable primitive root')


def prime_divisors(n):
    q=2
    while q*q<=n:
        if n%q==0:
            yield q
            while n%q==0:n//=q
        q+=1
    if n>1:yield n


def fourier(arr,w,p):
    n=len(arr)
    return [sum(x*pow(w,j*k,p) for j,x in enumerate(arr))%p for k in range(n)]


def circular(a,b,p):
    n=len(a)
    return [sum(a[t]*b[(j-t)%n] for t in range(n))%p for j in range(n)]


def conv_all(seq,p):
    n=len(seq[0]); out=[1]+[0]*(n-1)
    for a in seq:out=circular(out,a,p)
    return out


def audit(p=97,n=16,trial_count=500,seed=801):
    assert (p-1)%n==0
    w=find_root(p,n)
    rng=random.Random(seed)
    for trial in range(trial_count):
        m=rng.randrange(2,8)
        signals=[[rng.randrange(p) for _ in range(n)] for _ in range(m)]
        if trial%9==0:signals[0]=[1]*n  # zeros in many Fourier bins
        spectra=[fourier(v,w,p) for v in signals]
        original=conv_all(signals,p)
        assert fourier(original,w,p)==[prod_mod([s[k] for s in spectra],p) for k in range(n)]
        index=rng.randrange(m);pos=rng.randrange(n);delta=rng.randrange(p)
        revised=[s[:] for s in signals]
        revised[index][pos]=(revised[index][pos]+delta)%p
        result=conv_all(revised,p)
        except_conv=conv_all(signals[:index]+signals[index+1:],p)
        expected=[(original[j]+delta*except_conv[(j-pos)%n])%p for j in range(n)]
        assert result==expected,(p,n,trial)
        output_ft=fourier(result,w,p)
        for k in range(n):
            delta_ft=delta*pow(w,pos*k,p)
            predicted=((spectra[index][k]+delta_ft)*prod_mod([spectra[j][k] for j in range(m) if j!=index],p))%p
            assert output_ft[k]==predicted,(p,n,trial,k)
        # Simultaneous changes to two factors (exponential terms not expanded).
        other=(index+1)%m
        revised[other][(pos+2)%n]=(revised[other][(pos+2)%n]+3)%p
        twice=conv_all(revised,p)
        expected_ft=prod_mod_spectra([fourier(v,w,p) for v in revised],p)
        assert fourier(twice,w,p)==expected_ft
    return dict(prime=p,n=n,root=w,checked=trial_count,passed=True)


def prod_mod(v,p):
    result=1
    for x in v:result=result*x%p
    return result


def prod_mod_spectra(specs,p):
    return [prod_mod([s[k] for s in specs],p) for k in range(len(specs[0]))]


if __name__=='__main__':
    for p,n in [(17,8),(97,16),(193,32),(257,64)]:
        print(audit(p,n,trial_count=400))
