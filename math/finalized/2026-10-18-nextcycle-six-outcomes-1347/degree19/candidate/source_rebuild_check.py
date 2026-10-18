#!/usr/bin/env python3
"""Check pinned bytes and replay the documented source adaptation in isolation."""
from pathlib import Path
import hashlib,json,shutil,subprocess,tempfile,sys
R=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
pins=json.loads((R/'SOURCE_PINS.json').read_text())
for rec in pins:
 p=R/rec['local_path'];b=p.read_bytes()
 assert len(b)==rec['bytes'] and sha(p)==rec['sha256']
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==rec['git_blob_sha']
 original=Path(rec['source_local_path'])
 if original.exists():assert b==original.read_bytes()
names=['search_degree19.cpp','verify_literal.cpp','independent_literal_check.py','field_verify.py']
with tempfile.TemporaryDirectory(prefix='degree19-source-rebuild-') as td:
 p=Path(td);shutil.copytree(R/'sources',p/'sources');shutil.copy2(R/'adapt_source.py',p/'adapt_source.py')
 subprocess.run([sys.executable,'-I','adapt_source.py'],cwd=p,check=True)
 for n in names:assert (p/n).read_bytes()==(R/n).read_bytes()
 shutil.copy2(R/'search_field.py',p/'search_field.py')
 subprocess.run([sys.executable,'-I','search_field.py'],cwd=p,check=True,capture_output=True)
 assert (p/'FIELD_SEARCH.json').read_bytes()==(R/'FIELD_SEARCH.json').read_bytes()
v=json.loads((R/'NONSTABLE_CANDIDATE.json').read_text());a=lambda v:'{'+','.join(map(str,v))+'}'
header='static const int INPUT_Y[D]='+a(v['y'])+';\nstatic const int INPUT_H[8][D]={'+','.join(a(x) for x in v['H'])+'};\n'
assert header==(R/'candidate_data.h').read_text()
certificate=json.loads((R/'DEGREE19_LITERAL_CERTIFICATE.json').read_text());assert certificate['y']==v['y'] and certificate['H']==v['H']
seed=202610181330;mask=(1<<64)-1;nonzero=zero=0
while nonzero<=v['trial']:
 coords=[]
 for i in range(19):
  seed^=(seed<<13)&mask;seed^=seed>>7;seed^=(seed<<17)&mask;coords.append(seed%53)
 if not any(coords):zero+=1;continue
 nonzero+=1
assert coords==v['y']
receipt={'verdict':'PASS','source_pins_checked':len(pins),'adaptation_byte_identical':{n:sha(R/n) for n in names},'modulus_search_byte_identical':True,'header_and_candidate_json_bound':True,'certificate_and_candidate_json_bound':True,'independent_prng_replay':{'nonzero_cross_nodes':nonzero,'zero_cross_nodes_skipped':zero,'coordinate_draws':(nonzero+zero)*19,'hit_cross_node_matches':True}}
(R/'SOURCE_REBUILD_CHECK.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
