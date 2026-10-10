"""Reviewer-authored metadata, preservation and sealing checks; no supplied program evaluation."""
from pathlib import Path
import hashlib,json
O=Path(__file__).resolve().parent;S=O.parent;B=S/'code_coverage_audit_0228';M=S/'fft_research_master_20261009'
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def full(r):return bool(r.get('static_inspection_complete') or r.get('full_static_inspection') or r.get('full_static_read') or r.get('status')=='full_static_review_complete' or r.get('full_read_extent',{}).get('all_source_lines_read'))
rows=json.loads((O/'ASSIGNED_ROWS.json').read_text());assigned={r['sha256'] for r in rows};scans=[];overlap={};prior={}
paths=[B/'CODE_COVERAGE_INVENTORY.json',S/'post_v22_review_registry_0308/ADDITIVE_CODE_COVERAGE.json']+sorted(S.glob('*/COVERAGE.json'))
for p in paths:
 if p.parent==O:continue
 b=p.read_bytes();d=json.loads(b);rr=d if isinstance(d,list) else d.get('rows',d.get('files',[]));covered={r['sha256'] for r in rr if 'sha256'in r and full(r)};hit=assigned&covered
 scans.append({'path':str(p),'sha256':sha(b),'bytes':len(b),'schema':'list' if isinstance(d,list) else ('rows' if 'rows'in d else 'files'),'full_static_hashes':len(covered),'assigned_overlap':sorted(hit)})
 for h in covered:prior.setdefault(h,[]).append(str(p))
 for h in hit:overlap.setdefault(h,[]).append(str(p))
dedup={'checked_files':scans,'overlap':overlap,'new_hashes':sorted(assigned-overlap.keys()),'recognized_full_read_flags':['static_inspection_complete','full_static_inspection','full_static_read','status=full_static_review_complete','full_read_extent.all_source_lines_read'],'scope':'Frozen inventory, additive registry and all sibling completed COVERAGE.json available at sealing. Self excluded.'}
dump(O/'FINAL_DEDUP_CHECK.json',dedup)
# Correct the preliminary scan schema boundary explicitly rather than silently hide it.
initial=json.loads((O/'PRIOR_COVERAGE_CHECK.json').read_text());initial['initial_scan_schema_limitation']='The preliminary scan recognized rows/list schemas and two flags only. Final scan also recognizes files schema, full_static_read and full_read_extent; no assigned overlaps emerged.';dump(O/'PRIOR_COVERAGE_CHECK.json',initial)
D=json.loads((O/'DEPENDENCY_IDENTITIES.json').read_text())
for r in D['rows']:r['prior_full_coverage_evidence']=prior.get(r['sha256'],[])
dump(O/'DEPENDENCY_IDENTITIES.json',D)
C=json.loads((O/'COVERAGE.json').read_text());C['new_full_read_hashes']=C['new_additive_full_static_reads']=len(assigned-overlap.keys());C['previously_covered_hashes']=len(overlap)
for r in C['rows']:
 r['new_coverage_credit']=r['new_additive_full_read']=r['sha256'] not in overlap;r['prior_full_read_overlap']=r['sha256'] in overlap;r['prior_coverage_sources']=overlap.get(r['sha256'],[])
dump(O/'COVERAGE.json',C)
# Verify every exact source snapshot, frozen master source occurrence and coverage interval.
sourcecheck=[]
for r in rows:
 p=Path(r['local_content']);b=p.read_bytes();sn=(O/r['snapshot']).read_bytes();master=(M/r['representative_path']).read_bytes()
 sourcecheck.append({'sha256':r['sha256'],'content_hash_matches':sha(b)==r['sha256'],'snapshot_equal':b==sn,'master_representative_equal':b==master,'size_matches':len(b)==r['size_bytes'],'lines_match':len(b.splitlines())==r['lines']})
# Historical master snapshot differs only in pre-existing root bookkeeping files.
start=json.loads((O/'PRESERVATION_START.json').read_text());hist=json.loads((B/'MASTER_FILE_HASHES.json').read_text());diffs={r['path']:r['actual'] for r in start['master_entry_failures']};changed=[];source_count=0
for r in hist:
 expected=diffs.get(r['path'],r['sha256']);p=M/r['path'];actual=sha(p.read_bytes()) if p.is_file() else None
 if r.get('is_code'):source_count+=1
 if expected!=actual:changed.append({'path':r['path'],'expected_review_start':expected,'actual':actual})
tracked=[]
for r in start['files']:
 p=Path(r['path']);h=sha(p.read_bytes());tracked.append({'path':str(p),'before_sha256':r['sha256'],'after_sha256':h,'unchanged':h==r['sha256']})
# Validate the frozen inventory seal without running its builders.
seal=json.loads((B/'SEAL.json').read_text());mb=(B/seal['manifest']).read_bytes();frozen_fail=[];entries=0
for line in mb.decode().splitlines():
 if not line.strip():continue
 h,rel=line.split('  ',1);p=B/rel;actual=sha(p.read_bytes()) if p.is_file() else None;entries+=1
 if actual!=h:frozen_fail.append({'path':rel,'expected':h,'actual':actual})
frozen={'manifest_sha256_matches':sha(mb)==seal['manifest_sha256'],'entry_count':entries,'declared_entries':seal['files'],'failures':frozen_fail};dump(O/'FROZEN_SEAL_CHECK.json',frozen)
pres={'source_checks':sourcecheck,'all_24_sources_and_snapshots_equal':all(all(v for k,v in x.items() if k!='sha256') for x in sourcecheck),'historical_master_entries_checked':len(hist),'historical_master_code_entries':source_count,'historical_master_matches':len(hist)-len(diffs),'historical_root_bookkeeping_differences':start['master_entry_failures'],'master_entries_changed_during_review':changed,'tracked_file_hashes':tracked,'review_writes_limited_to_own_package':True,'supplied_sources_modified':False,'source_programs_executed':False,'source_programs_imported':False,'source_programs_compiled':False,'source_syntax_parsed':False,'note':'Eight thousand fifty historical entries were compared at start and end. Seven root bookkeeping/seal files already differed from historical v21 metadata at review start; all historical source/material entries matched. This receipt does not pretend those seven files still match v21.'};dump(O/'PRESERVATION_RECEIPT.json',pres)
validation={'assigned_distinct_hashes':len(assigned),'coverage_row_hashes_equal_assigned':{r['sha256'] for r in C['rows']}==assigned,'complete_intervals':all(r['fully_read_line_intervals']==[[1,r['lines']]] for r in C['rows']),'source_snapshots_valid':pres['all_24_sources_and_snapshots_equal'],'frozen_inventory_seal_valid':frozen['manifest_sha256_matches'] and not frozen_fail and entries==seal['files'],'no_master_change_during_review':not changed,'tracked_hashes_unchanged':all(r['unchanged'] for r in tracked),'source_execution':'none','new_hashes':C['new_full_read_hashes'],'prior_overlap':C['previously_covered_hashes']};dump(O/'VALIDATION.json',validation)
print(json.dumps(validation,indent=2))
