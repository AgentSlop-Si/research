"""Independent rational interval review written 2026-10-17; no imports from prior work."""
from fractions import Fraction as Q
from decimal import Decimal, localcontext
from pathlib import Path
import hashlib, json
H={1:349604,2:60192,3:62585,4:20448,5:11808,7:7,8:1152,48:4866}
M,W=73,14336

def log_unit(x,N=70):
    assert 1 <= x <= 2
    z=(x-1)/(x+1)
    low=2*sum((z**(2*j+1)/Q(2*j+1) for j in range(N)),Q(0))
    tail=2*z**(2*N+1)/(Q(2*N+1)*(1-z*z))
    return low,low+tail

def log_interval(x):
    count=0
    while x>=2:
        x/=2;count+=1
    a,b=log_unit(x);c,d=log_unit(Q(2))
    return a+count*c,b+count*d

def exp_interval(lo,hi,degree=18):
    assert 0<=lo<=hi<1
    def terms(x):
        value=Q(1);total=value
        for j in range(1,degree+1):
            value*=x/Q(j);total+=value
        first_omitted=value*x/Q(degree+1)
        return total,total+first_omitted/(1-x/Q(degree+2))
    return terms(lo)[0],terms(hi)[1]

def show(x):
    with localcontext() as ctx:
        ctx.prec=45
        return str(Decimal(x.numerator)/Decimal(x.denominator))

def moment(a):
    low=high=Q(0)
    for r,h in H.items():
        l,u=log_interval(Q(M,r));l,u=exp_interval(a*l,a*u)
        weight=Q(r*h,W*M);low+=weight*l;high+=weight*u
    return low-1,high-1

receipt={'rank_count':sum(H.values()),'rank_mass':sum(r*h for r,h in H.items()),'denominator':W*M,'moments':{},'method':'Fresh range-reduced atanh with geometric tail; degree-18 exponential Taylor bounds; all deciding inequalities exact rational.'}
for name,a,sign in [('lower',Q('0.00167546267680'),-1),('upper',Q('0.00167546267682'),1),('delta',Q('0.0016754'),-1)]:
    l,u=moment(a)
    assert l<=u
    verified=(u<0) if sign<0 else (l>0)
    assert verified
    receipt['moments'][name]={'a':str(a),'lower_minus_one':show(l),'upper_minus_one':show(u),'sign_verified_exactly':verified}
receipt['absorption_gap']=str(Q('0.00167546267680')-Q('0.0016754'))
receipt['percent_larger_exponent_saving']=show(100*(Q('0.0016754')/Q('0.0012331685')-1))
receipt['limitations']=['Only validates stated histogram arithmetic; no physical macro or exact-array interface acceptance.','No supplied historical code imported or executed.','No formal verification or practical-runtime assertion.']
Path(__file__).with_name('fresh_r19_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
