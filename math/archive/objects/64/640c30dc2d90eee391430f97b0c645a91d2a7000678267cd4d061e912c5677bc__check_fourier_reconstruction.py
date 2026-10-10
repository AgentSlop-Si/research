#!/usr/bin/env python3
from fractions import Fraction as Q
from pathlib import Path
import json
import argparse
import hashlib

def trim(a):
    a=list(a)
    while a and a[-1]==0:a.pop()
    return a

def pa(a,b):
    return trim([(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))])

def pn(a):return [-x for x in a]
def pm(a,b):
    c=[Q(0)]*(max(0,len(a)+len(b)-1))
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return trim(c)
def pd(a,b):
    a=trim(a);b=trim(b)
    if not b:raise ZeroDivisionError
    q=[Q(0)]*max(0,len(a)-len(b)+1)
    while len(a)>=len(b):
        j=len(a)-len(b); t=a[-1]/b[-1];q[j]=t
        a=pa(a,pn([0]*j+[t*x for x in b]))
    return trim(q),a

def pinv(a,m):
    r0,r1=list(m),trim(a); s0,s1=[],[Q(1)]
    while r1:
        q,r=pd(r0,r1);r0,r1=r1,r;s0,s1=s1,pa(s0,pn(pm(q,s1)))
    if len(r0)!=1:raise ZeroDivisionError('nonunit base field')
    return pd([x/r0[0] for x in s0],m)[1]

class K:
    modulus=[Q(1)]*5
    def __init__(self,a=0):
        if isinstance(a,K):self.a=a.a;return
        a=list(a) if isinstance(a,(tuple,list)) else [a]
        a=pd([Q(x) for x in a],self.modulus)[1]
        self.a=tuple(a+[Q(0)]*(4-len(a)))
    def __add__(self,b):return K(pa(self.a,K(b).a))
    __radd__=__add__
    def __neg__(self):return K(pn(self.a))
    def __sub__(self,b):return self+-K(b)
    def __rsub__(self,b):return K(b)+-self
    def __mul__(self,b):return K(pm(self.a,K(b).a))
    __rmul__=__mul__
    def inv(self):return K(pinv(self.a,self.modulus))
    def __truediv__(self,b):return self*K(b).inv()
    def __rtruediv__(self,b):return K(b)*self.inv()
    def __eq__(self,b):return self.a==K(b).a
    def __bool__(self):return any(self.a)
    def __pow__(self,n):
        if n<0:return self.inv()**(-n)
        out=K(1); a=self
        while n:
            if n&1:out=out*a
            a=a*a;n//=2
        return out
    def serial(self):return [str(x) for x in self.a]
    def __repr__(self):return str(self.serial())

class E:
    p0=None;p1=None
    def __init__(self,a=0,b=0):
        if isinstance(a,E):self.a,self.b=a.a,a.b
        else:self.a,self.b=K(a),K(b)
    def __add__(self,y):
        y=E(y);return E(self.a+y.a,self.b+y.b)
    __radd__=__add__
    def __neg__(self):return E(-self.a,-self.b)
    def __sub__(self,y):return self+-E(y)
    def __rsub__(self,y):return E(y)+-self
    def __mul__(self,y):
        y=E(y)
        return E(self.a*y.a-self.p0*self.b*y.b,self.a*y.b+self.b*y.a-self.p1*self.b*y.b)
    __rmul__=__mul__
    def norm(self):return self.a*self.a-self.p1*self.a*self.b+self.p0*self.b*self.b
    def inv(self):
        norm=self.norm()
        if not norm:raise ZeroDivisionError('quadratic algebra denominator nonunit')
        return E((self.a-self.p1*self.b)/norm,-self.b/norm)
    def __truediv__(self,y):return self*E(y).inv()
    def __rtruediv__(self,y):return E(y)*self.inv()
    def __eq__(self,y):
        y=E(y);return self.a==y.a and self.b==y.b
    def __bool__(self):return bool(self.a) or bool(self.b)
    def __pow__(self,n):
        if n<0:return self.inv()**(-n)
        out=E(1);a=self
        while n:
            if n&1:out=out*a
            a=a*a;n//=2
        return out
    def serial(self):return {'constant':self.a.serial(),'delta':self.b.serial()}


def mm(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def ma(a,b):return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def ms(c,a):return [[c*x for x in r] for r in a]
def ident(n=5):return [[K(int(i==j)) for j in range(n)] for i in range(n)]
def diag(a):return [[x if i==j else K(0) for j in range(len(a))] for i,x in enumerate(a)]
def mi(a):
    n=len(a);b=[list(row)+ident(n)[i] for i,row in enumerate(a)]
    for j in range(n):
        k=next(i for i in range(j,n) if b[i][j]);b[j],b[k]=b[k],b[j]
        t=b[j][j];b[j]=[x/t for x in b[j]]
        for i in range(n):
            if i!=j:
                t=b[i][j];b[i]=[x-t*y for x,y in zip(b[i],b[j])]
    return [row[n:] for row in b]

parser=argparse.ArgumentParser();parser.add_argument('--out-dir',default=str(Path(__file__).resolve().parent));args=parser.parse_args()
source=Path(__file__).resolve().parent/'source/CERTIFICATE_INPUT.json'
cert=json.loads(source.read_text())
E.p0=K(cert['extension_polynomial_monic']['constant']);E.p1=K(cert['extension_polynomial_monic']['linear'])
def decode(x):return E(K(x['constant']),K(x['delta']))
u=list(map(decode,cert['u']));v=list(map(decode,cert['v']));delta=list(map(decode,cert['diagonal_correction']));t=decode(cert['pole_t'])
z=K([0,1]);g=1+2*(z**2+z**3);c=5*g
F=[[z**(i*j) for j in range(5)] for i in range(5)]
Fbar=[[z**(-i*j)/5 for j in range(5)] for i in range(5)]
adiag=[z**(3*i*i) for i in range(5)];A=diag(adiag);I=ident()
B=mi(ma(Fbar,A));assert B==[[K(x) for x in row] for row in cert['target']]
M=mm(A,F);M2=mm(M,M);assert mm(M2,M)==ms(c,I)
loop=mm(A,B);loop2=mm(loop,loop);loop3=mm(loop2,loop)
mu=ma(ma(ms(1+c,loop3),ms(-3*c,loop2)),ma(ms(3*c,loop),ms(-c,I)));assert mu==ms(0,I)
closure=ma(ma(ms(1+c,loop2),ms(1-2*c,loop)),ms(1+c,I))
assert mm(ma(I,ms(-1,loop)),closure)==I and mm(closure,ma(I,ms(-1,loop)))==I
assert mm(B,closure)==F
BAB=mm(mm(B,A),B);BABAB=mm(mm(BAB,A),B)
reconstructed=ma(ma(ms(1+c,B),ms(1-2*c,BAB)),ms(1+c,BABAB));assert reconstructed==F
counts={'B_calls':0,'Green_solves':0,'diagonal_corrections':0,'A_calls':0}

def solve_green(closing,x):
    counts['Green_solves']+=1
    weights=[E(1)]*4+[closing]
    pref,total=E(1),E(0)
    for j in range(5):total+=pref*x[j];pref*=weights[j]
    y=[total/(1-pref)]+[E(0)]*4
    for i in range(4,0,-1):y[i]=x[i]+weights[i]*y[(i+1)%5]
    assert all(y[i]-weights[i]*y[(i+1)%5]==x[i] for i in range(5))
    return y

def apply_B(x):
    counts['B_calls']+=1;counts['diagonal_corrections']+=1
    a=solve_green(t,[v[i]*x[i] for i in range(5)])
    b=solve_green(1/t,[u[i]*x[i] for i in range(5)])
    return [(1-t)*u[i]*a[i]+(t-1)*v[i]*b[i]+delta[i]*x[i] for i in range(5)]

def apply_A(x):
    counts['A_calls']+=1
    return [E(adiag[i])*x[i] for i in range(5)]

vectors=[[E(int(i==j)) for i in range(5)] for j in range(5)]
vectors += [[E(i+1) for i in range(5)],[E(z**i) for i in range(5)]]
for x in vectors:
    y0=apply_B(x);y1=apply_B(apply_A(y0));y2=apply_B(apply_A(y1))
    out=[E(1+c)*y0[i]+E(1-2*c)*y1[i]+E(1+c)*y2[i] for i in range(5)]
    expected=[sum(E(F[i][j])*x[j] for j in range(5)) for i in range(5)]
    assert out==expected
assert counts=={'B_calls':21,'Green_solves':42,'diagonal_corrections':21,'A_calls':14}
result={'status':'PASS','matrix_entries_per_identity':25,'identities':['target_inverse_definition','(AF)^3=cI','cubic_mu(AB)=0','(I-AB)*closure=I','closure*(I-AB)=I','B*closure=F','F=(1+c)B+(1-2c)BAB+(1+c)BABAB'],'c':c.serial(),'scan_basis_vectors':5,'scan_additional_vectors':2,'exact_output_entries':35,'all_scan_counts':counts,'per_transform_counts':{'sequential_B_calls':3,'nontrivial_cyclic_Green_solves':6,'diagonal_correction_applications':3,'chirp_A_applications':2},'scope':'Fixed N5 exact reconstruction; no all-length family, root-generation oracle or speedup claim.'}
output=Path(args.out_dir);output.mkdir(parents=True,exist_ok=True);path=output/'RECONSTRUCTION_RESULTS.json';path.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','scan_output_entries':35,'Green_solves':42,'result_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}))
