#!/usr/bin/env python3
"""Independent v13 audit. No source checkpoint code is imported or executed.
Run: python independent_v13_audit.py [output.json]
Only Python standard library and NumPy are used. Exact finite-field checks
are kept distinct from complex floating-point identity controls.
"""
import hashlib
import itertools
import json
import math
import sys
from pathlib import Path
import numpy as np


def factors(n):
    out=[]
    d=2
    while d*d<=n:
        if n%d==0:
            out.append(d)
            while n%d==0:n//=d
        d+=1
    if n>1:out.append(n)
    return out


def root(n,p):
    assert p>1 and all(p%d for d in range(2,math.isqrt(p)+1))
    assert (p-1)%n==0
    for a in range(1,p):
        if pow(a,n,p)==1 and all(pow(a,n//q,p)!=1 for q in factors(n)):
            return a
    raise AssertionError('root missing')


def phase(g,M,a,b,r,u):
    return (a*u*(u-1)//2+(a*M*r+b)*u)%g


def local_modular(g,M,a,b,p,z):
    """Independently evaluate the unnormalized recurrence for every basis input.
    The forcing and anti-periodic closure are derived from the phase's
    first difference, rather than calling the supplied checker or decoder.
    """
    K=g//M
    B=[[0]*g for _ in range(g)]
    P=[[0]*g for _ in range(g)]
    for n in range(g):
        r,u=divmod(n,M)
        c=pow(z,phase(g,M,a,b,r,u),p)
        H=[c*pow(z,(-j*M*r)%g,p)%p for j in range(K)]
        terms=[]
        gauges=[]
        for j in range(g):
            k=(a*j)%g
            gauge=pow(z,(a*j*(j-1)//2+b*j)%g,p)
            boundary=pow(z,(-M*(k+b)-a*M*(M-1)//2)%g,p)
            forcing=(H[k%K]-boundary*H[(k+a*M)%K])%p
            terms.append(forcing*pow(gauge,-1,p)%p)
            gauges.append(gauge)
        assert pow(z,(a*g*(g-1)//2+b*g)%g,p)==p-1
        value=sum(terms)*pow(2,-1,p)%p
        prefix=0
        for j in range(g):
            B[(a*j)%g][n]=gauges[j]*(value-prefix)%p
            prefix=(prefix+terms[j])%p
        for v in range(M):
            P[r*M+v][n]=pow(z,(phase(g,M,a,b,r,u)-phase(g,M,a,b,r,v))%g,p)
        for k in range(g):
            expected=sum(P[r*M+v][n]*pow(z,(-k*(r*M+v))%g,p) for v in range(M))%p
            assert B[k][n]==expected
    return B,P


def modular_rank(A,p):
    A=[r[:] for r in A]
    nr=len(A); nc=len(A[0]); row=0
    for col in range(nc):
        pivot=next((i for i in range(row,nr) if A[i][col]%p),None)
        if pivot is None:continue
        A[row],A[pivot]=A[pivot],A[row]
        inv=pow(A[row][col],-1,p)
        A[row]=[v*inv%p for v in A[row]]
        for i in range(nr):
            if i!=row and A[i][col]%p:
                c=A[i][col]
                A[i]=[(a-c*b)%p for a,b in zip(A[i],A[row])]
        row+=1
        if row==nr:break
    return row


def exact_case(N,p,M):
    g=N&-N; m=N//g; K=g//M
    z=root(N,p); zg=pow(z,m,p)
    if g==1:
        assert M==1
        return dict(N=N,p=p,M=M,degenerate_odd=True,primitive_root_verified=True)
    assert M<=K and g%M==0 and not M&(M-1)
    all_B=[]; all_P=[]; reversed_disagreements=0; local_entries=0
    for s in range(m):
        a=(2*s+1)%g; b=(3*s+1)%g
        bank=[]; projectors=[]
        for t in range(M):
            B,P=local_modular(g,M,a,(b+t*K)%g,p,zg)
            assert modular_rank(P,p)==K
            bank.append(B); projectors.append(P)
            if t==0:
                for q in range(g):
                    r,u=divmod(q,M)
                    for k in range(g):
                        reversed_value=sum(pow(zg,(phase(g,M,a,b,r,v)-phase(g,M,a,b,r,u)-k*(r*M+v))%g,p) for v in range(M))%p
                        reversed_disagreements+=(B[k][q]!=reversed_value)
        for i in range(g):
            for j in range(g):
                assert sum(P[i][j] for P in projectors)%p==(M if i==j else 0)
                local_entries+=1
        for length in range(1,M+1):
            partial=[[sum(P[i][j] for P in projectors[:length])%p for j in range(g)] for i in range(g)]
            assert modular_rank(partial,p)==length*K
        all_B.append(bank);all_P.append(projectors)
    one_row_entries=0; bank_entries=0
    for n in range(N):
        q,s=divmod(n,m)
        r,u=divmod(q,M)
        for k in range(N):
            k1=k%g
            total=0
            for t in range(M):
                actual=all_B[s][t][k1][q]*pow(z,(-k*s)%N,p)%p
                expected=sum(all_P[s][t][r*M+v][q]*pow(z,(-k*((r*M+v)*m+s))%N,p) for v in range(M))%p
                assert actual==expected
                total+=actual
                one_row_entries+=1
            assert total*pow(M,-1,p)%p==pow(z,(-k*n)%N,p)
            bank_entries+=1
    bad_spacing=False
    if M>1:
        bad=sum(pow(zg,t*(K+1),p) for t in range(M))%p
        assert bad!=0
        bad_spacing=True
        assert reversed_disagreements>0
    return dict(N=N,G=g,m=m,p=p,M=M,primitive_root=z,
                executor_entries_verified=one_row_entries,
                completed_bank_entries_verified=bank_entries,
                local_identity_entries_verified=local_entries,
                reversed_one_row_phase_disagreements=reversed_disagreements,
                wrong_spacing_rejected=bad_spacing)


def fourier(n):
    j=np.arange(n)
    return np.exp(-2j*np.pi*j[:,None]*j[None,:]/n)/math.sqrt(n)


def local_projector(g,M,a,b):
    P=np.zeros((g,g),complex)
    for r in range(g//M):
        s=np.exp(2j*np.pi*np.array([phase(g,M,a,b,r,u) for u in range(M)])/g)
        P[r*M:(r+1)*M,r*M:(r+1)*M]=np.outer(s.conj(),s)
    return P


def cov_integer(g,M):
    H=np.zeros((g,g),dtype=np.int64)
    for i in range(g):
        di=set(range(i%M-M+1,i%M+1))-{0}
        for j in range(g):
            dj=set(range(j%M-M+1,j%M+1))-{0}
            for d in di&dj:
                c=d*(j-i)%g
                H[i,j]+=1 if c==0 else (-1 if c==g//2 else 0)
    assert np.array_equal(H,H.T)
    assert np.array_equal(H@H,M*H)
    assert int(np.trace(H))==g*(M-1)
    for i in range(g):
        for j in range(g):
            if i%M!=j%M:assert H[i,j]==0
    return H


def dyadic_covariance():
    exact=[]; numeric=[]
    for g in (2,4,8,16,32,64,128):
        for M in (1,2,4,8):
            if M*M>g:continue
            H=cov_integer(g,M)
            exact.append(dict(G=g,M=M,nonzero_rank=0 if M==1 else g-g//M))
    for g,M in ((4,2),(8,2),(16,2),(16,4),(32,4)):
        F=fourier(g); I=np.eye(g); H=cov_integer(g,M)
        E=np.array([F@(local_projector(g,M,a,b)-I) for a in range(1,g,2) for b in range(g)])
        mean_error=float(np.max(abs(E.mean(axis=0))))
        residual=0.
        for k in range(g):
            empirical=E[:,k,:].conj().T@E[:,k,:]/len(E)
            d=np.exp(2j*np.pi*k*np.arange(g)/g)
            predicted=d[:,None]*(H/g)*d.conj()[None,:]
            residual=max(residual,float(np.max(abs(empirical-predicted))))
        assert mean_error<2e-13 and residual<2e-13
        numeric.append(dict(G=g,M=M,states=len(E),all_outputs=True,mean_residual=mean_error,covariance_residual=residual))
    return dict(exact_integer_projector_cases=exact,exhaustive_complex_ensemble_cases=numeric)


def gf_multiply(x,y,L,poly):
    z=0
    while y:
        if y&1:z^=x
        y>>=1;x<<=1
        if x&(1<<L):x^=poly
    return z


def pairwise_extension(g,m,M,L,poly):
    assert g==1<<L and m<=g
    schedules=np.array([[gf_multiply(A,s,L,poly)^B for s in range(m)] for A in range(g) for B in range(g)])
    for s in range(m):
        assert np.all(np.bincount(schedules[:,s],minlength=g)==g)
        for t in range(s):
            assert np.all(np.bincount(schedules[:,s]*g+schedules[:,t],minlength=g*g)==1)
    rng=np.random.default_rng(74013+g+m)
    x=rng.normal(size=g*m)+1j*rng.normal(size=g*m)
    cols=x.reshape(g,m); F=fourier(g); Fm=fourier(m)
    omega=np.exp(-2j*np.pi*np.arange(g)[:,None]*np.arange(m)[None,:]/(g*m))
    target=fourier(g*m)@x
    H=cov_integer(g,M)
    prediction=[]
    for k in range(g):
        d=np.exp(2j*np.pi*k*np.arange(g)/g)
        Q=d[:,None]*(H/g)*d.conj()[None,:]
        prediction.append(sum((cols[:,s].conj()@Q@cols[:,s]).real for s in range(m))/m)
    prediction=np.tile(prediction,m)
    errors=[]
    for a in range(1,g,2):
        cache=np.array([[F@local_projector(g,M,a,b)@cols[:,s] for b in range(g)] for s in range(m)])
        for betas in schedules:
            stages=np.column_stack([cache[s,betas[s],:] for s in range(m)])
            y=((stages*omega)@Fm.T).T.reshape(g*m)
            errors.append(y-target)
    errors=np.array(errors)
    actual=np.mean(abs(errors)**2,axis=0)
    residual=float(np.max(abs(actual-prediction)))
    assert residual<1e-11
    assert np.max(abs(errors.mean(axis=0)))<1e-12
    # Identical full-state reuse has the advertised m-fold worst-direction variance.
    w=np.zeros(g,complex)
    w[::M]=np.exp(2j*np.pi*np.arange(g//M)/(g//M))/math.sqrt(g//M)
    shared_errors=[]
    for a in range(1,g,2):
        for b in range(g):
            shared_errors.append(math.sqrt(m)*(F@(local_projector(g,M,a,b)-np.eye(g))@w)[0])
    shared_var=float(np.mean(abs(np.array(shared_errors))**2))
    baseline=M/g
    assert abs(shared_var/baseline-m)<1e-12
    return dict(G=g,m=m,M=M,enumerated_shared_slope_hash_states=len(errors),
                pairwise_beta_counts_exact=True,covariance_max_residual=residual,
                common_full_state_variance_ratio=shared_var/baseline,
                random_bits_this_construction=3*L-1,
                random_bits_independent_full_states=m*(2*L-1))


def conditioning_control(g,m,M):
    N=g*m; F=fourier(N)
    bank=[]
    for t in range(M):
        P=np.zeros((N,N),complex)
        for s in range(m):
            ids=np.arange(g)*m+s
            P[np.ix_(ids,ids)]=local_projector(g,M,2*s+1,(s+t*(g//M))%g)
        bank.append(F@P)
    stack=np.vstack(bank)/M
    residual=float(np.max(abs(stack.conj().T@stack-np.eye(N))))
    assert residual<1e-12
    assert np.max(abs(sum(bank)/M-F))<1e-12
    singular=np.linalg.svd(bank[0],compute_uv=False)
    assert np.max(abs(singular[:N//M]-M))<1e-11
    assert np.max(abs(singular[N//M:]))<1e-11
    # A shared twiddle table is downstream of each local sketch. Its error
    # cancels the M amplification exactly on averaging the complete bank.
    rng=np.random.default_rng(882)
    x=rng.normal(size=N)+1j*rng.normal(size=N)
    twiddle=np.exp(-2j*np.pi*np.arange(g)[:,None]*np.arange(m)[None,:]/N)
    delta=(rng.normal(size=(g,m))+1j*rng.normal(size=(g,m)))*1e-4
    distorted=twiddle+delta
    fg=fourier(g);fm=fourier(m)
    rows=[]
    for t in range(M):
        local=np.column_stack([fg@local_projector(g,M,2*s+1,(s+t*(g//M))%g)@x[s::m] for s in range(m)])
        rows.append(((local*distorted)@fm.T).T.reshape(N))
    aggregate=sum(rows)/M
    composed=(((fg@x.reshape(g,m))*distorted)@fm.T).T.reshape(N)
    assert np.max(abs(aggregate-composed))<1e-12
    actual=np.linalg.norm(aggregate-F@x)
    bound=float(np.max(abs(delta))*np.linalg.norm(x))
    assert actual<=bound+1e-12
    return dict(N=N,G=g,m=m,M=M,normalized_stack_gram_error=residual,
                common_twiddle_error_norm=float(actual),common_twiddle_error_bound=bound)


def main():
    result={'scope':'Independent mathematics and independently authored execution checks; no checkpoint program imported or executed.',
            'finite_field':[exact_case(*case) for case in [(24,97,2),(40,641,2),(48,97,4),(80,641,4),(96,97,4),(160,641,4),(64,257,8),(12,97,1),(7,29,1),(1,3,1)]],
            'covariance':dyadic_covariance(),
            'constructive_shared_randomness':[pairwise_extension(8,3,2,3,0b1011),pairwise_extension(16,5,4,4,0b10011)],
            'conditioning':[conditioning_control(8,3,2),conditioning_control(16,3,4),conditioning_control(16,5,4)]}
    result['checker_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    out=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('CHECK_RESULTS.json')
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
