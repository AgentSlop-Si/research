from pathlib import Path
import json,hashlib,shutil
D=Path(__file__).resolve().parent;src=D.parent/'candidate';out=D/'input'/'candidate'
expected='45ccd9b65629ec16415750c341da7b4dbb086c770d0189b89c566cd224284ecc'
mb=(src/'MANIFEST.json').read_bytes();assert hashlib.sha256(mb).hexdigest()==expected
m=json.loads(mb);assert len(m['files'])==17
seen=set();total=0
for entry in m['files']:
 p=entry['path'];assert p not in seen and '..' not in Path(p).parts and not Path(p).is_absolute();seen.add(p)
 data=(src/p).read_bytes();assert len(data)==entry['bytes'] and hashlib.sha256(data).hexdigest()==entry['sha256']
 dest=out/p;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data);total+=len(data)
(out/'MANIFEST.json').write_bytes(mb)
assert total==715901
for n in ['COVERAGE_PRIMARY.jsonl','COVERAGE_CONJUGATE.jsonl']:assert (D/'input'/n).read_bytes()==(out/n).read_bytes()
for n in ['PROOF.md','REVIEW.md','CHART.json']:assert (D/'input'/'sources'/n).read_bytes()==(out/'sources'/n).read_bytes()
res={'status':'PASS','manifest_sha256':expected,'manifested_files':17,'manifested_bytes':total,'all_bound_inputs_match_independent_verification':True,'excluded_convenience_files':['certify_four','PILOT.jsonl','PILOT.log']}
(D/'FROZEN_CANDIDATE_BINDING.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res))
