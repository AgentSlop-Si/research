"""Fresh independent integer-interval oracle, not production numerical code.

Different pi identity, interval Horner sine, and exact isqrt. Public target is
constructed directly from rational ell/N-k/M, without the retained iterator.
All endpoint intervals below have denominator 2**BITS.
"""
from fractions import Fraction
from math import factorial, isqrt

BITS=256
U=1 << BITS
TERMS=48
PI_TERMS=160


def ceildiv(a,b): return -((-a)//b)

def pi_interval():
    terms=[]
    for v in (2,3):
        total=sum((Fraction((-1)**j,(2*j+1)*v**(2*j+1)) for j in range(PI_TERMS)),Fraction())
        tail=Fraction((-1)**PI_TERMS,(2*PI_TERMS+1)*v**(2*PI_TERMS+1))
        terms.append((min(total,total+tail),max(total,total+tail)))
    lo=4*(terms[0][0]+terms[1][0]); hi=4*(terms[0][1]+terms[1][1])
    return (lo*U).__floor__(), (hi*U).__ceil__()


def add(a,b): return a[0]+b[0],a[1]+b[1]
def negate(a): return -a[1],-a[0]
def times(a,b):
    products=[x*y for x in a for y in b]
    return min(products)//U,ceildiv(max(products),U)

def rational_times(a,n,d=1):
    values=[a[0]*n,a[1]*n]
    return min(values)//d,ceildiv(max(values),d)


def quotient(a,b,normalization):
    assert b[0]>0
    lows=[x*U//(normalization*y) for x in a for y in b]
    highs=[ceildiv(x*U,normalization*y) for x in a for y in b]
    return min(lows),max(highs)


class Oracle:
    def __init__(self,N,M,D):
        self.N,self.M,self.D=N,M,D
        self.pi=pi_interval()
        self.coefficients=[]
        for j in range(TERMS):
            n=(-1)**j*U;d=factorial(2*j+1)
            self.coefficients.append((n//d,ceildiv(n,d)))
        numerator=1 << (2*TERMS+1+BITS)
        self.tail=ceildiv(numerator,factorial(2*TERMS+1))
        assert self.tail==1
        z=isqrt((M*U*U)//N)
        assert z*z*N<=M*U*U<(z+1)*(z+1)*N
        self.root=(z,z+1)
        self.calls=0
    def sine(self,argument):
        r=argument%2
        sign=1
        if r>1:r,sign=2-r,-1
        if r>Fraction(1,2):r=1-r
        if r==0:return (0,0)
        if r==Fraction(1,2):return (sign*U,sign*U)
        x=rational_times(self.pi,r.numerator,r.denominator)
        assert 0<=x[0]<=x[1]<=2*U
        square=times(x,x)
        polynomial=self.coefficients[-1]
        for coefficient in self.coefficients[-2::-1]:
            polynomial=add(times(polynomial,square),coefficient)
        ans=times(x,polynomial)
        ans=(ans[0]-self.tail,ans[1]+self.tail)
        return ans if sign>0 else negate(ans)
    def power(self,a,s):
        vals=[a[0]**s,a[1]**s]
        if s%2==0 and a[0]<=0<=a[1]:vals.append(0)
        divisor=1 << (BITS*(s-1))
        return min(vals)//divisor,ceildiv(max(vals),divisor)
    def coefficient(self,ell,k):
        self.calls+=1
        N,M,D=self.N,self.M,self.D
        m=M.bit_length()-1;s=D*m
        L=M//4;q=M//(8*s)
        u=(Fraction(ell,N)-Fraction(k,M))%1
        if u==0:
            first=((2*L+1)*U//M,)*2
            ratio=(U,U)
        else:
            denominator=self.sine(u)
            first=quotient(self.sine((2*L+1)*u),denominator,M)
            ratio=quotient(self.sine((2*q+1)*u),denominator,2*q+1)
        amplitude=times(times(first,self.power(ratio,s)),self.root)
        theta=Fraction(2*((N-1)//2)*ell,N)
        return (times(amplitude,self.sine(Fraction(1,2)-theta)),
                times(amplitude,self.sine(-theta)))
