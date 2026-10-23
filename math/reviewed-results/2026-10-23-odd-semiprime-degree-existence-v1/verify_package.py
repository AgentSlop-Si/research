"""Data-only integrity checker; never execute scientific programs."""
from pathlib import Path
import json,hashlib,zipfile,io
P=Path(__file__).parent
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(b):return {'bytes':len(b),'sha256':sha(b)}
M=json.loads((P/'PUBLIC_MANIFEST.json').read_text());b=(P/'evidence.zip').read_bytes();assert pin(b)=={k:M['archive'][k] for k in ['bytes','sha256']};z=zipfile.ZipFile(io.BytesIO(b));assert z.testzip() is None
assert len(z.namelist())==len(set(z.namelist()))==len(M['archive']['members'])
assert set(z.namelist())=={x['path'] for x in M['archive']['members']}
for x in M['archive']['members']:assert pin(z.read(x['path']))=={k:x[k] for k in ['bytes','sha256']}
maps={x['archive_path']:x for x in M['projection']['source_correspondence']}
for n,x in maps.items():assert pin(z.read(n))==x['public']
for x in M['projection']['historical_manifests']:
 b=z.read(x['archive_path']);assert pin(b)=={k:x[k] for k in ['bytes','sha256']};m=json.loads(b);label=x['archive_path'].rsplit('/',1)[0]
 for f in m.get('files',m.get('members',[])):assert maps[label+'/'+f['path']]['original']=={'bytes':f.get('bytes',f.get('size')),'sha256':f['sha256']}
for x in M['direct_science_copies']:assert (P/x['path']).read_bytes()==z.read(x['archive_path'])
for x in M['direct_files']:assert pin((P/x['path']).read_bytes())=={k:x[k] for k in ['bytes','sha256']}
print(json.dumps({'verified':True,'archive_bytes':M['archive']['bytes'],'archive_members':len(z.namelist()),'source_entries':len(maps),'scientific_execution':False}))
