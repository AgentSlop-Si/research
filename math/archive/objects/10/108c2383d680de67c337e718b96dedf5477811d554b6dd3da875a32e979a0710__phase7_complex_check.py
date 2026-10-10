#!/usr/bin/env python3
"""Independent complex128 numerical check: same algebra, independent numpy FFT."""
import numpy as np, json
from pathlib import Path

def synth(q,m,r,seed,shifts,a,beta):
    k=q//m
    rng=np.random.default_rng(seed)
    U=rng.normal(size=(k,r))+1j*rng.normal(size=(k,r))
    H=rng.normal(size=(r,m))+1j*rng.normal(size=(r,m))
    b=np.arange(k,dtype=np.int64)[:,None]
    t=np.arange(m,dtype=np.int64)[None,:]
    s=np.exp(2j*np.pi*(a*(t*(t-1)//2)+(a*m*b+beta)*t)/q)
    V=np.empty((k,m),dtype=np.complex128)
    for j in range(m):V[:,j]=U[(np.arange(k)+shifts[j])%k] @ H[:,j]
    return (V/s).reshape(q),U,H,V

def fused(q,m,U,H,shifts,a,beta):
    k=q//m
    out=np.empty(q,dtype=np.complex128)
    gs=np.fft.fft(U,axis=0)
    for ell in range(k):
        t=np.arange(m)
        mu=(ell+a*t)%k
        phases=np.exp(2j*np.pi*(
            -a*t*(t-1)/2-(beta+ell)*t +m*mu*np.asarray(shifts))/q)
        vect=phases*np.sum(gs[mu,:]*H.T,axis=1)
        out[ell::k]=np.fft.fft(vect)
    return out

def run():
    rows=[]
    for q,m in ((32,4),(64,4),(128,8),(256,8),(512,8),(1024,16),(2048,16),(4096,16)):
        k=q//m
        for r in (1,2,4):
            for flag in (0,1):
                rng=np.random.default_rng(123*q+10*r+flag)
                g=[0]*m if flag==0 else rng.choice(k,size=m,replace=False).tolist()
                a=3;beta=7
                x,U,H,V=synth(q,m,r,seed=q+r+flag,shifts=g,a=a,beta=beta)
                got=fused(q,m,U,H,g,a,beta)
                ref=np.fft.fft(x)
                err=float(np.max(np.abs(got-ref))/np.linalg.norm(x))
                rows.append({'q':q,'m':m,'r':r,'hidden_shifts':bool(flag),'relative_linf_error':err})
                assert err<2e-12,(q,m,r,flag,err)
    info={'cases':len(rows),'max_relative_linf_error':max(z['relative_linf_error'] for z in rows),
          'cases_detail':rows}
    Path(__file__).with_name('complex_verification.json').write_text(json.dumps(info,indent=2))
    print('PASS complex cases',len(rows),'max_rel_err',info['max_relative_linf_error'])
if __name__=='__main__':run()
