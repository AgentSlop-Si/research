#!/usr/bin/env python3
"""Fresh standalone exact Q(zeta_5) certificate. No research code imports."""
from fractions import Fraction as Q
from pathlib import Path
import json

P=5
class K:
    def __init__(self, v=0):
        if isinstance(v,K): self.a=v.a; return
        if isinstance(v,(int,Q)): v=[v]
        a=[Q(x) for x in v]+[Q(0)]*max(0,4-len(v))
        for e in range(len(a)-1,3,-1):
            q=a[e]
            for j in range(4):a[e-4+j]-=q
        self.a=tuple(a[:4])
    def __add__(self,o):
        o=K(o);return K([a+b for a,b in zip(self.a,o.a)])
    __radd__=__add__
    def __neg__(self):return K([-a for a in self.a])
    def __sub__(self,o):return self+-K(o)
    def __rsub__(self,o):return K(o)+-self
    def __mul__(self,o):
        o=K(o);a=[Q(0)]*7
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
        basis=[K([0]*j+[1]) for j in range(4)]
        cols=[(self*x).a for x in basis]
        a=[[cols[j][i] for j in range(4)]+[Q(i==0)] for i in range(4)]
        for j in range(4):
            r=next(i for i in range(j,4) if a[i][j]);a[j],a[r]=a[r],a[j]
            q=a[j][j];a[j]=[x/q for x in a[j]]
            for i in range(4):
                if i!=j:
                    q=a[i][j];a[i]=[x-q*y for x,y in zip(a[i],a[j])]
        return K([a[i][-1] for i in range(4)])
    def __truediv__(self,o):return self*K(o).inv()
    def __rtruediv__(self,o):return K(o)*self.inv()
    def serial(self):return [str(a) for a in self.a]

z=K([0,1]); one=K(1);zero=K()
def mm(a,b):return [[sum((a[i][h]*b[h][j] for h in range(len(b))),zero) for j in range(len(b[0]))] for i in range(len(a))]
def eye():return [[K(i==j) for j in range(P)]for i in range(P)]
def nnz(a):return sum(bool(v)for row in a for v in row)
def matserial(a):return [[v.serial() for v in row]for row in a]

c=z+z**4
d=2*z-z**2+z**3-2*z**4
assert c*c+c==1 and d and c
order=[0,1,2,4,3];b=[one,-one,c,-c,d]
F=[[z**(i*j%P) for j in range(P)]for i in range(P)]
C=eye()
for j in range(1,P):C[order[j]][order[j-1]]=-b[j-1]/b[j]
R=[[zero for _ in range(P)]for _ in range(P)]
for j in range(P):
    for t in range(P):R[order[j]][t]=sum((b[k]*z**(order[k]*t%P)for k in range(j+1)),zero)/b[j]
assert mm(C,R)==F
assert nnz(C)==9 and nnz(R)==20
zero_positions=[[i,t]for i in range(P)for t in range(P)if not R[i][t]]
assert sorted(zero_positions)==sorted([[1,0],[4,0],[4,1],[4,4],[3,2]])
# Build every separately charged latent slice, without merging colors.
slices=[];slice_supports=[]
for t in range(P):
    q=(-3*t*t)%P
    B=[[zero for _ in range(P)]for _ in range(P)]
    for i in range(P):B[i][t]=z**q*R[i][t]
    got=mm(mm(C,B),F)
    want=[[z**((q+(i+j)*t)%P)for j in range(P)]for i in range(P)]
    assert got==want
    slices.append(B);slice_supports.append(nnz(B))
assert slice_supports==[3,4,4,5,4]
# Endpoint-corrected total transfer is exactly the unnormalized Fourier matrix.
G=sum((z**((-3*t*t)%P)for t in range(P)),zero);assert G
Cp=[[z**((-3*i*i)%P)*C[i][j]/G for j in range(P)]for i in range(P)]
Ap=[[F[i][j]*z**((-3*j*j)%P)for j in range(P)]for i in range(P)]
Bsum=[[sum((B[i][j]for B in slices),zero)for j in range(P)]for i in range(P)]
assert mm(mm(Cp,Bsum),Ap)==F
# The nilpotent chain inverse has all fifteen triangular entries nonzero.
N=[[C[i][j]-K(i==j)for j in range(P)]for i in range(P)]
Ci=eye();power=eye()
for k in range(1,P):
    power=mm(power,N)
    Ci=[[Ci[i][j]+(-1)**k*power[i][j]for j in range(P)]for i in range(P)]
assert mm(C,Ci)==eye() and nnz(Ci)==15
out={
 'exact_field':'Q[z]/(1+z+z^2+z^3+z^4)',
 'p':P,'chain_order':order,'prefix_coefficients':[v.serial()for v in b],
 'c':c.serial(),'d':d.serial(),'C':matserial(C),'R':matserial(R),
 'A':'F_5[i,j]=z^(ij)','zero_positions_R':zero_positions,
 'outer_nnz_A':nnz(F),'outer_nnz_C':nnz(C),'middle_edges_by_latent_color':slice_supports,
 'total_edges':nnz(F)+nnz(C)+sum(slice_supports),'dense_baseline':2*P*P+P,
 'nnz_C_inverse':nnz(Ci),'delta_C':nnz(Ci)-nnz(C),'delta_A':0,'mixing_penalty':0,
 'every_aggregate_slice_exact':True,'endpoint_corrected_total_exact':True,
 'G':G.serial(),'separately_charged_latent_slices':[matserial(B)for B in slices]
}
Path(__file__).with_name('EXPLICIT_P5_CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items()if k not in ['C','R','separately_charged_latent_slices']},indent=2))
