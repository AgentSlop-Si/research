#!/usr/bin/env python3
"""Fresh standalone exact checker. Standard library only. Never imports source artifacts."""
from fractions import Fraction as Q
from pathlib import Path
import argparse, json, hashlib, math

# Independent fixed-degree field implementation. Inversion uses elimination.
class K:
    def __init__(self, value=0):
        if isinstance(value,K): self.c=value.c; return
        c=list(value) if isinstance(value,(list,tuple)) else [value]
        c=[Q(x) for x in c]+[Q(0)]*max(0,4-len(c))
        for j in range(len(c)-1,3,-1):
            for k in range(1,5): c[j-k]-=c[j]
        self.c=tuple(c[:4])
    def __add__(self,v):
        if isinstance(v,E):return NotImplemented
        v=K(v); return K([a+b for a,b in zip(self.c,v.c)])
    __radd__=__add__
    def __neg__(self):return K([-x for x in self.c])
    def __sub__(self,v):
        if isinstance(v,E):return NotImplemented
        return self+-K(v)
    def __rsub__(self,v):return K(v)+-self
    def __mul__(self,v):
        if isinstance(v,E):return NotImplemented
        v=K(v); r=[Q(0)]*7
        for i in range(4):
            for j in range(4):r[i+j]+=self.c[i]*v.c[j]
        return K(r)
    __rmul__=__mul__
    def inv(self):
        cols=[(self*K([0]*j+[1])).c for j in range(4)]
        a=[[cols[j][i] for j in range(4)]+[Q(i==0)] for i in range(4)]
        for j in range(4):
            p=next((i for i in range(j,4) if a[i][j]),None)
            if p is None:raise ZeroDivisionError('nonunit cyclotomic element')
            a[j],a[p]=a[p],a[j]
            v=a[j][j];a[j]=[x/v for x in a[j]]
            for i in range(4):
                if i!=j:
                    v=a[i][j];a[i]=[x-v*y for x,y in zip(a[i],a[j])]
        return K([a[i][4] for i in range(4)])
    def __truediv__(self,v):
        if isinstance(v,E):return NotImplemented
        return self*K(v).inv()
    def __rtruediv__(self,v):return K(v)*self.inv()
    def __eq__(self,v):
        if isinstance(v,E):return NotImplemented
        return self.c==K(v).c
    def __bool__(self):return any(self.c)
    def __pow__(self,n):
        if n<0:return self.inv()**(-n)
        out=K(1);base=self
        while n:
            if n&1:out=out*base
            base=base*base;n//=2
        return out
    def residue(self):
        return sum((x.numerator*pow(x.denominator,-1,241)%241)*pow(91,i,241) for i,x in enumerate(self.c))%241
    def data(self):return [str(x) for x in self.c]

class E:
    p0=K(0);p1=K(0)
    def __init__(self,a=0,b=0):
        if isinstance(a,E):self.a,self.b=a.a,a.b
        else:self.a,self.b=K(a),K(b)
    def __add__(self,v):
        v=E(v);return E(self.a+v.a,self.b+v.b)
    __radd__=__add__
    def __neg__(self):return E(-self.a,-self.b)
    def __sub__(self,v):return self+-E(v)
    def __rsub__(self,v):return E(v)+-self
    def __mul__(self,v):
        v=E(v)
        return E(self.a*v.a-self.p0*self.b*v.b,self.a*v.b+self.b*v.a-self.p1*self.b*v.b)
    __rmul__=__mul__
    def conj(self):return E(self.a-self.p1*self.b,-self.b)
    def norm(self):return self.a*self.a-self.p1*self.a*self.b+self.p0*self.b*self.b
    def inv(self):
        c=self.conj();n=self.norm();return E(c.a/n,c.b/n)
    def __truediv__(self,v):return self*E(v).inv()
    def __rtruediv__(self,v):return E(v)*self.inv()
    def __eq__(self,v):
        v=E(v);return self.a==v.a and self.b==v.b
    def __bool__(self):return bool(self.a) or bool(self.b)
    def __pow__(self,n):
        if n<0:return self.inv()**(-n)
        out=E(1);base=self
        while n:
            if n&1:out=out*base
            base=base*base;n//=2
        return out
    def data(self):return {'constant':self.a.data(),'root':self.b.data()}

# Sparse integer multivariate polynomials: alpha,beta,gamma,epsilon,d.
class P:
    dim=5
    def __init__(self,v=0):self.t=dict(v) if isinstance(v,dict) else ({(0,)*self.dim:int(v)} if v else {})
    def __add__(self,v):
        v=v if isinstance(v,P) else P(v);r=dict(self.t)
        for m,c in v.t.items():r[m]=r.get(m,0)+c
        return P({m:c for m,c in r.items() if c})
    __radd__=__add__
    def __neg__(self):return P({m:-c for m,c in self.t.items()})
    def __sub__(self,v):return self+-(v if isinstance(v,P) else P(v))
    def __rsub__(self,v):return P(v)+-self
    def __mul__(self,v):
        v=v if isinstance(v,P) else P(v);r={}
        for m,c in self.t.items():
            for n,b in v.t.items():
                k=tuple(x+y for x,y in zip(m,n));r[k]=r.get(k,0)+c*b
        return P({m:c for m,c in r.items() if c})
    __rmul__=__mul__
    def __pow__(self,n):
        r=P(1)
        for _ in range(n):r=r*self
        return r
    def __eq__(self,v):return self.t==(v.t if isinstance(v,P) else P(v).t)

def symbolic_checks():
    vs=[P({tuple(int(j==i) for j in range(5)):1}) for i in range(5)]
    a,b,g,e,d=vs
    L=b*b-g*e;M=-2*a*b+a*g+a*e+b*g+b*e-2*g*e;C=(b-g)**2
    poly=L*d*d+M*d+C
    residual=(b-g)*(b*d*d+(b-a)*d+b-g)-(e-b)*d*(g*d+2*g-a-b)
    assert residual==poly
    # Norm of t's numerator and denominator agree over the quadratic.
    s=a+b
    numerator=C*(g*g*L-g*s*M+s*s*C)
    denominator=g*g*C*L-g*(2*g-s)*M*L+(2*g-s)**2*L*L
    assert numerator==denominator
    # Cubic Fourier recovery: (1-z) Q(z) = 1 - [z^3-c(1-z)^3].
    z,c=vs[:2]
    assert (1-z)*((1+c)*z*z+(1-2*c)*z+1+c)==1-(z**3-c*(1-z)**3)
    return {'synthesis_remaining_equation_identity':True,'reciprocal_pole_norm_identity':True,'fourier_cubic_recovery_identity':True}

def matrix_multiply(A,B):
    return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]

def synthesize(q,save_full=False):
    eta=K([0,1]);g=1+2*(eta**2+eta**3)
    assert eta**5==1 and eta!=1 and g*g==5
    den=1+5*q**3*g
    assert den*(1-5*q**3*g)==1-125*q**6
    B=[[(eta**(i*j)-q*g*eta**(-3*(i+j)**2)+(5*q**3*g*eta**(-3*i*i) if i==j else 0))/den for j in range(5)] for i in range(5)]
    for i in range(5):
        for j in range(5):
            assert B[i][j]==B[j][i]
            assert B[i][j]==B[(-i)%5][(-j)%5]
    a,b,c,e,f,h=B[0][1],B[0][2],B[1][2],B[1][3],B[1][4],B[2][3]
    al,be,ga,ep=c/(a*b),e/(a*b),f/(a*a),h/(b*b)
    p2=be*be-ga*ep
    E.p1=(-2*al*be+al*ga+al*ep+be*ga+be*ep-2*ga*ep)/p2
    E.p0=(be-ga)**2/p2
    disc=E.p1*E.p1-4*E.p0
    d=E(0,1);assert d*d+E.p1*d+E.p0==0
    tden=E(ga)*(d+2)-al-be
    t=(E(ga)*d+E(al+be)*d*d)/tden
    kap=(t+d*d)/ga
    x=(t-d)/kap
    r=[None,x,(al-x)/d,(be-x)/d,(ga-x)/d]
    z=kap/(1+t)
    u=[E(1)]+[B[0][i]*r[i] for i in range(1,5)]
    v=[z/t]+[B[0][i]-z*u[i] for i in range(1,5)]
    diagonal=[B[i][i]-(1+t)*u[i]*v[i] for i in range(5)]
    assert t.norm()==1 and t.conj()==1/t
    guards={'a':a,'b':b,'gamma':ga,'beta_minus_gamma':be-ga,'polynomial_leading':p2,'discriminant':disc,'d_norm':d.norm(),'t_denominator_norm':tden.norm(),'kappa_norm':kap.norm(),'t_norm':t.norm(),'one_plus_t_norm':(1+t).norm(),'one_minus_t_norm':(1-t).norm()}
    for name,arr in [('u',u),('v',v),('diagonal',diagonal)]:
        for i,value in enumerate(arr):guards[name+str(i)+'_norm']=value.norm()
    assert len(guards)==27 and all(guards.values())
    residues={name:x.residue() for name,x in guards.items()}
    assert all(residues.values())
    target_residues=[[x.residue() for x in row] for row in B]
    expected=[[161,20,102,102,20],[20,182,62,26,92],[102,62,236,28,26],[102,26,28,236,62],[20,92,26,62,182]]
    assert target_residues==expected
    assert den.residue()==34 and E.p1.residue()==30 and E.p0.residue()==124
    assert disc.residue()==163 and pow(163,120,241)==240
    for i in range(5):
        for j in range(i+1,5):assert u[i]*v[j]+t*v[i]*u[j]==B[i][j]
    # Independently form both Green operators from powers of their weighted cycles.
    identity=[[E(int(i==j)) for j in range(5)] for i in range(5)]
    greens=[]
    for pole in [t,1/t]:
        W=[[E(0) for _ in range(5)] for _ in range(5)]
        for i in range(5):W[i][(i+1)%5]=pole if i==4 else E(1)
        power=identity;total=[[E(0) for _ in range(5)] for _ in range(5)]
        for k in range(5):
            total=[[total[i][j]+power[i][j] for j in range(5)] for i in range(5)]
            power=matrix_multiply(power,W)
        assert all(power[i][j]==pole*identity[i][j] for i in range(5) for j in range(5))
        G=[[total[i][j]/(1-pole) for j in range(5)] for i in range(5)]
        inverse=[[identity[i][j]-W[i][j] for j in range(5)] for i in range(5)]
        assert matrix_multiply(inverse,G)==identity and matrix_multiply(G,inverse)==identity
        greens.append(G)
    for i in range(5):
        for j in range(5):
            result=(1-t)*u[i]*greens[0][i][j]*v[j]+(t-1)*v[i]*greens[1][i][j]*u[j]+(diagonal[i] if i==j else 0)
            assert result==B[i][j] and result.conj()==B[i][j]
    # Apply actual cyclic scans to two dense vectors and all five basis vectors.
    def solve(pole,inp):
        out=[E(0)]*5;out[0]=sum(inp)/(1-pole)
        out[4]=inp[4]+pole*out[0]
        for i in range(3,0,-1):out[i]=inp[i]+out[i+1]
        for i in range(5):assert out[i]-(pole if i==4 else 1)*out[(i+1)%5]==inp[i]
        return out
    inputs=[[int(i==j) for i in range(5)] for j in range(5)]+[[1,2,3,4,5],[2,-1,0,3,-2]]
    for inp in inputs:
        y=solve(t,[v[i]*inp[i] for i in range(5)])
        z=solve(1/t,[u[i]*inp[i] for i in range(5)])
        output=[(1-t)*u[i]*y[i]+(t-1)*v[i]*z[i]+diagonal[i]*inp[i] for i in range(5)]
        assert output==[sum(B[i][j]*inp[j] for j in range(5)) for i in range(5)]
    data={'q':q,'physical_N':5*q*q,'denominator_residue':den.residue(),'quadratic_residues':[E.p0.residue(),E.p1.residue(),1],'guard_residues':residues,'all_27_guards_nonzero':True,'all_25_factor_entries_checked':True,'both_roots_checked':True,'all_100_inverse_entries_checked':True,'scan_entries_checked':35,'pole_norm':t.norm().data()}
    if save_full:
        data.update({'target':[[x.data() for x in row] for row in B],'quadratic_constant':E.p0.data(),'quadratic_linear':E.p1.data(),'t':t.data(),'u':[x.data() for x in u],'v':[x.data() for x in v],'diagonal_correction':[x.data() for x in diagonal],'guard_norms':{name:x.data() for name,x in guards.items()}})
    return data

def congruence_check():
    # Polynomial arithmetic over F241 verifies q=1+241k universally, not by sampling k.
    def add(a,b):
        r=[((a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0))%241 for i in range(max(len(a),len(b)))];
        while len(r)>1 and r[-1]==0:r.pop()
        return r
    def mul(a,b):
        r=[0]*(len(a)+len(b)-1)
        for i,x in enumerate(a):
            for j,y in enumerate(b):r[i+j]=(r[i+j]+x*y)%241
        return add(r,[0])
    q=add([1,241],[0]);q3=mul(mul(q,q),q)
    assert q==[1] and q3==[1]
    g=(1+2*(pow(91,2,241)+pow(91,3,241)))%241
    assert g==103 and add([1],mul([5*g],q3))==[34]
    for i in range(5):
        for j in range(5):
            numerator=add([pow(91,i*j,241)],mul([-g*pow(91,(-3*(i+j)**2)%5,241)],q))
            if i==j:numerator=add(numerator,mul([5*g*pow(91,(-3*i*i)%5,241)],q3))
            assert len(numerator)==1
    return {'polynomial_substitution_q_equals_1_plus_241k':True,'target_denominator_constant':34,'all_25_target_entries_constant':True}

def bluestein_checks():
    def prime(p):return p>=2 and all(p%d for d in range(2,math.isqrt(p)+1))
    def factors(n):
        out=[];d=2
        while d*d<=n:
            if n%d==0:
                out.append(d)
                while n%d==0:n//=d
            d+=1
        if n>1:out.append(n)
        return out
    def dft(x,root,p):
        return [sum(x[j]*pow(root,i*j,p) for j in range(len(x)))%p for i in range(len(x))]
    cases=[]
    for n in range(2,13):
        m=2*n-1;period=math.lcm(2*n,m);p=period+1
        while not prime(p):p+=period
        fac=factors(p-1)
        gen=next(g for g in range(2,p) if all(pow(g,(p-1)//r,p)!=1 for r in fac))
        theta=pow(gen,(p-1)//(2*n),p);omega=theta*theta%p;root=pow(gen,(p-1)//m,p)
        x=[(j*j+3*j+2)%p for j in range(n)]
        a=[x[j]*pow(theta,j*j,p)%p if j<n else 0 for j in range(m)]
        b=[0]*m
        for ell in range(-(n-1),n):b[ell%m]=pow(theta,(-ell*ell)%(2*n),p)
        fa,fb=dft(a,root,p),dft(b,root,p)
        product=[y*z%p for y,z in zip(fa,fb)]
        forward=dft(product,root,p)
        conv=[forward[(-i)%m]*pow(m,-1,p)%p for i in range(m)]
        output=[pow(theta,i*i,p)*conv[i]%p for i in range(n)]
        assert output==dft(x,omega,p)
        cases.append({'n':n,'padded_m':m,'prime':p,'verified_outputs':n})
    grid=[]
    for n in [1,2,3,4,10,100,10**6,10**9,10**12,10**30]:
        target=2*n-1;r=math.isqrt((target+4)//5)
        while 5*r*r<target:r+=1
        k=max(0,(r-1+2409)//2410);q=1+2410*k;m=5*q*q
        assert m>=target and (k==0 or 5*(q-2410)**2<target)
        assert m<target+4820*(math.isqrt(5*target)+1)+5*2410**2
        grid.append({'n':n,'q':q,'m':m,'minimal_grid_choice':True})
    return {'exact_convolution_controls':cases,'supported_length_padding_controls':grid}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out-dir',default=str(Path(__file__).resolve().parent));parser.add_argument('--q',type=int,action='append');args=parser.parse_args()
    qs=args.q or [1,483,1447,1929,2411]
    for q in qs:assert q>0 and q%2==1 and q%5 and q%241==1
    result={'status':'PASS','symbolic_identities':symbolic_checks(),'universal_congruence':congruence_check(),'all_length_reduction_controls':bluestein_checks(),'instances':[synthesize(q,save_full=(q in [1,483])) for q in qs]}
    first=result['instances'][0]['guard_residues']
    assert all(x['guard_residues']==first for x in result['instances'])
    output=Path(args.out_dir);output.mkdir(parents=True,exist_ok=True)
    path=output/'EXACT_EXTENSION_RESULTS.json';path.write_text(json.dumps(result,indent=2)+'\n')
    print('PASS: symbolic synthesis, pole reciprocity, cubic recovery, universal congruence; exact instances',qs)
    print('PASS: 27 common nonzero guard residues; full factorization, both roots, Green inverses, and scans per instance')
    print('PASS: 11 exact Bluestein convolution controls and 10 supported-length padding controls')
    print('result_sha256',hashlib.sha256(path.read_bytes()).hexdigest())
if __name__=='__main__':main()
