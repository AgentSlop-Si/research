from pathlib import Path
import hashlib,json
r=Path(__file__).resolve().parent;m=json.loads((r/'SEALED_MANIFEST.json').read_text())
for f,h in m['files'].items():assert hashlib.sha256((r/f).read_bytes()).hexdigest()==h,f
print('SEALED FILES PASS:',len(m['files']))
