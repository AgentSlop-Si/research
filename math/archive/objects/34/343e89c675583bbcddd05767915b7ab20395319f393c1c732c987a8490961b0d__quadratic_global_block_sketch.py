import numpy as np, math

TAU=2*np.pi

def project_blocks_global_chirp(x,K,a,beta):
    x=np.asarray(x,dtype=np.complex128); N=x.size; assert N%K==0
    M=N//K
    n=np.arange(N,dtype=np.int64)
    # use float phase reduced mod N to avoid huge ints
    phase=((a*(n.astype(object)*n.astype(object)) + beta*n.astype(object)) % N)
    sig=np.exp(2j*np.pi*np.array(phase,dtype=np.float64)/N)
    blocks=x.reshape(K,M); S=sig.reshape(K,M)
    d=np.sum(S*blocks,axis=1)
    y=(np.conjugate(S)*d[:,None]).reshape(N)
    return d,y,S

def decode_reference(d,S):
    K,M=S.shape; N=K*M
    y=(np.conjugate(S)*np.asarray(d)[:,None]).reshape(N)
    return np.fft.fft(y)/math.sqrt(N)

def decode_recurrence(d,N,K,a,beta):
    M=N//K
    d=np.asarray(d,dtype=np.complex128)
    D=np.fft.fft(d)  # D_s=sum_r d_r exp(-2pi i s r/K)
    # P recurrence with local phase sigma_{r,t}=exp(+2pi i/N [a t^2 + c_r t]) up to block scalar.
    # Since d generated with global chirp contains block scalar, need account for that in d before local formula.
    # global sig = exp(+2pi i/N [a(rM+t)^2 + beta(rM+t)])
    # = q_r * exp(+2pi i/N[a t^2 + (2aMr+beta)t])
    # q_r=exp(+2pi i/N[a r^2M^2+beta rM])
    r=np.arange(K,dtype=np.int64)
    qr=np.exp(2j*np.pi*((a*(r.astype(object)*r.astype(object))*M*M + beta*r.astype(object)*M)%N).astype(float)/N)
    # local summary dloc = sum local_sigma*x = d_global / q_r
    dloc=d/qr
    D=np.fft.fft(dloc)

    step=(2*a)%N
    g=math.gcd(step,N)
    Y=np.empty(N,dtype=np.complex128)
    omega=lambda z: np.exp(-2j*np.pi*(z%N)/N)
    # direct seeds for residues 0..g-1 using local formula
    rr=np.arange(K)
    tt=np.arange(M)
    for seed in range(g):
        vals=[]
        for r0 in range(K):
            c=(2*a*M*r0+beta)%N
            P=np.sum(np.exp(-2j*np.pi*((a*(tt.astype(object)*tt.astype(object)) + (seed+c)*tt.astype(object))%N).astype(float)/N))
            vals.append(dloc[r0]*np.exp(-2j*np.pi*seed*r0/K)*P)
        Y[seed]=np.sum(vals)/math.sqrt(N)

    # Recurrence: Y_m = D[m%K]/sqrtN + A_m e^{-2pi i beta/N} Y_{m+step}
    #              - B_m e^{-2pi i beta/K} D[(m+2aM)%K]/sqrtN
    # So solve forward along m -> m+step: Y_next = (Y_m - forcing_m)/(A_m e^{-2pi i beta/N})
    sqN=math.sqrt(N)
    cA=np.exp(-2j*np.pi*beta/N)
    cB=np.exp(-2j*np.pi*beta/K)
    for seed in range(g):
        m=seed
        while True:
            nxt=(m+step)%N
            if nxt==seed: break
            A=np.exp(-2j*np.pi*(a+m)/N)
            B=np.exp(-2j*np.pi*((a*M*M + m*M)%N)/N)
            forcing=D[m%K]/sqN - B*cB*D[(m+2*a*M)%K]/sqN
            Y[nxt]=(Y[m]-forcing)/(A*cA)
            m=nxt
    return Y

if __name__=='__main__':
    rng=np.random.default_rng(0)
    for N,K in [(256,16),(1024,32),(4096,64)]:
      for rep in range(5):
        a=int(2*rng.integers(0,N//2)+1); beta=int(rng.integers(0,N))
        x=rng.normal(size=N)+1j*rng.normal(size=N)
        d,y,S=project_blocks_global_chirp(x,K,a,beta)
        ref=np.fft.fft(y)/math.sqrt(N)
        got=decode_recurrence(d,N,K,a,beta)
        print(N,K,a,beta,np.max(np.abs(ref-got)))
