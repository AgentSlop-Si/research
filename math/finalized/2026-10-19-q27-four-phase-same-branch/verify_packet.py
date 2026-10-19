"""Read-only integrity verification of this complete public object."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
seal=json.loads((R/'PUBLICATION_SEAL.json').read_text())
mb=(R/'PUBLICATION_MANIFEST.json').read_bytes();assert sha(mb)==seal['manifest_sha256']
m=json.loads(mb);seen=set();total=0
for e in m['files']:
 p=Path(e['path']);assert not p.is_absolute() and '..' not in p.parts and e['path'] not in seen
 seen.add(e['path']);data=(R/p).read_bytes();assert len(data)==e['bytes'] and sha(data)==e['sha256'],e['path'];total+=len(data)
assert len(seen)==seal['manifested_files'] and total==seal['manifested_bytes']
for name,expected in [('candidate','45ccd9b65629ec16415750c341da7b4dbb086c770d0189b89c566cd224284ecc'),('review','4b18044f6c5d88f7e4fb19d3649820fb0d93363eee7074bf638bef1c7849140a')]:
 mb=(R/name/'MANIFEST.json').read_bytes();assert sha(mb)==expected
 for e in json.loads(mb)['files']:
  b=(R/name/e['path']).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256']
v=json.loads((R/'review/VERDICT.json').read_text());assert v['verdict']=='ACCEPT_NARROW' and v['proof_obligations']['Q_support_dimension']==126
owner=json.loads((R/'OWNER_DISPOSITION.json').read_text());assert owner['status']=='TO RESEARCH' and owner['priority']==50 and not owner['owner_closed']
assert owner['accepted_prior_three_coordinate_labels']==5984 and owner['accepted_new_four_coordinate_same_branch_labels']==280
print(json.dumps({'status':'PASS','manifested_files':len(seen),'manifested_bytes':total,'scientific_originals_preserved':True,'verdict':'ACCEPT_NARROW','owner_open':True,'priority':50}))
