"""Independent exact interval proof of the supplied variable-pole N4 root.

Uses directed integer-rounded rectangular intervals at 192-bit precision,
and quotient-rule derivatives of the four-term cyclic Green formula.
No constructor code, numerical library, or uploaded program is imported.
"""
from pathlib import Path
import json, hashlib

HERE=Path(__file__).resolve().parent
RAW_PATH=HERE/'VARIABLE_POLES_DYADIC_CERTIFICATE.json'
raw=json.loads(RAW_PATH.read_text())
PREC=192
S=1<<PREC
SHIFT=PREC-raw['precision_bits']
assert SHIFT>=1

def ceil(n,d):
    assert d>0
    return -((-n)//d)

class R:
    __slots__=('lo','hi')
    def __init__(self,lo,hi=None):
        self.lo=int(lo);self.hi=self.lo if hi is None else int(hi)
        assert self.lo<=self.hi
    def __add__(a,b):return R(a.lo+b.lo,a.hi+b.hi)
    def __neg__(a):return R(-a.hi,-a.lo)
    def __sub__(a,b):return a+-b
    def __mul__(a,b):
        v=[a.lo*b.lo,a.lo*b.hi,a.hi*b.lo,a.hi*b.hi]
        return R(min(v)//S,ceil(max(v),S))
    def sq(a):
        low=0 if a.lo<=0<=a.hi else min(a.lo*a.lo,a.hi*a.hi)
        return R(low//S,ceil(max(a.lo*a.lo,a.hi*a.hi),S))
    def inverse(a):
        assert not a.lo<=0<=a.hi
        # Reciprocal reverses order on each zero-free real interval.
        if a.lo>0:return R(S*S//a.hi,ceil(S*S,a.lo))
        return -((-a).inverse())
    def upper(a):return max(abs(a.lo),abs(a.hi))
    def zero_free(a):return a.lo>0 or a.hi<0

class C:
    __slots__=('re','im')
    def __init__(self,re,im=None):
        self.re=re if isinstance(re,R) else R(re)
        self.im=R(0) if im is None else im if isinstance(im,R) else R(im)
    def __add__(a,b):return C(a.re+b.re,a.im+b.im)
    def __neg__(a):return C(-a.re,-a.im)
    def __sub__(a,b):return a+-b
    def __mul__(a,b):return C(a.re*b.re-a.im*b.im,a.re*b.im+a.im*b.re)
    def inverse(a):
        den=a.re.sq()+a.im.sq()
        assert den.lo>0, 'A complex denominator rectangle was not certified zero-free'
        v=den.inverse()
        return C(a.re*v,-a.im*v)
    def bound_real_sup(a):return max(a.re.upper(),a.im.upper())
    def complex_operator_bound(a):return a.re.upper()+a.im.upper()
    def zero_free(a):return a.re.zero_free() or a.im.zero_free()

ZERO=C(0);ONE=C(S)
def scalar(n):return C(n*S)
def matrix(n,m):return [[ZERO for j in range(m)]for i in range(n)]
def eye(n):return [[ONE if i==j else ZERO for j in range(n)]for i in range(n)]
def mm(A,B):
    out=matrix(len(A),len(B[0]))
    for i in range(len(A)):
        for j in range(len(B[0])):
            v=ZERO
            for k in range(len(B)):v=v+A[i][k]*B[k][j]
            out[i][j]=v
    return out
def scale(z,A):return [[z*v for v in row]for row in A]
def plus(A,B):return [[x+y for x,y in zip(ar,br)]for ar,br in zip(A,B)]
def minus(A,B):return [[x-y for x,y in zip(ar,br)]for ar,br in zip(A,B)]
def diag(vals):return [[vals[i] if i==j else ZERO for j in range(len(vals))]for i in range(len(vals))]
def product(factors):
    out=factors[0]
    for a in factors[1:]:out=mm(out,a)
    return out
def flat(A):return [v for row in A for v in row]

order=[0,2,1,3]
position={j:k for k,j in enumerate(order)}
def green(p,nonaffine=False):
    powers=[ONE]
    for k in range(6):powers.append(powers[-1]*p)
    den=ONE-powers[4]
    assert den.zero_free()
    dinv=den.inverse();d2=dinv*dinv
    value=[powers[k]*dinv for k in range(4)]
    deriv=[]
    for k in range(4):
        numerator=scalar(4)*powers[k+3]
        if k:numerator=numerator+scalar(k)*powers[k-1]*den
        deriv.append(numerator*d2)
    distance=lambda i,j:((position[i]-position[j]) if nonaffine else (i-j))%4
    return [[value[distance(i,j)]for j in range(4)]for i in range(4)], [[deriv[distance(i,j)]for j in range(4)]for i in range(4)], den

unit=[ONE,C(0,S),-ONE,C(0,-S)]
FOURIER=[[unit[i*j%4]for j in range(4)]for i in range(4)]
def evaluate(z,derivatives):
    H=[];DH=[];denominators=[]
    for k in range(3):
        p,q,t=z[3*k:3*k+3]
        G,Gp,dp=green(p)
        J,Jq,dq=green(q,True)
        H.append(plus(G,scale(t,J)))
        DH.append([Gp,scale(t,Jq),J])
        denominators.extend([dp,dq])
    L=diag(z[9:13]);M=diag([ONE]+z[13:16])
    factors=[H[0],L,H[1],M,H[2]]
    f=flat(minus(product(factors),FOURIER))
    if not derivatives:return f,None,H,denominators
    cols=[]
    for k in range(3):
        for replacement in DH[k]:
            fs=factors.copy();fs[2*k]=replacement
            cols.append(flat(product(fs)))
    for k in range(4):
        vals=[ZERO]*4;vals[k]=ONE
        fs=factors.copy();fs[1]=diag(vals)
        cols.append(flat(product(fs)))
    for k in range(1,4):
        vals=[ZERO]*4;vals[k]=ONE
        fs=factors.copy();fs[3]=diag(vals)
        cols.append(flat(product(fs)))
    return f,[[cols[j][i]for j in range(16)]for i in range(16)],H,denominators

rho=int(raw['radius_numerator'])<<SHIFT
assert rho%2==0
centers=[(int(re)<<SHIFT,int(im)<<SHIFT)for re,im in raw['center']]
z0=[C(re,im)for re,im in centers]
# The full rectangle product contains the original Euclidean polydisc.
box=[C(R(re-rho,re+rho),R(im-rho,im+rho))for re,im in centers]
preconditioner=[[C(int(re)<<SHIFT,int(im)<<SHIFT)for re,im in row]for row in raw['preconditioner']]
f0,_,_,_=evaluate(z0,False)
Cf0=mm(preconditioner,[[v]for v in f0])
eta=max(row[0].bound_real_sup()for row in Cf0)
_,J,H,denominators=evaluate(box,True)
error=minus(eye(16),mm(preconditioner,J))
q=max(sum(entry.complex_operator_bound()for entry in row)for row in error)
assert q<S
small=rho//2
assert eta*S+q*small<small*S
assert all(z.zero_free()for z in box)
assert all(v.zero_free()for v in denominators)
assert all(v.zero_free()for h in H for v in flat(h))
commutators=[]
for i,j in [(0,1),(0,2),(1,2)]:
    comm=minus(mm(H[i],H[j]),mm(H[j],H[i]))
    locations=[[u,v]for u in range(4)for v in range(4)if comm[u][v].zero_free()]
    assert locations
    commutators.append({'stages':[i,j],'nonzero_entry_witnesses':locations})

out={
    'verified':True,
    'constructor_data_sha256':hashlib.sha256(RAW_PATH.read_bytes()).hexdigest(),
    'arithmetic':'192-bit integer-directed rectangular real intervals; no floating-point predicates',
    'derivatives':'Independent quotient rule on p^d/(1-p^4)',
    'scale':str(S),'original_radius_scaled':str(rho),
    'eta_numerator':str(eta),'q_numerator':str(q),
    'self_map_half_box_left':str(eta*S+q*small),
    'self_map_half_box_right':str(small*S),
    'all_pole_denominators_and_parameters_nonzero':True,
    'all_masks_and_stage_entries_nonzero':True,
    'noncommuting_stages':commutators,
    'claim':'The half-radius real rectangle maps strictly into itself and is contractive. Its unique exact zero lies inside the supplied Euclidean polydisc. The full-radius rectangle contains that polydisc and is also contractive, so the zero is unique in the supplied polydisc.',
    'limits':'N4 only; stage poles and couplings vary independently. No growing-length construction or faster FFT is certified.'
}
(HERE/'VARIABLE_POLES_INDEPENDENT_REVIEW.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
