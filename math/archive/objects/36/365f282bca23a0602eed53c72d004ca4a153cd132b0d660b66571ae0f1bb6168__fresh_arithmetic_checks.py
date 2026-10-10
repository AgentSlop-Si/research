"""Fresh arithmetic/metadata only: reads saved JSON/bytes, no supplied source imports."""
from pathlib import Path
from fractions import Fraction
import json,math,hashlib,collections,itertools,re
B=Path(__file__).resolve().parent
rows=json.loads((B/'STORED_RESULT_RECONCILIATION.json').read_text());P=json.loads((B/'PROVENANCE.json').read_text());E=json.loads((B/'EVIDENCE_INDEX.json').read_text());I={e['path']:e for e in E}
checks=[]
def record(name,condition,detail):
 checks.append({'check':name,'passed':bool(condition),'details':detail});assert condition,name
def read(n):return json.loads((B/rows[n-1]['result_evidence']['local']).read_text())
def sibling(n,name):return B/I[str(Path(P[n-1]['representative_path']).parent/name)]['local']
# Independent combinatorial counts and precise arithmetic, not transform replays.
d=read(1);record('S01 exact grid-count arithmetic',d['exact_grids']=={'lengths':260,'exact_phase_exponent_checks':sum(range(1,257))+511+513+1001+10007},d['exact_grids'])
record('S01 exhaustive permutation total',sum(d['finite_rank_gate']['outcomes'].values())==math.factorial(8),{'expected':math.factorial(8),'stored':d['finite_rank_gate']['outcomes']})
d=read(3);record('S03 rational condition proxy',Fraction(155,98)==(1/(1-Fraction(1,4))+1/(1-Fraction(1,5)))/(1/(1+Fraction(1,4))+1/(1+Fraction(1,5))),{'condition_bound':d['improved_complex_condition_bound']})
record('S03 singular sum on constants',1/(1-Fraction(3,2))+1/(1-Fraction(1,2))==0,{'alpha':'3/2','beta':'1/2','ones_eigenvalue':0})
d=read(5);record('S05 exact checker self-hash',d['checker_sha256']==P[4]['sha256'],{'sha256':d['checker_sha256']})
record('S05 completed-bank output counts',all(r.get('degenerate_odd') or r['completed_bank_entries_verified']==r['N']**2 and r['executor_entries_verified']==r['M']*r['N']**2 for r in d['finite_field']),{'fixture_count':len(d['finite_field'])})
d=read(6);err=3*(Fraction(5,6)**2+Fraction(7,6)**2);prob=Fraction(6*2**51,6**26)
record('S06 exact offset-grid rejection',err==Fraction(37,6)>4 and prob<Fraction(1,10000),{'error_squared':str(err),'tolerance_squared':4,'claimed_failure':str(prob),'stored_error':d['exact_offset_certificate_counterexample']['error_squared']})
record('S06 log-base block mismatch',4<=math.log(256)<8 and math.log2(256)==8,{'Q':256,'natural_log_rule_M':4,'base_two_rule_M':8,'stored':d['bessel_block_mismatch']})
d=read(7);record('S07 exhaustive N4 one-mode pair count',d['counts']['exhaustive_one_mode_pairs_N4']==9**4,{'stored':d['counts']['exhaustive_one_mode_pairs_N4'],'expected':9**4})
d=read(8);record('S08 exact exhaustive membership count',d['counts']['exhaustive_row_membership_vectors']==7**3+5**4+7**6,{'stored':d['counts']['exhaustive_row_membership_vectors']})
record('S08 fiber divisor scope gap',set(q for q in range(1,math.isqrt(12)+1) if 12%q==0)=={1,2,3} and set(q for q in range(1,13) if 12%q==0)=={1,2,3,4,6,12},{'N':12,'loop_Q':[1,2,3],'all_factorization_Q':[1,2,3,4,6,12]})
d=read(9);record('S09 kernel and reset enumeration counts',d['counts']['kernel_identities']==(7+17+31)*6*20 and d['counts']['reset_optimizer_checks']==sum(5**i for i in range(1,6))*3*4,{'kernels':d['counts']['kernel_identities'],'resets':d['counts']['reset_optimizer_checks']})
record('S09 reset support budget counterexample',sum([4,1,1])-max([4,1,1])==2<=4,{'supports':[4,1,1],'single_optimal_reset_remaining_support':2,'greedy_reset_after_accepting_4_cannot_fit_final_1':True})
d=read(13);record('S13 large rational coefficient bit counts',all(r['lambda_bits']==(math.factorial(r['n']//2)*(2*20**r['n'])**(r['n']//2)+2).bit_length() for r in d['rational_mixer']),{'stored_bit_counts':[r['lambda_bits'] for r in d['rational_mixer']]})
d=read(14);record('S14 useless median bound',all(17*Fraction(3,2)**h>1 for h in range(1,101)),{'formula':'17*(3/2)^h','h_checked':[1,100],'exponential_base_gt_one':True})
d=read(15);record('S15 stored case and rank counts',len(d['cases'])==d['case_count']==d['selected_commutator_determinants'] and d['correlated_rank_inequalities']==2*len(d['cases']) and sum(r['boundary_cycle_checks'] for r in d['cases'])==d['boundary_cycle_checks'],{'cases':d['case_count'],'boundary_checks':d['boundary_cycle_checks']})
d=read(16);record('S16 fixture counts',len(d['positive_fixed_factor_controls'])==10 and len(d['negative_fixed_factor_controls'])==10 and len(d['short_fingerprint_collision_controls'])==3,{'positive':10,'negative':10,'collision':3})
d=read(19);counter=d['noncanonical_residue_interface_counterexample'];p=counter['prime'];record('S19 noncanonical residues really coincide',[[x%p for x in row] for row in counter['target']]==counter['middle'],counter)
d=read(20);port=json.loads(sibling(20,'PORTABILITY.json').read_text());record('S20 stored replay source/result hash bindings',port['checker_sha256']==P[19]['sha256'] and port['result_sha256']==rows[19]['result_evidence']['sha256'],{'checker_sha256':port['checker_sha256'],'result_sha256':port['result_sha256'],'fresh_replay':False})
d=read(22);record('S22 exhaustive F5 Q4 case count',d['exhaustive_F5_Q4']['cases']==5**4*2*4*3,{'expected':15000,'stored':d['exhaustive_F5_Q4']['cases']})
d=read(23);fc=d['field_cases'];record('S23 full-output vector and bin totals',d['raw_full_transform_cases']==3*len(fc) and d['full_output_bins']==3*sum(c['N'] for c in fc) and d['convolution_checks']==4*len(fc),{'shapes':len(fc),'vectors':d['raw_full_transform_cases'],'bins':d['full_output_bins'],'convolutions':d['convolution_checks']})
root_checks=[]
for c in fc:
 p=c['p'];prime=p>1 and all(p%k for k in range(2,math.isqrt(p)+1));orders=[]
 for w,n in [(c['omega'],c['N']),(c['fft_root'],c['L'])]:orders.append(pow(w,n,p)==1 and all(pow(w,k,p)!=1 for k in range(1,n) if n%k==0))
 root_checks.append(prime and all(orders))
record('S23 fixture primality and both root orders',all(root_checks),{'field_cases':len(fc),'root_checks':2*len(fc)})
rankbytes=(B/rows[23]['result_evidence']['local']).read_bytes();record('S24 rank stream count and digest',len(rankbytes)==(8*7*6)**2 and set(rankbytes)=={15} and hashlib.sha256(rankbytes).hexdigest()=='9cb47d8a53038d7d482f3013df8d520bcc301db183b8a4914f383a9e1c5f8e70',{'bytes':len(rankbytes),'histogram':dict(collections.Counter(rankbytes)),'sha256':hashlib.sha256(rankbytes).hexdigest(),'meaning':'Stored ranks only, no new Macaulay computation'})
record('S24 saved failure list empty',sibling(24,'anchor_failures.txt').stat().st_size==0,{'bytes':sibling(24,'anchor_failures.txt').stat().st_size})
family=list(map(int,sibling(24,'family_N8.txt').read_text().split()));n,p=family[:2];entries=family[2:];record('S24 actual saved input within int64 product range',n==8 and len(entries)==4*n*n and all(0<=v<p for v in entries) and (p-1)**2<=2**63-1,{'N':n,'p':p,'matrix_entries':len(entries),'max_possible_single_product':(p-1)**2,'int64_max':2**63-1})
record('S24 unguarded wider-prime counterdomain',(4294967291-1)**2>2**63-1,{'example_modulus':4294967291,'max_residue_product':(4294967291-1)**2,'int64_max':2**63-1,'source_not_invoked':True})
d=read(25);record('S25 degree-identifying evaluation counts',all(v['identified_evaluations']==[int(k)**2+1,2*int(k)**2+1] for k,v in d['two_parameter_certificates'].items()),d['two_parameter_certificates'])
record('S25 exhaustive N4 permutation count',d['all_N4_minors_p998244353']['count']==d['all_N4_minors_p2013265921']['count']==math.factorial(4)**2,{'per_field':576})
record('S25 finite permutation metadata',all(v['permutations']==math.factorial(int(k)) and v['minimum']==int(k)//2 and v['minimizers']==1 for k,v in d['v16_exhaustive_permutations'].items()),{'sizes':list(d['v16_exhaustive_permutations'])})
d=read(32);record('S32 stored cut capacities',all(sum(a[2] for a in r['cut'])==r['capacity'] and r['deficit']==r['I'][1]-r['I'][0]-r['capacity'] for r in d['cases']),{'cases':len(d['cases']),'note':'capacity arithmetic only; no new graph maxflow'})
# Check a complete stored modular Bezout identity with safe JSON integer arithmetic.
z=json.loads(sibling(33,'N4_EQUAL_OUTER_MODULAR_BEZOUT.json').read_text());p=z['p'];v=[0]*60
for aa,bb in [(z['P'],z['U']),(z['Q'],z['V'])]:
 for i,a in enumerate(aa):
  for j,b in enumerate(bb):v[i+j]=(v[i+j]+a*b)%p
record('S33 modular Bezout integer identity',v==[0]*59+[1] and z['image_i']**2%p==p-1 and all(p%k for k in range(2,math.isqrt(p)+1)),{'p':p,'i_image':z['image_i'],'coefficient_order':'descending','lhs':v,'no_sympify_used':True})
d=read(36);record('S36 all-row-pair record coverage',len({tuple(r['rows']) for r in d['records']})==len(d['records'])==math.comb(16,2) and sum(d['certificate_kinds'].values())==120,{'row_pairs':120,'kinds':d['certificate_kinds']})
d=read(37);record('S37 stored Schur-rank and support counters',all(c['block_rank']==c['M']**2 and max(c['sparse_counts']['K'].values())<=9 and max(c['sparse_counts']['W1'].values())<=6 and max(c['sparse_counts']['W2'].values())<=6 for c in d),{'cases':len(d)})
d=read(38);cc=d['growing_radix']['cases'];record('S38 growing-radix expanded-volume ledger',all(r['expanded_inputs']==r['M']**2*r['b'] and r['applications']==r['m']*r['b']**3 and r['distinct_nodes']==r['m']//math.gcd(r['b'],r['m']) for r in cc),{'banks':len(cc),'summed_expanded_inputs':sum(r['expanded_inputs'] for r in cc)})
a=read(39)['uniform_cut_cases'];b=read(42)['uniform_cut_cases'];record('S39/S42 independently stored cut summaries agree',[(r['N'],r['cut_size'],r['Fourier_minor_size'],r['gap']) for r in a]==[(r['N'],r['cut_nodes'],r['source_width'],r['gap']) for r in b],{'cases':len(a),'first_positive_deficit_N':64})
d=read(41);c=d['cutoff_rectangle'];record('S41 exact large-N discrepancy arithmetic',d['cutoff_N']==2**27 and c['count']*d['cutoff_N']-c['W']*c['t']>9*d['cutoff_N'],{'N':d['cutoff_N'],'rectangle':c,'does_not_execute_large_N_transform':True})
d=read(43);record('S43 Jacobian certificate shape and dimension ledger',all(r['raw_separated_chart_variables']==4*(5*r['N']-4) and r['exact_modular_jacobian_rank']<=min(r['N']**2,17*r['N']-26) and (r['N']!=16 or len(r['nonzero_minor_certificate']['rows_in_order'])==len(r['nonzero_minor_certificate']['columns_in_order'])==246 and r['nonzero_minor_certificate']['determinant_mod_1009']!=0) for r in d['cases']),{'cases':len(d['cases']),'N16_minor_size':246,'no_new_jacobian_evaluation':True})
d=read(45);record('S45 noncoprime dimension metadata',all(r['independent_kernel_vectors']==r['N']//2>r['naive_d_plus_K'] for r in d['noncoprime_dimension_counterexamples']),d['noncoprime_dimension_counterexamples'])
d=read(47);record('S47 bank false positive trace arithmetic',(6*6+7*7+1+1)%17==2!=6,d['projector_false_positive'])
d=read(48);rs=d['N16_exact_coupling_rows'];record('S48 coupling cancellation ledgers',all(r['minimum_support_nonzero_couplings']==r['G_only']+r['J_only']+r['overlap']-r['maximum_simultaneous_cancellations'] and r['minimum_support_nonzero_couplings']>=r['G_only']+r['J_only']>=2 for r in rs),{'rows':len(rs),'minimum':d['N16_minimum_support_alpha_beta_nonzero']})
d=read(49);record('S49 planted normalization control metadata',all(c['positive_rank_one_gauge'] and c['single_entry_corruption_detected'] and c['interior_zero_detected'] for c in d['gauge_controls']),{'positive_and_negative_controls':len(d['gauge_controls'])})
d=read(51);record('S51 projective certificate partition counts',d['all_five_row_subsets_verified']==math.comb(16,5)==sum(d['certificate_counts'].values()) and sum(d['leading_coefficient_patterns'].values())==d['certificate_counts']['nonzero_homogeneous_resultant'],{'subsets':d['all_five_row_subsets_verified'],'kinds':d['certificate_counts'],'endpoint_patterns':d['leading_coefficient_patterns']})
record('S51 modular cyclotomic root relation',pow(8,8,97)==96 and pow(8,16,97)==1,{'p':97,'root':8})
d=read(52);record('S52 permutation/support cover count',d['permuted_F4_targets_tested']==math.factorial(4)**2 and len(d['all_relative_support_covers'])==2,{'permutations':576,'support_covers':2})
# Gaussian-integer arithmetic checks the tiny standard DFT factorization independently.
def gp(x,y):return (x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def matproduct(x,y):
 return [[tuple(sum(gp(x[i][k],y[k][j])[t] for k in range(4)) for t in (0,1)) for j in range(4)] for i in range(4)]
def lift(x):return [[(a,0) for a in r] for r in x]
A=lift([[1,1,0,0],[1,-1,0,0],[0,0,1,1],[0,0,1,-1]])
C=lift([[1,0,1,0],[0,1,0,1],[1,0,-1,0],[0,1,0,-1]])
D=lift([[int(i==j) for j in range(4)] for i in range(4)]);D[3][3]=(0,-1)
R=lift([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]])
answer=matproduct(matproduct(matproduct(C,D),A),R);units=[(1,0),(0,-1),(-1,0),(0,1)]
record('S52 independent exact Gaussian-integer F4 product',answer==[[units[i*j%4] for j in range(4)] for i in range(4)],{'entries':16,'arithmetic':'integer pairs only','matrix':answer})
write={'scope':'Fresh independently authored integer/Fraction arithmetic and stored-data checks only. No archived Python/C++ executed, imported, compiled or AST-parsed. Count/metadata checks are not transform/certificate reruns.','checks':checks,'check_count':len(checks),'all_passed':all(c['passed'] for c in checks)}
(B/'FRESH_REVIEWER_CHECKS.json').write_text(json.dumps(write,indent=2)+'\n');print(json.dumps({'checks':len(checks),'all_passed':write['all_passed']},indent=2))
