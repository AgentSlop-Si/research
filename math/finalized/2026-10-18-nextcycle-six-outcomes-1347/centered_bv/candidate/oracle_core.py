"""Reviewer's fresh 320-bit forward interval Taylor oracle for M=4N.
Different pi identity, recurrence and exact root than production/preserved oracle.
All interval endpoints have denominator 2**320. No candidate imports.
"""
from fractions import Fraction
from math import factorial
Q=320
U=1<<Q
def ceildiv(a,b):return -((-a)//b)
def add(x,y):return x[0]+y[0],x[1]+y[1]
def neg(x):return -x[1],-x[0]
def mul(x,y):
 products=[a*b for a in x for b in y]
 return min(products)//U,ceildiv(max(products),U)
def scale(x,a,b=1):
 vals=[a*v for v in x];return min(vals)//b,ceildiv(max(vals),b)
def pi_interval():
 def atan(d):
  terms=160
  a=sum((Fraction((-1)**j,(2*j+1)*d**(2*j+1)) for j in range(terms)),Fraction(0))
  b=a+Fraction((-1)**terms,(2*terms+1)*d**(2*terms+1))
  return min(a,b),max(a,b)
 a,b=atan(3),atan(7)
 low,high=8*a[0]+4*b[0],8*a[1]+4*b[1]
 return (low*U).__floor__(),(high*U).__ceil__()
PI=pi_interval()
TAIL=ceildiv((1<<129)*U,factorial(129))
assert TAIL==1
def sine(r):
 r%=2;sign=1
 if r>1:r=2-r;sign=-1
 if r>Fraction(1,2):r=1-r
 if not r:return (0,0)
 if r==Fraction(1,2):return sign*U,sign*U
 x=scale(PI,r.numerator,r.denominator);assert 0<=x[0]<=x[1]<2*U
 xx=mul(x,x);term=x;total=x
 for j in range(1,64):
  term=scale(neg(mul(term,xx)),1,2*j*(2*j+1))
  total=add(total,term)
 total=total[0]-TAIL,total[1]+TAIL
 return total if sign==1 else neg(total)
def divide(a,b,n):
 assert b[0]>0
 return min(x*U//(y*n) for x in a for y in b),max(ceildiv(x*U,y*n) for x in a for y in b)
def power(x,n):
 endpoints=[v**n for v in x]
 if n%2==0 and x[0]<=0<=x[1]:endpoints.append(0)
 denominator=U**(n-1)
 return min(endpoints)//denominator,ceildiv(max(endpoints),denominator)
def coefficient(N,M,D,ell,k):
 assert M==4*N
 m=M.bit_length()-1;s=D*m;L=M//4;q=M//(8*s)
 u=(Fraction(ell,N)-Fraction(k,M))%1
 if u==0:
  amp=(Fraction(2*(2*L+1)*U,M).__floor__(),Fraction(2*(2*L+1)*U,M).__ceil__())
 else:
  den=sine(u)
  primary=divide(sine((2*L+1)*u),den,M)
  ratio=divide(sine((2*q+1)*u),den,2*q+1)
  amp=scale(mul(primary,power(ratio,s)),2)
 phase=Fraction(-2*((N-1)//2)*ell,N)
 return mul(amp,sine(Fraction(1,2)+phase)),mul(amp,sine(phase))
