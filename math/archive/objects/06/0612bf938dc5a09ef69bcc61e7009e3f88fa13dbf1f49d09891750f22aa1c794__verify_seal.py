from pathlib import Path
import json,hashlib
D=Path(__file__).resolve().parent
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
expected=(D/'SEALED_MANIFEST.sha256').read_text().split()[0]
assert h(D/'SEALED_MANIFEST.json')==expected
m=json.loads((D/'SEALED_MANIFEST.json').read_text())
for row in m['files']:
    p=D/row['path'];assert len(p.read_bytes())==row['bytes'] and h(p)==row['sha256'],str(p)
sources=json.loads((D/'SOURCE_MANIFEST.json').read_text())
for row in sources:
    assert h(Path(row['absolute_path']))==row['sha256'],row['absolute_path']
    assert h(D/row['snapshot_path'])==row['sha256'],row['snapshot_path']
c=json.loads((D/'COVERAGE.json').read_text())
assert c['completed_rows']==40 and c['completed_bytes']==648428
assert [r['queue_index'] for r in c['rows']]==list(range(40))
assert all(r['inspection']=='complete_text_read' and r['read_evidence']['complete_character_coverage'] for r in c['rows'])
print('PASS: sealed report files and all 40 original/snapshot source hashes; 648428 bytes; exact assigned rows0–39.')
