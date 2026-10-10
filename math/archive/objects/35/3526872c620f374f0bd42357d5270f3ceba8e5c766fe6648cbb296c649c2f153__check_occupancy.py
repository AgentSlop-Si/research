"""Independent exact occupancy checks, freshly authored; no source code imported."""
import itertools,json,math
from fractions import Fraction

def observed(M,N,bits):
    bysize={1:set()};stack=[tuple(bits[i*N:(i+1)*N]) for i in range(M)]
    while stack:
        a=stack.pop();m=len(a);bysize.setdefault(m,set()).add(a)
        if m>1:stack.extend([a[::2],a[1::2]])
    return sum((m//2)*len(v) for m,v in bysize.items() if m>1)

def formula(M,N):
    K=M*N;s=Fraction(0)
    for t in range(1,N.bit_length()):
        m=1<<t;q=1<<m;r=K//m
        s+=(m//2)*q*(1-Fraction(q-1,q)**r)
    return s

checks=[]
for M,N in [(1,2),(1,4),(2,2),(2,4),(1,8),(2,8),(4,4)]:
    total=sum(observed(M,N,bits) for bits in itertools.product([0,1],repeat=M*N))
    mean=Fraction(total,1<<(M*N));assert mean==formula(M,N)
    checks.append(dict(M=M,N=N,expected_fraction=str(mean),cases=1<<(M*N)))

def approx_per_K(L,A):
    # M=N^A, total K=2^R, and every term computed stably on log scale.
    R=(A+1)*L;total=0.0
    for t in range(1,L+1):
        m=1<<t
        # Term after dividing by K/2 is (q/r)*(1-(1-1/q)^r).
        if m>R+60:ratio=1.0
        elif m<R-60:ratio=2.0**(m-R+t)
        else:
            qinv=2.0**(-m) if m<1074 else 0.0
            loglambda=(R-t-m)*math.log(2)
            lam=math.exp(loglambda) if loglambda<700 else math.inf
            ratio=-math.expm1(-lam)/lam if lam and math.isfinite(lam) else (1 if lam==0 else 0)
            if m<50:
                r=2.0**(R-t)
                ratio=-math.expm1(r*math.log1p(-qinv))/(r*qinv)
        total+=ratio
    return total
checks2=[]
for A in [0,1,3]:
 for L in [16,32,64,128,256,512,1024]:
    v=approx_per_K(L,A)
    checks2.append(dict(log2_N=L,M_exponent=A,twice_expected_per_MN=v,main_term=L-math.log2((A+1)*L),offset=v-(L-math.log2((A+1)*L)),retained_fraction=v/L))
print(json.dumps(dict(exact_exhaustive=checks,asymptotic_numeric=checks2),indent=2))
