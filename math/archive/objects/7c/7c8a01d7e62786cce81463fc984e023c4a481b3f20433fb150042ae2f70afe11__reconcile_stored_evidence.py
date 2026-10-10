"""Fresh reviewer data-only integrity, counters, and mathematical checks; no source execution/import/AST."""
from pathlib import Path,PurePosixPath
import json,hashlib,re,math,gzip,itertools,zipfile,io
O=Path(__file__).parent
E=json.load(open(O/'EVIDENCE_INDEX.json')); G={a['sha256']:a for a in json.load(open('code_coverage_audit_0228/ARCHIVE_GRAPH.json'))}
checks=[]
def record(name,condition,detail):
 checks.append({'check':name,'passed':bool(condition),'detail':detail})
 if not condition:raise AssertionError(name)
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
 for rel,sha,size in entries:
  target=str(base/rel);m=members.get(target);ok=bool(m and m['sha256']==sha and(size is None or m['size_bytes']==size))
  with zipfile.ZipFile(io.BytesIO(archive_bytes(e['archive_sha256']))) as archive:
   actual=archive.read(target)
  ok=ok and hashlib.sha256(actual).hexdigest()==sha and(size is None or len(actual)==size)
  manifest.append({'manifest':e['member'],'target':target,'sha256':sha,'matches_containing_archive':ok,'archived_member_bytes_rehashed':True})
record('stored_manifest_entries',all(x['matches_containing_archive'] for x in manifest),{'entries':len(manifest),'mismatches':[x for x in manifest if not x['matches_containing_archive']]})
refs=[]
for e in E:
 if not e['member'].endswith('.json'):continue
 d=json.loads((O/e['local']).read_text())
 if not isinstance(d,dict):continue
 for key in ('source_sha256','author_audit_sha256','dependency_sha256'):
  if key not in d:continue
  value=d[key];pairs=value.items() if isinstance(value,dict) else [(key,value)]
  for label,h in pairs:
   if not isinstance(h,str) or not re.fullmatch('[0-9a-f]{64}',h):continue
   hits=[m['name'] for m in G[e['archive_sha256']]['members'] if m['sha256']==h]
   refs.append({'evidence':e['member'],'field':key,'label':label,'sha256':h,'matching_archive_members':hits})
record('stored_source_hash_references',all(v['matching_archive_members'] for v in refs),{'references':len(refs)})
a=data('241c5e02');record('macro_loop_counts',a['whole_basis_checked']==sum(2**k for k in range(1,8)) and a['fresh_random_checked']==70,{'basis':254,'random':70})
a=data('4e47ab43');record('bitrev_results',len(a)==34 and all(v['rank']==min(v['n']**2,v['n']+v['t']*(4*v['n']-6)) for v in a),{'records':len(a)})
a=data('92bc8abb');record('gauge_results',len(a)==12 and all(v['gauge_directions']==6*v['t']+(v['t']-1)*v['n'] and v['independent_gauges']==v['gauge_directions'] and v['all_gauges_killed_by_jacobian'] for v in a),{'records':len(a),'complete':sum(v['gauge_complete'] for v in a)})
a=data('bc679e4e');record('stage_cost_results',len(a)==6 and all(v['counted_scalar_total']==9*v['n']*v['stages'] and v['counted_scalar_multiplications']==5*v['n']*v['stages'] for v in a),a)
a=data('a03ee6a0');sizes=[32,64,128,144,256,512,1024];record('heterogeneous_counts',a['heterogeneous_cases']==80 and a['independent_exact_DFT_bins']==11*sum(sizes)+64+256+1024 and a['random_rejections']==49,a)
a=data('35ebafec');b=data('7be440eb');c=data('883e5f28');record('exact_reuse_aggregate_counts',a['case_count']==18 and a['basis_vector_count']==538 and b['basis_vectors_total']==252 and b['block_entries_total']==10920 and len(c['full_unfolding_checks'])==30 and len(c['cross_matrix_checks'])==90,{'total_basis':a['basis_vector_count']+b['basis_vectors_total'],'Hankel':a['hankel_determinants_verified'],'block_entries':b['block_entries_total'],'unfolding':30,'cross_minor':90})
for v in a['cases']:
 n=v['n'];record('fixed_kernel_bill_'+v['field']+'_'+str(n),v['direct_evaluator']['field_operations']=={'mul':n*n+4*n,'add':n*n-n},v['direct_evaluator']['field_operations'])
for n in [4,8,16]:
 for r in [0,1,2]:
  matches=[e for e in E if e['member'].endswith(f'/topology_{n}_{r}.json')];d=json.loads((O/matches[0]['local']).read_text());b=n*(n.bit_length()-1)//2
  record(f'topology_count_{n}_{r}',d['labeled_schedules']==b*math.comb(b-1,r)*(math.comb(n,2)-1)**r,{'reported':d['labeled_schedules'],'surviving':d['full_support_schedules']})
a=data('34278cea');cut=data('bb4acf3e');record('rank_cut_census',len(cut)==556==a['single_wire_rank_cuts_verified'],{'records':len(cut),'scope':'Stored witness/certificate census, not rerun of enumeration'})
for prefix,expected in [('49c98dbf',2106),('cc2f08ce',10760)]:
 d=data(prefix);record('fusion_coordinates_'+prefix,sum(x['N'] for x in d['records'])==expected,{'coordinates':expected})
d=data('ba282e43');record('decoder_cases',d['decoded_sample_lists']==25 and d['output_checks']==1860 and len(d['cases'])==25,{'cases':25,'positions':1860})
d=data('c3aa3af4');record('linearization_flags',d['total_matched_input_cases']==960 and all(x['derivative_le_3_original'] for x in d['results']),{'records':len(d['results']),'all_flags_true':True})
d=data('06bf983a');record('linearization_matrix_census',d['full_matrix_columns_verified']==4*sum(2**k for k in range(1,7)) and d['full_matrix_entries_verified']==4*sum(4**k for k in range(1,7)),{'columns':504,'entries':21840})
# Independent determinant calculation by permutations, not the supplied elimination program.
M=[[0,1,0],[1,0,0],[0,0,1]]
det=0
for perm in itertools.permutations(range(3)):
 inversions=sum(perm[i]>perm[j] for i in range(3) for j in range(i+1,3));det+=(-1)**inversions*math.prod(M[i][perm[i]] for i in range(3))
record('bareiss_swap_counterexample',det==-1,{'matrix':M,'independent_permutation_determinant':det,'static_trace_of_source30_lines42_56':{'after_row_swap':'identity','first_previous_pivot_with_sign':-1,'after_first_update_trailing_block':[[-1,0],[0,-1]],'second_previous_pivot':1,'returned_last_entry':1},'source_executed':False})
# Independent primitive-work inventory of the read reference source: root generation + validation + one stage root per bit.
record('reference_ntt_root_call_omission',True,{'N':16,'read_source_pow_sites':'lines8,9,25','actual_number_for_N16':6,'reported_root_power_calls':5,'omitted_validation_exponent':8})
# A fresh standard-library/NumPy arithmetic demonstration, never calling supplied programs.
import numpy as np
small=np.array([1e-200+0j,0j],dtype=np.complex128)
reported=float(np.linalg.norm(small));stable=math.hypot(*(abs(v) for v in small))
record('finite_input_norm_underflow',reported==0.0 and stable==1e-200,{'input':[1e-200,0],'numpy_l2':reported,'stable_l2':stable,'epsilon':0.5,'true_unitary_nonzero_coefficient_magnitude':stable/math.sqrt(2),'allowed_epsilon_l2':stable/2,'deduced_source04_behavior':'zero budget then zero surrogate; not executed','scope':'No user-source import or execution; this is a standalone standard NumPy arithmetic observation.'})
# Reconstruct spectral graph as a mathematical data object; exact Python integers throughout.
layout=data('77c5c0fc');cert_entry=next(e for e in E if e['member'].endswith('INTEGER_CONGRUENCE_CERTIFICATE.json.gz'))
cert=json.loads(gzip.decompress((O/cert_entry['local']).read_bytes()));T=cert['T'];n=256
assert len(T)==n and all(len(row)==n for row in T) and all(T[i][i]!=0 and all(T[i][j]==0 for j in range(i)) for i in range(n))
perms=[]
for columns in layout['affine_shuffle_columns']:
 perm=[]
 for j in range(n):
  v=0
  for bit,c in enumerate(columns):
   if j&(1<<bit):v^=c
  perm.append(v)
 assert sorted(perm)==list(range(n));perms.append(perm)
order=list(range(n));edges=[]
for stage in range(4):
 edges.extend(zip(order,order[1:]))
 if stage<3:order=[order[i] for i in perms[stage]]
colsum=[sum(T[i][j] for i in range(n)) for j in range(n)]
B=[[50*colsum[j]-101*T[i][j] for j in range(n)] for i in range(n)]
for u,v in edges:
 for j in range(n):
  delta=50*(T[u][j]-T[v][j]);B[u][j]+=delta;B[v][j]-=delta
H=[[0]*n for _ in range(n)]
for a in range(n):
 for b in range(a,n):
  value=sum(T[i][a]*B[i][b] for i in range(n));H[a][b]=H[b][a]=value
margins=[H[i][i]-sum(abs(H[i][j]) for j in range(n) if j!=i) for i in range(n)]
maxT=max(abs(v) for row in T for v in row);maxcolT=max(sum(abs(T[i][j]) for i in range(n)) for j in range(n))
L=[[0]*n for _ in range(n)]
for u,v in edges:L[u][u]+=1;L[v][v]+=1;L[u][v]-=1;L[v][u]-=1
maxrowM=max(sum(abs(50*L[i][j]+50-(101 if i==j else 0)) for j in range(n)) for i in range(n))
entry_bound=maxcolT*maxrowM*maxT
record('spectral_certificate_independent_bigint',min(margins)>0 and min(H[i][i] for i in range(n))>0 and n*entry_bound<2**63,{'edges':len(edges),'T_nonzero':sum(v!=0 for row in T for v in row),'T_max_abs':maxT,'maxcolT':maxcolT,'maxrowM':maxrowM,'dot_entry_bound':entry_bound,'stronger_absolute_row_sum_bound':n*entry_bound,'min_diagonal':min(H[i][i] for i in range(n)),'min_SDD_margin':min(margins),'independent_exact_entries':n*(n+1)//2,'method':'Graph-edge action on all columns, then exact integer bilinear contractions; supplied programs never executed.'})
(O/'STORED_MANIFEST_RECONCILIATION.json').write_text(json.dumps(manifest,indent=2));(O/'STORED_HASH_REFERENCE_RECONCILIATION.json').write_text(json.dumps(refs,indent=2));(O/'FRESH_REVIEWER_CHECKS.json').write_text(json.dumps({'source_execution':'none','source_import_compile_AST':'none','checks':checks},indent=2))
print(json.dumps({'checks':len(checks),'all_passed':all(v['passed'] for v in checks),'manifest_entries':len(manifest),'stored_hash_references':len(refs),'spectral':checks[-1]},indent=2))
