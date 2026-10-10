#!/usr/bin/env python3
"""Fresh auditor controls. Never imports or executes a constructor/source file.

Usage: python audit_controls.py [result-json]
The source package is only hashed. All mathematical objects are recomputed here.
"""
from fractions import Fraction
from math import isqrt
from pathlib import Path
import hashlib, json, sys

SRC = Path('joint_chirp_bank_0200')

def snapshot():
    return {str(f): hashlib.sha256(f.read_bytes()).hexdigest()
            for f in sorted(SRC.rglob('*')) if f.is_file()}

class Field:
    def __init__(self, prime=None, modulus=None):
        self.prime, self.modulus = prime, modulus
        self.d = 1 if prime else len(modulus)-1
        self.zero, self.one = self.scalar(0), self.scalar(1)
    def scalar(self, n):
        return n % self.prime if self.prime else (Fraction(n),)+(Fraction(0),)*(self.d-1)
    def add(self, x, y):
        return (x+y)%self.prime if self.prime else tuple(a+b for a,b in zip(x,y))
    def neg(self, x):
        return (-x)%self.prime if self.prime else tuple(-a for a in x)
    def sub(self, x, y): return self.add(x,self.neg(y))
    def mul(self, x, y):
        if self.prime: return x*y%self.prime
        v=[Fraction(0)]*(2*self.d-1)
        for i,a in enumerate(x):
            for j,b in enumerate(y): v[i+j]+=a*b
        for k in range(len(v)-1,self.d-1,-1):
            for j in range(self.d): v[k-self.d+j]-=v[k]*self.modulus[j]
        return tuple(v[:self.d])
    def power(self, x, n):
        if n<0: return self.power(self.inv(x),-n)
        y=self.one
        while n:
            if n&1: y=self.mul(y,x)
            x=self.mul(x,x); n//=2
        return y
    def inv(self, x):
        if x==self.zero: raise ZeroDivisionError
        if self.prime: return pow(x,-1,self.prime)
        # Solve multiplication by x against 1. This is deliberately independent
        # of polynomial extended-Euclidean inversion in the constructor.
        basis=[tuple(Fraction(int(i==j)) for i in range(self.d)) for j in range(self.d)]
        cols=[self.mul(x,b) for b in basis]
        # Rational Gaussian elimination, rather than recursion through this field.
        a=[[cols[j][i] for j in range(self.d)]+[Fraction(i==0)] for i in range(self.d)]
        for j in range(self.d):
            k=next(k for k in range(j,self.d) if a[k][j]); a[j],a[k]=a[k],a[j]
            z=a[j][j]; a[j]=[t/z for t in a[j]]
            for k in range(self.d):
                if k!=j:
                    z=a[k][j]; a[k]=[t-z*u for t,u in zip(a[k],a[j])]
        return tuple(row[-1] for row in a)
    def div(self,x,y): return self.mul(x,self.inv(y))
    def total(self, xs):
        y=self.zero
        for x in xs: y=self.add(y,x)
        return y
    def serial(self,x):
        return x if self.prime else [str(c) for c in x]

class Poly:
    def __init__(self,F): self.F=F
    def tidy(self,p):
        p=list(p)
        while len(p)>1 and p[-1]==self.F.zero: p.pop()
        return p
    def add(self,p,q):
        F=self.F
        return self.tidy([F.add(p[i] if i<len(p) else F.zero,q[i] if i<len(q) else F.zero) for i in range(max(len(p),len(q)))])
    def scale(self,p,c): return self.tidy([self.F.mul(c,x) for x in p])
    def multiply(self,p,q):
        F=self.F; a=[F.zero]*(len(p)+len(q)-1)
        for i,x in enumerate(p):
            for j,y in enumerate(q): a[i+j]=F.add(a[i+j],F.mul(x,y))
        return self.tidy(a)
    def remainder(self,p,q):
        F=self.F; a=self.tidy(p); iq=F.inv(q[-1])
        while len(a)>=len(q) and a!=[F.zero]:
            t=len(a)-len(q); c=F.mul(a[-1],iq)
            for j,x in enumerate(q): a[t+j]=F.sub(a[t+j],F.mul(c,x))
            a=self.tidy(a)
        return a
    def gcd(self,p,q):
        F=self.F
        while q!=[F.zero]: p,q=q,self.remainder(p,q)
        return self.scale(p,F.inv(p[-1]))
    def derivative(self,p): return self.tidy([self.F.mul(self.F.scalar(i),p[i]) for i in range(1,len(p))] or [self.F.zero])
    def value(self,p,x):
        F=self.F; a=F.zero
        for c in reversed(p): a=F.add(F.mul(a,x),c)
        return a

def dot(F,a,b): return F.total(F.mul(x,y) for x,y in zip(a,b))
def solve(F,A,b):
    a=[list(row)+[v] for row,v in zip(A,b)]; n=len(a)
    for j in range(n):
        k=next(k for k in range(j,n) if a[k][j]!=F.zero); a[k],a[j]=a[j],a[k]
        z=F.inv(a[j][j]); a[j]=[F.mul(v,z) for v in a[j]]
        for k in range(n):
            if k!=j:
                z=a[k][j]
                if z!=F.zero: a[k]=[F.sub(v,F.mul(z,w)) for v,w in zip(a[k],a[j])]
    return [row[-1] for row in a]
def mm(F,A,B): return [[dot(F,row,col) for col in zip(*B)] for row in A]
def eye(F,n): return [[F.scalar(i==j) for j in range(n)] for i in range(n)]
def determinant(F,A):
    a=[row[:] for row in A]; d=F.one
    for j in range(len(a)):
        k=next((k for k in range(j,len(a)) if a[k][j]!=F.zero),None)
        if k is None: return F.zero
        if k!=j: a[j],a[k]=a[k],a[j]; d=F.neg(d)
        d=F.mul(d,a[j][j]); inv=F.inv(a[j][j])
        for k in range(j+1,len(a)):
            z=F.mul(a[k][j],inv)
            for l in range(j,len(a)): a[k][l]=F.sub(a[k][l],F.mul(z,a[j][l]))
    return d

def make_bank(F,N,w,sgn):
    P=Poly(F); r=(N+1)//2; h=(N+1)//2
    f=[F.power(w,(sgn*h*k*k)%N) for k in range(2*N)]
    def orthogonal(j):
        return solve(F,[[f[i+k] for k in range(j)] for i in range(j)],[F.neg(f[j+i]) for i in range(j)])+[F.one]
    a,b=orthogonal(r),orthogonal(r-1)
    # Independently verify every Hankel determinant up to the required size.
    for j in range(1,r+1):
        det=determinant(F,[[f[u+v] for v in range(j)] for u in range(j)])
        expect=F.one
        for u in range(j): expect=F.mul(expect,F.mul(f[u],f[u]))
        for u in range(j):
            for v in range(u+1,j): expect=F.mul(expect,F.sub(F.power(w,sgn*v%N),F.power(w,sgn*u%N)))
        assert det==expect and det!=F.zero
    def explicit(j):
        v=[F.one]
        for k in range(j): v=P.multiply(v,[F.neg(F.power(w,sgn*k%N)),F.one])
        return [F.div(F.mul(f[j],x),f[l]) for l,x in enumerate(v)]
    assert a==explicit(r) and b==explicit(r-1)
    assert P.gcd(a,b)==[F.one]
    unity=[F.neg(F.one)]+[F.zero]*(N-1)+[F.one]
    failures=[]
    for tau in range(2*N+1):
        p=P.add(a,P.scale(b,F.scalar(tau)))
        reasons=[]
        if p[0]==F.zero: reasons.append('zero_node')
        if len(P.gcd(p,P.derivative(p)))>1: reasons.append('multiple_node')
        if len(P.gcd(p,unity))>1: reasons.append('resonant_node')
        if not reasons: break
        failures.append({'tau':tau,'reasons':reasons})
    else: raise AssertionError('legal-pole search exhausted')
    for k in range(r-1): assert dot(F,p,f[k:k+r+1])==F.zero
    # Use the regular representation and ordinary linear solving to build the
    # quotient algebra. Trace is the literal matrix trace, not Newton sums.
    def pad(v): return v+[F.zero]*(r-len(v))
    basis=[[F.scalar(i==j) for i in range(r)] for j in range(r)]
    def times(v,u): return pad(P.remainder(P.multiply(v,u),p))
    def mult_matrix(v): return [list(row) for row in zip(*(times(v,e) for e in basis))]
    def invert(v): return solve(F,mult_matrix(v),basis[0])
    def tr(v): return F.total(mult_matrix(v)[j][j] for j in range(r))
    z=pad([F.zero,F.one]); zN=basis[0]
    for _ in range(N): zN=times(z,zN)
    q=[F.total(F.mul(p[j+l+1],f[l]) for l in range(r-j)) for j in range(r)]
    bweight=times(q,invert(pad(P.derivative(p))))
    assert len(P.gcd(bweight,p))==1
    v=bweight; moments=[]
    for _ in range(N): moments.append(tr(v)); v=times(z,v)
    assert moments==f[:N]
    close=[F.sub(u,v) for u,v in zip(basis[0],zN)]
    iclose=invert(close); weight=times(close,bweight)
    ell=[tr(times(weight,e)) for e in basis]
    def apply(x):
        acc=[F.zero]*r
        for t in reversed(x): acc=times(z,acc); acc[0]=F.add(acc[0],t)
        y0=times(iclose,acc); y=y0; out=[F.zero]*N; out[0]=dot(F,ell,y0)
        for i in range(N-1,0,-1): y=times(z,y); y[0]=F.add(y[0],x[i]); out[i]=dot(F,ell,y)
        assert F.sub(y0[0],times(z,y)[0])==x[0]
        assert all(F.sub(y0[j],times(z,y)[j])==F.zero for j in range(1,r))
        return out
    # Every basis vector is checked. Thus this is an all-input linear identity.
    cols=[]
    for k in range(N):
        out=apply([F.scalar(i==k) for i in range(N)])
        assert out==[f[(k-i)%N] for i in range(N)]
        cols.append(out)
    return {'sign':sgn,'tau':tau,'failed_candidates':failures,'p':[F.serial(c) for c in p],
            'hankel_sizes_checked':list(range(1,r+1)),'basis_output_comparisons':N*N},[list(row) for row in zip(*cols)]

def case(F,N,w):
    assert F.power(w,N)==F.one
    assert all(F.power(w,k)!=F.one for k in range(1,N))
    banks=[make_bank(F,N,w,s) for s in (-1,1)]
    h=(N+1)//2
    A=[F.power(w,h*i*i%N) for i in range(N)]; D=[F.inv(a) for a in A]
    FF=[[F.power(w,i*j%N) for j in range(N)] for i in range(N)]
    H=[[F.power(w,-h*(i+j)**2%N) for j in range(N)] for i in range(N)]
    G=F.total(A); c=F.mul(F.scalar(N),G); den=F.add(F.one,c)
    result={'N':N,'field':f'F_{F.prime}' if F.prime else f'Q(zeta_{N})','omega':F.serial(w),
            'r':(N+1)//2,'banks':[b[0] for b in banks],'c':F.serial(c),'target_invertible':den!=F.zero}
    if den==F.zero:
        M=[[F.add(F.div(F.power(w,-i*j%N),F.scalar(N)),A[i] if i==j else F.zero) for j in range(N)] for i in range(N)]
        assert determinant(F,M)==F.zero
        result['direct_singular_target_determinant']=F.serial(determinant(F,M))
        result['note']='Expected finite-field target exception: chirp banks valid but 1+NG=0.'
        return result
    B=[]
    for i in range(N):
        row=[]
        for j in range(N):
            direct=F.add(F.sub(FF[i][j],F.mul(G,H[i][j])),F.mul(c,D[i]) if i==j else F.zero)
            bank=F.sub(F.mul(F.mul(A[i],banks[0][1][i][j]),A[j]),F.mul(G,F.mul(F.mul(F.power(D[i],2),banks[1][1][i][j]),F.power(D[j],2))))
            if i==j: bank=F.add(bank,F.mul(c,D[i]))
            assert direct==bank
            row.append(F.div(bank,den))
        B.append(row)
    Finv=[[F.div(F.power(w,-i*j%N),F.scalar(N)) for j in range(N)] for i in range(N)]
    M=[[F.add(Finv[i][j],A[i] if i==j else F.zero) for j in range(N)] for i in range(N)]
    assert mm(F,M,B)==eye(F,N) and mm(F,B,M)==eye(F,N)
    FA=[[F.mul(FF[i][j],A[j]) for j in range(N)] for i in range(N)]
    assert mm(F,mm(F,FA,FA),FA)==[[c if i==j else F.zero for j in range(N)] for i in range(N)]
    BA=[[F.mul(B[i][j],A[j]) for j in range(N)] for i in range(N)]
    BAB=mm(F,BA,B); BABAB=mm(F,BA,BAB)
    recovered=[[F.add(F.add(F.mul(den,B[i][j]),F.mul(F.sub(F.one,F.mul(F.scalar(2),c)),BAB[i][j])),F.mul(den,BABAB[i][j])) for j in range(N)] for i in range(N)]
    assert recovered==FF
    result['full_B_entry_checks']=N*N; result['two_sided_inverse_entries']=2*N*N
    result['Fourier_recovery_entries']=N*N
    return result

def diagonal_criterion(F,N,w):
    P=Poly(F); m=(N-1)//2; data=[]
    for sign in (-1,1):
        q=F.power(w,sign%N); h=(N+1)//2
        f=[F.power(q,h*k*k%N) for k in range(N)]
        T=solve(F,[[f[i+j+1] for j in range(m)] for i in range(m)],
                [F.neg(f[i+m+1]) for i in range(m)])+[F.one]
        # Independent q-Pascal construction of the Gaussian binomial coefficients.
        coeff=[F.one]
        for n in range(1,m+1):
            nxt=[F.one]+[F.zero]*(n-1)+[F.one]
            for k in range(1,n): nxt[k]=F.add(coeff[k],F.mul(F.power(q,n-k),coeff[k-1]))
            coeff=nxt
        explicit=[F.mul(F.scalar((-1)**(m-j)),v) for j,v in enumerate(coeff)]
        assert T==explicit and T[0]==F.scalar((-1)**m)
        assert list(reversed(T))==[F.mul(F.scalar((-1)**m),v) for v in T]
        reasons=[]
        if len(P.gcd(T,P.derivative(T)))>1: reasons.append('multiple_node')
        if len(P.gcd(T,[F.neg(F.one)]+[F.zero]*(N-1)+[F.one]))>1: reasons.append('resonant_node')
        if m%2:
            assert P.value(T,F.one)==F.zero and 'resonant_node' in reasons
        for k in range(m): assert dot(F,T,f[k+1:k+m+2])==F.zero
        data.append({'sign':sign,'degree':m,'polynomial':[F.serial(x) for x in T],
                     'guard_failures':reasons,'exact_minimum_with_free_diagonal':m+bool(reasons)})
    return data

def diagonal_N5(F,w):
    N=5; P=Poly(F); data=[]
    for sign in (-1,1):
        q=F.power(w,sign%5); p=[F.one,F.neg(F.add(F.one,q)),F.one]
        f=[F.power(q,3*k*k%5) for k in range(5)]
        assert dot(F,p,f[1:4])==F.zero and dot(F,p,f[2:5])==F.zero
        assert len(P.gcd(p,P.derivative(p)))==1
        assert len(P.gcd(p,[F.neg(F.one)]+[F.zero]*4+[F.one]))==1
        f0=F.sub(F.add(F.power(q,3),F.power(q,4)),F.power(q,2))
        assert F.add(F.sub(f[2],F.mul(F.add(F.one,q),f[1])),f0)==F.zero
        assert determinant(F,[[f[1],f[2]],[f[2],f[3]]])!=F.zero
        data.append({'sign':sign,'polynomial':[F.serial(x) for x in p],
                     'diagonal_correction':F.serial(F.sub(F.one,f0)),'nonzero_branches':2})
    return data

def prime(n): return n>=2 and all(n%j for j in range(2,isqrt(n)+1))
def finite_field(N):
    p=2*N+1
    while not prime(p): p+=2*N
    F=Field(prime=p)
    w=next(w for w in range(2,p) if pow(w,N,p)==1 and all(pow(w,k,p)!=1 for k in range(1,N)))
    return F,w

def main():
    before=snapshot(); results=[]
    for N in (3,5,7,9,11,15,21):
        F,w=finite_field(N); item=case(F,N,w); item['diagonal_relaxation']=diagonal_criterion(F,N,w); results.append(item)
    # Exact characteristic-zero controls use rational coordinates, not complex floats.
    for N,phi in ((3,[1,1,1]),(5,[1,1,1,1,1])):
        F=Field(modulus=phi); w=(Fraction(0),Fraction(1))+(Fraction(0),)*(N-3)
        item=case(F,N,w); item['diagonal_relaxation']=diagonal_criterion(F,N,w); results.append(item)
        if N==5: relaxation=diagonal_N5(F,w)
    F9=Field(modulus=[1,0,0,1,0,0,1]); w9=(Fraction(0),Fraction(1))+(Fraction(0),)*4
    extra9=diagonal_criterion(F9,9,w9)
    after=snapshot(); assert before==after
    output={'status':'PASS','source_files_unchanged':True,'source_code_executed':False,
            'controls':results,'N5_diagonal_relaxation':relaxation,'N9_characteristic_zero_diagonal_criterion':extra9,
            'scope':'Independent exact controls; finite samples supplement the separately audited uniform proof.'}
    dest=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('AUDIT_RESULTS.json')
    dest.write_text(json.dumps(output,indent=2)+'\n')
    Path(__file__).with_name('SOURCE_HASHES_AFTER.json').write_text(json.dumps(after,indent=2)+'\n')
    print(json.dumps({'status':'PASS','cases':len(results),'results_file':str(dest),
                      'source_files_unchanged':before==after},sort_keys=True))
if __name__=='__main__': main()
