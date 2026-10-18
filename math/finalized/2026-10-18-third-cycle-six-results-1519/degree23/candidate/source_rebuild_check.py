#!/usr/bin/env python3
"""Check pinned input bytes, exact adaptation, canonical candidate and PRNG replay."""
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
names=['search_degree23.cpp','verify_literal.cpp','independent_literal_check.py','field_verify.py','search_field.py']
with tempfile.TemporaryDirectory(prefix='degree23-source-rebuild-') as td:
 p=Path(td);shutil.copytree(R/'sources',p/'sources');shutil.copy2(R/'adapt_source.py',p/'adapt_source.py')
 subprocess.run([sys.executable,'-I','adapt_source.py'],cwd=p,check=True)
 for n in names:assert (p/n).read_bytes()==(R/n).read_bytes()
 subprocess.run([sys.executable,'-I','search_field.py'],cwd=p,check=True,capture_output=True)
 assert (p/'FIELD_SEARCH.json').read_bytes()==(R/'FIELD_SEARCH.json').read_bytes()
v=json.loads((R/'NONSTABLE_CANDIDATE.json').read_text());a=lambda v:'{'+','.join(map(str,v))+'}'
header='static const int INPUT_Y[D]='+a(v['y'])+';\nstatic const int INPUT_H[8][D]={'+','.join(a(x) for x in v['H'])+'};\n'
assert header==(R/'candidate_data.h').read_text()
certificate=json.loads((R/'DEGREE23_LITERAL_CERTIFICATE.json').read_text());assert certificate['y']==v['y'] and certificate['H']==v['H']
seed=202610181502;mask=(1<<64)-1;nonzero=zero=0
while nonzero<=v['trial']:
 coords=[]
 for i in range(23):
  seed^=(seed<<13)&mask;seed^=seed>>7;seed^=(seed<<17)&mask;coords.append(seed%53)
 if not any(coords):zero+=1;continue
 nonzero+=1
assert coords==v['y']
# Only PRNG state remains uint64_t; all field order/exponent call paths are Big.
s=(R/'search_degree23.cpp').read_text();t=(R/'verify_literal.cpp').read_text()
assert 'using Big=mpz_class;' in s and 'const Big ORDER=' in s
assert '__uint128' not in s+t and '__int128' not in s+t
for token in ['F power(Big e)','Poly powmod(Poly x,Big e','power(ORDER-2)','powmod({F(0),F(1)},ORDER,h)','d.power((ORDER+3)/8)']:assert token in s
assert 'powmod(r,(ORDER-1)/2,h)' in t
receipt={'verdict':'PASS','source_pins_checked':len(pins),'adaptation_byte_identical':{n:sha(R/n) for n in names},'modulus_search_byte_identical':True,'header_and_candidate_json_bound':True,'certificate_and_candidate_json_bound':True,'order_power_inverse_split_sqrt_factor_use_unbounded_Big':True,'independent_prng_replay':{'nonzero_cross_nodes':nonzero,'zero_cross_nodes_skipped':zero,'coordinate_draws':(nonzero+zero)*23,'hit_cross_node_matches':True}}
(R/'SOURCE_REBUILD_CHECK.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
