"""Independent tiny numerical checks of stated mathematical formulas.
No imports, execution, or dynamic loading of any submitted source code.
These checks supplement the proof; they do not certify floating-point accuracy.
"""
import json, math
import numpy as np


def prime(q):
    return q >= 2 and all(q % d for d in range(2, math.isqrt(q)+1))


def plan(n, alpha=1/3):
    m = math.ceil(math.log2(4*n))
    while not prime(m):
        m += 1
    k = (4*n + m-1)//m
    while any(k % p == 0 for p in range(2,m) if prime(p)):
        k += 1
    return dict(n=n,m=m,k=k,q=m*k,r=m*k-4*n,
                H=math.ceil(n**alpha),L=max(12,math.ceil(2*alpha/math.pi*math.log(n))))


def segmented_check(n):
    p=plan(n); q,r,H,L = [p[x] for x in ['q','r','H','L']]
    rng=np.random.default_rng(n)
    z=rng.normal(size=q)+1j*rng.normal(size=q)
    d=np.arange(-L,L+1)
    info=[]; direct=[]
    for k in range(n):
        f,rem=divmod(k*r,n); b=rem*H//n; theta=(b+0.5)/H
        w=np.exp(-math.pi*(d-theta)**2/L)
        direct.append(w @ z[(4*k+f+d)%q])
        info.append((f,b))
    # Build maximal constant-(integer offset, phase bucket) runs independently.
    cuts=[0]+[k for k in range(1,n) if info[k]!=info[k-1]]+[n]
    B=2*L; F=1
    while F < 4*(B-1)+4*L+1:
        F*=2
    fast=np.zeros(n,dtype=complex)
    chunks=0
    for start,stop in zip(cuts[:-1],cuts[1:]):
        f,b=info[start]; theta=(b+0.5)/H
        taps=np.exp(-math.pi*(d-theta)**2/L)
        spectrum=np.fft.fft(taps[::-1],n=F)
        for k in range(start,stop,B):
            count=min(B,stop-k); chunks+=1
            raw=z[(4*k+f-L+np.arange(4*(B-1)+2*L+1))%q]
            conv=np.fft.ifft(np.fft.fft(raw,n=F)*spectrum)
            fast[k:k+count]=conv[2*L+4*np.arange(count)]
    segments=len(cuts)-1
    assert segments <= (r+1)*H
    assert chunks <= n/B+segments+1e-10
    err=float(np.max(abs(fast-direct)))
    assert err < 2e-13*max(1,float(np.max(np.abs(direct))))
    return {**p,'segments':segments,'segment_bound':(r+1)*H,'chunks':chunks,
            'fft_size':F,'max_FIR_discrepancy':err}


def gaussian_row_check(n):
    p=plan(n); q,m,H,L=[p[x] for x in ['q','m','H','L']]
    c=(n-1)//2; support=(np.arange(n)-c)%q
    t=(np.arange(q)+q//2)%q-q//2
    # q is odd here. This is the representative in [-1/2,1/2).
    t=t/q; tau=max(abs((np.arange(n)-c)/q)); taup=tau+m/q
    sig=math.sqrt(L); amp=math.exp(math.pi*L*tau*tau)
    e=math.exp(-math.pi*L*(1-2*taup)); A=2*e/(1-e)
    T=2*math.exp(-math.pi*L)/(1-math.exp(-2*math.pi))
    bound=math.sqrt(q/n)*m*amp*(A+T/sig)
    phase_bound=math.pi*tau/H
    touched=set(int(i//m) for i in support)
    ext=np.array([i for i in range(q) if i//m in touched])
    g=np.exp(math.pi*L*t[support]**2)/sig
    allj=np.arange(q); local=allj % m; block=allj//m
    states=[(a,b) for a,b in [(1,0),(2,7),(m+2,q//2)] if math.gcd(a,q)==1]
    d=np.arange(-L,L+1)
    maxratio=0.; maxphase=0.; pointwise=0.
    for k in sorted(set([0,1,n//3,n//2,n-1])):
        target=k*q/n; j=4*k+(k*p['r'])//n
        rem=(k*p['r'])%n; bucket=rem*H//n; theta=(bucket+.5)/H
        xi=j+theta
        W=np.exp(-math.pi*(d-theta)**2/L) @ np.exp(-2j*math.pi*(j+d)[:,None]*t[None,:])
        ideal=sig*np.exp(-math.pi*L*t*t)*np.exp(-2j*math.pi*xi*t)
        epsilon=W-ideal
        pointwise=max(pointwise,float(max(abs(epsilon[ext]))/(sig*A+T)))
        # Exact input-row norm for target frequency rounding; center phase has modulus 1.
        dc=(np.exp(-2j*math.pi*xi*t[support])-np.exp(-2j*math.pi*target*t[support]))/math.sqrt(n)
        maxphase=max(maxphase,float(np.linalg.norm(dc))/phase_bound)
        for a,b in states:
            # Chirp phase derived directly from the mathematical block definition.
            S=np.exp(2j*math.pi*(a*local*(local-1)/2+(a*m*block+b)*local)/q
                     +1j*math.pi*local/q)
            coeff=[]
            for jidx,gj in zip(support,g):
                inds=np.arange((jidx//m)*m,(jidx//m+1)*m)
                coeff.append(gj*S[jidx]*(np.conj(S[inds])@epsilon[inds])/math.sqrt(n))
            rownorm=float(np.linalg.norm(coeff)); maxratio=max(maxratio,rownorm/bound)
    assert maxratio < 1.001
    assert maxphase < 1.001
    # W-direct minus ideal has floating cancellation near 1e-13. Bound remains larger at these sizes.
    assert pointwise < 1.001
    return {**p,'gaussian_bound':bound,'max_remainder_operator_to_bound':maxratio,
            'max_phase_operator_to_bound':maxphase,'max_LC4_pointwise_to_bound':pointwise,
            'frequencies':5,'states':len(states)}


def alias_check():
    # Direct full finite-window frequency sums versus independent Poisson dual sums.
    records=[]
    for sig2 in [1.0,2.5,5.0,12.0]:
        sig=math.sqrt(sig2)
        for theta in [.01,.5,.99]:
            ts=np.array([-.24,-.125,0,.125,.24])
            ell=np.arange(-80,81)
            primal=np.exp(-math.pi*(ell-theta)**2/sig2) @ np.exp(-2j*math.pi*ell[:,None]*ts[None,:])
            dual=np.zeros(len(ts),dtype=complex)
            for k in range(-20,21):
                dual+=sig*np.exp(-math.pi*sig2*(ts+k)**2)*np.exp(-2j*math.pi*theta*(ts+k))
            mismatch=float(max(abs(primal-dual)))
            assert mismatch<2e-14
            records.append(mismatch)
    return {'cases':len(records),'max_Poisson_discrepancy':max(records)}


if __name__=='__main__':
    answer={'method':'Independently authored formulas; submitted modules never imported or executed.',
            'segmented_convolution':[segmented_check(n) for n in [67,127,257,509,1009]],
            'gaussian_rows':[gaussian_row_check(n) for n in [67,127,257,509]],
            'poisson':alias_check()}
    print(json.dumps(answer,indent=2))
