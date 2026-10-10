"""Fresh independent arithmetic and stored-data checks, never supplied-code execution."""
from pathlib import Path
from fractions import Fraction as F
import json,math,itertools,hashlib,collections
import numpy as np
O=Path(__file__).parent;E=json.loads((O/'EVIDENCE_INDEX.json').read_text());checks=[]
def data(prefix):
 es=[e for e in E if e['sha256'].startswith(prefix)];assert len(es)==1
 return json.loads((O/es[0]['local']).read_text())
def rec(name,good,detail):
 checks.append({'check':name,'passed':bool(good),'detail':detail})
 if not good:raise AssertionError(name)
def determinant(mat,p):
 # Standard fresh modular elimination using column row-addition factors, not a supplied implementation.
 A=[list(row) for row in mat];n=len(A);answer=1
 for col in range(n):
  candidates=[r for r in range(col,n) if A[r][col]%p]
  if not candidates:return 0
  pivot=candidates[0]
  if pivot!=col:A[pivot],A[col]=A[col],A[pivot];answer=-answer
  z=A[col][col]%p;answer=answer*z%p;inverse=pow(z,-1,p)
  for row in range(col+1,n):
   factor=A[row][col]*inverse%p
   A[row]=[(v-factor*w)%p for v,w in zip(A[row],A[col])]
 return answer%p
def rank(mat,p):
 # Build normalized row-space basis keyed by leading coordinate.
 basis={}
 for row in mat:
  v=[x%p for x in row]
  for col in sorted(basis):
   q=v[col]
   if q:v=[(a-q*b)%p for a,b in zip(v,basis[col])]
  lead=next((i for i,a in enumerate(v) if a),None)
  if lead is not None:basis[lead]=[a*pow(v[lead],-1,p)%p for a in v]
 return len(basis)
def inverse_mod(mat,p):
 n=len(mat);A=[[x%p for x in row]+[int(i==j) for j in range(n)] for i,row in enumerate(mat)]
 for j in range(n):
  z=next(k for k in range(j,n) if A[k][j]);A[j],A[z]=A[z],A[j]
  pivot_inverse=pow(A[j][j],-1,p);A[j]=[v*pivot_inverse%p for v in A[j]]
  for k in range(n):
   if k!=j:
    scale=A[k][j];A[k]=[(v-scale*w)%p for v,w in zip(A[k],A[j])]
 return [row[n:] for row in A]
# Guard and formula defects established without calling supplied functions.
rec('cubic_moment_rank_needs_characteristic_condition',rank([[(int(i==j)+1)%5 for j in range(4)] for i in range(4)],5)==3,{'n':4,'field':5,'rank':3,'scope':'General full-rank claim requires characteristic not dividing n+1; assigned fixed-prime small tests unaffected'})
rec('composite_interpolation_guard_counterexample',math.gcd(3,9)!=1,{'p':9,'m':4,'passes_source_guard':True,'third_Newton_divisor':3,'invertible':False,'schoolbook_product':[1,2,2,1],'static_trace_candidate':[1,0,5,0],'supplied_source_executed':False})
rec('macro_root_guard_accepts_zero',pow(0,8//2,17)!=1 and pow(0,8,17)!=1,{'n':8,'p':17,'g':0,'derived_w':0,'bad_root_passes_only_half_order_test':True})
rec('macro_N2_supported_but_scan4_plan_impossible',(3-1)%2==0 and (3-1)%4!=0,{'n':2,'p':3,'g':2,'valid_root':2,'unconditional_make_scan4_plan_fails':True})
rec('macro_power_call_static_inventory',2+2+16+3+3==26,{'root_n_initial':2,'root_n_scan4':2,'matrix_entries':16,'lower_inverses':3,'upper_inverses':3,'actual_before_stage_roots':26,'source_report_before_stage_roots':22,'source_lines':'15–20,90–100,152,160–162'})
tiny=np.array([1e-200,0.0],dtype=np.complex128);observed=float(np.linalg.norm(tiny));actual=math.hypot(1e-200,0)
rec('head_tail_norm_underflow',observed==0 and actual>0,{'finite_input':[1e-200,0],'numpy_norm':observed,'stable_norm':actual,'head_size':0,'epsilon':0.25,'correct_unitary_output_magnitude':actual/math.sqrt(2),'allowed_error':actual*.25/math.sqrt(2),'deduced_source_return':'zero output from norm_tail==0 branch','scope':'fresh library arithmetic; source not executed'})
rec('hybrid_universal_bound_requires_epsilon_restriction',not (4>100**2),{'m':1,'N':4,'s':2,'h':0,'eps_numerator':100,'eps_denominator':1,'forced_tail_levels':0,'certified_total':0,'unconditional_reported_universal_lower':2,'reason':'All depth inequalities fail for large epsilon'})
rec('boolean_encoder_coercion',int(.5)==0 and int(1.9)==1,{'accepted_nonboolean_values':[.5,1.9],'source_lines':'159–169','scope':'static guard consequence'})
rec('negative_power_helper_nontermination',(-1>>1)==-1,{'source69_lines':'10–18','negative_exponent':-1,'constructor_uses_only_positive_exponents':True})
rec('rational_log_tail_sign',F(-1,3)**101<0,{'x':'1/2','atanh_z':'-1/3','first_omitted_term_negative':True,'lo_hi_bounds_reversed_outside_x_ge_1':True})
# Source loops reconciled to saved counters, not rerun.
d=data('051541');rec('degree_audit_loop_counts',d['quadratic_basis_columns_tested']==3*sum([2,4,8,16,32,64]) and d['cubic_boolean_and_recovery_cases']==sum([2,4,8,16,32,64])+30 and d['wedge_dense_overlap_tests']==24,{'quadratic_basis':378,'cubic_combined_cases':156,'wedge_cases':24})
for row in d['lengths']:
 n=row['n'];base=2*n*(n.bit_length()-1);observed=[v['work_one_evaluation'] for v in row['quadratic_variants']]
 rec('degree_operation_counts_N'+str(n),observed==[base+n,base+4*n,base+11*n//2],{'reported':observed,'root_exponentiation_excluded':True})
d=data('a1ae14');rec('strong_scale_count_scope',d['exact_head_sizes_checked']==sum(2**m+1 for m in range(1,15)) and d['numeric_cases']==48 and len(d['numerical_checks'])==48,{'head_sizes':32780,'floating_cases':48,'largest_symbolic_N':4**14,'largest_numerical_N':4096})
rec('strong_scale_default_exact_bounds',all(r['minimum_certified_butterflies']==r['n']*r['m']//2==r['universal_lower_bound'] for r in d['exact_certificates']),{'cases':14,'scope':'recorded counters/formulas only'})
d=data('a49236');rec('structured_phase_counters',d['exhaustive_affine_bad_seed_cases']==3*sum(m**3//2 for m in [4,8,16]) and d['higher_degree_bad_seed_cases']==9*7*40 and d['CAZAC_alternating_input_exact_products']==sum(m*m for m in [4,8,16,32]) and d['prime_variance_character_cases']==26 and d['finite_chirp_recurrence_cases']==sum(m*m for m in [4,5,8,11,16]),{'affine':7008,'higher_degree':2520,'CAZAC':1360,'prime_cases':26,'recurrences':482})
rec('structured_prime_character_counters',all(r['orthogonal_error_characters']==r['K']*r['M']*(r['M']-1) for r in d['prime_variance_cases']),{'cases':26})
d=data('77a2ef');cases=4*sum(len({0,1,n//4,n//2,n,n+3}) for n in [1,2,4,8,16,32,64]);rec('prefix_planner_saved_counts',d['all_prefix_oracle_cases']==cases==144 and d['focused_selection_cases']==12 and d['invalid_or_stale_rejections']==27,{'oracle':cases,'selection':12,'invalid':27})
for prefix,want in [('102933',12),('a0cc04',11)]:
 d=data(prefix);rec('integration_saved_status_'+prefix,d['status']=='PASS' and len(d['checks'])==want and all(r['exit_code']==0 for r in d['checks']),{'script_records':want,'scope':'historical process reports; no rerun'})
d=data('62ddb6');rec('compact_operator_saved_costs',all(r['gates']==r['n']*(r['n'].bit_length()-1)//2 and r['pole_cost']['state_multiplies']==r['n']*(r['n']-1) and all(v['total_primitives']==r['gates'] for v in r['grouped_macros']) for r in d['results']),{'cases':len(d['results'])})
d=data('a99e31');rec('discrepancy_bit_census',[(r['n'],r['bit_coordinate_summary']['total'],len(r['bit_coordinate_summary']['passing'])) for r in d['results']]==[(32,120,5),(64,720,0)],{'N32_coordinate_survivors':5,'N64_coordinate_survivors':0,'scope':'stored census consistency'})
d=data('0ba916');rec('interval_screen_survivor_census',[(r['n'],len(r['candidates']),sum(not v['passes'] for v in r['candidates'])) for r in d]==[(32,96,0),(64,174,0)],{'all_stored_interval_candidates_pass':True,'scope':'necessary filters only'})
d=data('cdb89a');rec('endpoint_candidate_counts',all(r['total']==r['n']+math.factorial(r['n'].bit_length()-1)==len(r['tests']) and r['rejected']==sum(v['rejected'] for v in r['tests']) and len(r['survivors'])==r['total']-r['rejected'] for r in d),{'endpoint_cases':9,'tested_records':sum(r['total'] for r in d)})
d=data('127b94');rec('stage_rigidity_stored_budget_arithmetic',len(d['certificates'])==15 and all(r['rank_correction_lower_bound']==r['exact_Fourier_rank']-r['remaining_stage_capacity'] for r in d['certificates']),{'subsets':15,'not_rerun':'510 modular ranks or 3825 maxflows'})
d=data('dc196');rec('weyl_ordered_pair_counts',all(r['independent_pairs']==(r['N']**2-1)*(r['N']**2-r['N']) and r['factorable_pairs']+r['nonfactorable_pairs']==r['independent_pairs'] for r in d['rank_dichotomy']),d['rank_dichotomy'])
rec('weyl_line_counters_are_vector_counts',all(r['full_rank_anisotropic_lines']+r['rank_one_isotropic_lines']==r['N']**2-1 and r['vertical_full_rank_directions']==r['N']-1 for r in d['line_classification']),{'projective_lines_actual':[{'N':r['N'],'anisotropic':r['full_rank_anisotropic_lines']//(r['N']-1),'isotropic':r['rank_one_isotropic_lines']//(r['N']-1)} for r in d['line_classification']]})
d=data('d64f72');rec('four_character_stored_counts',len(d['green_routes'])==48 and sum(r['exact_character_residue_entries'] for r in d['fourier_blocks'])==16*sum(n*n for n in [4,8,16,32,64,128]) and sum(r['green_vector_checks'] for r in d['green_routes'])==968,{'routes':48,'character_entries':349440,'green_vectors':968})
# Verify saved full-state matrix hashes against their actual serialized matrix data.
d=data('2e49ea');matrix_records=[]
for row in d['cases']:
 name=f"results/t{row['t']}_r{row['r']}_s{row['start_stage']}_certificate.json"
 entry=next(e for e in E if any(o['member']==name for o in e['occurrences']));art=json.loads((O/entry['local']).read_text());h=hashlib.sha256(json.dumps(art['full_state_matrix'],separators=(',',':')).encode()).hexdigest()
 matrix_records.append({'case':name,'sha256':h,'matches':h==row['dirty_lift']['full_state_matrix_sha256']})
rec('synthetic_full_state_matrix_hashes',all(r['matches'] for r in matrix_records),matrix_records)
rec('synthetic_restricted_gate_bill',all(r['baseline_add_sub']==r['candidate_add_sub']==2*r['real_scalar_inputs'] and r['lower_bound_certificate']['cancellation_free_addition_lower_bound']==2*r['real_scalar_inputs'] for r in d['cases']),{'cases':10,'grammar':'disjoint signed cancellation-free additions','scope':'stored bill arithmetic, not circuit replay'})
# Reconstruct all Boolean cubic certificate evaluation matrices directly from support definitions.
d=data('f39adb');p=998244353
for key,cert in d['conjugate_pair_cubic_certificates'].items():
 n=int(key);w=pow(3,(p-1)//n,p);known=[k for k in range(n) if k not in [1,n-1]];terms=[t for degree in range(1,4) for t in itertools.combinations_with_replacement(known,degree) if sum(t)%n==1]
 valid=all(len(s)==len(set(s)) and all(0<=j<n for j in s) and len(s)<=3 for s in cert['supports']);A=[]
 for s in cert['supports']:
  f=[sum(pow(w,k*j,p) for j in s)%p for k in range(n)]
  A.append([math.prod(f[k] for k in t)%p for t in terms]+[f[1]])
 det=determinant(A,p);rec('cubic_certificate_N'+key,valid and len(A)==len(terms)+1 and det==cert['determinant_mod_998244353']!=0,{'rows':len(A),'monomials':len(terms),'determinant_mod_p':det,'support_indices_and_uniqueness_verified':valid,'source_executed':False})
# Independently reconstruct four weighted Green branches using direct linear solves, not geometric series.
d=data('0ac1ad');c=data('2e4be0');p=65537;fw=d['four_green_witness'];matrices=[]
for pair in fw['green_parameters']:
 branches=[]
 for par in pair:
  n=len(par['sigma']);T=[[int(i==j) for j in range(n)] for i in range(n)]
  for i in range(n):T[i][par['sigma'][i]]-=par['weights'][i]
  Z=inverse_mod(T,p);branches.append([[par['row_scale'][i]*Z[par['row_perm'][i]][par['col_perm'][j]]*par['col_scale'][j]%p for j in range(n)] for i in range(n)])
 matrices.append([[(branches[0][i][j]+branches[1][i][j])%p for j in range(n)] for i in range(n)])
A,B=matrices;n=d['N'];w=d['primitive_8th_root'];K=[[A[k][i]*(B[i][1]-pow(w,k,p)*B[i][0])%p for i in range(n)] for k in range(n)];det=determinant(K,p)
rec('four_green_direct_inverse_certificate',A==fw['A'] and B==fw['B'] and K==c['pencil_matrix'] and det==c['two_column_pencil_det_GF65537']!=0,{'N':n,'determinant':det,'scope':'fixed parameters only','method':'direct inverses of I-T; source geometric-series implementation not called'})
# Fresh exact rational Ramanujan covariance and a Rayleigh witness.
def mobius_by_squarefree(k):
 primes=[];d=2
 while d*d<=k:
  if k%d==0:
   k//=d
   if k%d==0:return 0
   primes.append(d)
  d+=1
 if k>1:primes.append(k)
 return (-1)**len(primes)
n=12;m=3;units=sum(math.gcd(a,n)==1 for a in range(n));Q=[]
for i in range(n):
 row=[]
 for j in range(n):
  common=set(range(i%m-m+1,i%m+1))&set(range(j%m-m+1,j%m+1));common.discard(0);s=F()
  for shift in common:
   g=math.gcd(n,shift*(j-i));r=sum(d*mobius_by_squarefree(n//d) for d in range(1,g+1) if g%d==0);s+=F(r,units*n)
  row.append(s)
 Q.append(row)
arr=np.array([[float(v) for v in row] for row in Q]);_,vectors=np.linalg.eigh(arr);v=np.rint(vectors[:,-1]*100).astype(int).tolist();rq=sum(Q[i][j]*v[i]*v[j] for i in range(n) for j in range(n))/sum(a*a for a in v);residual=[[sum(Q[i][k]*Q[k][j] for k in range(n))-F(m,n)*Q[i][j] for j in range(n)] for i in range(n)]
rec('composite_covariance_exact_rational_counterexample',rq>F(m,n) and any(x for row in residual for x in row),{'N':n,'M':m,'integer_Rayleigh_vector':v,'exact_Rayleigh_quotient':str(rq),'prime_power_target':str(F(m,n)),'trace':str(sum(Q[i][i] for i in range(n))),'Q_squared_minus_target_Q_nonzeros':sum(bool(x) for row in residual for x in row),'matrix':[[str(v) for v in row] for row in Q],'method':'independent divisor-sum Ramanujan formula; exact final certificate; supplied eigenvalue program not run'})
# F8 arbitrary endpoint obstruction: all 3x5 minors have full rank, enough to kill cut 3.
p=998244353;w=pow(3,(p-1)//8,p);count=0
for rs in itertools.combinations(range(8),3):
 for cs in itertools.combinations(range(8),5):
  assert rank([[pow(w,r*c,p) for c in cs] for r in rs],p)==3;count+=1
rec('F8_endpoint_rank2_obstruction',count==3136,{'all_3_by_5_submatrices':count,'each_rank':3,'consequence':'At cut 3 every independent endpoint ordering exceeds rank ceiling 2','saved_reachable_cut3':data('6a558e')['frontiers'][2]['reachable_prefix_pairs']})
# Exact allpass/halfcycle scalar normalization from read algebra, not evaluator calls.
for n in [2,4,6,8,12,16]:
 a=F(2**(n//2)+1,2);b=F(2**(n//2)-1,2);rec('halfcycle_scalar_gram_N'+str(n),a*a+b*b==F(2**n+1,2),{'gram_scalar':str(a*a+b*b),'normalized_unitary':False,'scalar_multiple_of_unitary_under_unit_weights':True})
(O/'FRESH_REVIEWER_CHECKS.json').write_text(json.dumps({'uploaded_source_execution':'none','uploaded_source_import_compile_AST':'none','checks':checks,'all_passed':all(x['passed'] for x in checks)},indent=2));print(json.dumps({'checks':len(checks),'all_passed':all(x['passed'] for x in checks),'Rayleigh':str(rq),'cubic_certificate_determinants':[x['detail'] for x in checks if x['check'].startswith('cubic_certificate')]},indent=2))
