from pathlib import Path
import hashlib,json,shutil,zipfile
B=Path('fft_research_master_20261009')
Z=B.with_suffix('.zip')
S=Path('materials_1954')
W=Path('v10_build')
P=W/'fft_research_master_20261009'
expected='cfa3c36da73eb7b494e0949f982a20a4f0c3039bc8b778b56468237731f01bc5'
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert Z.stat().st_size==44446702 and h(Z)==expected
with zipfile.ZipFile(Z) as z:
 assert z.testzip() is None
 assert len([x for x in z.infolist() if not x.is_dir()])==3726
assert (B/'SHA256SUMS').read_bytes()==(B/'SHA256SUMS.txt').read_bytes()
verified=0
for line in (B/'SHA256SUMS').read_text().splitlines():
 digest,name=line.split('  ',1)
 assert h(B/name)==digest, name
 verified+=1
assert not P.exists()
shutil.copytree(B,P)
roots=[]
for f in sorted(B.iterdir()):
 if f.is_file():
  shutil.copy2(f,P/'checkpoint_history'/('v9_'+f.name))
  roots.append({'path':f.name,'bytes':f.stat().st_size,'sha256':h(f)})
A=P/'additions'/'1954'; A.mkdir()
for dirname in ['source_triage','originals','extracted','audits']:(A/dirname).mkdir()
static=['SOURCE_TRIAGE_AND_FUSION.md','STATIC_VALIDATION.json','TRIAGE_SUMMARY.json','content_inventory.json','COMPARISON_SCOPE.json','inspect_archives.py','static_validation.py','compare_recursive.py']
for name in static:shutil.copy2(S/name,A/'source_triage'/name)
shutil.copy2(S/'SHA256SUMS',A/'source_triage'/'original_snapshot_SHA256SUMS')
provenance=json.loads((S/'library_provenance.json').read_text()); inventory=json.loads((S/'content_inventory.json').read_text())
byname={x['archive']:x for x in inventory}
refs={
 'fft_sparse_defect_green_gate_2026-10-10(1).zip':('additions/1930_static/source_archives/fft_sparse_defect_green_gate_2026-10-10.zip','additions/1930_sparse/'),
 'fft_green_research_phase26_2026-10-10(1).zip':('additions/1930_static/source_archives/fft_green_research_phase26_2026-10-10.zip','additions/1930_phase26/'),
 'fft_hero1_mixedradix_v13_20261010.zip':('additions/1930_static/source_archives/fft_hero1_mixedradix_v13_20261010.zip','additions/1930_v13/'),
 'fft_hero0_phase2_composite_green_2026-10-09(1).zip':('additions/1916/original_source.zip','additions/1916/'),
}
records=[]
for x in provenance:
 name=x['file_name']; src=S/'originals'/name; digest=h(src); assert digest==byname[name]['sha256']
 r={'received_utc':'2026-10-09T19:54:00Z','source_origin':'direct user attachment','filename':name,'library_file_id':x['library_file_id'],'library_version_number':x['current_version_number'],'bytes':src.stat().st_size,'sha256':digest}
 if name in refs:
  path,audit=refs[name]; assert h(P/path)==digest
  r.update({'archive_storage':'byte-identical existing original preserved once in master','master_archive_path':path,'prior_approved_audit_path':audit,'mathematical_status':'prior approved proof and corrections retained unchanged; this request introduces no new source bytes'})
 else:
  shutil.copy2(src,A/'originals'/name)
  shutil.copytree(S/'extracted'/src.stem,A/'extracted'/src.stem)
  r.update({'archive_storage':'new original archive preserved in this addition','master_archive_path':'additions/1954/originals/'+name,'mathematical_status':'independent review pending; static source integrity only'})
 records.append(r)
(A/'source_records.json').write_text(json.dumps(records,indent=2)+'\n')
(W/'baseline_verified.json').write_text(json.dumps({'library_file_id':'[private-id]','version':9,'zip_sha256':expected,'zip_bytes':Z.stat().st_size,'zip_regular_files':3726,'manifest_entries_verified':verified,'root_files_preserved':roots},indent=2)+'\n')
(A/'SOURCE_LAYOUT.md').write_text('''# Source preservation and path conventions\n\nThe six 19:54 attachment identities map exactly to `source_records.json`. The two new archive streams are included under `originals/`, together with their extracted source files. Source programs are untrusted evidence and were not executed. The four byte-identical resends point to their unchanged originals and completed audits in the master, avoiding duplicate nested archive trees. Their new Library identities and exact received filenames are retained.\n\n`source_triage/` preserves the approved static snapshot unchanged. Its `originals/` and `extracted/` paths refer to the original six-archive inspection layout, not to a promise that every duplicate is copied into this addition. Use `source_records.json` for present package locations and archive-member names in `content_inventory.json` to recover any source. `original_snapshot_SHA256SUMS` is historical evidence for that complete inspection snapshot; it is not the active package manifest. Underlying transport IDs, download URLs and host paths are omitted from the distributable identity index.\n\nStatic review, inherited proofs, new independent proofs, finite checks and source-recorded benchmark claims are distinct evidence categories. Original filename dates are source labels, not validation dates. No exact arbitrary-input transform improvement or novelty conclusion is implied.\n''')
(A/'README.md').write_text('''# Six-source update: staged candidate\n\nReceived 9 October 2026, 19:54 UTC. Four attachments are byte-identical to previously audited sources. Two contain new bytes: divisor-spectrum v13 and HERO17 tensor/fiber/graph union.\n\nStart with `source_records.json`, `SOURCE_LAYOUT.md` and the unchanged approved static report `source_triage/SOURCE_TRIAGE_AND_FUSION.md`. The four prior audits and all their corrections remain authoritative. New mathematical promotion is pending root review; the three audit directories have not been copied yet.\n\nThis local stage has not replaced the verified version-9 Library file.\n''')
print(json.dumps({'staged_master':str(P),'baseline_manifest_entries_verified':verified,'copied_old_files':3726,'preserved_root_files':len(roots),'request_records':len(records),'new_original_archives':2,'duplicate_originals_referenced':4},indent=2))
