"""Independently authored v7 audit. Does not import or execute supplied source.
Uses direct global chirp matrices for exhaustive probabilistic checks,
and an independently written modular-arithmetic recurrence test.
"""
import itertools, json, math
from pathlib import Path
import numpy as np

OUT=Path(__file__).parent

def literal_coefficients(N,M,a,beta,outputs):
    z=np.exp(2j*np.pi/N)
    indices=np.arange(N)
    # Modulo reduction avoids giant trigonometric arguments.
    g=z**((a*indices*indices+beta*indices)%N)
    coeff=[]
    for m in outputs:
        fourier=z**((-m*indices)%N)/math.sqrt(N)
        row=np.empty(N,complex)
        for block in range(N//M):
            sl=slice(block*M,(block+1)*M)
            row[sl]=g[sl]*np.dot(fourier[sl],np.conj(g[sl]))
        coeff.append(row-fourier)
    return np.asarray(coeff)

def predicted_covariance(N,M,m):
    # Character average computed by divisibility directly from paired positions.
    Q=np.zeros((N,N),complex)
    for n in range(N):
        for p in range(N):
            total=0
            for t in range(M):
                d=n%M-t
                if d==0: continue
                tp=p%M-d
                if not 0<=tp<M: continue
                c=2*d*(p-n)
                if (2*c)%N==0:
                    total+=1 if c%N==0 else -1
            Q[n,p]=total*np.exp(2j*np.pi*m*(n-p)/N)/N
    return Q

def exhaustive(N,M,outputs):
    Q=np.zeros((len(outputs),N,N),complex)
    means=np.zeros((len(outputs),N),complex)
    states=0
    for a in range(1,N,2):
        for beta in range(N):
            H=literal_coefficients(N,M,a,beta,outputs)
            means+=H
            for j in range(len(outputs)):
                Q[j]+=np.outer(H[j].conj(),H[j])
            states+=1
    Q/=states; means/=states
    discrepancies=[]; idempotencies=[]; ranks=[]; norms=[]
    for j,m in enumerate(outputs):
        prediction=predicted_covariance(N,M,m)
        discrepancies.append(float(np.max(np.abs(Q[j]-prediction))))
        norms.append(float(np.linalg.eigvalsh(Q[j])[-1]))
        if M>=2 and N//M>=2*M:
            alpha=2*M/N
            idempotencies.append(float(np.max(np.abs(Q[j]@Q[j]-alpha*Q[j]))))
            ranks.append(int(np.sum(np.linalg.eigvalsh(Q[j])>1e-9)))
            assert abs(norms[-1]-alpha)<1e-10
            assert ranks[-1]==(N//M)*(M-1)//2
    assert max(discrepancies)<1e-10
    assert np.max(np.abs(means))<1e-10
    return dict(N=N,M=M,outputs=outputs,states=states,max_covariance_error=max(discrepancies),
        max_mean_error=float(np.max(np.abs(means))),norms=norms,
        scalar_projector_defect=max(idempotencies,default=None),ranks=ranks)

P=998244353

def exact_modular_decoder(N,M,a,beta):
    # Work with unnormalized DFT so no square root is needed in the field.
    root=pow(3,(P-1)//N,P)
    powers=[pow(root,j,P) for j in range(N)]
    K=N//M
    x=[(j*j+17*j+31)%P for j in range(N)]
    g=[powers[(a*j*j+beta*j)%N] for j in range(N)]
    # Form global-gauge summaries and reconstruct the projection literally.
    y=[]
    for r in range(K):
        d=sum(g[r*M+t]*x[r*M+t] for t in range(M))%P
        y.extend(d*pow(g[r*M+t],P-2,P)%P for t in range(M))
    direct=[sum(y[j]*powers[(-m*j)%N] for j in range(N))%P for m in range(N)]
    # Separate local-gauge summaries for the derived recurrence.
    d=[sum(x[r*M+t]*powers[(a*t*t+(2*a*M*r+beta)*t)%N] for t in range(M))%P for r in range(K)]
    D=[sum(d[r]*powers[(-s*r*M)%N] for r in range(K))%P for s in range(K)]
    got=[None]*N
    for seed in [0,1]:
        # Seed directly from compressed summaries, without using direct[] values.
        got[seed]=sum(d[r]*powers[(-seed*r*M)%N]*sum(powers[(-a*t*t-(seed+2*a*M*r+beta)*t)%N] for t in range(M)) for r in range(K))%P
        m=seed
        for _ in range(N//2-1):
            nxt=(m+2*a)%N
            leading=powers[(-a-m-beta)%N]
            boundary=powers[(-a*M*M-m*M-beta*M)%N]
            forcing=(D[m%K]-boundary*D[(m+2*a*M)%K])%P
            got[nxt]=(got[m]-forcing)*pow(leading,P-2,P)%P
            m=nxt
    assert got==direct
    return dict(N=N,M=M,a=a,beta=beta,exact_match=True)

def spectral_checks():
    rows=[]
    for N,M in [(8,2),(16,2),(32,4),(64,4),(128,8),(256,8),(512,16)]:
        Q=predicted_covariance(N,M,0)
        alpha=2*M/N
        # Stronger exact count: independent enumeration of displacement sets.
        for u in range(M):
            ds=[u-t for t in range(M) if t!=u]
            for v in range(M.bit_length()-1):
                c=sum(abs(d)&-abs(d)==2**v for d in ds)
                assert c==M//(2**(v+1))
        vals=np.linalg.eigvalsh(Q)
        err=float(np.max(np.minimum(np.abs(vals),np.abs(vals-alpha))))
        assert err<1e-10
        x=np.array([complex(j%7-3,j%5-2) for j in range(N)])
        A=np.fft.fft(x.reshape(N//M,M),axis=0)/math.sqrt(N//M)
        selected=np.array([ell for ell in range(N//M) if ell%2==0 and ell%(2*M)!=0])
        energy_errors=[]
        for output in [0,1,3]:
            rayleigh=float(np.vdot(x,predicted_covariance(N,M,output)@x).real)
            spectral=alpha*float(np.sum(np.abs(A[(selected+output)%(N//M),:])**2))
            energy_errors.append(abs(rayleigh-spectral))
        assert max(energy_errors)<1e-10
        rows.append(dict(N=N,M=M,norm=float(vals[-1]),rank=int(np.sum(vals>1e-9)),expected_rank=(N//M)*(M-1)//2,spectral_two_level_error=err,max_spectral_energy_identity_error=max(energy_errors)))
    return rows

def median_enumeration():
    # Exact-integer pointwise product-subset inequality: no source theorem needed.
    rows=[]
    for R in [1,3,5,7]:
        s=(R+1)//2
        count=0
        for xs in itertools.product([-2,-1,0,1,3],repeat=R):
            lhs=abs(sorted(xs)[s-1])**(2*s)
            rhs=sum(math.prod(xs[j]**2 for j in subset) for subset in itertools.combinations(range(R),s))
            assert lhs<=rhs
            count+=1
        rows.append(dict(rows=R,pointwise_cases=count,all_pass=True))
    return rows

if __name__=='__main__':
    result={
      'provenance':'Independent code authored for this audit; no uploaded code imported or executed.',
      'exhaustive_covariances':[exhaustive(8,2,list(range(8))),exhaustive(16,2,[0,3,9]),exhaustive(32,4,[0,3,17]),exhaustive(16,1,[0,3])],
      'exact_finite_field_decoders':[exact_modular_decoder(N,M,a,b) for N,M in [(8,2),(32,4),(64,8),(128,8),(512,16)] for a,b in [(1,0),(3,7),(N-1,N-3)]],
      'spectrum_checks':spectral_checks(),
      'median_checks':median_enumeration(),
    }
    (OUT/'independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
