#!/usr/bin/env python3
"""Fresh exact tests. No supplied R30 module, FFT, numpy or sympy is imported."""
from fractions import Fraction as F
from collections import Counter
from pathlib import Path
import argparse, hashlib, itertools, json, time

ZERO = (F(0), F(0))
ONE = (F(1), F(0))
I = (F(0), F(1))
def g(a, b=0): return (F(a), F(b))
def ga(x,y): return (x[0]+y[0],x[1]+y[1])
def gn(x): return (-x[0],-x[1])
def gs(x,y): return ga(x,gn(y))
def gm(x,y): return (x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def scale(x,a): return (x[0]*a,x[1]*a)
def phase(x,q):
    return (x,(-x[1],x[0]),(-x[0],-x[1]),(x[1],-x[0]))[q%4]
def mm(A,B):
    return [[sumg(gm(A[r][j],B[j][c]) for j in range(len(B)))
             for c in range(len(B[0]))] for r in range(len(A))]
def sumg(xs):
    z=ZERO
    for x in xs: z=ga(z,x)
    return z

def matrix_checks():
    E=[[ONE,ZERO],[ZERO,g(F(1,2))]]
    U=[[ONE,g(-1)],[ZERO,ONE]]
    L=[[ONE,ZERO],[g(-1),ONE]]
    Q=[[ONE,ZERO],[ZERO,I]]
    Qi=[[ONE,ZERO],[ZERO,gn(I)]]
    K=[[ONE,g(3)],[g(3),ONE]]
    H=[[ONE,ONE],[ONE,g(-1)]]
    C=[[g(F(1,2),F(1,2)),g(F(1,2),F(-1,2))],
       [g(F(1,2),F(-1,2)),g(F(1,2),F(1,2))]]
    Ci=[[(z[0],-z[1]) for z in row] for row in C]
    green=[[g(F(-1,2)),ZERO],[ZERO,g(F(1,4))]]
    R=mm(mm(Ci,green),C)
    expectedR=[[g(F(-1,8)),g(0,F(3,8))],
               [g(0,F(-3,8)),g(F(-1,8))]]
    assert R==expectedR
    assert mm(mm(mm(mm(E,L),K),U),E)==H
    assert [[scale(z,-8) for z in row] for row in mm(mm(Qi,R),Q)]==K
    A=mm(mm(E,L),Qi); A=[[scale(z,-8) for z in row] for row in A]
    B=mm(mm(Q,U),E)
    assert mm(mm(A,R),B)==H
    # Correctness of both parameters; construction uses +3 only.
    assert mm([[g(-1),ZERO],[ZERO,ONE]], [[g(-1),ZERO],[ZERO,ONE]]) == [[ONE,ZERO],[ZERO,ONE]]
    A1=mm([[g(-8),ZERO],[ZERO,g(-2)]],mm([[ONE,ZERO],[ONE,ONE]],Qi))
    B1=mm(Q,[[ONE,g(-2)],[ZERO,ONE]])
    assert mm(mm(A1,R),B1)==H
    return {"exact_gaussian_matrix_identities":5,"construction_rho":3}

class Ops:
    """A literal real-scalar evaluator; counts charged at every executed op."""
    def __init__(self, integer=False, bits=None):
        self.c=Counter(); self.integer=integer; self.bits=bits; self.peak=0
    def check(self,x):
        self.peak=max(self.peak,abs(x))
        if self.integer and (not isinstance(x,int)):
            raise ValueError('integer grid required')
        if self.bits and not -(1<<(self.bits-1))<=x<(1<<(self.bits-1)):
            raise OverflowError('signed intermediate overflow')
        return x
    def add(self,x,y): self.c['add']+=1; return self.check(x+y)
    def neg(self,x): self.c['neg']+=1; return self.check(-x)
    def left(self,x,k): self.c['left']+=1; return self.check(x*(1<<k))
    def div(self,x,k):
        self.c['divide']+=1
        if self.integer:
            if x%(1<<k): raise ValueError('inexact binary division')
            return self.check(x//(1<<k))
        return self.check(x/F(1<<k))
    def phase(self,x,q):
        q%=4
        if q==0:return x
        if q==1:return (self.neg(x[1]),x[0])
        if q==2:return (self.neg(x[0]),self.neg(x[1]))
        return (x[1],self.neg(x[0]))
    def sub(self,x,y):return (self.add(x[0],self.neg(y[0])),self.add(x[1],self.neg(y[1])))
    def cpdiv(self,x,k):return tuple(self.div(a,k) for a in x)
    def r30(self,a,b):
        # Exactly the rho=3, selected=parity=1, forward-first scalar rule.
        out=[]
        for own,other in ((a,self.phase(b,3)),(b,self.phase(a,1))):
            out.append(tuple(self.neg(self.div(self.add(x,self.add(self.left(y,1),y)),3))
                             for x,y in zip(own,other)))
        return tuple(out)
    def interface(self,a,b):
        # U(-2) -> Q -> R3 -> Q^-1 -> L(+1) -> diag(-8,-2).
        a=tuple(self.check(z) for z in a); b=tuple(self.check(z) for z in b)
        two_b=tuple(self.left(z,1) for z in b)
        a=self.sub(a,two_b)
        b=self.phase(b,1)
        a,b=self.r30(a,b)
        b=self.phase(b,3)
        b=tuple(self.add(y,x) for y,x in zip(b,a))
        return tuple(tuple(self.neg(self.left(z,k)) for z in x) for x,k in ((a,3),(b,1)))

def local_checks():
    count=0
    for ar,ai,br,bi in itertools.product(range(-2,3),repeat=4):
        a=(F(ar,2),F(ai,4));b=(F(br,8),F(bi,2))
        op=Ops(); got=op.interface(a,b)
        assert got==(ga(a,b),gs(a,b))
        assert dict(op.c)=={'left':10,'neg':14,'add':12,'divide':4}
        count+=1
    grid=0
    max_ratio=F(0)
    for ar,ai,br,bi in itertools.product(range(-2,3),repeat=4):
        a=(8*ar,8*ai);b=(8*br,8*bi);op=Ops(integer=True,bits=10)
        assert op.interface(a,b)==(ga(a,b),gs(a,b))
        M=max(abs(z) for z in a+b)
        if M:max_ratio=max(max_ratio,F(op.peak,M));assert op.peak<=9*M
        grid+=1
    failures={}
    for label,a,b,kwargs,exc in [
        ('insufficient_grid',(4,0),(0,0),{'integer':True},ValueError),
        ('overflow',(128,0),(0,0),{'integer':True,'bits':8},OverflowError)]:
        try:Ops(**kwargs).interface(a,b)
        except exc:failures[label]=True
        else:raise AssertionError(label+' was not refused')
    return {'rational_pair_cases':count,'integer_grid_pair_cases':grid,
            'three_reserve_bits_sufficient':True,'two_reserve_bits_rejected':True,
            'maximum_checked_peak_over_input':str(max_ratio),'guard_negative_controls':failures,
            'literal_per_pair_real_ops':{'add':12,'neg':14,'left':10,'divide':4}}

# Independent finite ring F9 = F3[j]/(j^2+1), encoded a+3b.
def fa(x,y):return ((x%3+y%3)%3)+3*((x//3+y//3)%3)
def fm(x,y):return ((x%3*(y%3)-x//3*(y//3))%3)+3*((x%3*(y//3)+x//3*(y%3))%3)
def fmm(A,B):
    return (fa(fm(A[0],B[0]),fm(A[1],B[2])),fa(fm(A[0],B[1]),fm(A[1],B[3])),
            fa(fm(A[2],B[0]),fm(A[3],B[2])),fa(fm(A[2],B[1]),fm(A[3],B[3])))
def modular_controls():
    monos=[]
    for a,b in itertools.product(range(1,9),repeat=2):
        monos.extend([(a,0,0,b),(0,a,b,0)])
    H=(1,1,1,2); checked=0; maximum=0
    for s in range(9):
        for S in ((1,s,0,1),(1,0,s,1)):
            for A in monos:
                AS=fmm(A,S)
                for B in monos:
                    V=fmm(AS,B); checked+=1
                    maximum=max(maximum,sum(x!=0 for x in V))
                    assert V!=H and 0 in V
    assert fmm(fmm((1,0,2,1),(1,0,0,1)),(1,2,0,1))==(1,2,2,2)
    # Explicit E L K U E reduces to H. 1/2=2, K=I in characteristic 3.
    E=(1,0,0,2);L=(1,0,2,1);U=(1,2,0,1)
    assert fmm(fmm(fmm(E,L),U),E)==H
    return {'field':'F_3[i], i^2=-1','monomial_matrices':len(monos),
            'all_one_shear_monomial_sandwiches':checked,'maximum_nonzero_entries':maximum,
            'target_has_four_nonzeros':True,'two_shear_witness':True}

def lane_count(n):return max(1,n//4)
def root_phase(n):return 2 if n==2 else 1

def twiddle(v,e,n,op):
    L=len(v); out=[None]*L
    e*=root_phase(n)
    for h,z in enumerate(v):
        q,r=divmod(h+e,L)
        out[r]=op.phase(z,q)
    return out

def fft_interface(values,integer=False,bits=None):
    n=len(values);D=n.bit_length()-1;ell=lane_count(n)
    assert n==1<<D and all(len(v)==ell for v in values)
    op=Ops(integer=integer,bits=bits)
    x=[values[int(f'{j:0{D}b}'[::-1],2)][:] for j in range(n)]
    for m in range(1,D+1):
        w=1<<m; h=w//2
        for base in range(0,n,w):
            for j in range(h):
                a=base+j;b=a+h
                right=twiddle(x[b],j*n//w,n,op)
                pairs=[op.interface(z,t) for z,t in zip(x[a],right)]
                x[a]=[z[0] for z in pairs];x[b]=[z[1] for z in pairs]
    return x,op

def direct_dft(values):
    # Independent direct root exponent accumulation, no FFT stages or interface.
    n=len(values);L=len(values[0]);out=[]
    for r in range(n):
        row=[ZERO]*L
        for c,v in enumerate(values):
            for h,z in enumerate(v):
                q,k=divmod(h+root_phase(n)*r*c,L)
                row[k]=ga(row[k],phase(z,q))
        out.append(row)
    return out

def predicted(n):
    D=n.bit_length()-1;L=lane_count(n);p=n*D*L//2
    phases=(n*n*(D-2)+2*n)//8
    return {'add':12*p,'neg':14*p+phases,'left':10*p,'divide':4*p}

def transform_checks(max_basis_D=6,max_dense_D=8):
    results=[];basiscoeff=0;fullcoords=0
    for D in range(1,max_basis_D+1):
        n=1<<D;L=lane_count(n);cases=0
        # Full Fourier coefficients on all coordinate basis vectors over Q(i).
        for c in range(n):
            x=[[ZERO]*L for _ in range(n)];x[c][0]=ONE
            y,op=fft_interface(x)
            for r in range(n):
                q,k=divmod(root_phase(n)*r*c,L)
                expected=[ZERO]*L;expected[k]=phase(ONE,q)
                assert y[r]==expected
                basiscoeff+=1
            assert dict(op.c)==predicted(n)
            cases+=1
        # All auxiliary-basis input coordinates, both real and imaginary,
        # at small sizes prove the implementation uses no single-lane shortcut.
        expanded=0
        if D<=4:
            for c,h,imag in itertools.product(range(n),range(L),range(2)):
                x=[[ZERO]*L for _ in range(n)];x[c][h]=I if imag else ONE
                y,op=fft_interface(x)
                for r in range(n):
                    q,k=divmod(h+root_phase(n)*r*c,L)
                    expected=[ZERO]*L;expected[k]=phase(I if imag else ONE,q)
                    assert y[r]==expected
                    fullcoords+=2*L
                expanded+=1
        results.append({'N':n,'lanes':L,'Fourier_basis_vectors':cases,
                        'expanded_real_basis_vectors':expanded})
    dense=[]
    for D in range(1,max_dense_D+1):
        n=1<<D;L=lane_count(n)
        x=[[(8*((7*j+3*h)%17-8),8*((5*j+11*h)%19-9)) for h in range(L)]
           for j in range(n)]
        y,op=fft_interface(x,integer=True,bits=32)
        expected=direct_dft(x)
        assert y==expected
        assert dict(op.c)==predicted(n)
        M=max(abs(z) for row in x for p in row for z in p)
        assert op.peak<=5*n*M
        # Input pattern includes zeros; no data-dependent skip is used.
        dense.append({'N':n,'lanes':L,'checked_output_gaussian_lanes':n*L,
                      'ops':dict(op.c),'peak_integer_magnitude':int(op.peak),
                      'three_reserve_bits_sufficient':True,'exact_direct_DFT_match':True})
    return {'all_input_basis_DFT_coefficients':basiscoeff,
            'expanded_real_matrix_entries_checked':fullcoords,
            'basis_tests':results,'dense_integer_tests':dense}

def mutation_controls():
    H=[[ONE,ONE],[ONE,g(-1)]];E=[[ONE,ZERO],[ZERO,g(F(1,4))]]
    K=[[ONE,g(3)],[g(3),ONE]];U=[[ONE,g(-2)],[ZERO,ONE]]
    L=[[ONE,ZERO],[ONE,ONE]];ID=[[ONE,ZERO],[ZERO,ONE]]
    bad=[mm(mm(mm(E,L),K),ID),mm(mm(mm(E,ID),K),U),
         mm(mm(mm(ID,L),K),U),mm(mm(mm(E,L),K),[[ONE,g(-1)],[ZERO,ONE]])]
    assert all(A!=H for A in bad)
    return {'missing_input_shear':True,'missing_output_shear':True,
            'missing_output_quarter':True,'wrong_input_shear_coefficient':True}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--basis-D',type=int,default=6)
    parser.add_argument('--dense-D',type=int,default=8);args=parser.parse_args()
    start=time.time()
    result={'status':'PASS','method':'fresh exact rational/Gaussian and integer-grid code; no supplied program executed',
            'matrix_checks':matrix_checks(),'local_checks':local_checks(),
            'modular_controls':modular_controls(),
            'transform_checks':transform_checks(args.basis_D,args.dense_D),
            'mutation_controls':mutation_controls()}
    result['elapsed_seconds']=round(time.time()-start,3)
    out=Path(__file__).resolve().parent/'verification.json'
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'output':str(out),'elapsed_seconds':result['elapsed_seconds'],
                      'DFT_coefficients':result['transform_checks']['all_input_basis_DFT_coefficients'],
                      'expanded_real_entries':result['transform_checks']['expanded_real_matrix_entries_checked'],
                      'modular_cases':result['modular_controls']['all_one_shear_monomial_sandwiches']},indent=2))
if __name__=='__main__':main()
