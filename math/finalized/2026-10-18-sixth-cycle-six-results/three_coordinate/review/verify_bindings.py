"""Verify complete candidate freeze, nested manifests and exact source-byte relation."""
from pathlib import Path,PurePosixPath
import json,hashlib
R=Path(__file__).resolve().parent;C=R/'input'
expected='eb53d5009f728deb13fa55a2d467e43ce5a18249f0c4e32b3aa833633a6bb3cd'
b=(C/'FULL_MANIFEST.json').read_bytes();assert hashlib.sha256(b).hexdigest()==expected
m=json.loads(b);listed=set()
for q in m['files']:
 p=q['path'];P=PurePosixPath(p);assert not P.is_absolute()and '..'not in P.parts and p not in listed;listed.add(p)
 path=C/p;assert path.is_file()and not path.is_symlink();b=path.read_bytes();assert len(b)==q['bytes']and hashlib.sha256(b).hexdigest()==q['sha256']
actual={str(p.relative_to(C))for p in C.rglob('*')if p.is_file()and '__pycache__'not in p.parts}
assert actual==listed|{'FULL_MANIFEST.json'}
for mn,key in [('CORE_MANIFEST.json','core_manifest_sha256'),('OPTIONAL_CONTROLS_MANIFEST.json','optional_controls_manifest_sha256')]:
 b=(C/mn).read_bytes();assert hashlib.sha256(b).hexdigest()==m[key]
 for p,q in json.loads(b).items():
  b=(C/p).read_bytes();assert p in listed and len(b)==q['bytes']and hashlib.sha256(b).hexdigest()==q['sha256']
assert m['core_manifest_sha256']=='7116974db5eed031ad7fe5e4e907c2850c341bdc65cc2c7eb647527f544c93aa'
b=(C/'sources/FROZEN_REVIEW_ORIGINAL_BYTES.md').read_bytes();blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
assert blob=='0fb2b065b626d756850e0d5e9a2028b43bc06449'
assert (C/'sources/FROZEN_REVIEW.md').read_bytes()==b+b'\n'
report={'result':'PASS','candidate_full_manifest_sha256':expected,'candidate_core_manifest_sha256':m['core_manifest_sha256'],'optional_controls_manifest_sha256':m['optional_controls_manifest_sha256'],'manifested_files':len(listed),'complete_regular_file_coverage':True,'original_review_git_blob_sha1':blob,'core_review_is_original_plus_one_newline':True,'optional_controls_status':'Read and byte-bound; not required for the independently reconstructed proof and not independently replayed in this review.'}
(R/'FREEZE_BINDINGS.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
