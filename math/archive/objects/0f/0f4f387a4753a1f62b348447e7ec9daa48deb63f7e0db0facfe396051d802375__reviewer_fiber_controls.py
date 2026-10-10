"""Independent F015 recognition, synthesis, aggregate and Green-domain controls."""
import json,random,math
from pathlib import Path

def dft(v,w,p):return [sum(x*pow(w,j*k,p) for j,x in enumerate(v))%p for k in range(len(v))]
def bm(seq,p):
    C=[1];B=[1];L=0;since=1;old=1
    for n,x in enumerate(seq):
        z=(x+sum(C[j]*seq[n-j] for j in range(1,L+1)))%p
        if z==0:since+=1;continue
        prior=C[:];scale=z*pow(old,-1,p)%p
        if len(C)<len(B)+since:C.extend([0]*(len(B)+since-len(C)))
        for j,y in enumerate(B):C[j+since]=(C[j+since]-scale*y)%p
        if 2*L<=n:L=n+1-L;B=prior;old=z;since=1
        else:since+=1
    C.extend([0]*max(0,L+1-len(C)))
    return C[:L+1],L
def value(C,x,p):
    z=0
    for c in reversed(C):z=(z*x+c)%p
    return z
def recognize(y,eta,b,p):
    C,r=bm(y[:2*b],p)
    if r>b:return None
    if r==0:return {} if not any(y) else None
    hs=[h for h in range(len(y)) if value(C,pow(eta,h,p),p)==0]
    if len(hs)!=r:return None
    A=[sum(C[j]*y[i-j] for j in range(i+1))%p for i in range(r)]
    deriv=[j*C[j]%p for j in range(1,r+1)];modes={}
    for h in hs:
        z=pow(eta,h,p);den=value(deriv,z,p)
        if not den:return None
        a=-pow(z,-1,p)*value(A,z,p)*pow(den,-1,p)%p
        if not a:return None
        modes[h]=a
    rec=[sum(a*pow(eta,(-h*u)%len(y),p) for h,a in modes.items())%p for u in range(len(y))]
    return modes if rec==y else None
def synthesize(modes,n,Q,M,w,p):
    theta=pow(w,M,p);out=[0]*n
    for h in range(M):
        z=[modes[t].get(h,0)*pow(w,h*t,p)%p for t in range(Q)]
        vals=dft(z,theta,p)
        for v in range(Q):out[h+M*v]=M*vals[v]%p
    return out
def rank(A,p):
    a=[r[:] for r in A];r=0
    for c in range(len(a[0])):
        h=next((i for i in range(r,len(a)) if a[i][c]),None)
        if h is None:continue
        a[r],a[h]=a[h],a[r];iv=pow(a[r][c],-1,p)
        for i in range(r+1,len(a)):
            f=a[i][c]*iv%p
            for j in range(c,len(a[0])):a[i][j]=(a[i][j]-f*a[r][j])%p
        r+=1
        if r==len(a):break
    return r
def main():
    p=257;rng=random.Random(934843);cap=aggregate=outputs=heavy=0
    for n in [4,8,16,32,64,128]:
        w=pow(3,256//n,p);assert pow(w,n,p)==1 and pow(w,n//2,p)!=1
        Q=2**((n.bit_length()-1)//2);M=n//Q;eta=pow(w,Q,p)
        for b in sorted(set([1,2 if M>=4 else 1,M//2])):
          for case in range(10):
            modes=[]
            for t in range(Q):
                r=rng.randrange(M+1) if case>=6 else rng.randrange(b+1)
                modes.append({h:rng.randrange(1,p) for h in rng.sample(range(M),r)})
            x=[0]*n
            for t in range(Q):
                for u in range(M):x[t+Q*u]=sum(a*pow(eta,(-h*u)%M,p) for h,a in modes[t].items())%p
            if case==5:x[-1]=(x[-1]+1)%p
            ys=[x[t::Q] for t in range(Q)]
            true=[]
            for y in ys:true.append({h:z*pow(M,-1,p)%p for h,z in enumerate(dft(y,eta,p)) if z})
            got=[recognize(y,eta,b,p) for y in ys];ok=all(z is not None for z in got)
            assert ok==all(len(z)<=b for z in true);cap+=1
            if ok:
                assert got==true and synthesize(got,n,Q,M,w,p)==dft(x,w,p);outputs+=n
            for budget in sorted(set([0,Q,n//4,n])):
                ell=M.bit_length()-1;a=max(1,(budget+Q-1)//Q);B=min(M//2,a*ell)
                found=[];K=0;heavy_now=0;accepted=True
                for y,tr in zip(ys,true):
                    z=recognize(y,eta,B,p)
                    if z is None:
                        assert len(tr)>B;z=tr;heavy_now+=1
                    found.append(z);K+=len(z)
                    if K>budget:accepted=False;break
                assert accepted==(sum(map(len,true))<=budget)
                assert heavy_now<=budget//(B+1)+(not accepted)
                if accepted:assert synthesize(found,n,Q,M,w,p)==dft(x,w,p);outputs+=n
                aggregate+=1;heavy+=heavy_now
    # Invertible but locally inadmissible Green scan, checked independently.
    p=17;n=16;w=3;L=[[0]*n for _ in range(n)]
    for j in range(n):L[j][j]=(7+pow(w,j,p))%p;L[j][(j-1)%n]=(L[j][(j-1)%n]+2)%p
    zero=[j for j in range(n) if not L[j][j]];assert zero==[3] and rank(L,p)==16
    F=[[pow(w,i*j,p) for j in range(n)] for i in range(n)]
    P=[[0]*n for _ in range(n)]
    for j in range(n):P[j][j]=(7+2*pow(w,(-j)%n,p))%p;P[j][(j-1)%n]=(P[j][(j-1)%n]+1)%p
    mm=lambda A,B:[[sum(x*y for x,y in zip(row,col))%p for col in zip(*B)] for row in A]
    assert mm(F,P)==mm(L,F)
    out={'cap_cases':cap,'aggregate_cases':aggregate,'heavy_fallbacks':heavy,'explicit_outputs_checked':outputs,'Green_counterexample':{'p':p,'N':n,'root':w,'zero_diagonal':zero,'rank':16,'covariance_verified':True},'note':'Direct polynomial evaluation and DFT references are controls; the asymptotic pruned algorithm is proved in the audit.'}
    Path(__file__).with_name('reviewer_fiber_results.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
if __name__=='__main__':main()
