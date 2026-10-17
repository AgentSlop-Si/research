#!/usr/bin/env python3
"""Independent final review: exact trace controls, no candidate executable imported/run."""
from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import json
import sympy as sp

HERE=Path(__file__).resolve().parent
CAND=HERE.parent/'source'
q=sp.Symbol('q')
expected={'PROOF.md':'33a1f1ac507f745d152a34ba6b1545d6bc4db867250c54d3dcda642d740d77d5',
          'MANIFEST.json':'34091161d95a471ed1f2468211e3c59e9f80baa0f312470c92d6a2c62f31b4ad'}
hashes={}
for name,digest in expected.items():
    actual=sha256((CAND/name).read_bytes()).hexdigest()
    assert actual==digest,(name,actual,digest)
    hashes[name]=actual
manifest=json.loads((CAND/'MANIFEST.json').read_text())
for item in manifest['files']:
    p=CAND/item['path']; data=p.read_bytes()
    assert len(data)==item['bytes']
    assert sha256(data).hexdigest()==item['sha256']

# Derive trace(J^2) from the source recurrence rather than build R_h or run
# the author's coefficient multiplication. J has diagonal a_0,...,a_(h-1),0,
# unit superdiagonal, and subdiagonal b_1,...,b_(h-1),-t.
# a_n=q^(2n)+q^(2n-1)-q^(n-1), b_n=q^(4n-3)-q^(3n-3).
def normalize(d,N):
    out=defaultdict(int)
    for e,c in d.items(): out[e%N]+=c
    return {e:c for e,c in out.items() if c}
def polynomial(d,N):
    return sp.Poly.from_dict({(e,):c for e,c in normalize(d,N).items()},q,domain=sp.ZZ)
def residual(trace,N,phase=-3):
    r=defaultdict(int)
    for e,c in trace.items(): r[e]+=c; r[e+1]-=c
    r[phase]+=4
    return polynomial(r,N).rem(sp.Poly(sp.cyclotomic_poly(N,q),q))
trace_checks=[]
for N in range(4,258,2):
    h=N//2; tr=defaultdict(int)
    for n in range(h):
        a=[(2*n,1),(2*n-1,1),(n-1,-1)]
        for e,c in a:
            for f,d in a: tr[e+f]+=c*d
    for n in range(1,h):
        tr[4*n-3]+=2; tr[3*n-3]-=2
    assert residual(tr,N).is_zero
    assert not residual(tr,N,phase=-2).is_zero
    # Last edge contributes 2*(1)*(-t), independent of N. If +2t is used
    # instead, the cleared residual at t=1 is -4*(1-q), which is nonzero.
    wrong_sign=sp.Poly(-4+4*q,q).rem(sp.Poly(sp.cyclotomic_poly(N,q),q))
    assert not wrong_sign.is_zero
    trace_checks.append({'N':N,'trace_identity':True,'wrong_phase_rejected':True,'wrong_t_sign_rejected':True})

# A symbolic affine comparison certifies every N>=44, not a finite sweep.
N=sp.Symbol('N', real=True)
affine=sp.expand(sp.Rational(7,11)*N-2-sp.Rational(9,8)*(N/2+1))
assert affine==sp.Rational(13,176)*N-sp.Rational(25,8)
assert affine.subs(N,44)==sp.Rational(1,8)
assert sp.diff(affine,N)==sp.Rational(13,176)>0

# Independently exercise the spectral estimate on exactly selected rational
# complex nodes, so roots are neither approximated nor taken from author data.
# We use direct row sums to certify sigma_min <= sqrt(m), and numerical SVD
# only as a non-certifying sanity check of the reported inequalities.
import numpy as np
node_sets=[([0,1,-1], 'zero-node legal-for-obstruction'),
           ([0,1,1], 'repeated-root singular'),
           ([1,2,3], 'real nodes'),
           ([1j,-1j,2+1j,-2j], 'complex nodes'),
           ([0,1,-1,2,-2], 'five-node case')]
spectral=[]
for nodes,label in node_sets:
    m=len(nodes); h=m-1
    V=np.array([[z**j for z in nodes] for j in range(m)],dtype=complex)
    sv=np.linalg.svd(V,compute_uv=False)
    rho=max(abs(z) for z in nodes)
    assert abs(np.linalg.norm(V.conj().T[:,0])-m**0.5)<1e-12
    assert sv[0]+1e-12>=rho**h
    assert sv[-1]<=m**0.5+1e-12
    repeated=len(set(nodes))<m
    if repeated:
        assert sp.Matrix([[z**j for z in nodes] for j in range(m)]).det()==0
        kappa='infinite (exact repeated columns)'
    else:
        kappa=float(sv[0]/sv[-1])
        assert kappa+1e-10>=rho**h/m**0.5
    spectral.append({'case':label,'m':m,'kappa_sanity_only':kappa,'spectral_inequalities':True})

out={'status':'PASS', 'candidate_hashes':hashes, 'manifest_members_verified':len(manifest['files']),
     'exact_recurrence_trace_cases':trace_checks,
     'affine_constant_proof':{'expression':str(affine),'value_at_44':'1/8','slope':'13/176'},
     'independent_spectral_sanity_cases':spectral,
     'limits':['Candidate code was inspected as text only and was not imported or executed.',
               'The recurrence trace checks are finite exact controls, not an all-degree proof.',
               'The arbitrary-node SVD checks are numerical sanity checks, not spectral certificates.',
               'Copied source hashes were verified; remote GitHub source was not re-fetched.']}
(HERE/'CONTROL_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'manifest_members_verified':len(manifest['files']),'exact_trace_cases':len(trace_checks),'spectral_cases':len(spectral)},indent=2))
