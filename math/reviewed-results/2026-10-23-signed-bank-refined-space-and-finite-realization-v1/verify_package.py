"""Byte integrity only. No research program is executed."""
from pathlib import Path
import json,hashlib,zipfile,io
P=Path(__file__).parent
def sha(b):return hashlib.sha256(b).hexdigest()
def check(raw,m):
 assert len(raw)==m['bytes'] and sha(raw)==m['sha256'];z=zipfile.ZipFile(io.BytesIO(raw));assert z.testzip() is None;assert len(z.namelist())==len(set(z.namelist()))==len(m['members']);assert set(z.namelist())=={x['path'] for x in m['members']}
 for x in m['members']:
  b=z.read(x['path']);assert len(b)==x['bytes'] and sha(b)==x['sha256']
 return z
def maps(z,m):
 for x in m['projection']['source_correspondence']:
  if x['public'] is None:assert x['archive_path'] not in z.namelist();continue
  b=z.read(x['archive_path']);assert x['public']=={'bytes':len(b),'sha256':sha(b)}
M=json.loads((P/'PUBLIC_MANIFEST.json').read_text());raw=b''.join((P/x['path']).read_bytes() for x in M['archive']['parts']);z=check(raw,M['archive']);maps(z,M)
for x in M['archive']['parts']:
 b=(P/x['path']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256'] and raw[x['offset']:x['offset']+len(b)]==b
for x in M['projection']['historical_manifests']:
 b=z.read(x['archive_path']);assert len(b)==x['bytes'] and sha(b)==x['sha256'];d=json.loads(b);v=d.get('members',d.get('files',d));fs={a.get('path',a.get('name',a.get('file'))):{'bytes':a.get('bytes',a.get('size')),'sha256':a['sha256']} for a in v} if isinstance(v,list) else v;label=x['archive_path'].rsplit('/',1)[0]
 for n,v in fs.items():
  o=next(a['original'] for a in M['projection']['source_correspondence'] if a['archive_path']==label+'/'+n);assert o['sha256']==v if isinstance(v,str) else o==v
nested=[];parent=z
for dep in ['dependencies/cubic','dependencies/quartic','dependencies/support']:
 m=json.loads(parent.read(dep+'/PUBLIC_MANIFEST.json'));parent=check(parent.read(dep+'/evidence.zip'),m['archive']);maps(parent,m);nested.append(len(parent.namelist()))
for x in M['direct_science_copies']:assert (P/x['path']).read_bytes()==z.read(x['archive_path'])
for x in M['direct_files']:
 b=(P/x['path']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256']
b=z.read('finite_author/RESOLVENT_INVERSES.u8');assert len(b)==4828736 and sha(b)=='6b3852380804f9a1a7d1f9f343af06b11f1dd2edc141f5e2f2e8c92213435bd6'
print(json.dumps({'verified':True,'archive_bytes':len(raw),'members':len(z.namelist()),'original_source_entries':71,'published_source_entries':69,'nested_members':nested,'exact_inverse_bytes':len(b),'research_code_executed':False}))
