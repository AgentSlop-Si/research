import json,hashlib,sys
from pathlib import Path
base=Path('material_extension_source_review_0500/worker_materials')
rows=json.loads((base/'ROWS.json').read_text())
start,end=map(int,sys.argv[1:])
parts=[]; records=[]
for i in range(start,end):
 r=rows[i]; b=Path(r['local_content']).read_bytes(); assert hashlib.sha256(b).hexdigest()==r['sha256']; assert len(b)==r['size_bytes']
 lines=b.decode('utf-8').splitlines()
 parts.append('\n===== SOURCE %d %s %s | %d bytes %d lines =====\n'%(i,r['sha256'],r['representative_path'],len(b),len(lines)))
 parts.extend('%4d %s\n'%(j,line) for j,line in enumerate(lines,1))
 records.append({'index':i,'sha256':r['sha256'],'bytes_half_open':[0,len(b)],'lines_inclusive':[1,len(lines)],'source_path':r['local_content']})
out=''.join(parts); name='READ_%02d_%02d.txt'%(start,end)
(base/name).write_text(out)
(base/(name+'.json')).write_text(json.dumps({'command':'python material_extension_source_review_0500/worker_materials/read_sources.py %d %d'%(start,end),'output_file':str(base/name),'output_sha256':hashlib.sha256(out.encode()).hexdigest(),'records':records},indent=2))
print(out,end='')
