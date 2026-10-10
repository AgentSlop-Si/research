"""Reviewer packaging and integrity checks only. Does not interpret source code."""
from pathlib import Path
import json,hashlib,shutil
O=Path(__file__).parent;NOW='2026-10-10T05:21:20Z';rows=json.load(open(O/'ASSIGNED_SOURCES.json'));provs=json.load(open(O/'PROVENANCE.json'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,obj):(O/name).write_text(json.dumps(obj,indent=2)+'\n')
notes={}
for line in (O/'PER_SOURCE_NOTES.tsv').read_text().splitlines():
 i,role,find=line.split('\t',2);notes[int(i)]=(role,find)
assert set(notes)==set(range(46))
stored={int(i):txt for i,txt in [line.split('\t',1) for line in (O/'STORED_RESULT_NOTES.tsv').read_text().splitlines()]}
start=json.load(open(O/'REGISTRY_START_SNAPSHOT.json'));shutil.copyfile('post_v22_review_registry_0308/ADDITIVE_CODE_COVERAGE.json',O/'REGISTRY_END_SNAPSHOT.json');end=json.load(open(O/'REGISTRY_END_SNAPSHOT.json'))
inv=json.load(open('code_coverage_audit_0228/CODE_COVERAGE_INVENTORY.json'));covered={r['sha256'] for r in inv if r.get('static_inspection_complete')}|{r['sha256'] for r in end['rows']};existing=sorted({r['sha256'] for r in rows}&covered)
write('DEDUPLICATION.json',{'registry_start_count':start['current_full_static_reads'],'registry_end_count':end['current_full_static_reads'],'assigned_unique_hashes':len(rows),'already_accepted_assigned_hashes':existing,'new_coverage_credit':len(rows)-len(existing),'central_registry_modified':False})
reviews=[];readlog=[]
for i,(r,pv) in enumerate(zip(rows,provs)):
 b=(O/'sources'/r['sha256']).read_bytes();assert len(b)==r['size_bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'];assert len(b.decode().splitlines())==r['lines']
 rr=[[1,r['lines']]] if i not in (13,40) else ([[1,420],[421,821]] if i==13 else [[1,340],[341,606]])
 evidence=sorted(set(pv.get('stored_evidence_hashes',[])+[h for c in pv.get('verified_standalone_contexts',[]) for h in c['stored_evidence_hashes']]))
 ps={k:pv[k] for k in ('archive_sha256','archive_first_observed_at','member_index','member','byte_identity_verified') if k in pv};ps['standalone_verified_paths']=[c['source_path'] for c in pv['verified_standalone_contexts']];ps['full_context_file']='PROVENANCE.json';ps['index']=i
 rev={'review_id':f'S{i:02}','sha256':r['sha256'],'representative_path':r['representative_path'],'bytes':r['size_bytes'],'lines':r['lines'],'read_scope':{'first_line':1,'last_line':r['lines'],'full_static_inspection':True,'source_executed':False,'source_imported':False,'source_compiled':False,'source_AST_parsed':False},'role':notes[i][0],'findings':notes[i][1],'stored_result_reconciliation':stored.get(i,'No standalone result producer in this source. Associated archive evidence is historical, not a fresh correctness/execution certificate.'),'source_snapshot':'sources/'+r['sha256'],'numbered_snapshot':f'line_numbered/{i:02}.txt','provenance':ps,'origin_class':r['origin_class'],'origin_basis':r['origin_basis'],'related_evidence_hashes':evidence,'claim_boundaries':{'full_source_read':True,'supplied_execution_in_current_review':False,'general_correctness_proved':False,'novelty_established':False,'global_FFT_improvement_established':False}}
 reviews.append(rev);readlog.append({'review_id':rev['review_id'],'sha256':r['sha256'],'displayed_and_reviewed_ranges':rr,'complete_first_to_last':True,'source_bytes':len(b)})
write('SOURCE_REVIEWS.json',reviews);write('READ_LOG.json',readlog)
md=['# Per-source inert inspection','', 'All 46 exact hashes were read from first to last; no supplied source was run, imported, compiled or AST-parsed.','']
for r in reviews:md += [f'## {r["review_id"]} — {r["representative_path"]}',f'- SHA-256: `{r["sha256"]}`',f'- Scope: lines 1–{r["lines"]}, {r["bytes"]} bytes; {r["role"]}',r['findings'],'',r['stored_result_reconciliation'],'']
(O/'SOURCE_REVIEWS.md').write_text('\n'.join(md))
evidence_sha=sha(O/'SOURCE_REVIEWS.json');cov=[]
for r in reviews:cov.append({'review_id':r['review_id'],'sha256':r['sha256'],'representative_path':r['representative_path'],'batch':'batch_01.json','bytes':r['bytes'],'lines':r['lines'],'full_static_inspection':True,'static_inspection_complete':True,'full_source_read':True,'line_ranges':[[1,r['lines']]],'source_executed_in_review':False,'evidence_file':'SOURCE_REVIEWS.json','evidence_sha256':evidence_sha,'snapshot':r['source_snapshot'],'new_coverage_credit':r['sha256'] not in existing})
write('COVERAGE.json',{'package':O.name,'completed_utc':NOW,'assigned_batches':['batch_01.json'],'assigned_batch_hashes':46,'fully_read_hashes_this_review':46,'new_full_read_hashes':46-len(existing),'new_coverage_credit':46-len(existing),'previously_covered_hashes':len(existing),'total_source_bytes_read':sum(r['bytes'] for r in reviews),'total_source_lines_read':sum(r['lines'] for r in reviews),'all_assigned_new_source_reads_complete':True,'all_research_material_checks_finished':False,'dependency_closure_complete':False,'source_execution':'none','source_import_compilation_syntax_parse':'none','scope_note':'Full first-to-last inert inspection of 46 assigned exact hashes; historical result/manifest/dependency reconciliation and51 new reviewer arithmetic checks. No supplied execution and no central registry edits. No global FFT improvement or novelty conclusion.','rows':cov})
write('ASSIGNMENT.json',{'batch_directory':'remaining_source_queue_0502','batch_names':['batch_01.json'],'source_hash_count':46,'source_bytes':343250,'source_lines':8172})
print('Packaged',len(reviews),'reviews, new credit',46-len(existing),'registry at',end['current_full_static_reads'])
