#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
D=Path(__file__).resolve().parent
m=json.loads((D/'MANIFEST.json').read_text())
for p,h in m.items():
    assert hashlib.sha256((D/p).read_bytes()).hexdigest()==h,p
seal=json.loads((D/'SEAL.json').read_text())
assert hashlib.sha256((D/'MANIFEST.json').read_bytes()).hexdigest()==seal['manifest_sha256']
assert seal['members']==len(m)
print(json.dumps({'status':'PASS_LOCAL_PACKET_HASHES','members':len(m),'manifest_sha256':seal['manifest_sha256']},indent=2))
