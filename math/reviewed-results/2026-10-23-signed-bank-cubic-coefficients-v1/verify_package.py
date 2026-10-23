"""Data-only recursive archive integrity. No scientific execution."""
from pathlib import Path
import json,hashlib,zipfile,io
P=Path(__file__).parent
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(b):return {'bytes':len(b),'sha256':sha(b)}
def check(raw,M):
 a=M['archive'];assert pin(raw)=={k:a[k] for k in ['bytes','sha256']};z=zipfile.ZipFile(io.BytesIO(raw));assert z.testzip() is None
 assert len(z.namelist())==len(set(z.namelist()))==len(a['members']);assert set(z.namelist())=={x['path'] for x in a['members']}
 for x in a['members']:assert pin(z.read(x['path']))=={k:x[k] for k in ['bytes','sha256']}
 return z
M=json.loads((P/'PUBLIC_MANIFEST.json').read_text());z=check((P/'evidence.zip').read_bytes(),M)
maps={x['archive_path']:x for x in M['projection']['source_correspondence']}
for n,x in maps.items():assert pin(z.read(n))==x['public']
for x in M['projection']['historical_manifests']:
 b=z.read(x['archive_path']);assert pin(b)=={k:x[k] for k in ['bytes','sha256']};m=json.loads(b);fs=m.get('files',m.get('members',m));label=x['archive_path'].rsplit('/',1)[0]
 if isinstance(fs,list):fs={a['path']:{'bytes':a.get('bytes',a.get('size')),'sha256':a['sha256']} for a in fs}
 for n,v in fs.items():
  o=maps[label+'/'+n]['original'];assert (o['sha256']==v if isinstance(v,str) else o==v)
qm=json.loads(z.read('dependencies/quartic/PUBLIC_MANIFEST.json'));q=check(z.read('dependencies/quartic/evidence.zip'),qm)
sm=json.loads(q.read('dependencies/support/PUBLIC_MANIFEST.json'));s=check(q.read('dependencies/support/evidence.zip'),sm)
for x in M['direct_science_copies']:assert (P/x['path']).read_bytes()==z.read(x['archive_path'])
for x in M['direct_files']:assert pin((P/x['path']).read_bytes())=={k:x[k] for k in ['bytes','sha256']}
print(json.dumps({'verified':True,'archive_bytes':M['archive']['bytes'],'archive_members':len(z.namelist()),'source_entries':len(maps),'nested_quartic_members':len(q.namelist()),'nested_support_members':len(s.namelist()),'scientific_execution':False}))
