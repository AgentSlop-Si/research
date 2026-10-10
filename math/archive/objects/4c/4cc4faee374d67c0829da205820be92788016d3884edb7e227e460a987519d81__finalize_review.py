"""Fresh reviewer packaging; originals and central registry are read-only."""
from pathlib import Path
import json,hashlib,shutil,collections,zipfile,io
O=Path(__file__).parent;ROOT=Path('fft_research_master_20261009')
def read(name):return json.loads((O/name).read_text())
def write(name,data):(O/name).write_text(json.dumps(data,indent=2)+'\n')
shutil.copy('code_coverage_audit_0228/CODE_COVERAGE_INVENTORY.json',O/'INVENTORY_SNAPSHOT.json')
shutil.copy('post_v22_review_registry_0308/ADDITIVE_CODE_COVERAGE.json',O/'REGISTRY_END_SNAPSHOT.json')
rows=read('ASSIGNED_SOURCES.json');P=read('PROVENANCE.json');G={a['sha256']:a for a in read('ARCHIVE_GRAPH_SNAPSHOT.json')};E=read('EVIDENCE_INDEX.json');I=read('INVENTORY_SNAPSHOT.json');R0=read('REGISTRY_START_SNAPSHOT.json');R1=read('REGISTRY_END_SNAPSHOT.json')
covered={r['sha256'] for r in R1['rows']}|{r['sha256'] for r in I if r.get('static_inspection_complete')}
notes={int(a):(b,c) for a,b,c in (line.split('\t',2) for line in (O/'PER_SOURCE_NOTES.tsv').read_text().splitlines())};assert len(notes)==len(rows)==70
# Supplement generic hash refs with global archive membership and serialized matrix resolution.
refs=read('STORED_HASH_REFERENCE_RECONCILIATION.json');global_members=collections.defaultdict(list)
for ah,a in G.items():
 for m in a['members']:global_members[m['sha256']].append({'archive_sha256':ah,'member':m['name']})
for r in refs:
 if r['matching_archive_members']:r['resolution']='matching_member_in_containing_archive'
 elif 'full_state_matrix_sha256' in r['field']:r['resolution']='serialized_matrix_hash_independently_verified_in_FRESH_REVIEWER_CHECKS'
 elif r['referenced_sha256'] in G:r['resolution']='archive_hash_in_global_graph';r['global_archive_path']=G[r['referenced_sha256']]['first_observed_at']
 elif r['referenced_sha256'] in global_members:r['resolution']='matching_member_in_other_archive_metadata';r['global_candidates']=global_members[r['referenced_sha256']]
 else:r['resolution']='not_reconciled_to_archived_file_bytes; may be historical/external or serialized logical-content digest'
write('STORED_HASH_REFERENCE_RECONCILIATION.json',refs)
D=read('DEPENDENCY_RECONCILIATION.json')
for r in D['imports']:
 if r['kind']=='unresolved_local_or_external' and r['module']=='window_gate':
  ah='5e7b63e9028941805d30247a53b76e76f2c44a4b7daea9115946a2f385d6fcf5';a=G[ah];parts=a['first_observed_at'].split('!');raw=(ROOT/parts[0]).read_bytes()
  for p in parts[1:]:
   with zipfile.ZipFile(io.BytesIO(raw)) as z:raw=z.read(p)
  assert hashlib.sha256(raw).hexdigest()==ah
  member=next(m for m in a['members'] if m['name']=='fft_window_rank_gate_2026-10-09/window_gate.py')
  with zipfile.ZipFile(io.BytesIO(raw)) as z:b=z.read(z.infolist()[member['member_index']])
  assert hashlib.sha256(b).hexdigest()==member['sha256']
  r.update(kind='nested_predecessor_exact_hash_located_runtime_layout_unverified',candidates=[{'archive_sha256':ah,'archive_path':a['first_observed_at'],'member':member['name'],'sha256':member['sha256'],'byte_identity_verified':True,'new_full_source_read_claimed':False}],note='Exact predecessor dependency exists in the nested archive; source32 main expects an extracted external sibling directory. No runtime path resolution was executed.')
write('DEPENDENCY_RECONCILIATION.json',D)
reviews=[]
for r,p in zip(rows,P):
 b=(O/'sources'/r['sha256']).read_bytes();assert len(b)==r['size_bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'];assert Path(r['local_content']).read_bytes()==b
 role,finding=notes[r['index']]
 suffix={9:' Fresh data check independently matches all ten serialized full-state matrix hashes to the stored summary.',47:' Fresh reviewer reconstruction supplies an exact rational N=12,M=3 Rayleigh witness 1196/3033>1/4 and Q²!=Q/4, removing reliance on numerical eigenvalues for that counterexample.',58:' Fresh reviewer reconstruction validates all archived conjugate-pair supports and independently reproduces nonzero determinants at N=8,16,32; the malformed-input guard defect does not invalidate those checked artifacts.',59:' Fresh reviewer checks all 3,136 3x5 F8 submatrices have rank 3, independently establishing the recorded cut-3 obstruction.',64:' Fresh reviewer direct inverses (rather than the source geometric-series implementation) reconstruct saved A/B and reproduce determinant 55687 modulo 65537.',65:' Fresh reviewer validates within-support uniqueness/range for every archived N=8,16,32 witness and independently reproduces all three determinant residues.',32:' Exact window_gate bytes were located and rehashed in nested predecessor archive 5e7b63e9…; its external extracted runtime layout remains unverified.'}.get(r['index'],'')
 reviews.append({'review_id':f"S{r['index']:02}",'sha256':r['sha256'],'representative_path':r['representative_path'],'bytes':r['size_bytes'],'lines':r['line_count'],'read_scope':{'first_line':1,'last_line':r['line_count'],'full_static_inspection':True,'source_executed':False,'source_imported':False,'source_compiled':False,'source_AST_parsed':False},'role':role,'findings':finding+suffix,'source_snapshot':'sources/'+r['sha256'],'numbered_snapshot':f"line_numbered/{r['index']:02}.txt",'provenance':p,'origin_class':r['origin_class'],'origin_basis':r['origin_basis'],'dependency_reconciliation':'DEPENDENCY_RECONCILIATION.json','stored_evidence_scope':'Historical related files collected by archive provenance. Manifests rehashed; targeted counters/certificates independently reconciled in FRESH_REVIEWER_CHECKS.json. No general claim every historical assertion/proof or runtime dependency is verified.'})
write('SOURCE_REVIEWS.json',reviews)
md=['# Full static source reviews','', 'All 70 exact sources were read first to last. Source execution/import/compile/AST: none. Correctness qualifications and novelty are separate.','']
for r in reviews:md += [f"## {r['review_id']}: {r['representative_path']}",'',f"SHA-256: {r['sha256']}",f"Full read: lines 1–{r['lines']}; {r['bytes']} bytes.",f"Role: {r['role']}",'',r['findings'],'',f"Archive: {r['provenance']['archive_sha256']} member {r['provenance']['member']}",'']
(O/'SOURCE_REVIEWS.md').write_text('\n'.join(md))
reviewhash=hashlib.sha256((O/'SOURCE_REVIEWS.json').read_bytes()).hexdigest();covered_rows=[r for r in rows if r['sha256'] in covered];new=len(rows)-len(covered_rows)
write('DEDUPLICATION.json',{'registry_start_full_static_reads':R0['current_full_static_reads'],'registry_end_full_static_reads':R1['current_full_static_reads'],'assigned_hashes':len(rows),'assigned_already_covered_at_end':[r['sha256'] for r in covered_rows],'new_coverage_credit':new,'central_registry_modified':False})
write('COVERAGE.json',{'package':O.name,'completed_utc':'2026-10-10T05:26:51Z','assigned_batches':['batch_02.json'],'assigned_batch_hashes':70,'fully_read_hashes_this_review':70,'new_full_read_hashes':new,'new_coverage_credit':new,'previously_covered_hashes':len(covered_rows),'total_source_bytes_read':sum(r['bytes'] for r in reviews),'total_source_lines_read':sum(r['lines'] for r in reviews),'all_assigned_new_source_reads_complete':True,'all_research_material_checks_finished':False,'dependency_closure_complete':False,'source_execution':'none','source_import_compilation_syntax_parse':'none','scope_note':'Full first-to-last inert reading of all assigned hashes. Stored PASS/timings are historical. Only fresh reviewer metadata and independent arithmetic ran. No central registry changes. No global completion or novelty certification.','rows':[{'review_id':r['review_id'],'sha256':r['sha256'],'representative_path':r['representative_path'],'batch':'batch_02.json','bytes':r['bytes'],'lines':r['lines'],'full_static_inspection':True,'static_inspection_complete':True,'full_source_read':True,'line_ranges':[[1,r['lines']]],'source_executed_in_review':False,'evidence_file':'SOURCE_REVIEWS.json','evidence_sha256':reviewhash,'snapshot':r['source_snapshot'],'new_coverage_credit':r['sha256'] not in covered} for r in reviews]})
print(json.dumps({'sources':len(reviews),'new_coverage':new,'existing':len(covered_rows),'registry_end':R1['current_full_static_reads'],'reference_resolution':dict(collections.Counter(r['resolution'] for r in refs)),'dependency_kinds':dict(collections.Counter(r['kind'] for r in D['imports']))},indent=2))
