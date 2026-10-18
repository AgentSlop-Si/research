from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
files=[]
for p in sorted(root.rglob('*')):
 if p.is_file() and p.name!='MANIFEST.json':
  b=p.read_bytes();files.append(dict(path=str(p.relative_to(root)),bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
(root/'MANIFEST.json').write_text(json.dumps(dict(owner='M-NONLINEAR-COMPATIBILITY',status='unresolved; exact encoding checked',files=files),indent=2)+'\n')
print('Bound',len(files),'files')
