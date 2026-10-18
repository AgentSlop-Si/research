"""Verify source and package integrity without running the scientific program."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
m=json.loads((ROOT/'MANIFEST.json').read_text())
for r in m['files']:
 b=(ROOT/r['path']).read_bytes()
 assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],r['path']
for r in json.loads((ROOT/'SOURCE_BINDINGS.json').read_text()):
 b=(ROOT/r['local_file']).read_bytes()
 assert hashlib.sha256(b).hexdigest()==r['local_sha256']
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['git_blob_sha']
c=json.loads((ROOT/'CHECK_RESULTS.json').read_text())
assert c['source_sha256']==hashlib.sha256((ROOT/'dense_dispatch.py').read_bytes()).hexdigest()
assert c['checks_sha256']==hashlib.sha256((ROOT/'fresh_checks.py').read_bytes()).hexdigest()
assert c['status']=='PASS_FRESH_BOUNDED_REFERENCE_CONTROLS'
print(json.dumps({'status':'PASS_INTEGRITY_ONLY','files':len(m['files']),
                  'source_blobs':9,'scientific_tests_rerun':False},sort_keys=True))
