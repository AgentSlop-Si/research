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

z=K([0,1]); g=1+2*(z**2+z**3)
assert z**5==1 and z!=1 and g*g==5
B=[[(z**(i*j)-g*z**(-3*(i+j)**2)+(5*g*z**(-3*i*i) if i==j else 0))/(1+5*g) for j in range(5)] for i in range(5)]
Binv=[[(z**(-i*j))/5+(z**(3*i*i) if i==j else 0) for j in range(5)] for i in range(5)]
for i in range(5):
 for j in range(5):
  assert sum(B[i][k]*Binv[k][j] for k in range(5))==int(i==j)
  assert sum(Binv[i][k]*B[k][j] for k in range(5))==int(i==j)
a,b,c,e,f,h=B[0][1],B[0][2],B[1][2],B[1][3],B[1][4],B[2][3]
assert B[0][4]==a and B[0][3]==b and B[3][4]==c and B[2][4]==e
A,Cb,C,D=c/(a*b),e/(a*b),f/(a*a),h/(b*b)
p2=Cb*Cb-C*D
p1=-2*A*Cb+A*C+A*D+Cb*C+Cb*D-2*C*D
p0=(Cb-C)**2
assert p2 and p0
E.p0=p0/p2;E.p1=p1/p2
print('constants',A,Cb,C,D)
print('monic polynomial', E.p0,E.p1)
disc=E.p1*E.p1-4*E.p0
print('discriminant',disc)
assert disc
xdelta=E(0,1)
assert xdelta*xdelta+E(E.p1)*xdelta+E(E.p0)==0
A,Cb,C,D=E(A),E(Cb),E(C),E(D)
t=(C*xdelta+(A+Cb)*xdelta*xdelta)/(C*(xdelta+2)-(A+Cb))
print('t',t.serial())
for name,x in [('delta',xdelta),('t',t),('t-1',t-1),('t+1',t+1)]:
 print('guard',name,x.norm())
 assert x.norm()
kappa=(t+xdelta*xdelta)/C
x=(t-xdelta)/kappa
r=[None,x,(A-x)/xdelta,(Cb-x)/xdelta,(C-x)/xdelta]
zpar=kappa/(1+t)
u=[E(1)]+[E(B[0][i])*r[i] for i in range(1,5)]
v=[zpar/t]+[E(B[0][i])-zpar*u[i] for i in range(1,5)]
for i in range(5):
 for j in range(i+1,5):
  assert u[i]*v[j]+t*v[i]*u[j]==E(B[i][j]),('offdiag',i,j)
diag=[E(B[i][i])-(1+t)*u[i]*v[i] for i in range(5)]
# Direct Green inverse formula and full target identity.
G0=[[E(1 if i<=j else 0)+ (t if i>j else 0) for j in range(5)] for i in range(5)]
G0=[[x/(1-t) for x in row] for row in G0]
G1=[[(E(1) if i<=j else 1/t)/(1-1/t) for j in range(5)] for i in range(5)]
for i in range(5):
 for j in range(5):
  val=(1-t)*u[i]*G0[i][j]*v[j]+(t-1)*v[i]*G1[i][j]*u[j]+(diag[i] if i==j else 0)
  assert val==E(B[i][j]),('target',i,j)
  w0=t if i==4 else E(1);w1=1/t if i==4 else E(1)
  assert G0[i][j]-w0*G0[(i+1)%5][j]==E(int(i==j))
  assert G1[i][j]-w1*G1[(i+1)%5][j]==E(int(i==j))
print('PASS 25 entries, both Green inverses, 10 off-diagonals')
result={'status':'PASS','base_field':'Q[zeta]/(1+zeta+zeta²+zeta³+zeta⁴)','extension_polynomial_monic':{'constant':E.p0.serial(),'linear':E.p1.serial(),'quadratic':K(1).serial()},'discriminant':disc.serial(),'pole_t':t.serial(),'delta':xdelta.serial(),'u':[x.serial() for x in u],'v':[x.serial() for x in v],'diagonal_correction':[x.serial() for x in diag],'target':[[x.serial() for x in row] for row in B],'guards':{name:x.norm().serial() for name,x in [('delta',xdelta),('t',t),('t-1',t-1),('t+1',t+1),('kappa',kappa),('t_denominator',C*(xdelta+2)-(A+Cb))]},'verified_full_target_entries':25,'verified_inverse_entries':50,'verified_forced_target_inverse_entries':50}
# Irreducible quadratic reduction at the accepted N5 arithmetic place.
def residue(a, p=241, root=91):
    return sum((x.numerator * pow(x.denominator, -1, p) % p) * pow(root, i, p) for i,x in enumerate(a.a)) % p
assert residue(E.p1)==30 and residue(E.p0)==124
assert residue(disc)==163 and pow(163,120,241)==240
trace_t=2*t.a-E.p1*t.b
assert t*t-E(trace_t)*t+1==0 and t.norm()==1
result['pole_polynomial_monic']={'constant':K(1).serial(),'linear':(-trace_t).serial(),'quadratic':K(1).serial()}
result['guard_norm_residues_mod_241']={name:residue(x.norm()) for name,x in [('delta',xdelta),('t',t),('t-1',t-1),('t+1',t+1),('kappa',kappa),('t_denominator',C*(xdelta+2)-(A+Cb))]}
assert all(result['guard_norm_residues_mod_241'].values())
result['irreducible_reduction']={'prime':241,'zeta_residue':91,'delta_polynomial':[124,30,1],'discriminant':163,'Euler_criterion':240}
# All four primitive embeddings are covered by base-field automorphisms.
result['endpoint_nonzero_norms']={name:[x.norm().serial() for x in values] for name,values in [('u',u),('v',v),('diagonal_correction',diag)]}
assert all(x.norm() for values in [u,v,diag] for x in values)
result['guard_scope']='Every recorded guard norm is a nonzero element of Q(zeta5), so it is nonzero under every primitive embedding and at both roots of the separable quadratic.'
parser=argparse.ArgumentParser();parser.add_argument('--out-dir',default=str(Path(__file__).resolve().parent));args=parser.parse_args()
output=Path(args.out_dir);output.mkdir(parents=True,exist_ok=True)
path=output/'EXACT_THREE_GREEN_RESULTS.json';path.write_text(json.dumps(result,indent=2)+'\n')
print('result_sha256',hashlib.sha256(path.read_bytes()).hexdigest())
