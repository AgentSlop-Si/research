#!/usr/bin/env python3
"""Independent finite controls for the v11 mathematical audit.
No source-bundle code is imported, evaluated, or executed. Only NumPy and
mpmath (installed libraries) are used. Claims of exactness rest on proofs,
not on these floating-point checks.
"""
import json, math, platform, hashlib
from pathlib import Path
import numpy as np
import mpmath as mp
mp.mp.dps = 70
OUT = Path(__file__).resolve().parent
SOURCE = OUT.parent / 'extracted' / 'fft_all_length_fused_fp_v11(1)' / 'fft_all_length_fused_fp_v11'

def bj(r,z):
    """Fresh bounded-argument factorial series, not SciPy or uploaded code."""
    sign = (-1)**(-r) if r < 0 else 1
    r = abs(r)
    z = np.asarray(z, dtype=float)
    term = np.ones_like(z)
    for j in range(1,r+1): term *= z/(2*j)
    acc = term.copy()
    for j in range(1,40):
        term = term * (-z*z/(4*j*(r+j)))
        acc = acc + term
    return sign*acc

def grid(n):
    q=1<<(n-1).bit_length()
    j=np.array([(2*k*q+n)//(2*n) for k in range(n)],dtype=int)
    d=np.array([k*q-int(j[k])*n for k in range(n)],dtype=int)
    return q,j,d/n

def tail(R):
    a=math.pi/2
    return 2*math.exp(math.pi**2/(4*(R+1)))*a**R/math.factorial(R)/(1-a/(R+1))

def local_tail(delta,H):
    a=delta/2; r=H+1
    return 2*math.exp(delta*delta/(4*(r+1)))*a**r/math.factorial(r)/(1-a/(r+1))

def cheb_coeff(theta,R):
    # Independent cosine definition, rather than Chebyshev recurrence.
    x=np.clip(2*theta,-1,1)
    c=np.array([np.cos(r*np.arccos(x)) for r in range(R)],dtype=complex)
    for r in range(1,R): c[r] *= 2*(-1j)**r
    return c

def clenshaw(c,theta):
    n=c.shape[1]; u=np.zeros(n,dtype=complex); v=u.copy(); node=2*theta
    for r in reversed(range(1,len(c))):
        w=c[r]+2*node*u-v
        v,u=u,w
    return c[0]+node*u-v

def phase_matrix(q,m,a,beta):
    k=q//m
    return np.array([[np.exp(2j*math.pi*((a*t*(t-1)//2+(a*m*b+beta)*t)%q)/q) for t in range(m)] for b in range(k)])

def compress_matrix(q,m,a,beta):
    S=phase_matrix(q,m,a,beta); C=np.zeros((q//m,q),complex)
    for b in range(q//m): C[b,b*m:(b+1)*m]=S[b]
    return C

def dft(q):
    return np.exp(-2j*np.pi*np.outer(np.arange(q),np.arange(q))/q)/math.sqrt(q)

def recurrence_decoder(q,m,a,beta,d,selected):
    """Closed-form cycle recurrence; direct DFT and cumsum are independent controls."""
    k=q//m
    f=np.exp(-2j*np.pi*np.outer(np.arange(k),np.arange(k))/k) @ d
    cycle=np.array([(a*t)%q for t in range(q)])
    gauge=np.array([np.exp(2j*np.pi*((a*t*(t-1)//2+beta*t)%q)/q) for t in range(q)])
    boundary=np.array([np.exp(-2j*np.pi*((m*(int(v)+beta)+a*m*(m-1)//2)%q)/q) for v in cycle])
    forcing=(f[cycle%k]-boundary*f[(cycle+a*m)%k])/math.sqrt(q)
    terms=forcing/gauge
    prefix=np.r_[0,np.cumsum(terms[:-1])]
    y=np.empty(q,complex); y[cycle]=gauge*(sum(terms)/2-prefix)
    return y[selected]

def weights(n,m,R,H):
    q,selected,theta=grid(n); k=q//m; coeff=cheb_coeff(theta,R)
    z=math.pi*np.arange(k)/k; delta=math.pi*np.arange(m)/q
    exact=np.array([bj(r,math.pi*np.arange(n)/q) for r in range(R)])
    approx=[]
    for r in range(R):
        a=np.zeros((k,m))
        for h in range(-H,H+1): a+=bj(r-h,z)[:,None]*bj(h,delta)[None,:]
        approx.append(a.ravel()[:n])
    approx=np.array(approx)
    return coeff.T @ exact, coeff.T @ approx, approx

results={'scope':'Independent mathematical controls, no uploaded-code execution', 'python':platform.python_version(), 'numpy':np.__version__, 'mpmath':mp.__version__}
# Verify scalar reconstruction against an independent high-precision library.
max_bessel=0.0
for r in range(-4,19):
    for z in [0,.001,.1,.7,1.5,math.pi]:
        max_bessel=max(max_bessel,abs(float(bj(r,z))-float(mp.besselj(r,z))))
assert max_bessel<2e-14
results['bessel_series_max_abs_error']=max_bessel
# Exact arithmetic grid identities, including trivial N=1.
for n in range(1,514):
    q,j,theta=grid(n)
    assert len(set(j))==n and min(j)>=0 and max(j)<q
    assert max(abs(theta))<=.5
results['exact_grid_lengths_checked']=513
# Selected cycle decoder equals direct U C* at all small states.
decoder_checks=[]; rng=np.random.default_rng(9102026)
for q,m in [(8,2),(16,4),(32,4)]:
    U=dft(q); selected=np.arange(0,q,2); d=rng.normal(size=q//m)+1j*rng.normal(size=q//m)
    err=0.0
    for a in range(1,q,2):
        for beta in range(q):
            C=compress_matrix(q,m,a,beta)
            ref=(U@C.conj().T@d)[selected]
            got=recurrence_decoder(q,m,a,beta,d,selected)
            err=max(err,float(np.max(abs(got-ref))))
    assert err<2e-12
    decoder_checks.append({'Q':q,'M':m,'states':q*q//2,'max_abs_error':err})
results['selected_decoder_exhaustive']=decoder_checks
# Clenshaw vs direct polynomial sum with factorial-decaying row magnitudes.
clenshaw_error=0.0
for n in [7,13,31,61]:
    q,j,theta=grid(n)
    for R in [1,2,6,12,20]:
        raw=rng.normal(size=(R,n))+1j*rng.normal(size=(R,n))
        raw*=np.array([(math.pi/2)**r/math.factorial(r) for r in range(R)])[:,None]
        coeff=raw.copy()
        for r in range(1,R): coeff[r]*=2*(-1j)**r
        ref=np.sum(raw*cheb_coeff(theta,R),axis=0)
        clenshaw_error=max(clenshaw_error,float(np.max(abs(ref-clenshaw(coeff,theta)))))
assert clenshaw_error<5e-14
results['clenshaw_direct_max_abs_error']=clenshaw_error
# Kernel tails, exact center operator infinity-from-2 norm, negative channel parity.
kernel_checks=[]; negative_error=0.0
for n,m in [(7,2),(13,4),(31,4),(61,8),(127,8)]:
    q,j,theta=grid(n); delta=math.pi*(m-1)/q
    for R in [4,8,12]:
        exact_kernel=np.exp(-2j*np.pi*np.outer(theta,np.arange(n)/q))
        for H in [0,1,2]:
            trunc,fused,wr=weights(n,m,R,H)
            source_eps=tail(R)+(2*R-1)*local_tail(delta,H)
            fused_error=float(np.max(abs(fused-exact_kernel)))
            addition_error=float(np.max(abs(fused-trunc)))
            center_2inf=float(np.max(np.linalg.norm(fused-exact_kernel,axis=1))/math.sqrt(n))
            assert addition_error<=(2*R-1)*local_tail(delta,H)+3e-14
            assert fused_error<=source_eps+3e-14
            row={'N':n,'Q':q,'M':m,'R':R,'H':H,'kernel_error':fused_error,'center_2_to_inf':center_2inf,'source_bound':source_eps,'addition_ratio':addition_error/max((2*R-1)*local_tail(delta,H),1e-300)}
            if H==0:
                sharp=tail(R)+delta
                assert fused_error<=sharp+3e-14
                row['sharper_H0_bound']=sharp
                row['sharper_H0_ratio']=fused_error/sharp
            kernel_checks.append(row)
    for h in range(1,5):
        negative_error=max(negative_error,float(np.max(abs(bj(-h,math.pi*np.arange(m)/q)-(-1)**h*bj(h,math.pi*np.arange(m)/q)))))
results['kernel_checks']=kernel_checks
results['negative_channel_parity_max_error']=negative_error
# Exhaustively average random states and check full error covariance matrices.
cov_checks=[]; rank_checks=[]
for n,m in [(7,2),(13,4),(17,4)]:
    q,selected,theta=grid(n); U=dft(q); R=10
    for H in [0,1]:
        _,W,_=weights(n,m,R,H)
        base=math.sqrt(q/n)*U[selected,:n]
        center=base*W
        all_L=[]; compressions=[]
        for a in range(1,q,2):
            for beta in range(q):
                C=compress_matrix(q,m,a,beta)
                L=math.sqrt(q/n)*(U[selected]@(C.conj().T@C))[:,:n]*W
                all_L.append(L)
        all_L=np.array(all_L)
        mean_error=float(np.max(abs(all_L.mean(axis=0)-center)))
        eig_ratio=0.0
        for out in range(n):
            e=all_L[:,out,:]-center[out]
            cov=e.conj().T@e/len(all_L)
            eig=float(np.linalg.eigvalsh(cov)[-1])
            bound=m/n*float(np.max(abs(W[out])))**2
            eig_ratio=max(eig_ratio,eig/bound)
        assert mean_error<1e-13 and eig_ratio<=1+1e-12
        cov_checks.append({'N':n,'Q':q,'M':m,'H':H,'states':len(all_L),'mean_max_error':mean_error,'max_covariance_ratio_using_actual_kernel_envelope':eig_ratio})
        # Demonstrate the fused row really factors through H+1 local channels.
        a,beta=1,2; C=compress_matrix(q,m,a,beta); k=q//m
        reduced=[]
        for h in range(H+1):
            wt=np.tile(bj(h,math.pi*np.arange(m)/q),k)
            reduced.append((C*wt)[:,:n])
        G=np.vstack(reduced)
        rank=int(np.linalg.matrix_rank(G,tol=1e-11))
        L=all_L[beta]
        rankL=int(np.linalg.matrix_rank(L,tol=1e-11))
        assert rankL<=rank and rank<=(H+1)*k
        # Row map recovery from G is a numerical factorization diagnostic only.
        residual=float(np.max(abs(L-(L@np.linalg.pinv(G))@G)))
        assert residual<2e-11
        rank_checks.append({'N':n,'Q':q,'M':m,'H':H,'rank_channels':rank,'rank_row':rankL,'rank_cap':(H+1)*k,'factorization_max_error':residual})
results['exhaustive_fused_covariance']=cov_checks
results['reduced_channel_rank']=rank_checks
# H=0 limiting error and frozen-block Taylor check (exact arithmetic formulas).
frozen=[]
for n,m in [(13,4),(31,4),(61,8),(127,8)]:
    q,j,theta=grid(n); b=np.arange(n)//m; delta=math.pi*(m-1)/q
    true=np.exp(-2j*np.pi*np.outer(theta,np.arange(n)/q))
    frozen_kernel=np.exp(-2j*np.pi*np.outer(theta,b*m/q))
    err=float(np.max(abs(frozen_kernel-true)))
    assert err<=delta+2e-14
    R=12; z=-2j*np.pi*np.outer(theta,b*m/q); term=np.ones_like(z); poly=term.copy()
    for r in range(1,R): term*=z/r; poly+=term
    taylor_error=float(np.max(abs(poly-true)))
    bound=delta+math.pi**R/math.factorial(R)
    assert taylor_error<=bound+2e-14
    frozen.append({'N':n,'M':m,'frozen_bias':err,'Delta':delta,'Taylor_R':R,'Taylor_total_error':taylor_error,'Taylor_bound':bound})
results['frozen_block_variant']=frozen
# Source manifests are data only; independently hash every top-level source file.
evidence={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(SOURCE.iterdir()) if p.is_file()}
(OUT/'SOURCE_CHECKSUMS.json').write_text(json.dumps(evidence,indent=2)+'\n')
results['all_assertions_passed']=True
(OUT/'CHECK_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
print('PASS: independent Bessel series, 513 exact grids, 672 decoder states, Clenshaw, 45 kernel cases, 6 exhaustive covariance cases, 6 rank cases, 4 frozen-block controls.')
print('Bessel series maximum error:',max_bessel)
print('Selected decoder maximum error:',max(v['max_abs_error'] for v in decoder_checks))
print('Clenshaw maximum error:',clenshaw_error)
print('Covariance maximum ratio:',max(v['max_covariance_ratio_using_actual_kernel_envelope'] for v in cov_checks))
print('No uploaded code was executed or imported.')
