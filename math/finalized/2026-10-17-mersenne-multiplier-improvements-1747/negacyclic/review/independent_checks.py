"""Review-only mathematical controls; imports/executes no supplied/candidate code.
Python multiplication, modular exponentiation and dense DFTs are test oracles.
No runtime/bit-complexity conclusion is inferred from these finite tests.
"""
import hashlib, json, math, random
from collections import Counter
from itertools import product
from pathlib import Path
from zipfile import ZipFile

out=Path(__file__).parent
candidate=Path(__file__).resolve().parent.parent/'source'
counts=Counter(); rng=random.Random(174120261017)
for name, expected in json.loads((candidate/'MANIFEST.json').read_text()).items():
    assert hashlib.sha256((candidate/name).read_bytes()).hexdigest()==expected
    counts['manifest_bindings']+=1
bindings=json.loads((candidate/'SOURCE_BINDINGS.json').read_text())
import os
archive=Path(os.environ.get('MERSENNE_EXTERNAL_INPUTS', str(Path(__file__).resolve().parents[2]/'external-inputs')))/'source.zip'
assert hashlib.sha256(archive.read_bytes()).hexdigest()==bindings['archive_sha256']
with ZipFile(archive) as z:
    for entry in bindings['read_members']:
        assert hashlib.sha256(z.read(entry['path'])).hexdigest()==entry['sha256']
        counts['source_member_bindings']+=1

def coeff(a,b):
    k=len(a); c=[0]*k
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            c[(i+j)%k]+=(1 if i+j<k else -1)*x*y
    return c

def decode(c,k,B,Q):
    S=(B-1)**2
    for j,v in enumerate(c):
        lo=-(k-1-j)*S; hi=(j+1)*S
        assert lo<=v<=hi
        u=v%Q
        assert (u if u<=hi else u-Q)==v
        counts['coefficient_decodes']+=1

for B,k in [(2,1),(2,2),(2,4),(3,2),(3,4),(4,2),(5,2)]:
    vectors=list(product(range(B),repeat=k)); D=k*(B-1)**2
    for a in vectors:
        for b in vectors:
            c=coeff(a,b); decode(c,k,B,D+1)
            assert (sum(a[i]*B**i for i in range(k))*sum(b[i]*B**i for i in range(k))-sum(c[i]*B**i for i in range(k)))%(B**k+1)==0
            counts['negacyclic_products']+=1
# Strict > is necessary for this complete interval criterion.
assert 1%2==(-1)%2
counts['strict_bound_negative_control']+=1

for p in [3,5,7,9,15,31]:
    for s in range(2,25,2):
        Q=(p**s+1)//2
        assert Q%2==1 and p**s%Q==Q-1
        digits=[(p+1)//2]+[(p-1)//2]*(s-1)
        assert sum(x*p**j for j,x in enumerate(digits))==Q
        for K in [2,4,8,16]:
            if s%K: continue
            theta=pow(p,s//K,Q); omega=theta**2%Q
            assert pow(theta,K,Q)==Q-1
            for ell in range(1,K):
                assert sum(pow(omega,ell*j,Q) for j in range(K))%Q==0
            for u in [0,1,Q-2,Q-1]+[rng.randrange(Q) for _ in range(8)]:
                h=u
                for _ in range(K.bit_length()-1): h=(h+(Q if h%2 else 0))//2
                assert (K*h-u)%Q==0
                for a in [0,1,s-1,s,s+1,2*s-1]:
                    e=a%s; sign=-1 if a>=s else 1
                    hi,lo=divmod(u,p**(s-e)) if e else (0,u)
                    folded=sign*(lo*p**e-hi)
                    assert folded%Q==u*pow(p,a,Q)%Q
                    assert -2*Q<folded<2*Q
                    counts['odd_power_shift_controls']+=1
                counts['odd_halving_controls']+=1
            counts['principal_root_cases']+=1

native_nodes=Counter()
def native(x,y,p,s,half):
    Q=(p**s+1)//(2 if half else 1)
    assert 0<=x<Q and 0<=y<Q
    plan=None
    if s>12:
        for K in [8,4]:
            if s%K: continue
            d=s//K; B=p**d; D=K*(B-1)**2
            t=K
            while (p**t+1)//(2 if half else 1)<=D: t+=K
            if t<s:
                plan=(K,d,B,t); break
    if plan is None: return x*y%Q
    K,d,B,t=plan; R=(p**t+1)//(2 if half else 1)
    theta=pow(p,t//K,R); omega=theta**2%R
    def split(v):
        a=[]
        for _ in range(K): v,digit=divmod(v,B); a.append(digit)
        assert v==0
        return a
    # Binary Q-1 is the exceptional residue p**s, outside K ordinary blocks.
    if not half and x==Q-1: return -y%Q
    if not half and y==Q-1: return -x%Q
    a,b=split(x),split(y)
    def dft(a,sgn): return [sum(v*pow(omega,sgn*j*l,R) for j,v in enumerate(a))%R for l in range(K)]
    fa=dft([v*pow(theta,j,R)%R for j,v in enumerate(a)],1)
    fb=dft([v*pow(theta,j,R)%R for j,v in enumerate(b)],1)
    raw=dft([native(u,v,p,t,half) for u,v in zip(fa,fb)],-1)
    c=[]
    for j,u in enumerate(raw):
        u=u*pow(K,-1,R)*pow(theta,-j,R)%R
        hi=(j+1)*(B-1)**2
        c.append(u if u<=hi else u-R)
    assert c==coeff(a,b)
    carry=0; digits=[]
    for v in c:
        carry,digit=divmod(v+carry,B); digits.append(digit)
    low=sum(v*B**j for j,v in enumerate(digits))
    folded=low-carry
    assert -2*Q<folded<2*Q
    native_nodes['odd' if half else 'binary']+=1
    return folded%Q

for p,half in [(2,False),(3,True),(7,True),(15,True),(31,True)]:
    for s in [16,24,32,40,64,96]:
        Q=(p**s+1)//(2 if half else 1)
        for x,y in [(0,0),(1,Q-1),(Q-1,Q-1),(Q-2,Q-3)]+[(rng.randrange(Q),rng.randrange(Q)) for _ in range(12)]:
            assert native(x,y,p,s,half)==x*y%Q
            counts['recursive_native_products']+=1

# Exact parameter-chain checks at sizes much larger than feasible arithmetic.
# For m>=2, bit_length(K*(2**m-1)**2)=2*m+log2(K).
def ideal_K(n):
    L=n.bit_length()-1
    z=max(1,math.isqrt(n)//L)
    return 1<<(z.bit_length()-1)
chains=[]
for exponent in [32,64,128,256,512,1024,2048,4096]:
    n=1<<exponent; n0=n; chain=[]
    while n>=1<<24:
        K=ideal_K(n); assert n%K==0
        m=n//K; b=2*m+K.bit_length()-1
        r=K*((b+K-1)//K)
        assert 0<r<n and r%K==0
        nxt=ideal_K(r)
        assert K>=nxt and r%nxt==0
        chain.append({'log2_n':n.bit_length()-1,'log2_K':K.bit_length()-1,'log2_r':r.bit_length()-1})
        counts['rounded_recursion_transitions']+=1
        n=r
    chains.append({'initial_log2_n':exponent,'levels_above_2pow24':len(chain),'last_n':n,'chain':chain})
res={'status':'PASS','counts':dict(counts),'recursive_transform_nodes':dict(native_nodes),'parameter_chains':chains,'candidate_manifest_sha256':hashlib.sha256((candidate/'MANIFEST.json').read_bytes()).hexdigest(),'supplied_code_executed':False,'candidate_code_executed':False,'scope':'Independent finite exact controls; no complexity or novelty inference from tests.'}
(out/'RESULTS.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps({k:v for k,v in res.items() if k!='parameter_chains'},indent=2))
