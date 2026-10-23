"""Data-only package integrity, never import or execute scientific programs."""
from pathlib import Path
import json,hashlib,zipfile,io
P=Path(__file__).parent
def sha(b):return hashlib.sha256(b).hexdigest()
def check(raw,a):
 assert len(raw)==a['bytes'] and sha(raw)==a['sha256'];z=zipfile.ZipFile(io.BytesIO(raw));assert z.testzip() is None;assert len(z.namelist())==len(set(z.namelist()))==len(a['members']);assert set(z.namelist())=={x['path'] for x in a['members']}
 for x in a['members']:
  b=z.read(x['path']);assert len(b)==x['bytes'] and sha(b)==x['sha256']
 return z
M=json.loads((P/'PUBLIC_MANIFEST.json').read_text());z=check((P/'evidence.zip').read_bytes(),M['archive'])
for x in M['projection']['source_correspondence']:
 b=z.read(x['archive_path']);assert x['public']=={'bytes':len(b),'sha256':sha(b)}
for x in M['projection']['historical_manifests']:
 b=z.read(x['archive_path']);assert len(b)==x['bytes'] and sha(b)==x['sha256'];m=json.loads(b);fs=m.get('files',m);fs={x['path']:{'bytes':x.get('bytes',x.get('size')),'sha256':x['sha256']} for x in fs} if isinstance(fs,list) else fs;label=x['archive_path'].rsplit('/',1)[0]
 for n,v in fs.items():
  original=next(a['original'] for a in M['projection']['source_correspondence'] if a['archive_path']==label+'/'+n);assert (original['sha256']==v if isinstance(v,str) else original==v)
d=json.loads(z.read('dependencies/support/PUBLIC_MANIFEST.json'));old=check(z.read('dependencies/support/evidence.zip'),d['archive'])
for x in M['direct_science_copies']:assert (P/x['path']).read_bytes()==z.read(x['archive_path'])
for x in M['direct_files']:
 b=(P/x['path']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256']
print(json.dumps({'verified':True,'source_entries':M['projection']['source_entries'],'archive_bytes':M['archive']['bytes'],'archive_members':len(z.namelist()),'nested_support_members':len(old.namelist()),'scientific_execution':False}))
