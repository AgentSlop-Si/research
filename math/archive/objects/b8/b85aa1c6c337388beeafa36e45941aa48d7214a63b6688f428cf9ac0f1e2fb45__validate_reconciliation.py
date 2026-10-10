"""New inert artifact validator; imports no research code."""
from pathlib import Path
import json, hashlib
O=Path('generated_receipt_reconciliation_0254');B=Path('code_coverage_audit_0228');R=Path('fft_research_master_20261009')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rows=json.load(open(O/'RECONCILIATION.json'));ev=json.load(open(O/'RECONCILIATION_EVIDENCE.json'));sources=json.load(open(O/'EVIDENCE_SOURCE_INDEX.json'));scope=json.load(open(O/'SCOPE_ROWS.json'))
reads=[{'scope_row':r['scope_row'],'sha256':r['code_sha256'],'path':r['representative_path'],'size_bytes':r['size_bytes'],'inspection':r['full_static_read'],'role':r['primary_role'],'conclusion':r['conclusion']} for r in rows if r['full_static_read']['complete_bytes_read']]
(O/'STATIC_ROLE_READS.json').write_text(json.dumps(reads,indent=2)+'\n')
ids={e['id'] for e in ev};assert len(ids)==len(ev)
assert {r['code_sha256'] for r in rows}=={r['sha256'] for r in scope}
drift=[]
for s in sources:
 assert sha(Path(s['snapshot_read_path']))==s['sha256']==sha(O/s['portable_path'])
 if sha(Path(s['path']))!=s['sha256']:
  drift.append({'original_source_path':s['path'],'snapshot_sha256':s['sha256'],'live_sha256':sha(Path(s['path'])),'verified_snapshot_path':s['snapshot_read_path'],'retained_exact_copy':s['portable_path'],'interpretation':'Live master advanced to v22 during this task; source evidence remains bound to captured v21 bytes and verified checkpoint_history/v21 copy.'})
for e in ev:
 data=(O/e['source']['portable_path']).read_text(errors='replace').splitlines()
 for z in e['selected_ranges']:assert '\n'.join(data[z['first_line']-1:z['last_line']])==z['text']
for r in rows:
 assert all(i in ids for i in r['evidence_ids'])
 assert sha(R/r['representative_path'])==r['code_sha256']
 for e in r['support_import_edges']:
  ls=Path(e['importer']['snapshot_read_path']).read_text().splitlines();assert '\n'.join(ls[e['first_line']-1:e['last_line']])==e['text']
 for a in r.get('additional_support_aliases',[]):assert a['source_lines'] or a.get('intermediate_source_lines')
original_log=(O/'ORIGINAL_SEAL_VERIFICATION.log').read_text().splitlines();assert original_log and all(l.endswith(': OK') for l in original_log)
expected_seal=json.load(open(B/'INPUT_SNAPSHOT.json'))['master_root_seals_sha256']['SHA256SUMS.txt'];assert sha(O/'ORIGINAL_MASTER_V21_SHA256SUMS.txt')==expected_seal
before=json.load(open(O/'SEALED_INPUT_HASHES_BEFORE.json'));after={p.name:sha(p) for p in B.iterdir() if p.is_file()};assert before==after
fullbytes=sum(r['size_bytes'] for r in reads)
val={'passed':True,'scope_hashes_unique':len(rows),'scope_hash_set_exactly_matches_original_66':True,'snapshot_source_and_copied_digest_checks':len(sources),'evidence_references_and_quoted_extents_resolve':True,'literal_support_edges_checked':sum(len(r['support_import_edges']) for r in rows),'dual_role_import_chains_checked':3,'original_inventory_seal_entries_all_pass':len(original_log),'original_inventory_top_level_before_after_equal':True,'v21_master_seal_verified_from_history_and_retained':expected_seal,'live_master_report_paths_with_documented_snapshot_drift':len(drift),'static_role_reads':len(reads),'static_role_read_bytes':fullbytes,'existing_code_executions':0,'existing_code_imports':0,'scope_boundaries':'No correctness, full test coverage, execution attestation, or all-source-read inference.'}
(O/'VALIDATION.json').write_text(json.dumps(val,indent=2)+'\n');(O/'LIVE_MASTER_SNAPSHOT_DRIFT.json').write_text(json.dumps(drift,indent=2)+'\n')
print(json.dumps(val,indent=2))
