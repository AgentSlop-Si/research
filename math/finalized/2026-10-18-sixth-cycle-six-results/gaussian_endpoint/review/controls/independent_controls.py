#!/usr/bin/env python3
"""New independent transcription tests; never loads historical research code."""
import hashlib, json, math, platform, random
from pathlib import Path
import sympy as s
import mpmath as mp
import scipy
from scipy.integrate import quad
from scipy.special import i0e

ROOT = (Path(__file__).resolve().parents[2] / 'candidate')
SEED = 202610182112
rng = random.Random(SEED)
counts = dict(manifest_files=0, original_source_copies=0, dense_projectors=0,
              exact_pivots=0, determinant_ratio_checks=0, adaptive_paths=0,
              positive_queries=0, redundant_queries=0, disk_integrals=0,
              high_precision_bound_chains=0, block_counts=0)
def simp(A): return A.applyfunc(s.cancel)
def eq(A,B): assert all(s.cancel(z)==0 for z in A-B)
def adj(A): return A.conjugate().T

def projector(P,d):
    eq(P,adj(P)); eq(P*P,P); assert s.cancel(s.trace(P))==d

# Exact sealed-packet identity, including source copies against originals.
for line in (ROOT/'MANIFEST.sha256').read_text().splitlines():
    digest, rel = line.split(maxsplit=1)
    assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==digest
    counts['manifest_files']+=1
manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
for entry in manifest['sources']:
    data=(ROOT/entry['copy']).read_bytes()
    assert data==(ROOT / entry['public_source_path']).read_bytes()
    assert len(data)==entry['bytes']
    assert hashlib.sha256(data).hexdigest()==entry['sha256']
    if 'expected_sha256' in entry: assert entry['sha256']==entry['expected_sha256']
    counts['original_source_copies']+=1

# Rational complex Householder-generated subspaces. Independently calculate
# every conditional variance as a principal determinant ratio as well as pivot.
for n in range(1,7):
    Q=s.eye(n)
    for _ in range(2):
        v=s.Matrix([rng.randint(-2,2)+s.I*rng.randint(-2,2) for _ in range(n)])
        if v==s.zeros(n,1): v[0]=1
        H=s.eye(n)-2*v*adj(v)/(adj(v)*v)[0]
        Q=simp(H*Q)
    eq(adj(Q)*Q,s.eye(n))
    for d in range(1,n+1):
        B=Q[:,:d]; original=simp(B*adj(B)); P=original
        selected=[]; prevdet=s.Integer(1)
        for q in range(d,0,-1):
            projector(P,q)
            j=max(range(n),key=lambda j:P[j,j])
            v=P[j,j]
            assert v>=s.Rational(q,n) and j not in selected
            selected.append(j)
            principal=original.extract(selected,selected)
            determinant=s.factor(principal.det())
            assert s.cancel(determinant/prevdet-v)==0
            prevdet=determinant
            P=simp(P-P[:,j]*P[j,:]/v)
            cross=original.extract(range(n),selected)
            direct=simp(original-cross*principal.inv()*adj(cross))
            eq(P,direct)
            projector(P,q-1)
            counts['exact_pivots']+=1
            counts['determinant_ratio_checks']+=1
        eq(P,s.zeros(n)); counts['dense_projectors']+=1

# Transcript-dependent coefficients, query directions, response-based stop,
# and an explicitly redundant last query. Whole-transcript least-norm solve
# is independent of the sequential update being tested.
n=6; eye=s.eye(n); branches={'stop':0,'positive':0,'negative':0}
for value in [0,s.Rational(1,3),2+s.I,-2+s.I,2-s.I,-2-s.I]:
    x=s.Matrix([value,0,1+s.I,2-s.I,-3,2*s.I])
    P=s.eye(n); m=s.zeros(n,1); rows=[]; responses=[]
    a1=eye[:,0]+s.I*eye[:,1]; queries=[a1]
    k=0
    while k<len(queries):
        a=queries[k]; y=(adj(a)*x)[0]
        v=s.cancel((adj(a)*P*a)[0]); mu=(adj(a)*m)[0]
        rows.append(adj(a)); responses.append(y)
        if v==0:
            assert s.cancel(y-mu)==0; counts['redundant_queries']+=1
        else:
            m=simp(m+P*a*(y-mu)/v)
            P=simp(P-P*a*adj(a)*P/v)
            counts['positive_queries']+=1
        if k==0:
            if s.expand(y*s.conjugate(y))<=1: branches['stop']+=1
            else:
                if s.re(y)>0:
                    a2=(1+y)*eye[:,2]+(1-s.I*y)*eye[:,3]; branches['positive']+=1
                else:
                    a2=(1+y)*eye[:,4]+(1-s.I*y)*eye[:,5]; branches['negative']+=1
                queries.extend([a2,(2+y)*a1-s.I*a2])
        k+=1
    A=s.Matrix.vstack(*rows); ids=list(A.T.rref()[1]); A0=A.extract(ids,range(n))
    inv=(A0*adj(A0)).inv(); direct=simp(adj(A0)*inv*A0)
    eq(m,direct*x); eq(P,s.eye(n)-direct)
    eq(A*m,s.Matrix(responses)); eq(A*P,s.zeros(A.rows,n))
    projector(P,n-len(ids)); assert n-len(ids)>=4
    counts['adaptive_paths']+=1
assert all(branches.values())

# Independent disk probability via polar Bessel quadrature, avoiding ncx2.
max_excess=0.; max_error=0.
for v in [.1,.7,2.]:
    for radius in [0.,.05,.4,1.3,3.]:
        bound=-math.expm1(-radius*radius/v)
        for shift in [0.,.1,.8,3.]:
            f=lambda rho: 2*rho/v*math.exp(-(rho-shift)**2/v)*i0e(2*rho*shift/v)
            probability,err=quad(f,0,radius,epsabs=1e-12,epsrel=1e-12)
            assert probability<=bound+5e-12
            max_excess=max(max_excess,probability-bound); max_error=max(max_error,err)
            counts['disk_integrals']+=1

# High-precision orientation controls, including sharp balanced rank one.
mp.mp.dps=80
for n in [1,2,3,5,16,64]:
    for d in sorted(set([1,max(1,n//3),max(1,n//2),n])):
        for radius in [mp.mpf(0),mp.mpf('0.01'),mp.mpf('.3'),mp.mpf(1),mp.mpf(3),mp.mpf(10)]:
            actual=(-mp.expm1(-radius**2))**d
            product=mp.fprod(-mp.expm1(-n*radius**2/q) for q in range(1,d+1))
            half=(-mp.expm1(-2*n*radius**2/d))**((d+1)//2)
            exponential=mp.exp(-mp.mpf(d)/2*mp.exp(-2*n*radius**2/d))
            delta=mp.mpf(d)/(2*n)
            weakened=mp.exp(-delta*n/2*mp.exp(-2*radius**2/delta))
            chain=[actual,product,half,exponential,weakened]
            assert all(a<=b+mp.mpf('1e-75') for a,b in zip(chain,chain[1:]))
            if d==1:
                balanced=-mp.expm1(-n*radius**2)
                assert abs(balanced-product)<mp.mpf('1e-75')
            counts['high_precision_bound_chains']+=1

for M in range(1,31):
    for N in range(6*M,9*M+1):
        assert s.Rational(N//M-2)>=s.Rational(N,2*M)
        assert s.Rational(N//M-2)>=s.Rational(N,M)-3
        counts['block_counts']+=1

out={'status':'PASS','seed':SEED,'counts':counts,'adaptive_branches':branches,
     'disk_diagnostics':{'max_probability_excess':max_excess,'max_quad_error':max_error},
     'versions':{'python':platform.python_version(),'sympy':s.__version__,'scipy':scipy.__version__,'mpmath':mp.__version__},
     'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
     'historical_programs_executed':False,'network_requests':False,
     'note':'Finite exact and numerical transcription controls, not a substitute for the all-N proof.'}
print(json.dumps(out,indent=2,sort_keys=True))
