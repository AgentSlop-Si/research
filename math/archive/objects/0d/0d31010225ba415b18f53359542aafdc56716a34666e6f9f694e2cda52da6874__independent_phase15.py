"""Independent audit derived from mathematical definitions, not uploaded code.
Only this script, standard-library modules, and NumPy are executed.
"""
from pathlib import Path
import cmath, hashlib, json, math, random
import numpy as np

P = 998244353
PRIMITIVE = 3

def fft(a, inverse=False):
    n=len(a); out=list(a); j=0
    for i in range(1,n):
        bit=n>>1
        while j&bit: j^=bit; bit>>=1
        j^=bit
        if i<j: out[i],out[j]=out[j],out[i]
    size=2
    while size<=n:
        w=pow(PRIMITIVE,(P-1)//size,P)
        if inverse:w=pow(w,-1,P)
        for start in range(0,n,size):
            phase=1
            for k in range(size//2):
                u=out[start+k];v=out[start+k+size//2]*phase%P
                out[start+k]=(u+v)%P;out[start+k+size//2]=(u-v)%P
                phase=phase*w%P
        size*=2
    if inverse:out=[v*pow(n,-1,P)%P for v in out]
    return out

def cycles(n,b):
    seen=set(); result=[]
    for k in range(n):
        if k in seen:continue
        cyc=[];j=k
        while j not in seen:
            seen.add(j);cyc.append(j);j=j*(1+b)%n
        assert j==k
        result.append(cyc)
    return result

def geometry(n,b):
    l=n//b;records=[]
    for cyc in cycles(n,b):
        d=len(cyc);g=l//d;k=cyc[0]
        assert k%g==0
        u=k//g;assert 0<=u<b
        if d>1:assert u%2
        for e in range(d):
            a=(pow(u,-1,d)*e)%d if d>1 else 0
            c=(u*a-e)//d
            records.append((cyc,e,d,g,u,a,c))
    assert len(records)==n
    return records

def fold_spectra(top,n,b):
    l=n//b;levels={l:[list(v) for v in top]};d=l
    wb=pow(PRIMITIVE,(P-1)//b,P);count=0
    while d>1:
        prev=levels[d];now=[[0]*b for _ in range(d//2)]
        for a in range(d//2):
            for q in range(b//2):
                u=prev[a][2*q];v=pow(wb,q,P)*prev[a+d//2][2*q]%P
                now[a][q]=(u+v)%P;now[a][q+b//2]=(u-v)%P;count+=1
        levels[d//2]=now;d//=2
    assert count==(n-b)//2
    return levels

def extract(levels,n,b):
    wb=pow(PRIMITIVE,(P-1)//b,P)
    return [pow(wb,c%(b),P)*levels[d][a][u]%P for cyc,e,d,g,u,a,c in geometry(n,b)]

def unfold(values,n,b):
    l=n//b;wb=pow(PRIMITIVE,(P-1)//b,P)
    levels={d:[[None]*b for _ in range(d)] for d in [1<<t for t in range(l.bit_length())]}
    for val,(cyc,e,d,g,u,a,c) in zip(values,geometry(n,b)):
        assert levels[d][a][u] is None
        levels[d][a][u]=val*pow(wb,(-c)%b,P)%P
    d=2;inv2=pow(2,-1,P);count=0
    while d<=l:
        low=levels[d//2];high=levels[d]
        for a in range(d//2):
            for q in range(b//2):
                u=low[a][q];v=low[a][q+b//2]
                assert u is not None and v is not None
                high[a][2*q]=(u+v)*inv2%P
                high[a+d//2][2*q]=(u-v)*inv2*pow(wb,-q,P)%P;count+=1
        d*=2
    assert count==(n-b)//2 and all(v is not None for row in levels[l] for v in row)
    return levels[l]

def direct_residual(x,n,b):
    l=n//b;wb=pow(PRIMITIVE,(P-1)//b,P);ans=[]
    for cyc,e,d,g,u,a,c in geometry(n,b):
        k=cyc[0];r=g*e
        ans.append(sum(x[j]*pow(wb,((k*j-r)//l)%b,P) for j in range(n) if (k*j-r)%l==0)%P)
    return ans

def full_output(ax,n,b):
    wn=pow(PRIMITIVE,(P-1)//n,P);out=[None]*n;index=0
    for cyc in cycles(n,b):
        d=len(cyc);g=(n//b)//d
        row=[ax[index+e]*pow(wn,g*e,P)%P for e in range(d)]
        index+=d
        for k,v in zip(cyc,fft(row)):out[k]=v
    assert all(v is not None for v in out)
    return out

def numerical_r(n,b):
    l=n//b;wb=cmath.exp(2j*math.pi/b)
    levels={l:np.eye(n,dtype=complex).reshape((l,b,n))};d=l
    while d>1:
        old=levels[d];new=np.zeros((d//2,b,n),dtype=complex)
        for a in range(d//2):
            for q in range(b//2):
                v=wb**q*old[a+d//2,2*q]
                new[a,q]=old[a,2*q]+v;new[a,q+b//2]=old[a,2*q]-v
        levels[d//2]=new;d//=2
    records=geometry(n,b)
    r=np.array([wb**c*levels[d][a,u] for cyc,e,d,g,u,a,c in records])
    g=np.array([v[3] for v in records])
    rhat=r/np.sqrt(g[:,None]);gram=rhat@rhat.conj().T
    assert np.max(np.abs(gram-np.eye(n)))<2e-12
    support=np.count_nonzero(np.abs(r)>1e-9,axis=1)
    assert np.array_equal(support,g)
    h=l.bit_length()-1
    assert int(support.sum())==n+n*h//2
    probs=abs(rhat)**2
    entropy=-sum(float(p)*math.log2(float(p)) for p in probs.flat if p>1e-15)
    assert abs(entropy-(n-b))<1e-9
    return {'N':n,'B':b,'gram_error':float(np.max(abs(gram-np.eye(n)))),'nnz_R':int(support.sum()),'entropy_R':entropy,'predicted_entropy_R':n-b}

def main():
    rng=random.Random(1450);rows=[]
    for n,b in [(16,8),(32,8),(64,8),(128,16),(256,16),(256,128),(512,32),(1024,32),(2048,64),(4096,64)]:
        l=n//b
        x=[rng.randrange(P) for _ in range(n)]
        top=[fft(x[a::l]) for a in range(l)]
        levels=fold_spectra(top,n,b);ax=extract(levels,n,b)
        assert unfold(ax,n,b)==top
        restored=[0]*n
        for a,row in enumerate(unfold(ax,n,b)):
            restored[a::l]=fft(row,inverse=True)
        assert restored==x
        assert full_output(ax,n,b)==fft(x)
        if n<=1024:assert ax==direct_residual(x,n,b)
        hist={}
        for cyc in cycles(n,b):hist[len(cyc)]=hist.get(len(cyc),0)+1
        expected={1:b,**{1<<t:b//2 for t in range(1,l.bit_length())}}
        assert hist==expected
        base=n*(b.bit_length()-1)//2;fold=(n-b)//2
        orbit=sum(len(cyc)*(len(cyc).bit_length()-1)//2 for cyc in cycles(n,b))
        assert base+fold+orbit==n*(n.bit_length()-1)//2
        # Entropies of all three normalized factors, in bits.
        ebase=n*math.log2(b);efold=n-b;eorbit=n*(math.log2(l)-1)+b
        assert ebase+efold+eorbit==n*math.log2(n)
        assert (ebase,efold,eorbit)==(2*base,2*fold,2*orbit)
        rows.append({'N':n,'B':b,'L':l,'full_modular_equality':True,'direct_residual_checked':n<=1024,'inverse_round_trip':True,'butterflies':{'base':base,'fold':fold,'orbit':orbit,'total':base+fold+orbit},'entropy_bits':{'base':ebase,'fold':efold,'orbit':eorbit}})
    result={'scope':'Independent script; no uploaded code executed. Symbolic proofs separately audited.','modulus':P,'modular_cases':rows,'complex_cases':[numerical_r(n,b) for n,b in [(16,8),(32,8),(64,8),(128,16),(256,16)]],'all_passed':True}
    here=Path(__file__).parent
    (here/'independent_phase15_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
