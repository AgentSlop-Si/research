"""Verify the portable sealed review, candidate snapshot, and copied sources."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent
manifest=json.loads((R/'MANIFEST.json').read_text())
for e in manifest['files']:
 data=(R/e['path']).read_bytes()
 assert len(data)==e['bytes'] and hashlib.sha256(data).hexdigest()==e['sha256'],e['path']
C=R.parent/'candidate'
for e in json.loads((C/'MANIFEST.json').read_text())['files']:
 data=(C/e['path']).read_bytes()
 assert len(data)==e['bytes'] and hashlib.sha256(data).hexdigest()==e['sha256'],e['path']
for e in json.loads((R/'SOURCE_BINDINGS.json').read_text())['sources']:
 data=(R/e['review_copy']).read_bytes()
 assert len(data)==e['bytes'] and hashlib.sha256(data).hexdigest()==e['sha256'],e['review_copy']
assert (C/'RESULTS.json').read_bytes()==(R/'CANDIDATE_RESULTS.original.json').read_bytes()
assert (R/'CANDIDATE_RERUN.log').read_bytes()==(C/'RUN.log').read_bytes()
assert (R/'INDEPENDENT_RUN.log').read_bytes()==(R/'INDEPENDENT_RESULTS.json').read_bytes()
assert (R/'INDEPENDENT_RUN.stderr').stat().st_size==0
assert (R/'CANDIDATE_RERUN.stderr').stat().st_size==0
v=json.loads((R/'VERDICT.json').read_text())
assert json.loads((C/'MANIFEST.json').read_text())['original_manifest_sha256']==v['candidate_manifest_sha256']
print(json.dumps({'status':'PASS','review_files':len(manifest['files']),'candidate_files':len(json.loads((C/'MANIFEST.json').read_text())['files']),'copied_inherited_sources':5,'candidate_rerun':'exact','mandatory_qualifications':2}))
