"""Independent exact checks of serial scan bounds and a two-scan FFT stage.
No uploaded modules are imported. No faster-FFT claim is made.
"""
import json,random
from pathlib import Path
P=998244353

def scan(x,a,b,forward=True):
    y=[0]*len(x);state=0
    for i in (range(len(x)) if forward else range(len(x)-1,-1,-1)):
        state=(a[i]*state+b[i]*x[i])%P;y[i]=state
    return y

def inverse_scan(y,a,b,forward=True):
    n=len(y);out=[]
    for i in range(n):
        j=i-1 if forward else i+1
        prior=y[j] if 0<=j<n else 0
        out.append((y[i]-a[i]*prior)*pow(b[i],-1,P)%P)
    return out

def apply(x,f,inverse=False):
    kind,data=f
    if kind=='scan':
        a,b,d=data;return (inverse_scan if inverse else scan)(x,a,b,d)
    if kind=='diag':return [v*(pow(c,-1,P) if inverse else c)%P for v,c in zip(x,data)]
    if inverse:
        out=[0]*len(x)
        for i,j in enumerate(data):out[j]=x[i]
        return out
    return [x[j] for j in data]

def word(x,fs,inverse=False):
    for f in (reversed(fs) if inverse else fs):x=apply(x,f,inverse)
    return x

def direct(x,inverse=False):
    n=len(x);root=pow(3,(P-1)//n,P)
    if inverse:root=pow(root,-1,P)
    out=[sum(v*pow(root,i*j,P) for j,v in enumerate(x))%P for i in range(n)]
    return [v*pow(n,-1,P)%P for v in out] if inverse else out

def scan_fft(x):
    n=len(x);levels=(n-1).bit_length()
    assert n==1<<levels
    if n==1:return x[:],0
    root=pow(3,(P-1)//n,P)
    rev=[int(format(i,'0%db'%levels)[::-1],2) for i in range(n)]
    out=[x[j]%P for j in rev];passes=0
    for level in range(1,levels+1):
        m=1<<level;wm=pow(root,n//m,P);ws=[1]
        for j in range(1,m//2):ws.append(ws[-1]*wm%P)
        layout=[];tw=[]
        for base in range(0,n,m):
            for j in range(m//2):layout.extend([base+j,base+j+m//2]);tw.append(ws[j])
        y=[out[j] for j in layout]
        a=[(-pow(2,-1,P) if i%2==0 else 0) for i in range(n)]
        b=[(1 if i%2==0 else -2*tw[i//2]%P) for i in range(n)]
        y=scan(y,a,b,False)
        y=scan(y,[i%2 for i in range(n)],[1]*n,True);passes+=2
        for i,j in enumerate(layout):out[j]=y[i]
    return out,passes

def main():
    rng=random.Random(202610091012);counts=dict(random_words=0,inverse_identity_vectors=0,fft_basis_vectors=0,fft_random_vectors=0,dense_fourier_inverse_matrices=0)
    for n in [1,2,3,4,5,8,16]:
        for t in range(1,7):
            for trial in range(20):
                fs=[]
                for _ in range(t):
                    pi=list(range(n));rng.shuffle(pi)
                    fs.extend([('perm',pi),('diag',[rng.randrange(1,P) for _ in range(n)]),('scan',([rng.choice([0,rng.randrange(P)]) for _ in range(n)],[rng.randrange(1,P) for _ in range(n)],bool(rng.randrange(2))))])
                pi=list(range(n));rng.shuffle(pi);fs.append(('perm',pi))
                cols=[]
                for j in range(n):
                    e=[int(i==j) for i in range(n)]
                    inv=word(e,fs,True)
                    assert word(inv,fs)==e
                    cols.append(inv);counts['inverse_identity_vectors']+=1
                support=[sum(cols[j][i]!=0 for j in range(n)) for i in range(n)]
                assert max(support)<=min(n,1<<t)
                assert min(support)<=min(n,1<<(t-1))
                counts['random_words']+=1
    for n in [1,2,4,8,16,32,64,128,256]:
        if n<=32:
            for j in range(n):
                x=[int(i==j) for i in range(n)];got,t=scan_fft(x)
                assert got==direct(x);assert t==2*(n.bit_length()-1)
                counts['fft_basis_vectors']+=1
        for _ in range(12):
            x=[rng.randrange(P) for _ in range(n)];got,t=scan_fft(x)
            assert got==direct(x);assert t==2*(n.bit_length()-1)
            counts['fft_random_vectors']+=1
        if n>1:
            assert all(v!=0 for j in range(n) for v in direct([int(i==j) for i in range(n)],True))
            counts['dense_fourier_inverse_matrices']+=1
    result=dict(status='passed',field_prime=P,counts=counts,
                scope='Exact correctness and finite support checks. The all-size lower bound is proved separately; this FFT is a classical O(N log N) construction expressed as scans.')
    Path(__file__).with_name('inverse_scan_checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
