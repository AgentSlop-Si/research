#!/usr/bin/env python3
"""Independent review controls. No submitted module or original R30 code is run.
Real-polynomial Fourier oracle: Q[z]/(z^(N/2)+1), not the submission's
Gaussian-lane oracle. N=2 retains Q[i] with zeta=-1.
"""
from fractions import Fraction as F
from collections import Counter
from itertools import product
from pathlib import Path
import hashlib,json,random,time

HERE=Path(__file__).resolve().parent
SOURCE=Path(__file__).resolve().parent.parent / 'candidate'

def ga(x,y):return (x[0]+y[0],x[1]+y[1])
def gm(x,y):return (x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def g(a=0,b=0):return (F(a),F(b))
def mm(a,b):
    return [[ga(gm(a[r][0],b[0][c]),gm(a[r][1],b[1][c])) for c in range(2)] for r in range(2)]
def chain(*args):
    out=args[0]
    for arg in args[1:]:out=mm(out,arg)
    return out

def algebra():
    O=g();I=g(1);J=g(0,1);H=[[I,I],[I,g(-1)]]
    C=[[g(F(1,2),F(1,2)),g(F(1,2),-F(1,2))],[g(F(1,2),-F(1,2)),g(F(1,2),F(1,2))]]
    Ci=[[(z[0],-z[1]) for z in row] for row in C]
    R=chain(Ci,[[g(-F(1,2)),O],[O,g(F(1,4))]],C)
    assert R==[[g(-F(1,8)),g(0,F(3,8))],[g(0,-F(3,8)),g(-F(1,8))]]
    Q=[[I,O],[O,J]];Qi=[[I,O],[O,g(0,-1)]]
    U=[[I,g(-2)],[O,I]];L=[[I,O],[I,I]];D=[[g(-8),O],[O,g(-2)]]
    assert chain(D,L,Qi,R,Q,U)==H
    K=[[I,g(3)],[g(3),I]]
    assert chain([[I,O],[O,g(F(1,4))]],L,K,U)==H
    assert chain([[I,O],[O,g(F(3,4))]],[[I,O],[g(-F(5,3)),I]],K,[[I,O],[O,g(F(1,3))]])==H
    unit_family=0
    # Gaussian units include all phases times powers of 2 and of 1+i.
    units=[g(F(2)**k) for k in range(-5,6)] + [g(F(2)**k,F(2)**k) for k in range(-4,5)]
    for p in units:
        den=p[0]*p[0]+p[1]*p[1]
        pinv=(p[0]/den,-p[1]/den);q=gm(g(4),pinv)
        qden=q[0]*q[0]+q[1]*q[1];qinv=(q[0]/qden,-q[1]/qden)
        got=chain([[I,O],[O,qinv]],[[I,O],[ga(q,g(-3)),I]],K,[[I,ga(p,g(-3))],[O,I]],[[I,O],[O,pinv]])
        assert got==H
        unit_family+=1
    mutants=[chain(D,Qi,R,Q,U),chain(D,L,Qi,R,Q),chain([[I,O],[O,I]],L,Qi,R,Q,U),chain(D,L,Qi,R,Q,[[I,g(-1)],[O,I]])]
    assert all(x!=H for x in mutants)
    return {'two_shear_identity':True,'R30_conjugacy':True,'rational_one_shear_witness':True,'scaling_family_cases':unit_family,'live_algebraic_mutants_rejected':len(mutants)}

# F9 uses tuples, independently of the submitted integer encoding.
F9=list(product(range(3),repeat=2));Z=(0,0);ONE=(1,0)
def fadd(a,b):return ((a[0]+b[0])%3,(a[1]+b[1])%3)
def fmul(a,b):return ((a[0]*b[0]-a[1]*b[1])%3,(a[0]*b[1]+a[1]*b[0])%3)
def matmul(a,b):return tuple(fadd(fmul(a[2*r],b[c]),fmul(a[2*r+1],b[c+2])) for r in range(2) for c in range(2))
def modular():
    nonzero=[x for x in F9 if x!=Z]
    mon=[]
    for a,b in product(nonzero,repeat=2):mon.extend([(a,Z,Z,b),(Z,a,b,Z)])
    target=(ONE,ONE,ONE,(2,0));count=0;max_support=0
    for s in F9:
        for shear in [(ONE,s,Z,ONE),(ONE,Z,s,ONE)]:
            for l in mon:
                a=matmul(l,shear)
                for r in mon:
                    v=matmul(a,r);count+=1
                    max_support=max(max_support,sum(x!=Z for x in v))
                    assert v!=target and Z in v
    # Each of both implemented parameter/direction choices reduces to I.
    def reduce_fraction(x):return (x.numerator%3)*pow(x.denominator%3,-1,3)%3
    for rho,sgn in product([3,-3],[1,-1]):
        matrix=[g(-F(1,8)),g(0,F(rho*sgn,8)),g(0,-F(rho*sgn,8)),g(-F(1,8))]
        assert tuple(tuple(reduce_fraction(v) for v in z) for z in matrix)==(ONE,Z,Z,ONE)
    return {'monomial_matrices':len(mon),'one_shear_sandwiches':count,'maximum_support':max_support,'both_rhos_both_directions_reduce_to_identity':True}

class Arithmetic:
    def __init__(self,bits=None):self.count=Counter();self.peak=0;self.bits=bits
    def check(self,x):
        self.peak=max(self.peak,abs(x))
        if self.bits is not None and not -(2**(self.bits-1))<=x<2**(self.bits-1):raise OverflowError
        return x
    def add(self,a,b):self.count['add']+=1;return self.check(a+b)
    def minus(self,a):self.count['neg']+=1;return self.check(-a)
    def shift(self,a,k):self.count['left']+=1;return self.check(a*2**k)
    def divide(self,a,k):
        self.count['divide']+=1
        if isinstance(a,int):
            if a%2**k:raise ArithmeticError('inexact divide')
            return self.check(a//2**k)
        return self.check(a/F(2**k))
    def root(self,a,e):
        # z^d=-1. This code naturally accounts for signs of reduced terms.
        d=len(a);out=[0]*d
        for j,c in enumerate(a):
            q,r=divmod(j+e,d);out[r]=self.minus(c) if q%2 else c
        return out
    def pair(self,a,b):
        for v in a+b:self.check(v)
        d=len(a);quarter=d//2
        u=[self.add(x,self.minus(self.shift(y,1))) for x,y in zip(a,b)]
        v=self.root(b,quarter)
        vroute=self.root(v,-quarter);uroute=self.root(u,quarter)
        r=[self.minus(self.divide(self.add(x,self.add(self.shift(y,1),y)),3)) for x,y in zip(u,vroute)]
        s=[self.minus(self.divide(self.add(x,self.add(self.shift(y,1),y)),3)) for x,y in zip(v,uroute)]
        s=self.root(s,-quarter)
        s=[self.add(x,y) for x,y in zip(s,r)]
        return ([self.minus(self.shift(x,3)) for x in r],[self.minus(self.shift(x,1)) for x in s])

def poly_size(n):return max(2,n//2)
def root_power(n):return 2 if n==2 else 1

def fourier(x,bits=None):
    n=len(x);D=n.bit_length()-1;op=Arithmetic(bits)
    # Independent bit arithmetic, avoiding the submitted string reversal.
    def reverse(j):
        r=0
        for _ in range(D):r=(r<<1)|(j&1);j>>=1
        return r
    y=[x[reverse(j)][:] for j in range(n)]
    width=2
    while width<=n:
        half=width//2
        for start in range(0,n,width):
            for offset in range(half):
                a=start+offset;b=a+half
                t=op.root(y[b],root_power(n)*offset*(n//width))
                y[a],y[b]=op.pair(y[a],t)
        width*=2
    return y,op

def dft_poly(x):
    # Full polynomial convolution with each root monomial, in Q[z]/(z^d+1).
    n=len(x);d=len(x[0]);out=[]
    for r in range(n):
        row=[0]*d
        for c in range(n):
            for h,coefficient in enumerate(x[c]):
                power=h+root_power(n)*r*c
                quotient,remainder=divmod(power,d)
                row[remainder]+=(-coefficient if quotient%2 else coefficient)
        out.append(row)
    return out

def expected_count(n):
    D=n.bit_length()-1;ell=max(1,n//4);pairs=n*D*ell//2
    return {'add':12*pairs,'neg':14*pairs+(n*n*(D-2)+2*n)//8,'left':10*pairs,'divide':4*pairs}

def tests():
    results=[];basis_comparisons=0;expanded_entries=0
    for D in range(1,7):
        n=2**D;d=poly_size(n)
        for c in range(n):
            x=[[0]*d for _ in range(n)];x[c][0]=8
            actual,op=fourier(x)
            for r in range(n):
                row=[0]*d;q,h=divmod(root_power(n)*r*c,d);row[h]=8*(-1 if q%2 else 1)
                assert actual[r]==row;basis_comparisons+=1
            assert dict(op.count)==expected_count(n)
        expanded=0
        if n<=16:
            for c,h in product(range(n),range(d)):
                x=[[0]*d for _ in range(n)];x[c][h]=8
                actual,op=fourier(x)
                expected=dft_poly(x)
                assert actual==expected;expanded+=1;expanded_entries+=(n*d)
        results.append({'N':n,'real_polynomial_degree':d,'coordinate_basis_vectors':n,'expanded_basis_vectors':expanded})
    rng=random.Random(202610180013)
    dense=[]
    for D in range(1,9):
        n=2**D;d=poly_size(n)
        x=[[8*rng.randint(-20,20) for _ in range(d)] for _ in range(n)]
        actual,op=fourier(x,bits=32);assert actual==dft_poly(x)
        assert dict(op.count)==expected_count(n)
        M=max(abs(v) for row in x for v in row)
        assert op.peak<=5*n*M
        dense.append({'N':n,'real_output_coefficients':n*d,'ops':dict(op.count),'peak':op.peak})
    # Exact rational Gaussian pair and all sign corners for the peak bound.
    pairs=0;peak_ratio=F(0)
    for vals in product(range(-2,3),repeat=4):
        a=[F(vals[0],2),F(vals[1],4)];b=[F(vals[2],8),F(vals[3],16)]
        op=Arithmetic();got=op.pair(a,b)
        assert got==([x+y for x,y in zip(a,b)],[x-y for x,y in zip(a,b)])
        assert dict(op.count)=={'add':12,'neg':14,'left':10,'divide':4};pairs+=1
    for vals in product([-8,0,8],repeat=4):
        op=Arithmetic();op.pair(list(vals[:2]),list(vals[2:]))
        M=max(abs(x) for x in vals)
        if M:peak_ratio=max(peak_ratio,F(op.peak,M));assert op.peak<=9*M
    assert peak_ratio==9
    controls={}
    for label,a,b,bits,error in [('two_reserve_bits',[4,0],[0,0],None,ArithmeticError),('overflow',[128,0],[0,0],8,OverflowError)]:
        try:Arithmetic(bits).pair(a,b)
        except error:controls[label]=True
        else:raise AssertionError(label)
    # Enumerate all twiddle exponents independently of the closed-form count.
    twiddles=[]
    for D in range(1,13):
        n=2**D;ident=quarter=general=signs=0;ell=max(1,n//4)
        for stage in range(1,D+1):
            width=2**stage
            for j in range(width//2):
                e=j*(n//width);copies=n//width
                if e==0:ident+=copies
                elif n>=4 and e==n//4:quarter+=copies
                else:general+=copies
                signs+=copies*e
        assert general==n*D//2-3*n//2+2
        assert quarter==n//2-1
        assert signs==(n*n*(D-2)+2*n)//8
        twiddles.append({'N':n,'identity':ident,'i':quarter,'general':general,'lane_signs':signs})
    return {'basis_DFT_coefficients':basis_comparisons,'expanded_real_matrix_entries':expanded_entries,'basis_tests':results,'dense_tests':dense,'rational_pair_cases':pairs,'sharp_checked_pair_peak_ratio':str(peak_ratio),'negative_controls':controls,'twiddle_checks':twiddles}

def source_hashes():
    manifest=json.loads((SOURCE/'MANIFEST.json').read_text());checked=[]
    for row in manifest['files']:
        p=SOURCE/row['file'];data=p.read_bytes();sha=hashlib.sha256(data).hexdigest()
        assert len(data)==row['bytes'] and sha==row['sha256']
        checked.append({'file':str(p),'bytes':len(data),'sha256':sha})
    for row in json.loads((SOURCE/'INPUT_REFERENCES.json').read_text())['inputs']:
        data=(SOURCE/row['path']).read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
    return {'release_files':checked,'source_reference_hashes_verified':4}

def main():
    start=time.monotonic();result={'status':'PASS','method':'Independent exact review controls; no submitted or original R30 program imported or executed','hashes':source_hashes(),'algebra':algebra(),'modular':modular(),'transforms_and_ledger':tests()}
    result['elapsed_seconds']=round(time.monotonic()-start,3)
    (HERE/'independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'elapsed_seconds':result['elapsed_seconds'],'modular_cases':result['modular']['one_shear_sandwiches'],'basis_coefficients':result['transforms_and_ledger']['basis_DFT_coefficients'],'expanded_entries':result['transforms_and_ledger']['expanded_real_matrix_entries']},indent=2))
if __name__=='__main__':main()
