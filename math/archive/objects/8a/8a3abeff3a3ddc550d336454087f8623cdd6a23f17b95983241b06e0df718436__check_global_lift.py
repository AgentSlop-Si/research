#!/usr/bin/env python3
"""Fresh standard-library checker. Imports no predecessor or exploratory code."""
from fractions import Fraction as Q
from pathlib import Path
import json, math, time
OUT=Path(__file__).resolve().parent

class Field:
    def __init__(self,mod): self.mod=tuple(map(Q,mod)); self.n=len(mod)-1
    def __call__(self,a=0):
        if isinstance(a,Elt):
            assert a.f is self; return a
        if isinstance(a,(int,Q)): a=[a]
        a=list(map(Q,a))+[Q(0)]*self.n
        for k in range(len(a)-1,self.n-1,-1):
            c=a[k]
            for j in range(self.n): a[k-self.n+j]-=c*self.mod[j]
        return Elt(self,tuple(a[:self.n]))
class Elt:
    def __init__(self,f,a):self.f=f;self.a=a
    def __add__(self,b):
        b=self.f(b);return Elt(self.f,tuple(x+y for x,y in zip(self.a,b.a)))
    __radd__=__add__
    def __neg__(self):return Elt(self.f,tuple(-x for x in self.a))
    def __sub__(self,b):return self+-self.f(b)
    def __rsub__(self,b):return self.f(b)+-self
    def __mul__(self,b):
        b=self.f(b);a=[Q(0)]*(2*self.f.n-1)
        for i,x in enumerate(self.a):
            if x:
                for j,y in enumerate(b.a):
                    if y:a[i+j]+=x*y
        return self.f(a)
    __rmul__=__mul__
    def inv(self):
        assert self
        n=self.f.n; cols=[(self*self.f([0]*j+[1])).a for j in range(n)]
        a=[[cols[j][i] for j in range(n)]+[Q(i==0)] for i in range(n)]
        for k in range(n):
            h=next(i for i in range(k,n) if a[i][k]);a[k],a[h]=a[h],a[k]
            d=a[k][k];a[k]=[x/d for x in a[k]]
            for i in range(n):
                if i!=k:
                    d=a[i][k]
                    if d:a[i]=[x-d*y for x,y in zip(a[i],a[k])]
        return self.f([a[i][-1] for i in range(n)])
    def __truediv__(self,b):return self*self.f(b).inv()
    def __rtruediv__(self,b):return self.f(b)*self.inv()
    def __pow__(self,n):
        if n<0:return self.inv()**(-n)
        x=self;y=self.f(1)
        while n:
            if n&1:y=y*x
            x=x*x;n//=2
        return y
    def __bool__(self):return any(self.a)
    def __eq__(self,b):
        try:return self.a==self.f(b).a
        except (TypeError,AssertionError):return False
    def data(self):return [str(x) for x in self.a]

def trim(a):
    a=list(a)
    while len(a)>1 and not a[-1]:a.pop()
    return a

def add(a,b):
    z=a[0]*0;return trim([(a[i] if i<len(a) else z)+(b[i] if i<len(b) else z) for i in range(max(len(a),len(b)))])
def neg(a):return [-x for x in a]
def sub(a,b):return add(a,neg(b))
def scale(a,s):return trim([x*s for x in a])
def mul(a,b):
    c=[a[0]*0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]=c[i+j]+x*y
    return trim(c)
def pw(a,n):
    b=[a[0]*0+1]
    while n:
        if n&1:b=mul(a,b)
        a=mul(a,a);n//=2
    return b
def divmodp(a,b):
    a=trim(a);b=trim(b);assert any(b);z=a[0]*0;q=[z]*max(1,len(a)-len(b)+1);inv=1/b[-1]
    while any(a) and len(a)>=len(b):
        k=len(a)-len(b);v=a[-1]*inv;q[k]=v
        a=sub(a,[z]*k+scale(b,v))
    return trim(q),a
def gcdp(a,b):
    while any(b):a,b=b,divmodp(a,b)[1]
    return scale(a,1/a[-1])
def derivative(a):return trim([i*a[i] for i in range(1,len(a))] or [a[0]*0])
def exactq(a,b):
    q,r=divmodp(a,b);assert not any(r);return q
def evalp(a,x):
    y=x*0
    for c in reversed(a):y=y*x+c
    return y

def build_polynomials(K):
    z=K([0,1]);a=[K(1),z**2];b=[K(1),z**3];c=[z**2,z**3];e=[z**3,z**2];f=[z**4,K(1)];h=[z,K(1)]
    A=mul(mul(c,a),b);B=mul(mul(e,a),b);C=mul(f,pw(b,2));E=mul(h,pw(a,2));S=add(A,B);U=sub(scale(C,2),S)
    L=sub(pw(B,2),mul(C,E));M=add(add(add(add(scale(mul(A,B),-2),mul(A,C)),mul(A,E)),mul(B,C)),sub(mul(B,E),scale(mul(C,E),2)));J=pw(sub(B,C),2)
    RT=add(sub(mul(L,pw(U,2)),mul(mul(M,U),C)),mul(J,pw(C,2)))
    N=add(sub(scale(mul(mul(mul(S,J),U),L),-2),mul(M,add(scale(mul(mul(S,J),C),-1),mul(sub(mul(C,L),mul(S,M)),U)))),scale(mul(mul(J,sub(mul(C,L),mul(S,M))),C),2))
    D=mul(L,RT);Guard=[K(1)]
    for v in [a,b,C,sub(A,B),sub(B,C),sub(C,S),L,RT]:Guard=mul(Guard,v)
    return N,D,Guard

def universal_identities():
    # Expanded integer-polynomial checks with variables alpha,beta,gamma,epsilon,delta.
    class P:
        def __init__(self,c=0):
            self.v=c if isinstance(c,dict) else ({(0,0,0,0,0):c} if c else {})
        def __add__(self,b):
            b=b if isinstance(b,P) else P(b);v=self.v.copy()
            for e,c in b.v.items():v[e]=v.get(e,0)+c
            return P({e:c for e,c in v.items() if c})
        __radd__=__add__
        def __neg__(self):return P({e:-c for e,c in self.v.items()})
        def __sub__(self,b):return self+-(b if isinstance(b,P) else P(b))
        def __rsub__(self,b):return P(b)+-self
        def __mul__(self,b):
            b=b if isinstance(b,P) else P(b);v={}
            for e,c in self.v.items():
                for f,d in b.v.items():
                    g=tuple(x+y for x,y in zip(e,f));v[g]=v.get(g,0)+c*d
            return P({e:c for e,c in v.items() if c})
        __rmul__=__mul__
        def __pow__(self,n):
            z=P(1)
            for _ in range(n):z=z*self
            return z
    vs=[]
    for i in range(5):e=[0]*5;e[i]=1;vs.append(P({tuple(e):1}))
    a,b,c,e,d=vs;L=b*b-c*e;M=-2*a*b+a*c+a*e+b*c+b*e-2*c*e;J=(b-c)**2;S=a+b;U=2*c-S
    residual=(b-c)*(b*d*d+(b-a)*d+b-c)-(e-b)*d*(c*d+2*c-a-b)
    assert not (residual-(L*d*d+M*d+J)).v
    assert not (J*(c*c*L-c*S*M+S*S*J)-(c*c*J*L-c*U*M*L+U*U*L*L)).v

def polynomial_certificate():
    K=Field([1,1,1,1,1]);N,D,G=build_polynomials(K)
    # Explicit new degree-five formula, independently checked by multiplication.
    ns=[[7,10,10,0],[7,8,8,2],[3,8,10,4],[-5,-8,-4,2],[-1,-8,-6,0],[-3,-10,-10,0]]
    ds=[[1,0,0,0],[1,-1,-1,1],[-1,-1,0,2],[0,1,3,1],[2,1,2,0],[1,0,0,0]]
    n=list(map(K,ns));d=list(map(K,ds));assert mul(N,d)==mul(D,n)
    assert any(sub(n,scale(d,n[0])))  # The numerator is not n(0)*denominator.
    assert len(gcdp(n,d))==1
    radical=exactq(G,gcdp(G,derivative(G)));radical=scale(radical,1/radical[-1]);assert len(radical)==9
    assert len(gcdp(radical,derivative(radical)))==1
    assert len(N)==19 and len(D)==19 and len(G)==33
    # Recover formulas without relying on the exploratory JSON.
    common=gcdp(N,D); nr=exactq(N,common);dr=exactq(D,common)
    nr=scale(nr,1/dr[0]);dr=scale(dr,1/dr[0]);assert nr==n and dr==d
    return K,n,d,{'numerator':[x.data() for x in n],'denominator':[x.data() for x in d],'exception_polynomial':[x.data() for x in radical],'degrees':{'unreduced_numerator':18,'unreduced_denominator':18,'common_factor':len(common)-1,'reduced_numerator':5,'reduced_denominator':5,'raw_guard':32,'distinct_exception_bound':8}}

def matmul(A,B,p=None):
    n=len(A);l=len(B);m=len(B[0]);zero=0 if p else A[0][0]*0
    out=[[zero for _ in range(m)] for _ in range(n)]
    if p:
        for i in range(n):
            for j in range(m):out[i][j]=sum(A[i][k]*B[k][j] for k in range(l))%p
    else:
        for i in range(n):
            for j in range(m):out[i][j]=sum((A[i][k]*B[k][j] for k in range(l)),zero)
    return out

def rank(A,p):
    A=[r[:] for r in A];i=0
    for j in range(len(A[0])):
        k=next((k for k in range(i,len(A)) if A[k][j]%p),None)
        if k is None:continue
        A[i],A[k]=A[k],A[i];q=pow(A[i][j],-1,p);A[i]=[x*q%p for x in A[i]]
        for k in range(len(A)):
            if k!=i:
                v=A[k][j];A[k]=[(x-v*y)%p for x,y in zip(A[k],A[i])]
        i+=1
        if i==len(A):break
    return i

def modular_kernels(n,w,p,lam=1,need_B=True):
    h=(n+1)//2;F=[[pow(w,i*j,p) for j in range(n)] for i in range(n)];A=[pow(w,h*i*i,p) for i in range(n)];D=[pow(a,-1,p) for a in A]
    H=[[pow(w,(-h*(i+j)**2)%n,p) for j in range(n)] for i in range(n)];G=sum(A)%p;c=n*G%p;den=(1+pow(lam,3,p)*c)%p
    if need_B:assert den
    B=[[(F[i][j]-lam*G*H[i][j]+(lam*lam*c*D[i] if i==j else 0))*pow(den,-1,p)%p for j in range(n)] for i in range(n)] if need_B else None
    return F,A,D,H,G,c,B

def value_mod(v,z,p):return sum((x.numerator*pow(x.denominator,-1,p)%p)*pow(z,i,p) for i,x in enumerate(v.a))%p

def pole_data(r,z,p):
    a=(1+r*pow(z,2,p))%p;b=(1+r*pow(z,3,p))%p;c=(pow(z,2,p)+r*pow(z,3,p))%p;e=(pow(z,3,p)+r*pow(z,2,p))%p;f=(pow(z,4,p)+r)%p;h=(z+r)%p
    A=c*a*b%p;B=e*a*b%p;C=f*b*b%p;E=h*a*a%p;S=(A+B)%p;U=(2*C-S)%p;L=(B*B-C*E)%p;M=(-2*A*B+A*C+A*E+B*C+B*E-2*C*E)%p;J=(B-C)**2%p
    RT=(L*U*U-M*U*C+J*C*C)%p;guard=a*b*C*(A-B)*(B-C)*(C-S)*L*RT%p
    if not guard:return None
    N=(-2*S*J*U*L-M*(-S*J*C+(C*L-S*M)*U)+2*J*(C*L-S*M)*C)%p;D=L*RT%p
    return N*pow(D,-1,p)%p

def reconstruct_block(r,z,p,expected_trace):
    entries=[[ (pow(z,i*j,p)+r*pow(z,(-3*(i+j)**2)%5,p))%p for j in range(5)] for i in range(5)]
    a,b,c,e,f,h=entries[0][1],entries[0][2],entries[1][2],entries[1][3],entries[1][4],entries[2][3]
    al=c*pow(a*b,-1,p)%p;be=e*pow(a*b,-1,p)%p;ga=f*pow(a*a,-1,p)%p;ep=h*pow(b*b,-1,p)%p
    L=(be*be-ga*ep)%p;M=(-2*al*be+al*ga+al*ep+be*ga+be*ep-2*ga*ep)%p;J=(be-ga)**2%p;p1=M*pow(L,-1,p)%p;p0=J*pow(L,-1,p)%p
    class Quad:
        def __init__(self,a=0,b=0):self.a=a%p;self.b=b%p
        def co(self,x):return x if isinstance(x,Quad) else Quad(x)
        def __add__(self,x):x=self.co(x);return Quad(self.a+x.a,self.b+x.b)
        __radd__=__add__
        def __neg__(self):return Quad(-self.a,-self.b)
        def __sub__(self,x):return self+-self.co(x)
        def __rsub__(self,x):return self.co(x)+-self
        def __mul__(self,x):x=self.co(x);return Quad(self.a*x.a-p0*self.b*x.b,self.a*x.b+self.b*x.a-p1*self.b*x.b)
        __rmul__=__mul__
        def norm(self):return (self.a*self.a-p1*self.a*self.b+p0*self.b*self.b)%p
        def inv(self):
            norm=self.norm();assert norm
            return Quad(self.a-p1*self.b,-self.b)*pow(norm,-1,p)
        def __truediv__(self,x):return self*self.co(x).inv()
        def __eq__(self,x):x=self.co(x);return self.a==x.a and self.b==x.b
    dd=Quad(0,1);tt=(ga*dd+(al+be)*dd*dd)/(ga*(dd+2)-al-be);kk=(tt+dd*dd)*pow(ga,-1,p)
    assert tt+tt.inv()==expected_trace
    if not kk.norm() or not (1+tt).norm():return False
    xx=(tt-dd)/kk
    rr=[None,xx,(al-xx)/dd,(be-xx)/dd,(ga-xx)/dd];zz=kk/(1+tt)
    uu=[Quad(1)]+[entries[0][i]*rr[i] for i in range(1,5)];vv=[zz/tt]+[entries[0][i]-zz*uu[i] for i in range(1,5)]
    assert tt+tt.inv()==expected_trace
    for i in range(5):
        for j in range(i+1,5):assert uu[i]*vv[j]+tt*vv[i]*uu[j]==entries[i][j]
    return True

def finite_control(N,p,w,numer,denom,full=True,spectral=True):
    assert pow(w,N,p)==1 and all(pow(w,N//r,p)!=1 for r in range(2,N+1) if N%r==0 and all(r%d for d in range(2,math.isqrt(r)+1)))
    m=N//5;e5=m*pow(m,-1,5);em=5*pow(5,-1,m);eta=pow(w,e5,p);theta=pow(w,em,p)
    F,A,D,H,G,c,B=modular_kernels(N,w,p);f,a,d,h,g,cc,b5=modular_kernels(5,eta,p,need_B=False);fm,am,dm,hm,gm,cm,bm=modular_kernels(m,theta,p,need_B=False)
    assert G==g*gm%p and c==cc*cm%p
    idx=lambda a,b:(e5*a+em*b)%N
    for aa in range(5):
      for bb in range(m):
       for ac in range(5):
        for bd in range(m):
         i,j=idx(aa,bb),idx(ac,bd)
         target=(f[aa][ac]*fm[bb][bd]-G*h[aa][ac]*hm[bb][bd]+(c*d[aa]*dm[bb] if aa==ac and bb==bd else 0))*pow(1+c,-1,p)%p
         assert target==B[i][j]
    if full:
        X=[[(pow(N,-1,p)*pow(w,(-i*j)%N,p)+(A[i] if i==j else 0))%p for j in range(N)] for i in range(N)]
        identity=[[int(i==j) for j in range(N)] for i in range(N)]
        assert matmul(X,B,p)==identity and matmul(B,X,p)==identity
    rows=[];endpoint_checks=0;trace_only_checks=0
    for bb in range(m):
      for bd in range(m):
        rho=-G*hm[bb][bd]*pow(fm[bb][bd],-1,p)%p;t=pole_data(rho,eta,p)
        if t is not None:
            nv=sum(value_mod(v,eta,p)*pow(rho,i,p) for i,v in enumerate(numer))%p;dv=sum(value_mod(v,eta,p)*pow(rho,i,p) for i,v in enumerate(denom))%p;assert dv and t==nv*pow(dv,-1,p)%p
            if reconstruct_block(rho,eta,p,t):endpoint_checks+=1
            else:trace_only_checks+=1
            rows.append({'b':bb,'d':bd,'rho':rho,'trace':t})
    R=list(range(m//2));I=[idx(aa,bb) for aa in range(5) for bb in R];J=[i for i in range(N) if i not in I]
    cutrank=rank([[B[i][j] for j in J] for i in I],p);assert cutrank==5*(m//2)
    spectral_result=None
    if spectral:
        M=[[f[i][j]*a[j]%p for j in range(5)] for i in range(5)];M2=matmul(M,M,p);M3=matmul(M2,M,p);assert M3==[[cc*int(i==j)%p for j in range(5)] for i in range(5)]
        roots=[x for x in range(p) if pow(x,3,p)==cc];assert len(roots)==3
        projectors=[];ranks=[];L=[];solvers=[]
        for t in roots:
            P=[[(int(i==j)+pow(t,-1,p)*M[i][j]+pow(t,-2,p)*M2[i][j])*pow(3,-1,p)%p for j in range(5)] for i in range(5)]
            assert matmul(P,P,p)==P;projectors.append(P);ranks.append(rank(P,p));L.append(matmul(P,f,p));solvers.append(modular_kernels(m,theta,p,t)[-1])
        assert sum(ranks)==5
        for i,P in enumerate(projectors):
            for j,Qq in enumerate(projectors):
                if i!=j:assert matmul(P,Qq,p)==[[0]*5 for _ in range(5)]
        assert [[sum(P[i][j] for P in projectors)%p for j in range(5)] for i in range(5)]==[[int(i==j) for j in range(5)] for i in range(5)]
        for aa in range(5):
         for bb in range(m):
          for ac in range(5):
           for bd in range(m):assert sum(L[k][aa][ac]*solvers[k][bb][bd] for k in range(3))%p==B[idx(aa,bb)][idx(ac,bd)]
        spectral_result={'eigenvalues':roots,'multiplicities':ranks,'all_entry_reconstruction':True}
    controls=[];seen=set()
    for row in rows:
        if row['trace'] not in seen:controls.append(row);seen.add(row['trace'])
    return {'N':N,'prime':p,'omega':w,'eta':eta,'theta':theta,'G':G,'c':c,'full_two_sided_inverse':full,'crt_entries_checked':N*N,'complementary_fiber_cut_rank':cutrank,'good_ratio_count':len(set(r['rho'] for r in rows)),'distinct_pole_traces':len(seen),'quadratic_endpoint_checks':endpoint_checks,'quadratic_trace_only_checks':trace_only_checks,'trace_witnesses':controls,'spectral_recursion':spectral_result}

def charzero_fifteen(numer,denom):
    # Phi_15(x)=x^8-x^7+x^5-x^4+x^3-x+1.
    K=Field([1,-1,0,1,-1,1,0,-1,1]);w=K([0,1]);N=15;h=8;assert w**15==1 and w**5!=1 and w**3!=1
    powers=[w**i for i in range(N)];A=[powers[(h*i*i)%N] for i in range(N)];G=sum(A,K(0));c=N*G;assert G*G==-15;dinv=(1-c)/(1+N**3)
    assert dinv*(1+c)==1
    F=[[powers[(i*j)%N] for j in range(N)] for i in range(N)];B=[[(F[i][j]-G*powers[(-h*(i+j)**2)%N]+(c*powers[(-h*i*i)%N] if i==j else 0))*dinv for j in range(N)] for i in range(N)]
    X=[[(Q(1,N)*powers[(-i*j)%N]+(A[i] if i==j else 0)) for j in range(N)] for i in range(N)]
    ident=[[K(int(i==j)) for j in range(N)] for i in range(N)];assert matmul(X,B)==ident and matmul(B,X)==ident
    eta=w**6;theta=w**10
    embed=lambda v:sum((v.a[i]*eta**i for i in range(4)),K(0))
    nn=list(map(embed,numer));dd=list(map(embed,denom));traces=[]
    for d in [0,1]:
        rho=-G*theta**((-2*d*d)%3);traces.append(evalp(nn,rho)/evalp(dd,rho))
    assert traces[0]!=traces[1]
    return {'N':15,'field':'Q[x]/Phi_15(x)','full_two_sided_inverse_entries':450,'G':G.data(),'two_block_trace_values':[x.data() for x in traces],'different_traces':True}

def main():
    start=time.time();universal_identities();K,n,d,polys=polynomial_certificate();print('Polynomial invariant and eight-exception certificate passed.',flush=True)
    exact=charzero_fifteen(n,d);print('Characteristic-zero full N=15 control passed.',flush=True)
    controls=[]
    for args in [(15,31,9,True,True),(45,181,16,True,True),(65,131,4,False,False),(245,491,4,False,False)]:
        N,p,w,full,spectral=args;v=finite_control(N,p,w,n,d,full,spectral);controls.append(v);print('Finite full-CRT control',N,'traces',v['distinct_pole_traces'],flush=True)
    result={'polynomial_invariant':polys,'characteristic_zero':exact,'finite_controls':controls,'seconds':round(time.time()-start,3),'scope':'Direct one-reciprocal-pair-per-block pole bank obstruction, not a lower bound for arbitrary global Green sums.'}
    (OUT/'GLOBAL_LIFT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS',result['seconds'],'seconds')
if __name__=='__main__':main()
