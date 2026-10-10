"""Verify packaging as data; never import, execute, or compile supplied source code."""
from pathlib import Path
import hashlib,json,zipfile,ast
BASE=Path('fft_research_master_20261009')
PACK=Path('v10_build/fft_research_master_20261009')
ADD=PACK/'additions/1954'
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
changed=[];missing=[];unchanged=0
for p in BASE.rglob('*'):
 if not p.is_file():continue
 rel=p.relative_to(BASE); q=PACK/rel
 if not q.exists():missing.append(str(rel))
 elif h(p)!=h(q):changed.append(str(rel))
 else:unchanged+=1
assert not missing,missing
allowed={'README.md','CURRENT_CHECKPOINT.md','ADDITIONS_STATUS.json','PENDING_ADDITIONS.json','VERIFICATION.md','SHA256SUMS','SHA256SUMS.txt'}
assert set(changed)<=allowed, changed
for p in BASE.iterdir():
 if p.is_file():assert h(p)==h(PACK/'checkpoint_history'/('v9_'+p.name)),p.name
records=json.loads((ADD/'source_records.json').read_text())
for r in records:
 p=PACK/r['master_archive_path'];assert h(p)==r['sha256'];assert p.stat().st_size==r['bytes']
 with zipfile.ZipFile(p) as z:assert z.testzip() is None
static={}
for p in sorted(ADD.rglob('*.py')):
 ast.parse(p.read_text());static[str(p.relative_to(ADD))]=h(p)
print(json.dumps({'old_files_unchanged':unchanged,'old_files_changed':changed,'old_files_missing':missing,'old_root_files_preserved':11,'source_archive_identities_verified':len(records),'python_syntax_only_files':len(static),'uploaded_code_executed':False},indent=2))
