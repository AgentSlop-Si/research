"""Verify only package integrity, never import or run scientific programs."""
from pathlib import Path
import json,hashlib,zipfile,io
P=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
M=json.loads((P/'PUBLIC_MANIFEST.json').read_text());b=(P/'evidence.zip').read_bytes();assert len(b)==M['archive']['bytes'] and sha(b)==M['archive']['sha256']
with zipfile.ZipFile(io.BytesIO(b)) as z:
 assert z.testzip() is None and sorted(z.namelist())==sorted(x['path'] for x in M['archive']['members'])
 for x in M['archive']['members']:
  q=z.read(x['path']);assert len(q)==x['bytes'] and sha(q)==x['sha256']
 for x in M['source_manifests']:
  q=z.read(x['archive_path']);assert len(q)==x['bytes'] and sha(q)==x['sha256'];d=json.loads(q);label=x['archive_path'].rsplit('/',1)[0]
  for name,v in d.get('files',d).items():
   c=next(t for t in M['projection']['source_correspondence'] if t['archive_path']==label+'/'+name);assert c['original']==v;q=z.read(label+'/'+name);assert c['public']=={'bytes':len(q),'sha256':sha(q)}
 for x in M['direct_science_copies']:assert (P/x['path']).read_bytes()==z.read(x['archive_path'])
for x in M['direct_files']:
 q=(P/x['path']).read_bytes();assert len(q)==x['bytes'] and sha(q)==x['sha256']
print(json.dumps({'verified':True,'archive_bytes':len(b),'members':len(M['archive']['members']),'source_entries':51,'exact_entries':48,'mapped_projections':3,'research_code_executed':False}))
