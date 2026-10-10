"""Fresh reviewer-owned controls; reads inert JSON only, never supplied code."""
from pathlib import Path
from fractions import Fraction
import json,math,hashlib,collections
P=Path(__file__).parent
idx=json.loads((P/'STORED_OUTPUTS_INDEX.json').read_text())
def artifact(suffix):
 r=next(r for r in idx if r['member_name'].endswith(suffix))
 return json.loads((P/r['snapshot']).read_text()),{'archive_sha256':r['archive_sha256'],'member_name':r['member_name'],'sha256':r['sha256']}
def determinant(matrix,p):
 a=[[v%p for v in row] for row in matrix];n=len(a);answer=1
 for col in range(n):
  pivot=next((r for r in range(col,n)if a[r][col]),None)
  if pivot is None:return 0
  if pivot!=col:a[col],a[pivot]=a[pivot],a[col];answer=-answer
  diag=a[col][col];answer=answer*diag%p;inv=pow(diag,-1,p)
  for r in range(col+1,n):
   t=a[r][col]*inv%p
   for c in range(col,n):a[r][c]=(a[r][c]-t*a[col][c])%p
 return answer%p
def inverse(a,p):
 n=len(a);work=[[x%p for x in a[r]]+[int(r==c)for c in range(n)]for r in range(n)]
 for c in range(n):
  pivot=next(r for r in range(c,n)if work[r][c]);work[c],work[pivot]=work[pivot],work[c]
  v=pow(work[c][c],-1,p);work[c]=[(x*v)%p for x in work[c]]
  for r in range(n):
   if r!=c:
    v=work[r][c];work[r]=[(x-v*y)%p for x,y in zip(work[r],work[c])]
 return [r[n:]for r in work]
controls=[]
# A: deterministic bias/failure from data-dependent plan reused on changed data.
n=1024;eps=Fraction(2,5);delta=Fraction(1,20);k=math.ceil(4/float(eps)**2*math.log(4*n/float(delta)))
assert k<n
old_tail=n;new_tail=2*n;estimator_dc=Fraction(k)*Fraction(old_tail,k)/32;true_dc=Fraction(new_tail,32);error=abs(true_dc-estimator_dc);threshold=eps*new_tail/32
assert error>threshold
controls.append({'id':'stale_head_tail_plan','kind':'fresh exact arithmetic counterexample','n':n,'epsilon':str(eps),'delta':str(delta),'head_size':0,'old_input':'all ones','new_input':'all twos','sample_count':k,'all_draw_sequences_covered':True,'estimated_unitary_DC':str(estimator_dc),'correct_unitary_DC':str(true_dc),'error':str(error),'allowed_error':str(threshold),'failure_probability_on_reused_plan':1,'conclusion':'Length-only plan acceptance and old tail_l1 scaling lose unbiasedness and violate the requested bound. This independently models the algebra, not an execution of supplied code.'})
# B: the two weighted pair scans reduce exactly to one ordinary butterfly.
cases=0
for p in (17,97,257):
 for a in range(7):
  for b in range(7):
   for w in range(1,8):
    scaled=(-2*w*b)%p;first=(a-pow(2,-1,p)*scaled)%p;second=(scaled+first)%p
    assert (first,second)==((a+w*b)%p,(a-w*b)%p);cases+=1
controls.append({'id':'two_scan_butterfly','kind':'fresh exact modular control','cases':cases,'primes':[17,97,257],'conclusion':'Two pair scans recover ordinary butterfly; this does not reduce log N levels.'})
# C: archived N64 sector matrices reconstructed via direct inverse of I-tau P,
# independent of the supplied geometric-sum Green implementation.
a,src=artifact('SECTOR_FRAME_CERTIFICATE.json');p=a['prime'];assert all(p%d for d in range(2,math.isqrt(p)+1))
greens=[]
for route,guard in zip(a['nested_cycle_successors'],a['fixed_rational_inverse_guards']):
 assert sorted(route)==list(range(64));d=guard['d'];assert (pow(d,64,p)-1)%p==guard['d64_minus_1_mod_p']!=0
 walk=[];v=0
 for j in range(64):walk.append(v);v=route[v]
 assert v==0 and len(set(walk))==64
 for i in range(64):
  v=i
  for j in range(32):v=route[v]
  assert v==(i+32)%64
 tau=pow(d,-1,p);M=[[int(i==j)for j in range(64)]for i in range(64)]
 for j,i in enumerate(route):M[i][j]=(M[i][j]-tau)%p
 greens.append(inverse(M,p))
def sector_rows(i,sign):return [[(g[i][j]+sign*g[i][j+32])%p for j in range(32)]for g in greens]
for r in a['projected_frame_minor_records']:
 rows=sector_rows(r['row'],r['sector_sign']);minor=[[row[j]for j in r['columns']]for row in rows]
 assert determinant(minor,p)==r['determinant_mod_p']!=0
for r in a['minimal_row_zero_certificate']:
 rows=sector_rows(r['row'],r['sector_sign']);assert [[row[j]for j in r['columns']]for row in rows]==r['minor_mod_p']
for r in a['four_row_direct_sum_certificates']:
 mat=[row for i in r['rows']for row in sector_rows(i,r['sector_sign'])]
 assert mat==r['stacked_minor_mod_p'];assert determinant(mat,p)==r['determinant_mod_p']!=0
controls.append({'id':'archived_N64_sector_reconstruction','kind':'fresh exact modular control using archived route data','input':src,'routes_reconstructed':8,'projected_minors_verified':len(a['projected_frame_minor_records']),'direct_sum_minors_verified':len(a['four_row_direct_sum_certificates']),'route_half_turn_verified':True,'conclusion':'Stored fixed-route sector witnesses are independently arithmetically consistent; no general mixing-family exclusion or historic execution attestation.'})
# D: directly verify stored N16 augmented rank witnesses (not route/prefix replay).
a,src=artifact('N16_OUTER_GATE_RESULTS.json');p=a['field']['prime'];ds=[]
for r in a['augmented_rank_nine_witnesses']:
 v=determinant(r['minor_mod_prime'],p);assert v==r['determinant_mod_prime']!=0;ds.append(v)
controls.append({'id':'archived_N16_augmented_minors','kind':'fresh exact determinant checks on stored matrices','input':src,'minor_count':len(ds),'determinants':ds,'conclusion':'Stored matrices rank9 modulo p; association to claimed fixed-inner templates remains source/provenance evidence, not independently rebuilt here.'})
# E: static test entrypoint order, no AST/compilation/execution of supplied text.
manifest=json.loads((P/'SOURCE_MANIFEST.json').read_text());records=[]
for i in (28,31):
 row=manifest[i-1];lines=(P/'sources'/row['sha256']).read_text().splitlines();main=next(j for j,line in enumerate(lines,1)if "if __name__=='__main__'" in line)
 later=[{'line':j,'definition':s}for j,s in enumerate(lines,1)if j>main and s.startswith('class ')]
 assert later;records.append({'sha256':row['sha256'],'main_line':main,'classes_after_main':later})
controls.append({'id':'test_entrypoint_order','kind':'fresh inert text structural observation','records':records,'conclusion':'Ordinary unittest.main exits before later class definitions; imported unittest discovery can include them.'})
# F: archived rational finite-bridge mass and positive-slack consistency.
a,src=artifact('frame-certificate.json');b=a['bit'];mass=sum(int(t)*v for t,v in b['child_multiplicities'].items());assert mass==b['total_rank']==b['m']*b['W']-b['N']+b['L'];assert len(a['assembly']['constraints'])==47 and all(Fraction(x)>0 for x in a['assembly']['constraints'].values());assert len(a['assembly']['margins'])==7
controls.append({'id':'archived_frame_arithmetic','kind':'fresh exact arithmetic over stored data','input':src,'rank_mass':mass,'wires':b['W'],'strict_constraints':47,'margins':7,'kappa':a['kappa'],'conclusion':'Internal exact scalar arithmetic agrees; did not replay full serialized dirty word or inherited transfer proofs.'})
# G: analytical counter identities in all archived streaming rows.
a,src=artifact('streaming/results.json');checked=0
for r in a['cases']:
 n,k=r['n'],r['active_k'];pc,gc,bc=r['preparation_counts'],r['generation_counts'],r['full_ntt_counts'];assert gc['output_coefficients']==n;assert bc.get('butterflies',0)==n*(n.bit_length()-1)//2
 if k:
  f=r['convolution_length'];blocks=(n+k-1)//k
  assert pc['prep_multiplications']==3*k*k-k;assert pc['ntt_calls']==2;assert gc['ntt_calls']==4*blocks;assert gc['butterflies']==2*blocks*f*(f.bit_length()-1);assert gc['pointwise_multiplications']==2*blocks*f
 checked+=1
assert checked==a['number_of_cases']==184
controls.append({'id':'archived_streaming_counts','kind':'fresh count reconciliation, not transform replay','input':src,'cases':checked,'declared_direct_cases':a['direct_verified_cases'],'conclusion':'All archived counter fields match source formulas; no verification of the historical timings or actual numerical outputs.'})
# H: clean GF2 identity cannot by itself imply characteristic-zero identity.
assert (1^1)==0 and Fraction(1)+Fraction(1)==2
controls.append({'id':'field_scope','kind':'fresh exact algebra scope control','GF2_two_copies_of_one':0,'characteristic_zero_two_copies_of_one':2,'conclusion':'A binary XOR compiler certificate alone does not prove the corresponding positive scalar-addition word over Q/C.'})
(P/'INDEPENDENT_CONTROLS.json').write_text(json.dumps({'supplied_source_executed':False,'supplied_source_imported_compiled_or_AST_parsed':False,'controls':controls},indent=2)+'\n')
print(json.dumps({'independent_controls':len(controls),'all_completed':True,'N64_minors':64,'N16_minors':len(ds),'stale_plan_error':str(error),'stale_plan_target':str(threshold)}))
