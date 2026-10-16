"""Independent R18 witness check. Written for this audit; imports no packet code.

Data inputs only: root_candidate.json and a non-pickled numeric .npy witness.
Exact integer polynomial values/derivatives; independently constructed radical
Fourier enclosures; explicit rational truncation error for a smaller beta test.
"""
import json, math, time, hashlib
from pathlib import Path
from fractions import Fraction as Q
import numpy as np

root=Path(__file__).resolve().parent/'data'
EXPECTED_INPUT_HASHES = {
    'root_candidate.json': '8457f187c24ce1d0eb5ec55c5628c4d66e7e443d344848deec6a3ec4dfd30e88',
    'inverse_witness.npy': '8ba041f5c08f96b7b4604ece84142c54382dd0ab2094e9558d19ad6a55d24ada',
}
# Verify the sealed bytes of both inputs before decoding either input.
for name, expected_hash in EXPECTED_INPUT_HASHES.items():
    actual_hash = hashlib.sha256((root/name).read_bytes()).hexdigest()
    if actual_hash != expected_hash:
        raise ValueError('Input SHA-256 mismatch: '+name)
if not __debug__:
    raise RuntimeError('Run without Python -O or -OO; audit assertions are required.')
tic=time.monotonic()
rec=json.loads((root/'root_candidate.json').read_text())
assert rec['n']==16 and rec['depth']==4 and rec['branches_per_stage']==2
assert rec['precision_bits']==320 and rec['radius_power_of_two']==-100
n=16; t=4; m=n*n; P=320; D=1<<P
active=rec['active']; pars=rec['parameters_scaled']; orders=rec['orders']
assert len(pars)==320 and len(active)==256 and len(set(active))==256
assert all(type(v) is int and 0<=v<320 for v in active)
assert len(orders)==4 and all(len(o)==2 for o in orders)
assert all(sorted(o)==list(range(n)) for pair in orders for o in pair)
ar=np.array([int(p[0]) for p in pars],dtype=object).reshape(4,5,16)
ai=np.array([int(p[1]) for p in pars],dtype=object).reshape(4,5,16)

def zero(shape):return np.zeros(shape,dtype=object)
def eye():return np.eye(n,dtype=object),zero((n,n))
def mul(A,B):
    a,b=A;c,d=B
    return a@c-b@d,a@d+b@c
def outer(a,b,c,d):return np.outer(a,c)-np.outer(b,d),np.outer(a,d)+np.outer(b,c)

hs=[]; stages=[]
for k in range(t):
    hpair=[]
    for order in orders[k]:
        pos={v:i for i,v in enumerate(order)}
        hpair.append(np.array([[int(pos[i]>pos[j])-int(pos[i]<pos[j]) for j in range(n)] for i in range(n)],dtype=object))
    hs.append(hpair)
    sr=np.diag(ar[k,0]*D);si=np.diag(ai[k,0]*D)
    for a,b,h in [(1,2,hpair[0]),(3,4,hpair[1])]:
        ur,ui=outer(ar[k,a],ai[k,a],ar[k,b],ai[k,b])
        sr+=h*ur;si+=h*ui
    stages.append((sr,si))

# Each stage denominator is D^2, and all products below remain exact.
prefix=[eye()]
for s in stages:prefix.append(mul(s,prefix[-1]))
suffix=[None]*t
u=eye()
for k in range(t-1,-1,-1):suffix[k]=u;u=mul(u,stages[k])
Mr,Mi=prefix[-1]

# Form derivative by inserting its sparse stage matrix in the whole product.
# A derivative-stage denominator is D, hence total Jacobian denominator D^7.
Jr=zero((m,m));Ji=zero((m,m))
for col,idx in enumerate(active):
    k,rem=divmod(idx,5*n); block,j=divmod(rem,n)
    vr=zero((n,n));vi=zero((n,n))
    if block==0:vr[j,j]=D
    elif block in (1,3):
        inp=block+1;h=hs[k][(block-1)//2]
        vr[j,:]=h[j,:]*ar[k,inp];vi[j,:]=h[j,:]*ai[k,inp]
    else:
        out=block-1;h=hs[k][(block-2)//2]
        vr[:,j]=h[:,j]*ar[k,out];vi[:,j]=h[:,j]*ai[k,out]
    ur,ui=mul(suffix[k],mul((vr,vi),prefix[k]))
    Jr[:,col]=ur.ravel();Ji[:,col]=ui.ravel()
print('Exact center and Jacobian built',time.monotonic()-tic,flush=True)

# Separately check every derivative column by exact coefficient perturbation.
# Each single coordinate enters the product affinely, so a one-unit numerator
# perturbation changes the product numerator by the stored derivative column.
for col,idx in enumerate(active):
    k,rem=divmod(idx,5*n);block,j=divmod(rem,n)
    xr=ar.copy();xi=ai.copy();xr[k,block,j]+=1
    sr=np.diag(xr[k,0]*D);si=np.diag(xi[k,0]*D)
    for a,b,h in [(1,2,hs[k][0]),(3,4,hs[k][1])]:
        ur,ui=outer(xr[k,a],xi[k,a],xr[k,b],xi[k,b])
        sr+=h*ur;si+=h*ui
    u=eye()
    for kk,s in enumerate(stages):u=mul((sr,si) if kk==k else s,u)
    assert np.array_equal((u[0]-Mr).ravel(),Jr[:,col])
    assert np.array_equal((u[1]-Mi).ravel(),Ji[:,col])
print('All 256 exact derivative perturbations agree',time.monotonic()-tic,flush=True)

# Enclose F16 directly using sqrt(2), sqrt(2+sqrt(2))/2,
# sqrt(2-sqrt(2))/2 and quadrant symmetries, without trigonometric calls.
K=512; S=1<<K
def ceil_sqrt(v):
    k=math.isqrt(v)
    return k+(k*k<v)
lo2=math.isqrt(2*S*S);hi2=ceil_sqrt(2*S*S)
sqrt_half=(lo2//2,(hi2+1)//2)
cosine=(math.isqrt((2*S+lo2)*S)//2,(ceil_sqrt((2*S+hi2)*S)+1)//2)
sine=(math.isqrt((2*S-hi2)*S)//2,(ceil_sqrt((2*S-lo2)*S)+1)//2)
one=(S,S);zero_i=(0,0)
def neg(a):return -a[1],-a[0]
circ=[one,cosine,sqrt_half,sine,zero_i,neg(sine),neg(sqrt_half),neg(cosine),neg(one),neg(cosine),neg(sqrt_half),neg(sine),zero_i,sine,sqrt_half,cosine]
# sin(theta)=cos(pi/2-theta); F uses negative sine and normalization 1/4.
fbound=Q(0)
for i in range(n):
    for j in range(n):
        e=i*j%16; cr=circ[e];ci=neg(circ[(4-e)%16])
        mr=Q(int(Mr[i,j]),D**8);mi=Q(int(Mi[i,j]),D**8)
        re=max(abs(mr-Q(cr[0],4*S)),abs(mr-Q(cr[1],4*S)))
        im=max(abs(mi-Q(ci[0],4*S)),abs(mi-Q(ci[1],4*S)))
        fbound=max(fbound,re+im)

# Decode binary64 preconditioner entries as exact dyadic rationals.
w=np.load(root/'inverse_witness.npy',allow_pickle=False)
assert w.shape==(m,m) and w.dtype==np.dtype('complex128')
assert np.isfinite(w).all()
rs=[[float(w[i,j].real).as_integer_ratio() for j in range(m)] for i in range(m)]
iss=[[float(w[i,j].imag).as_integer_ratio() for j in range(m)] for i in range(m)]
E=max(b for rows in (rs,iss) for row in rows for a,b in row)
Br=np.array([[a*(E//b) for a,b in row] for row in rs],dtype=object)
Bi=np.array([[a*(E//b) for a,b in row] for row in iss],dtype=object)
bnorm=Q(max(int(v) for v in np.sum(abs(Br)+abs(Bi),axis=1)),E)

# Round each exact Jacobian coordinate downward to units 2^-256.
# Its induced row-sum error is bounded by 2*m*2^-256.
T=1<<256;shift=7*P-256
Rr=Jr//(1<<shift);Ri=Ji//(1<<shift)
Er,Ei=mul((Br,Bi),(Rr,Ri))
Er=np.eye(m,dtype=object)*(E*T)-Er
beta=Q(max(int(v) for v in np.sum(abs(Er)+abs(Ei),axis=1)),E*T)+bnorm*Q(2*m,T)
alpha=bnorm*fbound
L=max(int(x) for x in (abs(ar)+abs(ai)).flat)
L=(L+D-1)//D+1
B0=L+2*n*L*L;B1=1+4*n*L;B2=4*n
H=t*B0**(t-1)*B2+t*(t-1)*B0**(t-2)*B1**2
r=Q(1,1<<100)
q=beta+bnorm*H*r
selfmap=alpha+beta*r+bnorm*H*r*r/2
checks={'residual_lt_1e_minus_88':fbound<Q(1,10**88),
        'alpha_lt_1e_minus_85':alpha<Q(1,10**85),
        'beta_lt_4e_minus_9':beta<Q(4,10**9),
        'Bnorm_lt_616':bnorm<616,'L_equals_6':L==6,
        'H_equals_2782698762672':H==2782698762672,
        'q_lt_4e_minus_9':q<Q(4,10**9),'selfmap_lt_radius':selfmap<r,
        'radius_le_one':r<=1}
def rat(x):return {'numerator':str(x.numerator),'denominator':str(x.denominator),'display':float(x)}
result={'method':'independent exact integer polynomial and Jacobian evaluation; rational radical target enclosure; bounded Jacobian rounding; no supplied code executed',
 'inputs':{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in ['root_candidate.json','inverse_witness.npy']},
 'checks':checks,'passed':all(checks.values()),'fbound':rat(fbound),'alpha_bound':rat(alpha),'beta_bound':rat(beta),'Bnorm':rat(bnorm),'L':L,'H':H,'radius':rat(r),'q':rat(q),'selfmap':rat(selfmap),'seconds':time.monotonic()-tic}
out=Path(__file__).with_name('independent_result_reproduced.json');out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:({v2:v3 for v2,v3 in v.items() if v2=='display'} if isinstance(v,dict) and 'display' in v else v) for k,v in result.items()},indent=2),flush=True)
assert result['passed']

reference=json.loads(Path(__file__).with_name('independent_result.json').read_text())
exact_reference={k:v for k,v in reference.items() if k!='seconds'}
exact_result={k:v for k,v in result.items() if k!='seconds'}
if exact_reference != exact_result:
    raise AssertionError('Fresh result differs from reference in a non-timing field')
print('Reference exact-result comparison: PASS (elapsed seconds excluded)',flush=True)
