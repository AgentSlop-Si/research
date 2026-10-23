"""Integrity only; never imports or executes scientific programs."""
from pathlib import Path
import json,hashlib,zipfile,io
P=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
M=json.loads((P/'PUBLIC_MANIFEST.json').read_text());parts=[]
for q in M['archive']['parts']:
 b=(P/q['path']).read_bytes();assert len(b)==q['bytes'] and sha(b)==q['sha256'];parts.append(b)
raw=b''.join(parts);assert len(raw)==M['archive']['bytes'] and sha(raw)==M['archive']['sha256']
with zipfile.ZipFile(io.BytesIO(raw)) as z:
 assert z.testzip() is None
 assert sorted(z.namelist())==sorted(q['path'] for q in M['archive']['members'])
 for q in M['archive']['members']:
  b=z.read(q['path']);assert len(b)==q['bytes'] and sha(b)==q['sha256']
 for q in M['source_manifests']:
  b=z.read(q['archive_path']);assert len(b)==q['bytes'] and sha(b)==q['sha256'];label=q['archive_path'].rsplit('/',1)[0]
  for name,v in json.loads(b).items():
   c=next(x for x in M['projection']['correspondence'] if x['archive_path']==label+'/'+name);assert c['original']==v
   b=z.read(label+'/'+name);assert c['public']=={'bytes':len(b),'sha256':sha(b)}
 for q in M['direct_science_copies']:assert (P/q['path']).read_bytes()==z.read(q['archive_path'])
for q in M['direct_files']:
 b=(P/q['path']).read_bytes();assert len(b)==q['bytes'] and sha(b)==q['sha256']
(P/'evidence.zip').write_bytes(raw)
print(json.dumps({'verified':True,'archive_bytes':len(raw),'members':len(M['archive']['members']),'source_entries':M['projection']['source_entries'],'exact':M['projection']['byte_exact_source_entries'],'projections':M['projection']['administrative_projected_source_entries'],'research_code_executed':False}))
