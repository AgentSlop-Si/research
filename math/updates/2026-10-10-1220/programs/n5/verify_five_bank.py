#!/usr/bin/env python3
"""Fresh exact N=5 five-bank control. Standard library only; no research imports.
Arithmetic in Q[q]/Phi_5. All field inverses are checked.
This control verifies the literal, fully specified WITNESS.json artifact.
"""
from fractions import Fraction as F
import json
import hashlib
from pathlib import Path

class K:
    __slots__=('v',)
    def __init__(self, v=0):
        if isinstance(v,K): self.v=v.v; return
        if isinstance(v,(int,F)): v=[v]
        a=list(map(F,v))+[F(0)]*max(0,4-len(v))
        for i in range(len(a)-1,3,-1):
            for j in range(1,5): a[i-j]-=a[i]
        self.v=tuple(a[:4])
    def __add__(self,o):
        o=K(o); return K([a+b for a,b in zip(self.v,o.v)])
    __radd__=__add__
    def __neg__(self): return K([-a for a in self.v])
    def __sub__(self,o): return self+-K(o)
    def __rsub__(self,o): return K(o)+-self
    def __mul__(self,o):
        o=K(o); a=[F(0)]*7
        for i,x in enumerate(self.v):
            for j,y in enumerate(o.v): a[i+j]+=x*y
        return K(a)
    __rmul__=__mul__
    def inv(self):
        assert self
        cols=[(self*K([0]*i+[1])).v for i in range(4)]
        m=[[cols[j][i] for j in range(4)]+[F(i==0)] for i in range(4)]
        for i in range(4):
            p=next(j for j in range(i,4) if m[j][i]); m[i],m[p]=m[p],m[i]
            d=m[i][i]; m[i]=[v/d for v in m[i]]
            for j in range(4):
                if j!=i:
                    d=m[j][i]; m[j]=[a-d*b for a,b in zip(m[j],m[i])]
        z=K([m[i][-1] for i in range(4)])
        assert self*z==1
        return z
    def __truediv__(self,o): return self*K(o).inv()
    def __rtruediv__(self,o): return K(o)*self.inv()
    def __pow__(self,n):
        if n<0:return self.inv()**(-n)
        a=K(1); b=self
        while n:
            if n&1:a=a*b
            b=b*b;n//=2
        return a
    def __eq__(self,o):return self.v==K(o).v
    def __bool__(self):return any(self.v)
    def serial(self):return [str(a) for a in self.v]
    def __repr__(self):return str(self.serial())

q=K([0,1]); c=q+q**4
assert c*(c+1)==1

def gaussian(n,k,z):
    if k<0 or k>n:return K(0)
    tab=[K(1)]+[K(0)]*k
    for m in range(1,n+1):
        tab=[tab[j]+z**(m-j)*tab[j-1] if j else K(1) for j in range(k+1)]
    return tab[k]

def solve(m,b):
    n=len(m);p=len(m[0]);rows=[[K(x) for x in row]+[K(v)] for row,v in zip(m,b)]
    piv=[];r=0
    for j in range(p):
        hit=next((i for i in range(r,n) if rows[i][j]),None)
        if hit is None:continue
        rows[r],rows[hit]=rows[hit],rows[r]
        inv=rows[r][j].inv();rows[r]=[x*inv for x in rows[r]]
        for i in range(n):
            if i!=r:
                scale=rows[i][j]; rows[i]=[x-scale*y for x,y in zip(rows[i],rows[r])]
        piv.append(j);r+=1
        if r==n:break
    if any(not any(row[:-1]) and row[-1] for row in rows):return None,r
    ans=[K(0)]*p
    for i,j in enumerate(piv):ans[j]=rows[i][-1]
    assert all(sum((K(x)*z for x,z in zip(row,ans)),K(0))==v for row,v in zip(m,b))
    return ans,r

def determinant(m):
    m=[row[:] for row in m]; value=K(1)
    for j in range(len(m)):
        pivot=next((i for i in range(j,len(m)) if m[i][j]),None)
        if pivot is None:return K(0)
        if pivot!=j:m[pivot],m[j]=m[j],m[pivot];value=-value
        d=m[j][j];value*=d
        for i in range(j+1,len(m)):
            scale=m[i][j]/d
            for k in range(j,len(m)):m[i][k]-=scale*m[j][k]
    return value

def coefficient(e,d,alpha,ell,a,b):
    if d*ell%5!=b:return K(0)
    r=e*a%5
    return alpha**r*K(gaussian(r+ell,ell,q**(e*d%5))) if r+ell<=4 else K(0)

def zeros():return [[K(0) for _ in range(5)] for _ in range(5)]
def identity():return [[K(i==j) for j in range(5)] for i in range(5)]
def madd(x,y):return [[a+b for a,b in zip(r,s)] for r,s in zip(x,y)]
def mscale(x,c):return [[a*c for a in r] for r in x]
def mmul(x,y):return [[sum((x[i][k]*y[k][j] for k in range(5)),K(0)) for j in range(5)] for i in range(5)]

def main():
    witness=json.loads(Path(__file__).with_name('WITNESS.json').read_text())
    banks=[(b['epsilon'],b['delta_sign'],K(b['alpha'])) for b in witness['banks']]
    h=[[K(v) for v in b['normalized_h']] for b in witness['banks']]
    y=q; z=banks[1][2]
    ranks=[]; determinants={}
    for b in range(5):
        ells=[d*b%5 for e,d,a in banks]
        mat=[[coefficient(e,d,a,l,k,b) for (e,d,a),l in zip(banks,ells)] for k in range(5)]
        ans,rank=solve(mat,[q**(4*(a+b)**2%5) for a in range(5)])
        assert ans is not None
        ranks.append(rank)
        if b in (0,2,3):determinants[str(b)]=determinant(mat).serial()
    assert determinants=={'0':['-1093','-5351','-6894','-3592'],'2':['31','21','-17','-30'],'3':['6','19','21','9']}
    x=banks[0][2];z=banks[1][2];y=banks[2][2];v=banks[3][2];u=banks[4][2]
    M=c*y*y-q*q;N=(y+q*q)/c
    assert N==(x+z)*M-x*z
    assert u==c*v*v-q*q and v==c*u*u-q*q
    assert z==(N-x*M)/(M-x)
    assert x!=z and all(alpha for e,d,alpha in banks)
    C=sum((q**(-j*j%5) for j in range(5)),K(0))/5
    assert C
    assert ranks==[5,4,5,5,3]
    target=[[K(q**(-i*j%5)) for j in range(5)] for i in range(5)]
    # Independently recover all target Weyl coefficients directly by trace.
    for a in range(5):
        for b in range(5):
            extracted=sum((target[(i+a)%5][i]*K(q**(-b*i%5)) for i in range(5)),K(0))/5
            assert extracted==K(C*q**(4*(a+b)**2%5))
            got=sum((h[n][l]*coefficient(e,d,alpha,l,a,b) for n,(e,d,alpha) in enumerate(banks) for l in range(5)),K(0))
            assert got==K(q**(4*(a+b)**2%5))
    total=zeros(); raw=[]
    I=identity()
    for idx,(e,d,alpha) in enumerate(banks):
        delta=1-alpha**5-1
        assert delta*delta.inv()==1
        weights=[sum((K(C)*delta*h[idx][l]*K(q**(-e*d*j*l%5)) for l in range(5)),K(0)) for j in range(5)]
        assert weights==[K(v) for v in witness['banks'][idx]['raw_weights']]
        assert delta==K(witness['banks'][idx]['Delta'])
        assert K(witness['banks'][idx]['beta'])==1
        bank=zeros()
        for j,w in enumerate(weights):
            X=zeros()
            for i in range(5):
                X[(i+e)%5][i]+=alpha
                X[i][i]+=K(q**(e*d*j+d*i))
            numerator=zeros();power=I
            for r in range(5):
                numerator=madd(numerator,power);power=mmul(power,X)
            branch=mscale(numerator,delta.inv())
            Q=madd(I,mscale(X,K(-1)))
            assert mmul(Q,branch)==I
            assert mmul(branch,Q)==I
            bank=madd(bank,mscale(branch,w/5))
        total=madd(total,bank)
        raw.append({'epsilon':e,'delta_sign':d,'alpha':alpha.serial(),'beta':K(1).serial(),'Delta':delta.serial(),'normalized_h':[v.serial() for v in h[idx]],'raw_weights':[v.serial() for v in weights]})
    assert total==target
    output={'status':'exact characteristic-zero five-bank witness verified','witness_sha256':hashlib.sha256(Path(__file__).with_name('WITNESS.json').read_bytes()).hexdigest(),'square_row_determinants':determinants,'arithmetic':'Q[q]/Phi_5, t=1+q','fixed_parameters':{'x1':K(1).serial(),'y':y.serial(),'x2':z.serial()},'row_ranks_b0_through_b4':ranks,'checks':{'generic_lemma_specialization':True,'three_determinant_residues':True,'25_Weyl_coefficients':True,'25_direct_trace_coefficients':True,'25_original_branch_inverses_both_sides':True,'5_Delta_units':True,'25_original_matrix_entries':True},'banks':raw}
    path=Path(__file__).with_name('certificate_results.json');path.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k!='banks'},indent=2))

if __name__=='__main__':main()
