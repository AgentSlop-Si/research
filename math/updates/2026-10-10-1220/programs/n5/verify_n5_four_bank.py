#!/usr/bin/env python3
"""Original exact certificate for the characteristic-zero N=5 four-bank obstruction.

Python standard library only. No imported research files, floating point, numerical
roots, parameter search, Groebner-basis routine, or finite-field inference.
Coefficients are exact in Q[q]/(1+q+q^2+q^3+q^4).
"""
from fractions import Fraction as F
from math import comb
import json

class K:
    """Cyclotomic field elements, stored in the basis 1,q,q^2,q^3."""
    def __init__(self, v=0):
        if isinstance(v, K): self.a=v.a; return
        if not isinstance(v, (tuple,list)): v=[v]
        a=list(map(F,v))+[F(0)]*max(0,4-len(v))
        for i in range(len(a)-1,3,-1):
            z=a[i]
            for j in range(1,5): a[i-j]-=z
        self.a=tuple(a[:4])
    def __add__(self,b):
        b=K(b); return K([x+y for x,y in zip(self.a,b.a)])
    __radd__=__add__
    def __neg__(self):return K([-x for x in self.a])
    def __sub__(self,b):return self+-K(b)
    def __rsub__(self,b):return K(b)+-self
    def __mul__(self,b):
        b=K(b);a=[F(0)]*7
        for i,x in enumerate(self.a):
            for j,y in enumerate(b.a):a[i+j]+=x*y
        return K(a)
    __rmul__=__mul__
    def __pow__(self,n):
        if n<0:return self.inv()**(-n)
        a=K(1);b=self
        while n:
            if n&1:a=a*b
            b=b*b;n//=2
        return a
    def inv(self):
        assert self != 0
        cols=[(self*K([0]*j+[1])).a for j in range(4)]
        rows=[[cols[j][i] for j in range(4)]+[F(i==0)] for i in range(4)]
        for j in range(4):
            p=next(i for i in range(j,4) if rows[i][j]);rows[j],rows[p]=rows[p],rows[j]
            z=rows[j][j];rows[j]=[x/z for x in rows[j]]
            for i in range(4):
                if i!=j:
                    z=rows[i][j];rows[i]=[x-z*y for x,y in zip(rows[i],rows[j])]
        return K([r[-1] for r in rows])
    def __truediv__(self,b):return self*K(b).inv()
    def __rtruediv__(self,b):return K(b)*self.inv()
    def __eq__(self,b):return self.a==K(b).a
    def vector(self):return [str(a) for a in self.a]

class L:
    """Laurent polynomials in x,y,u,v, with exact cyclotomic coefficients."""
    Z=(0,0,0,0)
    def __init__(self,v=0):
        if isinstance(v,L):self.d=dict(v.d)
        elif isinstance(v,dict):self.d={m:K(c) for m,c in v.items() if K(c)!=0}
        else:self.d={} if K(v)==0 else {self.Z:K(v)}
    @classmethod
    def monomial(cls,i,p=1):
        m=[0]*4;m[i]=p;return cls({tuple(m):K(1)})
    def __add__(self,b):
        d=dict(self.d)
        for m,c in L(b).d.items():d[m]=d.get(m,K(0))+c
        return L(d)
    __radd__=__add__
    def __neg__(self):return L({m:-c for m,c in self.d.items()})
    def __sub__(self,b):return self+-L(b)
    def __rsub__(self,b):return L(b)+-self
    def __mul__(self,b):
        d={}
        for m,c in self.d.items():
            for n,e in L(b).d.items():
                p=tuple(a+b for a,b in zip(m,n));d[p]=d.get(p,K(0))+c*e
        return L(d)
    __rmul__=__mul__
    def __pow__(self,n):
        if n<0:
            assert len(self.d)==1
            m,c=next(iter(self.d.items()));return L({tuple(n*a for a in m):c**n})
        a=L(1);b=self
        while n:
            if n&1:a=a*b
            b=b*b;n//=2
        return a
    def __truediv__(self,b):return self*L(b)**-1
    def __eq__(self,b):return self.d==L(b).d
    def substitute(self,values):
        out=L(0)
        for m,c in self.d.items():
            term=L(c)
            for a,n in zip(values,m):term=term*a**n
            out=out+term
        return out

q=K([0,1]);c=q+q**4;d=1+q**4
x,y,u,v=[L.monomial(i) for i in range(4)]
checks=[]
def check(name,condition):
    assert condition,name
    checks.append(name)
def Q(a):return L(a)
def gaussian(n,k,z):
    a=K(1)
    for i in range(1,k+1):a=a*(1-z**(n-k+i))/(1-z**i)
    return a

def multiply_weyl(A,B):
    ans={}
    for (a,b),z in A.items():
        for (r,l),w in B.items():
            ij=((a+r)%5,(b+l)%5)
            ans[ij]=ans.get(ij,L(0))+z*w*Q(q**((b*r)%5))
    return {ij:p for ij,p in ans.items() if p!=0}

check('q has order 5 and satisfies Phi5',q**5==1 and q!=1 and sum((q**j for j in range(5)),K(0))==0)
check('c inverse identity',c*(c+1)==1)
# Independently prove the signed inverse numerator formula as a Laurent-polynomial
# identity for generic alpha=x, beta=y and all twenty signed/phase branches.
for e,dd in [(1,1),(-1,1),(1,-1),(-1,-1)]:
    z=q**((e*dd)%5)
    for j in range(5):
        numerator={}
        for ell in range(5):
            for r in range(5-ell):
                numerator[(e*r%5,dd*ell%5)]=x**r*y**ell*Q(gaussian(r+ell,ell,z)*z**(j*ell))
        branch={(0,0):L(1),(e%5,0):-x,(0,dd%5):-y*Q(z**j)}
        check(f'original signed inverse identity ({e},{dd}), phase {j}',multiply_weyl(branch,numerator)=={(0,0):1-x**5-y**5})
# Root character orthogonality justifies independently free h-sector relaxation.
for a in range(5):
    check(f'phase character orthogonality sector {a}',sum((q**(j*a) for j in range(5)),K(0))==K(5 if a==0 else 0))
# Recompute all 25 Fourier Weyl coefficients directly by trace, without using the
# chirp formula in the computation. W(a,b)^(-1)e_i=q^[-b(i-a)]e_(i-a).
C=sum((q**((-j*j)%5) for j in range(5)),K(0))/5
check('nonzero Fourier normalization',C!=0)
for a in range(5):
    for b in range(5):
        coeff=sum((q**((-b*i-(i+a)*i)%5) for i in range(5)),K(0))/5
        check(f'Fourier Weyl coefficient ({a},{b})',coeff==C*q**((4*(a+b)**2)%5))
f=lambda a,b:q**((4*(a+b)**2)%5)
# Orientation order: x=(++), y=(-+), u=(--), v=(+-).
orient=[(1,1,x),(-1,1,y),(-1,-1,u),(1,-1,v)]
h={}
def local_coefficient(e,dd,a,ell,aa):
    r=(e*aa)%5
    return L(0) if r+ell>=5 else a**r*Q(gaussian(r+ell,ell,q**((e*dd)%5)))
for e,dd,a in orient:
    for ell in (1,2):
        h[e,dd,ell]=Q(f(e*ell,dd*ell)/gaussian(2*ell,ell,q**((e*dd)%5)))/a**ell
    check(f'exclusive h1 ({e},{dd})',h[e,dd,1]==Q(q**3+q+1)/a)
    check(f'exclusive h2 ({e},{dd})',h[e,dd,2]==Q(q**2)/a**2)

def offaxis_row_residual(dd,aa):
    return sum((h[e,dd,1]*local_coefficient(e,dd,a,1,aa) for e,ddd,a in orient if ddd==dd),L(0))-Q(f(aa,dd))
E1=x-Q(c)*y**2+Q(q**2);E2=y-Q(c)*x**2+Q(q**2)
E3=u-Q(c)*v**2+Q(q**2);E4=v-Q(c)*u**2+Q(q**2)
check('row +1 first equation',offaxis_row_residual(1,2)==-Q(q**4)*E1)
check('row +1 second equation',offaxis_row_residual(1,3)==-Q(q**2)*E2)
check('row -1 first equation',offaxis_row_residual(-1,-2)==-Q(q**4)*E3)
check('row -1 second equation',offaxis_row_residual(-1,-3)==-Q(q**2)*E4)
# Obtain every h3 from the actual b=+/-2 outer coefficient, independently of
# the compact axis equations later checked below.
for dd in (1,-1):
    for e in (1,-1):
        aa=e%5
        residue=Q(f(aa,2*dd))-sum((h[ee,dd,2]*local_coefficient(ee,dd,a,2,aa) for ee,ddd,a in orient if ddd==dd),L(0))
        a=next(a for ee,ddd,a in orient if ee==e and ddd==dd)
        opposite=next(a for ee,ddd,a in orient if ee==e and ddd==-dd)
        h[e,-dd,3]=residue/local_coefficient(e,-dd,opposite,3,aa)
        check(f'forced h3 ({e},{-dd})',h[e,-dd,3]==-(1+Q(d)/a)/opposite)
axis_plus=Q(q**2)*(x**-2+y**-2)-u**-1-v**-1-Q(d)*(x**-1*v**-1+y**-1*u**-1)-Q(q)
axis_minus=Q(q**2)*(u**-2+v**-2)-x**-1-y**-1-Q(d)*(x**-1*v**-1+y**-1*u**-1)-Q(q)
for dd,expected in [(1,axis_plus),(-1,axis_minus)]:
    actual=sum((h[e,dd,2]+h[e,-dd,3] for e in (1,-1)),L(0))-Q(f(0,2*dd))
    check(f'full coefficient axis (0,{2*dd%5})',actual==expected)
check('row pair type factorization',E1-E2==(x-y)*(1+Q(c)*(x+y)))
A=lambda a,b:Q(q**2)*(a**-2+b**-2)+a**-1+b**-1
check('axis subtraction has no coupling term',axis_plus-axis_minus==A(x,y)-A(u,v))
check('type separation identity',A(x,y)-Q(2*c)+(x+y)*(x-y)**2*x**-2*y**-2==E2*x**-2+E1*y**-2)
# Nondiagonal pairs have fixed sum s and product p.
s=-1/c;p=1/c**2-q**2/c;disc=s*s-4*p
check('nondiagonal sum polynomial',s==q**3+q**2)
check('nondiagonal product polynomial',p==1-q-2*q**2-2*q**3)
check('nondiagonal discriminant polynomial',disc==-3+4*q+7*q**2+7*q**3)
check('nondiagonal sum and product nonzero',s!=0 and p!=0)
check('nondiagonal discriminant nonzero',disc!=0)
check('fixed sum and product solve summed row equation',s-c*(s*s-2*p)+2*q**2==0)
# Both pairs diagonal, x=y=t and u=v=w. They obey B(z)=0, with
# B(z)=c z^2-z-q^2; the shared axis condition is D(t,w)=0.
t=x;w=y
B=lambda z:Q(c)*z*z-z-Q(q**2)
D=lambda a,b:Q(2*c-q)*a*b-2*(a+b)-Q(2*d)
check('diagonal axis denominator identity',axis_plus.substitute([t,t,w,w])*t*w==D(t,w)-2*w/t*B(t))
# If t != w, the quadratic gives t+w=1/c and tw=-q^2/c.
R_distinct=-(2*c-q)*q**2-2-2*c*d
check('distinct diagonal residual value',R_distinct==-2-2*q+2*q**2-q**3)
check('distinct diagonal residual nonzero',R_distinct!=0)
# If t=w, eliminate between B(t) and D(t,t) with a polynomial Bezout identity.
a=2*c-q
l1=2*q**3+2*q**2-q+2;l0=q**3+2*q**2+2*q
lin=Q(l1)*t+Q(l0)
check('equal diagonal linear elimination',Q(c)*D(t,t)-Q(a)*B(t)==lin)
R_equal=c*l0*l0+l0*l1-q**2*l1*l1
check('equal diagonal Bezout certificate',Q(l1*l1)*B(t)-(Q(c*l1)*t-Q(c*l0+l1))*lin==Q(R_equal))
check('equal diagonal residual value',R_equal==1+4*q-11*q**2+6*q**3)
check('equal diagonal residual nonzero',R_equal!=0)
# For two nondiagonal pairs: (u,v)=(x,y) or (u,v)=(y,x).
sumxy=x+y;prodxy=x*y
S_same=Q(q**2)*(sumxy**2-2*prodxy)-sumxy*prodxy-Q(2*d)*prodxy-Q(q)*prodxy**2
S_swapped=Q(q**2)*(sumxy**2-2*prodxy)-sumxy*prodxy-Q(d)*(sumxy**2-2*prodxy)-Q(q)*prodxy**2
check('same-order nondiagonal axis scaling',axis_plus.substitute([x,y,x,y])*x**2*y**2==S_same)
check('swapped nondiagonal axis scaling',axis_plus.substitute([x,y,y,x])*x**2*y**2==S_swapped)
R_same=q**2*(s*s-2*p)-s*p-2*d*p-q*p*p
R_swapped=q**2*(s*s-2*p)-s*p-d*(s*s-2*p)-q*p*p
check('same ordered nondiagonal residual value',R_same==-5-5*q+5*q**3)
check('same ordered nondiagonal residual nonzero',R_same!=0)
check('swapped nondiagonal residual value',R_swapped==-9-19*q-17*q**2-5*q**3)
check('swapped nondiagonal residual nonzero',R_swapped!=0)
# Eisenstein at 5 for Phi5(z+1), documenting why a nonzero degree<4
# rational polynomial cannot vanish at any primitive complex fifth root.
shift=[sum(comb(j,i) for j in range(i,5)) for i in range(5)]
check('Phi5 shifted Eisenstein coefficients',shift==[5,10,10,5,1])
check('Eisenstein divisibility at 5',all(a%5==0 for a in shift[:-1]) and shift[0]%25!=0 and shift[-1]%5!=0)
print(json.dumps({
    'result':'PASS: no four-bank Fourier representation at N=5 over characteristic zero',
    'arithmetic':'Exact rational arithmetic in Q[q]/Phi5, standard Python library only',
    'checks_passed':len(checks),
    'checks':checks,
    'nonzero_certificates_basis_1_q_q2_q3':{
        'diagonal_distinct':R_distinct.vector(),
        'diagonal_equal':R_equal.vector(),
        'nondiagonal_same_order':R_same.vector(),
        'nondiagonal_swapped_order':R_swapped.vector()
    },
    'scope':'All four alpha parameters may be arbitrary nonzero complex numbers; amplitudes are freely relaxed. The obstruction uses actual (0,+/-2) coefficients in addition to necessary row equations. No finite-field lift, raw-weight sufficiency claim, or runtime claim is made.'
},indent=2))
