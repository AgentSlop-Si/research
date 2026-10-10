"""Fresh reviewer data-only integrity, counters, and mathematical checks; no source execution/import/AST."""
from pathlib import Path,PurePosixPath
import json,hashlib,re,math,gzip,itertools,zipfile,io
O=Path(__file__).parent
E=json.load(open(O/'EVIDENCE_INDEX.json')); G={a['sha256']:a for a in json.load(open('code_coverage_audit_0228/ARCHIVE_GRAPH.json'))}
checks=[]
def record(name,condition,detail):
 checks.append({'check':name,'passed':bool(condition),'detail':detail})
 # Record failures without suppressing remaining evidence reconciliation.
def data(prefix):
 es=[e for e in E if e['sha256'].startswith(prefix)];assert len(es)==1
 return json.loads((O/es[0]['local']).read_text())
archive_cache={}
def archive_bytes(h):
 if h in archive_cache:return archive_cache[h]
 pieces=G[h]['first_observed_at'].split('!');b=(Path('fft_research_master_20261009')/pieces[0]).read_bytes()
 for name in pieces[1:]:
  with zipfile.ZipFile(io.BytesIO(b)) as z:b=z.read(name)
 assert hashlib.sha256(b).hexdigest()==h
 archive_cache[h]=b;return b
manifest=[]
for e in E:
 name=PurePosixPath(e['member']).name.lower()
 if not any(t in name for t in ['manifest','sha256','bundle_sha']):continue
 text=(O/e['local']).read_text();entries=[]
 if name.endswith('.json'):
  d=json.loads(text);d=d.get('files',d) if isinstance(d,dict) else d
  if isinstance(d,list):entries=[(v['path'],v['sha256'],v.get('bytes')) for v in d if isinstance(v,dict) and 'path' in v and 'sha256' in v]
  elif isinstance(d,dict):
   for k,v in d.items():
    if isinstance(v,str) and re.fullmatch('[0-9a-f]{64}',v):entries.append((k,v,None))
    elif isinstance(v,dict) and 'sha256' in v:entries.append((k,v['sha256'],v.get('bytes')))
 else:
  for line in text.splitlines():
   m=re.fullmatch(r'([0-9a-f]{64})  (.+)',line)
   if m:entries.append((m[2],m[1],None))
 members={m['name']:m for m in G[e['archive_sha256']]['members']};base=PurePosixPath(e['member']).parent
 if name=='hardened_v3_manifest.json':base=base/'hardened_overlay' # Explicit location stated in archived README_AUDIT.md.
 for rel,sha,size in entries:
  target=str(base/rel);m=members.get(target);ok=bool(m and m['sha256']==sha and(size is None or m['size_bytes']==size))
  with zipfile.ZipFile(io.BytesIO(archive_bytes(e['archive_sha256']))) as archive:
   actual=archive.read(target) if target in archive.namelist() else b''
  ok=ok and hashlib.sha256(actual).hexdigest()==sha and(size is None or len(actual)==size)
  manifest.append({'manifest':e['member'],'target':target,'sha256':sha,'matches_containing_archive':ok,'archived_member_bytes_rehashed':bool(m),'actual_archive_sha256':m['sha256'] if m else None,'present_in_containing_archive':bool(m)})
record('stored_manifest_entries',all(x['matches_containing_archive'] for x in manifest),{'entries':len(manifest),'mismatches':[x for x in manifest if not x['matches_containing_archive']]})
refs=[]
for e in E:
 if not e['member'].endswith('.json'):continue
 d=json.loads((O/e['local']).read_text())
 if not isinstance(d,dict):continue
 for key in ('source_sha256','author_audit_sha256','dependency_sha256','sha256'):
  if key not in d:continue
  value=d[key];pairs=value.items() if isinstance(value,dict) else [(key,value)]
  for label,h in pairs:
   if not isinstance(h,str) or not re.fullmatch('[0-9a-f]{64}',h):continue
   hits=[m['name'] for m in G[e['archive_sha256']]['members'] if m['sha256']==h]
   refs.append({'evidence':e['member'],'field':key,'label':label,'sha256':h,'matching_archive_members':hits})
record('stored_source_hash_references',all(v['matching_archive_members'] for v in refs),{'references':len(refs)})
# Reconcile declared loop populations and arithmetic ledgers against stored data.
a=data('504c02e9');record('phase9_stored_suite_population',sum(v['unittest_count'] for v in a)==253 and all(v['passed'] for v in a),{'suite_count':len(a),'unittest_count':sum(v['unittest_count'] for v in a),'scope':'Archived reports; suites include inherited code, not just 50 assigned sources.'})
a=data('cb7f1f50');record('median_stored_population',len(a['one_row_equivalence'])==4 and len(a['local_variance_checks'])==18 and len(a['median_comparison'])==36 and len(a['local_sparse_exact_recovery'])==12 and len(a['tone_moment_barrier'])==5,a['summary'])
record('median_sparse_union_formula',all(math.isclose(r['union_failure_upper_bound'],min(1.,r['K']*r['M']*math.comb(r['rows'],(r['rows']+1)//2)*(((r['M']-1)*r['h']/r['K'])**((r['rows']+1)//2)))) for r in a['local_sparse_exact_recovery']),{'records':12,'trials':sum(r['trials'] for r in a['local_sparse_exact_recovery'])})
record('tone_fourth_moment_formula',all(math.isclose(r['closed_form_kurtosis'],r['K']/(r['M']-1)+2-2/(r['M']-1)) for r in a['tone_moment_barrier']),{'records':5})
a=data('045005ec');record('documented_snapshot_cancellation',a['snapshot_subtraction_cancellation']=={'represented_state_fft':1.0,'coalesced':0.0,'explicit_rebase':1.0},a['snapshot_subtraction_cancellation'])
a=data('6f619487');record('fixed_pair_loop_counts',a['independent_fork_cases']==12*60 and a['accumulating_stream_steps']==12*60*5 and a['sibling_fork_checks']==3600,a)
a=data('b3032d3d');record('v2_stored_suffix_and_oracles',all(v['visited_events']==2 and v['correct'] for v in a['shared_history']) and a['arbitrary_bin_sweep']['comparisons']==234 and a['multi_consumer_sweep']['comparisons']==3000,{'shared_history':a['shared_history'],'arbitrary':a['arbitrary_bin_sweep'],'multi':a['multi_consumer_sweep']})
a=data('0dfdd1fe');record('v3_stored_remaining_costs',a['partition_history']['after_200_replans']==201 and a['update_replan_cost'][-1]['cluster_metric_calls']==5457 and not a['same_version_cache_roundoff']['bitwise_identical'],{'update_replan_cost':a['update_replan_cost'],'partition_history':a['partition_history'],'roundoff':a['same_version_cache_roundoff']})
a=data('1107e0e3');record('decimation_populations',a['cases']==len(a['rows'])==13 and a['full_basis_vectors']==sum(r['n'] for r in a['rows'])==138 and a['normalized_split_basis_vectors']==sum(max(0,2*r['n']-4) for r in a['rows'])==224,{'cases':13,'basis':138,'split_basis':224})
record('decimation_node_and_horner_ledgers',all(r['full_H_count']['recursive_nodes_by_depth']=={str(d):3**d for d in range(r['n'].bit_length()-1)} and r['sparse_Horner_comparison']=={'mul':3*r['n']**2-2*r['n'],'add':2*r['n']**2-2*r['n']} for r in a['rows']) and all(r['sparse_Horner_online_operations']==5*r['n']**2-4*r['n'] for r in a['larger_gate_ledgers']),{'rows':13,'larger_ledgers':a['larger_gate_ledgers']})
a=data('3336399f');record('feedback_populations',a['cases']==36 and a['full_state_basis_vectors']==sum(r['basis_vectors'] for r in a['cases_detail'])==840 and a['random_full_states']==4*36,{'cases':36,'basis':840,'random':144,'focused_valid':a['focused_valid_edge_cases']})
for r in a['cases_detail']+a['examples']:
 n,R=r['n'],r['R'];d=r['cost'];k=d['rank_one_correction'];M=d['ADD_T_calls'];g=r['gain_update'];kg=g['rank_one_correction'];prep=r['coefficient_preparation']
 record('feedback_ledger_'+str(n)+'_'+str(R)+'_'+r['mode']+'_'+str(r.get('p','example')),d['acyclic_scalar_instructions']==3*M*n*(n+1)//2+2*(R-1)*(6*n-3) and k['scalar_instructions']==6*k['functional_nonzeros']+3*k['output_nonzeros']-4 and d['scalar_instructions']==d['acyclic_scalar_instructions']+k['scalar_instructions'] and kg['scalar_instructions']==6*kg['functional_nonzeros']+3*kg['output_nonzeros']-4 and prep=={'mul':(R-1)*(3*n-1)+2*n,'add':(R-1)*(2*n-1)+n-1,'sub':1,'constant_inverse':1},{'online_initial':d['scalar_instructions'],'gain_update':kg['scalar_instructions'],'scope':'Additional base q-kernel, compilation and reciprocal preparation not included in online gate total.'})
# Recompute native timing summaries from raw samples, without invoking any transform.
a=data('685f2491');summary=data('171f027c');rows=a['results']
record('native_measurement_population',len(rows)==147 and len(a['dynamic_range_checks'])==64 and a['checksum_calls']==147*(1+a['repeats']),{'rows':len(rows),'raw_timing_samples':sum(len(r['raw_seconds']) for r in rows),'checksums':a['checksum_calls']})
def qtl(v,f):
 s=sorted(v);p=(len(s)-1)*f;i=int(p);return s[i] if i==len(s)-1 else s[i]+(s[i+1]-s[i])*(p-i)
record('native_raw_sample_summaries',all(math.isclose(r['median_seconds'],qtl(r['raw_seconds'],.5),rel_tol=1e-14) and math.isclose(r['q25_seconds'],qtl(r['raw_seconds'],.25),rel_tol=1e-14) and math.isclose(r['q75_seconds'],qtl(r['raw_seconds'],.75),rel_tol=1e-14) and r['minimum_seconds']==min(r['raw_seconds']) for r in rows),{'rows':147})
for r in rows:
 match=[x for x in rows if (x['n'],x['family'])==(r['n'],r['family'])];native=min((x for x in match if x['method'] in ['native_dit','native_dif']),key=lambda x:x['median_seconds']);numpy=next(x for x in match if x['method']=='numpy')
 r['nw']=r['q75_seconds']<native['q25_seconds'];r['pw']=r['q75_seconds']<numpy['q25_seconds']
 record('native_ratio_'+str(r['n'])+'_'+r['family']+'_'+r['method'],math.isclose(r['ratio_to_faster_native_baseline'],r['median_seconds']/native['median_seconds'],rel_tol=1e-14) and math.isclose(r['ratio_to_numpy'],r['median_seconds']/numpy['median_seconds'],rel_tol=1e-14),{'scope':'Stored sample arithmetic only'})
ap=[r for r in rows if r['method'].startswith('epsilon')]
sets={'all_approximate':ap,'nonzero_outputs':[r for r in ap if not r['all_zero_output']],'nonzero_and_relative_l2_error_at_most_1e_minus_10':[r for r in ap if not r['all_zero_output'] and r['relative_l2_error']<=1e-10],'all_zero_outputs':[r for r in ap if r['all_zero_output']],'zero_only_mode':[r for r in rows if r['method']=='zero_pruned']}
for name,rs in sets.items():
 got={'cases':len(rs),'native_median_wins':sum(r['ratio_to_faster_native_baseline']<1 for r in rs),'numpy_median_wins':sum(r['ratio_to_numpy']<1 for r in rs),'native_nonoverlapping_middle_half_wins':sum(r['nw'] for r in rs),'numpy_nonoverlapping_middle_half_wins':sum(r['pw'] for r in rs)}
 record('native_stratification_'+name,all(summary[name][k]==v for k,v in got.items()),got)
a=data('ffb25ee2');record('native_basis_population',a['basis_vectors']==sum(2**k for k in range(7))==127 and a['basis_method_comparisons']==6*127 and len(a['near_threshold_controls'])==3,a)
a=data('a6a8b5c2');record('boundary_population_and_ledgers',a['cases']==13 and a['basis_vectors']==138 and all(r['one_sparse_C']['field_operations']=={'mul':2*r['n'],'add':r['n']} and r['full_H_C_horner']['field_operations']=={'mul':3*r['n']**2-2*r['n'],'add':2*r['n']**2-2*r['n']} for r in a['cases_detail']),{'cases':13,'basis':138,'negative_control':a['finite_exponential_negative_control']})
a=data('f16d4196');record('resolvent_populations',a['configurations']==15 and a['basis_vectors']==266 and a['shifted_resolvent_vectors']==3*(266+15) and a['covariance_chain_outputs']==5*15,{'basis':266,'shifted_resolvents':843,'chain_outputs':75})
for r in a['cases']:
 n=r['n'];l=n.bit_length()-1
 record('resolvent_bills_'+r['field']+'_'+str(n),r['fast_online']=={'mul':5*n*l//2+8*n,'add':5*n*l//2+2*n,'sub':5*n*l//2+2*n} and r['resolvent_query']=={'mul':4*n+l,'sub':n,'constant_inverse':1,'neg':n,'add':2*n-1},r['resolvent_query'])
a=data('93b98755');record('tail_populations',a['configurations']==48 and a['basis_vectors']==sum(r['n'] for r in a['records'])==1318 and a['mixed_vectors']==96 and a['aggregate_identity_checks']==52 and a['full_similarity_checks']==42,{'cases':48,'basis':1318,'mixed_polynomial_uses':96,'aggregate_checks':52,'full_comparator':42})
for r in a['records']:
 n,k=r['n'],r['r'];l=n.bit_length()-1;s=(2*k).bit_length()-1;b=(2*n+4*k)*s
 record('tail_ledger_'+r['field']+'_'+str(n)+'_'+str(k),r['online']=={'mul':b+6*n+8*k,'add':b+2*n-2*k,'sub':b} and r['forward_ffts']==n//k+2 and r['inverse_ffts']==n//k+2,r['online'])
arithmetic=('mod_mul','mod_add','mod_sub','int_mul','int_add','int_sub','int_neg','divmod')
for pref,expected,keys in [('08679a3b',195,['cold_baseline','cold_graph','warm_baseline','warm_graph']),('90c61351',96,['cold_baseline','coordinate_chain','numeric_chain','warm_numeric_chain'])]:
 a=data(pref);record('integer_population_'+pref,a['exact_integer_products_checked']==expected,{'products':expected,'cases':len(a['cases'])})
 for r in a['cases']:
  for key in keys:
   d=r[key];record('integer_ledger_'+pref+'_'+str(r['n'])+'_'+r.get('family','numeric')+'_'+key,d['total_arithmetic']==sum(d['counts'].get(k,0) for k in arithmetic) and d['product_arithmetic']==sum(x[2] for x in d['schedule']) and d['total_arithmetic']==d['preparation_arithmetic']+d['discovery_arithmetic']+d['product_arithmetic']+4*r['n']*8,{'total_arithmetic':d['total_arithmetic'],'scope':'Comparisons/copies/addressing separate from scalar-arithmetic objective'})
a=data('866e1e60');record('grading_populations_and_ledgers',a['configurations']==13 and a['basis_vectors']==138 and a['related_outputs']==552 and all(r['preparation']=={'mul':21*r['n']//2+r['n'].bit_length()-1-3,'sub':2*r['n']-1,'constant_inverse':2,'neg':r['n']+1} and r['input_output_update']=={'mul':3*r['n']-1,'add':r['n']-1} for r in a['rows']),{'cases':13,'basis':138,'related_outputs':552})
(O/'STORED_MANIFEST_RECONCILIATION.json').write_text(json.dumps(manifest,indent=2));(O/'STORED_HASH_REFERENCE_RECONCILIATION.json').write_text(json.dumps(refs,indent=2));(O/'STORED_EVIDENCE_CHECKS.json').write_text(json.dumps({'method':'Reviewer data-only recomputation; supplied source never executed/imported/compiled/AST-parsed','checks':checks},indent=2))
print(json.dumps({'checks':len(checks),'passed':sum(v['passed'] for v in checks),'failed_check_names':[v['check'] for v in checks if not v['passed']],'manifest_entries':len(manifest),'hash_references':len(refs)},indent=2))
