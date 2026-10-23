"""Public package-integrity checks only; no scientific code execution."""
from pathlib import Path
import hashlib,json,zipfile,io
P=Path(__file__).parent
def sha(b):return hashlib.sha256(b).hexdigest()
def check(raw,m):
 assert len(raw)==m['bytes'] and sha(raw)==m['sha256'];z=zipfile.ZipFile(io.BytesIO(raw));assert z.testzip() is None;assert len(z.namelist())==len(set(z.namelist()))==len(m['members']);assert set(z.namelist())=={x['path'] for x in m['members']}
 for x in m['members']:
  b=z.read(x['path']);assert len(b)==x['bytes'] and sha(b)==x['sha256']
 return z
def maps(z,m):
 for x in m['projection']['source_correspondence']:
  b=z.read(x['archive_path']);assert x['public']=={'bytes':len(b),'sha256':sha(b)}
M=json.loads((P/'PUBLIC_MANIFEST.json').read_text());raw=b''.join((P/x['path']).read_bytes() for x in M['archive']['parts']);z=check(raw,M['archive']);maps(z,M)
for x in M['archive']['parts']:
 b=(P/x['path']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256'] and raw[x['offset']:x['offset']+len(b)]==b
for x in M['projection']['historical_manifests']:
 b=z.read(x['archive_path']);assert len(b)==x['bytes'] and sha(b)==x['sha256'];d=json.loads(b);v=d.get('members',d.get('files',d));fs={a['path']:{'bytes':a.get('bytes',a.get('size')),'sha256':a['sha256']} for a in v} if isinstance(v,list) else v;label=x['archive_path'].rsplit('/',1)[0]
 for n,v in fs.items():
  original=next(a['original'] for a in M['projection']['source_correspondence'] if a['archive_path']==label+'/'+n);assert (original['sha256']==v if isinstance(v,str) else original==v)
sm=json.loads(z.read('dependencies/sparse/PUBLIC_MANIFEST.json'));sz=check(z.read('dependencies/sparse/evidence.zip'),sm['archive']);maps(sz,sm)
om=json.loads(sz.read('dependencies/odd_middle/PUBLIC_MANIFEST.json'));oz=check(sz.read('dependencies/odd_middle/evidence.zip'),om['archive']);maps(oz,om)
for x in M['direct_science_copies']:assert (P/x['path']).read_bytes()==z.read(x['archive_path'])
for x in M['direct_files']:
 b=(P/x['path']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256']
print(json.dumps({'verified':True,'archive_bytes':len(raw),'members':len(z.namelist()),'source_entries':len(M['projection']['source_correspondence']),'nested_sparse_members':len(sz.namelist()),'nested_single_middle_members':len(oz.namelist()),'research_code_executed':False}))
