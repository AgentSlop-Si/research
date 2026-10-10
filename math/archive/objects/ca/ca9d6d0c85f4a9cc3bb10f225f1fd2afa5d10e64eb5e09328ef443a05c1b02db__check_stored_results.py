"""New review checks of inert data and independent arithmetic; no supplied program execution."""
from pathlib import Path,PurePosixPath
from fractions import Fraction as F
import hashlib,json,zipfile,io,re,math,gzip
O=Path(__file__).parent; E=json.load(open(O/'EVIDENCE_INDEX.json')); G={a['sha256']:a for a in json.load(open('code_coverage_audit_0228/ARCHIVE_GRAPH.json'))}; cache={}; checks=[]
def rec(name,ok,detail):
 checks.append({'check':name,'passed':bool(ok),'detail':detail});assert ok,name
def data(prefix):
 es=[e for e in E if e['sha256'].startswith(prefix)];assert len(es)==1;return json.loads((O/es[0]['local']).read_text())
def frac(d):return F(int(d['numerator']),int(d['denominator']))
def raw(h):
 if h not in cache:
  pieces=G[h]['first_observed_at'].split('!');b=(Path('fft_research_master_20261009')/pieces[0]).read_bytes()
  for n in pieces[1:]:
   with zipfile.ZipFile(io.BytesIO(b)) as z:b=z.read(n)
  assert hashlib.sha256(b).hexdigest()==h;cache[h]=b
 return cache[h]
def read_member(h,m):
 with zipfile.ZipFile(io.BytesIO(raw(h))) as z:b=z.read(z.infolist()[m['member_index']])
 assert hashlib.sha256(b).hexdigest()==m['sha256'];return b
manifests=[]; refs=[];summaries=[]
for e in E:
 file=O/e['local'];name=e['occurrences'][0]['member'];d=None
 if name.endswith('.json'):
  try:d=json.loads(file.read_text())
  except Exception:continue
  if re.search(r'result|certificate|receipt|guard|control|diagnostic',name,re.I):
   summaries.append({'sha256':e['sha256'],'names':[o['member'] for o in e['occurrences']],'top_level':{k:({'type':'list','count':len(v)} if isinstance(v,list) else {'type':'dict','keys':list(v)} if isinstance(v,dict) else v) for k,v in d.items()} if isinstance(d,dict) else {'type':'list','count':len(d)},'historical_only':True,'program_rerun':False})
 entries=[]
 if re.search(r'manifest|sha256sums',name,re.I):
  if d is not None:
   v=d.get('files',d) if isinstance(d,dict) else d
   if isinstance(v,dict):
    for k,a in v.items():
     if isinstance(a,str) and re.fullmatch('[0-9a-f]{64}',a):entries.append((k,a,None))
     elif isinstance(a,dict) and isinstance(a.get('sha256'),str):entries.append((a.get('path',k),a['sha256'],a.get('size_bytes',a.get('bytes'))))
   elif isinstance(v,list):
    entries=[(a.get('path',a.get('name')),a['sha256'],a.get('bytes',a.get('size_bytes'))) for a in v if isinstance(a,dict) and a.get('sha256') and a.get('path',a.get('name'))]
  else:
   for l in file.read_text().splitlines():
    m=re.fullmatch(r'([0-9a-f]{64})\s+\*?(.+)',l)
    if m:entries.append((m[2],m[1],None))
 for occ in e['occurrences']:
  h=occ['archive_sha256'];members=G[h]['members'];base=PurePosixPath(occ['member']).parent
  for path,expected,size in entries:
   candidates=[m for m in members if m['name'] in (str(base/path),path)]
   if not candidates:
    suffix=[m for m in members if m['name'].endswith('/'+path)];candidates=suffix if len(suffix)==1 else []
   match=any(m['sha256']==expected and(size is None or m['size_bytes']==size) for m in candidates)
   rehashed=False
   if candidates:
    for m in candidates:read_member(h,m)
    rehashed=True
   manifests.append({'manifest_sha256':e['sha256'],'manifest':occ['member'],'archive_sha256':h,'target_reference':path,'expected_sha256':expected,'resolved_candidates':[{'name':m['name'],'sha256':m['sha256']} for m in candidates],'status':'match' if match else 'mismatch' if candidates else 'unresolved_in_same_archive','archived_bytes_rehashed':rehashed})
  if isinstance(d,dict):
   for key,value in d.items():
    if not re.search(r'source.*sha256|sha256.*source|author_audit_sha256|dependency_sha256|local_sha256|accepted_small_chart_sha256',key):continue
    pairs=value.items() if isinstance(value,dict) else [(key,value)]
    for label,v in pairs:
     if not isinstance(v,str) or not re.fullmatch('[0-9a-f]{64}',v):continue
     hits=[m for m in members if m['sha256']==v]
     for m in hits:read_member(h,m)
     refs.append({'result_sha256':e['sha256'],'result':occ['member'],'field':key,'label':label,'sha256':v,'archive_sha256':h,'matching_archive_members':[m['name'] for m in hits],'status':'matched_archived_bytes' if hits else 'unresolved_in_same_archive'})
# Finite historical counters and derived inequalities, not rerunning their programs.
a=data('0ebfd9dd');rec('commuting_multiset_census',a['total_multisets_checked']==sum(v['multisets'] for r in a['exhaustive_short_multisets_numerical'] for v in r['rows'])==238767,{'matrices':len(a['exact_phase_matrix_checks']),'boundary_examples':len(a['strict_cutoff_examples'])})
a=data('17c27879');rec('allpass_operation_counts',all(r['preparation_field_operations']==r['N']+1 and r['application_field_operations']==7*r['N']-2 for r in a['operation_counts']),{'cases':len(a['operation_counts'])})
a=data('c3aa3af4');rec('linearizer_record_census',len(a['results'])==24 and a['total_matched_input_cases']==960,{'scope':'Historical recorded agreement, not reexecution or formal-identity proof.'})
a=data('701d1b75');rec('holonomy_boundary_data',a['b_equals_one_boundary_control']['premerge_cycle_lengths']==[4,4] and all(r['joint_group_order']==8 for r in a['one_level_instances']+a['hierarchical_chain_instances']),{'one_level':8,'chain':9})
a=data('bfc94510');rec('lowrank_counts',len(a['exact_fourier4'])==12 and len(a['numerical_perturbations'])==99 and len(a['product_checks'])==87,a['summary'])
a=data('92a0544f');rec('spectral_counts',len(a['spectral_instances'])==16 and len(a['isolation_instances'])==36,a['summary'])
a=data('6f4d0bb5');rec('macro_exact_census',a['affine_operator_matrix_cases']*5==a['affine_dense_gaussian_source_cases']+a['affine_singular_determinant_cases'] and a['exhaustive_permutation_movement_cases']==sum(math.factorial(n) for n in range(2,8)) and a['N64_boundary_budgets']==[32,21,13,7,4,2,1,0],{'affine':64,'permutations':5912,'nonuniform':11859,'cyclic_minors':2121})
a=data('5b08afc6');rec('v3_decoder_stored_error_bounds',len(a['experiments'])==15 and all(r['decoder_error_normalized']<=r['decoder_bound_normalized']+1e-12 for r in a['experiments']),{'rows':15,'scope':'Individual historical observations, not a probability certificate.'})
a=data('c414b1c7');rec('v4_decoder_stored_error_bounds',len(a['packed_correctness'])==20 and all(r['decoder_error_normalized']<=r['decoder_bound_normalized']+1e-12 for r in a['packed_correctness']),{'rows':20,'sampling_rows':len(a['sampling_scaling'])})
viol=[{'log2N':v['log2N'],'sample':v['eta_sample'],'total_claimed':v['eta_total_budget'],'sum_sampling_decoder':v['eta_sample']+v['eta_total_budget']/2} for kind in ['cost_model_linear','cost_model_subfft'] for v in a[kind] if v['eta_sample']+v['eta_total_budget']/2>v['eta_total_budget']+1e-15]
rec('v4_finite_budget_understatement_confirmed',bool(viol),{'violating_stored_rows':viol,'meaning':'Finite-size model bookkeeping, not asymptotic disproof.'})
a=data('91ea1951');rho=frac(a['polydisk_radius']);E0=frac(a['center_derivative_defect_bound']);c2=frac(a['quadratic_derivative_constant']);c3=frac(a['cubic_derivative_constant']);q=frac(a['contraction_factor_bound']);res=frac(a['residual_upper_bound']);h=[frac(v) for v in a['layer_matrix_bounds']];l=[frac(v) for v in a['layer_direction_bounds']]
rec('N16_stored_exact_scalar_certificate_reconciliation',c2==8*(l[2]*l[1]*h[0]+l[2]*h[1]*l[0]+h[2]*l[1]*l[0]) and c3==12*l[2]*l[1]*l[0] and q==E0+c2*rho+c3*rho*rho and frac(a['image_radius_upper_bound'])==res+q*rho<rho and q<1 and frac(a['physical_nonzero_margin'])>0,{'rho':str(rho),'q_decimal':float(q),'residual_decimal':float(res),'margin_decimal':float(frac(a['physical_nonzero_margin'])),'root_radius_refinement':str(res/(1-q)),'limitation':'Reconciles recorded rational scalars only, not matrix/chart recomputation.'})
b=data('20e30397');rec('outer_rejection_stored_scalar_certificate',frac(b['derived_seed_root_bound'])==res/(1-q)<frac(b['accepted_seed_root_radius_used']) and frac(b['total_preconditioned_minor_defect'])==frac(b['center_preconditioned_minor_defect'])+frac(b['seed_and_bank_minor_perturbation'])<1,{'total_defect_decimal':float(frac(b['total_preconditioned_minor_defect'])),'scope':b['scope']})
a=data('f9b0957b');rec('inner_guard_scalar_reconciliation',all(frac(r['total_nonsingularity_bound'])==frac(r['center_inverse_defect'])+frac(r['preconditioner_norm'])*frac(r['seed_direction_bound'])*frac(r['root_radius'])<1 for r in a['results']),{'bounds':[float(frac(r['total_nonsingularity_bound'])) for r in a['results']]})
a=data('18e2930b');rec('common_pole_minor_census',a['minor_count']==sum(len(r['sectors'][str(s)]['minors']) for r in a['rows'] for s in (-1,1))==96 and len(a['rows'])==32,{'minus_all_legal_rank':8,'plus_half_rank':7,'polynomials_not_recomputed':True})
a=data('138328e5');rec('mixer_stored_count_formula',all(r['forward_field_ops']-r['inverse_field_ops']==-2*r['n']-1 for r in a['exact_executor']),{'exact_lengths':len(a['exact_executor']),'gap_certificates':len(a['exact_gap_certificates'])})
# Four receipts: source snapshots are function-only. Hash decompressed inert JSON words.
receipts={}
for e in E:
 for o in e['occurrences']:
  m=re.fullmatch(r'results/(baseline|carrier)-(23|25)/receipt.json',o['member'])
  if not m:continue
  a=json.loads((O/e['local']).read_text());h=a['h'];R=a['compiled']['roles'];stem=str(PurePosixPath(o['member']).parent);member=next(x for x in G[o['archive_sha256']]['members'] if x['name']==stem+'/word.json.gz');word=gzip.decompress(read_member(o['archive_sha256'],member));digest=hashlib.sha256(word).hexdigest()
  rec('binary_receipt_'+m[1]+'_'+m[2],R==a['replay']['roles']==a['profile']['R'] and a['compiled']['rank_mass']==a['replay']['rank_mass']==a['profile']['rank_sum']==h*R+h*(h-1) and digest==a['word_sha256'],{'roles':R,'rank_mass':a['compiled']['rank_mass'],'decompressed_word_sha256':digest,'full_word_replay_performed':False})
  receipts[(m[1],h)]=a
rec('carrier_no_role_improvement',all(receipts[('baseline',h)]['compiled']['roles']==receipts[('carrier',h)]['compiled']['roles'] for h in (23,25)),{'h23_word_unchanged':receipts[('baseline',23)]['word_sha256']==receipts[('carrier',23)]['word_sha256'],'h25_word_changed':receipts[('baseline',25)]['word_sha256']!=receipts[('carrier',25)]['word_sha256'],'meaning':'Historical local variant changes an h25 word but not role count; no new saving established.'})
# Independent fresh arithmetic demonstrations, not copied algorithms or supplied imports.
rec('finite_field_function_derivative_scope',all(pow(x,3,3)==x for x in range(3)) and 3%3==0,{'p':3,'same_function':'x^3=x','formal_derivatives':[0,1]})
rec('insufficient_general_root_guard',pow(6,6,7)==1 and pow(6,3,7)!=1 and pow(6,2,7)==1,{'prime':7,'N':6,'generator':6,'guard_accepts_root_order':2})
rec('event_replay_scanning_counterexample',sum(range(1,101))==5050,{'events':100,'queries':100,'lag_each':1,'q':1,'without_compact_total_loop_visits':5050,'advertised_replay_work_units':100,'source_trace_only':True})
rec('negative_cpp_remainder_guard',-(1%8)==-1,{'N':8,'pa':0,'pb':0,'sparse_position':-1,'Cplusplus_remainder':-1,'emitted_access':'out[-1]','no_Cplusplus_executed':True})
before=2.5e307;increment=1e308*.25;changed=before+increment;overflow=1e308+1e308
rec('subscription_nonatomic_overflow_arithmetic',math.isinf(overflow) and math.isfinite(changed) and changed!=before,{'old_edit':1e308,'delta':1e308,'opposite_sample':.25,'cached_before':before,'cached_after_before_guard':changed,'rejected_metadata_sum':'infinity','supplied_method_executed':False})
rec('invalid_contraction_guard_can_pass',F(1)/(1-F(2))<F(2,10**12),{'e':'1','q':'2','e/(1-q)':'-1','guard_must_also_require_q_below_1':True,'stored_valid_certificate_unaffected':True})
rec('finite_model_budget_exact',F(3,4)+F(95,100)/2==F(49,40)>F(95,100),{'log2N':64,'sample':'3/4','decoder':'19/40','total':'49/40','label_budget':'19/20'})
perm=[((x+2*y+1)%4)*2+y for x in range(4) for y in range(2)];seen=set();lens=[]
for i in range(8):
 if i in seen:continue
 v=i;n=0
 while v not in seen:seen.add(v);n+=1;v=perm[v]
 lens.append(n)
rec('b1_boundary_fresh_cycles',lens==[4,4],{'permutation':perm,'cycle_lengths':lens})
rec('halfcycle_N2_boundary_exact',F(3,2)**2+F(1,2)**2==F(5,2),{'S_squared':'-I','K':'(3I+S)/2','K_adjoint_K':'(5/2)I','word_length':1,'N_over_2':1,'not_shorter_than_boundary':True})
rec('oddN_spectral_formula_scope',F(7,3)!=F(9,4),{'N':3,'true_min_singular_squared_at_eigenvalue_minus1':'9/4','even_formula_gives':'7/3','supplied_test_sizes_all_even':True})
rec('retained_phase_padding',math.ceil(2049/1024)*1024*16==49152>2049*16,{'visible_bytes':32784,'retained_bytes':49152})
(O/'STORED_MANIFEST_RECONCILIATION.json').write_text(json.dumps(manifests,indent=2));(O/'STORED_HASH_REFERENCE_RECONCILIATION.json').write_text(json.dumps(refs,indent=2));(O/'STORED_RESULT_SUMMARIES.json').write_text(json.dumps(summaries,indent=2));(O/'FRESH_REVIEWER_CHECKS.json').write_text(json.dumps({'source_execution':'none','source_import_compile_AST':'none','checks':checks},indent=2))
print(json.dumps({'fresh_checks':len(checks),'all_passed':all(c['passed'] for c in checks),'manifest_statuses':{s:sum(v['status']==s for v in manifests) for s in set(v['status'] for v in manifests)},'hash_reference_statuses':{s:sum(v['status']==s for v in refs) for s in set(v['status'] for v in refs)},'stored_result_summaries':len(summaries),'budget_understatement_rows':viol},indent=2))
