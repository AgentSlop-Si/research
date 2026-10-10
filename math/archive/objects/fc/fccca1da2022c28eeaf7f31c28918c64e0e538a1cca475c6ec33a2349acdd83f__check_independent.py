#!/usr/bin/env python3
"""Independent exact B5 construction audit. Standard library; no source imports."""
from fractions import Fraction as Q
import json, random
from pathlib import Path

def solve(A,b):
    n=len(b); a=[list(A[i])+[b[i]] for i in range(n)]
    for j in range(n):
        k=next(k for k in range(j,n) if a[k][j]); a[k],a[j]=a[j],a[k]
        t=a[j][j]; a[j]=[x/t for x in a[j]]
        for k in range(n):
            if k!=j:
                t=a[k][j]; a[k]=[x-t*y for x,y in zip(a[k],a[j])]
    return [r[-1] for r in a]

class K:
    def __init__(self,x=0):
        self.a=x.a if isinstance(x,K) else tuple(Q(v) for v in ((list(x)+[0]*4)[:4] if isinstance(x,(tuple,list)) else [x,0,0,0]))
    def __bool__(self): return any(self.a)
    def __eq__(self,o): return self.a==K(o).a
    def __add__(self,o): return K([x+y for x,y in zip(self.a,K(o).a)])
    __radd__=__add__
    def __neg__(self): return K([-x for x in self.a])
    def __sub__(self,o): return self+-K(o)
    def __rsub__(self,o): return K(o)+-self
    def __mul__(self,o):
        b=K(o).a; c=[Q(0)]*7
        for i,x in enumerate(self.a):
            for j,y in enumerate(b): c[i+j]+=x*y
        for i in range(6,3,-1):
            for j in range(i-4,i): c[j]-=c[i]
        return K(c[:4])
    __rmul__=__mul__
    def inv(self):
        assert self
        cols=[(self*K([0]*j+[1])).a for j in range(4)]
        return K(solve(list(zip(*cols)),[Q(1),Q(0),Q(0),Q(0)]))
    def __truediv__(self,o): return self*K(o).inv()
    def __rtruediv__(self,o): return K(o)*self.inv()
    def __pow__(self,n):
        if n<0:return self.inv()**(-n)
        a=self; b=K(1)
        while n:
            if n&1:b=b*a
            a=a*a;n//=2
        return b
    def data(self):return [str(x) for x in self.a]
    def mod(self,p=241,z=91):return sum((x.numerator*pow(x.denominator,-1,p)%p)*pow(z,j,p) for j,x in enumerate(self.a))%p

Z=K([0,1]); G=1+2*Z**2+2*Z**3
assert Z**5==1 and sum(Z**i for i in range(5))==0 and G*G==5
B=[[ (Z**(i*j)-G*Z**(-3*(i+j)**2)+(5*G*Z**(-3*i*i) if i==j else 0))/(1+5*G) for j in range(5)] for i in range(5)]
Qmat=[[Z**(-i*j)/5+(Z**(3*i*i) if i==j else 0) for j in range(5)] for i in range(5)]
def mm(A,B):return [[sum(x*y for x,y in zip(r,c)) for c in zip(*B)] for r in A]
def isid(A):return all(x==(i==j) for i,r in enumerate(A) for j,x in enumerate(r))
assert isid(mm(B,Qmat)) and isid(mm(Qmat,B))
a,b,c,e,f,h=B[0][1],B[0][2],B[1][2],B[1][3],B[1][4],B[2][3]
al,be,ga,ep=c/(a*b),e/(a*b),f/(a*a),h/(b*b)
lead=be*be-ga*ep
p1=(-2*al*be+al*ga+al*ep+be*ga+be*ep-2*ga*ep)/lead
p0=(be-ga)**2/lead
assert p1==K([-326,-3932,-2918,-714])/781
assert p0==K([-7096,672,5728,10576])/8591
disc=p1*p1-4*p0
assert disc and p1.mod()==30 and p0.mod()==124 and disc.mod()==163
assert pow(163,120,241)==240

class E:
    def __init__(self,a=0,b=0):self.a,self.b=(a.a,a.b) if isinstance(a,E) else (K(a),K(b))
    def __bool__(self):return bool(self.a) or bool(self.b)
    def __eq__(self,o):o=E(o);return self.a==o.a and self.b==o.b
    def __add__(self,o):o=E(o);return E(self.a+o.a,self.b+o.b)
    __radd__=__add__
    def __neg__(self):return E(-self.a,-self.b)
    def __sub__(self,o):return self+-E(o)
    def __rsub__(self,o):return E(o)+-self
    def __mul__(self,o):
        o=E(o);v=self.b*o.b
        return E(self.a*o.a-p0*v,self.a*o.b+self.b*o.a-p1*v)
    __rmul__=__mul__
    def conj(self):return E(self.a-p1*self.b,-self.b)
    def norm(self):return self.a*self.a-p1*self.a*self.b+p0*self.b*self.b
    def inv(self):
        n=self.norm();assert n
        c=self.conj();return E(c.a/n,c.b/n)
    def __truediv__(self,o):return self*E(o).inv()
    def __rtruediv__(self,o):return E(o)*self.inv()
    def __pow__(self,n):
        if n<0:return self.inv()**(-n)
        a=self;b=E(1)
        while n:
            if n&1:b=b*a
            a=a*a;n//=2
        return b
    def data(self):return [self.a.data(),self.b.data()]

d=E(0,1)
den=E(ga)*(d+2)-al-be
t=(E(ga)*d+E(al+be)*d*d)/den
kap=(t+d*d)/ga
x=(t-d)/kap
r=[x,(E(al)-x)/d,(E(be)-x)/d,(E(ga)-x)/d]
z=kap/(1+t)
u=[E(1)]+[E(B[0][i])*r[i-1] for i in range(1,5)]
v=[z/t]+[E(B[0][i])-z*u[i] for i in range(1,5)]
di=[E(B[i][i])-(1+t)*u[i]*v[i] for i in range(5)]
assert t==E(1)+E(K([-49,36,65,-87])/44)*d
assert t.norm()==1 and t.conj()==1/t
assert t*t+E(K([13996,58170,-73235,-211995])/17182)*t+1==0
assert kap*r[3]==1+d
assert all(E(B[i][j])==u[i]*v[j]+t*v[i]*u[j] for i in range(5) for j in range(i+1,5))

guards={k:E(val) for k,val in {'a':a,'b':b,'gamma':ga,'beta_minus_gamma':be-ga,'leading':lead,'disc':disc,'d':d,'denominator_t':den,'kappa':kap,'t':t,'1+t':1+t,'1-t':1-t}.items()}
guards.update({f'{name}{i}':val for name,vals in [('u',u),('v',v),('diagonal',di)] for i,val in enumerate(vals)})
for name,val in guards.items():assert val.norm(),name
assert all(val.norm().mod()!=0 for val in guards.values())

Id=[[E(int(i==j)) for j in range(5)] for i in range(5)]
actual=[]; inverse_checks=0
for pole in [t,1/t]:
    W=[[E(0) for j in range(5)] for i in range(5)]
    for i in range(5):W[i][(i+1)%5]=E(1) if i<4 else pole
    ImW=[[Id[i][j]-W[i][j] for j in range(5)] for i in range(5)]
    # Rebuild Green by finite geometric series, not by the claimed triangular kernel.
    power=Id; geo=[[E(0) for j in range(5)] for i in range(5)]
    for k in range(5):
        geo=[[geo[i][j]+power[i][j] for j in range(5)] for i in range(5)]
        power=mm(power,W)
    assert all(power[i][j]==pole*Id[i][j] for i in range(5) for j in range(5))
    green=[[geo[i][j]/(1-pole) for j in range(5)] for i in range(5)]
    assert isid(mm(ImW,green)) and isid(mm(green,ImW));inverse_checks+=50
    actual.append(green)
rec=[[(1-t)*u[i]*actual[0][i][j]*v[j]+(t-1)*v[i]*actual[1][i][j]*u[j]+(di[i] if i==j else 0) for j in range(5)] for i in range(5)]
assert all(rec[i][j]==B[i][j] for i in range(5) for j in range(5))
assert all(rec[i][j].conj()==B[i][j] for i in range(5) for j in range(5))

# Separate generic finite-field synthesis controls, unrelated to the chirp input.
rng=random.Random(3105); cases=0; p=101
iv=lambda x:pow(x%p,-1,p)
for trial in range(400):
    aa,bb,cc,ee,ff,hh=[rng.randrange(1,p) for _ in range(6)]
    A=cc*iv(aa*bb)%p; Bc=ee*iv(aa*bb)%p; C=ff*iv(aa*aa)%p; D=hh*iv(bb*bb)%p
    l=(Bc*Bc-C*D)%p; m=(-2*A*Bc+A*C+A*D+Bc*C+Bc*D-2*C*D)%p;n=(Bc-C)**2%p
    for dd in range(1,p):
        if (l*dd*dd+m*dd+n)%p:continue
        den0=(C*(dd+2)-A-Bc)%p
        if not den0 or not(Bc-C)%p:continue
        tt=(C*dd+(A+Bc)*dd*dd)*iv(den0)%p
        kk=(tt+dd*dd)*iv(C)%p
        if not kk or tt in (0,1,p-1):continue
        xx=(tt-dd)*iv(kk)%p;rr=[xx,(A-xx)*iv(dd)%p,(Bc-xx)*iv(dd)%p,(C-xx)*iv(dd)%p]
        zz=kk*iv(1+tt)%p;top=[aa,bb,bb,aa]
        uu=[1]+[top[i]*rr[i]%p for i in range(4)]
        vv=[zz*iv(tt)%p]+[(top[i]-zz*uu[i+1])%p for i in range(4)]
        want={(0,1):aa,(0,2):bb,(0,3):bb,(0,4):aa,(1,2):cc,(1,3):ee,(1,4):ff,(2,3):hh,(2,4):ee,(3,4):cc}
        assert all((uu[i]*vv[j]+tt*vv[i]*uu[j])%p==v0 for (i,j),v0 in want.items())
        cases+=1

result={'status':'PASS','target_inverse_entries':50,'green_inverse_entries':inverse_checks,'reconstructed_entries':25,'conjugate_entries':25,'upper_entries':10,'generic_synthesis_controls':cases,'generic_synthesis_entries':10*cases,'minimal_terms':3,'minimality_scope':'fixed N5 chirp, Hamiltonian row cycles, arbitrary diagonal endpoints and zero edges allowed; lower bound inherited from separately sealed all-order audit','p1':p1.data(),'p0':p0.data(),'discriminant':disc.data(),'finite_reduction':{'p':241,'zeta':91,'p1':30,'p0':124,'disc':163,'Euler':240},'target':[[x.data() for x in row] for row in B],'normalized_constants':{k:x.data() for k,x in [('alpha',al),('beta',be),('gamma',ga),('epsilon',ep)]},'pole':t.data(),'u':[x.data() for x in u],'v':[x.data() for x in v],'diagonal':[x.data() for x in di],'guard_norms':{k:x.norm().data() for k,x in guards.items()},'guard_norms_mod241':{k:x.norm().mod() for k,x in guards.items()}}
Path('INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:result[k] for k in ['status','target_inverse_entries','green_inverse_entries','reconstructed_entries','conjugate_entries','generic_synthesis_controls','minimal_terms']},sort_keys=True))
