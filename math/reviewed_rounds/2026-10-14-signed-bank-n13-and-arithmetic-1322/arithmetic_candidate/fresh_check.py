#!/usr/bin/env python3
"""Independent literal and Toeplitz-factor checks. No historical code is imported."""
import hashlib, json, time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
SRC=ROOT/'dependencies/RAW_CERTIFICATE.json'
class Field:
    def __init__(self,p,mod):
        self.p=p; self.mod=mod; self.d=len(mod)-1; self.zero=(0,)*self.d; self.one=self.val(1); self.order=p**self.d
    def val(self,x):
        if isinstance(x,int): return (x%self.p,)+(0,)*(self.d-1)
        return tuple(v%self.p for v in x)
    def add(self,a,b): return tuple((u+v)%self.p for u,v in zip(a,b))
    def neg(self,a): return tuple(-u%self.p for u in a)
    def sub(self,a,b): return self.add(a,self.neg(b))
    def mul(self,a,b):
        c=[0]*(2*self.d-1)
        for i,u in enumerate(a):
            for j,v in enumerate(b): c[i+j]=(c[i+j]+u*v)%self.p
        for i in range(len(c)-1,self.d-1,-1):
            v=c[i]
            for j in range(self.d): c[i-self.d+j]=(c[i-self.d+j]-v*self.mod[j])%self.p
        return tuple(c[:self.d])
    def power(self,a,n):
        if n<0: return self.power(self.inv(a),-n)
        r=self.one
        while n:
            if n&1:r=self.mul(r,a)
            a=self.mul(a,a); n//=2
        return r
    def inv(self,a):
        assert a!=self.zero
        r=self.power(a,self.order-2); assert self.mul(r,a)==self.one
        return r
    def div(self,a,b):return self.mul(a,self.inv(b))
    def sum(self,values):
        r=self.zero
        for v in values:r=self.add(r,v)
        return r

def eye(f,n):return [[f.one if i==j else f.zero for j in range(n)] for i in range(n)]
def mm(f,A,B):return [[f.sum(f.mul(a,b) for a,b in zip(row,col)) for col in zip(*B)] for row in A]
def mv(f,A,x):return [f.sum(f.mul(a,b) for a,b in zip(row,x)) for row in A]
def invert(f,A):
    n=len(A); H=[list(r)+e for r,e in zip(A,eye(f,n))]
    for j in range(n):
        p=next(i for i in range(j,n) if H[i][j]!=f.zero); H[j],H[p]=H[p],H[j]
        v=f.inv(H[j][j]); H[j]=[f.mul(v,a) for a in H[j]]
        for i in range(n):
            if i!=j and H[i][j]!=f.zero:
                v=H[i][j]; H[i]=[f.sub(a,f.mul(v,b)) for a,b in zip(H[i],H[j])]
    assert [r[:n] for r in H]==eye(f,n)
    return [r[n:] for r in H]

def literal_matrix(f,n,q,a,b,e,d,j):
    A=[[f.zero]*n for _ in range(n)]
    for t in range(n):
        A[t][t]=f.sub(f.one,f.mul(b,f.power(q,d*(t+e*j))))
        A[(t+e)%n][t]=f.sub(A[(t+e)%n][t],a)
    return A

def backward_solve(f,n,q,a,b,e,d,j,x):
    # Divide by alpha, never by a possibly zero diagonal.
    if a==f.zero:
        return [f.div(x[t],f.sub(f.one,f.mul(b,f.power(q,d*(t+e*j))))) for t in range(n)]
    ix=[(e*i)%n for i in range(n)]
    r=[f.div(f.sub(f.one,f.mul(b,f.power(q,d*(t+e*j)))),a) for t in ix]
    z=[f.neg(f.div(x[t],a)) for t in ix]
    P=f.one; h=f.zero
    for i in range(n-1,-1,-1):P=f.mul(r[i],P); h=f.add(f.mul(r[i],h),z[i])
    y=[f.zero]*n; y[n-1]=f.div(h,f.sub(f.one,P))
    for i in range(n-1,0,-1):y[i-1]=f.add(f.mul(r[i],y[i]),z[i])
    out=[f.zero]*n
    for i,t in enumerate(ix):out[t]=y[i]
    return out

def toeplitz_conjugate(f,n,q,a,b,e,d,w):
    """Construct F B F^-1 using diagonal/Toeplitz factors only.
    Returns the represented matrix and classification. All transforms of the
    fixed weights are setup, independent of a later input vector.
    """
    invn=f.inv(f.val(n))
    psi=[f.mul(invn,f.sum(f.mul(w[j],f.power(q,e*d*j*h)) for j in range(n))) for h in range(n)]
    ix=[(d*r)%n for r in range(n)]
    ds=[f.sub(f.one,f.mul(a,f.power(q,-e*k))) for k in ix]
    out=[[f.zero]*n for _ in range(n)]
    if b==f.zero:
        for r,k in enumerate(ix):out[k][k]=f.div(psi[0],ds[r])
        return out,'diagonal'
    zeros=[r for r,v in enumerate(ds) if v==f.zero]
    if not zeros:
        p=[]; c=f.one
        for val in ds:c=f.mul(c,f.div(b,val)); p.append(c)
        P=p[-1]; den=f.sub(f.one,P)
        for r in range(n):
            for s in range(n):
                h=psi[(r-s)%n]
                if r<s:h=f.mul(P,h)
                out[ix[r]][ix[s]]=f.div(f.mul(p[r],h),f.mul(den,f.mul(p[s],ds[s])))
        return out,'full_toeplitz'
    assert len(zeros)==1
    r0=zeros[0]; ix=ix[r0:]+ix[:r0]; ds=ds[r0:]+ds[:r0]
    p=[f.one]
    for r in range(1,n):p.append(f.mul(p[-1],f.div(ds[r],b)))
    # Column s' refers to original cyclic column (s'+1) mod N.
    for r in range(n):
        for s in range(r,n):
            h=psi[(r-s-1)%n]
            out[ix[r]][ix[(s+1)%n]]=f.neg(f.div(f.mul(p[s],h),f.mul(b,p[r])))
    return out,'upper_triangular_toeplitz'

def run_case(f,n,q,bank,check_all_inverses=True):
    a=f.val(bank['alpha']);b=f.val(bank['beta']);e=bank['epsilon'];d=bank['delta'];w=[f.val(z) for z in bank['raw_weights']]
    Delta=f.sub(f.sub(f.one,f.power(a,n)),f.power(b,n));assert Delta!=f.zero
    F=[[f.power(q,-k*t) for t in range(n)] for k in range(n)]
    Finv=[[f.mul(f.inv(f.val(n)),f.power(q,k*t)) for t in range(n)] for k in range(n)]
    B=[[f.zero]*n for _ in range(n)]
    x=[f.val((t*t+3*t+1)%f.p) for t in range(n)]
    for j in range(n):
        A=literal_matrix(f,n,q,a,b,e,d,j);R=invert(f,A)
        assert mm(f,A,R)==eye(f,n) and mm(f,R,A)==eye(f,n)
        assert backward_solve(f,n,q,a,b,e,d,j,x)==mv(f,R,x)
        c=f.div(w[j],f.val(n))
        for r in range(n):
            for s in range(n):B[r][s]=f.add(B[r][s],f.mul(c,R[r][s]))
    H,kind=toeplitz_conjugate(f,n,q,a,b,e,d,w)
    assert mm(f,mm(f,F,B),Finv)==H
    return B,H,kind

def main():
    start=time.monotonic(); raw=SRC.read_bytes(); cert=json.loads(raw)
    f=Field(23,[13,13,13,1]);n=cert['N'];q=f.val(cert['q'])
    total=[[f.zero]*n for _ in range(n)];hat=[[f.zero]*n for _ in range(n)];kinds=[]
    for bank in cert['banks']:
        B,H,kind=run_case(f,n,q,bank);kinds.append(kind)
        for i in range(n):
            for j in range(n):total[i][j]=f.add(total[i][j],B[i][j]);hat[i][j]=f.add(hat[i][j],H[i][j])
    F=[[f.power(q,-i*j) for j in range(n)] for i in range(n)]
    assert total==F and hat==F
    # Distinct small field, all orientations, zero alpha/beta, single-zero diagonal,
    # generic cyclic case, and dense weights. All data generated here.
    g=Field(11,[0,1]); cases=0; categories={}
    for a,b in [(0,2),(2,0),(1,1),(2,1),(3,2),(5,4)]:
        if (1-pow(a,5,11)-pow(b,5,11))%11==0:continue
        for e in [-1,1]:
            for d in [-1,1]:
                z={'alpha':a,'beta':b,'epsilon':e,'delta':d,'raw_weights':[(j*j+2*j+4)%11 for j in range(5)]}
                _,_,kind=run_case(g,5,g.val(3),z); cases+=1;categories[kind]=categories.get(kind,0)+1
    chirp_checks=[]
    for prime,nn,qq in [(23,11,13),(53,13,16),(11,5,3)]:
        ff=Field(prime,[0,1]); hh=pow(2,-1,nn); rr=ff.val(qq)
        for k in range(nn):
            for t in range(nn):
                assert ff.power(rr,-k*t)==ff.mul(ff.power(rr,-hh*k*k),ff.mul(ff.power(rr,hh*(k-t)*(k-t)),ff.power(rr,-hh*t*t)))
        chirp_checks.append({'p':prime,'N':nn,'q':qq,'entries':nn*nn})
    for c in [0,1,100,6054]:
        T=c
        for k in range(2,7):
            T=11*T+11**(k-1)*c+10*(11**(k-1)-1)
            assert T==k*11**(k-1)*c+(10*k-11)*11**(k-1)+1
    result={'status':'PASS','classical_chirp_checks':chirp_checks,'radix11_recurrence_checks':'k=1..6 pass' ,'source_sha256':hashlib.sha256(raw).hexdigest(),'N11_banks':len(kinds),'N11_literal_branches':11*len(kinds),'N11_nonzero_raw_weights':sum(any(w) for b in cert['banks'] for w in b['raw_weights']),'N11_factor_kinds':kinds,'N11_total_entries_checked':121,'small_field_cases':cases,'small_field_factor_kinds':categories,'recurrence_vs_gaussian_and_both_inverse_products':'all pass','elapsed_seconds':round(time.monotonic()-start,6)}
    (ROOT/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
