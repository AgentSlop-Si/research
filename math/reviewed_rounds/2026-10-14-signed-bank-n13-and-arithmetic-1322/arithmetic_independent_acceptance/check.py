#!/usr/bin/env python3
"""Fresh independent finite-field matrix and convolution audit; no imported research programs."""
import json, hashlib, time
from pathlib import Path
from functools import lru_cache
HERE=Path(__file__).resolve().parent
SOURCE=HERE/'dependencies/RAW_CERTIFICATE.json'

class K:
    def __init__(self,p,mod=None):
        self.p=p; self.mod=mod; self.d=len(mod)-1 if mod else 1; self.order=p**self.d
    def digits(self,a):
        out=[]
        for _ in range(self.d):out.append(a%self.p);a//=self.p
        return out
    def pack(self,a):return a%self.p if isinstance(a,int) else sum((c%self.p)*self.p**i for i,c in enumerate(a))
    def add(self,a,b):
        if self.d==1:return (a+b)%self.p
        return self.pack([x+y for x,y in zip(self.digits(a),self.digits(b))])
    def neg(self,a):
        if self.d==1:return -a%self.p
        return self.pack([-x for x in self.digits(a)])
    def sub(self,a,b):return self.add(a,self.neg(b))
    @lru_cache(None)
    def mul(self,a,b):
        if self.d==1:return a*b%self.p
        v=[0]*(2*self.d-1)
        for i,x in enumerate(self.digits(a)):
            for j,y in enumerate(self.digits(b)):v[i+j]+=x*y
        for i in range(len(v)-1,self.d-1,-1):
            z=v[i]%self.p
            for j in range(self.d):v[i-self.d+j]-=z*self.mod[j]
        return self.pack(v[:self.d])
    def power(self,a,n):
        if n<0:return self.power(self.inv(a),-n)
        out=1
        while n:
            if n%2:out=self.mul(out,a)
            a=self.mul(a,a);n//=2
        return out
    @lru_cache(None)
    def inv(self,a):
        assert a
        r=self.power(a,self.order-2);assert self.mul(a,r)==1
        return r
    def div(self,a,b):return self.mul(a,self.inv(b))
    def total(self,a):
        s=0
        for x in a:s=self.add(s,x)
        return s

def ident(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def matmul(k,A,B):return [[k.total(k.mul(u,v) for u,v in zip(r,c)) for c in zip(*B)] for r in A]
def matrix_inverse(k,A):
    n=len(A);m=[r.copy()+e for r,e in zip(A,ident(n))]
    for c in range(n):
        pivot=next(i for i in range(c,n) if m[i][c]);m[c],m[pivot]=m[pivot],m[c]
        z=k.inv(m[c][c]);m[c]=[k.mul(z,v) for v in m[c]]
        for i in range(n):
            if i==c:continue
            z=m[i][c]
            if z:m[i]=[k.sub(v,k.mul(z,w)) for v,w in zip(m[i],m[c])]
    assert [r[:n] for r in m]==ident(n)
    return [r[n:] for r in m]
def conv(k,a,b):
    out=[0]*(len(a)+len(b)-1)
    for i,v in enumerate(a):
        for j,w in enumerate(b):out[i+j]=k.add(out[i+j],k.mul(v,w))
    return out
def toep(k,n,kernel,x):return conv(k,kernel,x)[n-1:2*n-1]
def cyclic(k,a,b):
    n=len(a);c=conv(k,a,b);out=c[:n]
    for i in range(n,len(c)):out[i-n]=k.add(out[i-n],c[i])
    return out

def chirp(k,n,q,x,sign=-1):
    assert n%2
    h=pow(2,-1,n)
    D=[k.power(q,(sign*h*t*t)%n) for t in range(n)]
    C=[k.power(q,(-sign*h*t*t)%n) for t in range(n)]
    u=cyclic(k,C,[k.mul(d,v) for d,v in zip(D,x)])
    return [k.mul(d,v) for d,v in zip(D,u)]

def bank_factors(k,n,q,a,b,e,d,w):
    # Setup weight transform independently through ordinary polynomial multiplication.
    psi=[k.mul(k.inv(n%k.p),v) for v in chirp(k,n,q,w,e*d)]
    direct=[k.div(k.total(k.mul(w[j],k.power(q,(e*d*j*r)%n)) for j in range(n)),n%k.p) for r in range(n)]
    assert psi==direct
    ix=[(d*r)%n for r in range(n)]
    ds=[k.sub(1,k.mul(a,k.power(q,(-e*i)%n))) for i in ix]
    if not b:
        assert all(ds)
        def apply(x):
            y=[0]*n
            for r,i in enumerate(ix):y[i]=k.div(k.mul(psi[0],x[i]),ds[r])
            return y
        return apply,'diagonal',None
    zero=[r for r,v in enumerate(ds) if not v]
    assert len(zero)<=1
    if not zero:
        p=[];r=1
        for z in ds:r=k.div(k.mul(r,b),z);p.append(r)
        P=p[-1];assert P!=1
        kernel=[k.mul(P,psi[t%n]) if t<0 else psi[t] for t in range(1-n,n)]
        def apply(x):
            u=[k.div(x[i],k.mul(p[s],ds[s])) for s,i in enumerate(ix)]
            v=toep(k,n,kernel,u);out=[0]*n
            for r,i in enumerate(ix):out[i]=k.div(k.mul(p[r],v[r]),k.sub(1,P))
            return out
        return apply,'full',None
    z=zero[0];ix=ix[z:]+ix[:z];ds=ds[z:]+ds[:z]
    p=[1]
    for v in ds[1:]:p.append(k.div(k.mul(p[-1],v),b))
    kernel=[psi[(t-1)%n] if t<=0 else 0 for t in range(1-n,n)]
    def apply(x):
        u=[k.mul(p[s],x[ix[(s+1)%n]]) for s in range(n)]
        v=toep(k,n,kernel,u);out=[0]*n
        for r,i in enumerate(ix):out[i]=k.neg(k.div(v[r],k.mul(b,p[r])))
        return out
    return apply,'one_zero',z

COUNTS={};ROTATIONS={};TOTAL=0

def test_bank(k,n,q,a,b,e,d,w):
    global TOTAL
    Delta=k.sub(k.sub(1,k.power(a,n)),k.power(b,n));assert Delta
    F=[[k.power(q,(-i*j)%n) for j in range(n)] for i in range(n)]
    Fi=[[k.div(k.power(q,(i*j)%n),n%k.p) for j in range(n)] for i in range(n)]
    assert matmul(k,F,Fi)==ident(n)
    B=[[0]*n for _ in range(n)]
    for j in range(n):
        A=ident(n)
        for t in range(n):
            A[(t+e)%n][t]=k.sub(A[(t+e)%n][t],a)
            A[t][t]=k.sub(A[t][t],k.mul(b,k.power(q,(d*(t+e*j))%n)))
        R=matrix_inverse(k,A);assert matmul(k,A,R)==ident(n) and matmul(k,R,A)==ident(n)
        coef=k.div(w[j],n%k.p)
        for u in range(n):
            for v in range(n):B[u][v]=k.add(B[u][v],k.mul(coef,R[u][v]))
    H=matmul(k,matmul(k,F,B),Fi)
    apply,kind,rotation=bank_factors(k,n,q,a,b,e,d,w)
    columns=[apply([int(i==j) for i in range(n)]) for j in range(n)]
    represented=[list(r) for r in zip(*columns)]
    assert represented==H,(k.p,k.d,n,a,b,e,d,kind)
    COUNTS[kind]=COUNTS.get(kind,0)+1;TOTAL+=1
    if rotation is not None:ROTATIONS.setdefault(str(n),set()).add(rotation)
    return B,represented

def main():
    started=time.monotonic();n11raw=SOURCE.read_bytes();cert=json.loads(n11raw)
    test_sets=[(K(7),3,2,'exhaustive'),(K(11),5,3,'exhaustive'),(K(19),9,4,'sample'),(K(53),13,16,'sample'),(K(2,[1,1,1]),3,2,'exhaustive'),(K(2,[1,1,0,1]),7,2,'exhaustive')]
    dataset_stats=[];chirp_checks=0
    for k,n,q,mode in test_sets:
        assert k.power(q,n)==1 and all(k.power(q,i)!=1 for i in range(1,n))
        before=TOTAL
        pairs=[(a,b) for a in range(k.order) for b in range(k.order)] if mode=='exhaustive' else list(dict.fromkeys([(k.power(q,i),b) for i in range(n) for b in [1,2,3]]+[(0,0),(0,2),(2,0),(2,2),(3,4),(7,11)]))
        w=[((j*j+5*j+2)%k.order) for j in range(n)]
        for a,b in pairs:
            if not k.sub(k.sub(1,k.power(a,n)),k.power(b,n)):continue
            for e in [-1,1]:
                for d in [-1,1]:test_bank(k,n,q,a,b,e,d,w)
        F=[[k.power(q,(-i*j)%n) for j in range(n)] for i in range(n)]
        for col in range(n):
            x=[int(i==col) for i in range(n)]
            assert chirp(k,n,q,x)==[row[col] for row in F];chirp_checks+=1
        dataset_stats.append({'p':k.p,'degree':k.d,'N':n,'q':q,'bank_cases':TOTAL-before})
    k=K(23,[13,13,13,1]);n=cert['N'];q=k.pack(cert['q']);assert k.power(q,n)==1
    sums=[[0]*n for _ in range(n)];sumsH=[[0]*n for _ in range(n)]
    for row in cert['banks']:
        B,H=test_bank(k,n,q,k.pack(row['alpha']),k.pack(row['beta']),row['epsilon'],row['delta'],[k.pack(w) for w in row['raw_weights']])
        for i in range(n):
            for j in range(n):sums[i][j]=k.add(sums[i][j],B[i][j]);sumsH[i][j]=k.add(sumsH[i][j],H[i][j])
    F=[[k.power(q,(-i*j)%n) for j in range(n)] for i in range(n)]
    assert sums==F and sumsH==F
    for col in range(n):
        x=[int(i==col) for i in range(n)]
        assert chirp(k,n,q,x)==[r[col] for r in F];chirp_checks+=1
    # Adversarial control: the chirp must fail if the kernel exponent's sign is reversed.
    n=5;q=3;k=K(11);h=pow(2,-1,n)
    assert any(k.power(q,(-h*i*i-h*(i-j)*(i-j)-h*j*j)%n)!=k.power(q,(-i*j)%n) for i in range(n) for j in range(n))
    result={'status':'PASS','total_bank_cases':TOTAL,'factor_case_counts':COUNTS,'zero_diagonal_rotation_indices':{n:sorted(s) for n,s in ROTATIONS.items()},'datasets':dataset_stats,'N11_certificate_banks':len(cert['banks']),'N11_source_sha256':hashlib.sha256(n11raw).hexdigest(),'N11_full_sum_and_conjugated_sum':'both equal F in all 121 entries','chirp_basis_columns_checked':chirp_checks,'negative_control_wrong_chirp_sign':'rejected','setup_DFT':'checked against direct sums; implemented using ordinary schoolbook polynomial product and cyclic folding','online_toeplitz':'implemented using ordinary polynomial product; all matrix columns checked','circular_fft_calls':0,'elapsed_seconds':round(time.monotonic()-started,3)}
    (HERE/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
