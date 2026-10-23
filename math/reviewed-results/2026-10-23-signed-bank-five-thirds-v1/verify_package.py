from pathlib import Path
import json,hashlib,zipfile
H=Path(__file__).parent;m=json.loads((H/'PUBLIC_MANIFEST.json').read_text());sha=lambda b:hashlib.sha256(b).hexdigest();a=m['archive'];b=(H/a['path']).read_bytes();assert len(b)==a['bytes'] and sha(b)==a['sha256']
with zipfile.ZipFile(H/a['path']) as z:
 assert len(z.namelist())==len(set(z.namelist()))==len(a['members']);assert set(z.namelist())=={x['path'] for x in a['members']}
 for x in a['members']:
  b=z.read(x['path']);assert len(b)==x['bytes'] and sha(b)==x['sha256']
 for x in m['projection']['source_correspondence']:
  b=z.read(x['archive_path']);assert len(b)==x['public']['bytes'] and sha(b)==x['public']['sha256']
 for x in m['direct_readable']:assert (H/x['path']).read_bytes()==z.read(x['archive_path'])
print(json.dumps({'status':'PASS','members':len(a['members']),'source_entries':m['projection']['source_entries'],'scientific_programs_executed':False}))
