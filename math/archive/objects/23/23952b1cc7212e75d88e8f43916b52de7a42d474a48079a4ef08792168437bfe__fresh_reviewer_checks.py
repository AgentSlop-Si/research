"""Fresh reviewer-authored bounded controls. No supplied code is executed, imported, compiled or parsed."""
from pathlib import Path
from fractions import Fraction
import json,hashlib,math,itertools
O=Path(__file__).parent;M=Path('fft_research_master_20261009');rows=json.loads((O/'ASSIGNED_SOURCES.json').read_text());checks=[]
def record(name,condition,detail,kind='fresh_independent_arithmetic'):
 checks.append({'check':name,'passed':bool(condition),'detail':detail,'kind':kind})
def receipt(i,name):
 p=(M/rows[i]['representative_path']).parent/name
 b=p.read_bytes();return json.loads(b),{'path':str(p),'sha256':hashlib.sha256(b).hexdigest()}
def det(mat,p):
 # Leibniz expansion is deliberately independent of supplied elimination helpers.
 n=len(mat);total=0
 for perm in itertools.permutations(range(n)):
  inversions=sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n));v=(-1)**inversions
  for i,j in enumerate(perm):v=v*mat[i][j]%p
  total=(total+v)%p
 return total
def rank(mat,p):
 a=[[int(x)%p for x in r] for r in mat];h=0
 for col in range(len(a[0]) if a else 0):
  sel=next((j for j in range(h,len(a)) if a[j][col]),None)
  if sel is None:continue
  a[sel],a[h]=a[h],a[sel];v=pow(a[h][col],-1,p)
  a[h]=[x*v%p for x in a[h]]
  for j in range(h+1,len(a)):
   v=a[j][col];a[j]=[(x-v*y)%p for x,y in zip(a[j],a[h])]
  h+=1
  if h==len(a):break
 return h
# Explicit guard counterexamples derived from the mathematical definitions.
z=pow(2,(7-1)//6,7);order=next(k for k in range(1,7) if pow(z,k,7)==1)
record('non_power_of_two_root_guard',pow(z,6,7)==1 and order==3,{'n':6,'p':7,'g':2,'z':z,'actual_order':order,'conclusion':'The helper n-th-root test does not certify exact order for non-dyadic n.'})
p=1201;n=8;omega=p-7
L=[[(7+pow(omega,i,p))*(i==j)+2*(j==(i-1)%n) for j in range(n)] for i in range(n)]
B=[[(7+2*pow(omega,-i,p))*(i==j)+(j==(i-1)%n) for j in range(n)] for i in range(n)]
ld,bd=det(L,p),det(B,p)
r,src=receipt(2,'INDEPENDENT_RESULTS.json');old=r['inherited_solver_control']
record('invertible_matrix_zero_diagonal',L[1][1]%p==0 and ld==945 and bd!=0,{'field':p,'N':n,'omega':omega,'zero_diagonal_index':1,'L_determinant':ld,'P_determinant':bd,'historical_values_match':ld==old['L_determinant'] and bd==old['P_determinant'],'receipt':src,'scope':'Fresh determinant checks only, not re-execution of the archived solver.'})
# Nonpole alpha=-1 does not guarantee packet-block completeness.
n=5;p=11;w=3;alpha=10
A=[[pow(alpha,(d*pow(h,-1,n))%n,p) for h in range(1,n)] for d in range(1,n)]
rk=rank(A,p)
record('nonpole_packet_block_rank_failure',pow(alpha,n,p)!=1 and rk==2,{'N':n,'p':p,'alpha':alpha,'block_x':0,'rank':rk,'required_full_rank':4})
# A trace root may exist even when no nonidentity N-th root exists in the base field.
roots=[x for x in range(5) if pow(x,3,5)==1 and x!=1]
record('trace_domain_requires_base_field_roots',not roots and (4**3-3*4-2)%5==0,{'p':5,'N':3,'trace_t':4,'nonidentity_base_field_roots':roots,'Dickson3_minus2':0})
# Direct full-space walk for the explicit horizon countercontrol, independent of compressed rules.
p=65537;n=16;ret=[0,4,8,12];state=[0]*n
for idx,v in zip(ret,[1,2,3,4]):state[idx]=v
retained=[]
for step in range(1,6):
 nxt=[0]*n
 for j,v in enumerate(state):
  nxt[(2*j)%n]=(nxt[(2*j)%n]+v)%p
  nxt[(2*j+1)%n]=(nxt[(2*j+1)%n]+pow(64,j,p)*v)%p
 retained.append([nxt[j] for j in ret])
 for j in ret:nxt[j]=0
 state=nxt
r,src=receipt(48,'INDEPENDENT_RESULTS.json')
record('compressed_horizon_counterexample',retained[-1]==[0,57313,0,510] and retained[-1]==r['beyond_horizon']['exact'],{'N':16,'b':2,'degree':5,'direct_first_return_outputs':retained,'receipt':src})
# Recompute two historical determinant witnesses directly from their stored matrices.
for i,name,key,expected in [(21,'FOUR_BY_FOUR_GATE_RESULTS.json','coefficient_matrix',60131),(25,'SPECTRAL_RESULTS.json','minor',19255)]:
 r,src=receipt(i,name);p=r.get('prime',r.get('p'));value=det(r[key],p)
 record('stored_minor_'+str(i),value==expected,{'field':p,'dimension':len(r[key]),'fresh_Leibniz_determinant':value,'receipt':src,'scope':'Verifies the stored matrix determinant; does not independently reconstruct its target operator.'},'fresh_arithmetic_on_stored_data')
# Verify exact relation of two historical N16 receipts and their input chart hash.
r,src=receipt(3,'INDEPENDENT_CERTIFICATE.json');s,_=receipt(3,'sources/EXACT_CONTRACTION_CERTIFICATE.json');chart=(M/rows[3]['representative_path']).parent/'sources/DYADIC_AFFINE_CHART.json'
q=lambda x:Fraction(int(x['numerator']),int(x['denominator']))
matched={k:q(v)==q(s[k]) for k,v in r['bounds'].items()}
record('N16_receipt_fraction_and_chart_binding',all(matched.values()) and hashlib.sha256(chart.read_bytes()).hexdigest()==r['chart_sha256'],{'matching_fraction_fields':matched,'chart_sha256':r['chart_sha256'],'receipt':src,'scope':'Receipt consistency, not recomputation of chart/Jacobian or acceptance of contraction theorem.'},'stored_evidence_reconciliation')
# Count ledgers reconstructed from finite loop domains, separately from algorithm claims.
def countcheck(i,file,path,value):
 r,s=receipt(i,file);v=r
 for k in path:v=v[k]
 observed=len(v) if isinstance(v,list) else v
 record('receipt_count_'+str(i)+'_'+'_'.join(map(str,path)),observed==value,{'path':path,'stored':observed,'independently_counted_domain':value,'receipt':s},'stored_evidence_reconciliation')
countcheck(0,'VERIFIED_RESULTS.json',['all_24_sheet_permutations'],math.factorial(4))
countcheck(0,'VERIFIED_RESULTS.json',['hierarchical_route_controls'],2*8*2)
countcheck(0,'VERIFIED_RESULTS.json',['bank_controls'],5*2*2)
countcheck(1,'INDEPENDENT_RESULTS.json',['exhaustive_rank_partitions'],sum(math.comb(n,n//2) for n in (2,4,6,8,10,12)))
countcheck(1,'INDEPENDENT_RESULTS.json',['full_case_count'],sum(2*len({0,1,n//4,max(0,n//2-1),n//2}) for n in (2,4,6,8,10,12,16,30,32,64)))
countcheck(12,'INDEPENDENT_RESULTS.json',['recovery_cases'],3*sum(sum(n%d==0 for d in range(1,n+1)) for n in list(range(1,17))+[18,20,24,27,32,36]))
countcheck(16,'EXTERIOR_UNIQUENESS_CONTROLS.json',['cases'],4+4+3+1)
countcheck(17,'NONZERO_BUTTERFLY_CONTROLS.json',['cases'],3*2)
countcheck(26,'INDEPENDENT_RESULTS.json',['exhaustive_small_masks'],sum(2**n for n in range(2,7)))
countcheck(26,'INDEPENDENT_RESULTS.json',['exhaustive_mask_pairs'],sum(4**n for n in range(2,7)))
countcheck(26,'INDEPENDENT_RESULTS.json',['complete_filter_count'],12*12)
countcheck(28,'INDEPENDENT_RESULTS.json',['exhaustive_polynomials'],sum(p**3-1 for p in (7,13,17)))
countcheck(31,'SINGLE_EDIT_SEARCH.json',['number_of_single_Toffoli_layouts'],3*8*math.comb(7,2))
countcheck(37,'COMPRESSED_BOUNDARY_CONTROLS.json',['summary','parameters'],sum(range(1,8)))
countcheck(37,'COMPRESSED_BOUNDARY_CONTROLS.json',['summary','integer_count_parameters'],sum(range(1,129)))
countcheck(44,'WORD_ARRAY_CHECKS.json',['exact_word_array_cases'],4*7*3*3)
countcheck(48,'INDEPENDENT_RESULTS.json',['cases'],2*sum(range(1,9)))
countcheck(52,'INDEPENDENT_RESULTS.json',['monomial_classification_exhaustive_permutations'],sum(math.factorial(n) for n in range(2,9)))
countcheck(52,'INDEPENDENT_RESULTS.json',['exact_root_kernel_support_cases'],sum(n*(n-1) for n in range(2,81)))
# Newly enumerated occupancy expectation, not source execution.
values=[]
for bits in itertools.product((0,1),repeat=8):
 sets={};todo=[bits]
 while todo:
  a=todo.pop();sets.setdefault(len(a),set()).add(a)
  if len(a)>1:todo += [a[::2],a[1::2]]
 values.append(sum(k//2*len(v) for k,v in sets.items() if k>1))
actual=Fraction(sum(values),len(values));expected=sum((Fraction(k//2*(2**k))*(1-Fraction(2**k-1,2**k)**(8//k)) for k in (2,4,8)),Fraction())
record('binary_occupancy_N8',actual==expected,{'inputs':256,'exact_mean':str(actual),'formula':str(expected),'scope':'One bounded uniform binary input domain.'})
(O/'FRESH_REVIEWER_CHECKS.json').write_text(json.dumps({'source_execution':'none','source_import_compile_AST':'none','checks':checks,'all_passed':all(x['passed'] for x in checks),'scope':'Only newly authored bounded arithmetic and metadata checks ran. Historical PASS claims remain historical.'},indent=2)+'\n')
print('checks',len(checks),'failed',[x['check'] for x in checks if not x['passed']])
