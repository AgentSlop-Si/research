"""Fresh independent numerical falsification checks; no project program imported.
These checks do not replace the analytic proof and do not benchmark F132.
"""
import json, math, hashlib
from pathlib import Path
import numpy as np

OUT=Path(__file__).resolve().parent

def kernel(t, M, s):
    t=np.asarray(t,dtype=float)
    t=(t+0.5)%1.0-0.5
    L=M//4; q=M//(8*s)
    DL=(2*L+1)*np.sinc((2*L+1)*t)/np.sinc(t)
    Dq=(2*q+1)*np.sinc((2*q+1)*t)/np.sinc(t)
    return DL/M*(Dq/(2*q+1))**s

cases=[]
for N,s in [(17,2),(19,2),(31,2),(37,3),(65,2),(65,4),(127,3),(129,6)]:
    M=1<<(4*N-1).bit_length(); L=M//4; q=M//(8*s); h=16*s+1
    assert q>=1 and 2*h+2<M
    c=(N-1)//2
    ell=np.arange(N); k=np.arange(M)
    t=ell[:,None]/N-k[None,:]/M
    B=np.sqrt(M/N)*kernel(t,M,s)
    E=np.exp(-2j*np.pi*k[:,None]*(np.arange(N)-c)[None,:]/M)/np.sqrt(M)
    exact=np.exp(-2j*np.pi*ell[:,None]*np.arange(N)[None,:]/N)/np.sqrt(N)
    D=np.exp(-2j*np.pi*c*ell/N)
    identity_error=float(np.max(np.abs(D[:,None]*(B@E)-exact)))
    # Independent convolution definition of cutoff coefficients.
    g=np.ones(2*L+1)
    mu=np.ones(2*q+1)/(2*q+1)
    for _ in range(s):g=np.convolve(g,mu)
    js=np.arange(-L-s*q,L+s*q+1)
    passband_error=float(np.max(np.abs(g[np.abs(js)<=M//8]-1)))
    alias_squares=np.bincount(js%N,weights=g*g,minlength=N)
    exact_alias_norm=float(np.sqrt(np.max(alias_squares)))
    r=(ell*M)//N; theta=ell*M/N-r
    offsets=np.arange(-h,h+2)
    ix=(r[:,None]+offsets[None,:])%M
    Bh=np.zeros_like(B)
    Bh[np.arange(N)[:,None],ix]=B[np.arange(N)[:,None],ix]
    tail=B-Bh
    row_tail=float(np.max(np.sum(np.abs(tail),axis=1)))
    col_tail=float(np.max(np.sum(np.abs(tail),axis=0)))
    schur_tail=math.sqrt(row_tail*col_tail)
    tail_bound=12*4.0**(-s)
    quant=[]
    for a in [4,8,12]:
        eta=2.0**(-a); th=np.floor(theta/eta)*eta
        values=kernel((th[:,None]-offsets[None,:])/M,M,s)
        values=np.round(values/eta)*eta
        Bt=np.zeros_like(B)
        Bt[np.arange(N)[:,None],ix]=np.sqrt(M/N)*values
        err=Bt-Bh
        schur=math.sqrt(float(np.max(np.sum(np.abs(err),axis=1)))*float(np.max(np.sum(np.abs(err),axis=0))))
        bound=15*(2*h+4)*eta
        quant.append(dict(a=a,schur_error=schur,claimed_bound=bound,pass_check=schur<=bound))
    # Finite-difference derivative only as a falsification probe.
    theta_test=np.linspace(-h-0.37,h+0.63,1001)
    step=1e-5
    deriv=(kernel((theta_test+step)/M,M,s)-kernel((theta_test-step)/M,M,s))/(2*step)
    maxder=float(np.max(np.abs(deriv)))
    rec=dict(N=N,M=M,s=s,q=q,h=h,identity_max_entry_error=identity_error,passband_error=passband_error,alias_operator_norm=exact_alias_norm,tail_row_sum=row_tail,tail_column_sum=col_tail,tail_schur=schur_tail,tail_bound=tail_bound,max_finite_difference_derivative=maxder,quantization=quant)
    assert identity_error<2e-12 and passband_error<2e-12 and exact_alias_norm<=math.sqrt(8)+1e-12 and schur_tail<=tail_bound+1e-12 and maxder<4
    cases.append(rec)

# Construct an error allowed by the chirp FFT l2 contract and test its actual
# amplification after restricted input/output embeddings. This is not F132 error.
blue=[]
for N in [17,31,65,127,257,1001]:
    M=1<<(2*N-2).bit_length(); delta=1e-5
    k0=3
    t=np.arange(N)
    x=np.exp(1j*np.pi*t*t/N)*np.exp(2j*np.pi*k0*t/M)/np.sqrt(N)
    a=np.zeros(M,complex);a[:N]=x*np.exp(-1j*np.pi*t*t/N)
    z=np.fft.fft(a,norm='ortho')
    lam_err=np.zeros(M,complex);lam_err[k0]=math.sqrt(M/N)*delta*math.sqrt(2*N-1)
    out_err=np.fft.ifft(lam_err*z,norm='ortho')[:N]
    observed=float(np.linalg.norm(out_err)/delta)
    predicted=math.sqrt(N*(2*N-1)/M)
    assert abs(observed-predicted)<1e-10
    blue.append(dict(N=N,M=M,observed_error_over_delta=observed,predicted=predicted,ratio_over_sqrtN=observed/math.sqrt(N)))

result=dict(status='all independent numerical checks passed',scope='Analytic interpolation identities, norms, tails, coefficient discretization, and black-box Bluestein obstruction only. Not an execution or runtime test of uploaded F132 programs; numerical checks are not proofs.',interpolation_cases=cases,bluestein_cases=blue,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
(OUT/'fresh_check_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['interpolation_cases','bluestein_cases']},indent=2))
print('Interpolation cases:',len(cases),'Bluestein cases:',len(blue))
