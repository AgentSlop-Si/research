#!/usr/bin/env python3
"""Fresh standalone exact prime cyclotomic certificate. No research code imports."""
from fractions import Fraction as Q
from pathlib import Path
import json

P=5
class K:
    def __init__(self, v=0):
        if isinstance(v,K): self.a=v.a; return
        if isinstance(v,(int,Q)): v=[v]
        a=[Q(x) for x in v]+[Q(0)]*max(0,P-1-len(v))
        for e in range(len(a)-1,P-2,-1):
            q=a[e]
            for j in range(P-1):a[e-(P-1)+j]-=q
        self.a=tuple(a[:P-1])
    def __add__(self,o):
        o=K(o);return K([a+b for a,b in zip(self.a,o.a)])
    __radd__=__add__
    def __neg__(self):return K([-a for a in self.a])
    def __sub__(self,o):return self+-K(o)
    def __rsub__(self,o):return K(o)+-self
    def __mul__(self,o):
        o=K(o);a=[Q(0)]*(2*P-3)
        for i,x in enumerate(self.a):
            for j,y in enumerate(o.a):a[i+j]+=x*y
        return K(a)
    __rmul__=__mul__
    def __eq__(self,o):return self.a==K(o).a
    def __bool__(self):return any(self.a)
    def __pow__(self,n):
        if n<0:return self.inv()**(-n)
        a,b=K(1),self
        while n:
            if n&1:a=a*b
            b=b*b;n//=2
        return a
    def inv(self):
        assert self
        basis=[K([0]*j+[1]) for j in range(P-1)]
        cols=[(self*x).a for x in basis]
        a=[[cols[j][i] for j in range(P-1)]+[Q(i==0)] for i in range(P-1)]
        for j in range(P-1):
            r=next(i for i in range(j,P-1) if a[i][j]);a[j],a[r]=a[r],a[j]
            q=a[j][j];a[j]=[x/q for x in a[j]]
            for i in range(P-1):
                if i!=j:
                    q=a[i][j];a[i]=[x-q*y for x,y in zip(a[i],a[j])]
        return K([a[i][-1] for i in range(P-1)])
    def __truediv__(self,o):return self*K(o).inv()
    def __rtruediv__(self,o):return K(o)*self.inv()
    def serial(self):return [str(a) for a in self.a]

def mm(a,b):
    return [[sum((a[i][h]*b[h][j] for h in range(len(b)) if a[i][h] and b[h][j]),K()) for j in range(len(b[0]))] for i in range(len(a))]
def eye():return [[K(i==j)for j in range(P)]for i in range(P)]
def nnz(a):return sum(bool(v)for row in a for v in row)
def matserial(a):return [[v.serial()for v in row]for row in a]
def run(p,packed):
    global P
    P=p; z=K([0,1]);one=K(1);zero=K()
    zp=[z**t for t in range(p)]
    a=one+zp[1]+zp[-1]
    assert a and a!=one
    origins=list(range(1,p-2,4)) if packed else [0]
    m=len(origins)
    F=[[zp[i*j%p]for j in range(p)]for i in range(p)]
    C=eye();R=[row[:]for row in F]
    for q in origins:
        chain=[q,(q+1)%p,(q+2)%p,(q-1)%p]
        for j,link in enumerate([one,a,one],1):
            C[chain[j]][chain[j-1]]=link
            R[chain[j]]=[F[chain[j]][t]-link*R[chain[j-1]][t]for t in range(p)]
    assert len({i for q in origins for i in [q,(q+1)%p,(q+2)%p,(q-1)%p]})==4*m
    assert mm(C,R)==F
    assert nnz(C)==p+3*m and nnz(R)==p*p-4*m
    expected_zeros=sorted([(i,t)for q in origins for i,t in [((q+1)%p,0),((q-1)%p,0),((q-1)%p,1),((q-1)%p,p-1)]])
    zeros=[(i,t)for i in range(p)for t in range(p)if not R[i][t]]
    assert zeros==expected_zeros
    r=[sum(bool(R[i][t])for i in range(p))for t in range(p)]
    assert r==[p-2*m]+[p-m]+[p]*(p-3)+[p-m]
    N=[[C[i][j]-K(i==j)for j in range(p)]for i in range(p)]
    power=eye();Ci=eye()
    for k in range(1,4):
        power=mm(power,N)
        Ci=[[Ci[i][j]+(-1)**k*power[i][j]for j in range(p)]for i in range(p)]
    assert nnz(mm(power,N))==0
    assert nnz(Ci)==p+6*m and mm(C,Ci)==eye()
    inv2=(p+1)//2;slices=[]
    for t in range(p):
        phase=zp[(-inv2*t*t)%p]
        B=[[phase*R[i][t] if j==t else zero for j in range(p)]for i in range(p)]
        assert nnz(B)==r[t]
        actual=mm(mm(C,B),F)
        expected=[[zp[(-inv2*t*t+(i+j)*t)%p]for j in range(p)]for i in range(p)]
        assert actual==expected
        slices.append(B)
    G=sum((zp[(-inv2*t*t)%p]for t in range(p)),zero);assert G
    Bsum=[[sum((B[i][j]for B in slices),zero)for j in range(p)]for i in range(p)]
    Cprime=[[zp[(-inv2*i*i)%p]*C[i][j]/G for j in range(p)]for i in range(p)]
    Aprime=[[F[i][j]*zp[(-inv2*j*j)%p]for j in range(p)]for i in range(p)]
    assert mm(mm(Cprime,Bsum),Aprime)==F
    out={'p':p,'mode':'packed'if packed else'single_wrap_chain','origins':origins,'m':m,
         'nnz_A':p*p,'nnz_C':nnz(C),'nnz_R':nnz(R),'nnz_C_inverse':nnz(Ci),
         'middle_edges_by_latent_color':r,'total_edges':p*p+nnz(C)+sum(r),
         'dense_baseline':2*p*p+p,'saving':m,'inverse_expansion':3*m,'mixing_penalty':0,
         'zero_positions_R':zeros,'fiber_entries_checked':p**3,'corrected_transfer_entries_checked':p*p,
         'all_exact_checks_passed':True}
    if p==5 and not packed:
        out.update({'a':a.serial(),'C':matserial(C),'R':matserial(R),'separate_B_t':[matserial(B)for B in slices]})
    return out

cases=[run(5,False),run(5,True),run(7,True),run(11,True)]
# Exhaust the normalized at-most-two-extra-edge support patterns at p=3.
from itertools import combinations
positions=[(i,j)for i in range(3)for j in range(3)if i!=j]
classification={'square_zero':0,'two_cycle':0,'three_vertex_chain':0}
for k in range(3):
    for entries in combinations(positions,k):
        if len(entries)<2:kind='square_zero'
        else:
            (i,j),(u,v)=entries
            if i==v and j==u:kind='two_cycle'
            elif j==u or v==i:kind='three_vertex_chain'
            else:kind='square_zero'
        classification[kind]+=1
assert classification=={'square_zero':13,'two_cycle':3,'three_vertex_chain':6}
out={'scope':'Fresh exact prime-complex controls; symbolic proofs are in GAUSS_CHAIN_FAMILY.md',
     'cases':cases,'normalized_p3_support_classification':classification,
     'fiber_entries_checked':sum(c['fiber_entries_checked']for c in cases),
     'corrected_transfer_entries_checked':sum(c['corrected_transfer_entries_checked']for c in cases)}
Path(__file__).with_name('FOUR_CHAIN_EXACT_CONTROLS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'cases':[{k:v for k,v in c.items()if k not in ['C','R','separate_B_t']}for c in cases],
                  'normalized_p3_support_classification':classification},indent=2))
