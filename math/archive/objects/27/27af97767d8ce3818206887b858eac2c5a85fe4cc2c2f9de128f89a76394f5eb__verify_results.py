#!/usr/bin/env python3
"""Verify pinned inputs, complete tested-word comparison, and charged assembly."""
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
from hashlib import sha1,sha256
from math import comb
import gzip,importlib.util,json,sys
ROOT=Path(__file__).resolve().parent;UP=ROOT/'upstream'
sys.path.insert(0,str(UP/'research/pair-assembly'))
sys.path.insert(0,str(UP/'scripts/experiments'))
import balanced_assembly as balanced
import binary_frame_math as arithmetic
from independent_arithmetic import moment,js

def main():
 source=json.loads((ROOT/'source_manifest.json').read_text());verified=[]
 for f in source['files']:
  p=UP/f['path']
  assert p.is_file(), 'Missing pinned source: '+f['path']
  raw=p.read_bytes();digest=sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
  assert digest==f['git_blob_sha'],f['path'];verified.append(f['path'])
 official=json.loads((UP/'research/matrix-exponent-synthesis/candidate/arithmetic.json').read_text())
 base=json.loads((UP/'research/pair-assembly/frame/frame-certificate.json').read_text())
 axes=[];axis_checks={}
 for h in (23,25):
  b=json.loads((ROOT/'results'/f'baseline-{h}/receipt.json').read_text())
  c=json.loads((ROOT/'results'/f'carrier-{h}/receipt.json').read_text())
  bw=gzip.decompress((ROOT/'results'/f'baseline-{h}/word.json.gz').read_bytes())
  cw=gzip.decompress((ROOT/'results'/f'carrier-{h}/word.json.gz').read_bytes())
  assert b['profile']==official['source_profile']['axes'][(0 if h==23 else 1)]
  if h==23:assert bw==cw and b['profile']==c['profile']
  else:
   delta={r:cv-bv for r,(bv,cv) in enumerate(zip(b['profile']['blocks'],c['profile']['blocks'])) if cv!=bv}
   assert delta=={1:2,3:2,4:1,5:-1,7:-1}
  assert b['profile']['R']==c['profile']['R']
  assert b['profile']['rank_sum']==c['profile']['rank_sum']
  assert arithmetic.exactness(h)['modulus_gaps'][2]>0
  axis_checks[h]=dict(word_byte_equality=bw==cw,word_sha256=sha256(cw).hexdigest(),baseline_word_sha256=sha256(bw).hexdigest(),
   profile_block_changes={r:cv-bv for r,(bv,cv) in enumerate(zip(b["profile"]["blocks"],c["profile"]["blocks"])) if cv!=bv},
   roles=c['compiled']['roles'],full_basis_vectors=c['replay']['full_basis_vectors'],
   word_length=c['replay']['word_length'],distinct_matrices=c['profile']['distinct_matrices'],
   crt_matrices=c['profile']['crt_matrices'],crt_disagreements=c['profile']['crt_disagreements'],
   stats=c['compiled']['stats'])
  axes.append(c['profile'])
 m=575;N=comb(23,3)*comb(25,3)
 W=2*N+sum(N//f['v']*f['R'] for f in axes);L=sum(N//f['v']*f['loss'] for f in axes)
 parts={'data':Counter({1:18*N,21:2*N,17:2*N,481:2*N}),'paid_endpoint_copy':Counter({1:N})}
 for f in axes:
  h=f['h'];rep=N//f['v'];bank=rep*f['R']
  assert f['blocks'][h]==0
  assert sum(t*n for t,n in enumerate(f['blocks']))==h*f['R']+f['loss']==f['rank_sum']
  parts[f'internal_{h}']=Counter({t:n*rep for t,n in enumerate(f['blocks']) if t and n})
  parts[f'exterior_{h}']=Counter({h:bank,m-2*h:bank})
  parts[f'data_growth_{h}']=Counter({1:2*N,h-2:2*N})
 rows=sum(parts.values(),Counter());mass=sum(t*n for t,n in rows.items())
 oldrows={int(t):n for t,n in official['source_profile']['child_multiplicities'].items()}
 assert {t:rows[t]-oldrows.get(t,0) for t in set(rows)|set(oldrows) if rows[t]!=oldrows.get(t,0)}=={1:3542,3:3542,4:1771,5:-1771,7:-1771}
 assert (W,L,mass,m*W-mass,max(rows))==(137151806,2226400,78860441550,1846900,529)
 a,k,h=map(Q,(official['bit_saving'],official['kappa'],official['h_backoff']))
 oldlo,oldhi=moment(m,W,oldrows,a);assert oldhi<1
 lo,hi=moment(m,W,rows,a);assert lo>1
 required_a=k/(1-k)
 required_lo,required_hi=moment(m,W,rows,required_a);assert required_lo>1
 assembly=balanced.assembly(official['finite_bridge'],a,k,h=h)
 assert js(assembly)==official['assembly']
 assert js(balanced.cutoffs(official['finite_bridge'],assembly))==official['eventual_bounds']
 candidate_a=a-Q(3,10**11)
 candidate_lo,candidate_hi=moment(m,W,rows,candidate_a);assert candidate_hi<1
 q=candidate_a*(1-2*h);G=(1-h)*q/(1+q)
 candidate_k=Q((G*10**18).numerator//(G*10**18).denominator,10**18)
 candidate_assembly=balanced.assembly(official['finite_bridge'],candidate_a,candidate_k,h=h)
 assert candidate_k<k
 result=dict(status='PASS exact rejection: candidate is strictly worse',
  source_commit=source['commit'],verified_source_files=verified,axis_checks=axis_checks,
  counts=dict(m=m,N=N,W=W,L=L,rank_mass=mass,deficit=m*W-mass,maxchild=max(rows)),
  child_multiplicities=dict(sorted(rows.items())),baseline_bit_saving=a,baseline_kappa=k,
  candidate_moment_excess_at_baseline_lower=lo-1,candidate_moment_excess_at_baseline_upper=hi-1,
  candidate_moment_excess_at_required_a_lower=required_lo-1,required_a_for_baseline_kappa=required_a,
  baseline_moment_gap_lower=1-oldhi,
  candidate_valid_bit_saving=candidate_a,candidate_valid_kappa=candidate_k,
  candidate_valid_moment_gap_lower=1-candidate_hi,candidate_assembly=candidate_assembly,
  valid_witness_kappa_difference=candidate_k-k,
  assembly_constraints=len(assembly['constraints']),assembly_margins=assembly['margins'],
  limitations='Only retained-carrier clearing anchors at the two pinned axes are tested. No general optimality or lower bound; no new worst-case exponent; all-size framework and finite-to-asymptotic interfaces remain conditional.')
 (ROOT/'result.json').write_text(json.dumps(js(result),indent=2)+'\n')
 print('PASS: h23 word identical; h25 profile strictly worsens by two exact child splits; baseline exponent rejected')
 print('Candidate excess at baseline a lower',float(lo-1),'baseline kappa',float(k))
 print('Conservative valid candidate kappa',float(candidate_k),'difference',float(candidate_k-k))
if __name__=='__main__':main()
