#!/usr/bin/env python3
"""Independent exact controls; no author output is written or imported before verification."""
from pathlib import Path
from fractions import Fraction as F
import json, hashlib, sys, importlib.util
D=Path('/workspace/shared/alg034_centered_support_obstruction_20261019_1527')
BV=Path('/workspace/shared/centered_bounded_variation_20261018_1330')
OUT=Path(__file__).resolve().parent
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((D/'MANIFEST.json').read_text())
assert H(D/'MANIFEST.json')=='30b228192c017fcf49c35df56dd19fe52dfe49dd6a27dec4731e21fce4f3e2a4'
for n,h in manifest.items():assert H(D/n)==h,n
b=json.loads((D/'SOURCE_BINDINGS.json').read_text())
for v in b['bindings']:assert H(D/v['snapshot'])==H(Path(v['local_source']))==v['sha256']
bvm=json.loads((BV/'MANIFEST.json').read_text())
for n,h in bvm.items():assert H(BV/n)==h,n
assert H(BV/'MANIFEST.json')==b['accepted_manifest_sha256']
assert H(Path(b['owner_response_local_path']))==b['owner_response_sha256']
result={'status':'PASS_INDEPENDENT_EXACT_CHECKS','binding':{'packet_members':len(manifest),'bv_members':len(bvm),'original_bindings':len(b['bindings']),'owner_response':True}}

# Derive parameters independently from support length and normalization.
plans=[]
for a in (0,2):
 for r in list(range(a+3,65))+[128,256,512]:
  m=4*r;M=2**m;N=M//4;lam=2**a;K=2**(2*r)//(16*lam**2);J=N//K
  h=((J-1).bit_length()+1)//2
  assert J==2**(2*h) and h==r+a+1
  eps=F(lam,2**r);amp=F(J,2**(h+2*r))
  assert amp==2*eps and K*amp**2==F(1,4)
  assert (N//2-1)%K==K-1 and K>=4
  B=2*J;C=2**(3*r+a)
  assert C*C*(4*J)==N*B*B and (C-1)**2*(4*J)<N*B*B
  assert C*2**r==lam*M
  P=16*m+16;bits=P+a-r
  assert 2*((2**(bits-1)-1)**2)<(2**P*eps)**2
  # P-grid component rounding has squared complex error <= 2^(-2P-1).
  # R>1/2 suffices, using the minimal limiting norm on the RHS.
  assert F(1,2**(2*P+1)) < F(lam**2,2**(2*r+2))
  assert 160*m+4<M
  for k in (0,1,2,3,M//2,M-1):
   hh=80*m+1
   r0=-(-N*(k-hh-1)//M);r1=-(-N*(k+hh+1)//M)
   assert r1-r0==40*m+1<N
  plans.append({'r':r,'lambda':lam,'m':m,'K':K,'h':h,'cutoff':C*2**r,'min_numerator_bits':bits})
result['independent_plans']={'count':len(plans),'max_m':max(p['m'] for p in plans),'plans':plans}

# Literal dense-coordinate direct sums in the exact cyclotomic basis.
# X represents exp(2 pi i/M); every input coordinate, including zeros, is visited.
def dense_sum(m,K,k):
 M=2**m;N=M//4;a0=(N-1)//2;p={}
 for j in range(N):
  c=int(j%K==0)
  if c:
   e=((a0-j)*k)%M
   if e>=M//2:e-=M//2;c=-c
   p[e]=p.get(e,0)+c
 return {e:c for e,c in p.items() if c}
def monomial(m,e,c):
 M=2**m;e%=M
 if e>=M//2:e-=M//2;c=-c
 return {e:c}
m=12;M=2**m;N=M//4;K=4;J=N//K
selected={M//K*i:i for i in range(K)};nonzero=[]
for k in range(M):
 p=dense_sum(m,K,k)
 want_nonzero=(k%4!=0 or k in selected)
 assert bool(p)==want_nonzero
 if p:nonzero.append(k)
 if k in selected:assert p==monomial(m,-selected[k]*M//K,J)
assert len(nonzero)==3*M//4+K
result['full_spectrum_exact']={'m':m,'M':M,'dense_coordinate_visits':M*N,'nonzero_coordinates':len(nonzero),'zero_coordinates':M-len(nonzero),'selected_coordinates':list(selected),'selected_squared_energy':'1/4','alias_grid_zero_count':N-K}
more=[]
for r,a in ((4,0),(5,2)):
 m=4*r;M=2**m;N=M//4;K=2**(2*r-4-2*a);J=N//K
 for ell in range(K):
  assert dense_sum(m,K,M//K*ell)==monomial(m,-ell*M//K,J)
 more.append({'m':m,'lambda':2**a,'selected':K,'dense_coordinate_visits':N*K})
result['additional_exact_selected']=more
# Phase controls at the smallest instance: an uncentered positive real comb
# gives a positive monomial; the centered coefficient at ell=1 is negative i.
assert dense_sum(12,4,1024)=={1024:-256}
assert dense_sum(12,4,1024)!={0:256}
assert dense_sum(12,4,1024)!={1024:256}
result['phase_controls']={'uncentered_substitution_rejected':True,'opposite_sign_rejected':True}

# Four exactly dyadic selected targets. Equality at epsilon is admissible;
# actual 2 epsilon omissions, zero substitutions, and wrong-location moves fail.
eps=F(1,8);A=F(1,4);true={0:(A,0),1024:(0,-A),2048:(-A,0),3072:(0,A)}
def fails(Z):
 return [k for k,(x,y) in true.items() if (Z.get(k,(0,0))[0]-x)**2+(Z.get(k,(0,0))[1]-y)**2>eps**2]
for k in true:
 z=dict(true);del z[k];assert fails(z)==[k]
 z=dict(true);z[k]=(0,0);assert fails(z)==[k]
 z=dict(true);z[k+1]=z.pop(k);assert fails(z)==[k]
 z={j:(x/2,y/2) for j,(x,y) in true.items()};assert not fails(z)
assert eps**2<=eps**2 and A**2>eps**2
# All numerators with magnitude bit length less than B have too small a
# complex modulus to meet distance epsilon from a 2 epsilon selected target.
P=208;B=P-3
assert 2*(2**(B-1)-1)**2 < (2**P*eps)**2
result['threshold_controls']={'omissions':4,'retained_zero_failures':4,'wrong_location_failures':4,'legal_exact_threshold_values':4,'bit_length_floor':B}

# Independent row-first stencil audit of all columns; no endpoint formula is
# used to assemble these sets/counts.
m=12;M=2**m;N=M//4;hh=80*m+1;t=2*hh+2
counts=[0]*M;want={0,1,1024,2048,3072,M-1};rows={k:set() for k in want}
for ell in range(N):
 seen=set()
 for offset in range(-hh,hh+2):
  k=(ell*M//N+offset)%M
  assert k not in seen;seen.add(k);counts[k]+=1
  if k in want:rows[k].add(ell)
assert set(counts)=={40*m+1}
# Reexecute the unchanged accepted iterator for actual computed one-row
# medians. This is an iterator/median test; it makes no source-success claim.
sys.path.insert(0,str(BV/'runtime'))
from outer_wrapper import Header,Outer,ReceiptLedger
from sparse_output import produce_medians
L=ReceiptLedger();support=tuple(sorted(want));value_rows=(tuple((0,0) for _ in support),)
med=produce_medians(M,16*m+16,support,value_rows,L)
outer=Outer(Header(N,M,5,16*m+16),med,L)
got={k:set() for k in support};count=0
for incidence in outer.incidences():
 assert incidence.ordinal==count;count+=1
 assert incidence.ell not in got[incidence.k];got[incidence.k].add(incidence.ell)
assert got==rows and count==len(support)*(40*m+1) and outer.kernel is None
result['incidence_audit']={'all_columns':M,'row_first_visits':N*t,'per_column':40*m+1,'unchanged_iterator_columns':len(support),'unchanged_iterator_incidences':count,'scalar_setup':False,'coefficient_evaluations':0,'receipt':L.report()}

# Replicate author checks only after the complete hash audit; do not invoke
# main(), which would overwrite the author's CHECK_RESULTS.json.
spec=importlib.util.spec_from_file_location('frozen_author_checks',D/'check_obstruction.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
assert not hasattr(mod,'bv')
mod.verify_sources()
sys.path.insert(0,str(D/'runtime'))
import bounded_variation
from interval_core import Ledger,Rejected
mod.bv=bounded_variation;mod.Ledger=Ledger;mod.Rejected=Rejected
saved=json.loads((D/'CHECK_RESULTS.json').read_text())
replica={'status':'PASS_EXACT_CONTRACT_OBSTRUCTION_CHECKS','source_binding':mod.verify_sources(),
 'structural_parameter_checks':34,'parameter_plans':[mod.params(r,a) for a in (0,2) for r in list(range(a+3,17))+[32,64,128,256]],
 'direct_centered_selected_checks':[mod.direct_selected(mod.params(3,0)),mod.direct_selected(mod.params(4,0)),mod.direct_selected(mod.params(5,2))],
 'complete_alias_grid':mod.alias_grid_check(mod.params(3,0)),
 'source_controls':mod.source_controls(),'omission_controls':mod.omission_controls(),
 'no_general_provider_or_outer_execution_claim':True}
assert replica==saved
result['frozen_checks_reproduction']={'entire_result_equal':True,'default_rejections':2,'recognition_only_diagnostics':2,'author_files_written':False}
for n,h in manifest.items():assert H(D/n)==h,n
(OUT/'INDEPENDENT_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='independent_plans'},indent=2))
