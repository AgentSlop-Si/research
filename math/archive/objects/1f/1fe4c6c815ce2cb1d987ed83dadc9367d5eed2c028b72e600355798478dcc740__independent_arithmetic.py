"""Independent exact rational moment helpers authored during the companion audit.
50-term atanh logarithm bounds and 12-term exponential with exact tail.
"""
from fractions import Fraction as Q
from math import factorial

def log_bounds(x):
    x=Q(x); k=0
    while x>2: x/=2; k+=1
    def small(y):
        z=(y-1)/(y+1)
        lo=2*sum((z**(2*j+1)/Q(2*j+1) for j in range(50)),Q())
        hi=lo+2*z**101/(101*(1-z*z))
        return lo,hi
    l,u=small(x);l2,u2=small(Q(2));l+=k*l2;u+=k*u2
    den=10**50
    return Q((l*den).numerator//(l*den).denominator,den),Q(-(-(u*den).numerator//(u*den).denominator),den)

def moment(m,W,rows,a):
    lo=hi=Q()
    for t,n in rows.items():
        l,u=log_bounds(Q(m,t)); l*=a;u*=a
        assert 0<=l<=u<1
        L=sum((l**j/factorial(j) for j in range(13)),Q())
        U=sum((u**j/factorial(j) for j in range(13)),Q())+u**13/factorial(13)/(1-u/14)
        w=Q(t*n,m*W);lo+=w*L;hi+=w*U
    return lo,hi

def js(x):
    if isinstance(x,Q):return str(x)
    if isinstance(x,dict):return {str(k):js(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [js(v) for v in x]
    return x

