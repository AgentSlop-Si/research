import numpy as np, math, sys
sys.path.insert(0,'/mnt/data')


def unitfft(x): return np.fft.fft(x)/math.sqrt(len(x))

def make_phase(N,a,beta):
    n=np.arange(N,dtype=np.int64)
    # N power of two; safe for our test sizes
    return np.exp(2j*np.pi*(((np.int64(a)*n*n+np.int64(beta)*n)&np.int64(N-1)).astype(float))/N)

def project(x,M,a,beta):
    N=len(x); K=N//M
    sig=make_phase(N,a,beta).reshape(K,M)
    d=np.sum(sig*x.reshape(K,M),axis=1)
    return d

def decode_from_Dnorm(d,Dnorm,N,M,a,beta):
    # Adapt exact recurrence using supplied approximation to normalized K-DFT(d)
    K=N//M; D=np.asarray(Dnorm)*math.sqrt(K)
    r=np.arange(K,dtype=np.int64)
    # global chirp has block scalar q_r; local summaries dloc=d/q_r
    qr=np.exp(2j*np.pi*(((np.int64(a)*r*r*np.int64(M*M)+np.int64(beta)*r*np.int64(M))&np.int64(N-1)).astype(float))/N)
    dloc=d/qr
    # Dnorm passed is DFT of global d, not dloc! Need recursively transform dloc, not d.
    raise RuntimeError('use dloc recursively')

def project_local_summary(x,M,a,beta):
    # Return dloc for local-phase convention and block scalar qr, such that global d=qr*dloc.
    N=len(x);K=N//M
    r=np.arange(K,dtype=np.int64);t=np.arange(M,dtype=np.int64)
    c=(2*np.int64(a)*np.int64(M)*r+np.int64(beta)) & np.int64(N-1)
    # local sigma exp(2pi i/N(a t^2+c_r t))
    ph=(np.int64(a)*t[None,:]*t[None,:] + c[:,None]*t[None,:]) & np.int64(N-1)
    Sloc=np.exp(2j*np.pi*ph.astype(float)/N)
    dloc=np.sum(Sloc*x.reshape(K,M),axis=1)
    return dloc

def decode_local_from_Dnorm(dloc,Dnorm,N,M,a,beta):
    K=N//M; D=np.asarray(Dnorm,dtype=complex)*math.sqrt(K)
    step=(2*a)%N; g=math.gcd(step,N); assert g==2
    Y=np.empty(N,complex); sqN=math.sqrt(N)
    tt=np.arange(M,dtype=np.int64)
    # two direct seeds, vectorize over blocks; P seed per block x M
    rr=np.arange(K,dtype=np.int64)
    c=(2*np.int64(a)*np.int64(M)*rr+np.int64(beta)) & np.int64(N-1)
    for seed in range(g):
        ph=(np.int64(a)*tt[None,:]*tt[None,:] + ((np.int64(seed)+c[:,None])&np.int64(N-1))*tt[None,:]) & np.int64(N-1)
        P=np.sum(np.exp(-2j*np.pi*ph.astype(float)/N),axis=1)
        w=np.exp(-2j*np.pi*seed*rr/K)
        Y[seed]=np.sum(dloc*w*P)/sqN
    cA=np.exp(-2j*np.pi*beta/N); cB=np.exp(-2j*np.pi*beta/K)
    for seed in range(g):
        m=seed
        while True:
            nxt=(m+step)%N
            if nxt==seed: break
            A=np.exp(-2j*np.pi*(a+m)/N)
            B=np.exp(-2j*np.pi*((a*M*M+m*M)%N)/N)
            forcing=D[m%K]/sqN - B*cB*D[(m+2*a*M)%K]/sqN
            Y[nxt]=(Y[m]-forcing)/(A*cA)
            m=nxt
    return Y

def recursive_est(x,M,rng,base=16):
    x=np.asarray(x,complex);N=len(x)
    if N<=base or N%M: return unitfft(x)
    a=int(2*rng.integers(0,N//2)+1); beta=int(rng.integers(0,N))
    dloc=project_local_summary(x,M,a,beta)
    Dnorm=recursive_est(dloc,M,rng,base)
    return decode_local_from_Dnorm(dloc,Dnorm,N,M,a,beta)

def avg_est(x,M,L,rng,base=16):
    out=np.zeros(len(x),complex)
    for _ in range(L): out+=recursive_est(x,M,rng,base)
    return out/L

def cases(N,rng):
    n=np.arange(N,dtype=float)
    out={'flat':np.ones(N,complex),'gaussian':rng.normal(size=N)+1j*rng.normal(size=N),
         'random_phase':np.exp(2j*np.pi*rng.random(N)),
         'global_chirp':np.exp(2j*np.pi*(5*n*n+7*n)/N)}
    for s in [1,4,16,64]:
      if s<=N:
       z=np.zeros(N,complex);idx=rng.choice(N,s,replace=False);z[idx]=np.exp(2j*np.pi*rng.random(s));out[f'sparse{s}']=z
    return out

if __name__=='__main__':
 rng=np.random.default_rng(7)
 for N in [256,1024,4096]:
  print('N',N)
  for name,x in cases(N,rng).items():
   X=unitfft(x); norm=np.linalg.norm(x); scale=np.sum(np.abs(x))/math.sqrt(N)
   row=[]
   for L in [1,2,4,8,16]:
    es=[]; es1=[]
    for _ in range(8):
      Y=avg_est(x,4,L,rng,base=16)
      e=np.max(np.abs(Y-X));es.append(e/norm if norm else 0);es1.append(e/scale if scale else 0)
    row.append((L,float(np.median(es)),float(np.median(es1))))
   print(name,row)
