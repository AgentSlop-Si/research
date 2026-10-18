"""Independent final integration audit; never calls the candidate's check helpers.
Reconstructs original target and retention, freshly runs the separate accepted
Horner coefficient oracle, and reconstructs all stored interval receipts.
"""
import hashlib, importlib.util, json, math, sys, time
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parent
CANDIDATE=Path(__file__).resolve().parent.parent/'candidate'
EXPECTED='ea5dadd6ae52dd283f09389d3829d957dc1bdfd921b6e9a15699314487701b33'
def read(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def frac(n): return {'numerator':n.numerator,'denominator':n.denominator}
def scale(iv,n):
 x=[iv[0]*n,iv[1]*n]; return min(x),max(x)
def add(a,b): return a[0]+b[0],a[1]+b[1]
def sub(a,b): return a[0]-b[1],a[1]-b[0]
def main():
 started=time.monotonic()
 assert sha(CANDIDATE/'MANIFEST.json')==EXPECTED
 manifest=read(CANDIDATE/'MANIFEST.json')
 for record in manifest['files']:
  p=CANDIDATE/record['path']; assert p.stat().st_size==record['bytes'] and sha(p)==record['sha256']
 bindings=read(CANDIDATE/'SOURCE_BINDINGS.json')['local_sources']
 for record in bindings:
  p=CANDIDATE/record['snapshot_path']; original=CANDIDATE/record['source_path']
  assert p.read_bytes()==original.read_bytes() and sha(p)==record['sha256']
 provider=CANDIDATE/'runtime/centered_source.py'
 assert (CANDIDATE/'runtime/centered_source.py').read_bytes()==provider.read_bytes()
 original=read(CANDIDATE/'ORIGINAL.json'); saved=read(CANDIDATE/'OUTPUT.json')
 source=saved['source']; est=saved['estimates']; out=saved['output']
 m=original['m']; M=1<<m; N=M//4; a,b=original['data'][0]; F=original['F']; energy=N*(a*a+b*b)
 assert original['kind']=='dense' and len(original['data'])==N and all(pair==[a,b] for pair in original['data'])
 h=0
 while 4**h<energy: h+=1
 sigma=h-F; P=16*m+16; beta=Fraction(1,4); normalized_bits=math.ceil((beta+2)*m)
 assert source=={'m':m,'N':N,'F':F,'real':a,'imag':b,'h':h,'scale':sigma,'input_kind':'dense'}
 assert est['source']==source and P==est['bits'] and sigma==out['scale_power']==44
 assert energy==17408 and h==8 and out['bits']==0 and out['normalized_bits']==normalized_bits==25
 assert len(out['pairs'])==N==512 and all(type(v) is int and v%(1<<19)==0 for pair in out['pairs'] for v in pair)
 K=1<<math.ceil(Fraction(m,4)); supp=[k for k in range(M) if min(k,M-k)<=K and (k==0 or k%4)]
 assert [k for k,_ in est['pairs']]==supp and len(supp)==13 and est['cutoff']==K==8
 assert est['exact_support_size']==3*N+1==1537
 # Compute target in original physical units. Only the DC target is irrational.
 q=384; s=math.isqrt(N << (2*q)); assert s*s<=N<<(2*q)<(s+1)*(s+1)
 root=(Fraction(s,1<<q),Fraction(s+1,1<<q))
 factor=1<<(-F); dc=[scale(root,c*factor) for c in (a,b)]
 norm2=Fraction(energy*factor*factor)
 errors=[]
 for ell,pair in enumerate(out['pairs']):
  target=dc if ell==0 else ((0,0),(0,0))
  radius=[max(abs(v-lo),abs(v-hi)) for v,(lo,hi) in zip(pair,target)]
  errors.append(sum(x*x for x in radius))
 worst=max(range(N),key=errors.__getitem__); relative=errors[worst]/norm2
 assert worst==510 and relative==Fraction(18295620993,37383395344384)
 assert relative<=Fraction(2213,100000)**2
 target_receipt=read(CANDIDATE/'TARGET_CHECKS.json')
 for ell,e in enumerate(errors):
  author=Fraction(**target_receipt['row_squared_error_normalized_upper'][ell])
  independently_normalized=e/Fraction(1<<(2*sigma))
  assert independently_normalized<=author
  if ell: assert independently_normalized==author
 assert Fraction(**target_receipt['norm_squared_normalized'])==Fraction(17,64)
 assert Fraction(**target_receipt['squared_relative_error_upper'])==relative
 # Explicit full row stencil, distinct from both endpoint and delta traversal.
 spec=importlib.util.spec_from_file_location('review_retained_oracle',CANDIDATE/'retained_oracle.py')
 oracle=importlib.util.module_from_spec(spec); spec.loader.exec_module(oracle)
 op=oracle.Oracle(N,M,5); cutoff=16*5*m+1; grid=oracle.BITS+P
 stored=read(CANDIDATE/'RETAINED_TARGET_CHECKS.json'); all_rows=[]; counts=[]
 assert grid==stored['target_grid']==448 and len(stored['rows'])==N
 total=0; largest=Fraction(0)
 for ell,pair in enumerate(out['pairs']):
  stencil={(ell*M//N+j)%M for j in range(-cutoff,cutoff+2)}
  assert len(stencil)==2*cutoff+2==1764
  real=(0,0); imag=(0,0); l1=0; selected=[]
  for k,(x,y) in est['pairs']:
   if k not in stencil: continue
   cr,ci=op.coefficient(ell,k); selected.append(k)
   real=add(real,sub(scale(cr,x),scale(ci,y)))
   imag=add(imag,add(scale(cr,y),scale(ci,x)))
   l1+=abs(x)+abs(y)
  # Exact lifting from physical integer Y to normalized grid.
  vals=[v << (grid-sigma) for v in pair]
  radii=[max(abs(v-lo),abs(v-hi)) for v,(lo,hi) in zip(vals,(real,imag))]
  endpoint_squared=sum(r*r for r in radii)
  allowed=(l1 << (oracle.BITS-8*m))+(1 << (grid-normalized_bits))
  assert endpoint_squared<=allowed*allowed
  calculated={'ell':ell,'terms':len(selected),'real_interval':list(real),'imag_interval':list(imag),'squared_endpoint_error':endpoint_squared,'squared_allowed_error':allowed*allowed}
  assert calculated==stored['rows'][ell]
  all_rows.append(calculated); counts.append(len(selected)); total+=len(selected)
  largest=max(largest,Fraction(endpoint_squared,allowed*allowed))
 assert total==op.calls==stored['independent_coefficient_calls']==out['incidences']==5733
 assert max(counts)==out['max_row_terms']==13 and frac(largest)==stored['max_squared_error_to_squared_bound_ratio']
 # Recompute all disjoint numerical receipt totals without candidate verifier.
 report=read(CANDIDATE/'RESULTS.json'); receipts=report['receipts']
 front=receipts['front_production']; replay=receipts['source_replay']['replay_production']; comparison=receipts['source_replay']['comparison']; outer=receipts['outer_transfer']['outer_and_scatter']; scalar=receipts['outer_transfer']['scalar']
 assert front==replay and front['events']['dense_coordinate_visits']==512
 assert front['events']['coefficient_outputs']==13 and comparison['events']['comparison_nodes']==80
 assert scalar['operations']['coefficient_call']==scalar['operations']['certificate_pass']==total
 assert scalar['operations']['pi_setup']==scalar['operations']['sqrt_setup']==scalar['operations']['setup_complete']==1
 work=sum(x['arithmetic_bit_work_upper']+x['control_bit_work_upper'] for x in (front,replay,comparison))+outer['bit_work']+scalar['total_bit_work_upper']
 bits=sum(x['cumulative_bits_upper'] for x in (front,replay,comparison))+outer['produced_bits']+scalar['cumulative_integer_and_control_storage_bits_upper']
 costs=read(CANDIDATE/'COST_TOTALS.json')
 assert work==costs['disjoint_production_work_upper_sum']==86007892714819542569341088
 assert bits==costs['disjoint_cumulative_produced_control_bits_upper_sum']==1509313675658178
 result={'status':'PASS','author_manifest_sha256':EXPECTED,'manifest_members_verified':len(manifest['files']),'local_source_bindings_byte_checked':len(bindings),'actual_original_coordinates_checked':N,'exact_source_energy':energy,'h':h,'scale_power':sigma,'output_numerator_shift':sigma-normalized_bits,'physical_original_norm_squared':frac(norm2),'normalized_original_norm_squared':frac(Fraction(17,64)),'fresh_original_target_checks':N,'worst_original_target_row':worst,'squared_relative_error_exact':frac(relative),'certified_relative_error_upper':'0.02213','approximate_relative_error':math.sqrt(relative),'fresh_retained_coefficients':total,'fresh_retained_rows':N,'all_retained_receipts_exactly_reconstructed':True,'retained_row_terms':counts,'work_upper_sum':work,'cumulative_produced_control_bits_upper_sum':bits,'review_seconds':time.monotonic()-started,'candidate_check_helpers_called':False,'production_numerics_used_by_oracles':False,'external_writes':False}
 (ROOT/'INDEPENDENT_AUDIT.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k!='retained_row_terms'},indent=2))
if __name__=='__main__': main()
