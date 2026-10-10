#!/usr/bin/env python3
"""Data-only integrity checks. No uploaded Python is imported or executed."""
from pathlib import Path
import hashlib,json,zipfile
H=Path(__file__).resolve().parent
S=H/'extracted'/'fft_hero0_phase10_learned_rational'
def digest(b): return hashlib.sha256(b).hexdigest()
records=[]
for name,meta in json.loads((S/'SHA256SUMS.json').read_text()).items():
    b=(S/name).read_bytes()
    assert len(b)==meta['bytes'] and digest(b)==meta['sha256'],name
    records.append({'file':name,'bytes':len(b),'sha256':digest(b)})
identities=json.loads((H/'SOURCE_IDENTITIES.json').read_text())
for item in identities:
    b=(H/'originals'/item['filename']).read_bytes()
    assert len(b)==item['bytes'] and digest(b)==item['sha256']
assert (H/'originals/THEOREMS.md').read_bytes()==(S/'THEOREMS.md').read_bytes()==(H/'THEOREMS.md').read_bytes()
prior=(S/'prior_phase9_bundle.zip').read_bytes()
assert prior==(H/'inherited_reference/prior_phase9_bundle.zip').read_bytes()
assert digest(prior)=='30de2a8cdef3d1d03f76b4bc271c9bbf993650e3dc88d464ee43fb6687a836ff'
with zipfile.ZipFile(H/'originals/fft_hero0_phase10_learned_rational_2026-10-10.zip') as z:
    members=0
    for i in z.infolist():
        if i.is_dir():continue
        p=Path(i.filename)
        assert not p.is_absolute() and '..' not in p.parts
        assert z.read(i)==(H/'extracted'/p).read_bytes()
        members+=1
out={'source_manifest_files_verified':len(records),'archive_members_verified':members,
     'text_byte_identical':True,'inherited_phase9_byte_identical':True,
     'inherited_phase9_sha256':digest(prior),'manifest_records':records,
     'uploaded_code_executed':False}
(H/'INTEGRITY_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='manifest_records'},indent=2))
