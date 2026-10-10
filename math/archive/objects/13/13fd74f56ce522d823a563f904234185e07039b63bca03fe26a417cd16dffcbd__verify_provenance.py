#!/usr/bin/env python3
"""Read ZIPs as inert bytes; never execute or import archive members."""
from pathlib import Path
import hashlib,json,zipfile
root=Path(__file__).resolve().parent
expected={
 'offset_class_v12_original.zip':'89b05db6afc7e0e868cf647a08aaae18dc0baab6b3ed10ed28bf30e91cc82978',
 'v9_prior_original.zip':'4fb1574ed84c3beb1a3a4f33f116b139952ba9452495815cf47573d79a2aa5e4',
 'v11_prior_original.zip':'cea5b07e13545b38db58655e68cca1617e2f172ce9ba20b88d33c37963544e31'}
zips={}
for name,digest in expected.items():
 p=root/'sources'/name
 assert hashlib.sha256(p.read_bytes()).hexdigest()==digest,name
 z=zipfile.ZipFile(p);assert z.testzip() is None,name;zips[name]=z
v12=zips['offset_class_v12_original.zip'];v9=zips['v9_prior_original.zip'];v11=zips['v11_prior_original.zip']
manifest=next(n for n in v12.namelist() if n.endswith('/MANIFEST.sha256'))
prefix=manifest.rsplit('/',1)[0]+'/'
checked=0
for line in v12.read(manifest).decode().splitlines():
 digest,path=line.split(None,1);path=path.lstrip('*')
 assert hashlib.sha256(v12.read(prefix+path)).hexdigest()==digest,path
 checked+=1
core=v12.read(prefix+'unit_step_core.py')
assert core==v9.read('fft_unit_step_chirp_v9/prototype.py')
assert core==v11.read('fft_all_length_fused_fp_v11/unit_step_core.py')
assert v12.read(prefix+'v11_fused_reference.py')==v11.read('fft_all_length_fused_fp_v11/prototype.py')
print(json.dumps({'status':'PASS','archive_hashes':expected,'embedded_v12_manifest_entries':checked,
 'core_present_in_exact_prior_v11_archive':True,'v12_core_equals_prior_v9_and_v11':True,
 'v12_reference_equals_prior_v11_prototype':True,'uploaded_code_executed':False},indent=2))
